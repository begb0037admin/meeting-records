const $ = (s, root = document) => root.querySelector(s);
const items = $("#items");
let definitions = [];
let dragged = null;
$("#meetingDate").value = new Date().toISOString().slice(0, 10);
const uid = () => `itm_${new Date().toISOString().slice(0, 10).replaceAll("-", "")}_${crypto.randomUUID().replaceAll("-", "").slice(0, 12)}`;
// Session scope restores accidental refreshes, but does not carry chat into the next intake.
let draftId = sessionStorage.getItem("meetingPrepDraftId");
if (!draftId) { draftId = `draft_${crypto.randomUUID().replaceAll("-", "")}`; sessionStorage.setItem("meetingPrepDraftId", draftId); }
const resetDraft = () => { draftId = `draft_${crypto.randomUUID().replaceAll("-", "")}`; sessionStorage.setItem("meetingPrepDraftId", draftId); };
function message(el, text, ok = false) { el.textContent = text; el.className = `message ${ok ? "ok" : "error"}`; }
function renderNumbers() { [...items.children].forEach((el, i) => ($(".item-number", el).textContent = `Item ${i + 1}`)); }
async function api(path, body = {}, opts = {}) {
  const r = await fetch(path, { method: "POST", headers: opts.headers || { "Content-Type": "application/json" }, body: opts.body || JSON.stringify(body) });
  if (!r.ok) { let data = {}; try { data = await r.json(); } catch {} throw new Error(data.error || "Request failed"); }
  return opts.raw ? r : r.json();
}
function chatLine(el, text, kind) { const p = document.createElement("p"); p.className = `chat-line ${kind}`; p.textContent = text; $(".chat-messages", el).append(p); }
function renderTurns(el, turns) { $(".chat-messages", el).replaceChildren(); turns.forEach((t) => { chatLine(el, `Kevin: ${t.q}`, "user"); chatLine(el, `Lauren: ${t.a}`, "assistant"); }); }
function itemForChat(el) { return { title: $(".title", el).value.trim(), tone: $(".tone", el).value, detail: $(".detail", el).value, confirmedContext: $(".context", el).value }; }
function meetingForChat() { const current = definitions.find((m) => m.meetingId === $("#meetingSelect").value); return { title: current?.displayName || $("#adHocTitle").value.trim(), date: $("#meetingDate").value }; }
async function loadChat(el) { try { const data = await api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "load" }); renderTurns(el, data.turns || []); } catch (e) { chatLine(el, `Chat unavailable: ${e.message}`, "error"); } }
function clearChat(el) { api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "clear" }).catch(() => {}); }
async function sendChat(el) { const input = $(".chat-input", el); const text = input.value.trim(); if (!text) return; try { const data = await api("/api/chat", { draftId, itemId: el.dataset.itemId, op: "send", message: text, item: itemForChat(el), meeting: meetingForChat() }); input.value = ""; renderTurns(el, data.turns || []); } catch (e) { chatLine(el, `Chat unavailable: ${e.message}`, "error"); } }
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
function addItem(data = {}) {
  const el = $("#itemTemplate").content.firstElementChild.cloneNode(true); el.dataset.itemId = data.itemId || uid();
  $(".title", el).value = data.title || ""; $(".tone", el).value = data.tone || "update"; $(".priority", el).value = data.priority ?? 1; $(".detail", el).value = data.detail || ""; $(".context", el).value = data.confirmedContext || ""; $(".seed", el).value = data.speakerNoteSeed || "";
  if (data.carryForward) { $(".carry", el).textContent = `Carry-forward from ${data.carryForward.fromIntake} (${data.carryForward.fromItemId}); choose carried, resolved, or dismissed.`; const status = document.createElement("select"); status.className = "status"; status.innerHTML = '<option value="carried">Carried</option><option value="resolved">Resolved</option><option value="dismissed">Dismissed</option>'; status.value = data.status || "carried"; $(".carry", el).append(" ", status); el.dataset.carry = JSON.stringify(data.carryForward); } else el.dataset.carry = "";
  $(".remove", el).onclick = () => { clearChat(el); el.remove(); renderNumbers(); };
  $(".chat-send", el).onclick = () => sendChat(el); $(".chat-input", el).addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendChat(el); } }); $(".mic", el).onclick = () => recordVoice(el); $(".listen", el).onclick = () => listen(el);
  $(".attach-context", el).onclick = () => { const reply = [...$(".chat-messages", el).querySelectorAll(".assistant")].at(-1); if (reply) $(".context", el).value = reply.textContent.replace(/^Lauren: /, ""); };
  el.addEventListener("dragstart", () => { dragged = el; el.classList.add("dragging"); }); el.addEventListener("dragend", () => el.classList.remove("dragging")); el.addEventListener("dragover", (e) => { e.preventDefault(); const target = e.currentTarget; if (dragged && dragged !== target) { const before = e.clientY < target.getBoundingClientRect().top + target.offsetHeight / 2; items.insertBefore(dragged, before ? target : target.nextSibling); renderNumbers(); } });
  items.append(el); renderNumbers(); void loadChat(el);
}
async function loadMeetings() { try { const data = await api("/api/meetings/list"); definitions = data.meetings; for (const m of definitions) { const o = document.createElement("option"); o.value = m.meetingId; o.textContent = m.displayName; $("#meetingSelect").append(o); } } catch (e) { message($("#meetingMessage"), e.message); } }
$("#meetingSelect").addEventListener("change", async (e) => { if (!e.target.value) return; $("#adHocTitle").value = ""; try { const data = await api("/api/intakes/previous", { meetingId: e.target.value }); for (const item of data.eligibleCarryForward || []) addItem(item); if (data.eligibleCarryForward?.length) message($("#meetingMessage"), "Eligible prior items added. Review each disposition.", true); } catch (err) { message($("#meetingMessage"), err.message); } });
$("#newRecurring").onclick = () => { if (!$("#adHocTitle").value.trim()) return message($("#meetingMessage"), "Enter an ad-hoc title first."); message($("#meetingMessage"), "Creating recurring definitions is an explicit follow-up admin action; Phase 1 does not write definitions from the browser. Use the versioned definitions file, then select it here."); };
$("#addItem").onclick = () => addItem();
$("#submit").onclick = async () => { const meetingId = $("#meetingSelect").value; const title = (meetingId ? definitions.find((m) => m.meetingId === meetingId)?.displayName : $("#adHocTitle").value).trim(); const date = $("#meetingDate").value; if (!title || !date) return message($("#submitMessage"), "Select a recurring meeting or enter an ad-hoc title, and set a date."); const submittedItems = [...items.children]; const draft = submittedItems.map((el, index) => ({ itemId: el.dataset.itemId, position: index + 1, priority: Number($(".priority", el).value), title: $(".title", el).value.trim(), tone: $(".tone", el).value, detail: $(".detail", el).value, confirmedContext: $(".context", el).value, speakerNoteSeed: $(".seed", el).value, status: $(".status", el)?.value || "open", sources: [], carryForward: el.dataset.carry ? { ...JSON.parse(el.dataset.carry), disposition: $(".status", el).value } : null })).filter((x) => x.status !== "dismissed"); try { const data = await api("/api/intakes/submit", { schemaVersion: 1, meeting: { meetingId: meetingId || null, title, date, kind: meetingId ? "recurring" : "ad-hoc" }, items: draft, submittedBy: "Kevin" }); message($("#submitMessage"), `Locked intake submitted: ${data.path} (commit ${data.commitSha})`, true); $("#submit").disabled = true; submittedItems.forEach(clearChat); sessionStorage.removeItem("meetingPrepDraftId"); resetDraft(); } catch (e) { message($("#submitMessage"), e.message); } };
loadMeetings(); addItem();
