import test from "node:test";
import assert from "node:assert/strict";
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
  const store = new Map(); const calls = { put: 0 };
  return { store, calls, async get(key) { return store.get(key) || null; }, async put(key, value) { calls.put++; store.set(key, value); }, async delete(key) { store.delete(key); } };
}
async function call(path, body, env) {
  return worker.fetch(new Request(`https://meeting.test${path}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) }), { GITHUB_PAT: "test", ALLOWED_ORIGIN: "https://meeting.test", ...env });
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
