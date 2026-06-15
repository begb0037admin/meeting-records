# Rollover SOP — Team 1-1's

> This project uses the standard rollover procedure. See root `ROLLOVER_SOP.md` for the full one-page reference.

---

## When to roll
- Context > ~70% full
- Topic has shifted (e.g. moved from prep to post-meeting notes for a different person)
- Natural day/week boundary
- Session is becoming circular or confused

## When NOT to roll (yet)
- Mid-briefing with unsaved output
- < 10 minutes from completing the current person's section
→ Finish the micro-step, *then* roll.

---

## Team 1-1's Rollover Procedure

**1. STOP.** Acknowledge: "okay, rolling now."

**2. WRITE `docs/HANDOVER.md` FIRST.** Replace the file. Include:
- Which team member(s) were covered this session
- Any open actions raised but not yet logged
- Exactly where to pick up next

**3. UPDATE `docs/STATUS.md`.**
- Bump "Last updated"
- Refresh team cadence table (Last 1-1 / Next 1-1)
- Refresh In Progress / Blocked / Up Next

**4. SAVE THE BRIEFING** to `docs/sessions/YYYY-MM-DD-1on1-briefing.md` if a standard run was completed.

**5. COMMIT.** `git add docs/ && git commit -m "1-1 briefing YYYY-MM-DD"`

---

## Clone Bootstrap (next session)
1. Read `CLAUDE.md`
2. Read `docs/STATUS.md`
3. Read `docs/HANDOVER.md`
4. State the session goal. Begin work.
