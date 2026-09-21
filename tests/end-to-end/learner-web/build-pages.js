const { execFileSync } = require("node:child_process");
const { existsSync } = require("node:fs");
const path = require("node:path");

module.exports = function buildPages() {
  const root = path.resolve(__dirname, "../../..");
  const buildTools = path.join(root, "apps/learner-web/build-tools");
  const localPython = path.join(buildTools, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const python = process.env.LEARNER_WEB_PYTHON || (existsSync(localPython) ? localPython : "python3");
  for (const language of ["en", "hi"]) {
    execFileSync(python, [path.join(buildTools, "build.py"), "--instruction-language", language], {
      cwd: root,
      stdio: "inherit",
    });
  }
};
