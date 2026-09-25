# Learner Web build tool

Run commands from the repository root. Create a build environment and install its pinned YAML parser once:

```sh
python3 -m venv apps/learner-web/build-tools/.venv
apps/learner-web/build-tools/.venv/bin/python -m pip install --group apps/learner-web/build-tools/pyproject.toml:build
```

Dependencies are declared in the `build` dependency group in `pyproject.toml`. The install command requires a pip version supporting `--group`; upgrade pip in the virtual environment if that option is unavailable.

The commands below use the environment's Python directly (on Windows, use `.venv/Scripts/python.exe`). PyYAML is a build dependency; no Python or YAML parser ships to the browser. The default build uses English instructions, the Telugu course, and the `practical-telugu` course-content folder:

```sh
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py
```

All parameters can be supplied explicitly:

```sh
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py --instruction-language hi --course-name telugu --course-content-folder "practical telugu"
```

The build has four stages:

1. `include_html_files` copies HTML into a temporary workspace and replaces file include markers with the named files.
2. `merge_html_and_instructions` merges the selected course instruction files into lessons and fills every other page from its top-level YAML files.
3. `generate_course_content` inserts canonical course values, verifies that no placeholders remain in the selected lesson HTML, and removes review-only placeholder attributes and classes.
4. `publish_static_site` rejects unresolved placeholders in any page, then copies the prepared HTML, CSS, and assets into `apps/learner-web/dist/<instruction-language>/`.

Run the unit tests from the repository root:

```sh
apps/learner-web/build-tools/.venv/bin/python -m unittest discover -s apps/learner-web/build-tools/tests -v
```

Application pages have one HTML source each. `chapter.html` and `lesson.html` are generic sources: the build instantiates them once for every chapter and lesson folder in the selected course. Instruction-language files provide localized values; separate HTML files per language or chapter are not needed. Successive English and Hindi builds create these pages for the current course:

```text
dist/
├── index.html           # default English entry, usable from file or a static server root
├── en/                  # index, chapter-01, chapter-01-lesson-01, sign-in, patterns
└── hi/                  # the same page names
```

Building one language replaces only that language directory and preserves other generated languages. The entire `dist/` directory is generated output and is not committed.

## Page and content naming

| HTML source | Localized instructions | Optional fixed content | Generated page |
| --- | --- | --- | --- |
| `html/pages/index.html` | `content/index.en.yml`, `content/index.hi.yml` | `content/index.yml` | `dist/<language>/index.html` |
| `html/pages/chapter.html` | `content/subjects/languages/te/courses/practical-telugu/<chapter>/chapter.<language>.yml` | `<chapter>/chapter.yml` | `dist/<language>/<chapter>.html` |
| `html/pages/lesson.html` | `<chapter>/<lesson>/lesson.<language>.txt` and course `cards.<language>.txt` | `<chapter>/<lesson>/lesson.txt` | `dist/<language>/<chapter>-<lesson>.html` |
| `html/pages/sign-in.html` | `content/sign-in.<language>.yml` | — | `dist/<language>/sign-in.html` |
| `html/pages/patterns.html` | `content/patterns.<language>.yml` | `content/patterns.yml` | `dist/<language>/patterns.html` |

Here `content/` is the repository's top-level content folder; HTML and output paths are relative to `apps/learner-web/`. Application page filename stems must match their top-level YAML files. Course content is selected with `--course-name` and `--course-content-folder`; chapter and lesson folders below that course determine the generated page names and values. For example, `chapter-01/lesson-01/` becomes `chapter-01-lesson-01.html`. The generic `chapter-` and `lesson-` placeholder prefixes stay the same for every instance. This convention is build input, not a final educational content schema.

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
