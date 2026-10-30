# Team knowledge — how the Telemax team works

> **Applies to**: any question about the **team**, not the code — ticket process and statuses, who to
> ping, QC naming, Slack etiquette, leave / OOO, shared accounts and services, repositories, AI tooling
> onboarding.

These files are a **mirror** of the team's ClickUp docs, so Claude can answer a team question without a
tracker call. The ClickUp docs stay the source of truth: the `tlm-team-knowledge` skill answers from
here first, scans ClickUp live for what is missing or stale, and its `sync` mode refreshes this folder
and ships it upstream by PR, so a new or edited doc reaches every teammate's plugin.

| File | Covers | ClickUp source (`sources.json` key) |
|------|--------|-------------------------------------|
| [01 — Team process](01-team-process.md) | Board statuses + colors, daily routine, WIP limit, ownership, EPIC template, QC naming, Slack, leave & OOO | `team-process` |
| [02 — Services & access](02-services-and-access.md) | Shared developer account (Vercel, GitHub org, Firebase, App Store Connect, Play Console), repositories, app links | `services-credentials`, `random-guideline` |
| [03 — AI tooling](03-ai-tooling.md) | Installing this plugin, connectors, `/tlm-project-setup`, AI use cases | `plugin-guide`, `ai-useful-skills` |
| *(link only)* | Team member contacts | `team-contact` — personal data, read live, never mirrored |
| *(link only)* | Sprint reports | `sprint-reports` — read live |

## Rules for this folder

- **Never mirror a secret** — password, API key, token, 2FA code. A source page that contains one is
  mirrored without it, and the lead is told to remove it from ClickUp.
- **Never mirror personal data** (phone numbers, personal e-mails, addresses) — `link-only` docs.
- **Don't hand-edit a mirrored file** to change a process: change the ClickUp doc, then sync. A hand
  edit is overwritten by the next sync and never reaches the doc people actually read.
- `sources.json` is the manifest: which docs are mirrored, into which file, and the ClickUp
  `date_updated` at the last sync (that is how staleness is detected).
