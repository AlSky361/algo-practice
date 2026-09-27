#!/usr/bin/env python3
"""
Сканирует leetcode/, deepml/, sql/, project-euler/ и обновляет таблицы
в README.md между маркерами <!-- AUTO:xxx-START --> и <!-- AUTO:xxx-END -->.

Формат meta.yml:
    Для leetcode:
        title: Two Sum
        difficulty: Easy
        pattern: Arrays & Hashing
        url: https://...
        status: Решено              # необязательно, по умолчанию "Решено"
    Для deepml:
        title: Two Sum
        difficulty: Easy
        pattern: Arrays & Hashing
        url: https://...
        status: Решено              # необязательно, по умолчанию "Решено"
    Для project-euler:
        title: Multiples of 3 and 5
        url: https://...
        status: Решено

Язык решения определяется по наличию файлов solution.py / solution.cpp / solution.sql
внутри папки задачи.
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "Ошибка: не установлен PyYAML.\n"
        "Установи его и запусти скрипт снова:\n"
        "  pip install pyyaml --break-system-packages"
    )

ROOT = Path(__file__).parent
LANG_FILES = {
    "solution.py": "Py",
    "solution.cpp": "C++",
    "solution.sql": "SQL",
}


class MissingMetaError(Exception):
    pass


def read_meta(folder: Path) -> dict:
    meta_path = folder / "meta.yml"
    if not meta_path.exists():
        raise MissingMetaError(f"Нет meta.yml в папке: {folder.relative_to(ROOT).as_posix()}")
    try:
        data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise MissingMetaError(f"Не удалось разобрать {meta_path.relative_to(ROOT).as_posix()}: {e}")
    if not data.get("title"):
        raise MissingMetaError(f"В {meta_path.relative_to(ROOT).as_posix()} отсутствует обязательное поле 'title'")
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
            "folder": folder,
            "number": extract_number(folder.name),
            "title": meta.get("title"),
            "difficulty": meta.get("difficulty", "—"),
            "pattern": meta.get("pattern") or meta.get("topic", "—"),
            "status": meta.get("status", "Решено"),
            "lang": languages_in(folder),
            "rel_link": folder.relative_to(ROOT).as_posix(),
        })
    return tasks


def leetcode_table(tasks) -> str:
    if not tasks:
        return "_Пока нет решённых задач._\n"
    header = "| # | Задача | Сложность | Паттерн | Язык | Статус | Решение |\n"
    header += "|---|---|---|---|---|---|---|\n"
    rows = []
    for t in tasks:
        rows.append(
            f"| {t['number']} | {t['title']} | {t['difficulty']} | {t['pattern']} | "
            f"{t['lang']} | {t['status']} | [ссылка]({t['rel_link']}) |"
        )
    return header + "\n".join(rows) + "\n"


def deepml_table(tasks) -> str:
    if not tasks:
        return "_Пока нет решённых задач._\n"
    header = "| # | Задача | Сложность | Тема | Язык | Статус | Решение |\n"
    header += "|---|---|---|---|---|---|---|\n"
    rows = []
    for t in tasks:
        rows.append(
            f"| {t['number']} | {t['title']} | {t['difficulty']} | {t['pattern']} | "
            f"{t['lang']} | {t['status']} | [ссылка]({t['rel_link']}) |"
        )
    return header + "\n".join(rows) + "\n"


def sql_table(tasks) -> str:
    if not tasks:
        return "_Пока нет решённых задач._\n"
    header = "| # | Задача | Сложность | Статус | Решение |\n"
    header += "|---|---|---|---|---|\n"
    rows = []
    for t in tasks:
        rows.append(
            f"| {t['number']} | {t['title']} | {t['difficulty']} | {t['status']} | "
            f"[ссылка]({t['rel_link']}) |"
        )
    return header + "\n".join(rows) + "\n"


def project_euler_table(tasks) -> str:
    if not tasks:
        return "_Пока нет решённых задач._\n"
    header = "| # | Задача | Язык | Статус | Решение |\n"
    header += "|---|---|---|---|---|\n"
    rows = []
    for t in tasks:
        rows.append(
            f"| {t['number']} | {t['title']} | {t['lang']} | {t['status']} | "
            f"[ссылка]({t['rel_link']}) |"
        )
    return header + "\n".join(rows) + "\n"


def stats_line(lc, dm, sq, pe) -> str:
    def counts(tasks):
        e = sum(1 for t in tasks if t["difficulty"] == "Easy")
        m = sum(1 for t in tasks if t["difficulty"] == "Medium")
        h = sum(1 for t in tasks if t["difficulty"] == "Hard")
        return len(tasks), e, m, h

    lc_n, lc_e, lc_m, lc_h = counts(lc)
    dm_n, dm_e, dm_m, dm_h = counts(dm)
    sq_n, sq_e, sq_m, sq_h = counts(sq)

    return (
        f"- **LeetCode**: {lc_n} решено (Easy: {lc_e}, Medium: {lc_m}, Hard: {lc_h})\n"
        f"- **DeepML**: {dm_n} решено (Easy: {dm_e}, Medium: {dm_m}, Hard: {dm_h})\n"
        f"- **SQL**: {sq_n} решено (Easy: {sq_e}, Medium: {sq_m}, Hard: {sq_h})\n"
        f"- **Project Euler**: {len(pe)} решено\n"
    )


def replace_block(text: str, marker: str, new_content: str) -> str:
    start = f"<!-- AUTO:{marker}-START -->"
    end = f"<!-- AUTO:{marker}-END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{new_content}\n{end}"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    else:
        print(f"[!] Маркеры {marker} не найдены в README.md — блок добавлен в конец файла.")
        return text.rstrip() + "\n\n" + replacement + "\n"


def main():
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        sys.exit("Ошибка: README.md не найден рядом со скриптом")

    try:
        lc_tasks = collect_tasks(ROOT / "leetcode")
        dm_tasks = collect_tasks(ROOT / "deepml")
        sq_tasks = collect_tasks(ROOT / "sql")
        pe_tasks = collect_tasks(ROOT / "project-euler")
    except MissingMetaError as e:
        sys.exit(
            f"Ошибка: {e}\n"
            f"У каждой папки задачи должен быть meta.yml. "
            f"README.md не изменён."
        )

    text = readme_path.read_text(encoding="utf-8")
    text = replace_block(text, "STATS", stats_line(lc_tasks, dm_tasks, sq_tasks, pe_tasks))
    text = replace_block(text, "LEETCODE", leetcode_table(lc_tasks))
    text = replace_block(text, "DEEPML", deepml_table(dm_tasks))
    text = replace_block(text, "SQL", sql_table(sq_tasks))
    text = replace_block(text, "PROJECT_EULER", project_euler_table(pe_tasks))

    readme_path.write_text(text, encoding="utf-8")
    print(
        f"README.md обновлён: LeetCode {len(lc_tasks)}, DeepML {len(dm_tasks)}, "
        f"SQL {len(sq_tasks)}, Project Euler {len(pe_tasks)}."
    )


if __name__ == "__main__":
    main()
