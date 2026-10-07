# Learner Web build tool

Run commands from the repository root. Create a build environment and install its pinned YAML parser once:

```sh
python3 -m venv apps/learner-web/build-tools/.venv
apps/learner-web/build-tools/.venv/bin/python -m pip install --group apps/learner-web/build-tools/pyproject.toml:build
```

Dependencies are declared in the `build` dependency group in `pyproject.toml`. The install command requires a pip version supporting `--group`; upgrade pip in the virtual environment if that option is unavailable.

The commands below use the environment's Python directly (on Windows, use `.venv/Scripts/python.exe`). PyYAML is a build dependency; no Python or YAML parser ships to the browser. The default build uses English instructions, the Telugu course, the `practical-telugu` course-content folder, and the `telugu` distribution root:

```sh
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py
```

All parameters can be supplied explicitly:

```sh
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py --instruction-language hi --course-name telugu --course-content-folder "practical telugu" --distribution-root telugu
```

For a manual build without creating the project-local virtual environment, let `uv` install and run the declared build dependencies:

```sh
uv run --project apps/learner-web/build-tools --group build python apps/learner-web/build-tools/build.py
uv run --project apps/learner-web/build-tools --group build python apps/learner-web/build-tools/build.py --instruction-language hi --course-name telugu --course-content-folder "practical telugu" --distribution-root telugu
```

The build has four stages:

1. `include_html_files` copies HTML into a temporary workspace and replaces file include markers with the named files.
2. `merge_html_and_instructions` merges the selected course instruction files into lessons and fills every other page from its top-level YAML files.
3. `generate_course_content` inserts canonical course values, verifies that no placeholders remain in the selected lesson HTML, and removes review-only placeholder attributes and classes.
4. `publish_static_site` rejects unresolved placeholders in any page, then copies the prepared HTML, CSS, and assets into `apps/learner-web/dist/<distribution-root>/<instruction-language>/`.

## Firebase authentication bundle

Authentication source and its example course config remain in [`../auth/`](../auth/). Only npm dependencies and build machinery live in [`auth-build/`](auth-build/). From the repository root, run `npm ci --prefix apps/learner-web/build-tools/auth-build` once, then `npm run clean --prefix apps/learner-web/build-tools/auth-build` followed by `npm run build --prefix apps/learner-web/build-tools/auth-build` after changing authentication source. The clean step removes only `apps/learner-web/dist/auth.js`; npm writes the fresh bundle directly to that learner-web `dist/` directory. When a Firebase config is supplied, the regular static build copies the bundle into the generated course distribution at `apps/learner-web/dist/<distribution-root>/<instruction-language>/assets/js/firebase-auth.js` and adds the config and script reference to its HTML pages. The generic `dist/auth.js` is an intermediate artifact, not an upload root.

Authentication is disabled unless an exact course config is passed explicitly with `--firebase-config`. Start from [`firebase-config.example.json`](../auth/firebase-config.example.json), save the filled config as an untracked local file, then run the command from the repository root:

```sh
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py --firebase-config apps/learner-web/auth/firebase-config.telugu.local.json
```

The config's `courseOrigin` must be the course's exact HTTPS subdomain of `brainos.com`; the generated build rejects placeholder values and only accepts `auth.brainos.com` as the Firebase `authDomain`. Make a separate local config and build for every course origin. Never add provider secrets, service-account credentials, or the local config file to a published distribution.

Run the unit tests from the repository root:

```sh
apps/learner-web/build-tools/.venv/bin/python -m unittest discover -s apps/learner-web/build-tools/tests -v
```

Or let `uv` create and use the environment from the build tool's `pyproject.toml`:

```sh
uv run --project apps/learner-web/build-tools --group build python -m unittest discover -s apps/learner-web/build-tools/tests -v
```

Application pages have one HTML source each. `chapter.html` and `lesson.html` are generic sources: the build instantiates them once for every chapter and lesson folder in the selected course. Instruction-language files provide localized values; separate HTML files per language or chapter are not needed. Successive English and Hindi builds create these pages for the current course:

```text
dist/
└── telugu/              # default distribution root; upload this folder, not dist/
    ├── index.html       # default English entry, usable from file or a static server root
    ├── en/              # index, chapter-01, chapter-01-lesson-01, sign-in, patterns
    └── hi/              # the same page names
```

Building one language replaces only that language directory and preserves other generated languages. The shared npm auth artifact is at `dist/auth.js`; `build.py clean` preserves it while clearing generated course outputs so the Docker bind mount remains attached. All generated outputs are ignored and are not committed.

## Page and content naming

| HTML source | Localized instructions | Optional fixed content | Generated page |
| --- | --- | --- | --- |
| `html/pages/index.html` | `content/index.en.yml`, `content/index.hi.yml` | `content/index.yml` | `dist/<root>/<language>/index.html` |
| `html/pages/chapter.html` | `content/subjects/languages/te/courses/practical-telugu/<chapter>/chapter.<language>.yml` | `<chapter>/chapter.yml` | `dist/<root>/<language>/<chapter>.html` |
| `html/pages/lesson.html` | `<chapter>/<lesson>/lesson.<language>.txt` and course `cards.<language>.txt` | `<chapter>/<lesson>/lesson.txt` | `dist/<root>/<language>/<chapter>-<lesson>.html` |
| `html/pages/sign-in.html` | `content/sign-in.<language>.yml` | — | `dist/<root>/<language>/sign-in.html` |
| `html/pages/patterns.html` | `content/patterns.<language>.yml` | `content/patterns.yml` | `dist/<root>/<language>/patterns.html` |

Here `content/` is the repository's top-level content folder; HTML and output paths are relative to `apps/learner-web/`. Application page filename stems must match their top-level YAML files. Course content is selected with `--course-name` and `--course-content-folder`; chapter and lesson folders below that course determine the generated page names and values. `--distribution-root` names the independently deployable folder directly below `dist/` and defaults to `telugu`. For example, `chapter-01/lesson-01/` becomes `dist/telugu/<language>/chapter-01-lesson-01.html`. The generic `chapter-` and `lesson-` placeholder prefixes stay the same for every instance. This convention is build input, not a final educational content schema.

Use a flat YAML mapping with semantic keys prefixed by the page name:

```yaml
# content/index.en.yml
index-heading: "Learn one useful conversation at a time."
index-brand-home-label: "Telugu Tutor home"
```

```html
<h1>[#index-heading]</h1>
<a href="index.html" aria-label="[#index-brand-home-label]">…</a>
```

- Values are plain text and are escaped in both HTML text and attributes. Keep markup, layout, links, element IDs, and semantic structure in HTML. Use YAML block scalars for multiline prose; quote numeric or boolean-looking text.
- Every key must be used; duplicate keys, conflicting fixed/localized values, empty or non-text values, and unresolved placeholders fail the build before publication. Missing translations also fail; there is no silent English fallback.
- `[#instruction-language-tag]` is reserved for the locale declared by the selected course instruction file (`en-IN` or `hi-IN`). Other keys contain only lowercase letters, digits, and hyphens. Values cannot contain placeholder syntax.
- Fixed files hold canonical Telugu, language self-names, and explicitly tagged bilingual review specimens. Translatable page text belongs in language files, including titles, descriptions, and accessibility labels.
- The generated document includes alternate-language metadata. Ordinary relative links preserve the current instruction language. The existing preferences selector reflects the generated language but remains a static control.

To add another application page, create `html/pages/<page>.html` plus `content/<page>.en.yml` and `content/<page>.hi.yml`. The build discovers it automatically. The source should have `<html lang="[#instruction-language-tag]">`; optional shared values go in `content/<page>.yml`.

To add a chapter, create `<course>/<chapter>/chapter.yml`, `chapter.en.yml`, and `chapter.hi.yml` plus its lesson folders. The build discovers the chapter and fills the generic `chapter.html` source from that folder. To add a lesson, place `lesson.txt`, `lesson.en.txt`, `lesson.hi.txt`, `overview.en.yml`, and `overview.hi.yml` under `<chapter>/<lesson>/`. The `lesson.html` source generates the lesson page; the overview files supply that lesson's card in the chapter page. The build renders one card per lesson folder, with links to its distinct generated URL. The chapter template's `<!-- lesson-list:start -->` and `<!-- lesson-list:end -->` markers identify the card to repeat. Only its placeholders and lesson link vary; the existing card layout stays in HTML.

Place `<!--#include file="../includes/account-menu.inc" -->` in a page header to insert [`html/includes/account-menu.inc`](../html/includes/account-menu.inc) before text localization. The filename is relative to the including HTML file and must stay within `html/`. Include files cannot contain other include directives; use multiple markers in the page if needed. Each page's instruction file supplies `account-menu-label`, `account-preferences-link`, and `account-sign-in-link`. Include files are build inputs and are not published. See [ADR-022](../../../doc/design/ARCHITECTURE_DECISION_LOG.md#adr-022--single-level-html-includes-in-the-learner-web-build).

Delete the complete generated distribution without changing source files:

```sh
python3 apps/learner-web/build-tools/build.py clean
```
