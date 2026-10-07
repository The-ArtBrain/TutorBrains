import { build } from "esbuild";

await build({
  entryPoints: [process.env.BRAINOS_AUTH_ENTRY ?? "../../auth/src/main.js"],
  outfile: process.env.BRAINOS_AUTH_OUTFILE ?? "../../dist/auth.js",
  nodePaths: ["node_modules"],
  bundle: true,
  format: "iife",
  platform: "browser",
  target: ["es2020"],
  minify: true,
  legalComments: "none",
});
