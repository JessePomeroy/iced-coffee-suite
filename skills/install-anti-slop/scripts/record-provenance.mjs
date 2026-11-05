#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { provenanceFilename, sha256, verifyBundle } from "./bundle.mjs";

const [checkout, revision] = process.argv.slice(2);
if (!checkout || !/^[a-f0-9]{40}$/.test(revision ?? "")) {
  console.error("Usage: node scripts/record-provenance.mjs <upstream-git-checkout> <full-reviewed-revision>");
  process.exit(1);
}
const sourcePath = "skills/install-anti-slop/assets/anti-slop";
const directory = resolve(dirname(fileURLToPath(import.meta.url)), "../assets/anti-slop");
const git = (...args) => execFileSync("git", args, { cwd: resolve(checkout) });
const filenames = git("ls-tree", "-r", "--name-only", revision, "--", sourcePath)
  .toString().trim().split("\n").filter(Boolean)
  .map((filename) => filename.slice(sourcePath.length + 1)).sort();
function walk(path, prefix = "") {
  return readdirSync(path, { withFileTypes: true }).flatMap((entry) => {
    if (entry.isSymbolicLink()) throw new Error("Bundled source must use regular files");
    const name = prefix + entry.name;
    return entry.isDirectory() ? walk(resolve(path, entry.name), name + "/") : [name];
  });
}
const localNames = walk(directory).filter((name) => !["LICENSE", provenanceFilename].includes(name)).sort();
if (!filenames.length || JSON.stringify(filenames) !== JSON.stringify(localNames))
  throw new Error("Bundled file set differs from the reviewed upstream revision");

const files = {};
for (const filename of filenames) {
  const bytes = readFileSync(resolve(directory, filename));
  if (!bytes.equals(git("show", `${revision}:${sourcePath}/${filename}`)))
    throw new Error(`Bundled source does not match the reviewed upstream revision: ${filename}`);
  files[filename] = sha256(bytes);
}
const license = git("show", `${revision}:LICENSE`);
files.LICENSE = sha256(license);
const manifest = {
  schemaVersion: 1,
  repository: "https://github.com/dmmulroy/anti-slop",
  revision,
  sourcePath,
  licensePath: "LICENSE",
  files: Object.fromEntries(Object.entries(files).sort(([a], [b]) => a.localeCompare(b))),
};
writeFileSync(resolve(directory, "LICENSE"), license);
writeFileSync(resolve(directory, provenanceFilename), JSON.stringify(manifest, null, 2) + "\n");
verifyBundle(directory);
console.log(`Recorded ${filenames.length} unchanged source files and their license at ${revision}`);
