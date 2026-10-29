# vendor/telemax-qa-skill — a copy, not a submodule

Everything beside this file is a copy of another repository, with **upstream's command, skill and agent
names unchanged** (`/qa-*`, `checklist-format`, …), plus the local patches listed below. It is **not**
maintained here: edit it upstream, then re-copy. A fix made only in this directory is a fix that
disappears the next time anyone syncs, unless it is in the patch table below.

| | |
|---|---|
| Upstream | `https://github.com/dungvv-hblab-hbg/telemax-qa-skill` |
| Copied from | `main` @ `f7377f9` (v3.8, no-spec branch) |
| Copied on | 2026-10-29 |
| Local transform | none — names are upstream's. Plugin ≤ 2.25.0 renamed them to `tlm-qa-*`; that transform was dropped |

## Local patches — re-apply after every sync

These are edits made **here**, not upstream, at the team's request. A sync overwrites them; re-apply
(or upstream them) and keep this list current.

| Date | Files | Change |
|---|---|---|
| 2026-10-13 | `.claude/skills/clickup-bug-format/SKILL.md` + `assets/example-bug.md`, `.claude/agents/bug-proposer.md`, `.claude/agents/bug-filer.md` | Bug body = **Summary (~50 words)** first, then **Details**; Steps split into ≥1 **scenario**, each with a **full URL** (e.g. `https://dashboard-stage.telemax.com.au/manage/vehicles-v3/20451`), steps, then `Actual:` / `Expected:`; every evidence link is a full URL. `bugs-proposed.json` gains `summary` + `scenarios[]`. |
| 2026-10-13 | same files | No blank-line padding: section title sits directly on its content; exactly one blank line (2 newlines) between sections; no standalone "Details" title line. |
| 2026-10-13 | same files | `**Actual:**` / `**Expected:**` are bold, at line start, not indented — never a bullet or numbered item. |
| 2026-10-13 | `SKILL.md` | Optional **Note for dev** section is always last, after Traceability. |
| 2026-10-13 | `SKILL.md`, `example-bug.md` | "Field ClickUp" section renamed **Traceability** (parent ticket, TC ID, environment). No Priority/Type/Status/Assignee in the description — those are ClickUp task fields. No test date, except production bugs, which carry date + time (with timezone). |
| 2026-10-13 | `SKILL.md`, `example-bug.md` | Summary and Description break lines by idea (one idea per line, single newline) — never one long unbroken paragraph. |

## What it is

The Telemax **QA harness**: eleven slash commands (`/qa-*`), ten subagents
and eight skills that drive
`ticket → checklist → test-case Excel → run (UI/API) → ClickUp bug → verify production`, with three
human review stops. As of the v3.5 upstream, the six pipeline stages are joined by two read-only
diagnostics — `/qa-doctor` (environment/config health, installs nothing) and `/qa-status` (cross-stage
progress from `.qa/<ticket>/state.json`, reconciled against on-disk artifacts). Since `f8157c4` there
is also `/qa-retro` — a post-run review of the **harness itself** (two independent reviews via the
`retro-analyst` agent, cross-checked into a markdown report; it never edits `.claude/`, commits, or
re-runs tests). Its own README (in
this directory) is the authoritative manual — install
requirements, the three install traps, the token budget, and the three guardrails that were paid for
(`Append, không lấp lỗ trống` / `Khoá theo TC ID` / `Won't fix, không xoá dòng`). Since `f7377f9` (v3.8)
`/qa-analyze` also has a **no-spec branch** — a ticket with no spec, or an old feature with no ticket,
is asked about instead of having a spec inferred from the code (`.claude/agents/reference/no-spec-mode.md`,
`ui-explorer` agent).

## It installs into a consuming repo, not into this plugin

Like z-harness, this stays a **separate installable**, not wired into this plugin's `hooks.json` or
skill tree: its scripts are bash + Python, its commands live in a project's own `.claude/commands/`,
and it registers its own Playwright MCP via `.mcp.json`. The `tlm-qa-workflow` skill in this plugin is
the bridge — it detects whether the harness is installed in the current project, installs it from this
copy when it is not, and routes QA requests to the right `/qa-*` stage.

**Do not run `install.sh --force` into a repo that already runs this plugin.** A consuming repo has
`.claude/` (settings.local.json, `tlm-plugin/`), and `install.sh` refuses to overwrite it — that
refusal is correct. The merge path is manual and additive:

```bash
SRC=<rules-root>/vendor/telemax-qa-skill
cp -R "$SRC/.claude/commands" "$SRC/.claude/agents" "$SRC/.claude/skills" "$SRC/.claude/scripts" .claude/
cp "$SRC/.claude/qa-config.md" .claude/
cp -R "$SRC/telemax-e2e" .
cat "$SRC/gitignore.snippet" >> .gitignore
# .mcp.json: merge the "playwright" entry by hand if the repo already has one
```

## Names — upstream's, unchanged

Up to plugin 2.25.0 this copy was run through `apply-qa-prefix.py`, which renamed every command and skill
to `tlm-qa-*`. The team asked for upstream's names instead (2026-10-29): the harness's README, tutorial
and CHANGELOG all say `/qa-*`, and a renamed copy made every one of them wrong in a consuming repo. The
script is gone; `tlm-qa-workflow` STEP 1 tells a repo still holding the old `tlm-qa-*` install how to
replace it.

## Syncing, until something automated exists

The patched files (table above) are merged three-way — the last synced upstream commit is the base — so
an upstream edit to the same file keeps both sides; a plain re-copy would silently drop the patches:

```bash
UP=<a clone of telemax-qa-skill>; OLD=<"Copied from" sha above>; V=vendor/telemax-qa-skill
PATCHED=".claude/agents/bug-filer.md .claude/agents/bug-proposer.md
  .claude/skills/clickup-bug-format/SKILL.md .claude/skills/clickup-bug-format/assets/example-bug.md"
T=$(mktemp -d); cp $V/PROVENANCE.md $T/; for f in $PATCHED; do mkdir -p $T/$(dirname $f); cp $V/$f $T/$f; done
rm -rf $V && mkdir $V && git -C $UP archive main | tar -x -C $V && cp $T/PROVENANCE.md $V/
for f in $PATCHED; do git -C $UP show $OLD:$f > $T/$f.base
  git merge-file -p $T/$f $T/$f.base $V/$f > $T/$f.out; echo "$f conflicts=$?"; cp $T/$f.out $V/$f; done
```

A non-zero `conflicts=` leaves `<<<<<<<` markers in that file — resolve them before committing. Then update the table above. To check a sync, the harness carries its own CI checks — run them from
the vendored directory (they are location-independent, unlike z-harness's tests):

```bash
bash vendor/telemax-qa-skill/.claude/scripts/smoke-scripts.sh   # 19 assertions, no MCP needed
python3 vendor/telemax-qa-skill/scripts/lint-harness.py         # frontmatter name==dir, links, --project
```

Requires `bash` and `python3` **with `pyyaml` and `openpyxl` importable** (a venv is fine — the smoke
script resolves its interpreter via `qa-py.sh`); on a machine without them the red cases are
environment artifacts, not copy corruption. For a dependency-free integrity check, `diff -r` the clone against
this directory: only `PROVENANCE.md` and the patched files may differ. bash + Python is also why these scripts are **not** wired into
this plugin's own `hooks.json` — this plugin's hooks are Node precisely so they run on Windows.
