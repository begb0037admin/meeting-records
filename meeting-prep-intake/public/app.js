const $ = (s, root = document) => root.querySelector(s);
const items = $("#items");
let definitions = [];
let dragged = null;
const today = new Date().toISOString().slice(0, 10);
$("#meetingDate").value = today;
const uid = () =>
  `itm_${new Date().toISOString().slice(0, 10).replaceAll("-", "")}_${crypto.randomUUID().replaceAll("-", "").slice(0, 12)}`;
function message(el, text, ok = false) {
  el.textContent = text;
  el.className = `message ${ok ? "ok" : "error"}`;
}
function renderNumbers() {
  [...items.children].forEach(
    (el, i) => ($(".item-number", el).textContent = `Item ${i + 1}`),
  );
}
function addItem(data = {}) {
  const el = $("#itemTemplate").content.firstElementChild.cloneNode(true);
  el.dataset.itemId = data.itemId || uid();
  $(".title", el).value = data.title || "";
  $(".tone", el).value = data.tone || "update";
  $(".priority", el).value = data.priority ?? 1;
  $(".detail", el).value = data.detail || "";
  $(".context", el).value = data.confirmedContext || "";
  $(".seed", el).value = data.speakerNoteSeed || "";
  if (data.carryForward) {
    $(".carry", el).textContent =
      `Carry-forward from ${data.carryForward.fromIntake} (${data.carryForward.fromItemId}); choose carried, resolved, or dismissed.`;
    const status = document.createElement("select");
    status.className = "status";
    status.innerHTML =
      '<option value="carried">Carried</option><option value="resolved">Resolved</option><option value="dismissed">Dismissed</option>';
    status.value = data.status || "carried";
    $(".carry", el).append(" ", status);
    el.dataset.carry = JSON.stringify(data.carryForward);
  } else {
    el.dataset.carry = "";
  }
  $(".remove", el).onclick = () => {
    el.remove();
    renderNumbers();
  };
  el.addEventListener("dragstart", () => {
    dragged = el;
    el.classList.add("dragging");
  });
  el.addEventListener("dragend", () => el.classList.remove("dragging"));
  el.addEventListener("dragover", (e) => {
    e.preventDefault();
    const target = e.currentTarget;
    if (dragged && dragged !== target) {
      const before =
        e.clientY <
        target.getBoundingClientRect().top + target.offsetHeight / 2;
      items.insertBefore(dragged, before ? target : target.nextSibling);
      renderNumbers();
    }
  });
  items.append(el);
  renderNumbers();
}
async function api(path, body = {}) {
  const r = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || "Request failed");
  return data;
}
async function loadMeetings() {
  try {
    const data = await api("/api/meetings/list");
    definitions = data.meetings;
    for (const m of definitions) {
      const o = document.createElement("option");
      o.value = m.meetingId;
      o.textContent = m.displayName;
      $("#meetingSelect").append(o);
    }
  } catch (e) {
    message($("#meetingMessage"), e.message);
  }
}
$("#meetingSelect").addEventListener("change", async (e) => {
  if (!e.target.value) return;
  $("#adHocTitle").value = "";
  try {
    const data = await api("/api/intakes/previous", {
      meetingId: e.target.value,
    });
    for (const item of data.eligibleCarryForward || []) addItem(item);
    if (data.eligibleCarryForward?.length)
      message(
        $("#meetingMessage"),
        "Eligible prior items added. Review each disposition.",
        true,
      );
  } catch (err) {
    message($("#meetingMessage"), err.message);
  }
});
$("#newRecurring").onclick = () => {
  const title = $("#adHocTitle").value.trim();
  if (!title)
    return message($("#meetingMessage"), "Enter an ad-hoc title first.");
  message(
    $("#meetingMessage"),
    "Creating recurring definitions is an explicit follow-up admin action; Phase 1 does not write definitions from the browser. Use the versioned definitions file, then select it here.",
  );
};
$("#addItem").onclick = () => addItem();
$("#submit").onclick = async () => {
  const meetingId = $("#meetingSelect").value;
  const title = (
    meetingId
      ? definitions.find((m) => m.meetingId === meetingId)?.displayName
      : $("#adHocTitle").value
  ).trim();
  const date = $("#meetingDate").value;
  if (!title || !date)
    return message(
      $("#submitMessage"),
      "Select a recurring meeting or enter an ad-hoc title, and set a date.",
    );
  const draft = [...items.children]
    .map((el, index) => ({
      itemId: el.dataset.itemId,
      position: index + 1,
      priority: Number($(".priority", el).value),
      title: $(".title", el).value.trim(),
      tone: $(".tone", el).value,
      detail: $(".detail", el).value,
      confirmedContext: $(".context", el).value,
      speakerNoteSeed: $(".seed", el).value,
      status: $(".status", el)?.value || "open",
      sources: [],
      carryForward: el.dataset.carry
        ? {
            ...JSON.parse(el.dataset.carry),
            disposition: $(".status", el).value,
          }
        : null,
    }))
    .filter((x) => x.status !== "dismissed");
  try {
    const data = await api("/api/intakes/submit", {
      schemaVersion: 1,
      meeting: {
        meetingId: meetingId || null,
        title,
        date,
        kind: meetingId ? "recurring" : "ad-hoc",
      },
      items: draft,
      submittedBy: "Kevin",
    });
    message(
      $("#submitMessage"),
      `Locked intake submitted: ${data.path} (commit ${data.commitSha})`,
      true,
    );
    $("#submit").disabled = true;
  } catch (e) {
    message($("#submitMessage"), e.message);
  }
};
loadMeetings();
addItem();
