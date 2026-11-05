# Anti-slop profiles

The plugin exports individual rules; profiles below are configuration recipes,
not a new runtime layer. Copy only the selected entries into the project's existing
configuration and adjust based on actual diagnostics. No profile overrides an
existing project's explicitly chosen policy.

## Baseline for new installations

Start by previewing these at `warn`; promote to `error` after checking representative
code and resolving authorized migration work:

```json
{
  "anti-slop/no-chained-type-assertions": "error",
  "anti-slop/no-known-value-widening": "error",
  "anti-slop/no-widen-then-assert": "error"
}
```

These target assertion/widening patterns. They still require judgment about the
actual types and external contracts; do not claim zero false positives.

Review the contract before changing a diagnostic:

- Preserve deliberate finite-key mappings, mutable dynamic dictionaries, and
  public return types when callers rely on those contracts. An annotation that
  looks broad to a syntax rule is not proof of a defect.
- Replace erased local evidence with a named owner-derived payload, inference,
  or `satisfies` when it preserves the real contract. Do not introduce aliases
  merely to conceal a warning.
- Boundary decoders still accept `unknown` and validate it. Never substitute a
  cast for validation or coerce malformed input into an accepted string.
- Review partial third-party mocks and intentionally invalid fixtures individually.
  Prefer typed mock observations, honest optional fixture types, and real pure
  error constructors when these avoid unnecessary casts. Do not blanket-ignore
  tests or construct a complete SDK object just to satisfy syntax lint.

A repository can enforce `no-widen-then-assert` while the other two rules remain
reviewed warnings. Zero findings for one rule does not establish that the complete
profile is enforced. Baseline rules are syntax checks; in Svelte, the current
Oxlint integration checks extracted script blocks, not templates or styles.
`scripts/test-profiles.mjs` exercises positive and legitimate boundary examples
with an existing project toolchain; these are smoke fixtures, not the upstream
rule suite or a promise of exhaustive language coverage.

## Optional stricter policy

The remaining rules express stronger preferences about API shapes, test doubles,
runtime checks, names, reflection, dictionaries, and comments. Enable them only
for the requested project policy, with diagnostics reviewed first:

- `no-conditional-empty-object-spread`
- `no-module-mocking`
- `no-object-parameters`
- `no-reflect-apply`, `no-reflect-get`
- `no-runtime-typeof`
- `no-shape-in-symbol-names`
- `no-unknown-parameters`, `no-unknown-returns`, `no-unknown-type-aliases`
- `no-unsafe-dictionary-type`
- `require-safety-comment-for-type-assertion`

For domain-only enforcement, use the configuration's supported file overrides.
Determine real boundary paths first; do not assume a universal directory layout.
Disable `no-unknown-parameters`, `no-unknown-returns`, `no-unknown-type-aliases`,
and `no-runtime-typeof` on the specific parsers/validators and framework adapters
that legitimately handle untrusted input. If a boundary helper lives among domain
files, choose a precise exception instead of renaming or moving it just to appease
lint. A broad directory exemption should have a concrete ownership reason.

`no-runtime-typeof` supports `allowInTypeGuards: true`, but that only covers
predicate-returning guards, not every legitimate decoder. A decoder can accept
unknown, inspect a primitive, throw on invalid input, and return a domain value.
Do not force it into a predicate, add a dependency, or hide unknown behind an alias.

Verification examples for profile selection:
- A decoder accepting unknown and validating a string remains valid at a boundary.
- An internal function receiving unparsed unknown can be flagged under strict policy.
- A justified third-party test double is reviewed before banning module mocking.
- Existing enforced rules stay enforced unless their policy change is requested.
