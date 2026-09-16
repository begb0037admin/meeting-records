import test from "node:test";
import assert from "node:assert/strict";
import * as XLSX from "xlsx";
import worker, { eligibleCarryForward, validateIntake } from "../src/worker.js";

const item = {
  itemId: "itm_20260930_001",
  position: 1,
  priority: 1,
  title: "Status",
  tone: "update",
  detail: "Confirmed detail",
  confirmedContext: "Confirmed context",
  sources: [],
  carryForward: null,
  speakerNoteSeed: "",
  status: "open",
};
const draft = {
  schemaVersion: 1,
  meeting: {
    meetingId: "hr-systems-managers",
    title: "HR Systems Managers Meeting",
    date: "2026-09-30",
    kind: "recurring",
  },
  items: [item],
  submittedBy: "Kevin",
};

test("validates a complete locked Phase 1 intake", () => {
  const record = validateIntake(draft);
  assert.equal(record.status, "submitted");
  assert.equal(record.items[0].itemId, item.itemId);
});
test("rejects missing required item content", () => {
  assert.throws(
    () => validateIntake({ ...draft, items: [{ ...item, detail: undefined }] }),
    /missing or invalid/,
  );
});
test("carry-forward copies only open and carried previous items with an auditable pointer", () => {
  const carried = eligibleCarryForward({
    path: "intakes/hr-systems-managers/2026-09-16.json",
    record: {
      items: [
        item,
        { ...item, itemId: "itm_done", status: "resolved" },
        { ...item, itemId: "itm_gone", status: "dismissed" },
      ],
    },
  });
  assert.equal(carried.length, 1);
  assert.equal(carried[0].status, "carried");
  assert.equal(carried[0].carryForward.fromItemId, item.itemId);
  assert.notEqual(carried[0].itemId, item.itemId);
});

function kv() {
  const store = new Map(); const calls = { put: 0, keys: [], options: [] };
  return { store, calls, async get(key) { return store.get(key) || null; }, async put(key, value, options) { calls.put++; calls.keys.push(key); calls.options.push(options); store.set(key, value); }, async delete(key) { store.delete(key); } };
}
async function call(path, body, env) {
  return worker.fetch(new Request(`https://meeting.test${path}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) }), { GITHUB_PAT: "test", ALLOWED_ORIGIN: "https://meeting.test", ...env });
}
async function extractCall(fileName, bytes, env, itemId = "itm_extract") {
  const form = new FormData();
  form.append("file", new Blob([bytes]), fileName);
  form.append("itemId", itemId);
  return worker.fetch(new Request("https://meeting.test/api/extract", { method: "POST", body: form }), { GITHUB_PAT: "test", ALLOWED_ORIGIN: "https://meeting.test", ...env });
}
function workbookBytes({ macro = false } = {}) {
  const book = XLSX.utils.book_new();
  const status = XLSX.utils.aoa_to_sheet([["Name", "Count"], ["Open", 2], ["Carried", 3]]);
  status.B4 = { t: "n", f: "B2+B3", v: 5 };
  status["!ref"] = "A1:B4";
  XLSX.utils.book_append_sheet(book, status, "Status");
  XLSX.utils.book_append_sheet(book, XLSX.utils.aoa_to_sheet([["Owner", "Action"], ["Kevin", "Review"]]), "Actions");
  if (macro) {
    book.vbaraw = Uint8Array.from([1, 2, 3]);
    return XLSX.write(book, { type: "buffer", bookType: "xlsm" });
  }
  return XLSX.write(book, { type: "buffer", bookType: "xlsx" });
}
const chatItem = { title: "Status", tone: "update", detail: "Confirmed detail", confirmedContext: "" };
test("chat sends, persists, loads, clears, and isolates draft/item keys", async () => {
  const memory = kv(); const original = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify({ content: [{ type: "text", text: "Status update: confirmed." }] }), { status: 200 });
  try {
    const base = { draftId: "draft_one", itemId: "itm_one", item: chatItem, message: "Draft this" };
    const sent = await call("/api/chat", base, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" });
    assert.equal(sent.status, 200); assert.equal(memory.calls.put, 1);
    assert.equal((await (await call("/api/chat", { draftId: "draft_one", itemId: "itm_one", op: "load" }, { CHAT_KV: memory })).json()).turns.length, 1);
    assert.equal((await (await call("/api/chat", { draftId: "draft_two", itemId: "itm_one", op: "load" }, { CHAT_KV: memory })).json()).turns.length, 0);
    assert.equal((await (await call("/api/chat", { draftId: "draft_one", itemId: "itm_two", op: "load" }, { CHAT_KV: memory })).json()).turns.length, 0);
    assert.equal((await (await call("/api/chat", { draftId: "draft_one", itemId: "itm_one", op: "clear" }, { CHAT_KV: memory })).json()).ok, true);
  } finally { globalThis.fetch = original; }
});
test("chat rejects invalid ids and bad tone before KV or Anthropic", async () => {
  const memory = kv(); let fetched = false; const original = globalThis.fetch; globalThis.fetch = async () => { fetched = true; throw new Error("should not call"); };
  try {
    assert.equal((await call("/api/chat", { draftId: "bad", itemId: "itm_one", op: "load" }, { CHAT_KV: memory })).status, 400);
    assert.equal((await call("/api/chat", { draftId: "draft_one", itemId: "itm_one", item: { ...chatItem, tone: "bad" }, message: "x" }, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" })).status, 400);
    assert.equal(fetched, false);
  } finally { globalThis.fetch = original; }
});
test("failed Anthropic response leaves stored chat untouched", async () => {
  const memory = kv(); memory.store.set("chat:v1:draft_one:itm_one", JSON.stringify({ v: 1, turns: [{ q: "old", a: "reply", t: "2026-01-01T00:00:00Z" }] }));
  const original = globalThis.fetch; globalThis.fetch = async () => new Response(JSON.stringify({ error: { message: "down" } }), { status: 503 });
  try { assert.equal((await call("/api/chat", { draftId: "draft_one", itemId: "itm_one", item: chatItem, message: "new" }, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" })).status, 503); assert.equal(memory.calls.put, 0); } finally { globalThis.fetch = original; }
});
test("voice routes use configured AI models and degrade without AI", async () => {
  const seen = []; const ai = { async run(model, input) { seen.push([model, input]); return model.includes("whisper") ? { text: "heard" } : { audio: btoa("audio") }; } };
  const stt = await worker.fetch(new Request("https://meeting.test/api/voice/stt", { method: "POST", body: new Uint8Array(120) }), { GITHUB_PAT: "x", ALLOWED_ORIGIN: "https://meeting.test", AI: ai });
  const tts = await call("/api/voice/tts", { text: "hello" }, { AI: ai });
  assert.equal(stt.status, 200); assert.equal(tts.status, 200); assert.equal(seen[0][0], "@cf/openai/whisper-large-v3-turbo"); assert.equal(seen[1][0], "@cf/deepgram/aura-2-en");
  assert.equal((await call("/api/voice/tts", { text: "hello" }, {})).status, 501);
  const absent = await worker.fetch(new Request("https://meeting.test/api/voice/stt", { method: "POST", body: new Uint8Array(120) }), { GITHUB_PAT: "x", ALLOWED_ORIGIN: "https://meeting.test" }); assert.equal(absent.status, 501);
});

test("extracts a bounded two-sheet .xlsx without executing formulas", async () => {
  const memory = kv();
  const result = await extractCall("agenda.xlsx", workbookBytes(), { CHAT_KV: memory });
  const data = await result.json();
  assert.equal(result.status, 200);
  assert.equal(data.sheets.length, 2);
  assert.deepEqual(data.sheets[0].headers, ["Name", "Count"]);
  assert.deepEqual(data.sheets[0].dimensions, { rows: 4, cols: 2 });
  assert.match(data.sheets[0].preview, /Carried\t3/);
  assert.match(data.sheets[0].preview, /\t5/);
  assert.match(data.digest, /^sha256:[a-f0-9]{64}$/);
  assert.ok(Date.parse(data.expiresAt) > Date.now());
  assert.match(memory.calls.keys[0], /^extract:v1:extract_/);
  assert.deepEqual(memory.calls.options[0], { expirationTtl: 3600 });
});

test("rejects unsupported workbook extensions before parsing", async () => {
  const memory = kv(); const bytes = workbookBytes();
  const xlsm = await extractCall("agenda.xlsm", bytes, { CHAT_KV: memory });
  const xls = await extractCall("agenda.xls", bytes, { CHAT_KV: memory });
  assert.match((await xlsm.json()).error, /\.xlsm/);
  assert.match((await xls.json()).error, /\.xls/);
  assert.equal(memory.calls.put, 0);
});

test("rejects oversized, password-protected, macro, and garbage uploads cleanly", async () => {
  const memory = kv();
  const oversized = await extractCall("large.xlsx", new Uint8Array(5 * 1024 * 1024 + 1), { CHAT_KV: memory });
  const ole = await extractCall("locked.xlsx", Uint8Array.from([0xd0, 0xcf, 0x11, 0xe0, 0xa1, 0xb1, 0x1a, 0xe1]), { CHAT_KV: memory });
  const macro = await extractCall("renamed.xlsx", workbookBytes({ macro: true }), { CHAT_KV: memory });
  const garbage = await extractCall("garbage.xlsx", Uint8Array.from([0x50, 0x4b, 0x03, 0x04, 1, 2, 3]), { CHAT_KV: memory });
  assert.match((await oversized.json()).error, /5 MB/);
  assert.match((await ole.json()).error, /Password-protected/);
  assert.match((await macro.json()).error, /macro content/);
  assert.match((await garbage.json()).error, /valid .xlsx/);
  assert.equal(memory.calls.put, 0);
});

test("chat resolves only selected extraction sheets using isolated KV prefixes", async () => {
  const memory = kv();
  memory.store.set("extract:v1:extract_selected", JSON.stringify({ fileName: "agenda.xlsx", digest: "sha256:test", sheets: [{ name: "Keep", preview: "KEEP THIS" }, { name: "Hide", preview: "DO NOT INCLUDE" }] }));
  let body;
  const original = globalThis.fetch;
  globalThis.fetch = async (_url, options) => { body = JSON.parse(options.body); return new Response(JSON.stringify({ content: [{ type: "text", text: "Status update: confirmed." }] }), { status: 200 }); };
  try {
    const response = await call("/api/chat", { draftId: "draft_selected", itemId: "itm_selected", item: chatItem, message: "Use the selected sheet", extractionIds: [{ extractionId: "extract_selected", sheets: ["Keep"] }] }, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" });
    assert.equal(response.status, 200);
    const supplied = body.messages.at(-1).content;
    assert.match(supplied, /KEEP THIS/);
    assert.doesNotMatch(supplied, /DO NOT INCLUDE/);
    assert.equal(memory.calls.keys.at(-1), "chat:v1:draft_selected:itm_selected");
    assert.ok([...memory.store.keys()].some((key) => key.startsWith("extract:v1:")));
    assert.ok([...memory.store.keys()].some((key) => key.startsWith("chat:v1:")));
  } finally { globalThis.fetch = original; }
});

test("chat preserves an explicit unavailable extraction note", async () => {
  const memory = kv(); let body;
  const original = globalThis.fetch;
  globalThis.fetch = async (_url, options) => { body = JSON.parse(options.body); return new Response(JSON.stringify({ content: [{ type: "text", text: "Status update: clarify." }] }), { status: 200 }); };
  try {
    const response = await call("/api/chat", { draftId: "draft_missing", itemId: "itm_missing", item: chatItem, message: "Use it", extractionIds: [{ extractionId: "extract_missing", sheets: ["Gone"] }] }, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" });
    assert.equal(response.status, 200);
    assert.match(body.messages.at(-1).content, /no longer available/);
  } finally { globalThis.fetch = original; }
});
