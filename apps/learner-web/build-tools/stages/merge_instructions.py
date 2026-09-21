"""Merge application and lesson instructions into staged HTML."""

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import shutil


ENTRY_HEADING = re.compile(r"^\[([a-z0-9-]+)\]$")


@dataclass(frozen=True)
class LessonBuild:
    html_path: Path
    content_path: Path


def read_values(path: Path) -> dict[str, str]:
    """Read `[identifier]` and value blocks from a UTF-8 content file."""

    if not path.is_file():
        raise FileNotFoundError(f"Content file does not exist: {path}")

    values: dict[str, str] = {}
    identifier: str | None = None
    lines: list[str] = []

    def store_entry() -> None:
        if identifier is None:
            return
        value = "\n".join(lines).strip()
        if not value:
            raise ValueError(f"Empty value for [{identifier}] in {path}")
        if identifier in values:
            raise ValueError(f"Duplicate identifier [{identifier}] in {path}")
        values[identifier] = value

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = ENTRY_HEADING.fullmatch(line.strip())
        if heading:
            store_entry()
            identifier = heading.group(1)
            lines = []
        elif identifier is None:
            if line.strip():
                raise ValueError(f"Text appears before the first identifier in {path}")
        else:
            lines.append(line)

    store_entry()
    return values


def merge_values(*sources: tuple[Path, dict[str, str]]) -> dict[str, str]:
    """Merge content maps while rejecting conflicting identifiers."""

    merged: dict[str, str] = {}
    owners: dict[str, Path] = {}
    for path, values in sources:
        for identifier, value in values.items():
            if identifier in merged and merged[identifier] != value:
                raise ValueError(
                    f"Conflicting value for [{identifier}] in {owners[identifier]} and {path}"
                )
            merged[identifier] = value
            owners[identifier] = path
    return merged


def apply_values(html: str, values: dict[str, str], *, source: Path) -> str:
    """Replace visible placeholders and matching hidden data-element text."""

    for identifier, value in values.items():
        token = f"[#{identifier}]"
        data_pattern = re.compile(
            rf'(<data\b[^>]*\bid="{re.escape(identifier)}"[^>]*>)(.*?)(</data>)',
            re.DOTALL,
        )
        if token not in html and not data_pattern.search(html):
            raise ValueError(f"[{identifier}] from {source} is not used by the page HTML")

        safe_value = escape(value, quote=True)
        html = html.replace(token, safe_value)
        html = data_pattern.sub(lambda match: f"{match.group(1)}{safe_value}{match.group(3)}", html)

    return html


def _prepare_localized_document(
    html: str,
    *,
    language: str,
    language_tag: str,
    available_languages: tuple[str, ...],
    page_name: str,
) -> str:
    html = re.sub(r'(<html\b[^>]*\blang=")[^"]+("[^>]*>)', rf"\g<1>{language_tag}\g<2>", html, count=1)

    for available_language in available_languages:
        localized_href = f"../../../{available_language}/html/pages/{page_name}"
        html = re.sub(
            rf'(<link\s+rel="alternate"\s+hreflang="{re.escape(available_language)}"\s+href=")[^"]+("\s*>)',
            rf"\g<1>{localized_href}\g<2>",
            html,
        )

    return html


def merge_html_and_instructions(
    *,
    source_html_root: Path,
    work_root: Path,
    course_root: Path,
    page_content_root: Path,
    instruction_language: str,
) -> tuple[LessonBuild, ...]:
    """Copy source HTML to staging and insert selected instruction-language values."""

    language = instruction_language.strip().lower()
    if not re.fullmatch(r"[a-z]{2,3}(?:-[a-z0-9]+)*", language):
        raise ValueError(f"Invalid instruction language: {instruction_language!r}")

    prepared_html_root = work_root / "html"
    shutil.copytree(source_html_root, prepared_html_root)

    card_instructions_path = course_root / f"cards.{language}.txt"
    card_instructions = read_values(card_instructions_path)
    try:
        language_tag = card_instructions.pop("instruction-language-tag")
    except KeyError as error:
        raise ValueError(f"[instruction-language-tag] is missing from {card_instructions_path}") from error

    available_languages = tuple(
        sorted(path.name.removeprefix("cards.").removesuffix(".txt") for path in course_root.glob("cards.*.txt"))
    )
    lessons: list[LessonBuild] = []

    lesson_directories = sorted(course_root.glob("chapter-*/lesson-*"))
    if not lesson_directories:
        raise FileNotFoundError(f"No lesson content folders found in {course_root}")

    for lesson_directory in lesson_directories:
        lesson_instructions_path = lesson_directory / f"lesson.{language}.txt"
        canonical_content_path = lesson_directory / "lesson.txt"
        page_path = prepared_html_root / "pages" / f"{lesson_directory.name}.html"
        if not page_path.is_file():
            raise FileNotFoundError(f"Lesson HTML does not exist for {language}: {page_path}")

        instructions = merge_values(
            (card_instructions_path, card_instructions),
            (lesson_instructions_path, read_values(lesson_instructions_path)),
        )
        html = _prepare_localized_document(
            page_path.read_text(encoding="utf-8"),
            language=language,
            language_tag=language_tag,
            available_languages=available_languages,
            page_name=page_path.name,
        )
        page_path.write_text(
            apply_values(html, instructions, source=lesson_instructions_path),
            encoding="utf-8",
        )
        lessons.append(LessonBuild(html_path=page_path, content_path=canonical_content_path))

    # Import here to keep the shared placeholder helpers independent of YAML loading.
    from stages.page_instructions import generate_page_instructions

    lesson_paths = {lesson.html_path for lesson in lessons}
    for page_path in sorted(prepared_html_root.rglob("*.html")):
        if page_path not in lesson_paths:
            generate_page_instructions(
                page_path=page_path,
                content_root=page_content_root,
                language=language,
                language_tag=language_tag,
                available_languages=available_languages,
            )

    return tuple(lessons)
