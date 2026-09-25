# Learner Web static interface review

This directory currently contains a non-functional semantic Hypertext Markup Language (HTML) and Cascading Style Sheets (CSS) review slice. The landing page combines welcome and learning preferences, with a guest link to Chapter 01. The lesson presents one current Card with its content and available abilities.

Build both instruction languages using the [build instructions](build-tools/README.md), then open or serve `dist/index.html`. This root entry redirects to the default English page at `dist/en/html/pages/index.html`; Hindi is available at `dist/hi/html/pages/index.html`. Every course page is generated. Source HTML under `html/pages/` contains `[#key]` placeholders and is an authoring source, not the finished interface. Generated pages use ordinary relative links and can be opened directly from the filesystem or served by any static file server. Reusable interface icons live as separate files under [`assets/icons/`](assets/icons/); the interface does not depend on the specification SVGs in `doc/spec/`.

Application pages use repository-level `content/<page>.<language>.yml` instructions. The generic `chapter.html` source reads `chapter.yml` and `chapter.<language>.yml` from each selected course chapter folder; generic `lesson.html` reads lesson content from each lesson folder. Generated filenames include their chapter and lesson IDs. Optional top-level `content/<page>.yml` files hold fixed application material such as canonical Telugu and the catalogue's explicitly English and Hindi specimens. Text and accessibility labels are resolved during the build; no browser localization code is required.

Every page header includes the same [account menu partial](html/includes/account-menu.inc) during the build and uses [`account-menu.css`](css/components/account-menu.css). The circular image defaults to [`user.svg`](assets/icons/user.svg); a future identity integration can supply a user photo by replacing the image `src`. The current guest fixture links to the setup section on the index page and to Sign in. A signed-in state should replace the Sign in link with a real Sign out action when authentication exists; this static review has no sign-out endpoint.

## Current boundary

- HTML expresses document structure, navigation, language, forms, and learner-facing content.
- CSS provides a small responsive presentation layer.
- Navigation links work; controls that require application services are visibly disabled rather than appearing active.
- This fixture presents Lesson 1 through one Card but does not finalize the domain rule: a Card may represent a Lesson or an activity. Listen, Learn, Build, Talk, and Check may be useful authoring labels, but this interface does not expose them as phases, navigation, or an imposed order.
- There is no JavaScript, server, authentication integration, persistence, course schema, or final data contract.
- Firebase, Supabase, or another future identity service must bind behind the provider-neutral sign-in interface.
- Chapter 01 values are illustrative fixtures, not a proposed serialization format.

The [`patterns.html`](html/pages/patterns.html) catalogue documents the current Card structure through ordinary English and Hindi specimens. Shared Card, learner-space, user-action, and learning-group styles live under [`css/components/`](css/components/); catalogue-only layout remains in [`css/pattern-catalogue.css`](css/pattern-catalogue.css) and does not override component behavior. Visible `<data>` values keep stable meaning separate from localized wording. The catalogue is a review aid, not a template, cloning mechanism, educational hierarchy, or final data contract.
