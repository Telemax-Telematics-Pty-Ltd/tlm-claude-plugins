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
