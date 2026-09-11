# vendor/telemax-qa-skill — a copy, not a submodule

Everything beside this file is a copy of another repository, **plus one mechanical transform**: every
QA command and skill is prefixed with `tlm-qa-` (see "Namespacing" below). It is **not** maintained
here: edit it upstream, then re-copy, then re-apply the transform. A fix made only in this directory
is a fix that disappears the next time anyone syncs, and nobody will be watching for it.

| | |
|---|---|
| Upstream | `https://github.com/dungvv-hblab-hbg/telemax-qa-skill` |
| Copied from | `main` @ `25cdf9e` |
| Copied on | 2026-09-11 |
| Local transform | `../apply-qa-prefix.py` — `qa-*` commands & bare skill names → `tlm-qa-*` |

## What it is

The Telemax **QA harness**: ten slash commands (`/tlm-qa-*` here — see "Namespacing"), eight subagents
and eight skills that drive
`ticket → checklist → test-case Excel → run (UI/API) → ClickUp bug → verify production`, with three
human review stops. As of the v3.5 upstream, the six pipeline stages are joined by two read-only
diagnostics — `/tlm-qa-doctor` (environment/config health, installs nothing) and `/tlm-qa-status` (cross-stage
progress from `.qa/<ticket>/state.json`, reconciled against on-disk artifacts). Its own README (in
this directory) is the authoritative manual — install
requirements, the three install traps, the token budget, and the three guardrails that were paid for
(`Append, không lấp lỗ trống` / `Khoá theo TC ID` / `Won't fix, không xoá dòng`). The transform also
rewrites the harness's own README/CHANGELOG/docs to the prefixed names, so they match what a consuming
repo actually installs.

## It installs into a consuming repo, not into this plugin

Like z-harness, this stays a **separate installable**, not wired into this plugin's `hooks.json` or
skill tree: its scripts are bash + Python, its commands live in a project's own `.claude/commands/`,
and it registers its own Playwright MCP via `.mcp.json`. The `tlm-qa-workflow` skill in this plugin is
the bridge — it detects whether the harness is installed in the current project, installs it from this
copy when it is not, and routes QA requests to the right `/tlm-qa-*` stage.

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

## Namespacing — why the `tlm-qa-` prefix

Upstream ships the harness with **unprefixed** names: slash commands `/qa-analyze` … `/qa-status`, and
skills `checklist-format`, `testcase-template`, …. Installed as-is, those land in the same command and
skill namespace as everything else the consuming repo runs. So `../apply-qa-prefix.py` renames all ten
commands and all eight skills (dir + `name:` frontmatter + every cross-reference) to `tlm-qa-*`. **Agents
are left unprefixed** — they are internal subagents (`@test-runner`), never a user-facing slash command,
and never registered as a skill, so they need no namespace and renaming them is churn.

The transform is idempotent (negative-lookbehind guards) and reversible from the diff, but it means this
directory is **not** a byte-for-byte copy of upstream — the sync procedure below re-applies it.

## Syncing, until something automated exists

```bash
git -C <a clone of telemax-qa-skill> archive main | tar -x -C vendor/telemax-qa-skill
python3 vendor/apply-qa-prefix.py          # re-apply the tlm-qa- namespacing transform
```

Then update the table above. To check a sync, the harness carries its own CI checks — run them from
the vendored directory (they are location-independent, unlike z-harness's tests):

```bash
bash vendor/telemax-qa-skill/.claude/scripts/smoke-scripts.sh   # 18 assertions, no MCP needed
python3 vendor/telemax-qa-skill/scripts/lint-harness.py         # frontmatter name==dir, links, --project
```

Requires `bash` and `python3` **with `pyyaml` and `openpyxl` importable** (a venv is fine — the smoke
script resolves its interpreter via `qa-py.sh`); on a machine without them the red cases are
environment artifacts, not copy corruption. For a dependency-free integrity check, diff the **clone with
the same transform applied** against this directory — a bare `diff -r` against the raw clone will now show
every `qa-*` → `tlm-qa-*` rename and is expected to differ. bash + Python is also why these scripts are **not** wired into
this plugin's own `hooks.json` — this plugin's hooks are Node precisely so they run on Windows.
