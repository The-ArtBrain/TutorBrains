import { rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = dirname(fileURLToPath(import.meta.url));
const localOutput = resolve(packageRoot, "../../dist/auth.js");
const mountedOutput = "/workspace/apps/learner-web/dist/auth.js";
const output = process.env.BRAINOS_AUTH_OUTFILE
  ? resolve(process.env.BRAINOS_AUTH_OUTFILE)
  : localOutput;

if (output !== localOutput && output !== mountedOutput) {
  throw new Error("Refusing to clean an unexpected auth build output path");
}

await rm(output, { force: true });
