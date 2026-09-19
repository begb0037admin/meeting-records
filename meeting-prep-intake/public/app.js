const $ = (s, root = document) => root.querySelector(s);
const items = $("#items");
let definitions = [];
let dragged = null;
let assistantBodyCounter = 0;
$("#meetingDate").value = new Date().toISOString().slice(0, 10);
const uid = () => `itm_${new Date().toISOString().slice(0, 10).replaceAll("-", "")}_${crypto.randomUUID().replaceAll("-", "").slice(0, 12)}`;
// Session scope restores accidental refreshes, but does not carry chat into the next intake.
let draftId = sessionStorage.getItem("meetingPrepDraftId");
if (!draftId) { draftId = `draft_${crypto.randomUUID().replaceAll("-", "")}`; sessionStorage.setItem("meetingPrepDraftId", draftId); }
const resetDraft = () => { draftId = `draft_${crypto.randomUUID().replaceAll("-", "")}`; sessionStorage.setItem("meetingPrepDraftId", draftId); };
function message(el, text, ok = false) { el.textContent = text; el.classList.add("message"); el.classList.remove("ok", "error"); el.classList.add(ok ? "ok" : "error"); }
function renderNumbers() { [...items.children].forEach((el, i) => ($(".item-number", el).textContent = `Item ${i + 1}`)); }
const toneLabels = { update: "🔄 Update", raise: "🚩 Raise", fyi: "ℹ️ FYI", "decision-needed": "⚖️ Decision needed" };
const tonePillClasses = { update: "pill-blue", raise: "pill-coral", fyi: "pill-teal", "decision-needed": "pill-amber" };
function renderTone(el) { const tone = $(".tone", el).value; const pill = $(".tone-pill", el); pill.className = `tone-pill pill ${tonePillClasses[tone]}`; pill.textContent = toneLabels[tone]; }
async function api(path, body = {}, opts = {}) {
  const r = await fetch(path, { method: "POST", headers: opts.headers || { "Content-Type": "application/json" }, body: opts.body || JSON.stringify(body) });
  if (!r.ok) { let data = {}; try { data = await r.json(); } catch {} throw new Error(data.error || "Request failed"); }
  return opts.raw ? r : r.json();
}
function chatLine(el, text, kind) { const p = document.createElement("p"); p.className = `chat-line ${kind}`; p.textContent = text; $(".chat-messages", el).append(p); }
function renderTurns(el, turns) { $(".chat-messages", el).replaceChildren(); turns.forEach((t) => { chatLine(el, `Kevin: ${t.q}`, "user"); chatLine(el, `Lauren: ${t.a}`, "assistant"); }); }
// Detail is always Kevin's own pasted/verified source (email, transcript) — there is no separate
// unverified-vs-confirmed distinction in his workflow, so confirmedContext mirrors detail exactly
// rather than asking him to duplicate the same text into a second field.
function itemForChat(el) { const detail = $(".detail", el).value; return { title: $(".title", el).value.trim(), tone: $(".tone", el).value, detail, confirmedContext: detail }; }
function meetingForChat() { const current = definitions.find((m) => m.meetingId === $("#meetingSelect").value); return { title: current?.displayName || $("#adHocTitle").value.trim(), date: $("#meetingDate").value }; }
async function loadChat(el) { try { const data = await api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "load" }); renderTurns(el, data.turns || []); } catch (e) { chatLine(el, `Chat unavailable: ${e.message}`, "error"); } }
function clearChat(el) { api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "clear" }).catch(() => {}); }
function extractionForChat(el) { try { const extraction = JSON.parse(el.dataset.extraction || "null"); const sheets = [...el.querySelectorAll(".extract-sheet:checked")].map((input) => input.value); return extraction && sheets.length ? [{ extractionId: extraction.extractionId, sheets }] : []; } catch { return []; } }
async function sendChat(el) { const input = $(".chat-input", el); const text = input.value.trim(); if (!text) return; try { const data = await api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "send", message: text, item: itemForChat(el), meeting: meetingForChat(), extractionIds: extractionForChat(el) }); input.value = ""; renderTurns(el, data.turns || []); } catch (e) { chatLine(el, `Chat unavailable: ${e.message}`, "error"); } }
async function recordVoice(el) {
  try {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error("Recording is not available in this browser.");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true }); const recorder = new MediaRecorder(stream); const chunks = [];
    recorder.ondataavailable = (e) => chunks.push(e.data);
    recorder.onstop = async () => { stream.getTracks().forEach((track) => track.stop()); try { const blob = new Blob(chunks, { type: recorder.mimeType }); const data = await api("/api/voice/stt", {}, { body: blob, headers: { "Content-Type": blob.type } }); $(".chat-input", el).value = data.text || ""; } catch (e) { chatLine(el, `Voice unavailable: ${e.message}`, "error"); } };
    recorder.start(); const mic = $(".mic", el); mic.textContent = "Recording… click to stop"; mic.onclick = () => recorder.stop(); recorder.addEventListener("stop", () => { mic.textContent = "Mic"; mic.onclick = () => recordVoice(el); }, { once: true });
  } catch (e) { chatLine(el, `Voice unavailable: ${e.message}`, "error"); }
}
async function listen(el) { const reply = [...$(".chat-messages", el).querySelectorAll(".assistant")].at(-1); if (!reply) return; try { const r = await api("/api/voice/tts", { text: reply.textContent.replace(/^Lauren: /, "") }, { raw: true }); const url = URL.createObjectURL(await r.blob()); const audio = new Audio(url); audio.onended = () => URL.revokeObjectURL(url); await audio.play(); } catch (e) { chatLine(el, `Voice unavailable: ${e.message}`, "error"); } }
function renderExtraction(el, extraction) { const list = $(".extract-sheets", el); list.replaceChildren(); extraction.sheets.forEach((sheet) => { const row = document.createElement("div"); row.className = "extract-sheet-row"; const label = document.createElement("label"); const checkbox = document.createElement("input"); checkbox.type = "checkbox"; checkbox.className = "extract-sheet"; checkbox.value = sheet.name; label.append(checkbox, " " + sheet.name + " (" + sheet.dimensions.rows + " rows × " + sheet.dimensions.cols + " columns)"); const preview = document.createElement("pre"); preview.textContent = sheet.preview; row.append(label, preview); list.append(row); }); }
async function extractWorkbook(el) { const file = $(".xlsx-file", el).files[0]; const result = $(".extract-message", el); if (!file) return message(result, "Choose a .xlsx or .xlsm workbook first."); try { const form = new FormData(); form.append("file", file); form.append("itemId", el.dataset.itemId); const data = await api("/api/extract", {}, { body: form, headers: {} }); el.dataset.extraction = JSON.stringify({ extractionId: data.extractionId, digest: data.digest, fileName: data.fileName, sheets: data.sheets }); renderExtraction(el, data); message(result, "Extracted " + data.sheets.length + " sheet" + (data.sheets.length === 1 ? "" : "s") + ". " + (data.notes?.join(" ") || ""), true); } catch (e) { message(result, e.message); } }
// Stateless suggestion only — overwrites the visible Speaker-note seed field so Kevin
// can review/edit before submitting; nothing is written anywhere until he submits.
async function suggestSpeakerNote(el) {
  const result = $(".suggest-message", el);
  if (!$(".title", el).value.trim()) return message(result, "Enter a title first.");
  try {
    const data = await api("/api/speaker-notes/candidate", { item: itemForChat(el), meeting: meetingForChat(), extractionIds: extractionForChat(el) });
    $(".seed", el).value = data.candidate;
    message(result, "Candidate added to Speaker-note seed. Review and edit before submitting.", true);
  } catch (e) { message(result, e.message); }
}
function attachSelectedSheets(el) { try { const extraction = JSON.parse(el.dataset.extraction || "null"); const names = [...el.querySelectorAll(".extract-sheet:checked")].map((input) => input.value); if (!extraction || !names.length) return message($(".extract-message", el), "Select at least one sheet to attach."); const sheets = extraction.sheets.filter((sheet) => names.includes(sheet.name)); const text = sheets.map((sheet) => "[" + extraction.fileName + " — " + sheet.name + "]\n" + sheet.preview).join("\n\n"); const detail = $(".detail", el); detail.value = [detail.value.trim(), text].filter(Boolean).join(detail.value.trim() ? "\n\n" : ""); const sources = JSON.parse(el.dataset.sources || "[]"); sources.push({ kind: "extract", fileName: extraction.fileName, digest: extraction.digest, sheets: names }); el.dataset.sources = JSON.stringify(sources); message($(".extract-message", el), "Selected sheets attached to detail.", true); } catch (e) { message($(".extract-message", el), "Could not attach selected sheets: " + e.message); } }
function addItem(data = {}) {
  const el = $("#itemTemplate").content.firstElementChild.cloneNode(true); el.dataset.itemId = data.itemId || uid();
  const assistantBodyId = `assistant-body-${++assistantBodyCounter}`; const chatPanel = $(".chat-panel", el); const assistantToggle = $(".assistant-toggle", chatPanel); const assistantBody = $(".assistant-body", chatPanel); assistantBody.id = assistantBodyId; assistantToggle.setAttribute("aria-controls", assistantBodyId); assistantToggle.addEventListener("click", () => { const expanded = assistantToggle.getAttribute("aria-expanded") === "true"; assistantToggle.setAttribute("aria-expanded", String(!expanded)); assistantBody.hidden = expanded; }); const extractBodyId = `extract-body-${++assistantBodyCounter}`; const extractToggle = $(".extract-toggle", el); const extractBody = $(".extract-body", el); extractBody.id = extractBodyId; extractToggle.setAttribute("aria-controls", extractBodyId); extractToggle.addEventListener("click", () => { const expanded = extractToggle.getAttribute("aria-expanded") === "true"; extractToggle.setAttribute("aria-expanded", String(!expanded)); extractBody.hidden = expanded; }); const speakerBodyId = `speaker-body-${++assistantBodyCounter}`; const speakerToggle = $(".speaker-toggle", el); const speakerBody = $(".speaker-body", el); speakerBody.id = speakerBodyId; speakerToggle.setAttribute("aria-controls", speakerBodyId); speakerToggle.addEventListener("click", () => { const expanded = speakerToggle.getAttribute("aria-expanded") === "true"; speakerToggle.setAttribute("aria-expanded", String(!expanded)); speakerBody.hidden = expanded; });
  // Older carried-forward records may still carry a distinct confirmedContext from before the
  // two fields were merged (16 Sept 2026) — fold any extra content into detail rather than drop it.
  const detailValue = data.detail || ""; const priorContext = data.confirmedContext || "";
  const mergedDetail = priorContext && priorContext.trim() !== detailValue.trim() ? [detailValue, priorContext].filter(Boolean).join("\n\n") : detailValue;
  $(".title", el).value = data.title || ""; $(".tone", el).value = data.tone || "update"; $(".priority", el).value = data.priority ?? 1; $(".detail", el).value = mergedDetail; $(".seed", el).value = data.speakerNoteSeed || ""; el.dataset.sources = JSON.stringify(data.sources || []); renderTone(el); $(".tone", el).addEventListener("change", () => renderTone(el));
  if (data.carryForward) { $(".carry", el).textContent = `Carry-forward from ${data.carryForward.fromIntake} (${data.carryForward.fromItemId}); choose carried, resolved, or dismissed.`; const status = document.createElement("select"); status.className = "status"; status.innerHTML = '<option value="carried">Carried</option><option value="resolved">Resolved</option><option value="dismissed">Dismissed</option>'; status.value = data.status || "carried"; $(".carry", el).append(" ", status); el.dataset.carry = JSON.stringify(data.carryForward); } else { $(".carry", el).textContent = data.origin === "roadmap-weekly" ? `Pre-populated from ${data.sourceLabel || "the weekly roadmap"} — review before submitting.` : ""; el.dataset.carry = ""; }
  $(".remove", el).onclick = () => { clearChat(el); el.remove(); renderNumbers(); };
  $(".chat-send", el).onclick = () => sendChat(el); $(".chat-input", el).addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendChat(el); } }); $(".mic", el).onclick = () => recordVoice(el); $(".listen", el).onclick = () => listen(el);
  $(".add-update-line", el).onclick = () => { const input = $(".update-line", el); const text = input.value.trim(); if (!text) return; const today = new Date(); const date = `${String(today.getDate()).padStart(2, "0")}/${String(today.getMonth() + 1).padStart(2, "0")}/${String(today.getFullYear()).slice(-2)}`; const detail = $(".detail", el); detail.value = [`${date} - ${text}`, detail.value.trim()].filter(Boolean).join("\n\n"); input.value = ""; };
  $(".attach-context", el).onclick = () => { const reply = [...$(".chat-messages", el).querySelectorAll(".assistant")].at(-1); if (!reply) return; const detail = $(".detail", el); const text = reply.textContent.replace(/^Lauren: /, ""); detail.value = [detail.value.trim(), text].filter(Boolean).join(detail.value.trim() ? "\n\n" : ""); };
  $(".xlsx-file", el).addEventListener("change", (e) => { $(".file-name", el).textContent = e.target.files[0]?.name || "No file chosen"; }); $(".extract-btn", el).onclick = () => extractWorkbook(el); $(".attach-sheets", el).onclick = () => attachSelectedSheets(el);
  $(".suggest-seed", el).onclick = () => suggestSpeakerNote(el);
  el.addEventListener("dragstart", () => { dragged = el; el.classList.add("dragging"); }); el.addEventListener("dragend", () => el.classList.remove("dragging")); el.addEventListener("dragover", (e) => { e.preventDefault(); const target = e.currentTarget; if (dragged && dragged !== target) { const before = e.clientY < target.getBoundingClientRect().top + target.offsetHeight / 2; items.insertBefore(dragged, before ? target : target.nextSibling); renderNumbers(); } });
  items.append(el); renderNumbers(); void loadChat(el);
}
async function loadMeetings() { try { const data = await api("/api/meetings/list"); definitions = data.meetings; for (const m of definitions) { const o = document.createElement("option"); o.value = m.meetingId; o.textContent = m.displayName; $("#meetingSelect").append(o); } } catch (e) { message($("#meetingMessage"), e.message); } }
async function loadPendingDraft(meetingId) {
  try {
    const data = await api("/api/intakes/pending", { meetingId });
    if (data.pending) { $("#meetingDate").value = data.pending.date; for (const item of data.pending.items || []) addItem({ ...item, origin: "roadmap-weekly", sourceLabel: data.pending.sourceLabel }); message($("#meetingMessage"), `Pre-populated ${(data.pending.items || []).length} item(s) from ${data.pending.sourceLabel} — review before submitting.`, true); }
  } catch (err) { message($("#meetingMessage"), err.message); }
}
// Only the HR Systems Roadmap meeting has a real extraction pipeline behind it
// (automation/extract_hr_roadmap_pending.py reads the local Roadmap Master
// workbook) -- the button is meaningless for any other meeting, so it's hidden
// unless this exact meeting is selected.
const HR_ROADMAP_MEETING_ID = "hr-systems-roadmap";
let pullTimer = null, pullDeadline = 0;
function stopPulling() { if (pullTimer) { clearInterval(pullTimer); pullTimer = null; } }
function renderPullState(state) {
  const el = $("#pullStatus");
  if (!state || state.status === "idle") { el.textContent = ""; el.className = "message"; return; }
  if (state.status === "requested" || state.status === "running") return message(el, "Pulling… (checks every minute, usually done within 2 minutes)", true);
  if (state.status === "done") { const when = new Date(state.completedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }); return message(el, `Pulled at ${when} — ${state.itemCount} item(s).`, true); }
  message(el, `Failed — ${state.error || "unknown error"} (click to retry)`);
}
async function pollPullStatus(meetingId) {
  if (Date.now() > pullDeadline) { stopPulling(); return message($("#pullStatus"), "Failed — timed out waiting for the local pull job. Is it running? (click to retry)"); }
  try {
    const state = await api("/api/intakes/pull-status", { meetingId });
    renderPullState(state);
    if (state.status === "done" || state.status === "failed") { stopPulling(); if (state.status === "done") await loadPendingDraft(meetingId); }
  } catch { /* transient network hiccup while polling -- keep trying until the deadline */ }
}
function startPolling(meetingId) { stopPulling(); pullDeadline = Date.now() + 2 * 60 * 1000; pollPullStatus(meetingId); pullTimer = setInterval(() => pollPullStatus(meetingId), 4000); }
$("#pullRoadmap").onclick = async () => {
  const meetingId = $("#meetingSelect").value;
  if (meetingId !== HR_ROADMAP_MEETING_ID) return;
  message($("#pullStatus"), "Pulling… (checks every minute, usually done within 2 minutes)", true);
  try { await api("/api/intakes/pull-request", { meetingId }); startPolling(meetingId); }
  catch (e) {
    if (/already in progress/i.test(e.message)) { startPolling(meetingId); return; } // a real pull is running -- reflect it, not an error
    if (/wait a moment/i.test(e.message)) { message($("#pullStatus"), e.message, true); return; } // cooldown, not a failure
    message($("#pullStatus"), `Failed — ${e.message} (click to retry)`);
  }
};
$("#meetingSelect").addEventListener("change", async (e) => {
  stopPulling();
  const meetingId = e.target.value;
  $("#pullRoadmapBox").hidden = meetingId !== HR_ROADMAP_MEETING_ID;
  $("#pullStatus").textContent = "";
  if (!meetingId) return;
  $("#adHocTitle").value = "";
  try { const data = await api("/api/intakes/previous", { meetingId }); for (const item of data.eligibleCarryForward || []) addItem(item); if (data.eligibleCarryForward?.length) message($("#meetingMessage"), "Eligible prior items added. Review each disposition.", true); } catch (err) { message($("#meetingMessage"), err.message); }
  await loadPendingDraft(meetingId);
  if (meetingId === HR_ROADMAP_MEETING_ID) {
    try { const state = await api("/api/intakes/pull-status", { meetingId }); renderPullState(state); if (state.status === "requested" || state.status === "running") startPolling(meetingId); } catch { /* status check is best-effort */ }
  }
});
$("#newRecurring").onclick = () => { if (!$("#adHocTitle").value.trim()) return message($("#meetingMessage"), "Enter an ad-hoc title first."); message($("#meetingMessage"), "Creating recurring definitions is an explicit follow-up admin action; Phase 1 does not write definitions from the browser. Use the versioned definitions file, then select it here."); };
$("#addItem").onclick = () => addItem();
$("#submit").onclick = async () => { const meetingId = $("#meetingSelect").value; const title = (meetingId ? definitions.find((m) => m.meetingId === meetingId)?.displayName : $("#adHocTitle").value).trim(); const date = $("#meetingDate").value; if (!title || !date) return message($("#submitMessage"), "Select a recurring meeting or enter an ad-hoc title, and set a date."); const submittedItems = [...items.children]; const draft = submittedItems.map((el, index) => { const detail = $(".detail", el).value; return { itemId: el.dataset.itemId, position: index + 1, priority: Number($(".priority", el).value), title: $(".title", el).value.trim(), tone: $(".tone", el).value, detail, confirmedContext: detail, speakerNoteSeed: $(".seed", el).value, status: $(".status", el)?.value || "open", sources: JSON.parse(el.dataset.sources || "[]"), carryForward: el.dataset.carry ? { ...JSON.parse(el.dataset.carry), disposition: $(".status", el).value } : null }; }).filter((x) => x.status !== "dismissed"); try { const data = await api("/api/intakes/submit", { schemaVersion: 1, meeting: { meetingId: meetingId || null, title, date, kind: meetingId ? "recurring" : "ad-hoc" }, items: draft, submittedBy: "Kevin" }); message($("#submitMessage"), `Locked intake submitted: ${data.path} (commit ${data.commitSha})`, true); $("#submit").disabled = true; submittedItems.forEach(clearChat); sessionStorage.removeItem("meetingPrepDraftId"); resetDraft(); } catch (e) { message($("#submitMessage"), e.message); } };
loadMeetings(); addItem();
