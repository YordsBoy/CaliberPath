#!/usr/bin/env node
// scripts/inventory_ksas.js
//
// Scans content/Individual_KSAs/**/*.md (skipping README.md files and
// _crosswalk/ documentation artifacts), validates each against
// schemas/ksa.schema.json, and writes:
//   reports/ksa_inventory.json       — full structured inventory
//   reports/ksa_inventory_report.md  — human-readable summary
//   reports/validation_errors.json   — schema violations

const fs     = require("fs");
const path   = require("path");
const glob   = require("glob");
const matter = require("gray-matter");
const Ajv    = require("ajv");

// ── Config ────────────────────────────────────────────────────────────────────
const ROOT       = path.resolve(__dirname, "..");
const SRC_GLOB   = "content/Individual_KSAs/**/*.md";
const SCHEMA_PATH = path.join(ROOT, "schemas/ksa.schema.json");
const REPORTS_DIR = path.join(ROOT, "reports");

const OPTIONAL_FIELDS = ["cluster_tags", "source_frameworks"];

// ── Setup ─────────────────────────────────────────────────────────────────────
fs.mkdirSync(REPORTS_DIR, { recursive: true });

const schema   = JSON.parse(fs.readFileSync(SCHEMA_PATH, "utf8"));
const ajv      = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);

// ── Collect files ─────────────────────────────────────────────────────────────
const allFiles = glob.sync(SRC_GLOB, { cwd: ROOT });
// Exclusions from KSA classification scope:
//   - README.md files: sector overviews, not KSA definitions.
//   - Anything under a _crosswalk/ path segment: documentation artifacts
//     (sector adjacency matrices, population-pathway crosswalks) that
//     intentionally lack KSA front-matter. Without this exclusion they
//     produce persistent schema-invalid surface in validation output.
const isReadme    = f => path.basename(f).toLowerCase() === "readme.md";
const isCrosswalk = f => f.split(/[\\/]/).includes("_crosswalk");
const ksaFiles    = allFiles.filter(f => !isReadme(f) && !isCrosswalk(f));

const readmeCount    = allFiles.filter(isReadme).length;
const crosswalkCount = allFiles.filter(f => !isReadme(f) && isCrosswalk(f)).length;

console.log(`Found ${allFiles.length} .md files total, ${ksaFiles.length} KSA files (${readmeCount} READMEs + ${crosswalkCount} _crosswalk artifacts excluded)\n`);

// ── Accumulators ──────────────────────────────────────────────────────────────
const inventory        = [];   // one entry per KSA file
const validationErrors = [];   // files that fail schema
const missingOptionals = [];   // files missing optional fields

const countBy = (key) => {
  const map = {};
  inventory.forEach(item => {
    const val = item[key] || "__missing__";
    map[val] = (map[val] || 0) + 1;
  });
  return map;
};

// ── Process each file ─────────────────────────────────────────────────────────
for (const relPath of ksaFiles) {
  const absPath = path.join(ROOT, relPath);
  let parsed;

  try {
    const raw = fs.readFileSync(absPath, "utf8");
    parsed    = matter(raw);
  } catch (err) {
    validationErrors.push({
      file: relPath,
      errors: [{ message: `Failed to read/parse file: ${err.message}` }],
    });
    continue;
  }

  const data = parsed.data;

  // Normalise: some early files use 'levels' instead of 'proficiency_levels'
  if (data.levels && !data.proficiency_levels) {
    data.proficiency_levels = data.levels;
    delete data.levels;
  }

  // Backfill ksa_id from filename when missing (mirrors build script behaviour)
  if (!data.ksa_id) {
    data.ksa_id = path.basename(absPath, ".md")
      .replace(/\s+/g, "_")
      .toLowerCase();
  }

  // ── Schema validation ──────────────────────────────────────────────────────
  const valid = validate(data);
  if (!valid) {
    validationErrors.push({
      file:   relPath,
      ksa_id: data.ksa_id || null,
      label:  data.label  || null,
      errors: validate.errors.map(e => ({
        field:   e.instancePath || e.params?.missingProperty || "(root)",
        message: e.message,
        params:  e.params,
      })),
    });
  }

  // ── Optional-field audit ───────────────────────────────────────────────────
  const missingOpts = OPTIONAL_FIELDS.filter(f => {
    const v = data[f];
    return v === undefined || v === null || (Array.isArray(v) && v.length === 0);
  });

  if (missingOpts.length) {
    missingOptionals.push({
      file:          relPath,
      ksa_id:        data.ksa_id || null,
      label:         data.label  || null,
      missing_fields: missingOpts,
    });
  }

  // ── Inventory entry ────────────────────────────────────────────────────────
  inventory.push({
    file:              relPath,
    ksa_id:            data.ksa_id            || null,
    label:             data.label             || null,
    category:          data.category          || null,
    sector:            data.sector            || null,
    horizon:           data.horizon           || null,
    has_cluster_tags:  Array.isArray(data.cluster_tags)     && data.cluster_tags.length > 0,
    has_source_fw:     Array.isArray(data.source_frameworks) && data.source_frameworks.length > 0,
    proficiency_level_count: Array.isArray(data.proficiency_levels) ? data.proficiency_levels.length : 0,
    schema_valid:      valid,
  });
}

// ── Build inventory JSON ───────────────────────────────────────────────────────
const inventoryJson = {
  generated_at:     new Date().toISOString(),
  total_ksa_files:  ksaFiles.length,
  total_valid:      inventory.filter(i => i.schema_valid).length,
  total_invalid:    validationErrors.length,
  by_category:      countBy("category"),
  by_sector:        countBy("sector"),
  by_horizon:       countBy("horizon"),
  missing_optionals_count: missingOptionals.length,
  ksas:             inventory,
};

fs.writeFileSync(
  path.join(REPORTS_DIR, "ksa_inventory.json"),
  JSON.stringify(inventoryJson, null, 2),
  "utf8"
);

// ── Build validation errors JSON ───────────────────────────────────────────────
fs.writeFileSync(
  path.join(REPORTS_DIR, "validation_errors.json"),
  JSON.stringify(
    {
      generated_at:  new Date().toISOString(),
      total_errors:  validationErrors.length,
      errors:        validationErrors,
    },
    null,
    2
  ),
  "utf8"
);

// ── Helpers for Markdown report ───────────────────────────────────────────────
function tableFromMap(map, labelCol = "Value", countCol = "Count") {
  const rows = Object.entries(map).sort((a, b) => b[1] - a[1]);
  const lines = [
    `| ${labelCol.padEnd(45)} | ${countCol} |`,
    `| ${"-".repeat(45)} | ${"-".repeat(5)} |`,
    ...rows.map(([k, v]) => `| ${k.padEnd(45)} | ${String(v).padStart(5)} |`),
  ];
  return lines.join("\n");
}

function pct(n, total) {
  return total === 0 ? "0%" : `${Math.round((n / total) * 100)}%`;
}

// ── Build human-readable Markdown report ─────────────────────────────────────
const total      = ksaFiles.length;
const validCount = inventory.filter(i => i.schema_valid).length;
const errCount   = validationErrors.length;

const byCat     = countBy("category");
const bySector  = countBy("sector");
const byHorizon = countBy("horizon");

const missingClusterTags = missingOptionals.filter(m => m.missing_fields.includes("cluster_tags")).length;
const missingSourceFw    = missingOptionals.filter(m => m.missing_fields.includes("source_frameworks")).length;
const missingBoth        = missingOptionals.filter(m => m.missing_fields.length === 2).length;

const errorListSection = validationErrors.length === 0
  ? "_No validation errors found._\n"
  : validationErrors.map(e => {
      const errLines = e.errors.map(err => `  - \`${err.field}\`: ${err.message}`).join("\n");
      return `### \`${e.file}\`\n**KSA ID:** \`${e.ksa_id || "missing"}\` | **Label:** ${e.label || "missing"}\n\n${errLines}`;
    }).join("\n\n");

const missingOptSection = missingOptionals.length === 0
  ? "_All KSAs have both optional fields._\n"
  : missingOptionals.slice(0, 50).map(m =>
      `| \`${m.ksa_id || "?"}\` | ${m.label || "?"} | ${m.missing_fields.join(", ")} |`
    ).join("\n")
    + (missingOptionals.length > 50
        ? `\n\n_…and ${missingOptionals.length - 50} more. See \`ksa_inventory.json\` for full list._`
        : "");

const report = `# KSA Inventory Report

**Generated:** ${new Date().toUTCString()}
**Repository:** CaliberPath

---

## 1. Summary

| Metric | Value |
| ----------------------------------------- | ----- |
| Total KSA files scanned                   | **${total}** |
| Schema-valid                              | **${validCount}** (${pct(validCount, total)}) |
| Schema-invalid                            | **${errCount}** (${pct(errCount, total)}) |
| Missing \`cluster_tags\` (optional)         | ${missingClusterTags} |
| Missing \`source_frameworks\` (optional)    | ${missingSourceFw} |
| Missing both optional fields              | ${missingBoth} |

---

## 2. KSAs by Category

${tableFromMap(byCat, "Category")}

---

## 3. KSAs by Sector

${tableFromMap(bySector, "Sector")}

---

## 4. KSAs by Horizon

${tableFromMap(byHorizon, "Horizon")}

---

## 5. Missing Optional Fields

Fields checked: \`cluster_tags\`, \`source_frameworks\`

${missingOptionals.length > 0
  ? `| KSA ID | Label | Missing Fields |\n| --- | --- | --- |\n${missingOptSection}`
  : missingOptSection}

---

## 6. Validation Errors

${errorListSection}

---

## 7. Output Files

| File | Description |
| ---- | ----------- |
| \`reports/ksa_inventory.json\` | Full structured inventory (all ${total} KSAs) |
| \`reports/ksa_inventory_report.md\` | This document |
| \`reports/validation_errors.json\` | ${errCount} schema violation(s) with details |
`;

fs.writeFileSync(
  path.join(REPORTS_DIR, "ksa_inventory_report.md"),
  report,
  "utf8"
);

// ── Console summary ───────────────────────────────────────────────────────────
console.log("═".repeat(60));
console.log("  KSA Inventory Complete");
console.log("═".repeat(60));
console.log(`  KSA files scanned : ${total}`);
console.log(`  Schema-valid       : ${validCount}`);
console.log(`  Schema-invalid     : ${errCount}`);
console.log(`  Missing optionals  : ${missingOptionals.length} file(s)`);
console.log("─".repeat(60));
console.log("  Reports written to reports/");
console.log("    ksa_inventory.json");
console.log("    ksa_inventory_report.md");
console.log("    validation_errors.json");
console.log("═".repeat(60));

if (errCount > 0) {
  console.error(`\n${errCount} validation error(s) found. See reports/validation_errors.json`);
  process.exit(1);
}
