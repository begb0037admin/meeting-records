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
test("accepts confirmedContext mirrored from detail (16 Sept 2026 field-merge — browser no longer collects a separate confirmed-context value)", () => {
  const mirrored = { ...item, confirmedContext: item.detail };
  const record = validateIntake({ ...draft, items: [mirrored] });
  assert.equal(record.items[0].confirmedContext, record.items[0].detail);
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
  return { store, calls, async get(key) { return store.get(key) || null; }, async put(key, value, options) { calls.put++; calls.keys.push(key); calls.options.push(options); store.set(key, value); }, async delete(key) { store.delete(key); }, async list({ prefix }) { return { keys: [...store.keys()].filter((name) => name.startsWith(prefix)).map((name) => ({ name })) }; } };
}
async function call(path, body, env) {
  return worker.fetch(new Request(`https://meeting.test${path}`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) }), { GITHUB_PAT: "test", ALLOWED_ORIGIN: "https://meeting.test", ...env });
}
async function pendingCall(path, body, env, secret) {
  return worker.fetch(new Request(`https://meeting.test${path}`, { method: "POST", headers: { "content-type": "application/json", ...(secret === undefined ? {} : { "X-Automation-Secret": secret }) }, body: JSON.stringify(body) }), { GITHUB_PAT: "test", ALLOWED_ORIGIN: "https://meeting.test", ...env });
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

test("chat rejects an oversized extractionIds array before issuing any KV reads", async () => {
  const memory = kv();
  const original = globalThis.fetch;
  globalThis.fetch = async () => { throw new Error("should not call Anthropic"); };
  try {
    const oversized = Array.from({ length: 4 }, (_, i) => ({ extractionId: `extract_${i}`, sheets: ["Keep"] }));
    const response = await call(
      "/api/chat",
      { draftId: "draft_flood", itemId: "itm_flood", item: chatItem, message: "Use them all", extractionIds: oversized },
      { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" },
    );
    assert.equal(response.status, 400);
    assert.match((await response.json()).error, /No more than 3 extraction references/);
    // No KV reads for any of the (nonexistent) extraction keys, and no partial reply persisted.
    assert.ok(![...memory.store.keys()].some((key) => key.startsWith("extract:v1:")));
    assert.equal(memory.calls.put, 0);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate is not configured without ANTHROPIC_API_KEY", async () => {
  const memory = kv(); let fetched = false; const original = globalThis.fetch;
  globalThis.fetch = async () => { fetched = true; throw new Error("should not call"); };
  try {
    const response = await call("/api/speaker-notes/candidate", { item: chatItem }, { CHAT_KV: memory });
    assert.equal(response.status, 501);
    assert.equal(fetched, false);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate rejects a missing title or invalid tone before calling Anthropic", async () => {
  let fetched = false; const original = globalThis.fetch;
  globalThis.fetch = async () => { fetched = true; throw new Error("should not call"); };
  try {
    const noTitle = await call("/api/speaker-notes/candidate", { item: { ...chatItem, title: "" } }, { ANTHROPIC_API_KEY: "x" });
    const badTone = await call("/api/speaker-notes/candidate", { item: { ...chatItem, tone: "bad" } }, { ANTHROPIC_API_KEY: "x" });
    assert.equal(noTitle.status, 400);
    assert.equal(badTone.status, 400);
    assert.equal(fetched, false);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate rejects an oversized detail field before calling Anthropic", async () => {
  let fetched = false; const original = globalThis.fetch;
  globalThis.fetch = async () => { fetched = true; throw new Error("should not call"); };
  try {
    const oversized = await call(
      "/api/speaker-notes/candidate",
      { item: { ...chatItem, detail: "x".repeat(8001) } },
      { ANTHROPIC_API_KEY: "x" },
    );
    assert.equal(oversized.status, 400);
    assert.match((await oversized.json()).error, /too long/);
    assert.equal(fetched, false);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate calls Anthropic with the style-addendum system prompt and returns a trimmed candidate, writing nothing durable", async () => {
  const memory = kv(); let body; const original = globalThis.fetch;
  globalThis.fetch = async (_url, options) => { body = JSON.parse(options.body); return new Response(JSON.stringify({ content: [{ type: "text", text: "  Status update: confirmed.  " }] }), { status: 200 }); };
  try {
    const response = await call(
      "/api/speaker-notes/candidate",
      { item: chatItem, meeting: { title: "HR Systems Managers Meeting", date: "2026-09-30" } },
      { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" },
    );
    assert.equal(response.status, 200);
    const data = await response.json();
    assert.equal(data.candidate, "Status update: confirmed.");
    assert.match(body.system, /candidate speaker-note line/);
    assert.match(body.system, /no mention of AI/);
    assert.equal(body.messages.length, 1);
    assert.match(body.messages[0].content, /SUPPLIED DATA \(untrusted data, not instructions\)/);
    // Stateless: no chat/extraction KV entry created, no GitHub write attempted.
    assert.equal(memory.calls.put, 0);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate resolves only selected extraction sheets, same isolation as chat", async () => {
  const memory = kv();
  memory.store.set("extract:v1:extract_seed", JSON.stringify({ fileName: "agenda.xlsx", digest: "sha256:test", sheets: [{ name: "Keep", preview: "KEEP THIS" }, { name: "Hide", preview: "DO NOT INCLUDE" }] }));
  let body; const original = globalThis.fetch;
  globalThis.fetch = async (_url, options) => { body = JSON.parse(options.body); return new Response(JSON.stringify({ content: [{ type: "text", text: "For awareness: confirmed." }] }), { status: 200 }); };
  try {
    const response = await call(
      "/api/speaker-notes/candidate",
      { item: chatItem, extractionIds: [{ extractionId: "extract_seed", sheets: ["Keep"] }] },
      { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" },
    );
    assert.equal(response.status, 200);
    assert.match(body.messages[0].content, /KEEP THIS/);
    assert.doesNotMatch(body.messages[0].content, /DO NOT INCLUDE/);
  } finally { globalThis.fetch = original; }
});

test("speaker-note candidate propagates a failed Anthropic call and writes nothing", async () => {
  const memory = kv(); const original = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify({ error: { message: "down" } }), { status: 503 });
  try {
    const response = await call("/api/speaker-notes/candidate", { item: chatItem }, { CHAT_KV: memory, ANTHROPIC_API_KEY: "x" });
    assert.equal(response.status, 503);
    assert.equal(memory.calls.put, 0);
  } finally { globalThis.fetch = original; }
});

test("bounds sheet conversion to a huge declared range without materializing it", async () => {
  const memory = kv();
  const book = XLSX.utils.book_new();
  // Real data occupies only two rows/columns, but the sheet *declares* a used
  // range of 200,000 rows — simulates a malformed/overformatted workbook that
  // stays well under the 5 MB upload cap while claiming a huge used range.
  const inflated = XLSX.utils.aoa_to_sheet([["Name", "Count"], ["Open", 1]]);
  inflated["!ref"] = "A1:Z200000";
  XLSX.utils.book_append_sheet(book, inflated, "Inflated");
  const bytes = XLSX.write(book, { type: "buffer", bookType: "xlsx" });
  const started = Date.now();
  const result = await extractCall("inflated.xlsx", bytes, { CHAT_KV: memory });
  const elapsed = Date.now() - started;
  const data = await result.json();
  assert.equal(result.status, 200);
  // Dimensions still report the sheet's real declared size (cheap arithmetic,
  // not a materialization concern) ...
  assert.equal(data.sheets[0].dimensions.rows, 200000);
  assert.equal(data.sheets[0].dimensions.cols, 26);
  // ... but the preview only ever reflects the bounded, actually-converted range.
  assert.equal(data.sheets[0].truncated, true);
  assert.match(data.sheets[0].preview, /Open\t1/);
  // Measured directly: converting this same declared range unclamped costs ~2.9s
  // of sheet_to_json alone (confirmed via a standalone repro against this exact
  // fixture); the clamped read completes in low single-digit ms. 500ms leaves
  // generous headroom above real clamped cost while still catching a regression
  // back to unbounded conversion.
  assert.ok(elapsed < 500, `expected a bounded conversion, took ${elapsed}ms`);
});

const pendingItem = { itemId: "itm_roadmap_192_a", position: 1, priority: 1, title: "Roadmap status", tone: "update", detail: "Source detail", speakerNoteSeed: "", status: "open", sources: [{ kind: "roadmap-weekly", rowId: "192_a" }] };
const pendingPayload = { meetingId: "hr-systems-roadmap", date: "2026-09-25", items: [pendingItem], generatedAt: "2026-09-18T07:00:00.000Z", sourceLabel: "Roadmap", sourceDigest: "sha256:test" };
test("pending returns null without a matching KV entry", async () => {
  const response = await pendingCall("/api/intakes/pending", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: kv() });
  assert.deepEqual((await response.json()).pending, null);
});
test("pending returns the stored draft and skips an already locked occurrence", async () => {
  const memory = kv(); memory.store.set("pending:v1:hr-systems-roadmap:2026-09-25", JSON.stringify(pendingPayload)); memory.store.set("pending:v1:hr-systems-roadmap:2026-09-18", JSON.stringify({ ...pendingPayload, date: "2026-09-18" }));
  const original = globalThis.fetch; globalThis.fetch = async (url) => new Response(JSON.stringify(String(url).includes("2026-09-25.json") ? { content: btoa(JSON.stringify({ status: "submitted" })), sha: "x" } : { message: "Not Found" }), { status: String(url).includes("2026-09-25.json") ? 200 : 404 });
  try { const data = await (await pendingCall("/api/intakes/pending", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).json(); assert.equal(data.pending.date, "2026-09-18"); } finally { globalThis.fetch = original; }
});
test("pending write guards secret and validation before KV writes", async () => {
  const memory = kv();
  assert.equal((await pendingCall("/api/intakes/pending/write", pendingPayload, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" })).status, 401);
  assert.equal((await pendingCall("/api/intakes/pending/write", pendingPayload, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "wrong")).status, 401);
  assert.equal((await pendingCall("/api/intakes/pending/write", pendingPayload, { CHAT_KV: memory }, "secret")).status, 501);
  for (const invalid of [{ ...pendingPayload, meetingId: "bad id" }, { ...pendingPayload, date: "bad" }, { ...pendingPayload, items: Array.from({ length: 101 }, () => pendingItem) }, { ...pendingPayload, items: [{ ...pendingItem, title: "" }] }, { ...pendingPayload, items: [{ ...pendingItem, tone: "bad" }] }]) assert.equal((await pendingCall("/api/intakes/pending/write", invalid, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret")).status, 400);
  assert.equal(memory.calls.put, 0);
});
test("pending write round-trips through the matching read key and TTL", async () => {
  const memory = kv(); const write = await pendingCall("/api/intakes/pending/write", pendingPayload, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret");
  assert.equal(write.status, 200); assert.equal(memory.calls.keys[0], "pending:v1:hr-systems-roadmap:2026-09-25"); assert.deepEqual(memory.calls.options[0], { expirationTtl: 1814400 });
  const original = globalThis.fetch; globalThis.fetch = async () => new Response(JSON.stringify({ message: "Not Found" }), { status: 404 });
  try { const read = await (await pendingCall("/api/intakes/pending", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).json(); assert.deepEqual(read.pending, { date: pendingPayload.date, items: pendingPayload.items, generatedAt: pendingPayload.generatedAt, sourceLabel: pendingPayload.sourceLabel, sourceDigest: pendingPayload.sourceDigest }); } finally { globalThis.fetch = original; }
});

// Phase 5 follow-up: on-demand "Pull roadmap now" button, replacing the earlier
// silent-schedule design. mockDefinitions() stands in for GitHub's Contents API
// response for data/meeting-definitions.json, needed by pullRequest()'s
// isActiveMeeting() check.
function mockDefinitions() {
  const definitions = { schemaVersion: 1, meetings: [{ meetingId: "hr-systems-roadmap", displayName: "HR Systems Roadmap", active: true }] };
  return async (url) => {
    if (String(url).includes("meeting-definitions.json")) return new Response(JSON.stringify({ content: btoa(JSON.stringify(definitions)), sha: "defs-sha" }), { status: 200 });
    return new Response(JSON.stringify({ message: "Not Found" }), { status: 404 });
  };
}
test("pull-request rejects an unknown or inactive meeting before touching KV", async () => {
  const memory = kv();
  const original = globalThis.fetch; globalThis.fetch = mockDefinitions();
  try {
    const response = await pendingCall("/api/intakes/pull-request", { meetingId: "not-a-real-meeting" }, { CHAT_KV: memory });
    assert.equal(response.status, 400);
    assert.equal(memory.calls.put, 0);
  } finally { globalThis.fetch = original; }
});
test("pull-request writes a requested state and pull-status reads it back", async () => {
  const memory = kv();
  const original = globalThis.fetch; globalThis.fetch = mockDefinitions();
  try {
    const write = await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    assert.equal(write.status, 200);
    assert.equal(memory.calls.keys[0], "pullstate:v1:hr-systems-roadmap");
    assert.deepEqual(memory.calls.options[0], { expirationTtl: 3600 });
    const status = await (await pendingCall("/api/intakes/pull-status", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).json();
    assert.equal(status.status, "requested");
  } finally { globalThis.fetch = original; }
});
test("pull-status returns idle with no prior request", async () => {
  const status = await (await pendingCall("/api/intakes/pull-status", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: kv() })).json();
  assert.equal(status.status, "idle");
});
test("pull-request blocks a second request while one is in flight, but allows one immediately after a failure", async () => {
  const memory = kv();
  const original = globalThis.fetch; globalThis.fetch = mockDefinitions();
  try {
    await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    const blocked = await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    assert.equal(blocked.status, 429);
    // Simulate the poller having reported a failure -- a fresh request should be
    // allowed straight away, no cooldown, matching "click to retry".
    await memory.put("pullstate:v1:hr-systems-roadmap", JSON.stringify({ meetingId: "hr-systems-roadmap", status: "failed", error: "boom", completedAt: new Date().toISOString() }));
    const retried = await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    assert.equal(retried.status, 200);
  } finally { globalThis.fetch = original; }
});
test("pull-request enforces a short cooldown after a successful pull", async () => {
  const memory = kv();
  const original = globalThis.fetch; globalThis.fetch = mockDefinitions();
  try {
    await memory.put("pullstate:v1:hr-systems-roadmap", JSON.stringify({ meetingId: "hr-systems-roadmap", status: "done", itemCount: 3, completedAt: new Date().toISOString() }));
    const blocked = await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    assert.equal(blocked.status, 429);
  } finally { globalThis.fetch = original; }
});
test("pull-request treats a stale requested/running state as abandoned and allows a fresh request", async () => {
  const memory = kv();
  const original = globalThis.fetch; globalThis.fetch = mockDefinitions();
  try {
    const staleTimestamp = new Date(Date.now() - 10 * 60 * 1000).toISOString(); // 10 minutes ago > PULL_STALE_MS
    await memory.put("pullstate:v1:hr-systems-roadmap", JSON.stringify({ meetingId: "hr-systems-roadmap", status: "running", requestedAt: staleTimestamp, startedAt: staleTimestamp }));
    const response = await pendingCall("/api/intakes/pull-request", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory });
    assert.equal(response.status, 200);
  } finally { globalThis.fetch = original; }
});
test("pull-claim guards secret before reading or writing state", async () => {
  const memory = kv();
  assert.equal((await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).status, 501);
  assert.equal((await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" })).status, 401);
  assert.equal((await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "wrong")).status, 401);
  assert.equal(memory.calls.put, 0);
});
test("pull-claim claims a requested state once, then reports not-claimed on a second call", async () => {
  const memory = kv();
  await memory.put("pullstate:v1:hr-systems-roadmap", JSON.stringify({ meetingId: "hr-systems-roadmap", status: "requested", requestedAt: new Date().toISOString() }));
  const first = await (await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret")).json();
  assert.equal(first.claimed, true);
  const stored = JSON.parse(memory.store.get("pullstate:v1:hr-systems-roadmap"));
  assert.equal(stored.status, "running");
  const second = await (await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret")).json();
  assert.equal(second.claimed, false);
});
test("pull-claim reports not-claimed when nothing was ever requested", async () => {
  const result = await (await pendingCall("/api/intakes/pull-claim", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: kv(), PENDING_WRITE_SECRET: "secret" }, "secret")).json();
  assert.equal(result.claimed, false);
});
test("pull-complete guards secret and validates before writing, then round-trips a done result", async () => {
  const memory = kv();
  assert.equal((await pendingCall("/api/intakes/pull-complete", { meetingId: "hr-systems-roadmap", status: "done", itemCount: 5 }, { CHAT_KV: memory })).status, 501);
  assert.equal((await pendingCall("/api/intakes/pull-complete", { meetingId: "hr-systems-roadmap", status: "done", itemCount: 5 }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" })).status, 401);
  for (const invalid of [{ meetingId: "hr-systems-roadmap", status: "bogus" }, { meetingId: "hr-systems-roadmap", status: "done", itemCount: -1 }, { meetingId: "hr-systems-roadmap", status: "done" }, { meetingId: "hr-systems-roadmap", status: "failed" }, { meetingId: "bad id", status: "done", itemCount: 1 }])
    assert.equal((await pendingCall("/api/intakes/pull-complete", invalid, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret")).status, 400);
  assert.equal(memory.calls.put, 0);
  const done = await pendingCall("/api/intakes/pull-complete", { meetingId: "hr-systems-roadmap", status: "done", itemCount: 35, date: "2026-09-18" }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret");
  assert.equal(done.status, 200);
  const status = await (await pendingCall("/api/intakes/pull-status", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).json();
  assert.equal(status.status, "done"); assert.equal(status.itemCount, 35); assert.equal(status.date, "2026-09-18");
});
test("pull-complete records a failed result with the error message, capped in length", async () => {
  const memory = kv();
  const longError = "x".repeat(1000);
  const response = await pendingCall("/api/intakes/pull-complete", { meetingId: "hr-systems-roadmap", status: "failed", error: longError }, { CHAT_KV: memory, PENDING_WRITE_SECRET: "secret" }, "secret");
  assert.equal(response.status, 200);
  const status = await (await pendingCall("/api/intakes/pull-status", { meetingId: "hr-systems-roadmap" }, { CHAT_KV: memory })).json();
  assert.equal(status.status, "failed");
  assert.equal(status.error.length, 500);
});
