# E2E evidence: one before/after image per ticket

> **Applies to**: verifying a `Telemax2` fix end to end (a QC bug, a subtask, a ticket), locally against staging
> or on staging after the deploy, and posting that evidence to the tracker. Mirrored from the Telemax2 repo's
> `.claude/rules/e2e-before-after.md` (branch `dev`).

**Rule (MUST):** the evidence of an end-to-end check is **one image per ticket** with the "before" and the "after"
side by side, titled, captioned and with the changed area boxed. Never loose screenshots.

- **Before** = staging, the current build, on the data QA used (their company, vehicle and dates). It must
  reproduce the reported bug. **After** = the fix branch run locally (dashboard on :8080/:50800 and, for
  reports/exports, `Telemax.ReportsService.Api` on :5014, as `ReportServiceUrl` in user-secrets), or staging once
  deployed.
- **Same Playwright spec for both runs**, asserting the ticket's **Expected Result**: before fails on the bug, after
  passes. A test that fails for another reason (selector, data, timeout) is a script error: fix it, don't post it.
  Name the screenshots `before-*.png` / `after-*.png` so the two runs never overwrite each other.
- **The image says what it shows.** A reader who never opened the ticket must understand it:
  - `--title "TLM-<n>: <the case in a few words>"` and `--caption` lines: `Expected: …` (from the ticket),
    `Before: …` (what staging shows), `After: …` (what the fix shows), and the data used (company, vehicle, dates).
  - **Box the changed area.** At screenshot time, write the bounding box of the element that changed (the row, the
    tile, the field: `locator.boundingBox()`) to a sidecar `<screenshot>.box.json`:
    `[{"x":…,"y":…,"w":…,"h":…,"label":"Days included"}]`. The composer draws it red on before, green on after.
    Box the same element on both sides; when it is gone after the fix (e.g. a hidden row), box where it was.
  - **Box the input too.** When the case starts from something typed or picked (a search box, a filter, a form field),
    box that control as well (`label: "Input"`), assert its value before the screenshot, and add the caption
    `Input: "<value>" typed in <where>`: two result lists mean nothing without what produced them (TLM-6236).
  - **Nothing is drawn over the screenshot.** The composer draws each box as an outline inside the element's own edge
    and lists the box names in the band above each column ("Boxed: Input · Suggestions"). A label painted above a box,
    or an outline drawn outside it, covered the field label and the typed value (TLM-6236). Zoom into every box of the
    composite before posting: field labels, the typed value and neighbouring rows must read clearly.
- **Compose** with `compose_before_after.py OUT.png BEFORE.png AFTER.png [BEFORE2 AFTER2 ...] --title … --caption …`
  (before left, after right; extra pairs stack, e.g. Alert and Fleet Alert). The script ships with this rule at
  `ai/telemax2-knowledge/scripts/compose_before_after.py` under the rules root (Telemax2 also keeps a copy at
  `.claude/scripts/`); it needs Pillow. Evidence that is not on screen (an exported file's cells, a header) gets a
  rendered table image of the before/after values instead, with the same title and captions.
- **Look at each composite before posting.** Attach it to its ticket (`clickup_request_attachment_upload`) with a
  comment: environment, data used, what before showed, what after shows, the fix commit. The parent ticket gets a
  results table (one row per test, before/after columns, totals) plus every composite.
- Spec, screenshots and composites live in the e2e workspace (`../Telemax2_e2e`), never in the Telemax2 repo.
- Never put credentials or session tokens in a spec, a screenshot or a comment.

**Why (the failure it prevents):** loose screenshots on a ticket only make sense to whoever took them. QA and the PO
open the ticket, see two similar-looking pages and cannot tell which is the old build, what was supposed to change,
or whether the data even reproduces the bug. A screenshot of a test that failed for a selector or a timeout looks
exactly like a real regression. One composite per ticket, with the expected result in the caption and the changed
area boxed, is readable in a few seconds by someone who never opened the ticket, and pairing it with one spec that
fails before and passes after proves the fix rather than just showing a page.

---

## ❌ Don't

```text
Attachments: screenshot1.png, screenshot2.png, Screen Shot 2026-11-09 at 14.02.png
Comment: "Tested, works now."
```

No way to tell before from after, which data was used, or what "works" means.

## ✅ Do (illustrative values)

```bash
python3 compose_before_after.py TLM-1234-evidence.png before-vehicle-id.png after-vehicle-id.png \
  --title "TLM-1234: External API returns the public vehicle ID" \
  --caption "Expected: vehicleId is the public ID shown on the dashboard" \
  --caption "Before: staging returns the internal numeric ID" \
  --caption "After: the fix returns the public ID" \
  --caption "Data: <company>, <vehicle>, <dates QA used>"
```

Attached to TLM-1234 with a comment naming the environment, the data, before/after and the fix commit.

## Exceptions

- A change with nothing observable end to end (a refactor, a log line, an internal job with no visible output) gets
  no composite; say in the ticket why there is no e2e evidence.
- When the bug cannot be reproduced on staging, do not post a "before" that passes: report that it does not
  reproduce, with the data tried, and ask QA for theirs.

## Three columns, not two: design → before → after

When the change has a design, the evidence has **three** columns, in that order. The design is not decoration: holding
it beside the two builds is what catches a difference nobody filed. On TLM-4148 it surfaced two — the PDF frames draw a
`Vehicle` item the build drops, and one frame omits a `Days included` item the build prints. Both were deliberate and
already written into the code; neither had ever been put in front of a reviewer.

Export the frame from the design tool itself (its REST API, at 2x), not a screenshot of someone's screen, and link the
node so a reader can open it. When no frame covers a case, say so in that column — "no frame draws this" is information;
an empty cell is not.

## Evidence that is not on screen

An exported file (PDF, XLSX, CSV) is compared **cell by cell from the file**, read with a text extractor, *and* shown as
a rendered page image. The cells are the proof; the page is what makes it reviewable. Giving only one of the two makes a
reviewer either squint at a screenshot or trust a table they cannot place.

Two traps, both of which cost a full run each:

- **Export the artifact that can carry the claim.** Testing "the export keeps the grouping" against a format the spec
  says names no grouping proves nothing, however green it looks. Check what the requirement says each format carries
  before choosing one.
- **Parse by column position, not by whitespace.** A layout extractor separates narrow columns by a single space, so
  splitting on runs of spaces silently merges two cells and the two sides look different when they are not.

## A case the data cannot reach is not a failure

When a threshold, a volume or a date range puts a case out of reach on the environment you are on, the report says
**"not reachable here, and this is what would reach it"** — not "fail", and never a quiet pass. Then reach it somewhere
else: seed the volume locally and say in the evidence that this row was proven on a seed and why. A row that reads
"covered locally because staging holds 660 of the 5,000 rows needed" is worth more than a red mark nobody can action.

## Turn "flaky" into a number

"It sometimes does not work" is not something anyone can act on. Write the repetition into the test: press the control
every way it can be pressed, count how often it behaves, and put the count in the failure message. On TLM-4148 a control
that had misbehaved in three runs measured **7 of 7** once the test stopped clicking while a previous overlay was still
open — which turned a suspected defect into a fixed test, and saved a person from hunting something that was not there.

## When a test drives an API, print what it actually got

A poll that reports "it never finished" when the call answered `401`, `404` or an HTML fallback page costs run after run.
Put the real status and the first part of the body in the assertion message. Better still, prefer the path a user takes:
the UI needs no knowledge of which controller serves which report, how an enum serialises, or which header carries the
token — and it is what the requirement is written about.

## Environment parity is where specs die

A spec written against a local host usually fails on staging for reasons that have nothing to do with the change:

- timeouts sized for a local run expire **before the first assertion**, so the report says nothing at all;
- a value formatted per company (a date, a unit) breaks a parser that assumed one format, and reads as a product bug;
- company and vehicle hardcoded to one environment's seed;
- a route or an element that exists on one build and not the other.

Make the spec take its data per target, verify a step took effect instead of assuming the click landed, and keep the
reason in a comment where the next person will hit it.

## Keep the whole document true

When a run adds a results section, re-read every older section in the same document. A page whose new table says
"passed on staging" while an older card still says "needs stage" is worse than one that says nothing: the reader
believes whichever is nearer. Reconciling the old section is part of posting the new one.
