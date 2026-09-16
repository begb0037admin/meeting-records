const OWNER = "begb0037admin";
const REPO = "meeting-records";
const BRANCH = "main";
const DEFINITIONS_PATH = "data/meeting-definitions.json";
const TONES = new Set(["update", "raise", "fyi", "decision-needed"]);
const STATUSES = new Set(["open", "carried", "resolved", "dismissed"]);

function headers(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };
}
function response(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: headers(origin),
  });
}
function safeOrigin(request, env) {
  const configured = env.ALLOWED_ORIGIN || new URL(request.url).origin;
  const origin = request.headers.get("Origin");
  return !origin || origin === configured ? configured : null;
}
function githubHeaders(env) {
  return {
    Authorization: `Bearer ${env.GITHUB_PAT}`,
    Accept: "application/vnd.github+json",
    "Content-Type": "application/json",
    "User-Agent": "meeting-prep-intake-worker",
  };
}
function decode(content) {
  return JSON.parse(atob(content.replace(/\n/g, "")));
}
function slug(title) {
  const value = title
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
  if (!value) throw new Error("Ad-hoc title must contain letters or numbers.");
  return value.slice(0, 80);
}
function intakePath(meeting) {
  return meeting.kind === "recurring"
    ? `intakes/${meeting.meetingId}/${meeting.date}.json`
    : `intakes/ad-hoc/${slug(meeting.title)}-${meeting.date}.json`;
}
function error(message, status = 400) {
  const e = new Error(message);
  e.status = status;
  return e;
}

export function validateIntake(input) {
  if (
    !input ||
    input.schemaVersion !== 1 ||
    !input.meeting ||
    !Array.isArray(input.items) ||
    input.items.length === 0
  )
    throw error("Invalid intake schema: at least one item is required.");
  const { meeting } = input;
  if (
    !/^\d{4}-\d{2}-\d{2}$/.test(meeting.date) ||
    !meeting.title?.trim() ||
    !["recurring", "ad-hoc"].includes(meeting.kind)
  )
    throw error("Meeting title, ISO date, and kind are required.");
  if (
    meeting.kind === "recurring" &&
    !/^[a-z0-9-]+$/.test(meeting.meetingId || "")
  )
    throw error("Recurring meetingId is invalid.");
  if (meeting.kind === "ad-hoc" && meeting.meetingId)
    throw error("Ad-hoc records cannot have a meetingId.");
  const ids = new Set();
  let prior = 0;
  for (const item of input.items) {
    if (!/^itm_[A-Za-z0-9_-]+$/.test(item.itemId || "") || ids.has(item.itemId))
      throw error("Every item needs one unique stable itemId.");
    ids.add(item.itemId);
    if (
      !Number.isInteger(item.position) ||
      item.position <= prior ||
      !Number.isInteger(item.priority) ||
      item.priority < 0
    )
      throw error(
        "Item positions must be ordered positive integers and priority must be a non-negative integer.",
      );
    prior = item.position;
    if (
      !item.title?.trim() ||
      !TONES.has(item.tone) ||
      typeof item.detail !== "string" ||
      typeof item.confirmedContext !== "string" ||
      typeof item.speakerNoteSeed !== "string" ||
      !STATUSES.has(item.status)
    )
      throw error("An item has missing or invalid fields.");
    if (!Array.isArray(item.sources))
      throw error("Item sources must be an array.");
    if (
      item.carryForward !== null &&
      item.carryForward !== undefined &&
      (!item.carryForward.fromIntake ||
        !item.carryForward.fromItemId ||
        !STATUSES.has(item.carryForward.disposition))
    )
      throw error("Invalid carry-forward reference.");
  }
  return {
    schemaVersion: 1,
    status: "submitted",
    meeting,
    items: input.items,
    submittedAt: new Date().toISOString(),
    submittedBy: input.submittedBy || "Kevin",
    ...(input.supersedes ? { supersedes: input.supersedes } : {}),
  };
}
async function gh(env, path, options = {}) {
  const r = await fetch(
    `https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}${options.ref ? `?ref=${encodeURIComponent(options.ref)}` : ""}`,
    { ...options, headers: githubHeaders(env) },
  );
  return r;
}
async function getJson(env, path) {
  const r = await gh(env, path, { ref: BRANCH });
  if (r.status === 404) return null;
  if (!r.ok) throw error(`GitHub read failed (${r.status}).`, 502);
  const v = await r.json();
  return { data: decode(v.content), sha: v.sha };
}
async function listPrevious(env, meetingId) {
  const r = await fetch(
    `https://api.github.com/repos/${OWNER}/${REPO}/git/trees/${BRANCH}?recursive=1`,
    { headers: githubHeaders(env) },
  );
  if (!r.ok) throw error(`GitHub tree read failed (${r.status}).`, 502);
  const tree = (await r.json()).tree || [];
  const paths = tree
    .filter(
      (x) =>
        x.type === "blob" &&
        x.path.startsWith(`intakes/${meetingId}/`) &&
        x.path.endsWith(".json"),
    )
    .map((x) => x.path);
  const records = [];
  for (const path of paths) {
    const loaded = await getJson(env, path);
    if (loaded?.data.status === "submitted")
      records.push({ path, record: loaded.data, sha: loaded.sha });
  }
  records.sort((a, b) =>
    b.record.submittedAt.localeCompare(a.record.submittedAt),
  );
  return records[0] || null;
}
export function eligibleCarryForward(previous) {
  if (!previous?.record) return [];
  return previous.record.items
    .filter((i) => i.status === "open" || i.status === "carried")
    .map((i) => ({
      ...i,
      itemId: `itm_${crypto.randomUUID().replaceAll("-", "")}`,
      status: "carried",
      carryForward: {
        fromIntake: previous.path,
        fromItemId: i.itemId,
        disposition: "carried",
      },
    }));
}
async function submit(env, input) {
  const record = validateIntake(input);
  const base = intakePath(record.meeting);
  let path = base;
  const existing = await getJson(env, path);
  if (existing) {
    if (!record.supersedes)
      throw error(
        "This intake is already locked. Submit a revision with an explicit supersedes reference.",
        409,
      );
    if (record.supersedes !== base)
      throw error(
        "A revision must explicitly supersede the existing locked intake path.",
      );
    if (input.expectedSha !== existing.sha)
      throw error(
        "The intake changed after this revision was opened. Reload it and submit a new revision; nothing was overwritten.",
        409,
      );
    path = base.replace(/\.json$/, `.revision-${Date.now()}.json`);
  }
  const body = {
    message: `Submit meeting intake: ${record.meeting.title} ${record.meeting.date}`,
    content: btoa(
      unescape(encodeURIComponent(JSON.stringify(record, null, 2))),
    ),
    branch: BRANCH,
  };
  const r = await gh(env, path, { method: "PUT", body: JSON.stringify(body) });
  if (r.status === 409 || r.status === 422)
    throw error(
      "GitHub rejected this write due to a conflict. Reload and submit a new explicit revision; nothing was overwritten.",
      409,
    );
  if (!r.ok) throw error(`GitHub write failed (${r.status}).`, 502);
  const out = await r.json();
  return { path, commitSha: out.commit.sha, record };
}

export default {
  async fetch(request, env) {
    const origin = safeOrigin(request, env);
    if (!origin)
      return response(
        403,
        { ok: false, error: "Forbidden origin." },
        env.ALLOWED_ORIGIN || new URL(request.url).origin,
      );
    if (request.method === "OPTIONS")
      return new Response(null, { status: 204, headers: headers(origin) });
    const url = new URL(request.url);
    if (!url.pathname.startsWith("/api/")) return env.ASSETS.fetch(request);
    if (request.method !== "POST")
      return response(405, { ok: false, error: "POST only." }, origin);
    if (!env.GITHUB_PAT)
      return response(
        500,
        { ok: false, error: "Worker secret GITHUB_PAT is not set." },
        origin,
      );
    try {
      const input = await request.json();
      if (url.pathname === "/api/meetings/list") {
        const defs = await getJson(env, DEFINITIONS_PATH);
        return response(
          200,
          {
            ok: true,
            meetings: (defs?.data.meetings || []).filter((m) => m.active),
          },
          origin,
        );
      }
      if (url.pathname === "/api/intakes/previous") {
        if (!/^[a-z0-9-]+$/.test(input.meetingId || ""))
          throw error("Invalid meetingId.");
        const previous = await listPrevious(env, input.meetingId);
        return response(
          200,
          {
            ok: true,
            latest: previous?.record || null,
            latestPath: previous?.path || null,
            latestSha: previous?.sha || null,
            eligibleCarryForward: eligibleCarryForward(previous),
          },
          origin,
        );
      }
      if (url.pathname === "/api/intakes/submit")
        return response(
          201,
          { ok: true, ...(await submit(env, input)) },
          origin,
        );
      if (
        [
          "/api/extract",
          "/api/chat",
          "/api/voice/stt",
          "/api/voice/tts",
          "/api/speaker-notes/candidate",
        ].includes(url.pathname)
      )
        return response(
          501,
          { ok: false, error: "Not yet implemented; this is a later phase." },
          origin,
        );
      return response(404, { ok: false, error: "Unknown API route." }, origin);
    } catch (e) {
      return response(
        e.status || 500,
        { ok: false, error: e.message || "Unexpected error." },
        origin,
      );
    }
  },
};
