# Architecture Decision Record Log

**Status:** Active discussion log  
**Last reviewed:** 2026-08-27  
**Scope:** Current product-platform and app-skeleton architecture decisions  
**Authority:** Product decisions remain authoritative in the [platform specification](../spec/platform_spec.md); this log summarizes them alongside implementation decisions.

This file is the Architecture Decision Record (ADR) index for the current design. An **Accepted** entry governs the stated scope. **Accepted for first slice** does not select the final production architecture. **Proposed** requires review before it becomes binding. **Deferred** records a choice that should not be made yet.

## ADR-001 — Required production platforms

- **Status:** Accepted; fixed product decision
- **Decision:** Android, iOS, Windows, and macOS are required production platforms. Web remains optional.
- **Rationale:** Required platforms must support offline lessons, device capabilities, and adequate local intelligence without making a browser or permanent connection a prerequisite.
- **Consequence:** Selecting a Progressive Web App (PWA) as the final production scheme requires cross-platform evidence and an explicit amendment to the platform specification.
- **Source:** [Platform specification, fixed decisions](../spec/platform_spec.md#2-fixed-platform-decisions)

## ADR-002 — PWA for the first implementation slice

- **Status:** Accepted for first slice
- **Decision:** Implement Chapter 01 as the first localized read-and-speak learning slice in a PWA. English remains the default instruction language, and Hindi is the second instruction language used to prove localization and fallback behavior.
- **Rationale:** Chapter 01 already defines the lesson outcome, content, activities, and evidence. Semantic Hypertext Markup Language (HTML), standard JavaScript, browser media APIs, offline caching, and local browser storage cover its core learner behavior with the smallest application-specific dependency surface.
- **Consequence:** This experiment does not establish that a PWA satisfies every production-platform requirement.
- **Source:** [Platform options FAQ](PLATFORM_OPTIONS_FAQ.md#what-is-the-current-decision-for-the-first-implementation-slice)

## ADR-003 — Accounts and restricted-content authorization in the first slice

- **Status:** Accepted for first slice
- **Decision:** Include account creation and sign-in plus ability-based authorization for restricted content. Keep Telugu content, localized instructions, reference audio, recording and playback behavior, and local preferences or progress client-first.
- **Rationale:** The first slice must exercise the existing identity choices and verify that restricted access is granted by explicit abilities rather than roles or purchase state.
- **Consequence:** A minimal connected platform is required for identity integration, token validation, and authoritative ability or entitlement evaluation. Synchronization, remote inference, publication, and learner-initiated account or submission exports remain outside the first slice unless separately accepted. Commercial purchase flows remain outside the learning platform under ADR-017.
- **Source:** [Platform options FAQ](PLATFORM_OPTIONS_FAQ.md#what-is-the-current-decision-for-the-first-implementation-slice)

## ADR-004 — Tauri as an escalation path

- **Status:** Accepted
- **Decision:** Do not make Tauri an assumed foundation. Introduce it only after evidence demonstrates a native requirement that the PWA cannot satisfy adequately.
- **Rationale:** Tauri adds native code, builds, plug-ins, permissions, signing, and maintenance without improving semantic HTML, localization, Card architecture, or teaching behavior by itself.
- **Consequence:** Reconsider Tauri for inadequate local-model performance, browser-storage durability, native secure storage or SQLite, required store packaging, missing device APIs, background work, or essential operating-system integration.
- **Source:** [Platform options FAQ](PLATFORM_OPTIONS_FAQ.md#what-is-the-current-decision-for-the-first-implementation-slice)

## ADR-005 — Production application host remains open

- **Status:** Deferred
- **Decision:** Do not yet select the final production host.
- **Rationale:** The same Card and platform-service contracts must be tested through representative cross-platform fixtures before accepting a host.
- **Consequence:** PWA, Tauri 2.0, and Capacitor mobile plus Electron desktop remain candidate schemes, even though the PWA leads the first slice.
- **Source:** [App skeleton, potential schemes](APP_SKELETON_TECH_DESIGN.md#4-potential-platform-schemes)

## ADR-006 — Semantic HTML and standard JavaScript Cards

- **Status:** Accepted
- **Decision:** Represent learner-facing Cards as semantic HTML activated with standard JavaScript.
- **Rationale:** Native document and control semantics support accessibility, localization, reviewability, progressive activation, and portability without making a frontend framework authoritative.
- **Consequence:** React, Vue, Svelte, Flutter widgets, canvas-only presentation, and similar component systems are not part of the initial Card contract.
- **Source:** [App skeleton, semantic HTML Card contract](APP_SKELETON_TECH_DESIGN.md#semantic-html-card-contract)

## ADR-007 — Separate HTML meaning from educational-domain meaning

- **Status:** Accepted
- **Decision:** Use HTML for document and interaction semantics; use structured manifests and domain records for Lesson, Card, Character Unit, Word Unit, abilities, services, evidence, and accomplishment meaning.
- **Rationale:** HTML defines elements such as articles, headings, paragraphs, buttons, audio, and output, but it does not define the Telugu Tutor curriculum model.
- **Consequence:** Educational entities are not invented as authoritative custom HTML elements. HTML may carry stable references such as `data-card-id`, while the manifest remains authoritative.
- **Source:** [App skeleton, semantic HTML Card contract](APP_SKELETON_TECH_DESIGN.md#semantic-html-card-contract)

## ADR-008 — Flat reusable Cards

- **Status:** Accepted; fixed product decision
- **Decision:** Maintain one flat Card contract with no child Cards and no Card inheritance.
- **Rationale:** Cards are reusable presentation and activity definitions; curriculum composition and durable learner history are separate concerns.
- **Consequence:** Lessons, chapters, courses, and tables of contents are external ordered Card collections. Submissions, Evaluations, Accomplishments, and retained evidence are separate durable records.
- **Source:** [Platform specification, Card as a flat presentation entity](../spec/platform_spec.md#card-as-a-flat-presentation-entity)

## ADR-009 — Stable platform and intelligence service handles

- **Status:** Accepted; fixed product decision
- **Decision:** Cards request narrow, capability-oriented service handles bound during Card initialization.
- **Rationale:** Educational behavior must not depend on a provider, model, native plug-in, runtime, filesystem location, or network endpoint.
- **Consequence:** Registries and Evaluations retain implementation provenance; Cards see compatible contracts and results rather than provider identity.
- **Source:** [Platform specification, registered services](../spec/platform_spec.md#registered-service-and-intelligence-components)

## ADR-010 — Client-first and local-intelligence capable

- **Status:** Accepted; fixed product decision
- **Decision:** Run product functions and required intelligence in the client wherever technically feasible. Do not assume a permanent connection or remote inference service.
- **Rationale:** Local execution supports privacy, responsiveness, offline continuity, and controlled operating cost.
- **Consequence:** Connected execution requires compatible Card policy, product policy, consent, connectivity, and authorization. Missing local intelligence produces an alternative or **Not assessed**, never silent upload or fabricated feedback.
- **Source:** [Platform specification, local-intelligence contract](../spec/platform_spec.md#7-local-intelligence-contract)

## ADR-011 — Independent localization preferences

- **Status:** Accepted; fixed product decision
- **Decision:** Resolve canonical Telugu, instruction language, interface locale, transliteration, and accessibility preferences independently.
- **Rationale:** A learner may need combinations that do not match the device locale, and changing presentation preferences must not change educational identity or progress.
- **Consequence:** English is the declared instruction-language default when no selection exists; any fallback must be disclosed. Locale changes preserve Card, Submission, Evaluation, Accomplishment, and progress identity.
- **Source:** [Platform specification, internationalization](../spec/platform_spec.md#internationalization-multilingual-presentation-and-preferences)

## ADR-012 — Ability-based authorization

- **Status:** Accepted; fixed product decision
- **Decision:** Authorize explicit abilities over resources and constraints rather than granting permissions through role or persona names.
- **Rationale:** Narrow abilities are reviewable and can be evaluated consistently in local and connected contexts.
- **Consequence:** A declared ability permits a request but does not guarantee runtime availability; device capability, permission, consent, connectivity, authorization, and a compatible bound handle must also be present.
- **Source:** [Platform specification, Card technical abilities](../spec/platform_spec.md#card-technical-abilities)

## ADR-013 — Separate authored assets from learner evidence

- **Status:** Accepted
- **Decision:** Treat application assets, course content, local model resources, learner records, raw learner evidence, and exports as separate data classes.
- **Rationale:** They have different integrity, privacy, authorization, consent, retention, deletion, and distribution requirements.
- **Consequence:** Learner evidence never resolves through a course asset reference. Raw evidence is retained only when purpose, consent, authorization, and retention rules permit it.
- **Source:** [App skeleton, data-class separation](APP_SKELETON_TECH_DESIGN.md#data-class-separation)

## ADR-014 — Application-owned executable behavior

- **Status:** Proposed
- **Decision:** Course packages may supply reviewed semantic HTML, manifests, styles within an allowed policy, and media, but not executable scripts, inline event handlers, arbitrary remote addresses, or unrestricted styles.
- **Rationale:** Separating reviewed content from executable authority reduces the package security surface and keeps behavior versioned with the application runtime.
- **Consequence:** Application-owned JavaScript activates declared Card actions after package validation. The package format needs explicit element, attribute, address, media, and style policies.
- **Source:** [App skeleton, semantic HTML Card contract](APP_SKELETON_TECH_DESIGN.md#semantic-html-card-contract)

## ADR-015 — Backend language remains deferred

- **Status:** Deferred
- **Decision:** Do not select Kotlin with Ktor, TypeScript on Node.js, Go, or another backend language before a server requirement exists.
- **Rationale:** A language decision without hosting, operational ownership, or a validated connected capability would be speculative.
- **Consequence:** Stable network and domain contracts must remain independent of the eventual backend implementation language.
- **Source:** [App skeleton, backend language](APP_SKELETON_TECH_DESIGN.md#backend-language-is-not-yet-selected)

## ADR-016 — Modular monolith for the first connected platform

- **Status:** Proposed; applies only when connected services are introduced
- **Decision:** Begin the connected platform as a modular monolith rather than microservices.
- **Rationale:** Initial connected needs—identity validation, ability evaluation, catalogue and package delivery, and explicit exports—do not justify independently operated services.
- **Consequence:** Keep module boundaries clear, but defer deployment separation until scale, ownership, reliability, or security evidence requires it.
- **Source:** [App skeleton, minimal connected platform](APP_SKELETON_TECH_DESIGN.md#10-minimal-connected-platform)

## ADR-017 — Commerce remains outside the learning platform

- **Status:** Accepted; fixed product decision
- **Decision:** Telugu Tutor does not implement offers, checkout, payment processing, subscription billing, refunds, tax handling, or transaction reconciliation. A separate commerce application or service may translate a commercial outcome into an explicit, resource-scoped and optionally time-bounded ability grant, change, or revocation.
- **Rationale:** Learning behavior and authorization must not depend on a payment provider or assume that purchase is the only source of access. Complimentary, assigned, sponsored, purchased, subscribed, and restored access use the same authorization contract.
- **Consequence:** Cards never receive commerce or transaction state. A refund or expiry removes only abilities derived from that source and preserves unrelated abilities, progress, Accomplishments, and permitted Submission history.
- **Source:** [Platform specification, fixed decisions](../spec/platform_spec.md#2-fixed-platform-decisions)

## ADR-018 — Subject-neutral platform with build-time specializations

- **Status:** Accepted
- **Decision:** Name the repository and shared platform TutorBrains and keep them subject-neutral. A declarative product manifest selects the subjects, instruction languages, trusted subject, script, and target-language specializations, content packages, compatible models, and branding compiled or packaged into a focused or multi-subject application. Instruction-language support remains a data overlay unless a measured script, input, rendering, accessibility, or intelligence requirement needs trusted executable specialization code. Downloaded course packages remain reviewed, signed, data-only artifacts and cannot introduce executable code.
- **Rationale:** Telugu Tutor must remain the first focused product without embedding Telugu, language-learning, or any future subject into the shared application shell. Build-time selection preserves stable Card and service-handle contracts while allowing subject-, script-, and language-specific behavior where generic browser or platform facilities are insufficient.
- **Consequence:** Telugu Tutor becomes a product assembly within TutorBrains. Executable specializations use declared extension points, compatibility metadata, permissions, tests, and conflict detection; they cannot override Card meaning, authorization, evidence policy, or another specialization silently. Core platform, subject, script, and target-language resolution is deterministic. Canonical learning content and instruction-language overlays remain separately versioned data. Repository and content migration occurs through reviewable changes without changing stable Card, unit, capability, or existing ADR identifiers merely because paths change.
- **Source:** [Project structure, build-time specialization rationale](project_structure.md#8-build-time-specialization-rationale)

## ADR-019 — Instruction-language localization without JavaScript

- **Status:** Accepted
- **Decision:** Implement learner-facing instruction-language internationalization and localization through localized semantic HTML, conventional locale and instruction-language addresses, and Cascading Style Sheets (CSS). CSS may apply language- and direction-dependent fonts, shaping support, spacing, line breaking, layout, visibility, and responsive presentation. Localized words, labels, alternatives, fallback disclosures, and accessibility text remain real HTML content and must not be generated through CSS pseudo-elements. JavaScript must not select an instruction language, load a localization dictionary, inject or replace localized text, construct localized asset addresses, switch localized document fragments, or decide an instruction-language fallback.
- **Rationale:** Complete localized HTML remains readable, linkable, cacheable, testable, reviewable, and available to assistive technology before executable code runs. It also makes the actual and fallback languages inspectable through `lang`, `dir`, `hreflang`, semantic elements, and stable addresses. CSS is appropriate for presentation differences but not as a hidden content store.
- **Consequence:** Each supported combination is resolved before delivery through a static build, conventional localized asset address, or server-side document selection. Explicit HTML links or ordinary form submission change instruction language by navigating to another complete localized document. The selected document declares its actual root language, and embedded content in another language declares its own `lang` and, where needed, `dir`. Missing localization produces a visible and accessible HTML fallback disclosure. Dynamic or service-produced instruction text must arrive already localized with explicit language metadata; the frontend displays it as content and does not translate or localize it. JavaScript may activate unrelated learner interactions under other ADRs, but it cannot participate in instruction-language resolution or localization. Subject, script, or language specializations may improve rendering, input, or intelligence behavior but cannot override this boundary.
- **Exception governance:** Any proposed exception or discovered violation requires its own numbered ADR. That ADR must identify the exact scope, evidence that localized HTML and CSS are insufficient, accessibility and privacy effects, offline and caching effects, security implications, fallback behavior, tests, owner, and removal or review trigger. The exception ADR must be accepted before the violating implementation is merged or released. An implementation without an accepted exception ADR is a defect and blocks release; an ADR must not be added afterward merely to legitimize an avoidable violation.
- **Relationship:** This decision narrows ADR-006, ADR-014, and ADR-018 for instruction-language behavior. Their allowance for application-owned JavaScript or trusted executable specializations does not permit JavaScript-driven localization.
- **Source:** [Platform specification, internationalization](../spec/platform_spec.md#internationalization-multilingual-presentation-and-preferences)

## Open evidence and review triggers

- Can an installed PWA provide an accepted first-class experience on Android, iOS, Windows, and macOS?
- Can browser storage provide sufficient durability for permitted learner evidence and model packages?
- Can useful local Telugu speech processing meet quality and resource gates through browser facilities?
- How long must restricted Chapter 01 content remain usable offline before reauthorization?
- Which account recovery and credential-protection behavior is required for the first slice?
- When should automatic pronunciation assessment enter scope?
- Does any required media, input, accessibility, augmented-reality, or virtual-reality behavior require a native renderer or plug-in?

## Considered but not shortlisted

Valdi, .NET Multi-platform App UI, Flutter, Compose Multiplatform, React Native, Apache Cordova, Wails, Neutralinojs, four custom WebView shells, and a browser-plus-companion arrangement are not currently shortlisted. The reasons and reconsideration conditions are maintained in the [platform options FAQ](PLATFORM_OPTIONS_FAQ.md). “Not shortlisted” is not a permanent rejection.
