const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 10_000,
  use: {
    browserName: "chromium",
    channel: "chrome",
    headless: true,
  },
});
