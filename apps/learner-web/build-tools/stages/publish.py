"""Publish prepared learner-web HTML and its static dependencies."""

from pathlib import Path
import shutil
import tempfile


def publish_static_site(
    *,
    learner_web_root: Path,
    prepared_html_root: Path,
    instruction_language: str,
) -> int:
    """Atomically publish prepared HTML with unchanged CSS and assets."""

    source_directories = {
        "html": prepared_html_root,
        "css": learner_web_root / "css",
        "assets": learner_web_root / "assets",
    }
    missing = [source for source in source_directories.values() if not source.is_dir()]
    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Learner-web source directories are missing: {missing_list}")

    dist_root = learner_web_root / "dist"
    dist_root.mkdir(exist_ok=True)
    destination = dist_root / instruction_language.strip().lower()
    with tempfile.TemporaryDirectory(prefix=".language-", dir=dist_root) as temporary_directory:
        staging = Path(temporary_directory)

        for name, source in source_directories.items():
            shutil.copytree(
                source,
                staging / name,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
            )

        published_files = sum(1 for path in staging.rglob("*") if path.is_file())

        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)

    return published_files
