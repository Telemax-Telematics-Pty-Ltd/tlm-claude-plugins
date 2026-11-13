# Change review checklist: server, Blazor, tests, jobs, docs, PR

> **Applies to**: every `Telemax2` change before it is pushed or reviewed (self-review, `/tlm-code-review`,
> cross-review, PR comments). Each item is a generic failure that a real review caught; the tag at the end
> of a line is its source, not part of the rule.

**Rule (MUST):** walk the sections that match the diff and tick each item, or write in the PR why it does not
apply. An unticked item that applies is a review finding, not a nit.

**Why (the failure it prevents):** these defects compile, pass the happy-path test and look fine in a demo.
They show up later as a wrong page of results in a second tab, a job that fails without telling anyone, a 500
on an extreme date, or a doc that the next agent enforces although the code says the opposite.

---

## 1. Server / C#

- [ ] **Paged results from a server cache are keyed by one run.** The first page mints a run id; the client
      echoes it on every "Load more". A key built from the request minus its cursor lets two tabs or a re-run
      overwrite each other's snapshot. (e.g. TLM-4144 PR 2121)
- [ ] **A continuation whose snapshot is gone restarts** (tell the client to reload from page 1); it never
      slices a fresh recount, which skips or repeats rows. (PR 2121)
- [ ] **A capped best-effort pass ("at most N per run") cannot starve.** Items that can never succeed must
      not fill the budget every run: spread N across owners (round-robin) or remember known failures. (PR 2121)
- [ ] **A capped path agrees with the uncapped sibling** it claims parity with: same filter, same order,
      same result for a set smaller than N. (PR 2121)
- [ ] **User-supplied dates are bounds-checked before arithmetic.** Validate against the domain window
      (e.g. retention) *before* `AddDays`, `DateOnly` → `DateTime` or local → UTC, so an extreme value
      answers 400, not 500 (`ArgumentOutOfRangeException`). (PR 2121)

## 2. Background jobs and email

- [ ] **Every path that marks a job Failed can still build and send the failure email** — including
      input-parse failures, cancellations and a crash before the first row. (PR 2121)
- [ ] **Stored input is re-parsed with the same guard the run used.** The email/retry path must not
      re-deserialize the job input unguarded and throw where the run did not. (PR 2121)
- [ ] **A builder/template exception is not a provider refusal.** Only the provider's own reject goes to
      the retry path; a bug in building the message fails fast and is logged as ours. (PR 2121)
- [ ] **The test asserts the email** (sent, recipient, failure wording), not only the job's final state.
      (PR 2121)

## 3. Blazor client

- [ ] **Shared load task assigned before the first await.** An event handler that reloads data
      (company switch, filter reset) sets the shared `Task` field *before* its first `await`, so a
      concurrent `OnParametersSetAsync` / deep-link handler awaits the new load, not a stale completed
      one. (PR 2121)
- [ ] **Sibling pages already fixed the same race?** Reuse their pattern; grep the sibling pages before
      inventing a new one. (PR 2121)
- [ ] **A caught load failure tells the user.** If the catch leaves the screen empty, show the toast the
      sibling screens show; a console-only log is a finding. (PR 2121)

## 4. Tests

- [ ] **Every export writer that converts units has a non-default-unit test** (e.g. miles when the
      default is km) asserting the headers *and* the converted values. A writer without one is a finding.
      (PR 2121)
- [ ] **Each new guard has a test at the production entry point** that fails with the guard removed —
      e.g. the extreme date answers 400, the gone snapshot restarts, the failed job sends its email.

## 5. Docs, comments and spec

- [ ] **Comments and docs state the decision this change implements.** No comment telling the next feature
      to do what this change deliberately does not (e.g. "auto-enable the flag"). (PR 2121)
- [ ] **A cache or contract doc moves with the code**: TTL, sliding vs fixed expiry, restart and eviction
      semantics, key shape. (PR 2121)
- [ ] **"Proof" columns cite real test names.** After any rename, `git grep` every test method a design or
      spec cites. (PR 2121)
- [ ] **Rollback / cutover SQL covers every state the old code can still pick up** — pending emails and
      retries too, not only queued/running jobs. (PR 2121)
- [ ] **A deviation from the ticket** (page count, behaviour, scope) is an open question to the BA, or
      carries the BA's written OK on the ticket — a note in the design is not enough. (PR 2121)

## 6. PR description and scope

- [ ] **Changes outside the ticket are listed** — shared components, other reports, global styles — each
      with its regression scope. (PR 2121)
- [ ] **A flag-gated feature ships no ungated change silently.** Anything that runs with the flag off is
      called out in the PR. (PR 2121)
- [ ] **Template filled, no placeholders left.** (PR 2121)
- [ ] **Deploy / cutover order written**, plus a pod / image-version check before any flag is enabled.
      (PR 2121)
- [ ] **Rollback SQL included** when the change adds tables, states or migrations. (PR 2121)
- [ ] **Review verdict filled** whenever its box is ticked. (PR 2121)
- [ ] **Full test-suite result on the final commit** (not an earlier one). (PR 2121)
- [ ] **Evidence tasks recorded**, or explicitly moved to stage with a reason
      ([`06`](06-e2e-before-after-evidence.md)). (PR 2121)
- [ ] **`git diff --check` is clean** — no trailing whitespace, no blank line at end of file. (PR 2121)

---

## Exceptions

- A section that does not match the diff (no jobs, no Blazor) is skipped; say so in one line.
- An item the PO/BA decided against is kept unticked with a link to that written decision.
