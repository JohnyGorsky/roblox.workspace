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
    "jungle": "../roblox.jungle",
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

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
