<!-- Generated from skills/doc-lookup/SKILL.md by scripts/generate-compat-prompts.cjs. -->
---
name: doc-lookup
description: "Unified documentation lookup for Bug Hunter agents. Uses Context Hub (chub) as primary source with Context7 API fallback. Provides verified library/framework documentation to prevent false positives and ensure correct fix patterns."
---

# Doc Lookup — Verified Documentation Access

## Documentation Lookup (Context Hub + Context7 fallback)

When you need to verify a claim about how a library, framework, or API actually behaves — do NOT guess from training data. Look it up.

### When to use this

- "This framework includes X protection by default" — verify it
- "This ORM parameterizes queries automatically" — verify it
- "This function validates input" — verify it
- "The docs say to do X" — verify it
- Any claim about library behavior that affects your bug verdict

### How to use it

Resolve the installed file's directory first. This skill lives at
`<bug-hunter-root>/skills/doc-lookup/SKILL.md`; the helper is
`../../scripts/doc-lookup.cjs` relative to that directory. Resolve the absolute
bundle-root path and verify the helper exists before invoking it. Do not assume
an environment variable was injected, or use the current project's scripts.
In the examples below, replace `<bug-hunter-root>` with that resolved path.

The lookup script tries **Context Hub (chub)** first for curated, versioned docs, then falls back to **Context7** when chub doesn't have the library.

**Step 1: Search for the library**
```bash
node "<bug-hunter-root>/scripts/doc-lookup.cjs" search "<library>" "<what you need to know>"
```
Example: `node "<bug-hunter-root>/scripts/doc-lookup.cjs" search "prisma" "SQL injection parameterized queries"`

This returns results from both sources with a `recommended_source` and `recommended_id`.

**Step 2: Fetch documentation**
```bash
node "<bug-hunter-root>/scripts/doc-lookup.cjs" get "<library-or-id>" "<specific question>"
```
Example: `node "<bug-hunter-root>/scripts/doc-lookup.cjs" get "prisma/orm" "are raw queries parameterized by default"`

This fetches curated docs from chub if available, otherwise Context7 documentation snippets with code examples.

**Optional flags:**
- `--lang js|py` — language variant (for chub docs with multiple languages)
- `--source chub|context7` — force a specific source

### Rules

- Only look up docs when you have a SPECIFIC claim to verify. Do not speculatively fetch docs for every library in the codebase.
- Keep lookups specific and bounded. If a result does not resolve the claim, inspect installed source/types or the version-appropriate primary documentation rather than treating the first snippet as proof.
- If the API fails or returns nothing useful, say so explicitly: "Could not verify from docs — proceeding based on code analysis."
- Cite what you found: "Per Express docs: [quote]" or "Prisma docs confirm that $queryRaw uses parameterized queries."
