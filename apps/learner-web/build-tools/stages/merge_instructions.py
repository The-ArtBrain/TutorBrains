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
    pages_root = prepared_html_root / "pages"
    chapter_template = pages_root / "chapter.html"
    lesson_template = pages_root / "lesson.html"
    if not chapter_template.is_file() or not lesson_template.is_file():
        raise FileNotFoundError("Generic chapter.html and lesson.html sources are required")
    chapter_html = chapter_template.read_text(encoding="utf-8")
    lesson_html = lesson_template.read_text(encoding="utf-8")
    chapter_template.unlink()
    lesson_template.unlink()

    chapters = sorted(path for path in course_root.glob("chapter-*") if path.is_dir())
    if not chapters:
        raise FileNotFoundError(f"No chapter content folders found in {course_root}")

    # Import here to keep the shared placeholder helpers independent of YAML loading.
    from stages.page_instructions import generate_page_instructions, read_yaml_values

    lessons: list[LessonBuild] = []
    first_lesson_name: str | None = None
    for chapter_directory in chapters:
        lesson_directories = sorted(path for path in chapter_directory.glob("lesson-*") if path.is_dir())
        if not lesson_directories:
            raise FileNotFoundError(f"No lesson content folders found in {chapter_directory}")

        chapter_name = f"{chapter_directory.name}.html"
        lesson_names = [f"{chapter_directory.name}-{path.name}.html" for path in lesson_directories]
        first_lesson_name = first_lesson_name or lesson_names[0]
        chapter_path = pages_root / chapter_name
        start_marker = "<!-- lesson-list:start -->"
        end_marker = "<!-- lesson-list:end -->"
        before, separator, remaining = chapter_html.partition(start_marker)
        listing_template, end_separator, after = remaining.partition(end_marker)
        if not separator or not end_separator:
            raise ValueError("Generic chapter.html must contain one lesson-list marker pair")
        listings = []
        for lesson_directory, lesson_name in zip(lesson_directories, lesson_names):
            overview_path = lesson_directory / f"overview.{language}.yml"
            listing = listing_template.replace('id="lesson-title"', f'id="{lesson_directory.name}-title"')
            listing = listing.replace('aria-labelledby="lesson-title"', f'aria-labelledby="{lesson_directory.name}-title"')
            listing = listing.replace('href="lesson.html"', f'href="{lesson_name}"')
            listing = apply_values(listing, read_yaml_values(overview_path), source=overview_path)
            listings.append(listing.strip("\n"))
        chapter_path.write_text(before + "\n".join(listings) + after, encoding="utf-8")
        generate_page_instructions(
            page_path=chapter_path,
            content_root=chapter_directory,
            content_stem="chapter",
            language=language,
            language_tag=language_tag,
            available_languages=available_languages,
        )

        for lesson_directory, lesson_name in zip(lesson_directories, lesson_names):
            lesson_instructions_path = lesson_directory / f"lesson.{language}.txt"
            canonical_content_path = lesson_directory / "lesson.txt"
            page_path = pages_root / lesson_name
            instructions = merge_values(
                (card_instructions_path, card_instructions),
                (lesson_instructions_path, read_values(lesson_instructions_path)),
            )
            html = lesson_html.replace('href="chapter.html"', f'href="{chapter_name}"')
            html = _prepare_localized_document(
                html,
                language=language,
                language_tag=language_tag,
                available_languages=available_languages,
                page_name=page_path.name,
            )
            page_path.write_text(apply_values(html, instructions, source=lesson_instructions_path), encoding="utf-8")
            lessons.append(LessonBuild(html_path=page_path, content_path=canonical_content_path))

    first_chapter_name = f"{chapters[0].name}.html"
    lesson_paths = {lesson.html_path for lesson in lessons}
    for page_path in sorted(prepared_html_root.rglob("*.html")):
        if page_path not in lesson_paths:
            if page_path.name == first_chapter_name or any(page_path.name == f"{chapter.name}.html" for chapter in chapters):
                continue
            html = page_path.read_text(encoding="utf-8")
            html = html.replace('href="chapter.html"', f'href="{first_chapter_name}"')
            html = html.replace('href="lesson.html"', f'href="{first_lesson_name}"')
            page_path.write_text(html, encoding="utf-8")
            generate_page_instructions(
                page_path=page_path,
                content_root=page_content_root,
                language=language,
                language_tag=language_tag,
                available_languages=available_languages,
            )

    return tuple(lessons)
