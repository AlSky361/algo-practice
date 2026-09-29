#!/usr/bin/env python3
"""
Scans leetcode/, deepml/, sql/, project-euler/ and updates the tables
in README.md between <!-- AUTO:xxx-START --> and <!-- AUTO:xxx-END --> markers.

Usage:  python3 generate_readme.py

Requirements (the script exits with an error if they are not met):
- PyYAML must be installed:  pip install pyyaml
- Every task folder must contain a meta.yml with at least a `title`.

meta.yml format:
    leetcode:
        title: Two Sum
        difficulty: Easy
        pattern: Arrays & Hashing
        url: https://...
        status: Solved            # optional, defaults to "Solved"
    deepml:
        title: Linear Regression
        difficulty: Easy
        topic: Regression
        url: https://...
    sql:
        title: Second Highest Salary
        difficulty: Medium
        url: https://...
    project-euler:
        title: Multiples of 3 and 5
        url: https://...

The solution language is detected from solution.py / solution.cpp / solution.sql.
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "Error: PyYAML is not installed.\n"
        "Install it and run the script again:\n"
        "  pip install pyyaml"
    )

ROOT = Path(__file__).parent
LANG_FILES = {
    "solution.py": "Py",
    "solution.cpp": "C++",
    "solution.sql": "SQL",
}
EMPTY = "_No solved problems yet._\n"


class MissingMetaError(Exception):
    pass


def read_meta(folder: Path) -> dict:
    meta_path = folder / "meta.yml"
    rel = meta_path.relative_to(ROOT).as_posix()
    if not meta_path.exists():
        raise MissingMetaError(f"meta.yml not found in: {folder.relative_to(ROOT).as_posix()}")
    try:
        data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise MissingMetaError(f"Could not parse {rel}: {e}")
    if not data.get("title"):
        raise MissingMetaError(f"{rel} is missing the required 'title' field")
    return data


def languages_in(folder: Path) -> str:
    found = [label for fname, label in LANG_FILES.items() if (folder / fname).exists()]
    return ", ".join(found) if found else "—"


def extract_number(slug: str) -> str:
    parts = slug.split("-")
    return parts[0] if parts and parts[0].isdigit() else "—"


def collect_tasks(section_dir: Path):
    if not section_dir.exists():
        return []
    tasks = []
    for folder in sorted(section_dir.iterdir()):
        if not folder.is_dir():
            continue
        meta = read_meta(folder)
        tasks.append({
            "number": extract_number(folder.name),
            "title": meta.get("title"),
            "difficulty": meta.get("difficulty", "—"),
            "pattern": meta.get("pattern") or meta.get("topic", "—"),
            "status": meta.get("status", "Solved"),
            "lang": languages_in(folder),
            "rel_link": folder.relative_to(ROOT).as_posix(),
        })
    return tasks


def make_table(tasks, columns) -> str:
    """columns: list of (header, task_key or callable)."""
    if not tasks:
        return EMPTY
    header = "| " + " | ".join(h for h, _ in columns) + " |\n"
    header += "|" + "|".join("---" for _ in columns) + "|\n"
    rows = []
    for t in tasks:
        cells = [(getter(t) if callable(getter) else t[getter]) for _, getter in columns]
        rows.append("| " + " | ".join(str(c) for c in cells) + " |")
    return header + "\n".join(rows) + "\n"


def link(t):
    return f"[link]({t['rel_link']})"


def leetcode_table(tasks):
    return make_table(tasks, [
        ("#", "number"), ("Problem", "title"), ("Difficulty", "difficulty"),
        ("Pattern", "pattern"), ("Language", "lang"), ("Status", "status"), ("Solution", link),
    ])


def deepml_table(tasks):
    return make_table(tasks, [
        ("#", "number"), ("Problem", "title"), ("Difficulty", "difficulty"),
        ("Topic", "pattern"), ("Language", "lang"), ("Status", "status"), ("Solution", link),
    ])


def sql_table(tasks):
    return make_table(tasks, [
        ("#", "number"), ("Problem", "title"), ("Difficulty", "difficulty"),
        ("Status", "status"), ("Solution", link),
    ])


def project_euler_table(tasks):
    # Project Euler has no Easy/Medium/Hard, so no difficulty column.
    return make_table(tasks, [
        ("#", "number"), ("Problem", "title"), ("Language", "lang"),
        ("Status", "status"), ("Solution", link),
    ])


def stats_line(lc, dm, sq, pe) -> str:
    def counts(tasks):
        by = lambda d: sum(1 for t in tasks if t["difficulty"] == d)
        return len(tasks), by("Easy"), by("Medium"), by("Hard")

    def fmt(name, tasks):
        n, e, m, h = counts(tasks)
        return f"- **{name}**: {n} solved (Easy: {e}, Medium: {m}, Hard: {h})\n"

    return (
        fmt("LeetCode", lc) + fmt("DeepML", dm) + fmt("SQL", sq)
        + f"- **Project Euler**: {len(pe)} solved\n"
    )


def replace_block(text: str, marker: str, new_content: str) -> str:
    start = f"<!-- AUTO:{marker}-START -->"
    end = f"<!-- AUTO:{marker}-END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{new_content}\n{end}"
    if pattern.search(text):
        return pattern.sub(lambda _: replacement, text)
    print(f"[!] Markers for {marker} not found in README.md — block appended to the end.")
    return text.rstrip() + "\n\n" + replacement + "\n"


def main():
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        sys.exit("Error: README.md not found next to the script.")

    try:
        lc = collect_tasks(ROOT / "leetcode")
        dm = collect_tasks(ROOT / "deepml")
        sq = collect_tasks(ROOT / "sql")
        pe = collect_tasks(ROOT / "project-euler")
    except MissingMetaError as e:
        sys.exit(f"Error: {e}\nEvery task folder must have a valid meta.yml. README.md was not changed.")

    text = readme_path.read_text(encoding="utf-8")
    text = replace_block(text, "STATS", stats_line(lc, dm, sq, pe))
    text = replace_block(text, "LEETCODE", leetcode_table(lc))
    text = replace_block(text, "DEEPML", deepml_table(dm))
    text = replace_block(text, "SQL", sql_table(sq))
    text = replace_block(text, "PROJECT_EULER", project_euler_table(pe))
    readme_path.write_text(text, encoding="utf-8")
    print(f"README.md updated: LeetCode {len(lc)}, DeepML {len(dm)}, SQL {len(sq)}, Project Euler {len(pe)}.")


if __name__ == "__main__":
    main()
