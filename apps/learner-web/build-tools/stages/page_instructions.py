"""Generate non-lesson pages from top-level, page-named YAML content."""

from pathlib import Path
import re

import yaml

from stages.course_content import _remove_placeholder_markers
from stages.merge_instructions import apply_values, merge_values


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys instead of losing content."""

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("YAML content keys must be strings")
            if key in result:
                raise ValueError(f"Duplicate identifier [{key}]")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def read_yaml_values(path: Path) -> dict[str, str]:
    """Read a flat mapping of placeholder identifiers to plain text."""

    if not path.is_file():
        raise FileNotFoundError(f"Content file does not exist: {path}")
    try:
        values = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        if not isinstance(values, dict) or not values:
            raise ValueError("YAML content must be a nonempty mapping")
        for key, value in values.items():
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key):
                raise ValueError(f"Invalid placeholder identifier: {key!r}")
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"[{key}] must contain nonempty text; quote numbers and booleans")
            if "[#" in value:
                raise ValueError(f"[{key}] contains reserved placeholder syntax")
    except (yaml.YAMLError, ValueError) as error:
        raise ValueError(f"Invalid YAML content in {path}: {error}") from error
    return values


def generate_page_instructions(
    *,
    page_path: Path,
    content_root: Path,
    language: str,
    language_tag: str,
    available_languages: tuple[str, ...],
    content_stem: str | None = None,
) -> None:
    """Fill one HTML page without changing its layout or adding visible controls."""

    stem = content_stem or page_path.stem
    localized_path = content_root / f"{stem}.{language}.yml"
    shared_path = content_root / f"{stem}.yml"
    sources = []
    if shared_path.is_file():
        sources.append((shared_path, read_yaml_values(shared_path)))
    sources.append((localized_path, read_yaml_values(localized_path)))
    values = merge_values(*sources)

    # The course's selected instruction locale applies to every generated page.
    if "instruction-language-tag" in values:
        raise ValueError(f"instruction-language-tag is build-owned: {localized_path}")
    values["instruction-language-tag"] = language_tag
    html = apply_values(page_path.read_text(encoding="utf-8"), values, source=localized_path)

    # Discovery metadata has no visible effect. Relative page links stay in this locale.
    alternates = "\n".join(
        f'    <link rel="alternate" hreflang="{candidate}" '
        f'href="../../../{candidate}/html/pages/{page_path.name}">'
        for candidate in available_languages
        if (content_root / f"{stem}.{candidate}.yml").is_file()
    )
    html = html.replace("  </head>", f"{alternates}\n  </head>", 1)

    # Reflect the generated language in the existing static preferences control.
    def select_language(match: re.Match[str]) -> str:
        option = re.sub(r"\sselected(?:=\"[^\"]*\")?", "", match.group(0))
        if match.group(1) == language:
            option = option[:-1] + " selected>"
        return option

    if page_path.stem == "preferences":
        html = re.sub(r'<option\s+lang="([^"]+)"[^>]*>', select_language, html)

    page_path.write_text(_remove_placeholder_markers(html), encoding="utf-8")
