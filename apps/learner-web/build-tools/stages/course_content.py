"""Prepare course content for the learner-web build."""

from pathlib import Path


def generate_course_content(*, repository_root: Path) -> tuple[Path, ...]:
    """Return generated course-content inputs.

    Course-content generation is intentionally empty in the first build slice.
    The repository root is accepted now so this stage can grow without changing
    the build coordinator's interface.
    """

    if not repository_root.is_dir():
        raise FileNotFoundError(f"Repository root does not exist: {repository_root}")

    return ()
