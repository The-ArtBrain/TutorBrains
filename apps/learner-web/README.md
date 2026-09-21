# Learner Web static interface review

This directory currently contains a non-functional semantic Hypertext Markup Language (HTML) and Cascading Style Sheets (CSS) review slice. It starts at Chapter 01 and presents one current Lesson Card with its content and available abilities.

Build both instruction languages using the [build instructions](build-tools/README.md), then start with `dist/en/html/pages/index.html` or `dist/hi/html/pages/index.html`. Every page is generated. Source HTML under `html/pages/` contains `[#key]` placeholders and is an authoring source, not the finished interface. Generated pages use ordinary relative links and can be opened directly from the filesystem or served by any static file server. Reusable interface icons live as separate files under [`assets/icons/`](assets/icons/); the interface does not depend on the specification SVGs in `doc/spec/`.

The non-lesson pages use repository-level `content/<page>.<language>.yml` instructions, matching the HTML filename. Optional `content/<page>.yml` files contain fixed material such as canonical Telugu and the catalogue's explicitly English and Hindi specimens. Lesson content retains its existing course-owned text files. Text and accessibility labels are resolved during the build; no browser localization code is required. Layout, controls, and styling remain the reviewed interface.

## Current boundary

- HTML expresses document structure, navigation, language, forms, and learner-facing content.
- CSS provides a small responsive presentation layer.
- Navigation links work; controls that require application services are visibly disabled rather than appearing active.
- This fixture presents Lesson 1 through one Card but does not finalize the domain rule: a Card may represent a Lesson or an activity. Listen, Learn, Build, Talk, and Check may be useful authoring labels, but this interface does not expose them as phases, navigation, or an imposed order.
- There is no JavaScript, server, authentication integration, persistence, course schema, or final data contract.
- Firebase, Supabase, or another future identity service must bind behind the provider-neutral sign-in interface.
- Chapter 01 values are illustrative fixtures, not a proposed serialization format.

The [`patterns.html`](html/pages/patterns.html) catalogue documents the current Card structure through ordinary English and Hindi specimens. Shared Card, learner-space, user-action, and learning-group styles live under [`css/components/`](css/components/); catalogue-only layout remains in [`css/pattern-catalogue.css`](css/pattern-catalogue.css) and does not override component behavior. Visible `<data>` values keep stable meaning separate from localized wording. The catalogue is a review aid, not a template, cloning mechanism, educational hierarchy, or final data contract.
