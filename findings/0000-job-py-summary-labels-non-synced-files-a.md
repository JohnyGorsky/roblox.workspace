# FINDING 0000: job.py summary labels non-synced files as Auto-synced

**Project:** `roblox.workspace`
**Status:** open
**Severity:** med
**Created:** 2026-08-19 22:30:21

**Symptom:** job.py classifies a changed file as auto-synced unless it matches .jobconfig.json non_synced_paths, so docs, skills and config files land under the 'Auto-synced files' heading in final-summary.md. Seen in tide Job 001, where 10 markdown docs and 3 JSON config files were listed as auto-synced. Suggested fix: only classify a file as synced if it matches synced_paths, and put everything else under a neutral 'Other files' heading.
**Where:** _TODO: file / system_
**Repro / notes:** _TODO_
**Fix idea:** _TODO_
