---
name: tlm-team-knowledge
description: Answer any question about how the Telemax TEAM works — ticket process and board statuses, WIP limit, who to tag, EPIC template, QC naming ([QA][Module][TASK]/[BUG]), Slack etiquette, leave / OOO, the shared developer account and services (Vercel, GitHub org, Firebase, App Store Connect, Play Console), repositories, AI tooling onboarding — from the team-knowledge mirror first, then the team's ClickUp docs live. Its sync mode scans the ClickUp docs for new or edited pages, refreshes ai/team-knowledge/ and ships it straight to tlm-claude-plugins by PR. TRIGGER on team/process questions ("quy trình team", "ticket bị block thì sao", "nghỉ phép báo ở đâu", "status nào", "QC đặt tên ticket", "tài khoản chung", "credentials", "account nào để vào Vercel/Firebase", "repo nào", "onboard", "how does the team…"), and on "/tlm-team-knowledge sync", "sync team docs", "cập nhật knowledge từ ClickUp".
---

Team questions get answered from the team's own docs, never from general best practice. A plausible
answer that differs from the team's actual rule ("move it to Blocked" when the board has no such
status) is worse than "the docs don't say".

**Two modes**: **Answer** (default) · **Sync** (`/tlm-team-knowledge sync`)

The knowledge lives in `<rulesRoot>/ai/team-knowledge/` (`.claude/tlm-plugin/` when the project has a
live rules copy, else `${CLAUDE_PLUGIN_ROOT}`). `sources.json` there is the manifest: workspace,
scan scope, and every known doc with its mode and last-synced `updatedAt`.

---

## ANSWER

1. **Read the mirror** — `README.md`, then only the file(s) its table points to for this question.
2. **Answer from it** if it covers the question. Cite the source doc by title; quote status names
   exactly as written (they are the board's real names).
3. **Scan ClickUp live** when the mirror does not cover it, or the question names something the
   mirror lacks:
   - `clickup_search` with `asset_types: ["doc"]`, the question's keywords, and the manifest's
     `scope.spaceIds` as `location.projects` — **one** call, then `clickup_get_document_pages` on the
     best 1–3 hits. ClickUp has a daily call limit; don't read every doc.
   - A `link-only` doc (contacts, sprint reports) is always read live — that is the only way its
     content is used.
   - Answer from what the page says, naming the doc. Found nothing → say the team docs don't cover
     it and who to ask (Tony / Steph per `01-team-process.md`). Never fill the gap with a guess.
4. **Offer a sync** when the live scan found a doc that is newer than its `updatedAt` or missing from
   `sources.json` — one line, not a detour: "Doc *X* is newer than the plugin's copy — sync it?"

Never print a secret even if a live page contains one; say the page holds a credential and that it
should be removed from ClickUp.

---

## SYNC

Refresh the mirror from ClickUp and ship it upstream. **Preview → approval → write → diff → approval
→ PR.**

### S1 — Find what changed (2–3 calls)

- `clickup_search` with `asset_types: ["doc"]`, `location.projects: scope.spaceIds`, sorted by
  `updated_at` desc. Page through `next_cursor`.
- Keep hits whose folder (`hierarchy.category.id`) is in `scope.folderIds`, or that sit directly in a
  scoped space. Collapse multiple pages of one doc to the doc.
- Classify against `sources.json`:

| Class | Rule | Action |
|---|---|---|
| **NEW** | `docId` not in the manifest | Ask: mirror (into which file, new or existing) / link-only / ignore. Ignored docs go into the manifest with `mode: "ignore"` so they are not asked again. |
| **CHANGED** | hit `dateUpdated` > manifest `updatedAt` | Re-read and re-mirror (mirror) or just bump `updatedAt` (link-only). |
| **GONE** | in the manifest, not found by a direct `clickup_get_document_pages` | Ask before dropping the file content. |
| unchanged | — | Skip; don't fetch. |

Show the classification as one table and ask once (`AskUserQuestion`, one question per NEW doc).
Nothing changed → say so and stop.

### S2 — Rewrite the mirror

For each CHANGED / approved-NEW mirror doc, fetch the page(s) as `text/md` and rewrite its target file:

- **English**, same shape as the neighbours: a source blockquote, then the content as short sections.
  Keep the meaning; translate, don't reinterpret. Status names exactly as on the board, with the
  colored dot used in `01-team-process.md`.
- **Strip secrets** (passwords, API keys, tokens like `ctx7sk-…` / `figd_…`, 2FA codes, private keys)
  and **personal data** (phone numbers, personal e-mails, home addresses). Each strip is reported to
  the user with the doc name, so the lead can remove it from ClickUp too.
- Screenshots are dropped; keep the text around them.
- A new file gets the next number (`04-…md`) and a row in `README.md`'s table.
- Update `sources.json`: `updatedAt` = the page's `date_updated`, new entries with key/title/docId/
  pageIds/mode/file.

Write into the **rules root's** `ai/team-knowledge/` when the project has a live rules copy (it is in
effect at once). With no rules copy (Claude Desktop, a repo without `/tlm-project-setup`), copy
`${CLAUDE_PLUGIN_ROOT}/ai/team-knowledge/` into a staging dir under the scratchpad
(`<stage>/ai/team-knowledge/`) and write there — never into `${CLAUDE_PLUGIN_ROOT}`, which the next
plugin update overwrites.

### S3 — Review, then ship straight to tlm-claude-plugins

Same script as `tlm-rule-capture`, restricted to this one folder so nothing else in the rules copy
rides along:

```bash
export TLM_SYNC_DIRS=ai/team-knowledge TLM_BRANCH_PREFIX=knowledge/ TLM_BUMP=patch
export TLM_VENDOR_DIR=<rules copy dir, or the staging dir>     # + tlm.pluginRepo values if set
node <rulesRoot>/skills/tlm-rule-capture/plugin-pr.mjs diff   # REVIEW — show this to the user
```

Show the diff and **wait for the go-ahead** — this PR reaches the whole team. Then:

```bash
TLM_TITLE="knowledge: sync team docs from ClickUp (<doc titles>)" \
TLM_BODY="<one line per doc: NEW/CHANGED/GONE + title; list any stripped secrets as 'removed from mirror'>" \
node <rulesRoot>/skills/tlm-rule-capture/plugin-pr.mjs open team-docs-<YYYY-MM-DD>
```

`TLM_PR_MODE=gh` when `gh` is installed; otherwise `TLM_PR_MODE=api` with `GITHUB_TOKEN` exported
(the script sends it only in the Authorization header); otherwise it prints the compare URL. Report
the PR URL. With a rules copy, also commit the folder in the consuming repo.

---

## Never

- Answer a team question from general practice when the docs are silent.
- Mirror a secret or personal data, or paste one into the PR body.
- Hand-edit a mirrored file to change a process — change the ClickUp doc, then sync.
- Open the PR before the user has seen the diff.
