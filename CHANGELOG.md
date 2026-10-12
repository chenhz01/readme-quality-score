# Changelog

## v0.1.1 — 2026-10-12
- Documentation layer completed: README (Problem / How it works / Quickstart / why-not-X anchored on Readme-Health-Checker, standard-readme-linter-regex, AI-Powered-Github-Repo-Analyzer / Minimal Fallback / Trade-offs / Limits / FAQ), ALIGNMENT.md 16-item audit.
- Self-test re-verified green, no code changes needed this round: `python self_test.py` → `SUMMARY: PASS 56/56`.

## v0.1.0 — 2026-10-11
- Initial implementation: 12-section weighted checklist (100 points) with alias-regex detection, per-section suggestions, README flags (size, H1 count), `--min-score` CI gate mode, `--list-sections` rubric dump, `--json` output, file/stdin input, exit 2 on unreadable files.
- Self-test suite (functional / error / extreme-edge tiers).
