# Proposed Project Structure

**Status:** Discussion draft for review  
**Scope:** Repository organization for subject-neutral learner applications, build-time subject and language specializations, a modular backend, native plug-ins, machine-learning work, course content, ontology, delivery operations, and durable project memory  
**Related:** [App skeleton technical design](APP_SKELETON_TECH_DESIGN.md), [Platform specification](../spec/platform_spec.md), and [Architecture Decision Record log](ARCHITECTURE_DECISION_LOG.md)

## 1. Purpose

This document proposes a repository structure that can begin small without making later separation unnecessarily difficult. It supports:

- a semantic Hypertext Markup Language (HTML), Cascading Style Sheets (CSS), and standard JavaScript learner application;
- an optional Tauri host with Rust and narrow Android or iOS native plug-ins;
- a mostly Python backend that begins as a modular monolith;
- selected Rust or Java Spring services where their benefits justify a separate runtime;
- independently selectable mathematics, target-language, and script specializations compiled into a frontend build;
- separate canonical subject content, instruction-language overlays, interface localization, and notation preferences;
- independent model training, evaluation, packaging, server deployment, and on-device deployment;
- component-owned development operations and Data Operations (DataOps) where the component is independently built or deployed;
- shared cloud, identity, access, observability, and pipeline foundations;
- versioned course content and an explicit learning ontology; and
- durable project memory kept separately from Architecture Decision Records (ADRs).

The structure is a target organization, not a requirement to create every directory before it is needed. Empty speculative directories should not be created merely to match the diagram.

## 2. Organizing principles

1. **Organize around deployable applications and capability boundaries.** A visual widget or utility package owns tests and quality checks, but an application, service, model package, or infrastructure stack owns deployment.
2. **Start with a modular monolith.** Compatible Python service modules may be composed into one `platform-api` process while retaining explicit contracts and owned data boundaries.
3. **Treat polyglot components honestly.** A Rust or Java service cannot run inside the Python process. It may be released with the same system, but it remains a separate process with an explicit contract.
4. **Keep Cards independent of deployment.** Cards use stable service handles and learning-unit references. They do not know whether an implementation is local, in-process, native, or remote.
5. **Keep native code narrow.** Kotlin, Java, and Swift plug-ins provide device capabilities; they do not duplicate lesson, Card, or educational-domain logic.
6. **Separate source from large or sensitive artifacts.** Production datasets, learner evidence, model binaries, credentials, and private keys do not belong in Git.
7. **Keep ontology separate from presentation.** The ontology defines concepts and relationships. Units hold canonical learning content, while Cards hold presentation and interaction properties.
8. **Distinguish memory from decisions.** Memory summarizes current context and working knowledge; ADRs record consequential decisions, alternatives, status, and consequences.
9. **Compile trusted specializations into applications.** Subject, script, and target-language modules may extend rendering, input, accessibility, and intelligence behavior, but course packages remain data-only and cannot introduce executable code.
10. **Keep instructional language data-first.** An instruction-language overlay normally supplies localized explanations, terminology, examples, and accessibility text. Executable specialization is added only for a measured script, input, rendering, or model requirement.

## 3. Proposed repository tree

```text
TutorBrains/
├── AGENTS.md
├── README.md
├── apps/
│   ├── learner-web/
│   ├── learner-tauri/
│   └── platform-api/
├── products/
│   ├── telugu-tutor/
│   ├── mathematics-tutor/
│   └── multi-subject/
├── services/
│   ├── identity-access/
│   ├── content-catalogue/
│   ├── learner-records/
│   ├── evidence-management/
│   ├── package-distribution/
│   └── intelligence-gateway/
├── packages/
│   ├── web/
│   ├── python/
│   ├── rust/
│   ├── native/
│   └── generated-clients/
├── contracts/
│   ├── openapi/
│   ├── events/
│   ├── schemas/
│   └── compatibility-tests/
├── specializations/
│   ├── subjects/
│   │   ├── language-learning/
│   │   └── mathematics/
│   ├── scripts/
│   │   ├── telugu/
│   │   ├── han/
│   │   └── devanagari/
│   └── languages/
│       ├── te/
│       └── zh/
├── native-plugins/
│   ├── audio-capture/
│   ├── camera-and-image-input/
│   ├── direct-writing-input/
│   ├── secure-storage/
│   ├── local-model-runtime/
│   └── file-export/
├── models/
│   ├── shared/
│   ├── language-learning/
│   ├── mathematics/
│   ├── runtimes/
│   └── registry/
├── data/
│   ├── contracts/
│   ├── quality-rules/
│   ├── shared-pipelines/
│   ├── governance/
│   └── synthetic-samples/
├── content/
│   ├── ontology/
│   │   ├── core/
│   │   ├── language-learning/
│   │   └── mathematics/
│   ├── subjects/
│   │   ├── languages/
│   │   │   ├── te/
│   │   │   │   ├── units/
│   │   │   │   ├── cards/
│   │   │   │   ├── courses/
│   │   │   │   ├── instruction/
│   │   │   │   │   ├── en/
│   │   │   │   │   └── hi/
│   │   │   │   └── assets/
│   │   │   └── zh/
│   │   └── mathematics/
│   │       ├── units/
│   │       ├── cards/
│   │       ├── courses/
│   │       ├── instruction/
│   │       └── assets/
│   ├── shell-localization/
│   ├── shared-assets/
│   └── package-manifests/
├── platform/
│   ├── cloud/
│   │   ├── bootstrap/
│   │   ├── modules/
│   │   └── environments/
│   ├── deployment/
│   ├── observability/
│   ├── identity-and-access/
│   ├── secret-references/
│   └── pipeline-templates/
├── automation/
├── tests/
│   ├── end-to-end/
│   ├── contract/
│   └── cross-platform-fixtures/
├── tools/
├── memory/
│   ├── README.md
│   ├── PROJECT_MEMORY.md
│   ├── architecture.md
│   ├── conventions.md
│   ├── components/
│   ├── investigations/
│   ├── handoffs/
│   └── archive/
└── doc/
    ├── adr/
    ├── design/
    └── spec/
```

## 4. Top-level folder rationale

| Folder            | Contains                                                                                                   | Rationale                                                                                                    | Must not contain                                                                          |
| ----------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `apps/`           | User-facing applications and application composition roots                                                 | Makes final build and deployment ownership explicit                                                          | Reusable domain implementations that should be independently testable                     |
| `products/`       | Build manifests selecting subjects, instruction languages, specializations, content packages, models, and branding | Produces focused or multi-subject applications without forking the shared application shell              | Subject implementation code, secrets, or copied course content                            |
| `services/`       | Backend capability modules and independently runnable services                                             | Preserves service boundaries while allowing compatible Python modules to run together                        | Direct dependencies on frontend presentation or another service's private database tables |
| `packages/`       | Reusable language- or platform-specific libraries                                                          | Avoids copying contracts, adapters, and utilities between applications and services                          | Independent production deployments or unbounded general-purpose shared code               |
| `contracts/`      | Language-neutral application programming interface, event, and data-shape contracts                        | Allows Python, Rust, Java, JavaScript, Kotlin, and Swift components to agree without sharing implementations | Provider-specific implementation details or secrets                                       |
| `specializations/` | Trusted build-time subject, script, and target-language extension modules                                 | Allows required rendering, input, accessibility, and model behavior to be selected without changing core Cards | Runtime-downloaded executable code or canonical course content                          |
| `native-plugins/` | Capability-oriented Tauri and mobile plug-ins                                                              | Gives Android and iOS native work an explicit, independently testable home                                   | Course semantics, Card progression, or duplicated business policy                         |
| `models/`         | Model training definitions, evaluation, export, runtime integration, and version manifests                 | Keeps model lifecycle work separate from application and course content                                      | Production datasets, unreviewed learner evidence, or large model binaries in Git          |
| `data/`           | Shared data contracts, governance, quality rules, and reusable pipeline foundations                        | Provides common DataOps rules without taking ownership away from a component                                 | Production data, credentials, or component-specific migrations                            |
| `content/`        | Subject ontologies, canonical learning units, Cards, course collections, instruction overlays, assets, and package manifests | Keeps reviewed educational meaning and content versioned independently of executable specialization code | Application-owned scripts, learner state, or raw learner evidence                         |
| `platform/`       | Shared cloud, deployment, identity, access, observability, secret references, and pipeline templates       | Centralizes common operational foundations and reduces inconsistent security setup                           | Actual credentials, private keys, or service-owned business logic                         |
| `automation/`     | Repository-level pipeline dispatch and change detection                                                    | Selects the relevant component pipeline without centralizing every component's build logic                   | Component-specific deployment policy that belongs with that component                     |
| `tests/`          | System-level tests crossing application or service boundaries                                              | Provides a home for tests that no single component can own                                                   | Unit tests that should remain beside their implementation                                 |
| `tools/`          | Developer utilities, generators, validators, and repository maintenance tools                              | Separates product code from development support code                                                         | Production services disguised as scripts                                                  |
| `memory/`         | Durable project context, conventions, findings, and handoffs                                               | Gives agents and people one reviewable source for current working knowledge                                  | Secrets, personal data, raw conversations, or binding architecture decisions              |
| `doc/`            | Product specifications, implementation designs, and ADRs                                                   | Separates requirements, proposals, and accepted decisions                                                    | Generated operational state or transient agent notes                                      |

## 5. Application folder rationale

| Folder | Responsibility | Rationale | Deployment owner |
|---|---|---|---|
| `apps/learner-web/` | Progressive Web App (PWA) shell using semantic HTML, CSS, and standard JavaScript | Provides the smallest first learner slice and the shared presentation implementation | Learner Web application pipeline |
| `apps/learner-tauri/` | Optional installed host that assembles the shared web application, Rust core, and selected native plug-ins | Adds native packaging and protected platform capabilities only when measured requirements justify it | Tauri application pipeline, including signing and platform packaging |
| `apps/platform-api/` | Python composition root for selected backend service modules | Allows one deployable modular monolith without erasing internal capability boundaries | Platform application programming interface pipeline |

The role, internal structure, and deployment ownership of `apps/platform-api/` remain **under review**. Its row above records the current proposal and must not be treated as an accepted implementation design.

An application folder may contain `src/`, `tests/`, `config/`, `build-tools/`, and `ops/` when those directories are needed. In accordance with ADR-021, `build-tools/` owns application-specific build implementation, including generation, transformation, copying, and packaging preparation. `config/` owns version-controlled, non-secret application defaults and configuration schemas. `ops/` owns container definitions, server or process-manager configuration, health checks, deployment manifests, operational runbooks, and component pipeline entry points that invoke the build. Common operational policy and reusable pipeline steps remain under `platform/`.

### Product build manifests

| Folder | Selects | Rationale |
|---|---|---|
| `products/telugu-tutor/` | Telugu language-learning content, supported instruction languages, required script and language specializations, compatible models, and product branding | Preserves Telugu Tutor as the first focused product while the repository and platform become subject-neutral |
| `products/mathematics-tutor/` | Mathematics content, notation renderer, mathematical input, instruction-language overlays, and compatible evaluation models | Produces a mathematics-focused application without adding mathematics logic to the generic shell |
| `products/multi-subject/` | An approved collection of subjects and every specialization required by them | Allows one TutorBrains application to ship several subjects when product evidence supports that experience |

Each product contains a declarative `product.yaml` or equivalent build manifest. It identifies exact specialization and content-package versions. The build fails when a required specialization is absent, incompatible, ambiguous, or conflicts with another selected specialization.

## 6. Backend service rationale

| Folder | Initial responsibility | Why it is separate |
|---|---|---|
| `services/identity-access/` | Identity integration, token validation, and ability evaluation | Security policy and identity-provider integration have different change and review risks from course behavior |
| `services/content-catalogue/` | Approved content metadata and accessible package discovery | Content discovery can evolve independently from package transport and learner records |
| `services/learner-records/` | Student Card map, Submissions, Evaluations, and Accomplishments | Durable learning history needs explicit ownership and must remain distinct from reusable Card definitions |
| `services/evidence-management/` | Consent, retention, protection, and deletion of permitted raw evidence | Raw audio, images, or strokes have stricter privacy rules than nonsensitive learning records |
| `services/package-distribution/` | Versioned course, asset, and model package publication and delivery | Package integrity, rollout, rollback, and caching form a distinct operational capability |
| `services/intelligence-gateway/` | Policy-controlled access to explicitly allowed connected intelligence | Prevents Cards and clients from depending directly on model providers or remote endpoints |

Each backend capability should use this internal pattern when the directories are needed:

```text
services/learner-records/
├── component.yaml
├── src/
├── tests/
├── contracts/
├── config/
├── migrations/
├── data-pipelines/
└── ops/
    ├── Containerfile
    ├── runtime/
    ├── observability/
    ├── deployment/
    ├── runbooks/
    └── pipeline.yaml
```

| Internal folder | Rationale |
|---|---|
| `component.yaml` | Declares owner, language, dependencies, build entry point, deployment mode, and data classification in a machine-readable form |
| `src/` | Keeps the capability implementation local to its owner |
| `tests/` | Allows the component to prove its behavior without requiring the full system |
| `contracts/` | Holds the component's source contract before approved shared or generated forms are published to `contracts/` |
| `config/` | Declares non-secret component defaults, supported initialization parameters, and configuration validation without embedding environment-specific deployment values |
| `migrations/` | Makes the component responsible for its owned schema even when several modules share one physical database initially |
| `data-pipelines/` | Gives component-specific ingestion, transformation, export, or quality work an explicit DataOps owner |
| `ops/` | Keeps container packaging, runtime, deployment, runbooks, and component pipeline configuration beside the deployable unit |

Within `ops/`, `runtime/` contains server, process-manager, worker or thread settings, startup commands, and deployment-time initialization values. `observability/` contains component-specific telemetry wiring, dashboards, and alerts while using the logging, metrics, tracing, privacy, and redaction policy from `platform/observability/`. `deployment/` contains manifests and component-specific rollout configuration. Secret values do not belong in any of these directories.

Python modules composed into `apps/platform-api/` must communicate through explicit Python interfaces and owned repositories rather than reaching into each other's internal modules or tables. A Rust or Java Spring component remains an out-of-process service even if it is included in the same release and deployed beside the Python application.

## 7. Shared package and contract rationale

| Folder | Contains | Rationale |
|---|---|---|
| `packages/web/` | Card runtime, platform-service clients, localization helpers, and web adapters | Reuses learner-facing behavior without creating a frontend framework dependency |
| `packages/python/` | Focused Python contracts, observability helpers, and test utilities | Supports consistent backend behavior without creating one tightly coupled shared library |
| `packages/rust/` | Reusable Rust capability implementations and safe host adapters | Shares native logic across Tauri or Rust services where the contract is genuinely common |
| `packages/native/` | Reusable Android libraries and Swift packages not inherently tied to Tauri | Keeps valuable native implementation reusable if the application host changes |
| `packages/generated-clients/` | Generated clients for approved cross-process contracts | Prevents hand-maintained protocol drift across languages |
| `contracts/openapi/` | OpenAPI descriptions for request-response services | Provides language-neutral network contracts and generated-client inputs |
| `contracts/events/` | Event names, envelopes, payload schemas, and compatibility policy | Makes asynchronous integration versioned and testable |
| `contracts/schemas/` | Shared serialized data structures and manifest validation | Separates wire or file shape from any one language implementation |
| `contracts/compatibility-tests/` | Fixtures proving old and new producers and consumers remain compatible | Detects accidental breaking changes before deployment |

Sharing a physical repository does not justify sharing arbitrary code. A package should have a clear owner, supported consumers, compatibility policy, and removal path.

## 8. Build-time specialization rationale

A specialization is trusted application code selected before compilation or packaging. It extends a narrow platform contract; it does not replace the Card runtime or supply course progression. The initial specialization layers are:

| Folder | Responsibility | Example |
|---|---|---|
| `specializations/subjects/language-learning/` | Shared language-learning rendering, recording, comparison, transliteration, and assessment adapters | A pronunciation activity requests speech capture and a pronunciation-evaluation handle |
| `specializations/subjects/mathematics/` | Semantic mathematical notation rendering, expression input, step presentation, and mathematics-specific assessment adapters | A Card renders Mathematical Markup Language (MathML) and accepts an equivalent symbolic expression |
| `specializations/scripts/telugu/` | Telugu shaping fixtures, font policy, input behavior, segmentation, and script-specific accessibility checks | Tests combining marks, selection, line breaking, and spoken alternatives |
| `specializations/scripts/han/` | Han-script font fallback, line-breaking, annotation, input-method, and accessibility behavior shared where valid | A Chinese course validates character rendering, selection, and input without changing the generic Card contract |
| `specializations/scripts/devanagari/` | Devanagari shaping, font, input, segmentation, and accessibility behavior | Hindi instructional content and a future Devanagari target language reuse tested script support |
| `specializations/languages/te/` | Telugu-specific linguistic preprocessing, normalization, speech configuration, and compatible model profiles | A transcription request supplies Telugu language context behind the stable transcription handle |
| `specializations/languages/zh/` | Chinese-language segmentation, pronunciation representation, normalization, speech configuration, and compatible model profiles | A language Card requests a Chinese-compatible tokenizer or speech evaluator without naming its provider |

Each specialization uses the following shape as needed:

```text
specializations/languages/zh/
├── specialization.yaml
├── frontend/
├── intelligence/
├── native/
├── contracts/
├── tests/
└── ops/
```

| Internal folder | Rationale |
|---|---|
| `specialization.yaml` | Declares identity, version, kind, supported subjects, languages or scripts, required platform capabilities, compatible core versions, entry points, permissions, dependencies, and conflicts |
| `frontend/` | Contains build-time JavaScript, CSS, fonts, workers, renderers, or input adapters exposed only through approved platform contracts |
| `intelligence/` | Contains preprocessing, postprocessing, prompt or rubric profiles, model-adapter configuration, compatibility declarations, and evaluation fixtures |
| `native/` | Contains optional wrappers around approved native capabilities when browser behavior is insufficient |
| `contracts/` | Defines the specialization's extension points and the values it may exchange with the shared runtime |
| `tests/` | Proves rendering, input, accessibility, model behavior, fallback, and cross-platform compatibility |
| `ops/` | Owns build, dependency, security, and publication checks for the specialization artifact |

Resolution order is core platform, subject specialization, script specialization, and then target-language specialization. A later layer may fill a declared extension point but must not silently override Card meaning, authorization, evidence policy, or another layer's behavior. Conflicting providers require an explicit product choice rather than order-dependent selection.

Instruction-language content remains a data overlay by default. For example, Hindi explanations for mathematics do not require a Hindi executable module merely because the text is Hindi. A script specialization is selected only when the build needs tested font, shaping, input, segmentation, accessibility, or intelligence behavior beyond the generic platform.

Course packages remain reviewed, signed, data-only artifacts. They may declare required specialization identifiers and compatible version ranges, but they cannot ship JavaScript, WebAssembly, native binaries, commands, or model code. Consequently, a subject downloaded after installation can run only when its required executable specializations were already compiled into that application build.

## 9. Native plug-in rationale

| Folder | Capability | Typical native implementation |
|---|---|---|
| `native-plugins/audio-capture/` | Permission-aware recording and protected audio handles | Kotlin or Java on Android; Swift on iOS; Rust facade for Tauri |
| `native-plugins/camera-and-image-input/` | Camera capture, image selection, preview, and safe local handles | Android camera and picker adapters; iOS camera and photo-picker adapters |
| `native-plugins/direct-writing-input/` | Touch, stylus, and pointer stroke capture when browser support is insufficient | Platform-native input adapters with a common serialized stroke contract |
| `native-plugins/secure-storage/` | Small secrets and key material in operating-system protected storage | Android Keystore and Apple Keychain adapters behind one capability contract |
| `native-plugins/local-model-runtime/` | Local model loading, execution, streaming, cancellation, and provenance | Platform-compatible native runtimes behind capability-oriented handles |
| `native-plugins/file-export/` | Learner-authorized export through platform file or share facilities | Android and iOS document or share adapters |

A Tauri plug-in may contain `guest-js/`, Rust `src/`, `android/`, `ios/`, `permissions/`, `tests/`, and `ops/`. Reusable native logic should live in a standalone Android library or Swift package, with thin Tauri-specific bridge code around it. The plug-in owns compilation and contract tests; `apps/learner-tauri/` owns final bundling, signing, and release.

## 10. Model and DataOps rationale

| Folder | Contains | Rationale |
|---|---|---|
| `models/shared/` | Subject-neutral model tooling, evaluation harnesses, packaging rules, and common runtime contracts | Reuses safe lifecycle infrastructure without assuming that one model works for every subject or language |
| `models/language-learning/pronunciation/` | Training, evaluation, export, and manifests for pronunciation-related models | Keeps the task's evidence, language coverage, reliability thresholds, and release history together |
| `models/language-learning/speech-transcription/` | Speech transcription training and evaluation definitions | Separates transcription behavior from pronunciation evaluation and records supported languages explicitly |
| `models/language-learning/handwriting/` | Script image or stroke model training and evaluation definitions | Allows distinct script coverage, data governance, and platform constraints |
| `models/mathematics/expression-recognition/` | Printed or handwritten mathematical-expression recognition and semantic conversion | Keeps mathematical recognition separate from natural-language handwriting models |
| `models/mathematics/solution-evaluation/` | Step, equivalence, rubric, and supported-correction evaluation definitions | Allows mathematics-specific evaluation without introducing a Math Card subtype |
| `models/runtimes/browser/` | WebAssembly, Web Graphics Processing Unit (WebGPU), worker, and browser packaging integration | Measures and owns browser-specific model limits |
| `models/runtimes/tauri/` | Rust and native installed-client runtime integration | Keeps protected local execution outside Card code |
| `models/runtimes/server/` | Server inference packaging and adapters | Allows an explicitly authorized connected implementation without making it the assumed path |
| `models/registry/` | Version manifests, hashes, provenance, compatibility, and approval state | Records what may be packaged or deployed without committing model binaries |
| `data/contracts/` | Dataset field definitions, classifications, allowed purposes, and retention metadata | Makes training and operational pipelines agree on meaning and governance |
| `data/quality-rules/` | Shared validity, distribution, duplication, leakage, and safety checks | Prevents each model task from redefining basic quality policy |
| `data/shared-pipelines/` | Reusable pipeline components and templates | Reduces repeated infrastructure while leaving each task responsible for its pipeline |
| `data/governance/` | Consent, provenance, licensing, access, retention, and deletion rules | Keeps data use reviewable independently of implementation |
| `data/synthetic-samples/` | Small non-personal fixtures suitable for tests and examples | Enables repeatable local tests without exposing learner data |

Large datasets and model binaries belong in controlled stores or registries. Git should contain manifests, code, evaluation definitions, small synthetic fixtures, and immutable artifact references such as versions and cryptographic hashes.

An intelligence request includes task, subject, language or notation context, permitted inputs, reliability requirement, and allowed result vocabulary. A Card still calls a stable service handle; it does not select a base model, fine-tune, adapter, tokenizer, prompt, or provider. Product builds resolve compatible intelligence specializations and model artifacts, while the runtime records the selected implementation and version as Evaluation provenance.

Language- or subject-specific model changes may include deterministic normalization, tokenization, Large Language Model (LLM) prompt or rubric profiles, fine-tuning adapters, output constraints, and evaluation suites. Large adapter weights and model artifacts remain in the model registry; `specializations/*/intelligence/` contains their reviewed manifests and integration code. Local and connected implementations must pass the same behavioral contract before they satisfy the same handle.

## 11. Course content and ontology rationale

| Folder | Contains | Rationale |
|---|---|---|
| `content/ontology/core/` | Subject-neutral concepts such as learning unit, objective, prerequisite, Card reference, evidence, and assessment relationship | Gives every subject a small common semantic foundation without pretending all subjects have the same internal structure |
| `content/ontology/language-learning/` | Language, script, character, sound, word, grammar, sentence, register, and dialogue concepts and relations | Reuses language-learning semantics across Telugu and later target languages |
| `content/ontology/mathematics/` | Mathematical concept, notation, expression, problem, step, equivalence, justification, and proof concepts and relations | Represents mathematical meaning independently of localized explanation and visual notation |
| `content/subjects/languages/te/` | Canonical Telugu units, Cards, courses, assets, and instruction-language overlays | Preserves Telugu as a subject package rather than embedding it in the platform |
| `content/subjects/languages/zh/` | Canonical Chinese units, Cards, courses, assets, and instruction-language overlays | Allows Chinese content to select Han-script and Chinese-language specializations explicitly |
| `content/subjects/mathematics/` | Canonical semantic mathematics units, Cards, courses, assets, notation preferences, and instruction-language overlays | Keeps mathematical meaning stable while explanations and display conventions vary |
| `content/shell-localization/` | Subject-neutral application labels, platform messages, accessibility text, and fallback metadata | Separates interface locale from subject and instructional content |
| `content/shared-assets/` | Reviewed subject-neutral media, fonts, licenses, provenance, and accessibility metadata | Avoids duplicating genuinely shared assets while retaining explicit ownership and rights |
| `content/package-manifests/` | Immutable versions, approved references, integrity hashes, and compatibility requirements | Supports verified installation, rollback, offline resolution, and reproducible releases |

Each subject package may contain `units/`, `cards/`, `courses/`, `instruction/`, and `assets/`. For example, `content/subjects/languages/te/instruction/en/` and `instruction/hi/` localize Telugu explanations without changing canonical Telugu or Card identity. Mathematics uses the same separation: semantic expressions and objectives remain canonical, while terminology, explanations, narration, and notation preferences may vary by instruction language or locale.

The ontology describes meaning and relationships such as `composed-of`, `pronounced-as`, `variant-of`, `equivalent-to`, `used-in`, `example-of`, `contrasts-with`, `prerequisite-of`, `teaches`, and `assesses`. Learning-unit instances and Card presentation remain in their subject package. An ontology relationship must not introduce child Cards, Card inheritance, or subject-specific Card classes.

Readable YAML or JavaScript Object Notation (JSON) plus validation tests is sufficient initially. JavaScript Object Notation for Linked Data (JSON-LD), Resource Description Framework (RDF), or Web Ontology Language (OWL) should be adopted only if graph interchange or automated reasoning becomes a demonstrated requirement.

## 12. Platform and credential rationale

| Folder | Contains | Rationale |
|---|---|---|
| `platform/cloud/bootstrap/` | Remote state, account or project initialization, and provisioning-identity setup | Separates the prerequisites for managing infrastructure from the infrastructure managed afterward |
| `platform/cloud/modules/` | Reusable network, compute, storage, registry, and policy modules | Produces consistent cloud resources across environments |
| `platform/cloud/environments/` | Environment composition using non-secret configuration | Makes development, test, staging, and production differences explicit |
| `platform/deployment/` | Shared release topology and deployment coordination | Supports deploying the modular monolith and any necessary companion processes together |
| `platform/observability/` | Logging, metrics, tracing, alerting, and privacy-safe diagnostic policy | Gives components common operational signals and redaction rules |
| `platform/identity-and-access/` | Workload identities, access policy, and least-privilege role definitions | Separates infrastructure authorization from learner ability authorization |
| `platform/secret-references/` | Secret names, expected owners, consumers, rotation metadata, and retrieval policy | Allows components to refer to credentials without storing their values |
| `platform/pipeline-templates/` | Reusable build, test, security, packaging, and release steps | Gives component owners safe defaults without one central pipeline owning all behavior |

Actual credentials and private keys must remain in an approved secret manager, protected Continuous Integration (CI) environment, operating-system secure store, or similarly controlled facility. Repository files may contain examples, references, and access policy, but never live secret values.

## 13. Memory, ADR, and documentation rationale

| Folder or file | Contains | Rationale |
|---|---|---|
| `AGENTS.md` | Repository instructions that every coding or documentation agent must follow | Keeps mandatory working rules discoverable before an agent changes files |
| `memory/README.md` | Memory scope, allowed content, ownership, freshness, and archival rules | Prevents memory from becoming an unreviewed collection of transcripts or contradictory notes |
| `memory/PROJECT_MEMORY.md` | Concise current project context and pointers to authoritative sources | Replaces the root `memory.md` with an explicit durable location |
| `memory/architecture.md` | Current architectural boundaries summarized from specifications and accepted ADRs | Helps agents orient quickly without making the summary authoritative over its sources |
| `memory/conventions.md` | Naming, testing, review, and repository conventions | Preserves working agreements that are too detailed for `AGENTS.md` |
| `memory/components/` | Current context and known constraints for individual applications, services, models, or content areas | Makes component knowledge discoverable without organizing memory by transient agent identity |
| `memory/investigations/` | Dated findings, evidence, and unresolved questions | Keeps research distinct from accepted decisions |
| `memory/handoffs/` | Short-lived continuation notes for incomplete work | Supports agent or person handoff without polluting durable project context |
| `memory/archive/` | Superseded memory retained with date and provenance | Preserves history while preventing stale information from appearing current |
| `doc/adr/README.md` | ADR index, status definitions, numbering policy, and supersession links | Provides one authoritative entry point for architecture decisions |
| `doc/adr/ADR-NNN-title.md` | Context, decision, alternatives, consequences, status, and supersession for one decision | Makes consequential decisions independently reviewable and linkable |
| `doc/adr/ADR-template.md` | Required ADR fields and writing guidance | Keeps new decisions consistent |
| `doc/design/` | Candidate and accepted implementation designs | Explains how requirements may be implemented without silently becoming a product requirement |
| `doc/spec/` | Product requirements, platform-neutral contracts, capability catalogue, and unit specifications | Remains authoritative for what the product must do |

Memory may summarize an ADR or specification but must link to it and must not override it. Memory files must not contain credentials, learner data, raw private conversations, or undocumented binding decisions. Investigations should state their date, evidence, confidence, and unresolved questions.

The current `memory.md` can move to `memory/PROJECT_MEMORY.md`. The combined `doc/design/ARCHITECTURE_DECISION_LOG.md` can initially move without a content rewrite to `doc/adr/README.md`; individual ADRs can then be extracted when they are next revised. This keeps the migration reviewable and avoids competing decision sources.

## 14. Pipeline ownership

| Unit | Owns | Uses from the platform |
|---|---|---|
| Deployable application | Build, application tests, packaging, deployment, rollback, and release evidence | Shared pipeline steps, cloud targets, signing integration, observability, and secret references |
| Product build | Exact subject, instruction-language, specialization, content-package, model, and branding selection | Shared application shell, specialization registry, content registry, and compatibility validation |
| Backend service or module | Unit and contract tests, migrations, component DataOps, and independent deployment configuration when applicable | Shared database provisioning, workload identity, pipeline templates, and telemetry policy |
| Reusable package | Compilation, unit tests, compatibility checks, versioning, and publication when needed | Shared quality and dependency checks |
| Build-time specialization | Frontend, intelligence, native-wrapper, contract, compatibility, and security tests | Shared extension contracts, cross-platform fixtures, and artifact publication rules |
| Native plug-in | Android, iOS, Rust, permission, and contract tests | Shared mobile build environments, signing integration, and dependency policy |
| Model task | Training, evaluation, bias and safety checks, export, approval evidence, and model manifest | Shared data governance, compute, artifact registry, and pipeline templates |
| Subject content package | Content validation, ontology checks, instruction-language checks, media accessibility, declared specialization compatibility, integrity, and publication | Shared package registry and signing policy |
| Infrastructure stack | Planning, policy validation, controlled application, drift detection, and rollback | Shared identity and protected credentials |

Repository-level automation should detect changed paths and invoke the owning unit's pipeline. It should not duplicate the detailed build or deployment logic kept with that unit.

## 15. Adoption sequence

The structure should be introduced as real work requires it:

1. Keep the current specifications and design documents authoritative while this proposal is reviewed.
2. Record the subject-neutral TutorBrains platform and build-time specialization boundary in an ADR before renaming identifiers or moving content.
3. Establish `memory/` and `doc/adr/` through a reviewable documentation-only move.
4. Introduce `products/telugu-tutor/` as the first build manifest without changing existing stable Card, unit, capability, or ADR identifiers.
5. Create the core and language-learning ontology layers, then move Telugu-specific content under `content/subjects/languages/te/` through separately reviewable changes.
6. Create only the Telugu subject, Telugu script, and Telugu language specializations required by measured frontend or intelligence needs.
7. Create `apps/learner-web/` for the Chapter 01 implementation and add only the shared web packages and selected specializations it actually needs.
8. Create `apps/platform-api/` and the minimum Python service modules when the accepted identity and restricted-content boundary is implemented.
9. Add mathematics, Chinese, model, native plug-in, Tauri, or separately deployed service folders only after a validated product requirement selects them.

## 16. Questions for review

- Should `content/` be maintained in this repository or eventually versioned and released from a separately governed content repository?
- Which learning relationships belong in the initial ontology, and which should wait for curriculum validation?
- Which extension points may a specialization implement, and which core Card, authorization, evidence, and accessibility rules can never be overridden?
- Will the first TutorBrains application be a focused Telugu build or a multi-subject shell capable of installing additional data-only subject packages?
- Which script behaviors require executable specialization rather than fonts, semantic HTML, CSS, localization data, and conformance tests?
- How will product builds resolve and lock compatible frontend specialization, model adapter, content-package, and core-runtime versions?
- Should service modules share one physical database initially, and what schema-level enforcement will preserve ownership?
- Which component metadata must be mandatory in `component.yaml` before repository automation depends on it?
- What measured browser limitation would justify creating `apps/learner-tauri/` or a native plug-in?
- Which model task is the first justified local-intelligence experiment, and what evaluation threshold would permit learner-facing use?
