# 01 — Team process (tickets, QC, Slack, leave)

> **Source of truth**: ClickUp doc **Telemax Team Process** — see `sources.json` (`team-process`).
> This file is a mirror for answering team questions offline. When it and ClickUp disagree, ClickUp
> wins: re-sync (`/tlm-team-knowledge sync`) instead of editing this file by hand.

Status names below are the **real** Telemax2 board statuses (space-level), with the board's color so a
reader can match the badge they see in ClickUp.

| Status | Board color | Meaning in this process |
|---|---|---|
| ⚪ **TO DO** | `#87909e` gray | Not started, or put back because something more urgent came in |
| 🔴 **RE-OPEN** | `#e5484d` red | QC found bugs in round 1 |
| ⚫ **PENDING - ON HOLD** | `#646464` dark gray | Blocked — the blocker is written in a comment |
| 🔵 **IN PROGRESS** | `#1090E0` blue | Being worked on (WIP limit applies) |
| 🟠 **IN REVIEW** | `#E16B16` orange | Code review |
| 🟡 **DEPLOYED TO STAGING** | `#f8ae00` yellow | Dev done, waiting for QC — end of the dev's ownership |
| 🟣 **READY FOR PRODUCTION** | `#ab4aba` purple | QC verified, no bugs left |
| 🟢 **DEPLOYED TO PROD** | `#3db88b` green | Released |
| 🟢 **CLOSED** | `#008844` dark green | Done |
| 🔴 **CANCELLED** | `#d33d44` red | Dropped |

## 1. Daily routine (`/tlm-daily` automates the check)

- Check your assigned tickets every day. Blockers or points that need confirmation → leave a summary
  comment on the ticket.
- **WIP limit**: at most 1–2 tickets at a time.
- Ticket is blocked → move it to ⚫ **PENDING - ON HOLD**.
- Another ticket has higher priority → move the current ticket back to ⚪ **TO DO**, leave a comment
  with a note, and ping Tony.

**Why**: a ticket sitting in IN PROGRESS while nobody works on it hides the real load; the lead plans
the sprint from statuses, so a wrong status is a wrong plan.

## 2. Ticket ownership

- Each member owns their tickets from start until 🟡 **DEPLOYED TO STAGING**.
- Every assigned Epic / Parent ticket: fill in the **estimated due date** yourself.
- Pending / blocked: set ⚫ **PENDING - ON HOLD**, tag **Tony + Steph**, and write the issue plus the
  remaining TODOs / blockers.

## 3. Ticket creation (Telemax's EPIC template)

- Sub-task / sub-ticket: create it yourself with the **Telemax's EPIC** template.
- Epic / Parent task: **Tony** creates it. DM Tony the title + description (optional).
- Dev works on the **EPIC**; BA / QC work on their BA / QC subtasks under that EPIC.

## 4. QC process & naming convention

- `[QA][Module][TASK] …` — testing a new ticket (round 1).
- `[QA][Module][BUG] …` — working on the bugs found in the ticket (round 2).
- Round 1 done with bugs → QC logs bug subtasks and moves the ticket to 🔴 **RE-OPEN**.
- Verification passed (no bugs left) → QC moves the ticket to 🟣 **READY FOR PRODUCTION**.

## 5. Communication (Slack)

- Don't reply only inside a thread. If you reply in a thread, tick **"Also send to channel"** so the
  whole group sees it.
- Reply to the client as soon as possible. Need time → tell them when you will get back to them.

## 6. Leave & OOO

- Unplanned leave / day off: post in the **frontend_dev** channel.
- Planned leave: notify at the start of the month and log OOO on the **Telemax Calendar**.
