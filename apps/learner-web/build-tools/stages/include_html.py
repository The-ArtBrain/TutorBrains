"""Expand file includes in HTML before instruction values are merged."""

from pathlib import Path
import re
import shutil
from textwrap import indent


INCLUDE = re.compile(r'(?m)^([ \t]*)<!--#include file="([^"]+)" -->[ \t]*$')


def include_html_files(*, source_html_root: Path, destination_html_root: Path) -> None:
    """Copy HTML sources and replace each include with its named file."""

    shutil.copytree(source_html_root, destination_html_root)
    root = source_html_root.resolve()
    for page in destination_html_root.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        source_page = root / page.relative_to(destination_html_root)

        def insert(match: re.Match[str]) -> str:
            included = (source_page.parent / match.group(2)).resolve()
            if not included.is_relative_to(root):
                raise ValueError(f"HTML include escapes source directory: {page}")
            content = included.read_text(encoding="utf-8")
            if "<!--#include" in content:
                raise ValueError(f"Nested HTML include is not allowed in {included}")
            return indent(content.rstrip(), match.group(1))

        expanded = INCLUDE.sub(insert, html)
        if "<!--#include" in expanded:
            raise ValueError(f"Unresolved HTML include in {page}")
        page.write_text(expanded, encoding="utf-8")
