# Learner Web end-to-end tests

These Playwright tests cover the shared lesson HTML source through test cases TC-08, TC-15 through TC-18, and TC-29, plus the HTML Card-pattern evaluations TC-25 through TC-28. They use an installed Google Chrome browser and do not require a learner-web server. Build-pipeline unit tests separately verify that the same lesson source generates English and Hindi output.

## Latest verification

The complete suite was run in Google Chrome after consolidating the lesson source: **10 passed**. The build-pipeline unit suite also recorded **11 passed**. Continuous integration is not configured for this static review slice.

## Test cases

| ID    | Test                                           | Expected result                                                                                                                 | Automated               |
| -------| ------------------------------------------------| ---------------------------------------------------------------------------------------------------------------------------------| -------------------------|
| TC-01 | Open the learner landing page                  | Learning begins with Chapter 01; no Course Card is displayed.                                                                   | No                      |
| TC-02 | Inspect visible navigation                     | No Outline page, rail, or explicit Outline link is present in the current interface.                                            | No                      |
| TC-03 | Open the lesson page                           | The lesson uses the `page-shell page-shell--narrow` layout.                                                                     | No                      |
| TC-04 | Inspect the lesson structure                   | One logical Card `article` contains content, abilities, response, and references.                                               | No                      |
| TC-05 | Inspect the top of the Card                    | Staff-only Card state, name, and review description are not visible.                                                            | No                      |
| TC-06 | Inspect lesson navigation                      | No breadcrumbs, repeated activity heading, or phase-progress row appears.                                                       | No                      |
| TC-07 | Inspect the bottom of the lesson               | No “Exit to Chapter 01” footer appears; the top Exit link remains.                                                              | No                      |
| TC-08 | Read the main content in order                 | Telugu expression is followed by transliteration, Play audio, and Say it slowly.                                                | Yes — shared source     |
| TC-09 | Open transliteration                           | Native `details`/`summary` shows transliterated text and switches between Show all and Hide.                                    | No                      |
| TC-10 | Use audio controls                             | Play audio and Say it slowly remain visible, disabled, and non-functional.                                                      | No                      |
| TC-11 | View response abilities on a narrow viewport   | Speak, Write, Type, and Upload image stack in one column.                                                                       | No                      |
| TC-12 | View response abilities at `44rem` or wider    | The four abilities display evenly in one row.                                                                                   | No                      |
| TC-13 | Inspect Your response                          | The response placeholder appears before Meaning, Characters, and Grammar.                                                       | No                      |
| TC-14 | Inspect the reference group                    | Meaning, Characters, and Grammar are independent closed disclosures.                                                            | No                      |
| TC-15 | Inspect reference-group labeling               | No Related Learning, Extra work, or other learner-facing group heading appears.                                                 | Yes — shared source     |
| TC-16 | View the English lesson at `780 × 996`         | When Characters in this lesson wraps, all three disclosure outlines match the tallest item.                                     | Yes — English           |
| TC-17 | View a layout where no reference summary wraps | Summaries use their compact natural height without a fixed enlarged height.                                                     | Yes — shared source     |
| TC-18 | View the lesson below `44rem`                  | Reference disclosures stack, start closed, and open independently.                                                              | Yes — shared source     |
| TC-19 | Inspect Card appearance                        | No drop shadow appears beneath the Card.                                                                                        | No                      |
| TC-20 | Inspect colours                                | Canvas, borders, controls, and accents use the approved green palette.                                                          | No                      |
| TC-21 | Inspect icons                                  | Interface icons load from separate external SVG files rather than inline SVG.                                                   | No                      |
| TC-22 | Compare English and Hindi lessons              | Structure, control order, disabled state, disclosures, and responsive layout correspond.                                        | No                      |
| TC-23 | Inspect language metadata                      | Telugu uses `lang="te"`, transliteration uses `lang="te-Latn"`, and language links declare their language.                      | No                      |
| TC-24 | Inspect page source                            | No JavaScript, inline event handler, server binding, or functional behavior is introduced.                                      | No                      |
| TC-25 | Inspect the Card catalogue                     | The specimens are ordinary active HTML, contain no templates, use unique references, and keep Cards flat.                       | Yes                     |
| TC-26 | Compare class and stylesheet names             | Card, learner-space, user-action, and learning-group use the same component name in HTML and CSS.                               | Yes                     |
| TC-27 | Compare English and Hindi specimens            | Both instruction-language specimens use parallel stable values and preserve the same canonical Telugu.                          | Yes                     |
| TC-28 | Compare catalogue component layout             | Catalogue specimens use the component-defined action and learning-group columns without a catalogue-specific override.          | Yes                     |
| TC-29 | Inspect lesson data placeholders               | Separate lesson and instruction blocks provide all placeholder and accessibility sources; no literal `aria-label` or JavaScript resolution remains. | Yes — shared source     |

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
