---
name: tlm-feature-brief
description: Summarize a ticket tree for the people who watch it, posted as a ClickUp comment. On a feature (parent) ticket — read it and ALL its sub-tickets (descriptions, comments, threaded replies, statuses) and write a ~400-word client brief (what's included, use cases, quality, decisions needed) as ONE comment on that ticket. On a sub-ticket — write a short status rollup of that sub-ticket and post it as ONE comment on its PARENT. Both comments are updated in place on re-run. TRIGGER on "tóm tắt cho KH", "tổng hợp tính năng cho khách", "tính năng này đã build những gì", "feature brief", "client summary TLM-1234", "summarize vào parent", "roll up lên ticket cha", "rollup TLM-1234", and right after any skill posts a comment on a ticket that has a parent.
---

One command, two modes — picked from the ticket you give it:

| Ticket given | Mode | Reads | Writes | Posted on |
|---|---|---|---|---|
| has sub-tickets, no parent | **Brief** | the ticket + every descendant | ~400-word client brief | that ticket |
| has a parent | **Rollup** | that sub-ticket + its own children | ~80–150-word status | its direct parent |

**Pre-flight → Pick the mode → Collect → Reconcile → Draft (approve) → Post**

A **reporting skill**: it reads the tracker only — never the codebase — and writes exactly one
comment per run. The reader is the client or PO, not a developer: what they get, how they use it,
whether it is proven, what they must decide.

**Input**: a ticket id (`TLM-2807`) or URL; optionally `brief` / `rollup` to force a mode, a word
limit, a language (default `tlm.tickets.commentLanguage`, else English).

---

## PHASE 0 — PRE-FLIGHT

Read `tlm.tickets` from `.claude/settings.local.json` (fall back to `.claude/tlm.local.json`). Key
meanings: `${CLAUDE_PLUGIN_ROOT}/setup/tlm-config.reference.json`. Needed: `system` (this skill
supports `clickup`), `workspaceId`, `commentLanguage`.

Confirm the ClickUp MCP is reachable (**ToolSearch**: `clickup_get_task`, `clickup_get_task_comments`,
`clickup_get_threaded_comments`, `clickup_create_task_comment`, `clickup_update_comment`).

**Tickets is an all-or-nothing capability.** If the MCP is unreachable or `tlm.tickets.enabled` is
false, stop and point to `/tlm-project-setup` — never write a summary from memory.

---

## PHASE 1 — PICK THE MODE

Fetch the ticket (`include: ["description", "subtasks", "linked_tasks", "attachments"]`).

- **No parent** → **Brief** on this ticket.
- **Has a parent** → **Rollup** to the parent. Also fetch the parent (name, custom id, status).
- The user said `brief` on a sub-ticket → walk up to the top-most parent and run **Brief** there.
- The user's words were client-facing ("cho KH", "client summary") but the ticket has a parent →
  ask once: *"TLM-xxxx is part of TLM-yyyy '<name>'. Brief the whole feature, or roll this
  sub-ticket up to its parent?"*

---

## PHASE 2 — COLLECT

**Brief**: the ticket and **every** descendant, depth-first — sub-tickets of sub-tickets too (a
follow-up often has its own `[QA]` child). **Rollup**: the sub-ticket and its own descendants.

| What | How |
|---|---|
| Name, status, assignees, dates | `clickup_get_task` with `include: ["description", "subtasks", "attachments"]` |
| Every comment | `clickup_get_task_comments`; page with `start`/`start_id` until no more come back |
| Every reply | `clickup_get_threaded_comments` for each comment with `reply_count > 0` |
| Linked (non-child) tickets | name + status only — list, never fold their scope in |

Fetch siblings in parallel. Never stop at the first page or skip threads: the latest decision is
often a reply (a QC re-test PASS under the dev's comment). Skip comments that are earlier output of
this skill (PHASE 5 markers) — they are summaries, not sources.

Report coverage before drafting: *"Read N tickets, M comments, K replies."*

---

## PHASE 3 — RECONCILE

1. **Classify each ticket by its name/role:**
   - `[BA]` / exploration / spec → background only; never a feature line.
   - `[QC]` / `[QA]` / verify / test → **Quality** / **Verified**.
   - build ticket or follow-up → **What's included** / **Done** if its status is done
     (`ready for production`, `deployed to prod`, `Closed`, `complete`), else **In progress**.
   - bug raised during testing → Quality ("issue found → fixed"), not a feature.
2. **The newest statement wins.** Use the latest date, decision and verdict; never a superseded one.
3. Features come from the dev's "ready for QC / deployed" comments and the description, re-worded as
   what a user can now do. Verification comes from **QC's** comments — their verdict and environment.
4. **Open questions** = any "please confirm", "needs a decision from PO/BA", "is this acceptable"
   with no later answer → **Decisions needed** / **Open**, with the team's proposal and who it waits on.
5. **Use cases** (Brief only) — 3–4, each built on a **concrete example from the tickets** (a real
   model name, a real duplicate that was merged), never a generic sentence.
6. **Client status words:** `ready for production` → "Ready for production", `deployed to prod` →
   "Live", QC/staging statuses → "In testing", `Closed`/`complete` → "Done", else "In progress".

**Leave out** — noise to a client, and some of it internal: PR numbers, branch/class/file names,
`file:line`, migrations, cache TTLs, log levels, UTC arithmetic, DB rows, who-said-what, developer
names, internal test files, any token, key or internal URL. Deploy prerequisites stay out unless the
user asks for an internal version.

---

## PHASE 4 — DRAFT

Language as chosen (default English), Markdown, no emojis. Count words with `wc -w` on the draft —
do not estimate.

### Brief (~400 words, ±10%)

Budget: Summary ~60 · What's included ~120 · Use cases ~100 · Quality ~60 · Decisions + Next ~60.
Cut **Quality** first when over. Omit a section that would be empty.

```markdown
# <Feature name in plain words>

**<ROOT-ID> · Status: <client status> · Updated <d MMM yyyy>**

## Summary
<2–3 sentences: the problem before → what the system does now → the safeguard, if any>

## What's included
- **<Capability>:** <what a user can now do, one line>

## Use cases
1. **<Situation>:** <concrete example from the tickets → outcome>

## Quality
- <test round / environment / verdict>
- Issue found in testing: <issue> — fixed (<measured result if the tickets give one>)

## In progress
- <item — status>

## Decisions needed
- **<Question>:** <one line> — we suggest <team's proposal>.

## Next
<release / first scheduled run / what happens after go-live>
```

### Rollup (~80–150 words)

Drop a line that has nothing to say.

```markdown
**Rollup: <SUB-ID> <sub-ticket name>**
Status: <client status> · Updated <d MMM yyyy>

- **Done:** <what this slice delivered, in user terms>
- **Verified:** <QC/QA verdict + environment, or "not yet tested">
- **Open:** <unanswered question / blocker, and who it waits on>
- **Next:** <next step and date if the comments give one>
```

Show the draft with the coverage line and word count, and **wait for approval** before posting.

---

## PHASE 5 — POST (one comment, kept current)

| Mode | Target ticket | An earlier comment is the one that starts with |
|---|---|---|
| Brief | the root | `# ` on line 1 and `**<ROOT-ID> · Status:` on line 2 |
| Rollup | the direct parent | `**Rollup: <SUB-ID> ` |

1. Found → `clickup_update_comment` with the new text. Not found → `clickup_create_task_comment`
   on the target (`notify_all: false`).
2. Confirm with the target's ticket link.

**After a Rollup:**
- The parent itself has a parent → ask whether to roll it up one more level. Never cascade silently.
- The root already carries a Brief → offer once: *"The brief on <ROOT-ID> may be out of date —
  refresh it?"* On yes, run this skill in Brief mode on the root.

---

## RULES

- Never post without the user's approval of the text.
- Never change a ticket's status, assignee or fields — comments only.
- Brief goes on the root, Rollup on the direct parent — never on the ticket being summarized in
  Rollup mode.
- An id that does not resolve → say so and ask; never guess a parent.
