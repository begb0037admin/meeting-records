"""Poll for an on-demand HR Systems Roadmap pull request and process it.

Kevin explicitly rejected a silent unattended Thursday-morning schedule for
this feature (16 Sep 2026 follow-up) -- he wants to trigger the roadmap pull
himself from the browser ("Pull roadmap now" button) with visible pass/fail
feedback, and never a silent hang. This script is the deterministic,
no-LLM-in-the-loop worker side of that: run frequently (Windows Task
Scheduler, every 1-2 minutes -- see desktop-scripts/Register-HRRoadmapPoll.ps1),
it asks the Worker whether a pull has been requested
(POST /api/intakes/pull-claim, secret-gated -- atomically claims the request
so a second poller tick, or a second machine, never double-processes it), and
if so runs the exact same extraction logic as a manual run
(extract_hr_roadmap_pending.compute_payload / post_with_retry) and reports
success or failure back (POST /api/intakes/pull-complete) so the browser's
status indicator can show it. If nothing has been requested, this exits
quickly and quietly -- most invocations do nothing, by design, since it's
running every 1-2 minutes regardless of whether Kevin has clicked the button.

If this script (or the scheduled task running it) is not running at all, the
button's own client-side 5-minute timeout in the browser is what keeps Kevin
from being stuck watching "Pulling..." forever -- this script never needs to
be the only thing standing between him and visibility.
"""
import json, os, sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from extract_hr_roadmap_pending import MEETING_ID, USER_AGENT, WORKER_URL, compute_payload, log, post_with_retry

BASE = "https://meeting.lelitte.co.uk"
CLAIM_URL = f"{BASE}/api/intakes/pull-claim"
COMPLETE_URL = f"{BASE}/api/intakes/pull-complete"


def call(url, payload, secret):
    request = Request(
        url,
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json", "X-Automation-Secret": secret, "User-Agent": USER_AGENT},
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def report_failure(secret, message):
    try:
        call(COMPLETE_URL, {"meetingId": MEETING_ID, "status": "failed", "error": message[:500]}, secret)
    except (HTTPError, URLError, OSError) as exc:
        log(f"Also failed to report the failure back to the Worker: {exc}")


def main():
    secret = os.environ.get("MEETING_PREP_PENDING_SECRET")
    if not secret:
        log("MEETING_PREP_PENDING_SECRET is not set.")
        return 1

    try:
        claim = call(CLAIM_URL, {"meetingId": MEETING_ID}, secret)
    except (HTTPError, URLError, OSError) as exc:
        # A real network failure here just means this tick did nothing; the
        # button's own 5-minute client-side timeout is what protects Kevin from
        # an indefinite silent hang if this keeps failing.
        log(f"Claim check failed: {exc}")
        return 1

    if not claim.get("claimed"):
        return 0  # nothing requested this tick -- the common case, exit quietly

    log("Claimed a pending pull request -- running extraction.")
    try:
        payload = compute_payload()
    except Exception as exc:
        log(f"Extraction failed: {exc}")
        report_failure(secret, str(exc))
        return 1

    try:
        post_with_retry(WORKER_URL, payload, secret)
    except Exception as exc:
        log(f"Failed to write the pending draft: {exc}")
        report_failure(secret, str(exc))
        return 1

    try:
        call(
            COMPLETE_URL,
            {"meetingId": MEETING_ID, "status": "done", "itemCount": len(payload["items"]), "date": payload["date"]},
            secret,
        )
    except (HTTPError, URLError, OSError) as exc:
        # The draft itself is safely written either way -- only the success
        # notification failed to land. The button will show a timeout rather
        # than a false failure; acceptable degraded behaviour, not silent.
        log(f"Wrote the draft but failed to report success: {exc}")
        return 1

    log(f"Done: {len(payload['items'])} item(s) for {payload['date']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
