"""Apply canonical course content and finish generated lesson HTML."""

from pathlib import Path
import re

from stages.merge_instructions import LessonBuild, apply_values, read_values


def _remove_placeholder_markers(html: str) -> str:
    if "[#" in html:
        unresolved = sorted(set(re.findall(r"\[#([^\]]*)\]", html))) or ["malformed placeholder"]
        raise ValueError(f"Unresolved HTML placeholders: {', '.join(unresolved)}")

    html = re.sub(r'\sdata-source="#[a-z0-9-]+"', "", html)

    def clean_classes(match: re.Match[str]) -> str:
        classes = [name for name in match.group(1).split() if name != "data-placeholder"]
        return f'class="{" ".join(classes)}"' if classes else ""

    return re.sub(r'class="([^"]*)"', clean_classes, html)


def generate_course_content(*, lessons: tuple[LessonBuild, ...]) -> tuple[Path, ...]:
    """Insert canonical lesson values and remove resolved placeholder markers."""

    generated: list[Path] = []
    for lesson in lessons:
        html = lesson.html_path.read_text(encoding="utf-8")
        html = apply_values(html, read_values(lesson.content_path), source=lesson.content_path)
        html = _remove_placeholder_markers(html)
        lesson.html_path.write_text(html, encoding="utf-8")
        generated.append(lesson.html_path)

    return tuple(generated)
