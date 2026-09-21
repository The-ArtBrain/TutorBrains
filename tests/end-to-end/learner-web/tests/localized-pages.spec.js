const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const outputRoot = path.resolve(__dirname, "../../../../apps/learner-web/dist");
const pageUrl = (language, name) => pathToFileURL(path.join(outputRoot, language, "html/pages", `${name}.html`)).href;
const names = ["index", "chapter-01", "preferences", "sign-in", "patterns"];

for (const language of ["en", "hi"]) {
  for (const width of [390, 1280]) {
    test(`${language}: generated pages are readable and accessible at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      for (const name of names) {
        await page.goto(pageUrl(language, name));
        await expect(page.locator("html")).toHaveAttribute("lang", `${language}-IN`);
        await expect(page.locator("body")).not.toContainText("[#");
        await expect(page.locator("main h1")).toBeVisible();
        await expect(page.locator(".brand")).toHaveAccessibleName(
          language === "en" ? "Telugu Tutor home" : "तेलुगु ट्यूटर का मुख्य पृष्ठ",
        );
        const state = await page.evaluate(() => ({
          hasHorizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          scripts: document.scripts.length,
          unlabeledControls: Array.from(document.querySelectorAll("select, input")).filter(
            (control) => !control.labels?.length,
          ).length,
        }));
        expect(state, name).toEqual({ hasHorizontalOverflow: false, scripts: 0, unlabeledControls: 0 });
      }
      await page.goto(pageUrl(language, "preferences"));
      await expect(page.locator("#instruction-language option:checked")).toHaveAttribute("lang", language);
      await expect(page.locator("form button")).toBeDisabled();
    });
  }

  test(`${language}: navigation preserves language through the lesson and its return path`, async ({ page }) => {
    await page.goto(pageUrl(language, "index"));
    await page.locator('main a[href="chapter-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
    await page.locator('main a[href="lesson-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "lesson-01"));
    await page.locator('a[aria-labelledby="lesson-exit-label"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
    await page.locator('nav a[href="preferences.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "preferences"));
    await page.locator('main a[href="sign-in.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "sign-in"));
    await page.locator('main a[href="chapter-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
  });
}
