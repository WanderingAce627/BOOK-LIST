#!/usr/bin/env python3
"""扫描 books/ 目录，重新生成 README.md 中的书籍清单表格。

用法:
    python3 scripts/build_index.py

文件名约定（可选）: "书名 - 作者.epub"
    - 按最后一个 " - " 拆分书名与作者
    - 不写作者也能正常工作
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
README = ROOT / "README.md"

EXTENSIONS = {".pdf", ".epub", ".mobi", ".azw3", ".azw", ".txt", ".djvu", ".chm", ".fb2"}
START_MARK = "<!-- BOOKLIST:START -->"
END_MARK = "<!-- BOOKLIST:END -->"


def human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} GB"


def parse_name(stem: str) -> tuple[str, str]:
    """从文件名解析 (书名, 作者)。"""
    parts = re.split(r"\s+-\s+", stem, maxsplit=1)
    if len(parts) == 2 and parts[1].strip():
        return parts[0].strip(), parts[1].strip()
    return stem.strip(), "—"


def collect_books() -> list[tuple[str, str, str, str, int, str]]:
    """返回 (书名, 作者, 分类, 格式, 大小, 相对路径) 列表。"""
    rows = []
    for path in sorted(BOOKS_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        rel = path.relative_to(ROOT)
        category = rel.parts[1] if len(rel.parts) > 2 else "—"
        title, author = parse_name(path.stem)
        rows.append((
            title,
            author,
            category,
            path.suffix.lstrip(".").upper(),
            path.stat().st_size,
            rel.as_posix(),
        ))
    rows.sort(key=lambda r: (r[2], r[0].lower()))
    return rows


def render_table(rows: list[tuple[str, str, str, str, int, str]]) -> str:
    header = (
        "| # | 书名 | 作者 | 分类 | 格式 | 大小 | 文件 |\n"
        "| :-: | :--- | :--- | :--- | :--: | ---: | :--- |"
    )
    if not rows:
        return (
            header
            + "\n| — | *暂无书籍，把文件放进 `books/` 后运行 "
            "`python3 scripts/build_index.py`* | | | | | |"
        )

    lines = [header]
    for i, (title, author, category, fmt, size, rel) in enumerate(rows, 1):
        name = Path(rel).name
        lines.append(
            f"| {i} | {title} | {author} | {category} | {fmt} | "
            f"{human_size(size)} | [{name}](<{rel}>) |"
        )
    return "\n".join(lines)


def update_readme(table: str) -> bool:
    text = README.read_text(encoding="utf-8")
    if START_MARK not in text or END_MARK not in text:
        sys.exit(f"README.md 缺少标记 {START_MARK} / {END_MARK}")

    pattern = re.compile(
        re.escape(START_MARK) + r".*?" + re.escape(END_MARK), re.DOTALL
    )
    new_text = pattern.sub(f"{START_MARK}\n{table}\n{END_MARK}", text)
    if new_text == text:
        return False
    README.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    if not BOOKS_DIR.is_dir():
        sys.exit("找不到 books/ 目录")
    rows = collect_books()
    changed = update_readme(render_table(rows))
    print(f"共 {len(rows)} 本书" + ("，README.md 已更新" if changed else "，无变化"))
    for title, author, *_ in rows:
        print(f"  · {title} — {author}")


if __name__ == "__main__":
    main()
