#!/usr/bin/env python3
"""
apply-qa-prefix.py — namespace the vendored QA harness under `tlm-qa-`.

The harness upstream (dungvv-hblab-hbg/telemax-qa-skill) ships unprefixed slash
commands (`/qa-analyze`, …) and skill names (`checklist-format`, …). Inside this
plugin those names would sit in the same skill/command namespace as everything
else, so the vendored copy is transformed: every QA **command** and **skill** is
prefixed with `tlm-qa-`. Agents are left unprefixed — they are internal subagents,
never a user-facing slash command, and never registered as skills.

This makes `vendor/telemax-qa-skill/` **not** a verbatim copy. After every upstream
sync (`git archive main | tar -x -C vendor/telemax-qa-skill`) re-run this script to
re-apply the transform:

    python3 vendor/apply-qa-prefix.py

It is idempotent (negative lookbehind guards against double-prefixing), so running
it twice is a no-op on the second pass. See vendor/telemax-qa-skill/PROVENANCE.md.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemax-qa-skill")

# 10 slash commands (filenames in .claude/commands/). NOT the scripts qa-config /
# qa-log / qa-py / qa-state — those are helper scripts, not commands.
COMMANDS = [
    "analyze", "apply-feedback", "doctor", "file-bugs", "login",
    "run", "setup", "status", "verify-prod", "write-cases",
]
# 8 skills (directory names under .claude/skills/).
SKILLS = [
    "checklist-format", "clickup-bug-format", "common-validate", "e2e-scaffold",
    "git-diff-scope", "playwright-export", "postman-api-test", "testcase-template",
]

# `qa-run` -> `tlm-qa-run`, but never re-prefix an already-`tlm-qa-run`.
CMD_RE = re.compile(r"(?<!tlm-)\bqa-(" + "|".join(map(re.escape, COMMANDS)) + r")\b")
# `checklist-format` -> `tlm-qa-checklist-format`, guarded the same way.
SKILL_RE = re.compile(r"(?<!tlm-qa-)\b(" + "|".join(map(re.escape, SKILLS)) + r")\b")

TEXT_EXTS = {".md", ".sh", ".py", ".mjs", ".json", ".ts", ".txt", ".example"}


# PROVENANCE.md is our meta-doc: it deliberately quotes BOTH the unprefixed upstream
# names and the prefixed ones to explain the transform. Prefixing it would mangle that.
SKIP_FILES = {"PROVENANCE.md"}


def transform_text():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            ext = os.path.splitext(fn)[1]
            if ext not in TEXT_EXTS and fn != ".env.example":
                continue
            path = os.path.join(dirpath, fn)
            try:
                src = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            out = SKILL_RE.sub(r"tlm-qa-\1", CMD_RE.sub(r"tlm-qa-\1", src))
            if out != src:
                open(path, "w", encoding="utf-8").write(out)
                changed += 1
    return changed


def git_mv(src, dst):
    abs_src, abs_dst = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    if not os.path.exists(abs_src) or os.path.exists(abs_dst):
        return False
    r = subprocess.run(["git", "-C", ROOT, "mv", src, dst], capture_output=True)
    if r.returncode:  # fall back to a plain rename if git can't (e.g. untracked)
        os.rename(abs_src, abs_dst)
    return True


def rename_files():
    renamed = 0
    for c in COMMANDS:
        if git_mv(f".claude/commands/qa-{c}.md", f".claude/commands/tlm-qa-{c}.md"):
            renamed += 1
    for s in SKILLS:
        if git_mv(f".claude/skills/{s}", f".claude/skills/tlm-qa-{s}"):
            renamed += 1
    return renamed


def main():
    if not os.path.isdir(ROOT):
        sys.exit(f"not found: {ROOT}")
    # Rename on-disk first so path references the text pass rewrites resolve.
    renamed = rename_files()
    changed = transform_text()
    print(f"renamed {renamed} path(s) · rewrote {changed} file(s)")


if __name__ == "__main__":
    main()
