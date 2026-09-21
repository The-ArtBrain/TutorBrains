const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  globalSetup: require.resolve("./build-pages"),
  timeout: 10_000,
  use: {
    browserName: "chromium",
    channel: "chrome",
    headless: true,
  },
});
