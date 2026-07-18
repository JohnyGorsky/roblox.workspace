#!/usr/bin/env python3
"""
Shared, game-agnostic job scaffolder for the Roblox multi-game workspace.

Every job belongs to exactly one project (workspace | defender | jungle) and lives in that
project's `Jobs/NNN/` folder. A job progresses through fixed files:

    intake.md  ->  implementation-plan.md  ->  final-summary.md + changelog.md

Usage:
    python tools/job.py new     --project defender "Title" "Requirements text"
    python tools/job.py new     --project defender --from Planned/dash-ability.md
    python tools/job.py plan    --project defender 7 "Analysis" "Step 1" "Step 2"
    python tools/job.py summary --project defender 7 file1.luau file2.luau --notes "..."
    python tools/job.py release --project defender 7

Design notes:
- Project -> Jobs folder is resolved from this script's location (workspace/tools/job.py):
  workspace  -> <workspace>/Jobs
  defender   -> <workspace>/../roblox.defender/Jobs
  jungle     -> <workspace>/../roblox.jungle/Jobs
- The auto-sync vs manual-copy table is game-specific. If a project has a `.jobconfig.json` at its
  root with {"synced_paths": [...], "non_synced_paths": [...]}, `summary` uses it to categorize files.
  Projects without one (e.g. workspace) simply skip the sync table.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows consoles default to cp1252 and choke on emoji; force UTF-8 so prints never crash.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECTS = {
    "workspace": ".",          # this repo
    "defender": "../roblox.defender",
    "jungle": "../roblox.jungle.game",
}

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def project_root(project: str) -> Path:
    if project not in PROJECTS:
        sys.exit(f"Unknown project '{project}'. Choose one of: {', '.join(PROJECTS)}")
    return (WORKSPACE_ROOT / PROJECTS[project]).resolve()


def jobs_dir(project: str) -> Path:
    d = project_root(project) / "Jobs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def job_folder(project: str, num: int) -> Path:
    return jobs_dir(project) / f"{num:03d}"


def next_job_number(project: str) -> int:
    d = jobs_dir(project)
    nums = [int(p.name) for p in d.iterdir() if p.is_dir() and p.name.isdigit()]
    return (max(nums) + 1) if nums else 1


def load_sync_config(project: str):
    cfg = project_root(project) / ".jobconfig.json"
    if not cfg.exists():
        return None
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
        return data.get("synced_paths", []), data.get("non_synced_paths", [])
    except Exception as e:
        print(f"WARNING: could not read {cfg}: {e}")
        return None


# --------------------------------------------------------------------------- commands

def cmd_new(args):
    project = args.project
    if args.from_file:
        src = (Path.cwd() / args.from_file).resolve()
        if not src.exists():
            sys.exit(f"--from file not found: {src}")
        text = src.read_text(encoding="utf-8")
        title = args.title or src.stem.replace("-", " ").replace("_", " ").title()
        requirements = text
    else:
        if not args.title:
            sys.exit("Provide a \"Title\" (and optional \"Requirements\"), or use --from <file>.")
        title = args.title
        requirements = args.requirements or "_TODO: describe what we plan to do._"

    num = next_job_number(project)
    folder = job_folder(project, num)
    folder.mkdir(parents=True, exist_ok=True)
    intake = folder / "intake.md"
    intake.write_text(
        f"""# Job #{num:03d}: {title}

**Project**: `roblox.{project}`{'' if project == 'workspace' else ''}
**Created**: {now()}
**Status**: Requirements Gathering (intake)

## Requirements / goal

{requirements}

## Checklist

- [ ] Requirements reviewed (this intake)
- [ ] Implementation plan created & agreed
- [ ] Implementation completed
- [ ] Final summary + changelog written
""",
        encoding="utf-8",
    )
    print(f"Created Job #{num:03d} [{project}]: {title}")
    print(f"  {intake}")
    return num


def cmd_plan(args):
    folder = job_folder(args.project, args.num)
    if not folder.exists():
        sys.exit(f"Job #{args.num:03d} not found in {args.project}.")
    steps = "".join(f"{i}. {s}\n" for i, s in enumerate(args.steps, 1)) or "1. _TODO_\n"
    plan = folder / "implementation-plan.md"
    plan.write_text(
        f"""# Implementation Plan — Job #{args.num:03d}

**Project**: `roblox.{args.project}`
**Created**: {now()}
**Status**: Planning (awaiting go-ahead)

## Analysis

{args.analysis or "_TODO: investigation, findings, decisions._"}

## Implementation steps

{steps}
## What I need from you

- [ ] _TODO: Studio actions, asset IDs, decisions, go-ahead_

## Verification

- [ ] _TODO: how we confirm it works_
""",
        encoding="utf-8",
    )
    print(f"Created implementation plan: {plan}")


def cmd_summary(args):
    folder = job_folder(args.project, args.num)
    if not folder.exists():
        sys.exit(f"Job #{args.num:03d} not found in {args.project}.")

    files = args.files or []
    sync = load_sync_config(args.project)
    body = ""
    if sync and files:
        synced_paths, non_synced_paths = sync

        def is_synced(f: str) -> bool:
            fs = f.replace("\\", "/")
            for p in synced_paths:
                if p in fs:
                    return True
            for p in non_synced_paths:
                if p in fs:
                    return False
            return True  # default optimistic

        auto = [f for f in files if is_synced(f)]
        manual = [f for f in files if not is_synced(f)]
        body += "\n### ✅ Auto-synced files\n\n"
        body += "".join(f"- `{f}`\n" for f in auto) or "- _none_\n"
        body += "\n### ⚠️ Manual Studio copy required\n\n"
        body += "".join(f"- `{f}`\n" for f in manual) or "- _none_\n"
    else:
        body += "\n### Files changed\n\n"
        body += "".join(f"- `{f}`\n" for f in files) or "- _TODO_\n"

    summary = folder / "final-summary.md"
    summary.write_text(
        f"""# Final Summary — Job #{args.num:03d}

**Project**: `roblox.{args.project}`
**Completed**: {now()}
**Status**: ✅ Completed

## What was implemented

{args.notes or "_TODO: describe what was built._"}
{body}
## Verification

- [ ] _TODO: confirmed working_
""",
        encoding="utf-8",
    )
    print(f"Created final summary: {summary}")
    print("Reminder: also write changelog.md  ->  python tools/job.py release "
          f"--project {args.project} {args.num}")


def cmd_release(args):
    folder = job_folder(args.project, args.num)
    if not folder.exists():
        sys.exit(f"Job #{args.num:03d} not found in {args.project}.")
    changelog = folder / "changelog.md"
    changelog.write_text(
        """🛠️ Update Notes

✨ _TODO: one player-facing line per user-visible change (3–6 lines)._
❤️ _Player language, not code. One emoji per line._
""",
        encoding="utf-8",
    )
    print(f"Created changelog stub: {changelog}")


# --------------------------------------------------------------------------- todo / findings

# kind -> (folder name, header word, done word)
KINDS = {
    "todo": ("todo", "TODO", "resolved"),
    "finding": ("findings", "FINDING", "fixed"),
}


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:40] or "item"


def kind_dir(project: str, kind: str) -> Path:
    d = project_root(project) / KINDS[kind][0]
    d.mkdir(parents=True, exist_ok=True)
    return d


def next_entry_number(project: str, kind: str) -> int:
    nums = []
    for p in kind_dir(project, kind).glob("[0-9][0-9][0-9][0-9]-*.md"):
        try:
            nums.append(int(p.name[:4]))
        except ValueError:
            pass
    return (max(nums) + 1) if nums else 0


def find_entry(project: str, kind: str, num: int):
    for p in kind_dir(project, kind).glob(f"{num:04d}-*.md"):
        return p
    return None


def cmd_todo(args):
    d = kind_dir(args.project, "todo")
    num = next_entry_number(args.project, "todo")
    path = d / f"{num:04d}-{slugify(args.title)}.md"
    path.write_text(
        f"""# TODO {num:04d}: {args.title}

**Project:** `roblox.{args.project}`
**Status:** open
**Created:** {now()}

{args.note or "_(the thought/task; expand here, or promote to a Job when it's real work)_"}
""",
        encoding="utf-8",
    )
    print(f"Created TODO {num:04d} [{args.project}]: {args.title}\n  {path}")


def cmd_finding(args):
    d = kind_dir(args.project, "finding")
    num = next_entry_number(args.project, "finding")
    path = d / f"{num:04d}-{slugify(args.title)}.md"
    path.write_text(
        f"""# FINDING {num:04d}: {args.title}

**Project:** `roblox.{args.project}`
**Status:** open
**Severity:** {args.severity}
**Created:** {now()}

**Symptom:** {args.symptom or "_TODO_"}
**Where:** {args.where or "_TODO: file / system_"}
**Repro / notes:** _TODO_
**Fix idea:** _TODO_
""",
        encoding="utf-8",
    )
    print(f"Created FINDING {num:04d} [{args.project}] ({args.severity}): {args.title}\n  {path}")


def cmd_resolve(args):
    path = find_entry(args.project, args.kind, args.num)
    if not path:
        sys.exit(f"{args.kind} {args.num:04d} not found in {args.project}.")
    done = KINDS[args.kind][2]
    note = f" — {args.note}" if args.note else ""
    text = path.read_text(encoding="utf-8")
    new = re.sub(r"(?m)^\*\*Status:\*\* .*$",
                 f"**Status:** {done} ({now()[:10]}){note}", text, count=1)
    path.write_text(new, encoding="utf-8")
    print(f"Marked {args.kind} {args.num:04d} [{args.project}] {done}.")


def cmd_list(args):
    entries = sorted(kind_dir(args.project, args.kind).glob("[0-9][0-9][0-9][0-9]-*.md"))
    shown = 0
    for p in entries:
        m = re.search(r"(?m)^\*\*Status:\*\* (.+)$", p.read_text(encoding="utf-8"))
        status = (m.group(1).strip() if m else "?")
        is_open = status.startswith("open")
        if args.open_only and not is_open:
            continue
        print(f"{'[ ]' if is_open else '[x]'} {p.name[:4]} {p.name[5:-3]}  ({status})")
        shown += 1
    if shown == 0:
        print(f"No {'open ' if args.open_only else ''}{args.kind}s in {args.project}.")


# --------------------------------------------------------------------------- cli

def build_parser():
    p = argparse.ArgumentParser(description="Game-agnostic job scaffolder for the Roblox workspace.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_project(sp):
        sp.add_argument("--project", required=True, choices=list(PROJECTS),
                        help="Which project this job belongs to.")

    n = sub.add_parser("new", help="Create a new job (intake.md).")
    add_project(n)
    n.add_argument("title", nargs="?", help="Job title.")
    n.add_argument("requirements", nargs="?", help="Requirements text.")
    n.add_argument("--from", dest="from_file", help="Seed the intake from a Planned/ file.")
    n.set_defaults(func=cmd_new)

    pl = sub.add_parser("plan", help="Create implementation-plan.md.")
    add_project(pl)
    pl.add_argument("num", type=int)
    pl.add_argument("analysis", nargs="?")
    pl.add_argument("steps", nargs="*")
    pl.set_defaults(func=cmd_plan)

    s = sub.add_parser("summary", help="Create final-summary.md.")
    add_project(s)
    s.add_argument("num", type=int)
    s.add_argument("files", nargs="*")
    s.add_argument("--notes")
    s.set_defaults(func=cmd_summary)

    r = sub.add_parser("release", help="Create changelog.md stub.")
    add_project(r)
    r.add_argument("num", type=int)
    r.set_defaults(func=cmd_release)

    t = sub.add_parser("todo", help="Add a quick todo (todo/NNNN).")
    add_project(t)
    t.add_argument("title")
    t.add_argument("note", nargs="?")
    t.set_defaults(func=cmd_todo)

    f = sub.add_parser("finding", help="Log a deferred bug (findings/NNNN).")
    add_project(f)
    f.add_argument("title")
    f.add_argument("symptom", nargs="?")
    f.add_argument("--severity", default="med", choices=["low", "med", "high"])
    f.add_argument("--where")
    f.set_defaults(func=cmd_finding)

    rs = sub.add_parser("resolve", help="Mark a todo/finding resolved/fixed.")
    add_project(rs)
    rs.add_argument("kind", choices=["todo", "finding"])
    rs.add_argument("num", type=int)
    rs.add_argument("note", nargs="?")
    rs.set_defaults(func=cmd_resolve)

    ls = sub.add_parser("list", help="List todos/findings ([ ]=open, [x]=done).")
    add_project(ls)
    ls.add_argument("kind", choices=["todo", "finding"])
    ls.add_argument("--open", dest="open_only", action="store_true", help="only open items")
    ls.set_defaults(func=cmd_list)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
