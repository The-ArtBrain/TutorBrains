# Project Memory

## Directory Structure

```text
TutorBrains/
├── README.md
├── memory.md
└── doc/
    ├── design/
    │   ├── APP_SKELETON_TECH_DESIGN.md
    │   ├── ARCHITECTURE_DECISION_LOG.md
    │   ├── CAPACITOR_ELECTRON_PLATFORM_DESIGN.md
    │   ├── PLATFORM_OPTIONS_FAQ.md
    │   ├── PWA_PLATFORM_DESIGN.md
    │   ├── TAURI_PLATFORM_DESIGN.md
    │   └── project_structure.md
    └── spec/
        ├── CHAPTER_01_TUTOR_PRD.md
        ├── capability_matrix.md
        ├── characters_spec.md
        ├── common_spec.md
        ├── grammar_spec.md
        ├── platform_spec.md
        ├── sentence_spec.md
        ├── student_onboarding_guide.md
        └── vocabulary_spec.md
```

## Directory Purpose

- `doc/` contains project documentation.
- `doc/design/` contains implementation designs, candidate platform schemes, and the Architecture Decision Record (ADR) log. These designs implement the product specifications but do not override them.
- `doc/spec/` contains product specifications and product requirements documents (PRDs).
- `ARCHITECTURE_DECISION_LOG.md` is the current index of fixed, accepted, proposed, and deferred architecture decisions.
- `APP_SKELETON_TECH_DESIGN.md` defines the shared semantic Hypertext Markup Language (HTML) and standard JavaScript application skeleton and compares the shortlisted schemes.
- `PWA_PLATFORM_DESIGN.md`, `TAURI_PLATFORM_DESIGN.md`, and `CAPACITOR_ELECTRON_PLATFORM_DESIGN.md` define the three candidate platform schemes.
- `PLATFORM_OPTIONS_FAQ.md` records shortlist criteria, rejected alternatives, and reconsideration triggers.
- `project_structure.md` proposes the subject-neutral TutorBrains repository organization, product manifests, and trusted build-time specialization boundaries.
- `characters_spec.md` defines the chapter-neutral model for independently accessible Telugu script units; chapters own the lesson links.
- `common_spec.md` defines tutor behaviour and product requirements inherited by every chapter.
- `grammar_spec.md` defines the chapter-neutral model for independently accessible grammar and usage units; chapters own the lesson links.
- `CHAPTER_01_TUTOR_PRD.md` defines the tutor product requirements driven by the Chapter 01 lesson specification.
- `capability_matrix.md` defines the technology-neutral product capabilities and ability-based authorization model.
- `platform_spec.md` defines platform requirements, runtime boundaries, and platform-neutral presentation entities.
- `sentence_spec.md` defines the chapter-neutral model for independently accessible sentence units.
- `student_onboarding_guide.md` defines the student journey before Chapter 01 and maps each action to the capability catalogue.
- `vocabulary_spec.md` defines the chapter-neutral model for independently accessible vocabulary units.

## Architecture Decisions

The product decisions in `doc/spec/platform_spec.md` remain authoritative. `doc/design/ARCHITECTURE_DECISION_LOG.md` records their implementation consequences and must be updated when an architecture decision changes.

### Fixed and accepted product direction

- Android, iOS, Windows, and macOS are required production platforms; Web remains optional.
- Cards use one flat, reusable contract with no child Cards or Card inheritance. Lessons, chapters, courses, and tables of contents are external ordered collections.
- Cards request narrow capability-oriented platform and intelligence service handles. They do not depend on providers, models, native plug-ins, storage paths, or network endpoints.
- Product functions and required intelligence run in the client wherever technically feasible. Missing or unreliable intelligence produces an alternative or **Not assessed**, never silent upload or fabricated feedback.
- Canonical Telugu, instruction language, interface locale, transliteration, and accessibility preferences are independent. English is the disclosed instruction-language default when no selection exists.
- Authorization grants explicit abilities over resources and constraints rather than roles or personas.
- Commerce remains outside the learning applications and Telugu Tutor platform. A separate commerce application or service owns offers, payments, subscriptions, refunds, taxes, and transaction reconciliation and communicates only explicit, scoped, and optionally time-bounded ability changes. Paid and non-paid access use the same authorization contract; Cards never receive commerce state.
- TutorBrains is the subject-neutral repository and shared platform. Telugu Tutor is its first focused product. Declarative product manifests select trusted build-time subject, script, and target-language specializations; instruction-language support remains data-first, and downloaded course packages remain data-only.

### Accepted implementation direction

- Build Chapter 01 as the first localized read-and-speak slice in a Progressive Web App (PWA). English remains the default instruction language, and Hindi is the second instruction language used to prove localization and fallback behavior.
- Include account creation and sign-in plus ability-based restricted-content authorization. Use a minimal connected platform for identity integration, token validation, and authoritative ability or entitlement evaluation while keeping lesson behavior and progress client-first.
- Synchronization, remote inference, content publication, learner-initiated account or submission exports, and automatic pronunciation assessment remain outside the first slice unless separately accepted. Commercial purchase flows remain permanently outside the learning platform. The Chapter 01 pilot-data export remains required research instrumentation.
- Keep Tauri as an escalation path only when evidence demonstrates a native requirement that the PWA cannot meet adequately.
- Keep educational-domain meaning in manifests and domain records; HTML owns document and interaction semantics.
- Keep authored assets, course content, model resources, learner records, raw learner evidence, and exports as separate data classes.

### Proposed and deferred decisions

- Proposed: course packages contain reviewed content and media, while executable behavior remains application-owned.
- Proposed: when connected services become necessary, begin with a modular monolith rather than microservices.
- Deferred: the final production host remains open among PWA, Tauri 2.0, and Capacitor mobile plus Electron desktop until cross-platform evidence selects one.
- Deferred: select no backend language until a validated server requirement exists.

## Working Conventions

- Understand the directory structure and the purpose of the relevant folders before adding, moving, or changing files.
- When work includes Artificial Intelligence (AI) assistance, provide appropriate attribution in the resulting commit or deliverable.

Update this file when the project structure or the purpose of a directory changes.
