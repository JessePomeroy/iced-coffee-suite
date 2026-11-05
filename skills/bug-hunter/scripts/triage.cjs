#!/usr/bin/env node

/**
 * triage.cjs — Zero-token pre-Recon codebase triage
 *
 * Runs BEFORE any LLM agent is invoked. Uses pure filesystem operations
 * (no fd, rg, grep, or any optional CLI tool) to:
 *
 * 1. Count and classify all source files
 * 2. Decide the optimal execution strategy
 * 3. Build a risk-scored file list using path heuristics
 * 4. Compute FILE_BUDGET from actual file sizes
 * 5. Output a machine-readable plan the orchestrator can act on directly
 *
 * This replaces the expensive "Recon agent reads 2,000 files" step with
 * a deterministic script that costs 0 tokens and runs in <2 seconds.
 *
 * Usage:
 *   triage.cjs scan <targetPath> [--output <path>] [--max-depth <n>]
 *   triage.cjs scan <targetPath> --format human
 *
 * Output: JSON plan to stdout (or --output file) with:
 *   - strategy: "single-file" | "small" | "parallel" | "extended" | "scaled" | "large-codebase"
 *   - fileBudget: computed from actual file sizes
 *   - domains: directory-level risk classification
 *   - riskMap: file-level classification (only for ≤200 files)
 *   - plan: which mode file to read, whether --loop is needed
 */

const fs = require('fs');
const path = require('path');

const MAX_SCAN_DEPTH = 100;

// ─── Source extensions ───────────────────────────────────────────────
const {
  DEFAULT_SOURCE_TOKEN_BUDGET,
  MAX_FILES_PER_CHUNK,
  SOURCE_SKIP_DIRECTORIES: SKIP_DIRS,
  buildSourceChunks,
  isServerSourcePath,
  isSupportedSourceFile,
  isTestSourcePath,
  sourceExclusionReason
} = require('./source-config.cjs');

// ─── Non-source directories (low value for bug hunting) ─────────────
const LOW_VALUE_DIRS = new Set([
  'docs', 'doc', 'documentation', 'assets', 'public', 'static',
  'images', 'img', 'icons', 'fonts', 'styles', 'css', 'scss',
  'less', 'locales', 'i18n', 'l10n', 'translations',
  'migrations', 'seeds', 'fixtures', 'snapshots', '__snapshots__',
  'scripts', 'tools', 'devtools', 'examples', 'samples', 'demo',
  'storybook', '.storybook', 'stories'
]);

// ─── Risk classification by directory name ──────────────────────────
const CRITICAL_PATTERNS = /\b(auth|security|session|token|jwt|oauth|saml|permission|acl|rbac|crypto|secret|credential|password|login|signup|register|verify|middleware|gateway|proxy|payment|billing|checkout|charge|subscription|stripe|paypal|webhook|callback)\b/i;
const HIGH_PATTERNS = /\b(api|route|router|controller|handler|endpoint|resolver|service|model|schema|database|db|repository|store|state|queue|worker|job|cron|consumer|producer|cache|redis|mongo|prisma|sequelize|typeorm|knex|sql|graphql|trpc|grpc|socket|websocket|sse|stream|upload|download|file|storage|s3|email|notification|sms)\b/i;
const MEDIUM_PATTERNS = /\b(util|utils|helper|helpers|lib|common|shared|core|config|env|logger|error|exception|validator|sanitize|transform|format|parse|convert|serialize)\b/i;

// ─── Walk filesystem (no external tools needed) ─────────────────────
function walkDir(dirPath, maxDepth, currentDepth) {
  if (currentDepth > maxDepth) {
    return [];
  }

  let entries;
  try {
    entries = fs.readdirSync(dirPath, { withFileTypes: true });
  } catch {
    return [];
  }

  const results = [];

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);

    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || entry.name.startsWith('.')) {
        continue;
      }
      results.push(...walkDir(fullPath, maxDepth, currentDepth + 1));
    } else if (entry.isFile() && isSupportedSourceFile(fullPath)) {
      results.push(fullPath);
    }
  }

  return results;
}

// ─── Classify a single file by its path ─────────────────────────────
function classifyFile(filePath, repoRoot) {
  const relative = path.relative(repoRoot, filePath);
  const parts = relative.split(path.sep);
  const dirPath = parts.slice(0, -1).join('/');
  const fileName = parts[parts.length - 1];

  // Test files
  if (isTestSourcePath(relative)) {
    return 'context-only';
  }

  // Low-value directories
  if (parts.some((p) => LOW_VALUE_DIRS.has(p.toLowerCase()))) {
    return 'low';
  }

  // Check file path + name against risk patterns
  const fullPathStr = dirPath + '/' + fileName;
  if (CRITICAL_PATTERNS.test(fullPathStr)) {
    return 'critical';
  }
  if (isServerSourcePath(relative) || HIGH_PATTERNS.test(fullPathStr)) {
    return 'high';
  }
  if (MEDIUM_PATTERNS.test(fullPathStr)) {
    return 'medium';
  }

  // Default: medium (unknown files are worth scanning)
  return 'medium';
}

// ─── Discover domain boundaries ─────────────────────────────────────
function discoverDomains(files, repoRoot) {
  // Group files by their top-level meaningful directory
  const domainFiles = new Map();

  for (const filePath of files) {
    const relative = path.relative(repoRoot, filePath);
    const parts = relative.split(path.sep);

    // Find the domain root: first 1-2 meaningful directory levels
    let domainKey;
    if (parts.length <= 1) {
      domainKey = '.';
    } else if (['src', 'lib', 'app', 'packages', 'services', 'apps', 'modules'].includes(parts[0].toLowerCase())) {
      domainKey = parts.length >= 3 ? parts.slice(0, 2).join('/') : parts[0];
    } else {
      domainKey = parts[0];
    }

    if (!domainFiles.has(domainKey)) {
      domainFiles.set(domainKey, []);
    }
    domainFiles.get(domainKey).push(filePath);
  }

  // Classify each domain
  const domains = [];
  for (const [domainPath, domainFileList] of domainFiles.entries()) {
    const riskCounts = { critical: 0, high: 0, medium: 0, low: 0, 'context-only': 0 };
    for (const f of domainFileList) {
      const risk = classifyFile(f, repoRoot);
      riskCounts[risk] += 1;
    }

    // Domain tier = based on concentration of risk, not just presence
    let tier;
    const total = domainFileList.length;
    const criticalRatio = riskCounts.critical / total;
    const highRatio = riskCounts.high / total;

    if (riskCounts.critical >= 3 && criticalRatio >= 0.15) {
      // Genuinely critical: meaningful portion of files are critical
      tier = 'CRITICAL';
    } else if (riskCounts.critical >= 1 && criticalRatio >= 0.3) {
      // Small domain where most files are critical
      tier = 'CRITICAL';
    } else if (riskCounts.critical >= 1) {
      // Has some critical files but mostly other stuff — boost to HIGH
      tier = 'HIGH';
    } else if (riskCounts.high > 0) {
      tier = 'HIGH';
    } else if (riskCounts['context-only'] === total) {
      tier = 'CONTEXT-ONLY';
    } else if (riskCounts.low > total * 0.5) {
      tier = 'LOW';
    } else {
      tier = 'MEDIUM';
    }

    domains.push({
      path: domainPath,
      tier,
      fileCount: domainFileList.length,
      riskBreakdown: riskCounts,
      files: domainFileList.map((f) => path.relative(repoRoot, f))
    });
  }

  // Sort: CRITICAL first, then HIGH, then MEDIUM, then rest
  const tierOrder = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3, 'CONTEXT-ONLY': 4 };
  domains.sort((a, b) => (tierOrder[a.tier] ?? 99) - (tierOrder[b.tier] ?? 99));

  return domains;
}

// ─── Compute FILE_BUDGET from actual file sizes ─────────────────────
function computeFileBudget(files) {
  if (files.length === 0) {
    return { fileBudget: MAX_FILES_PER_CHUNK, avgLines: 0, totalLines: 0, avgTokens: 0, sampledFiles: 0 };
  }

  // Sample up to 30 files to estimate average size (fast, even for huge repos)
  const sampleSize = Math.min(30, files.length);
  const step = Math.max(1, Math.floor(files.length / sampleSize));
  let totalLines = 0;
  let totalBytes = 0;
  let sampled = 0;
  const maxSampleBytes = 5 * 1024 * 1024;

  for (let i = 0; i < files.length && sampled < sampleSize; i += step) {
    try {
      const stat = fs.statSync(files[i]);
      if (stat.size > maxSampleBytes) {
        continue;
      }
      const content = fs.readFileSync(files[i], 'utf8');
      totalLines += content.split('\n').length;
      totalBytes += Buffer.byteLength(content);
      sampled += 1;
    } catch {
      // Skip unreadable files
    }
  }

  if (sampled === 0) {
    return { fileBudget: MAX_FILES_PER_CHUNK, avgLines: 0, totalLines: 0, avgTokens: 0, sampledFiles: 0 };
  }

  const avgLines = Math.round(totalLines / sampled);
  const avgBytes = Math.round(totalBytes / sampled);
  const avgTokens = Math.max(1, Math.ceil(avgBytes / 4));
  const estimatedTotalLines = avgLines * files.length;

  // Use the first risk-ordered concrete chunk as the safe FILE_BUDGET.
  // The runtime keeps the full variable-size plan and enforces every chunk.
  const plannedChunks = buildSourceChunks(files, {
    maxFiles: MAX_FILES_PER_CHUNK,
    maxSourceTokens: DEFAULT_SOURCE_TOKEN_BUDGET,
    enforceTokenBudget: true
  });
  const fileBudget = plannedChunks.length > 0
    ? Math.max(1, plannedChunks[0].files.length)
    : MAX_FILES_PER_CHUNK;

  return {
    fileBudget,
    avgLines,
    totalLines: estimatedTotalLines,
    avgTokens,
    sampledFiles: sampled,
    plannedChunkCount: plannedChunks.length
  };
}

// ─── Determine strategy ─────────────────────────────────────────────
function determineStrategy(fileCount, fileBudget) {
  if (fileCount <= 1) {
    return { strategy: 'single-file', modeFile: 'modes/single-file.md', needsLoop: false };
  }
  if (fileCount <= 10) {
    return { strategy: 'small', modeFile: 'modes/small.md', needsLoop: false };
  }
  if (fileCount <= fileBudget) {
    return { strategy: 'parallel', modeFile: 'modes/parallel.md', needsLoop: false };
  }
  if (fileCount <= fileBudget * 2) {
    return { strategy: 'extended', modeFile: 'modes/extended.md', needsLoop: false };
  }
  if (fileCount <= fileBudget * 3) {
    return { strategy: 'scaled', modeFile: 'modes/scaled.md', needsLoop: false };
  }
  return { strategy: 'large-codebase', modeFile: 'modes/large-codebase.md', needsLoop: true };
}

// ─── Build the risk map (file-level, only for small/medium codebases)
function buildRiskMap(files, repoRoot) {
  const riskMap = { critical: [], high: [], medium: [], low: [], 'context-only': [] };

  for (const filePath of files) {
    const risk = classifyFile(filePath, repoRoot);
    const relative = path.relative(repoRoot, filePath);
    riskMap[risk].push(relative);
  }

  // Sort each tier alphabetically
  for (const tier of Object.keys(riskMap)) {
    riskMap[tier].sort();
  }

  return riskMap;
}

// ─── Main: triage scan ──────────────────────────────────────────────
function scan(targetPath, options) {
  const resolvedTarget = path.resolve(targetPath);
  const maxDepth = options.maxDepth ?? 20;

  if (!Number.isInteger(maxDepth) || maxDepth < 0 || maxDepth > MAX_SCAN_DEPTH) {
    throw new Error(`max depth must be an integer between 0 and ${MAX_SCAN_DEPTH}`);
  }

  if (!fs.existsSync(resolvedTarget)) {
    throw new Error(`Target not found: ${resolvedTarget}`);
  }

  const stat = fs.statSync(resolvedTarget);
  if (!stat.isFile() && !stat.isDirectory()) {
    throw new Error(`Target must be a file or directory: ${resolvedTarget}`);
  }
  const repoRoot = path.resolve(options.repoRoot || (stat.isFile() ? inferFileRoot(resolvedTarget) : resolvedTarget));
  if (!fs.statSync(repoRoot).isDirectory()) throw new Error('--repo-root must be a directory');
  assertContained(resolvedTarget, repoRoot);
  const excludedFiles = [];
  const candidates = options.files !== undefined
    ? readFileScope(options.files).map((file) => path.resolve(repoRoot, file))
    : stat.isFile() ? [resolvedTarget] : walkDir(resolvedTarget, maxDepth, 0);
  const allFiles = [...new Set(candidates)].filter((file) => {
    assertContained(file, repoRoot);
    if (!fs.statSync(file).isFile()) throw new Error(`Scoped path must be a file: ${file}`);
    const relative = path.relative(repoRoot, file);
    const reason = sourceExclusionReason(file, repoRoot);
    if (reason) excludedFiles.push({ file: relative, reason });
    return reason === null;
  });
  const totalFiles = allFiles.length;

  // Compute FILE_BUDGET
  const budget = computeFileBudget(allFiles);

  // Determine strategy
  const { strategy, modeFile, needsLoop } = determineStrategy(totalFiles, budget.fileBudget);

  // Discover domains
  const domains = discoverDomains(allFiles, repoRoot);

  // Explicit scopes always retain exact paths; whole-repository scans may summarize.
  const includeFileRiskMap = options.files !== undefined || totalFiles <= 200;
  const riskMap = includeFileRiskMap ? buildRiskMap(allFiles, repoRoot) : null;

  // Build scan order: CRITICAL → HIGH → MEDIUM → LOW (skip context-only)
  let scanOrder;
  if (riskMap) {
    scanOrder = [...riskMap.critical, ...riskMap.high, ...riskMap.medium, ...riskMap.low];
  } else {
    // For large codebases, just list domains in priority order
    scanOrder = domains
      .filter((d) => d.tier !== 'CONTEXT-ONLY')
      .map((d) => `${d.path}/ (${d.fileCount} files, ${d.tier})`);
  }

  // Token estimates
  const scannable = allFiles.filter((file) => classifyFile(file, repoRoot) !== 'context-only').length;
  const tokensPerFile = budget.avgTokens || 400;
  const reconTokens = includeFileRiskMap ? Math.min(totalFiles * 20, 5000) : Math.min(domains.length * 100, 3000);
  const perHunterChunk = Math.min(budget.fileBudget, scannable) * tokensPerFile;
  const totalTokenEstimate = reconTokens + (scannable * tokensPerFile) + (scannable * 200); // 200 tokens per finding estimate

  // Recommendations
  const recommendations = [];
  if (strategy === 'single-file' || strategy === 'small') {
    recommendations.push('Small codebase — Recon is optional, proceed directly to Hunter.');
  }
  if (strategy === 'large-codebase') {
    recommendations.push('Large codebase — use domain-scoped auditing. Process one domain at a time.');
    recommendations.push(`${domains.filter((d) => d.tier === 'CRITICAL').length} CRITICAL domains to audit first.`);
    if (!needsLoop) {
      recommendations.push('Consider --loop for full coverage.');
    }
  }
  if (budget.avgLines > 300) {
    recommendations.push(`Large files (avg ${budget.avgLines} lines) — FILE_BUDGET is low (${budget.fileBudget}). Chunking is important.`);
  }
  if (totalFiles > 500 && !includeFileRiskMap) {
    recommendations.push('File-level risk map omitted for performance. Recon should classify files within each domain.');
  }
  if (riskMap && riskMap.critical.length + riskMap.high.length + riskMap.medium.length === 0 && riskMap.low.length > 0) {
    recommendations.push('Only LOW-tier source files detected — promote them into scan order to avoid an empty audit.');
  }

  const result = {
    generatedAt: new Date().toISOString(),
    target: resolvedTarget,
    repoRoot,
    excludedFiles,
    totalFiles,
    scannableFiles: scannable,
    strategy,
    modeFile,
    needsLoop,
    fileBudget: budget.fileBudget,
    avgLines: budget.avgLines,
    avgTokensPerFile: budget.avgTokens || 400,
    estimatedTotalLines: budget.totalLines,
    sampledFiles: budget.sampledFiles,
    plannedChunkCount: budget.plannedChunkCount || 0,
    domains: domains.map((d) => ({
      path: d.path,
      tier: d.tier,
      fileCount: d.fileCount,
      riskBreakdown: d.riskBreakdown
    })),
    scanOrder,
    tokenEstimate: {
      recon: reconTokens,
      perHunterChunk,
      totalPipeline: totalTokenEstimate
    },
    recommendations
  };

  // Include file-level risk map only for small-to-medium codebases
  if (riskMap) {
    result.riskMap = riskMap;
  }

  // Include domain file lists only for large-codebase strategy
  if (strategy === 'large-codebase') {
    result.domainFileLists = {};
    for (const domain of domains) {
      if (domain.tier !== 'CONTEXT-ONLY') {
        result.domainFileLists[domain.path] = domain.files.filter((file) => !isTestSourcePath(file));
      }
    }
  }

  return result;
}

function assertContained(file, repoRoot) {
  for (const [candidate, root] of [[file, repoRoot], [fs.realpathSync(file), fs.realpathSync(repoRoot)]]) {
    const relative = path.relative(root, candidate);
    if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
      throw new Error(`Scoped path is outside --repo-root: ${file}`);
    }
  }
}

function inferFileRoot(file) {
  let directory = path.dirname(file);
  let fallbackRoot;
  while (true) {
    // A nested package is not a repository boundary: it may itself be a test
    // fixture or dependency. Prefer enclosing Git context over package markers.
    if (fs.existsSync(path.join(directory, '.git'))) return directory;
    if (fs.existsSync(path.join(directory, 'package.json'))) fallbackRoot = directory;
    const parent = path.dirname(directory);
    const name = path.basename(directory);
    if (isTestSourcePath(name) || (SKIP_DIRS.has(name) && parent !== path.parse(directory).root)
      || name === '.svelte-kit') {
      fallbackRoot = parent;
    }
    if (parent === directory) break;
    directory = parent;
  }
  if (fallbackRoot) return fallbackRoot;
  // Keep conventional context/generated ancestors visible even without a project marker.
  const parts = path.dirname(file).split(path.sep);
  const boundary = parts.findLastIndex((part) => isTestSourcePath(part)
    || ['src', 'lib', '.svelte-kit', 'node_modules', 'dist', 'build'].includes(part));
  return boundary >= 0 ? parts.slice(0, boundary).join(path.sep) || path.parse(file).root : path.dirname(file);
}

function readFileScope(input) {
  const value = JSON.parse(input.trim().startsWith('[') ? input : fs.readFileSync(path.resolve(input), 'utf8'));
  const files = Array.isArray(value) ? value : value?.ok === true ? value.changedFiles : null;
  if (!Array.isArray(files) || files.some((file) => typeof file !== 'string' || !file.trim())) {
    throw new Error('--files must contain a JSON array of nonempty paths or an ok:true resolver object with changedFiles');
  }
  return files;
}

// ─── Human-readable output ──────────────────────────────────────────
function formatHuman(result) {
  const lines = [];
  lines.push(`Bug Hunter Triage — ${result.target}`);
  lines.push('═'.repeat(60));
  lines.push('');
  lines.push(`Total source files:    ${result.totalFiles}`);
  lines.push(`Scannable files:       ${result.scannableFiles}`);
  lines.push(`Average lines/file:    ${result.avgLines}`);
  lines.push(`FILE_BUDGET:           ${result.fileBudget}`);
  lines.push(`Strategy:              ${result.strategy}`);
  lines.push(`Mode file:             ${result.modeFile}`);
  lines.push(`Needs --loop:          ${result.needsLoop ? 'YES' : 'no'}`);
  lines.push('');
  lines.push('Domains:');
  // Sort by tier for display: CRITICAL → HIGH → MEDIUM → LOW → CONTEXT-ONLY
  const tierOrder = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3, 'CONTEXT-ONLY': 4 };
  const sorted = [...result.domains].sort((a, b) => (tierOrder[a.tier] ?? 99) - (tierOrder[b.tier] ?? 99));
  for (const d of sorted) {
    lines.push(`  ${d.tier.padEnd(12)} ${d.path} (${d.fileCount} files)`);
  }
  lines.push('');
  lines.push('Token estimates:');
  lines.push(`  Recon:           ~${result.tokenEstimate.recon.toLocaleString()} tokens`);
  lines.push(`  Per Hunter chunk: ~${result.tokenEstimate.perHunterChunk.toLocaleString()} tokens`);
  lines.push(`  Full pipeline:   ~${result.tokenEstimate.totalPipeline.toLocaleString()} tokens`);
  lines.push('');
  if (result.recommendations.length > 0) {
    lines.push('Recommendations:');
    for (const r of result.recommendations) {
      lines.push(`  • ${r}`);
    }
  }
  return lines.join('\n');
}

// ─── CLI ─────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = { command: null, target: null, output: null, maxDepth: 20, format: 'json', files: undefined, repoRoot: undefined };
  let i = 0;
  if (argv.length > 0 && !argv[0].startsWith('-')) {
    args.command = argv[0];
    i = 1;
  }
  if (i < argv.length && !argv[i].startsWith('-')) {
    args.target = argv[i];
    i += 1;
  }
  while (i < argv.length) {
    const flag = argv[i];
    if (flag === '--files' || flag === '--repo-root') {
      if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) throw new Error(`${flag} requires a value`);
      args[flag === '--files' ? 'files' : 'repoRoot'] = argv[i + 1];
      i += 2;
    } else if (flag === '--output' && i + 1 < argv.length) {
      args.output = argv[i + 1];
      i += 2;
    } else if (flag === '--max-depth' && i + 1 < argv.length) {
      const maxDepth = Number(argv[i + 1]);
      if (!Number.isInteger(maxDepth) || maxDepth < 0 || maxDepth > MAX_SCAN_DEPTH) {
        throw new Error(`--max-depth must be an integer between 0 and ${MAX_SCAN_DEPTH}`);
      }
      args.maxDepth = maxDepth;
      i += 2;
    } else if (flag === '--format' && i + 1 < argv.length) {
      args.format = argv[i + 1];
      i += 2;
    } else {
      i += 1;
    }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.command !== 'scan' || !args.target) {
    console.error('Usage:');
    console.error('  triage.cjs scan <targetPath> [--files <manifest.json>] [--repo-root <root>] [--output <path>] [--max-depth <n>] [--format json|human]');
    process.exit(1);
  }

  const result = scan(args.target, { maxDepth: args.maxDepth, files: args.files, repoRoot: args.repoRoot });

  if (args.format === 'human') {
    console.log(formatHuman(result));
  } else {
    const json = JSON.stringify(result, null, 2);
    if (args.output) {
      const dir = path.dirname(args.output);
      if (dir && !fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(args.output, json + '\n', 'utf8');
      console.log(JSON.stringify({ ok: true, outputPath: args.output, totalFiles: result.totalFiles, strategy: result.strategy }));
    } else {
      console.log(json);
    }
  }
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
