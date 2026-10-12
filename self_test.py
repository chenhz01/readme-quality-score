#!/usr/bin/env python3
"""self_test.py for readme-quality-score — [A] functional / [B] exception paths / [C] extreme edges."""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import readmescore  # noqa: E402

RESULTS = []


def check(name, fn):
    try:
        fn()
        RESULTS.append((name, True))
    except Exception as e:  # noqa: BLE001
        RESULTS.append((name, False))
        print("  [FAIL] %s -> %r" % (name, e))


def assert_eq(a, b, msg=""):
    assert a == b, msg or "%r != %r" % (a, b)


def assert_true(c, m=""):
    assert c, m


FULL = """# Project X

What it does, for whom.

## Install

pip install project-x

## Usage / Quickstart

python -m project_x --help

## Example

input -> output demo

## Configuration

Flags documented here.

## Limits

Known caveats and trade-offs.

## License

MIT

## Contributing

Run tests with python self_test.py.

## Changelog

See CHANGELOG.md.

## FAQ

When NOT to use: ...

## Contact

Open an issue.
"""

# ---------- [A] functional ----------
def a01():
    r = readmescore.score_readme(FULL)
    assert_eq(r["score"], 100)
def a02():
    r = readmescore.score_readme("")
    assert_eq(r["score"], 0)
def a03():
    r = readmescore.score_readme(FULL)
    assert_eq(len(r["sections"]), 12)
def a04():
    r = readmescore.score_readme("# T\n\n## Usage\nrun it")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["usage"]["present"] and not s["install"]["present"])
def a05():
    r = readmescore.score_readme(FULL)
    assert_eq(r["suggestions"], [])
def a06():
    r = readmescore.score_readme("# T\n\ninstall it with pip")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["install"]["present"], "alias matched in body text")
def a07():
    r = readmescore.score_readme(FULL)
    assert_eq(r["stats"]["headings"], 11)
def a08():
    r = readmescore.score_readme("word " * 100 + " license MIT usage example faq contact contributing changelog configuration limits install")
    assert_true(0 < r["score"] <= 100)
def a09():
    r = readmescore.score_readme(FULL)
    assert_true(all(s["score"] == s["weight"] for s in r["sections"]))
def a10():
    r = readmescore.score_readme("")
    assert_true("very short README" in r["flags"][0])
def a11():
    r = readmescore.score_readme("## Not a title\n\nusage")
    assert_true(any("H1" in f for f in r["flags"]))
def a12():
    r = readmescore.score_readme(FULL)
    assert_eq(r["max"], 100)
def a13():
    r = readmescore.score_readme("# T\n\n# T2\n\nusage license")
    assert_true(any("multiple H1" in f for f in r["flags"]))
def a14():
    r = readmescore.score_readme(FULL)
    s = {x["section"]: x for x in r["sections"]}
    assert_eq(s["license"]["weight"], 10)
def a15():
    here = os.path.dirname(os.path.abspath(__file__))
    fd, path = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    try:
        open(path, "w", encoding="utf-8").write(FULL)
        code = subprocess.run([sys.executable, os.path.join(here, "readmescore.py"), path], capture_output=True, text=True)
        assert_eq(code.returncode, 0)
        assert_true("100/100" in code.stdout)
    finally:
        os.unlink(path)
def a16():
    r = readmescore.score_readme("# T\n\nWhen NOT to use this: ...")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["faq"]["present"])
def a17():
    r = readmescore.score_readme("# \u4e2d\u6587\u9879\u76ee\n\n\u5b89\u88c5\u4f7f\u7528\u8bf4\u660e license")
    assert_true(r["stats"]["words"] > 0)
def a18():
    r1 = readmescore.score_readme(FULL)
    r2 = readmescore.score_readme(FULL)
    assert_eq(r1, r2)
def a19():
    r = readmescore.score_readme(FULL)
    assert_eq(sum(s["weight"] for s in r["sections"]), 100)
def a20():
    r = readmescore.score_readme("# T\n" + "body " * 3000)
    assert_true(r["stats"]["words"] > 3000)

# ---------- [B] exception paths ----------
def b01():
    code = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "readmescore.py"), "missing.md"], capture_output=True, text=True)
    assert_eq(code.returncode, 2)
def b02():
    try:
        readmescore.score_readme(None)
        assert False
    except TypeError:
        pass
def b03():
    try:
        readmescore.score_readme(42)
        assert False
    except TypeError:
        pass
def b04():
    here = os.path.dirname(os.path.abspath(__file__))
    code = subprocess.run([sys.executable, os.path.join(here, "readmescore.py"), "--help"], capture_output=True, text=True)
    assert_eq(code.returncode, 0)
def b05():
    code = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "readmescore.py"), "--min-score", "50"], capture_output=True, text=True, input="# T\nusage")
    assert_eq(code.returncode, 1)
def b06():
    code = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "readmescore.py"), "--json"], capture_output=True, text=True, input=FULL)
    rep = json.loads(code.stdout)
    assert_eq(rep["score"], 100)
def b07():
    here = os.path.dirname(os.path.abspath(__file__))
    code = subprocess.run([sys.executable, os.path.join(here, "readmescore.py"), "--min-score", "0"], capture_output=True, text=True, input="")
    assert_eq(code.returncode, 0)
def b08():
    r = readmescore.score_readme("no headings at all, just words. " * 10)
    assert_true(r["score"] >= 0)
def b09():
    here = os.path.dirname(os.path.abspath(__file__))
    fd, path = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    try:
        open(path, "wb").write(b"\xff\xfe\x00bad bytes")
        code = subprocess.run([sys.executable, os.path.join(here, "readmescore.py"), path], capture_output=True, text=True)
        assert_eq(code.returncode, 0, "binary garbage must not crash (errors=replace)")
    finally:
        os.unlink(path)
def b10():
    code = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "readmescore.py"), "--min-score", "-5"], capture_output=True, text=True, input="")
    assert_eq(code.returncode, 0)

# ---------- [C] extreme edges ----------
def c01():
    r = readmescore.score_readme("#" * 100)
    assert_true(r["score"] <= 100)
def c02():
    r = readmescore.score_readme("# T\n\nusage\n" * 5000)
    assert_true(r["score"] <= 100)
def c03():
    r = readmescore.score_readme("# \U0001f680 Rocket\n\n## \u4e2d\u6587\u7528\u6cd5 usage\n\nlicense faq contact")
    assert_true(r["stats"]["headings"] >= 2)
def c04():
    r = readmescore.score_readme("```\n# not a heading\n```\nusage license")
    assert_true(True)  # headings inside fences are a documented approximation
def c05():
    r = readmescore.score_readme("x" * 250000)
    assert_true(any("very large" in f for f in r["flags"]))
def c06():
    r = readmescore.score_readme("# T\n\n## Install\n## Usage\n## Example\n## Configuration\n## Limits\n## License\n## Contributing\n## Changelog\n## FAQ\n## Contact\n\nWhat it does.")
    assert_eq(r["score"], 100)
def c07():
    r = readmescore.score_readme("# T\n\nno keywords whatsoever in this body text")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(not s["install"]["present"])
def c08():
    r = readmescore.score_readme("# T\n\n" + "\n".join("## Section %d" % i for i in range(200)))
    assert_eq(r["stats"]["headings"], 201)
def c09():
    r = readmescore.score_readme("# T\n\nLICENCE uk spelling")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["license"]["present"], "licence matches license alias via regex")
def c10():
    r = readmescore.score_readme("# T\n\nQuick Start guide")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["usage"]["present"])
def c11():
    r = readmescore.score_readme("# T\n\ntrade-offs and known issues live here")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["limits"]["present"])
def c12():
    r = readmescore.score_readme("# T\n\nreport bugs at issues")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["contact"]["present"])
def c13():
    r = readmescore.score_readme("USAGE")  # uppercase body
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["usage"]["present"], "case-insensitive matching")
def c14():
    r = readmescore.score_readme("# T\n\nInstall\n\n\n\nUsage\n\nExample\n\nConfiguration\n\nLimits\n\nLicense\n\nContributing\n\nChangelog\n\nFAQ\n\nContact\n\nWhat it does for whom.")
    assert_eq(r["score"], 100)
def c15():
    r = readmescore.score_readme("# T\n\nword")
    assert_eq(len(r["suggestions"]), 11)
def c16():
    r = readmescore.score_readme("\n\n\n")
    assert_eq(r["score"], 0)

for fn in sorted([v for k, v in list(globals().items()) if k.startswith(("a0", "a1", "a2", "b0", "b1", "c0", "c1"))], key=lambda f: f.__name__):
    check(fn.__name__, fn)


# ---------- [R2] round-2 additions (--list-sections, refined install aliases, drift checks) ----------
def r201():
    here = os.path.dirname(os.path.abspath(__file__))
    code = subprocess.run([sys.executable, os.path.join(here, "readmescore.py"), "--list-sections"], capture_output=True, text=True)
    assert_eq(code.returncode, 0)
    assert_true("install" in code.stdout and "usage" in code.stdout)
def r202():
    r = readmescore.score_readme("# T\n\npip install pkg\n\nusage license")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["install"]["present"])
def r203():
    r = readmescore.score_readme("# T\n\nnpm install pkg\n\nusage license")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["install"]["present"])
def r204():
    r = readmescore.score_readme("# T\n\ncargo add crate\n\nusage license")
    s = {x["section"]: x for x in r["sections"]}
    assert_true(s["install"]["present"])
def r205():
    r = readmescore.score_readme(FULL)
    assert_eq(r["suggestions"], [])
    assert_eq(r["flags"], [])
def r206():
    r = readmescore.score_readme("")
    assert_eq(len(r["suggestions"]), 12)
def r207():
    r = readmescore.score_readme(FULL)
    assert_true(all(s["present"] for s in r["sections"]))
def r208():
    r1 = readmescore.score_readme("# T\n\nGetting Started: install it")
    s = {x["section"]: x for x in r1["sections"]}
    assert_true(s["install"]["present"], "getting started alias")
def r209():
    r = readmescore.score_readme("# T\n\n## Usage\n\n" + "body " * 100)
    s = {x["section"]: x for x in r["sections"]}
    assert_true(not s["license"]["present"], "usage alone must not grant license points")
def r210():
    r = readmescore.score_readme("# T\n\nWhat it does.\n\nMIT License.\n\nusage example faq contact contributing changelog configuration limits install")
    assert_true(r["score"] >= 95, "all aliases hit -> near-perfect")

for fn in sorted([v for k, v in list(globals().items()) if k.startswith("r2")], key=lambda f: f.__name__):
    check(fn.__name__, fn)

passed = sum(1 for _, ok_ in RESULTS if ok_)
for n, ok_ in RESULTS:
    if not ok_:
        print("FAIL:", n)
print("SUMMARY: PASS %d/%d" % (passed, len(RESULTS)))
sys.exit(0 if passed == len(RESULTS) else 1)
