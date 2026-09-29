const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const outputRoot = path.resolve(__dirname, "../../../../apps/learner-web/dist/telugu");
const pageUrl = (language, name) => pathToFileURL(path.join(outputRoot, language, `${name}.html`)).href;
const names = ["index", "chapter-01", "sign-in", "patterns"];

test("root index opens the default English learner page", async ({ page }) => {
  await page.goto(pathToFileURL(path.join(outputRoot, "index.html")).href);
  await expect(page).toHaveURL(pageUrl("en", "index"));
  await expect(page.locator("html")).toHaveAttribute("lang", "en-IN");
});

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
        const menu = page.locator(".account-menu");
        await expect(menu.locator("summary")).toHaveAccessibleName(
          language === "en" ? "Account menu" : "खाता मेनू",
        );
        await expect(menu.locator('a[href="index.html#preferences"]')).toBeHidden();
        await menu.locator("summary").click();
        await expect(menu.locator('a[href="index.html#preferences"]')).toBeVisible();
        await expect(menu.locator('a[href="sign-in.html"]')).toBeVisible();
        const state = await page.evaluate(() => ({
          hasHorizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          scripts: Array.from(document.scripts, (script) => ({
            src: script.getAttribute("src"),
            defer: script.defer,
          })),
          unlabeledControls: Array.from(document.querySelectorAll("select, input")).filter(
            (control) => !control.labels?.length,
          ).length,
        }));
        expect(state, name).toEqual({
          hasHorizontalOverflow: false,
          scripts: [{ src: "assets/js/instruction-language-preference.js", defer: true }],
          unlabeledControls: 0,
        });
      }
      await page.goto(pageUrl(language, "index"));
      const indexSections = page.locator("main > section");
      await expect(indexSections.nth(0).locator('a[href="sign-in.html"]')).toBeVisible();
      const preferences = page.locator("#preferences");
      await expect(preferences).not.toHaveAttribute("open", "");
      await expect(preferences.locator("#setup-title")).toBeHidden();
      await preferences.locator("summary").click();
      await expect(preferences).toHaveAttribute("open", "");
      await expect(page.locator('.guest-entry a[href="#next-chapter"]')).toBeVisible();
      const nextChapter = page.locator("#next-chapter");
      await expect(nextChapter).not.toHaveAttribute("open", "");
      await expect(nextChapter.locator('a[href="chapter-01.html"]')).toBeHidden();
      await nextChapter.locator("summary").click();
      await expect(nextChapter).toHaveAttribute("open", "");
      await expect(nextChapter.locator('a[href="chapter-01.html"]')).toBeVisible();
      await expect(page.locator("#instruction-language option:checked")).toHaveAttribute("lang", language);
      await expect(page.locator("form button")).toBeDisabled();
      await expect(page.locator('main a[href="chapter-01.html"]')).toBeVisible();
    });
  }

  test(`${language}: navigation preserves language through the lesson and its return path`, async ({ page }) => {
    await page.goto(pageUrl(language, "index"));
    await page.locator("#next-chapter summary").click();
    await page.locator('main a[href="chapter-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
    await page.locator('main a[href="chapter-01-lesson-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01-lesson-01"));
    await page.locator(".lesson-context").click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
    await page.locator(".account-menu summary").click();
    await page.locator('nav a[href="index.html#preferences"]').click();
    await expect(page).toHaveURL(`${pageUrl(language, "index")}#preferences`);
    await page.locator('.account-menu summary').click();
    await page.locator('nav a[href="sign-in.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "sign-in"));
    await page.locator('main a[href="chapter-01.html"]').click();
    await expect(page).toHaveURL(pageUrl(language, "chapter-01"));
  });
}
