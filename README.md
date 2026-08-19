# TeluguTutorbrain

A Telugu teacher.

## Product specifications

- [Student onboarding guide](doc/spec/student_onboarding_guide.md) — student actions before Chapter 01, mapped to the capability catalogue.
- [Common product specification](doc/spec/common_spec.md) — tutor behaviour inherited by every chapter.
- [Chapter 01 Tutor Product Requirements Document](doc/spec/CHAPTER_01_TUTOR_PRD.md) — the first guided greeting lesson.
- [Capability matrix](doc/spec/capability_matrix.md) — technology-neutral product capabilities and ability-based authorization.
- [Platform and logical presentation specification](doc/spec/platform_spec.md) — required platforms, local-intelligence boundaries, component inventory, and the card model.
- [Character units](doc/spec/characters_spec.md), [grammar units](doc/spec/grammar_spec.md), [vocabulary units](doc/spec/vocabulary_spec.md), and [sentence units](doc/spec/sentence_spec.md) — reusable learning-unit definitions.

## Technical designs

- [Architecture Decision Record log](doc/design/ARCHITECTURE_DECISION_LOG.md) — current fixed, accepted, proposed, and deferred architecture decisions.
- [App skeleton technical design](doc/design/APP_SKELETON_TECH_DESIGN.md) — shared semantic HTML and standard JavaScript architecture, platform-service contracts, and comparison of three potential schemes.
- [Progressive Web App platform design](doc/design/PWA_PLATFORM_DESIGN.md) — browser-installed candidate and its required-platform proof burden.
- [Tauri platform design](doc/design/TAURI_PLATFORM_DESIGN.md) — Tauri 2.0 candidate with a Rust client boundary.
- [Capacitor and Electron platform design](doc/design/CAPACITOR_ELECTRON_PLATFORM_DESIGN.md) — Capacitor for Android and iOS plus Electron for Windows and macOS.
- [Platform scheme Frequently Asked Questions](doc/design/PLATFORM_OPTIONS_FAQ.md) — reasons Valdi, .NET Multi-platform App UI, Flutter, and other options are not currently shortlisted.
