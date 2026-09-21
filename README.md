# TutorBrains

A subject-neutral learning platform. Telugu Tutor is its first focused product.

## Learner web commands

Run the end-to-end tests from the repository root:

```sh
npm --prefix tests/end-to-end/learner-web test
```

Debug one test with Playwright Inspector, replacing `TC-16` as needed:

```sh
npm --prefix tests/end-to-end/learner-web test -- --debug --grep "TC-16"
```

Watch the complete suite run in a visible browser:

```sh
npm --prefix tests/end-to-end/learner-web test -- --headed --workers=1
```

Set up the build environment once, then generate the English and Hindi pages from the repository root:

```sh
python3 -m venv apps/learner-web/build-tools/.venv
apps/learner-web/build-tools/.venv/bin/python -m pip install --group apps/learner-web/build-tools/pyproject.toml:build
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py
apps/learner-web/build-tools/.venv/bin/python apps/learner-web/build-tools/build.py --instruction-language hi
```

The defaults are English instructions, the Telugu course, and the `practical-telugu` content folder; output is published below `apps/learner-web/dist/en/` and `dist/hi/`. Open the generated `html/pages/index.html` in either directory. Application pages use top-level `content/<page>.<language>.yml` files. Generic chapter and lesson HTML sources are filled from the selected course's chapter and lesson folders, producing identity-specific filenames. See [`apps/learner-web/build-tools/README.md`](apps/learner-web/build-tools/README.md) for conventions, parameters, and unit tests. Browser tests build both languages automatically using this environment (or `LEARNER_WEB_PYTHON`).

Remove all generated learner-web output with `python3 apps/learner-web/build-tools/build.py clean`.

## Product specifications

- [Student onboarding guide](doc/spec/student_onboarding_guide.md) — student actions before Chapter 01, mapped to the capability catalogue.
- [Common product specification](doc/spec/common_spec.md) — tutor behaviour inherited by every chapter.
- [Chapter 01 Tutor Product Requirements Document](doc/spec/CHAPTER_01_TUTOR_PRD.md) — the first guided greeting lesson.
- [Capability matrix](doc/spec/capability_matrix.md) — technology-neutral product capabilities and ability-based authorization.
- [Platform and logical presentation specification](doc/spec/platform_spec.md) — required platforms, local-intelligence boundaries, component inventory, and the card model.
- [Character units](doc/spec/characters_spec.md), [grammar units](doc/spec/grammar_spec.md), [vocabulary units](doc/spec/vocabulary_spec.md), and [sentence units](doc/spec/sentence_spec.md) — reusable learning-unit definitions.

## Technical designs

- [Architecture Decision Record log](doc/design/ARCHITECTURE_DECISION_LOG.md) — current fixed, accepted, proposed, and deferred architecture decisions.
- [Proposed project structure](doc/design/project_structure.md) — subject-neutral repository organization and build-time specialization boundaries.
- [App skeleton technical design](doc/design/APP_SKELETON_TECH_DESIGN.md) — shared semantic HTML and standard JavaScript architecture, platform-service contracts, and comparison of three potential schemes.
- [Progressive Web App platform design](doc/design/PWA_PLATFORM_DESIGN.md) — browser-installed candidate and its required-platform proof burden.
- [Tauri platform design](doc/design/TAURI_PLATFORM_DESIGN.md) — Tauri 2.0 candidate with a Rust client boundary.
- [Capacitor and Electron platform design](doc/design/CAPACITOR_ELECTRON_PLATFORM_DESIGN.md) — Capacitor for Android and iOS plus Electron for Windows and macOS.
- [Platform scheme Frequently Asked Questions](doc/design/PLATFORM_OPTIONS_FAQ.md) — reasons Valdi, .NET Multi-platform App UI, Flutter, and other options are not currently shortlisted.
