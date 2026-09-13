# Learner Web build tool

Run the learner-web build from the repository root. The default build uses English instructions, the Telugu course, and the `practical-telugu` course-content folder:

```sh
python3 apps/learner-web/build-tools/build.py
```

All parameters can be supplied explicitly:

```sh
python3 apps/learner-web/build-tools/build.py  --instruction-language hi --course-name telugu --course-content-folder "practical telugu"
```

The build has three stages:

1. `merge_html_and_instructions` copies the shared lesson HTML into a temporary workspace and merges the selected application and lesson instruction files into it.
2. `generate_course_content` inserts canonical course values, verifies that no placeholders remain in the selected lesson HTML, and removes review-only placeholder attributes and classes.
3. `publish_static_site` copies the prepared HTML, CSS, and assets into `apps/learner-web/dist/<instruction-language>/`.

Run the unit tests from the repository root:

```sh
python3 -m unittest discover -s apps/learner-web/build-tools/tests -v
```

The source contains one lesson HTML file, such as `html/pages/lesson-01.html`. Instruction-language files provide the localized values; a separate HTML template per language is not needed. For example, successive English and Hindi builds create:

```text
dist/
├── en/html/pages/lesson-01.html
└── hi/html/pages/lesson-01.html
```

Building one language replaces only that language directory and preserves other generated languages. The entire `dist/` directory is generated output and is not committed.

Delete the complete generated distribution without changing source files:

```sh
python3 apps/learner-web/build-tools/build.py clean
```
