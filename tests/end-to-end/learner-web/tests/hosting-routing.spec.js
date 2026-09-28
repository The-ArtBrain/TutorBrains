const fs = require("node:fs");
const path = require("node:path");
const { expect, test } = require("@playwright/test");

const repositoryRoot = path.resolve(__dirname, "../../../..");
const infraRoot = path.join(repositoryRoot, "apps/learner-web/infra");
const distRoot = path.join(repositoryRoot, "apps/learner-web/dist");
const preferenceScriptPath = path.join(
  repositoryRoot,
  "apps/learner-web/assets/js/instruction-language-preference.js",
);

async function loadRootFunction() {
  const source = fs.readFileSync(path.join(infraRoot, "functions/index.js"), "utf8");
  return import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);
}

test("root Function selects a supported language and returns an uncacheable redirect", async () => {
  const { onRequest } = await loadRootFunction();
  const response = onRequest({
    request: new Request("https://learntelugu.brainos.in/", {
      headers: { "Accept-Language": "en-IN;q=0.4, hi-IN;q=0.9" },
    }),
  });

  expect(response.status).toBe(307);
  expect(response.headers.get("location")).toBe("/hi/index.html");
  expect(response.headers.get("cache-control")).toBe("private, no-store");
  expect(response.headers.get("vary")).toBe("Cookie, Accept-Language");
  expect(response.headers.get("x-content-type-options")).toBe("nosniff");
});

test("root Function accepts only a valid preference cookie and otherwise falls back safely", async () => {
  const { onRequest } = await loadRootFunction();
  const redirectFor = (cookie, acceptLanguage = "hi-IN") =>
    onRequest({
      request: new Request("https://learntelugu.brainos.in/", {
        headers: { Cookie: cookie, "Accept-Language": acceptLanguage },
      }),
    }).headers.get("location");

  expect(redirectFor("tb_instruction_language=en")).toBe("/en/index.html");
  expect(redirectFor("tb_instruction_language=fr")).toBe("/hi/index.html");
  expect(redirectFor("tb_instruction_language=%E0%A4%A", "fr-FR")).toBe("/en/index.html");
});

test("route policy invokes the Function only for the site root", () => {
  const routes = JSON.parse(fs.readFileSync(path.join(infraRoot, "policies/_routes.json"), "utf8"));

  expect(routes).toEqual({ version: 1, include: ["/"], exclude: [] });
  expect(routes.include).not.toContain("/*");
});

test("generated locale pages load the hosted preference script", () => {
  for (const language of ["en", "hi"]) {
    const html = fs.readFileSync(path.join(distRoot, language, "index.html"), "utf8");
    expect(html).toContain('src="assets/js/instruction-language-preference.js"');
    expect(fs.existsSync(path.join(distRoot, language, "assets/js/instruction-language-preference.js"))).toBe(true);
  }
});

for (const language of ["en", "hi"]) {
  test(`hosted ${language} page persists only its validated path locale`, async ({ page, context }) => {
    await page.route("https://learntelugu.brainos.in/**", (route) =>
      route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Test</title>" }),
    );
    await page.goto(`https://learntelugu.brainos.in/${language}/index.html`);
    await page.addScriptTag({ content: fs.readFileSync(preferenceScriptPath, "utf8") });

    const cookies = await context.cookies("https://learntelugu.brainos.in/");
    const preference = cookies.find(({ name }) => name === "tb_instruction_language");
    expect(preference?.value).toBe(language);
    expect(preference?.secure).toBe(true);
    expect(preference?.sameSite).toBe("Lax");
  });
}

test("hosted preference script ignores an unsupported leading path", async ({ page, context }) => {
  await page.route("https://learntelugu.brainos.in/**", (route) =>
    route.fulfill({ contentType: "text/html", body: "<!doctype html><title>Test</title>" }),
  );
  await page.goto("https://learntelugu.brainos.in/fr/index.html");
  await page.addScriptTag({ content: fs.readFileSync(preferenceScriptPath, "utf8") });

  const cookies = await context.cookies("https://learntelugu.brainos.in/");
  expect(cookies.some(({ name }) => name === "tb_instruction_language")).toBe(false);
});
