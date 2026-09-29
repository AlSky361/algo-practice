#!/usr/bin/env python3
"""
Creates a folder for a new task with solution templates and meta.yml.

Usage:
    python3 new_problem.py leetcode 347 top-k-frequent-elements -d Medium -p "Arrays & Hashing"
    python3 new_problem.py sql 176 second-highest-salary -d Medium
    python3 new_problem.py project-euler 1 multiples-of-3-and-5

Once solved, set `status: Solved` in meta.yml and run generate_readme.py.
Only tasks with status Solved appear in the README.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent

PADDING = {"leetcode": 4, "sql": 4, "deepml": 2, "project-euler": 3}

PY_TEMPLATE = '''class Solution:
    def solve(self):
        pass
'''

CPP_TEMPLATE = '''#include <vector>

class Solution {
public:
    void solve() {
    }
};
'''

SQL_TEMPLATE = "-- Write your query here\n"


def build_meta(section: str, title: str, difficulty: str, pattern: str, url: str) -> str:
    """Fields match what generate_readme.py reads."""
    lines = [f"title: {title}"]
    if section != "project-euler":
        lines.append(f"difficulty: {difficulty}")
    if section == "leetcode":
        lines.append(f"pattern: {pattern}")
    elif section == "deepml":
        lines.append(f"topic: {pattern}")
    lines.append(f"url: {url}")
    lines.append("status: In progress")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("section", choices=PADDING, help="section folder")
    parser.add_argument("number", type=int, help="problem number")
    parser.add_argument("slug", help="problem slug, e.g. two-sum")
    parser.add_argument("-d", "--difficulty", default="Easy",
                        choices=["Easy", "Medium", "Hard"],
                        help="difficulty (default: Easy)")
    parser.add_argument("-p", "--pattern", default="",
                        help="pattern (LeetCode) or topic (DeepML)")
    parser.add_argument("--lang", nargs="+", default=None,
                        choices=["py", "cpp", "sql"],
                        help="solution files to create "
                             "(default: py cpp; sql for the sql section)")
    args = parser.parse_args()

    langs = args.lang or (["sql"] if args.section == "sql" else ["py", "cpp"])

    folder = ROOT / args.section / f"{args.number:0{PADDING[args.section]}d}-{args.slug}"
    if folder.exists():
        print(f"Already exists: {folder.relative_to(ROOT)}", file=sys.stderr)
        return 1
    folder.mkdir(parents=True)

    if "py" in langs:
        (folder / "solution.py").write_text(PY_TEMPLATE, encoding="utf-8")
    if "cpp" in langs:
        (folder / "solution.cpp").write_text(CPP_TEMPLATE, encoding="utf-8")
    if "sql" in langs:
        (folder / "solution.sql").write_text(SQL_TEMPLATE, encoding="utf-8")

    url = f"https://leetcode.com/problems/{args.slug}/" if args.section in ("leetcode", "sql") else ""
    title = args.slug.replace("-", " ").title()
    (folder / "meta.yml").write_text(
        build_meta(args.section, title, args.difficulty, args.pattern, url),
        encoding="utf-8",
    )

    print(f"Created: {folder.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
