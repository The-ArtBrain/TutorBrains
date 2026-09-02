const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const patternsUrl = pathToFileURL(
  path.join(__dirname, "../../../..", "apps", "learner-web", "html", "pages", "patterns.html"),
).href;

test.beforeEach(async ({ page }) => {
  await page.goto(patternsUrl);
});

test("TC-25 keeps the Card template inert and structurally flat", async ({ page }) => {
  const result = await page.locator("#card-shell-template").evaluate((template) => ({
    renderedCards: document.querySelectorAll("article.card-shell").length,
    articleCount: template.content.querySelectorAll("article.card-shell").length,
    directSections: template.content.querySelectorAll("article.card-shell > section").length,
    labelledElements: Array.from(template.content.querySelectorAll("[aria-labelledby]")).every((element) =>
      element.getAttribute("aria-labelledby").split(/\s+/).every((id) => template.content.getElementById(id)),
    ),
  }));

  expect(result).toEqual({
    renderedCards: 0,
    articleCount: 1,
    directSections: 3,
    labelledElements: true,
  });
});

test("TC-26 cloning the outer template leaves nested content inert", async ({ page }) => {
  const result = await page.evaluate(() => {
    const outer = document.querySelector("#card-shell-template");
    document.querySelector("main").append(outer.content.cloneNode(true));

    return {
      renderedCards: document.querySelectorAll("article.card-shell").length,
      nestedTemplate: Boolean(document.querySelector("article.card-shell #help-control-template")),
      renderedHelpButtons: document.querySelectorAll("article.card-shell li button").length,
    };
  });

  expect(result).toEqual({ renderedCards: 1, nestedTemplate: true, renderedHelpButtons: 0 });
});

test("TC-27 nested content renders only after separate cloning", async ({ page }) => {
  await page.evaluate(() => {
    const outer = document.querySelector("#card-shell-template");
    document.querySelector("main").append(outer.content.cloneNode(true));

    const nested = document.querySelector("article.card-shell #help-control-template");
    nested.parentElement.append(nested.content.cloneNode(true));
  });

  await expect(page.locator("article.card-shell li button")).toHaveCount(1);
  await expect(page.getByRole("button", { name: "Help action placeholder" })).toBeVisible();
});
