import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

export const provenanceFilename = "PROVENANCE.json";
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

export function verifyBundle(directory) {
  const manifest = JSON.parse(readFileSync(resolve(directory, provenanceFilename), "utf8"));
  if (
    manifest.schemaVersion !== 1 ||
    manifest.repository !== "https://github.com/dmmulroy/anti-slop" ||
    !/^[a-f0-9]{40}$/.test(manifest.revision) ||
    !manifest.files || typeof manifest.files !== "object" || Array.isArray(manifest.files) ||
    !manifest.files["index.ts"] || !manifest.files.LICENSE
  ) throw new Error("Invalid anti-slop provenance manifest");

  for (const [filename, expected] of Object.entries(manifest.files)) {
    if (
      !/^(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_.-]+$/.test(filename) ||
      filename.split("/").some((part) => part === "." || part === "..") ||
      typeof expected !== "string" || !/^[a-f0-9]{64}$/.test(expected)
    ) throw new Error("Invalid anti-slop file record");
    if (sha256(readFileSync(resolve(directory, filename))) !== expected)
      throw new Error(`Bundled anti-slop file differs from its provenance: ${filename}`);
  }
  return manifest;
}
