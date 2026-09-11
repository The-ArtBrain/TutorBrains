"""Fill and publish learner-web HTML."""

from pathlib import Path
import shutil
import tempfile


PUBLISHED_DIRECTORIES = ("html", "css", "assets")


def fill_and_publish_html(
    *,
    learner_web_root: Path,
    course_content: tuple[Path, ...],
) -> int:
    """Publish the current static site unchanged.

    The course-content argument is reserved for the later placeholder-filling
    step. In the first slice, the source directories are copied as-is.
    """

    del course_content

    source_directories = [learner_web_root / name for name in PUBLISHED_DIRECTORIES]
    missing = [source for source in source_directories if not source.is_dir()]
    if missing:
        missing_list = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Learner-web source directories are missing: {missing_list}")

    destination = learner_web_root / "dist"
    with tempfile.TemporaryDirectory(prefix=".dist-", dir=learner_web_root) as temporary_directory:
        staging = Path(temporary_directory)

        for source in source_directories:
            shutil.copytree(
                source,
                staging / source.name,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
            )

        published_files = sum(1 for path in staging.rglob("*") if path.is_file())

        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)

    return published_files
