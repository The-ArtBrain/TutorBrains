"""Publish prepared learner-web HTML and its static dependencies."""

from pathlib import Path
import re
import shutil
import tempfile

from stages.course_content import _remove_placeholder_markers


def publish_static_site(
    *,
    learner_web_root: Path,
    prepared_html_root: Path,
    instruction_language: str,
    distribution_root: str = "telugu",
) -> int:
    """Atomically publish prepared HTML with unchanged CSS and assets."""

    source_directories = {
        "css": learner_web_root / "css",
        "assets": learner_web_root / "assets",
    }
    prepared_pages_root = prepared_html_root / "pages"
    missing = [source for source in (*source_directories.values(), prepared_pages_root) if not source.is_dir()]
    root_entry = learner_web_root / "index.html"
    if instruction_language.strip().lower() == "en" and not root_entry.is_file():
        missing.append(root_entry)
    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Learner-web source directories are missing: {missing_list}")

    # Check every page before touching an already published language directory.
    for page in prepared_html_root.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        _remove_placeholder_markers(html)
        if "<!--#include" in html:
            raise ValueError(f"Unexpanded HTML include in {page}")

    dist_root = learner_web_root / "dist"
    dist_root.mkdir(exist_ok=True)
    site_root = dist_root / distribution_root
    site_root.mkdir(exist_ok=True)
    destination = site_root / instruction_language.strip().lower()
    with tempfile.TemporaryDirectory(prefix=".language-", dir=site_root) as temporary_directory:
        staging = Path(temporary_directory)

        for page in prepared_pages_root.glob("*.html"):
            html = page.read_text(encoding="utf-8")
            html = re.sub(
                r'(?P<attribute>href|src)="\.\./\.\./(?P<directory>css|assets)/',
                r'\g<attribute>="\g<directory>/',
                html,
            )
            (staging / page.name).write_text(html, encoding="utf-8")

        for name, source in source_directories.items():
            shutil.copytree(
                source,
                staging / name,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", "*.inc"),
            )

        published_files = sum(1 for path in staging.rglob("*") if path.is_file())

        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)

    if instruction_language.strip().lower() == "en":
        shutil.copy2(root_entry, site_root / "index.html")
        published_files += 1

    return published_files
