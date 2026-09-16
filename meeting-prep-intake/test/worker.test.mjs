import test from "node:test";
import assert from "node:assert/strict";
import { eligibleCarryForward, validateIntake } from "../src/worker.js";

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
