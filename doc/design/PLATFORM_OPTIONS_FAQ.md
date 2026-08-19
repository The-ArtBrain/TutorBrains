# Platform Scheme Frequently Asked Questions

**Status:** Discussion draft  
**Purpose:** Record why three schemes are shortlisted and why other evaluated options are not currently shortlisted  
**Parent design:** [App skeleton technical design](APP_SKELETON_TECH_DESIGN.md)

## What does "not shortlisted" mean?

It means the option currently conflicts with one or more declared product or architecture preferences, duplicates a shortlisted scheme with a weaker fit, or does not cover all required platforms. It is not a permanent rejection. An option can return when requirements change or new evidence resolves its gap.

## What are the shortlist criteria?

The current shortlist prioritizes:

- semantic Hypertext Markup Language (HTML) as the learner-facing Card representation;
- standard JavaScript without requiring a frontend component framework;
- Android, iOS, Windows, and macOS coverage, or a clearly stated feasibility question about that coverage;
- client-side operation, including local intelligence where required;
- optional rather than mandatory connected services;
- a small and reviewable dependency surface;
- ability-based authorization rather than roles;
- protected learner evidence, explicit consent, deletion, and export boundaries;
- equivalent localization, accessibility, media, and input behavior; and
- platform-specific code confined behind shared service handles.

The three shortlisted schemes are:

1. [Progressive Web App](PWA_PLATFORM_DESIGN.md);
2. [Tauri 2.0](TAURI_PLATFORM_DESIGN.md); and
3. [Capacitor mobile plus Electron desktop](CAPACITOR_ELECTRON_PLATFORM_DESIGN.md).

## What is the current decision for the first implementation slice?

Use a Progressive Web App (PWA) for the Chapter 01 localized read-and-speak learning slice. English remains the default instruction language, and Hindi is the second instruction language used to prove localization and fallback behavior. Keep Tauri as an escalation path for a demonstrated native requirement rather than making it an assumed foundation.

The first slice should use semantic HTML, standard JavaScript, packaged Telugu content, localized instructions, prerecorded reference audio, learner recording and playback, and local preferences or progress. It includes account creation and sign-in plus ability-based authorization for restricted content. A minimal connected platform therefore supplies identity integration, token validation, and authoritative ability or entitlement evaluation.

Synchronization, remote inference, content publication, learner-initiated account or submission exports, and automatic pronunciation assessment remain outside the first slice unless separately accepted. The Chapter 01 pilot-data export remains part of the product requirements document; it is research instrumentation rather than a learner account-export feature.

Commercial purchase flows also remain outside the Telugu Tutor learning platform permanently. A separate commerce application or service owns offers, payments, subscriptions, and refunds. Telugu Tutor receives only the resulting explicit, scoped, and optionally time-bounded ability changes; paid and non-paid access use the same authorization contract.

This is a decision about the first implementation slice, not yet a final decision that a PWA satisfies every required production platform. The PWA must still pass the platform evidence described in its [candidate design](PWA_PLATFORM_DESIGN.md), and selecting it as the production scheme would require reconciling the current platform specification as described below.

Tauri should be introduced only when evidence establishes at least one concrete need that the PWA cannot satisfy adequately, such as:

- a local Telugu speech or pronunciation model cannot meet the required performance, reliability, privacy, or offline behavior through browser facilities;
- model packages or permitted learner evidence cannot be stored with adequate durability under browser quota and eviction behavior;
- native secure storage, SQLite, controlled files, or package verification is required;
- application-store packaging is a confirmed product requirement that an installed PWA cannot meet adequately;
- a required device capability lacks a suitable browser API; or
- essential background work or operating-system integration cannot be delivered reliably by the PWA.

Tauri does not itself improve semantic HTML, localization, Card architecture, or teaching behavior. Its value is a controlled bridge to native code, storage, packaging, and operating-system services. Until one of those capabilities becomes necessary, its Rust code, native builds, plug-ins, permissions, signing, and cross-platform maintenance are additional cost without a demonstrated learner benefit.

References: [PWA overview](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps), [browser storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria), [Tauri features and plug-ins](https://v2.tauri.app/plugin/), [Tauri distribution](https://v2.tauri.app/distribute/)

## Why is Valdi not shortlisted?

Valdi uses TypeScript and familiar declarative TSX syntax, but it does not preserve standard HTML. Elements such as `view` and `label` compile into native platform views rather than a browser Document Object Model (DOM). Its primary documented native targets are iOS, Android, and macOS; Windows is not listed as a primary supported target.

Valdi is attractive when the priority is native view performance, gestures, animation, native bindings, and JavaScript/TypeScript authoring. It is a weaker fit when Cards must remain independently usable semantic HTML documents and Windows is required.

Valdi could be reconsidered if:

- Card semantics move into a platform-neutral data model rather than HTML;
- HTML becomes only one renderer;
- Windows is deferred or supported adequately; and
- the team accepts Valdi's framework vocabulary, build system, dependency surface, and current external beta status.

Embedding HTML Cards in Valdi's WebView element would create two presentation systems and would not by itself solve Windows support.

Reference: [Snap Valdi](https://github.com/Snapchat/Valdi)

## Why is .NET Multi-platform App UI HybridWebView not shortlisted?

.NET Multi-platform App UI (.NET MAUI) `HybridWebView` is a credible four-platform host for arbitrary HTML, Cascading Style Sheets (CSS), and JavaScript. It packages the web content locally and lets JavaScript call C#/.NET code.

It is not currently shortlisted because it introduces a substantial .NET, C#, MAUI, Extensible Application Markup Language (XAML), and Mac Catalyst commitment when the stated preference is standard HTML and JavaScript with a small dependency gap. It also uses the same class of differing system WebViews as other hybrid schemes.

It could be reconsidered if:

- one managed host across all four platforms is more important than minimizing the .NET dependency;
- C# is preferred for local services and model integration;
- Mac Catalyst is acceptable for macOS; and
- its camera, microphone, stylus, secure storage, evidence, and model spike outperforms the shortlisted schemes.

Reference: [.NET MAUI HybridWebView](https://learn.microsoft.com/en-us/dotnet/maui/user-interface/controls/hybridwebview?view=net-maui-10.0)

## Why is Flutter not shortlisted?

Flutter covers Android, iOS, Windows, and macOS and supplies a consistent declarative renderer with native interoperability. It remains a strong general cross-platform application option.

It is not shortlisted because Flutter Cards would be Dart widget trees, not standard semantic HTML. The product would need an HTML-to-Flutter renderer or a second HTML representation for Web and content review. That adds an impedance layer precisely where the current preference asks for semantic HTML to remain authoritative.

Flutter could be reconsidered if consistent cross-platform rendering and plug-in maturity become more important than literal HTML Cards.

Reference: [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms)

## Why is Kotlin and Compose Multiplatform not shortlisted?

Kotlin Multiplatform and Compose Multiplatform provide shared business logic and declarative user interfaces across Android, iOS, Windows, and macOS with strong native interoperability.

They are not shortlisted because Compose elements are not semantic HTML or a browser DOM. A separate Web/Card renderer would be required, and desktop delivery introduces the Java Virtual Machine (JVM) and its packaging considerations.

They could be reconsidered if native platform integration and a Kotlin codebase become higher priorities than standards-based HTML Cards.

Reference: [Compose Multiplatform platform stability](https://kotlinlang.org/docs/multiplatform/supported-platforms.html)

## Why is React Native not shortlisted?

React Native renders framework components into native views. The Windows and macOS targets use additional platform extensions rather than the core mobile implementation.

React Native is not shortlisted because React Native components are not standard semantic HTML, the desktop target surface is more fragmented, and a separate Web renderer would be required. React syntax familiarity does not make its native view tree a browser DOM.

React Native could be reconsidered if a native component ecosystem and React team experience outweigh the Card portability requirement.

References: [React Native](https://reactnative.dev/), [React Native for Windows](https://microsoft.github.io/react-native-windows/)

## Why is Capacitor alone not sufficient?

Capacitor is shortlisted as the mobile half of one scheme. It is well aligned with an existing semantic HTML and JavaScript application and provides Android and iOS plug-ins.

It is not a complete standalone scheme because its official focus is Android, iOS, and Progressive Web Apps. It does not provide the required Windows and macOS installed applications by itself. Pairing it with Electron supplies the desktop half.

Reference: [Capacitor documentation](https://capacitorjs.com/docs)

## Why is Electron alone not sufficient?

Electron is shortlisted as the desktop half of one scheme. It provides a controlled Chromium renderer, Node.js/native integration, packaging, and desktop operating-system services.

It is not a complete standalone scheme because it does not target Android or iOS. It also adds a bundled Chromium and Node.js runtime, which must be justified by desktop capability and consistency benefits.

Reference: [Electron documentation](https://www.electronjs.org/docs/latest/)

## Why is Apache Cordova not shortlisted?

Apache Cordova can package HTML and JavaScript for mobile and provides a long-standing plug-in model. Its documentation also includes browser and Electron-related platforms.

Capacitor is preferred for the current mobile half because it presents a more current web-first native runtime, integrates with existing web applications, and exposes a focused Swift/Java plug-in model. Choosing Cordova would still require a desktop strategy and a separate evaluation of current plug-in maintenance and platform parity.

Cordova could be reconsidered if a required mature Cordova plug-in has no adequate Capacitor or custom-native equivalent.

Reference: [Apache Cordova documentation](https://cordova.apache.org/docs/en/latest/)

## Why are Wails and Neutralinojs not shortlisted?

Wails and Neutralinojs both preserve HTML and JavaScript and offer lighter desktop alternatives to Electron.

- Wails combines web technologies with a Go application core on Windows, macOS, and Linux.
- Neutralinojs supplies a lightweight desktop/web host and native-operation bridge.

Neither currently covers the required Android and iOS installed applications. Adding a mobile host would create another split scheme. Electron remains in the current split shortlist because its bundled Chromium and mature desktop native/module ecosystem provide a clearer reason to accept that split.

References: [Wails](https://wails.io/docs/introduction/), [Neutralinojs](https://neutralino.js.org/docs/)

## Why not build four thin native WebView shells?

A custom shell could use Android WebView, iOS/macOS WKWebView, and Windows WebView2 while preserving the same HTML application.

This minimizes commitment to a cross-platform host framework but creates four maintained application projects, bridges, permission systems, packaging pipelines, lifecycle implementations, and local-model integrations. It has the smallest framework dependency and the largest product-owned platform surface.

It could be reconsidered if the shortlisted hosts add unacceptable dependencies or block required device/model capabilities and the team is prepared to own all four shells.

## Why not use a browser plus a local companion service?

A Progressive Web App could communicate with a separately installed local service for models, private storage, and package validation. This is plausible on desktop but difficult to distribute, authenticate, secure, and support. It is a poor fit for iOS and Android lifecycle and application-store expectations.

It could be reconsidered for a desktop-only administrative or authoring tool, not as the initial learner platform.

## Does PWA already violate the platform specification?

Potentially. The current platform specification says Web is optional and required platforms must receive first-class applications rather than redirects to a website. The PWA scheme is retained because it tests whether an installed PWA can satisfy the intended outcome with the smallest dependency surface.

PWA selection requires explicit evidence and a deliberate platform-specification amendment. It cannot become the default merely because the frontend already uses HTML.

## Are frameworks such as Lit, React, Vue, or Svelte platform schemes?

No. They are frontend libraries or frameworks. They may produce semantic HTML, but they do not independently provide Android, iOS, Windows, and macOS packaging, secure native storage, application permissions, or local native model execution.

The initial shared frontend deliberately uses standard JavaScript and native DOM APIs. A frontend framework can be evaluated later if the Card runtime develops a demonstrated complexity that native APIs do not manage clearly.

## Can a rejected option still use the same Cards?

Only if it can consume the same semantic Card HTML and manifest without changing their meaning. Hybrid WebView hosts can usually do this directly. Native-widget frameworks such as Valdi, Flutter, Compose Multiplatform, and React Native would require a separate renderer or a change from HTML to an intermediate Card model.

## What evidence would change the shortlist?

- A required platform or device capability cannot pass in any current scheme.
- A local intelligence runtime has materially better support in another host.
- Dependency, security, accessibility, application-store, or operational evidence invalidates a shortlisted scheme.
- Windows or another required platform is deferred.
- Literal semantic HTML stops being a product requirement.
- The team selects a primary native language or operating stack that materially changes maintenance cost.
