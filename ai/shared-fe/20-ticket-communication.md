# Ticket communication — cite the source of truth, spell out every test case, ask the PO to confirm decisions

Applies to every text that discusses requirements or tests on a tracker ticket (ClickUp comment,
threaded reply, ticket description, QA question, bug report, rollup) **and** to the same discussion
in chat with the user.

## The rule

**1. Cite the single source of truth.** A statement about what the system must do (a layout, a label, a
field, a rule, an expected result) names where it comes from:

- **Figma** — the node link (`…?node-id=<id>`) plus the frame / layer name, and the value read from it
  ("Figma *Alert report / Header* (node 12:345): title is Montserrat SemiBold 20, text `Alert Report`").
- **Artifact** — the published spec / test-analysis / design page link, plus the section or row.
- **The ticket itself** — the acceptance-criteria line or the PO/BA comment (quoted, with its author
  and date).

When sources disagree, say which one wins and why (Figma and the PO's written decision beat the
ticket's older text; the newest PO/BA statement beats an older one) — never silently pick one. When no
source covers the point, say so and ask; never present a guess as the requirement.

**2. Write the test case out, never only its ID.** A reference to a test case carries its content,
not just `TC-007`:

```
TC-007 — Export XLSX with a date range of 31 days
  Precondition: company 410, vehicle "Truck 12", alerts on 1–31 Oct
  Steps: Reports → Alert report → range 01/10–31/10 → Export XLSX
  Expected: file downloads; header row matches Figma node 12:345; 31 day groups
  Source: Figma <link> / checklist #12
```

At minimum: **ID + title + expected result + source**. Add precondition/steps when the reader needs
them to re-run it. The same holds for checklist numbers (`#12`), bug ids and acceptance-criteria
numbers: write what the item says next to its number.

**3. A Q&A for the PO: decided items list the decision; only undecided items list options.** When a
change needs the PO's sign-off before release (behaviour the ticket left open, an edge case dev had to
settle), sort every item into one of two groups:

- **Decided by dev → the decision only.** A short plain-language **question** plus **"Dev decision:"** —
  the behaviour already built — with an example when it is not obvious. No "A or B?", no
  "Alternative: …", no "(recommended)": the PO confirms or overrides, they don't re-design a built
  behaviour.
- **Not decided yet → the most feasible options.** Only when dev genuinely cannot settle it (a business
  call, a wording the PO owns): list the **2–3 most feasible options**, each with what the user would
  see, under a separate *Open — need your choice* heading. Dev's lean, if any, in one line. No long
  tail of unlikely options.

```
M2. After an alert, when does the next one fire?
    Dev decision: the count restarts from 0; the next alert needs another N km within 7 days.
    E.g. a 1000 km limit and a vehicle doing 2000 km/week → about 2 alerts/week.

Open — need your choice
Q1. A rule has no recipient left (all were removed). What happens when it fires?
    a) Send it to the account owner.
    b) Show it in-app only; no email/SMS/push.
```

- **Label the item codes once.** A prefix per area (`M` = Mileage alert, `R` = Road Surface alert) and say
  what the prefix means in the heading, so `M2` means something to a reader who never saw the list.
- **Say how to reply and what it blocks.** Open with: reply **"OK all"**, or **"OK except M2, R5"** plus the
  behaviour wanted instead, **plus a pick for each open item** — and that release waits on this reply.
- **Keep "no action needed" apart.** Consequences the PO should know but not decide (existing rules
  start firing, CS to be told) go under a separate *Notes* heading, each with who does what.
- Put the Q&A in the **ticket description** (it is the current state, edited as answers come in), and a
  short comment tagging the PO that points to it.

## Why

The reader of a ticket comment — PO, QC, the next developer, the client — does not have the Excel,
the checklist or the Figma frame open. `TC-007 failed` or `per #12` sends each of them to look it up
before they can even agree or disagree, and a lookup against a sheet that has since been renumbered
lands on the wrong case. A requirement stated without its source can't be checked and gets argued from
memory; quoting the Figma node / artifact section ends that argument in one read and lets anyone see
when the design changed after the comment was written.

A decided item written as options hands the design back to the PO: they weigh trade-offs they did not
build, the reply comes back as a third option nobody coded, and release slips while it is re-built. The
opposite mistake is as costly: an item dev could not settle, presented as "Dev decision", gets a
rubber-stamp "OK" on a call nobody actually made — so a genuinely open item shows its few real options. Bare
codes (`M1`, `Q-A`) and engineering wording force the PO to ask what the question even is — one more
round-trip before a "yes". Stating the built decision turns the round into one read and "OK all", and an
override names the exact item to change.

## Examples

❌ `TC-003, TC-007 fail on staging. TC-011 blocked.`
✅ `TC-003 "Alert list shows the vehicle name" — fails: column is empty (expected per Figma node 12:345).`
   `TC-007 "Export XLSX, 31-day range" — fails: header row differs from Figma (screenshot attached).`
   `TC-011 "Schedule weekly report" — blocked: no staging company with a weekly schedule.`

❌ `Answer to #4: yes.`
✅ `#4 "Should suspended companies appear in the filter?" — Yes, greyed out (PO, comment 2026-11-03).`

❌ `The title should be bold.`
✅ `Title: Montserrat SemiBold 20 / 28 (Figma "Report header", node 12:345) — the ticket text says
   "bold", Figma wins.`

❌ `Q-A. "Left unsealed" when the trip ends on gravel: own wording "Trip ended on an unsealed road"
   (recommended), or one neutral wording "Unsealed stretch ended"?`
✅ `R5. A trip ends while the vehicle is still on an unsealed road — what does the "left unsealed road"
   alert say? Dev decision: its own wording, "Trip ended on an unsealed road — X km".`
   (Dev had built this wording, so it is a decision, not a choice.)

❌ `Dev decision: TBD` — or a list of six variants for one open item.
✅ `Q1 (open). Alert wording is the PO's call: a) "Trip ended on an unsealed road — X km"
   b) "Unsealed stretch ended — X km". Dev leans a): it says why the stretch ended.`

## Exceptions

- A **table** whose columns already carry the case title and expected result may use the ID as the
  row key — the content is on the same row.
- A follow-up reply in the **same thread** may refer to a case already written out in full in the
  comment it answers.
