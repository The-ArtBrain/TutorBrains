const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const patternsUrl = pathToFileURL(
  path.join(__dirname, "../../../..", "apps", "learner-web", "dist", "en", "patterns.html"),
).href;

test.beforeEach(async ({ page }) => {
  await page.goto(patternsUrl);
});

test("TC-25 keeps Card specimens as ordinary flat HTML", async ({ page }) => {
  const result = await page.evaluate(() => {
    const activeIds = Array.from(document.querySelectorAll("[id]"), ({ id }) => id);
    const referencesResolve = Array.from(document.querySelectorAll("[aria-labelledby]")).every((element) =>
      element
        .getAttribute("aria-labelledby")
        .split(/\s+/)
        .every((id) => document.getElementById(id)),
    );

    return {
      templates: document.querySelectorAll("template").length,
      renderedCatalogueCards: document.querySelectorAll(".catalogue-specimen article.card").length,
      childCards: document.querySelectorAll("article.card article.card").length,
      activeIdsAreUnique: new Set(activeIds).size === activeIds.length,
      activeReferencesResolve: referencesResolve,
    };
  });

  expect(result).toEqual({
    templates: 0,
    renderedCatalogueCards: 2,
    childCards: 0,
    activeIdsAreUnique: true,
    activeReferencesResolve: true,
  });
});

test("TC-26 keeps component class and stylesheet names aligned", async ({ page }) => {
  const result = await page.evaluate(() => {
    const expectedComponents = ["card", "learner-space", "user-action", "learning-group"];
    const stylesheetNames = Array.from(document.styleSheets, ({ href }) => href && new URL(href).pathname.split("/").pop());

    return expectedComponents.map((component) => {
      return {
        component,
        hasRootClass: Boolean(document.querySelector(`.catalogue-specimen .${component}`)),
        hasStylesheet: stylesheetNames.includes(`${component}.css`),
      };
    });
  });

  expect(result).toEqual([
    { component: "card", hasRootClass: true, hasStylesheet: true },
    { component: "learner-space", hasRootClass: true, hasStylesheet: true },
    { component: "user-action", hasRootClass: true, hasStylesheet: true },
    { component: "learning-group", hasRootClass: true, hasStylesheet: true },
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
    const visibleColumnCount = (selector) => {
      const container = specimen.querySelector(selector);
      const itemPositions = Array.from(container.children, (item) =>
        Math.round(item.getBoundingClientRect().left),
      );

      return new Set(itemPositions).size;
    };

    return {
      userActionColumns: visibleColumnCount(".user-actions"),
      learningGroupColumns: visibleColumnCount(".card__learning-groups"),
    };
  });

  expect(result).toEqual({
    userActionColumns: 4,
    learningGroupColumns: 3,
  });
});
