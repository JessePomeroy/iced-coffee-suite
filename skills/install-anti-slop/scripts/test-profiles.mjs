#!/usr/bin/env node
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { cpSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const project = process.argv[2];
if (!project) {
  console.error("Usage: node scripts/test-profiles.mjs <project-with-installed-oxlint>");
  process.exit(1);
}
const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const root = mkdtempSync(join(tmpdir(), "anti-slop-profile-"));
try {
  symlinkSync(resolve(project, "node_modules"), join(root, "node_modules"), "dir");
  const install = spawnSync(process.execPath, [join(skill, "scripts/install.mjs"), join(root, "plugin")], { encoding: "utf8" });
  assert.equal(install.status, 0, install.stderr);
  cpSync(join(skill, "fixtures"), join(root, "fixtures"), { recursive: true });
  const config = {
    categories: { correctness: "off" }, plugins: [],
    jsPlugins: [{ name: "anti-slop", specifier: "./plugin/index.ts" }],
    rules: Object.fromEntries(["no-chained-type-assertions", "no-known-value-widening", "no-widen-then-assert"].map((rule) => [`anti-slop/${rule}`, "warn"])),
  };
  const run = (fixture) => {
    writeFileSync(join(root, ".oxlintrc.json"), JSON.stringify(config));
    const result = spawnSync(resolve(project, "node_modules/.bin/oxlint"), ["-c", ".oxlintrc.json", "--format", "json", `fixtures/${fixture}.ts`], { cwd: root, encoding: "utf8" });
    assert.ok(result.status === 0 || result.status === 1, result.stderr);
    const report = JSON.parse(result.stdout);
    return { status: result.status, codes: report.diagnostics.map((item) => item.code).sort() };
  };
  const positive = run("positive");
  assert.equal(positive.status, 0);
  assert.deepEqual(positive.codes, ["anti-slop(no-chained-type-assertions)", "anti-slop(no-known-value-widening)", "anti-slop(no-widen-then-assert)"].sort());
  assert.deepEqual(run("boundary"), { status: 0, codes: [] });
  const contracts = run("reviewed-contract");
  assert.equal(contracts.status, 0);
  assert.deepEqual(contracts.codes, ["anti-slop(no-chained-type-assertions)", ...Array(3).fill("anti-slop(no-known-value-widening)")].sort());
  config.rules["anti-slop/no-widen-then-assert"] = "error";
  assert.equal(run("positive").status, 1);
  assert.deepEqual(run("boundary"), { status: 0, codes: [] });
  console.log("Profile smoke passed: three baseline signals, valid decoder, four review-required contract signals, and selective enforcement.");
} finally {
  rmSync(root, { recursive: true, force: true });
}
