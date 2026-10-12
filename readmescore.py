#!/usr/bin/env python3
"""readme-quality-score — structural completeness scorer for README files.

Weighted section checklist (total 100) + missing-section suggestions.
Pure stdlib. Read-only. Fails closed (exit 2) on unreadable files.
"""
import argparse
import json
import re
import sys

SECTIONS = [
    ("title", 5, ["^#\\s+\\S"], "Add a top-level `# Title` heading."),
    ("description", 10, ["what|about|intro|description|overview"], "Open with a short paragraph: what the project does and who needs it."),
    ("install", 15, ["install|setup|getting started|requirements|prerequisite|(pip|npm|cargo|gem|go) (install|add)"], "Add an `## Install` section with exact commands."),
    ("usage", 15, ["usage|quickstart|quick start|how (to|it)|run|example"], "Add a `## Usage` / `## Quickstart` section with a runnable command."),
    ("examples", 10, ["example|demo|sample|tutorial"], "Show at least one concrete example (input -> output)."),
    ("configuration", 5, ["config|option|flag|environment|settings"], "Document flags/env vars, or state that there are none."),
    ("limits", 10, ["limit|caveat|trade-?off|known issue|not a|assumption"], "State known limits and assumptions honestly."),
    ("license", 10, ["licen[cs]e|licensing"], "Add a `## License` section naming the license."),
    ("contributing", 5, ["contribut|development|dev setup|testing"], "Say how others can contribute or run the tests."),
    ("changelog", 5, ["changelog|version|release|history"], "Link or include a changelog."),
    ("faq", 5, ["faq|troubleshoot|when not|question"], "Add an FAQ (include 'When NOT to use' if possible)."),
    ("contact", 5, ["contact|issue|report|feedback|support|author"], "Tell readers where to report problems (issues, email)."),
]

H_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def extract_headings(text):
    return [(len(m.group(1)), m.group(2).strip().lower()) for m in H_RE.finditer(text)]


def section_present(name, aliases, text, headings):
    if name == "title":
        return bool(headings) and headings[0][0] == 1
    if isinstance(aliases, str):
        aliases = [aliases]
    body = text.lower()
    for a in aliases:
        if re.search(a, body):
            return True
    return False


def score_readme(text):
    """Score README text. Returns {score, max, sections, suggestions, stats}."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    headings = extract_headings(text)
    sections = []
    suggestions = []
    total = 0
    for name, weight, aliases, advice in SECTIONS:
        present = section_present(name, aliases, text, headings)
        gained = weight if present else 0
        total += gained
        sections.append({"section": name, "weight": weight, "present": present, "score": gained})
        if not present:
            suggestions.append(advice)
    words = len(text.split())
    flags = []
    if words < 50:
        flags.append("very short README (<50 words)")
    if len(text) > 200000:
        flags.append("very large README (>200k chars) — consider splitting")
    if headings and headings[0][0] != 1:
        flags.append("no top-level H1 heading")
    h1_count = sum(1 for lvl, _ in headings if lvl == 1)
    if h1_count > 1:
        flags.append("multiple H1 headings (%d)" % h1_count)
    return {
        "score": total,
        "max": 100,
        "sections": sections,
        "suggestions": suggestions,
        "stats": {"words": words, "headings": len(headings)},
        "flags": flags,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="readme-quality-score", description="Score README structural completeness (0-100) and list missing sections.")
    ap.add_argument("file", nargs="?", help="README file; omit to read stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--min-score", type=int, default=0, help="exit 1 if score is below this threshold")
    ap.add_argument("--list-sections", action="store_true", help="print the checklist and exit")
    args = ap.parse_args(argv)
    if args.list_sections:
        for name, weight, _a, _ad in SECTIONS:
            print("%-15s %d" % (name, weight))
        return 0
    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        else:
            text = sys.stdin.read()
    except OSError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    report = score_readme(text)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("score: %d/100" % report["score"])
        for s in report["sections"]:
            print("  %-15s %3d/%-3d %s" % (s["section"], s["score"], s["weight"], "ok" if s["present"] else "MISSING"))
        for fl in report["flags"]:
            print("flag: %s" % fl)
        if report["suggestions"]:
            print("suggestions:")
            for s in report["suggestions"]:
                print("  - %s" % s)
    return 1 if report["score"] < args.min_score else 0


if __name__ == "__main__":
    sys.exit(main())
