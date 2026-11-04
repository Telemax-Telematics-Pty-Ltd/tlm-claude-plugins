# Ticket communication — cite the source of truth, spell out every test case

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

## Why

The reader of a ticket comment — PO, QC, the next developer, the client — does not have the Excel,
the checklist or the Figma frame open. `TC-007 failed` or `per #12` sends each of them to look it up
before they can even agree or disagree, and a lookup against a sheet that has since been renumbered
lands on the wrong case. A requirement stated without its source can't be checked and gets argued from
memory; quoting the Figma node / artifact section ends that argument in one read and lets anyone see
when the design changed after the comment was written.

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

## Exceptions

- A **table** whose columns already carry the case title and expected result may use the ID as the
  row key — the content is on the same row.
- A follow-up reply in the **same thread** may refer to a case already written out in full in the
  comment it answers.
