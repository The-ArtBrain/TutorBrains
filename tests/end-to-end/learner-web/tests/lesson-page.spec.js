const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { expect, test } = require("@playwright/test");

const lessonPages = ["lesson-01.html", "lesson-01-hi.html"];

function lessonUrl(filename) {
  return pathToFileURL(path.join(__dirname, "../../../..", "apps", "learner-web", "html", "pages", filename)).href;
}

async function openLesson(page, filename, viewport) {
  await page.setViewportSize(viewport);
  await page.goto(lessonUrl(filename));
}

async function disclosureMeasurements(page) {
  return page.locator(".reference-item .content-disclosure").evaluateAll((disclosures) =>
    disclosures.map((disclosure) => {
      const summary = disclosure.querySelector("summary");
      const range = document.createRange();
      range.selectNodeContents(summary);

      return {
        disclosureHeight: disclosure.getBoundingClientRect().height,
        summaryHeight: summary.getBoundingClientRect().height,
        summaryLines: Array.from(range.getClientRects()).filter(
          (rectangle) => rectangle.width > 0 && rectangle.height > 0,
        ).length,
      };
    }),
  );
}

for (const filename of lessonPages) {
  test.describe(filename, () => {
    test("TC-08 keeps the lesson content controls in semantic order", async ({ page }) => {
      await openLesson(page, filename, { width: 780, height: 996 });

      const isOrdered = await page.evaluate(() => {
        const contentHelp = document.querySelector(".content-help");
        const buttons = contentHelp.querySelectorAll(":scope > button");
        const nodes = [
          document.querySelector(".target-expression"),
          contentHelp.querySelector(".content-disclosure--transliteration"),
          buttons[0],
          buttons[1],
        ];

        return nodes.every(
          (node, index) =>
            node &&
            (index === 0 ||
              Boolean(nodes[index - 1].compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING)),
        );
      });

      expect(isOrdered).toBe(true);
    });

    test("TC-15 keeps the reference group unnamed and its disclosures independent", async ({ page }) => {
      await openLesson(page, filename, { width: 780, height: 996 });

      const referenceGroup = page.locator(".reference-group");
      await expect(referenceGroup.locator("article.reference-item")).toHaveCount(3);
      await expect(referenceGroup.locator("h1, h2, h3, h4, h5, h6")).toHaveCount(0);
      await expect(referenceGroup.locator("details:not([open])")).toHaveCount(3);
      await expect(page.locator("body")).not.toContainText("Related Learning");
      await expect(page.locator("body")).not.toContainText("Extra work");
    });

    if (filename === "lesson-01.html") {
      test("TC-16 matches disclosure outlines when a summary wraps at 780 by 996", async ({ page }) => {
        await openLesson(page, filename, { width: 780, height: 996 });

        const measurements = await disclosureMeasurements(page);
        expect(measurements[1].summaryLines).toBeGreaterThan(1);

        const outlineHeights = measurements.map(({ disclosureHeight }) => Math.round(disclosureHeight));
        expect(new Set(outlineHeights).size).toBe(1);
      });
    }

    test("TC-17 keeps summaries compact whenever none of them wraps", async ({ page }) => {
      await openLesson(page, filename, { width: 680, height: 996 });

      const measurements = await disclosureMeasurements(page);
      expect(measurements.every(({ summaryLines }) => summaryLines === 1)).toBe(true);

      const rootFontSize = await page.locator("html").evaluate(
        (html) => Number.parseFloat(getComputedStyle(html).fontSize),
      );
      const normalMinimumHeight = rootFontSize * 2.8;

      for (const { summaryHeight } of measurements) {
        expect(summaryHeight).toBeLessThanOrEqual(normalMinimumHeight + 1);
      }
    });

    test("TC-18 stacks closed disclosures below 44rem and opens only the selected one", async ({ page }) => {
      await openLesson(page, filename, { width: 390, height: 844 });

      const articles = page.locator(".reference-item");
      const boxes = await articles.evaluateAll((items) =>
        items.map((item) => {
          const rectangle = item.getBoundingClientRect();
          return {
            top: rectangle.top,
            bottom: rectangle.bottom,
            left: rectangle.left,
            width: rectangle.width,
          };
        }),
      );

      expect(boxes[1].top).toBeGreaterThan(boxes[0].bottom);
      expect(boxes[2].top).toBeGreaterThan(boxes[1].bottom);
      expect(Math.max(...boxes.map(({ width }) => width)) - Math.min(...boxes.map(({ width }) => width))).toBeLessThanOrEqual(1);
      expect(Math.max(...boxes.map(({ left }) => left)) - Math.min(...boxes.map(({ left }) => left))).toBeLessThanOrEqual(1);

      const disclosures = page.locator(".reference-item details");
      await expect(page.locator(".reference-item details[open]")).toHaveCount(0);
      await disclosures.nth(1).locator("summary").click();

      const openStates = await disclosures.evaluateAll((items) => items.map((item) => item.open));
      expect(openStates).toEqual([false, true, false]);
    });
  });
}
