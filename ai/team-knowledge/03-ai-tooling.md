# 03 — AI tooling onboarding (tlm-claude-plugins)

> **Sources**: ClickUp docs **tlm-claude-plugins guide** (`plugin-guide`) and **AI useful skills**
> (`ai-useful-skills`) — see `sources.json`. Both are mostly screenshots; this is the text part.

## Install

1. Claude Desktop → **+** → add plugins → add marketplace
   `https://github.com/Telemax-Telematics-Pty-Ltd/tlm-claude-plugins`, or in Claude Code:
   ```
   /plugin marketplace add Telemax-Telematics-Pty-Ltd/tlm-claude-plugins
   /plugin install tlm-claude-plugins@tlm-claude-plugins
   ```
2. Create a folder for plugin usage and open it in Claude.
3. Connect the **ClickUp, GitHub and Slack** Claude connectors. Context7 and Figma (Framelink) need a
   personal key — ask Tony; it goes into your local settings, never into a doc or a commit.
4. Run `/tlm-project-setup` and register the projects: Telemax2 (Azure, `stage`),
   telemax-install-app (`develop`), Telemax-Ops (`staging`).
5. QA: run `/tlm-qa-workflow` to set up the QA environment.

## Use cases shown in "AI useful skills"

- **Mobile — dev done**: ClickUp comment with video/images → deployment summary, confirmed before it
  is posted on the ticket.
- **Mobile — release notes**: `tlm-mobile-release-notes` (autoloads on a commit range).
- **Mobile — one-shot prompt**: ticket → implementation → Slack summary.
- **FE**: screen from Figma with a self-mocked API boilerplate (`tlm-figma-to-code`).
