"""Publish prepared learner-web HTML and its static dependencies."""

from pathlib import Path
import json
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
    firebase_config_path: Path | None = None,
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

    firebase_config = None
    auth_bundle = learner_web_root / "dist/auth.js"
    if firebase_config_path is not None:
        if not firebase_config_path.is_file():
            raise FileNotFoundError(f"Firebase config does not exist: {firebase_config_path}")
        if not auth_bundle.is_file():
            raise FileNotFoundError(
                f"Firebase auth bundle is missing: {auth_bundle}. Run npm ci, npm run clean, and npm run build in apps/learner-web/build-tools/auth-build."
            )
        firebase_config = json.loads(firebase_config_path.read_text(encoding="utf-8"))
        firebase_config = validate_firebase_config(firebase_config)

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

        if firebase_config is not None:
            auth_destination = staging / "assets/js"
            auth_destination.mkdir(parents=True, exist_ok=True)
            shutil.copy2(auth_bundle, auth_destination / "firebase-auth.js")
            for page in staging.glob("*.html"):
                html = page.read_text(encoding="utf-8")
                config_script = (
                    "<script>window.BRAINOS_FIREBASE_CONFIG = "
                    + json.dumps(firebase_config, separators=(",", ":"), ensure_ascii=True)
                    + ";</script>\n"
                    + '<script src="assets/js/firebase-auth.js" defer></script>'
                )
                html = html.replace("</body>", f"{config_script}\n</body>")
                page.write_text(html, encoding="utf-8")

        published_files = sum(1 for path in staging.rglob("*") if path.is_file())

        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)

    if instruction_language.strip().lower() == "en":
        shutil.copy2(root_entry, site_root / "index.html")
        published_files += 1

    return published_files


def validate_firebase_config(config: object) -> dict:
    """Validate public per-course Firebase settings before enabling browser auth."""
    if not isinstance(config, dict):
        raise ValueError("Firebase config must be a JSON object")
    firebase = config.get("firebase")
    required = ("apiKey", "authDomain", "projectId", "appId")
    if not isinstance(firebase, dict) or any(not isinstance(firebase.get(key), str) for key in required):
        raise ValueError(f"Firebase config.firebase must contain string values for {', '.join(required)}")
    if set(firebase) != set(required):
        raise ValueError(f"Firebase config.firebase may contain only {', '.join(required)}")
    if firebase["authDomain"].lower() != "auth.brainos.com":
        raise ValueError("Firebase authDomain must be auth.brainos.com")
    if any("<" in firebase[key] or ">" in firebase[key] for key in required):
        raise ValueError("Replace all <placeholder> values in the Firebase config before building")
    origin = config.get("courseOrigin")
    label = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    if not isinstance(origin, str) or not re.fullmatch(rf"https://(?:{label}\.)+brainos\.com", origin):
        raise ValueError("courseOrigin must be an exact HTTPS origin on a course subdomain of brainos.com")
    hostname = origin.removeprefix("https://").lower()
    if hostname == "auth.brainos.com" or not hostname.removesuffix(".brainos.com"):
        raise ValueError("courseOrigin must identify a course subdomain, such as https://learntelugu.brainos.com")
    providers = config.get("enabledProviders", [])
    allowed = {"google", "apple", "facebook", "microsoft", "x", "linkedin"}
    if not isinstance(providers, list) or any(item not in allowed for item in providers):
        raise ValueError(f"enabledProviders may contain only {', '.join(sorted(allowed))}")
    if len(set(providers)) != len(providers):
        raise ValueError("enabledProviders cannot contain duplicates")
    if not isinstance(config.get("phoneEnabled"), bool):
        raise ValueError("phoneEnabled must be true or false")
    course_id = config.get("courseId")
    if not isinstance(course_id, str) or not course_id.strip() or "<" in course_id or ">" in course_id:
        raise ValueError("Replace the courseId placeholder with a stable course identifier")
    return {
        "enabled": True,
        "courseId": course_id,
        "courseOrigin": origin,
        "firebase": firebase,
        "enabledProviders": providers,
        "phoneEnabled": config["phoneEnabled"],
    }
