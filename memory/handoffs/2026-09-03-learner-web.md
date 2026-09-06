# Learner Web Handoff

**Date:** 2026-09-03  
**Branch:** `feat/learner-web-static-html`  
**Status:** Static learner-interface review slice with automated browser coverage

## Scope

The current learner-web work is static semantic Hypertext Markup Language (HTML) and Cascading Style Sheets (CSS). Controls that need services remain deliberately non-functional. No JavaScript runtime, server, authentication, persistence, or content schema has been introduced.

## Current learner-page decisions

- The reviewed learner journey begins at Chapter 01. There is no Course Card or Outline interface at present; the absence of Outline is not a permanent architecture rule.
- A lesson presents one flat Card `article`. Content, response abilities, learner response, and references are parts of that Card rather than additional Cards.
- Breadcrumbs, the visible phase-progress row, repeated activity headings, learner-facing Card metadata, and the bottom Exit section were removed. Staff review context remains only in an HTML comment.
- The visible content order is Telugu expression, transliteration disclosure, Play audio, and Say it slowly.
- Speak, Write, Type, and Upload image are disabled controls. They stack vertically on narrow screens.
- Meaning, Characters in this lesson, and Grammar in this lesson appear after Your response. They move as one layout group but remain three independent, initially closed `article` disclosures with no learner-facing group heading.
- The lesson uses `page-shell page-shell--narrow`. The shared Card shadow token is `none`.
- The green palette follows the lesson wireframe, and interface icons are separate Scalable Vector Graphics (SVG) files.
- English and Hindi lesson pages retain parallel semantic structure and explicit language metadata.

## Tests

End-to-end browser tests are under [`tests/end-to-end/learner-web/`](../../tests/end-to-end/learner-web/). The test README contains the TC-01 through TC-27 catalogue and marks automated coverage.

- Automated lesson coverage: TC-08, TC-15, TC-16, TC-17, and TC-18.
- TC-16 runs against English because its assertion requires the longer English Characters summary to wrap at `780 × 996`; the Hindi label does not wrap at that size.
- Automated inert-template coverage: TC-25 through TC-27.
- Latest recorded complete run: 12 passing tests.

Run the suite:

```sh
cd tests/end-to-end/learner-web
npm install
npm test
```

Watch one test with Playwright Inspector:

```sh
npx playwright test --debug -g "TC-16"
```

## Review references

- [Learner-web guidance](../../apps/learner-web/AGENTS.md)
- [Learner-web review notes](../../apps/learner-web/README.md)
- [End-to-end test instructions and catalogue](../../tests/end-to-end/learner-web/README.md)
- [Lesson wireframe](../../doc/spec/student-lesson-wireframe.svg)
- [Proposed project structure](../../doc/design/project_structure.md)

## Continuation notes

- Manual cases that are not marked automated in the test catalogue still require review or future automation.
- Keep the static-interface boundary unless the work is explicitly expanded.
- Do not treat the current absence of Outline as a permanent rule.
- The root `memory.md` already had an unrelated working-tree modification when this handoff was created and was not edited as part of this work.
