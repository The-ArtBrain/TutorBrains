const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  globalSetup: require.resolve("./build-pages"),
  timeout: 10_000,
  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR || "./test-results",
  use: {
    browserName: "chromium",
    channel: "chrome",
    headless: true,
  },
});
