#!/usr/bin/env node
import { copyFileSync, existsSync, lstatSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { provenanceFilename, verifyBundle } from "./bundle.mjs";

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const source = resolve(skillRoot, "assets/anti-slop");
const arguments_ = process.argv.slice(2);
const usage = "Usage: node scripts/install.mjs [target-directory] [--force]";
const targets = arguments_.filter((argument) => !argument.startsWith("-"));
const unknown = arguments_.filter((argument) => argument.startsWith("-") && !["--force", "--help", "-h"].includes(argument));
if (unknown.length || targets.length > 1) {
  console.error(usage);
  process.exit(1);
}
if (arguments_.includes("--help") || arguments_.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
const [targetArgument] = targets;
const target = resolve(process.cwd(), targetArgument ?? "tools/oxlint/anti-slop");
const force = arguments_.includes("--force");
const manifest = verifyBundle(source);

if (existsSync(target) && !force) {
  console.error(`Refusing to overwrite ${target}. Re-run with --force only after reviewing the existing files.`);
  process.exit(1);
}

const filenames = [...Object.keys(manifest.files), provenanceFilename];
// Inspect every destination before writing; force replaces owned files, not links.
for (const filename of filenames) {
  const parts = filename.split("/");
  for (let depth = 0; depth <= parts.length; depth++) {
    const path = join(target, ...parts.slice(0, depth));
    const stat = lstatSync(path, { throwIfNoEntry: false });
    if (stat && (stat.isSymbolicLink() || (depth === parts.length ? !stat.isFile() : !stat.isDirectory())))
      throw new Error(`Refusing unsafe anti-slop destination: ${path}`);
  }
}

for (const filename of filenames) {
  const destination = resolve(target, filename);
  mkdirSync(dirname(destination), { recursive: true });
  copyFileSync(resolve(source, filename), destination);
}
verifyBundle(target);
console.log(`Copied the verified anti-slop bundle at ${manifest.revision} to ${target}`);
console.log(`Configure Oxlint with: ${target}/index.ts`);
