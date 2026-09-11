#!/usr/bin/env python3
"""Build the static learner-web distribution."""

from pathlib import Path

from stages.course_content import generate_course_content
from stages.fill_html import fill_and_publish_html


def main() -> None:
    learner_web_root = Path(__file__).resolve().parents[1]
    repository_root = learner_web_root.parents[1]

    course_content = generate_course_content(repository_root=repository_root)
    published_files = fill_and_publish_html(
        learner_web_root=learner_web_root,
        course_content=course_content,
    )

    print(f"Published {published_files} files to {learner_web_root / 'dist'}")


if __name__ == "__main__":
    main()
