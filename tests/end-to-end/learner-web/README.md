# Learner Web end-to-end tests

These Playwright tests cover lesson-page test cases TC-08, TC-15, TC-16, TC-17, and TC-18, plus isolated HTML-template evaluations TC-25 through TC-27. They use an installed Google Chrome browser and do not require a learner-web server.

## Latest verification

The complete suite was run in Google Chrome after adding the template evaluations: **12 passed**. The earlier manual lesson-page run also recorded **9 passed** before those three tests were added. Continuous integration is not configured for this static review slice.

## Test cases

| ID | Test | Expected result | Automated |
|---|---|---|---|
| TC-01 | Open the learner landing page | Learning begins with Chapter 01; no Course Card is displayed. | No |
| TC-02 | Inspect visible navigation | No Outline page, rail, or explicit Outline link is present in the current interface. | No |
| TC-03 | Open either lesson page | The lesson uses the `page-shell page-shell--narrow` layout. | No |
| TC-04 | Inspect the lesson structure | One logical Card `article` contains content, abilities, response, and references. | No |
| TC-05 | Inspect the top of the Card | Staff-only Card state, name, and review description are not visible. | No |
| TC-06 | Inspect lesson navigation | No breadcrumbs, repeated activity heading, or phase-progress row appears. | No |
| TC-07 | Inspect the bottom of the lesson | No “Exit to Chapter 01” footer appears; the top Exit link remains. | No |
| TC-08 | Read the main content in order | Telugu expression is followed by transliteration, Play audio, and Say it slowly. | Yes — English and Hindi |
| TC-09 | Open transliteration | Native `details`/`summary` shows transliterated text and switches between Show all and Hide. | No |
| TC-10 | Use audio controls | Play audio and Say it slowly remain visible, disabled, and non-functional. | No |
| TC-11 | View response abilities on a narrow viewport | Speak, Write, Type, and Upload image stack in one column. | No |
| TC-12 | View response abilities at `44rem` or wider | The four abilities display evenly in one row. | No |
| TC-13 | Inspect Your response | The response placeholder appears before Meaning, Characters, and Grammar. | No |
| TC-14 | Inspect the reference group | Meaning, Characters, and Grammar are independent closed disclosures. | No |
| TC-15 | Inspect reference-group labeling | No Related Learning, Extra work, or other learner-facing group heading appears. | Yes — English and Hindi |
| TC-16 | View the English lesson at `780 × 996` | When Characters in this lesson wraps, all three disclosure outlines match the tallest item. | Yes — English |
| TC-17 | View a layout where no reference summary wraps | Summaries use their compact natural height without a fixed enlarged height. | Yes — English and Hindi |
| TC-18 | View the lesson below `44rem` | Reference disclosures stack, start closed, and open independently. | Yes — English and Hindi |
| TC-19 | Inspect Card appearance | No drop shadow appears beneath the Card. | No |
| TC-20 | Inspect colours | Canvas, borders, controls, and accents use the approved green palette. | No |
| TC-21 | Inspect icons | Interface icons load from separate external SVG files rather than inline SVG. | No |
| TC-22 | Compare English and Hindi lessons | Structure, control order, disabled state, disclosures, and responsive layout correspond. | No |
| TC-23 | Inspect language metadata | Telugu uses `lang="te"`, transliteration uses `lang="te-Latn"`, and language links declare their language. | No |
| TC-24 | Inspect page source | No JavaScript, inline event handler, server binding, or functional behavior is introduced. | No |
| TC-25 | Inspect the inert Card template | No Card is rendered; the template contains one flat article, three sibling sections, and valid label references. | Yes |
| TC-26 | Clone the outer template in test code | One Card renders, while the preserved nested template and its help control remain inert. | Yes |
| TC-27 | Clone the nested template separately in test code | The help control renders only after explicit nested-content cloning. | Yes |

## Install

From the repository root:

```sh
cd tests/end-to-end/learner-web
npm install
```

## Run

```sh
npm test
```

## Watch the tests run

Run one test with Playwright Inspector so you can pause, step through, and inspect the page:

```sh
npx playwright test --debug -g "TC-16"
```

Run the complete suite in a visible browser, one test at a time:

```sh
npx playwright test --headed --workers=1
```

The tests finish quickly, so use debug mode when you want time to inspect an individual test.
