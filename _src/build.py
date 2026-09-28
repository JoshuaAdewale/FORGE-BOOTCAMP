"""Compile Python-authored curriculum into browser-ready JS data files."""
import json, os, importlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
sys.path.insert(0, HERE)

BUNDLES = [
    ("meta.js", ["pages_meta"], True),
    ("curriculum-1.js", ["pages_p1", "pages_p2"], False),
    ("curriculum-2.js", ["pages_p3", "pages_p4"], False),
    ("curriculum-3.js", ["pages_p5", "pages_p6"], False),
    ("sectors.js", ["pages_sectors"], False),
    ("career.js", ["pages_career"], False),
    ("exercises.js", ["pages_exercises"], False),
    ("income.js", ["pages_income"], False),
    ("global.js", ["pages_global"], False),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for fname, mods, first in BUNDLES:
        pages = []
        for m in mods:
            mod = importlib.import_module(m)
            pages.extend(mod.PAGES)
        total += len(pages)
        for p in pages:
            p["body"] = p["body"].replace("~~~", "```")
        body = json.dumps(pages, ensure_ascii=False, indent=1)
        head = "window.COURSE = window.COURSE || { pages: [] };\n" if first else ""
        js = head + "window.COURSE.pages = window.COURSE.pages.concat(\n" + body + "\n);\n"
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(js)
        print("wrote", fname, len(pages), "pages")
    print("TOTAL PAGES:", total)

if __name__ == "__main__":
    main()
