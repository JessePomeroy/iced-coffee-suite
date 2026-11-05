import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { verifyBundle } from "./bundle.mjs";

const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");

test("fresh install, reviewed replacement, and source drift preserve ownership", () => {
  const root = mkdtempSync(join(tmpdir(), "anti-slop-install-"));
  try {
    const source = join(root, "skill");
    const target = join(root, "consumer");
    cpSync(skill, source, { recursive: true });
    const run = (...args) => spawnSync(process.execPath, [join(source, "scripts/install.mjs"), target, ...args], { encoding: "utf8" });
    assert.equal(run().status, 0);
    assert.deepEqual(verifyBundle(target), verifyBundle(join(source, "assets/anti-slop")));

    const entry = join(target, "index.ts");
    const original = readFileSync(entry, "utf8");
    writeFileSync(entry, "// consumer customization\n");
    assert.equal(run().status, 1);
    assert.equal(readFileSync(entry, "utf8"), "// consumer customization\n");

    const extra = join(target, "consumer-notes.txt");
    writeFileSync(extra, "preserve me\n");
    assert.equal(run("--force").status, 0);
    assert.equal(readFileSync(entry, "utf8"), original);
    assert.equal(readFileSync(extra, "utf8"), "preserve me\n");

    writeFileSync(join(source, "assets/anti-slop/index.ts"), "// source drift\n");
    const failure = run("--force");
    assert.notEqual(failure.status, 0);
    assert.match(failure.stderr, /differs from its provenance/);
    assert.equal(readFileSync(entry, "utf8"), original);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("invalid manifest paths are rejected before copying", () => {
  const root = mkdtempSync(join(tmpdir(), "anti-slop-manifest-"));
  try {
    cpSync(join(skill, "assets/anti-slop"), root, { recursive: true });
    const path = join(root, "PROVENANCE.json");
    const manifest = JSON.parse(readFileSync(path, "utf8"));
    manifest.files["../escaped.ts"] = "0".repeat(64);
    writeFileSync(path, JSON.stringify(manifest));
    assert.throws(() => verifyBundle(root), /Invalid anti-slop file record/);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("force rejects destination symlinks before replacing any owned file", () => {
  const root = mkdtempSync(join(tmpdir(), "anti-slop-symlink-"));
  try {
    const target = join(root, "consumer");
    const unrelated = join(root, "unrelated.ts");
    const owned = join(target, "LICENSE");
    mkdirSync(target);
    writeFileSync(unrelated, "unrelated source\n");
    writeFileSync(owned, "existing license\n");
    symlinkSync(unrelated, join(target, "index.ts"));
    const result = spawnSync(process.execPath, [join(skill, "scripts/install.mjs"), target, "--force"], { encoding: "utf8" });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Refusing unsafe anti-slop destination/);
    assert.equal(readFileSync(unrelated, "utf8"), "unrelated source\n");
    assert.equal(readFileSync(owned, "utf8"), "existing license\n");
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("help and invalid CLI arguments never create files", () => {
  const root = mkdtempSync(join(tmpdir(), "anti-slop-cli-"));
  try {
    for (const [args, status] of [
      [["--help"], 0], [["-h"], 0], [["--force", "--typo"], 1], [["first", "second"], 1],
    ]) {
      const result = spawnSync(process.execPath, [join(skill, "scripts/install.mjs"), ...args], { cwd: root, encoding: "utf8" });
      assert.equal(result.status, status);
      assert.deepEqual(readdirSync(root), []);
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
