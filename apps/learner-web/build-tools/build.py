#!/usr/bin/env python3
"""Build a localized static learner-web distribution."""

import argparse
from pathlib import Path
import re
import shutil
import tempfile

from stages.course_content import generate_course_content
from stages.merge_instructions import merge_html_and_instructions
from stages.publish import publish_static_site


COURSE_SUBJECT_FOLDERS = {"telugu": "te"}


def folder_slug(value: str) -> str:
    """Convert a human-readable name to a repository folder name."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Folder names must contain at least one letter or number")
    return slug


def parse_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("build", "clean"), default="build")
    parser.add_argument("--instruction-language", default="en")
    parser.add_argument("--course-name", default="telugu")
    parser.add_argument("--course-content-folder", default="practical telugu")
    return parser.parse_args(arguments)


def clean_distribution(*, learner_web_root: Path) -> bool:
    """Delete only the generated learner-web distribution directory."""

    destination = learner_web_root / "dist"
    if not destination.exists():
        return False
    shutil.rmtree(destination)
    return True


def resolve_course_root(
    *,
    repository_root: Path,
    course_name: str,
    course_content_folder: str,
) -> Path:
    course_slug = folder_slug(course_name)
    subject_folder = COURSE_SUBJECT_FOLDERS.get(course_slug, course_slug)
    content_folder = folder_slug(course_content_folder)
    return (
        repository_root
        / "content"
        / "subjects"
        / "languages"
        / subject_folder
        / "courses"
        / content_folder
    )


def main(arguments: list[str] | None = None) -> None:
    options = parse_arguments(arguments)
    learner_web_root = Path(__file__).resolve().parents[1]

    if options.command == "clean":
        removed = clean_distribution(learner_web_root=learner_web_root)
        if removed:
            print(f"Deleted {learner_web_root / 'dist'}")
        else:
            print(f"Nothing to clean at {learner_web_root / 'dist'}")
        return

    repository_root = learner_web_root.parents[1]
    course_root = resolve_course_root(
        repository_root=repository_root,
        course_name=options.course_name,
        course_content_folder=options.course_content_folder,
    )

    if not course_root.is_dir():
        raise FileNotFoundError(f"Course content folder does not exist: {course_root}")

    with tempfile.TemporaryDirectory(prefix=".build-", dir=learner_web_root) as temporary_directory:
        work_root = Path(temporary_directory)
        lessons = merge_html_and_instructions(
            source_html_root=learner_web_root / "html",
            work_root=work_root,
            course_root=course_root,
            page_content_root=repository_root / "content",
            instruction_language=options.instruction_language,
        )
        generate_course_content(lessons=lessons)
        published_files = publish_static_site(
            learner_web_root=learner_web_root,
            prepared_html_root=work_root / "html",
            instruction_language=options.instruction_language,
        )

    destination = learner_web_root / "dist" / options.instruction_language.strip().lower()
    print(
        f"Published {published_files} files to {destination} "
        f"for {options.course_name!r}, {options.course_content_folder!r}, "
        f"instruction language {options.instruction_language!r}"
    )


if __name__ == "__main__":
    main()
