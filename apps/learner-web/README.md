# Learner Web static interface review

This directory currently contains a non-functional semantic Hypertext Markup Language (HTML) and Cascading Style Sheets (CSS) review slice. It explores the learner-facing Course → Chapter → Lesson → flat Card hierarchy using Chapter 01 content.

Start with [`html/pages/index.html`](html/pages/index.html). The pages use ordinary relative links and can be opened directly from the filesystem or served by any static file server. Reusable interface icons live as separate files under [`assets/icons/`](assets/icons/); the interface does not depend on the specification SVGs in `doc/spec/`.

## Current boundary

- HTML expresses document structure, navigation, language, forms, and learner-facing content.
- CSS provides a small responsive presentation layer.
- Navigation links work; controls that require application services are visibly disabled rather than appearing active.
- There is no JavaScript, server, authentication integration, persistence, course schema, or final data contract.
- Firebase, Supabase, or another future identity service must bind behind the provider-neutral sign-in interface.
- Chapter 01 values are illustrative fixtures, not a proposed serialization format.

The inert [`patterns.html`](html/pages/patterns.html) page records the `<template>` investigation. Templates are interface fragments only; they do not define the educational hierarchy.
