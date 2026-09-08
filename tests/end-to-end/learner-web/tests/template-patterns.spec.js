const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const patternsUrl = pathToFileURL(
  path.join(__dirname, "../../../..", "apps", "learner-web", "html", "pages", "patterns.html"),
).href;

test.beforeEach(async ({ page }) => {
  await page.goto(patternsUrl);
});

test("TC-25 keeps exactly four structural templates inert", async ({ page }) => {
  const result = await page.evaluate(() => {
    const templates = Array.from(document.querySelectorAll("template"));
    const activeIds = Array.from(document.querySelectorAll("[id]"), ({ id }) => id);
    const referencesResolve = (root, getById) =>
      Array.from(root.querySelectorAll("[aria-labelledby]")).every((element) =>
        element
          .getAttribute("aria-labelledby")
          .split(/\s+/)
          .every((id) => getById(id)),
      );

    return {
      templateIds: templates.map(({ id }) => id),
      renderedCatalogueCards: document.querySelectorAll(".catalogue-specimen article.card").length,
      cardTemplateArticles: document.querySelector("#template-card").content.querySelectorAll("article.card").length,
      childCards: document.querySelector("#template-card").content.querySelectorAll("article.card article.card").length,
      activeIdsAreUnique: new Set(activeIds).size === activeIds.length,
      activeReferencesResolve: referencesResolve(document, (id) => document.getElementById(id)),
      templateReferencesResolve: templates.every((template) =>
        referencesResolve(template.content, (id) => template.content.getElementById(id)),
      ),
    };
  });

  expect(result).toEqual({
    templateIds: [
      "template-card",
      "template-learner-space",
      "template-user-action",
      "template-learning-group",
    ],
    renderedCatalogueCards: 2,
    cardTemplateArticles: 1,
    childCards: 0,
    activeIdsAreUnique: true,
    activeReferencesResolve: true,
    templateReferencesResolve: true,
  });
});

test("TC-26 keeps template naming aligned with root classes and stylesheets", async ({ page }) => {
  const result = await page.evaluate(() => {
    const expectedComponents = ["card", "learner-space", "user-action", "learning-group"];
    const stylesheetNames = Array.from(document.styleSheets, ({ href }) => href && new URL(href).pathname.split("/").pop());

    return expectedComponents.map((component) => {
      const template = document.querySelector(`#template-${component}`);
      return {
        component,
        hasTemplate: Boolean(template),
        hasRootClass: Boolean(template && template.content.querySelector(`.${component}`)),
        hasStylesheet: stylesheetNames.includes(`${component}.css`),
      };
    });
  });

  expect(result).toEqual([
    { component: "card", hasTemplate: true, hasRootClass: true, hasStylesheet: true },
    { component: "learner-space", hasTemplate: true, hasRootClass: true, hasStylesheet: true },
    { component: "user-action", hasTemplate: true, hasRootClass: true, hasStylesheet: true },
    { component: "learning-group", hasTemplate: true, hasRootClass: true, hasStylesheet: true },
  ]);
});

test("TC-27 keeps English and Hindi values parallel in one document", async ({ page }) => {
  const specimens = page.locator(".catalogue-specimen");
  await expect(specimens).toHaveCount(2);
  await expect(specimens.nth(0)).toHaveAttribute("lang", "en-IN");
  await expect(specimens.nth(1)).toHaveAttribute("lang", "hi-IN");

  const result = await specimens.evaluateAll((items) =>
    items.map((item) => ({
      cardValues: Array.from(item.querySelectorAll("data"), (value) => value.getAttribute("value")),
      capabilityValues: Array.from(item.querySelectorAll('data[value^="capability:"]'), (value) =>
        value.getAttribute("value"),
      ),
      teluguLanguageValues: Array.from(item.querySelectorAll('data[lang="te"]'), (value) => value.textContent.trim()),
    })),
  );

  expect(result[0].cardValues).toEqual(result[1].cardValues);
  expect(result[0].capabilityValues).toEqual([
    "capability:speak",
    "capability:write",
    "capability:type",
    "capability:accept-learner-image",
  ]);
  expect(result[0].capabilityValues).toEqual(result[1].capabilityValues);
  expect(result[0].teluguLanguageValues).toEqual(result[1].teluguLanguageValues);
});

test("TC-28 keeps component layouts unchanged inside the catalogue", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 1000 });

  const result = await page.locator(".catalogue-specimen").first().evaluate((specimen) => {
    const columnCount = (selector) =>
      getComputedStyle(specimen.querySelector(selector)).gridTemplateColumns.split(" ").length;

    return {
      userActionColumns: columnCount(".user-actions"),
      learningGroupColumns: columnCount(".card__learning-groups"),
    };
  });

  expect(result).toEqual({
    userActionColumns: 4,
    learningGroupColumns: 3,
  });
});
