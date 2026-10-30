# 02 — Services, repositories and access

> **Sources**: ClickUp docs **Services & Credentials** (`services-credentials`) and **Telemax random
> guideline** (`random-guideline`) — see `sources.json`. ClickUp wins on any disagreement.
>
> **No secret is ever mirrored here** — no password, API key, token or 2FA code. If a source page
> contains one, the sync drops it and tells the lead to remove it from ClickUp.

## Shared developer account

- **developer@telemax.com.au** is the shared account for the team services below. Don't create these
  with a personal account — what the team builds, deploys or releases must survive someone leaving.
- Access to the account: ask **Tony / Steph** (shared through a secure channel, never in chat).

| Service | Used for |
|---|---|
| Vercel | Hosting / deployments for web projects |
| GitHub org (common) | `Telemax-Telematics-Pty-Ltd` |
| Firebase | App distribution, push, mobile backend (Installer / Fleet apps) |
| App Store Connect | iOS builds, TestFlight, App Store releases |
| Google Play Console | Android builds, testing tracks, Play Store releases |

Per-developer tokens (Figma, Context7, …) are personal: local `.claude/settings.local.json` / `.env`
only, never committed, never pasted into ClickUp / Slack / a prompt.

## Repositories

| Where | Repo | What |
|---|---|---|
| Azure DevOps | `Telemax2` (`dev.azure.com/ashphayer/_git/Telemax2`) | Main .NET system; OpenSpec folder at `/openspec` on `dev` |
| GitHub | `Telemax-Telematics-Pty-Ltd/telemax-mintlify` | Docs site |
| GitHub | `Telemax-Telematics-Pty-Ltd/Telemax-Ops` | Ops app (`staging` branch) |
| GitHub | `steph-telemax/telemax-install-app` | Installer mobile app (`develop` branch) |
| GitHub | `Telemax-Telematics-Pty-Ltd/tlm-claude-plugins` | This plugin |

## Apps & environments

- **Telemax Orders (staging)**: `https://telemax-orders-staging.vercel.app/` — Telemax-Ops repo, on
  Vercel. The staging admin login is on the ClickUp page *Telemax Ops — Orders & Customer Portal*
  (read it live; not mirrored).
- **Telemax Customer Portal (staging)**: `https://telemax-portal-staging.vercel.app/` — customers reach
  it from the dashboard `https://dashboard-stage.telemax.com.au/` → **Manage account**.

- **Installer / Fleet management apps** — Firebase App Distribution (Android) and App Store Connect
  (iOS). Ask Steph / Tony for access.
- **SMS command page (stage)**: `https://dashboard-stage.telemax.com.au/commands/sms`
- **Karmo vehicles** reference material: Google Drive folder linked from the random-guideline doc.
