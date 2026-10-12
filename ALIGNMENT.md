# Alignment Audit (Rules 85-100 / 16 items) — readme-quality-score v0.1.1

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| 1 | Safety/Ethics section | N/A | Not a security-research repo; read-only by construction (never writes files); fails closed (exit 2) on unreadable input |
| 2 | Privacy/dezero | PASS | No secrets/tokens/real names in any file; only contact line uses hcac4735@agent.qq.com (README License section); grep `(sk-\|ghp_\|api[_-]?key\s*=\s*['"][A-Za-z0-9])` → 0 hits |
| 3 | Copyright boundary | PASS | Readme-Health-Checker / standard-readme-linter-regex / AI-Powered-Github-Repo-Analyzer comparisons are structural restatements of their public descriptions, no >50-char copied text; MIT LICENSE present, "zhengming contributors" |
| 4 | Fact-check annotation | PASS | 56-check suite "~3 s" marked [Measured] with repro `python self_test.py`; "~1 s" scoring timing marked ~; all claims qualitative |
| 5 | Confidence grading | PASS | Opener [High ≥80%] tied to the suite; structure-vs-quality limits framed as scope; ≥2 explicit labels |
| 6 | PLAN B built-in | PASS | "Minimal Fallback (PLAN B)" section: single grep presence check, zero setup |
| 7 | Timeout preset | PASS | Quickstart states "~2 min" with ~1 s / ~3 s step markers |
| 8 | Rule-conflict arbitration | PASS | "Design Trade-offs" opens with priority order: explainability > determinism > zero-dependency > detection recall |
| 9 | Version changelog | PASS | CHANGELOG.md v0.1.0 + v0.1.1; v0.1.1 records documentation completion and suite re-verification |
| 10 | Exemption instruction | N/A | Session-level rule; static repo content not applicable |
| 11 | External-knowledge cutoff | PASS | why-not-X comparisons and scope claims dated "as of 2026-10-12" |
| 12 | Assumption explicitness | PASS | "[Core Assumptions]" section with 4 items |
| 13 | Logic-check trio | PASS | self_test.py three-tier suite (functional / error / extreme-edge, incl. non-string input, 200k-char flag, H1 anomalies); `python self_test.py` → `SUMMARY: PASS 56/56` |
| 14 | Socratic question | PASS | FAQ "When NOT to use this tool?" with 4 anti-use-cases (prose quality, link validation, pointer READMEs, spec conformance) |
| 15 | Pareto improvement | PASS | v0.1.1 documentation round: README documents the 30% install+usage weighting rationale, keyword-stuffing second-order risk, and rubric customization absent from the module docstring; traceable in CHANGELOG |
| 16 | Ultimate fallback (≤60-word opener) | PASS | First paragraph = 58 words, contains what-it-is and the "docs CI gate" judgment sentence |

Second-order effects (rule 16 bonus): PASS — "Limits & Second-order Effects" covers score-chasing keyword stuffing, split-doc score drops, and presence≠comprehension.

Scan evidence: `grep -rEn "(sk-|ghp_|api[_-]?key\s*=\s*['\"][A-Za-z0-9])" .` → 0 hits; `grep -rn "hcac4735@agent.qq.com" README.md` → 1 hit.
