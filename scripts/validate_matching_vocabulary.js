#!/usr/bin/env node
// scripts/validate_matching_vocabulary.js
//
// KSA-Enrichment Ops/QA validator — WS-KSA-PERSONALIZATION-ENRICHMENT.
// Built by CC per the Ops/QA Validator Spec (Commission Deliverable 3 of 3, Info/Tech, 2026-06-20),
// released under Strategist -> CC handoff 2026-06-20 (LSA v5.28). Read-only: verifies, never authors or repairs.
//
// Four assertions:
//   (a) Schema conformance — discharged by scripts/validate_ksas.js, REUSED (DRY composition). The verification
//       gate runs validate_ksas.js first; this script does NOT duplicate the Ajv logic. Assertions (b)-(d) layer on top.
//   (b) Per-entry matching_vocabulary validity (non-empty `term`; in-enum `term_type`) with ksa_id + index
//       on any violation. HARD FAIL (non-zero exit).
//   (c) Coverage report over the 45 behavioral records — informational; printed and written to reports/. Exit 0 regardless.
//   (d) Crosswalk-integrity — every ksa_id referenced in any _crosswalk/ file exists in master_ksa.json.
//       HARD FAIL (non-zero exit).
//
// Inputs (read-only): schemas/ksa.schema.json, data/master_ksa.json, content/Individual_KSAs/**/_crosswalk/**/*.md
// Scope fences: no Tier 3 scoring/levels/weights; no record mutation; no framework_refs.

const fs   = require("fs");
const path = require("path");
const glob = require("glob");
const globSync = glob.sync || glob.globSync;

const SCHEMA_PATH = "schemas/ksa.schema.json";
const MASTER_PATH = "data/master_ksa.json";
const CROSSWALK_GLOB = "content/Individual_KSAs/**/_crosswalk/**/*.md";
const REPORT_DIR  = "reports";
const REPORT_PATH = path.join(REPORT_DIR, "matching_vocabulary_coverage_report.md");

// The 45 behavioral records are the three behavioral domain directories
// (self_management_personal_mastery/, professionalism/, leadership_influence/). master_ksa.json carries no
// directory path, so the behavioral corpus is identified by its `category` field — the clean in-corpus signal.
const BEHAVIORAL_CATEGORIES = ["Professionalism", "Leadership", "Self Management"];

// ---------------------------------------------------------------------------
// Load inputs
// ---------------------------------------------------------------------------
const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, "utf8"));
const ksas   = JSON.parse(fs.readFileSync(MASTER_PATH, "utf8"));

// term_type enum is sourced from the schema (single source of truth — no drift if the enum changes).
const TERM_TYPE_ENUM =
  schema.properties &&
  schema.properties.matching_vocabulary &&
  schema.properties.matching_vocabulary.items &&
  schema.properties.matching_vocabulary.items.properties &&
  schema.properties.matching_vocabulary.items.properties.term_type &&
  schema.properties.matching_vocabulary.items.properties.term_type.enum;

if (!Array.isArray(TERM_TYPE_ENUM) || TERM_TYPE_ENUM.length === 0) {
  console.error(`❌  Could not read matching_vocabulary.term_type enum from ${SCHEMA_PATH}. ` +
                `Has commit (a) (the schema-property addition) landed?`);
  process.exit(1);
}

const idSet = new Set(ksas.map(k => k.ksa_id));

let hardFail = false;

// ---------------------------------------------------------------------------
// Assertion (b): per-entry matching_vocabulary validity
// ---------------------------------------------------------------------------
console.log("── Assertion (b): matching_vocabulary entry validity ───────────────");
const bViolations = [];

ksas.forEach(k => {
  if (!Object.prototype.hasOwnProperty.call(k, "matching_vocabulary")) return;
  const mv = k.matching_vocabulary;
  if (!Array.isArray(mv)) {
    bViolations.push({ ksa_id: k.ksa_id, index: "-", problem: "matching_vocabulary is not an array" });
    return;
  }
  mv.forEach((entry, i) => {
    if (entry === null || typeof entry !== "object" || Array.isArray(entry)) {
      bViolations.push({ ksa_id: k.ksa_id, index: i, problem: "entry is not an object" });
      return;
    }
    const term = entry.term;
    const termType = entry.term_type;
    if (typeof term !== "string" || term.trim().length === 0) {
      bViolations.push({ ksa_id: k.ksa_id, index: i, problem: `empty or non-string term (got ${JSON.stringify(term)})` });
    }
    if (!TERM_TYPE_ENUM.includes(termType)) {
      bViolations.push({ ksa_id: k.ksa_id, index: i, problem: `out-of-enum term_type (got ${JSON.stringify(termType)})` });
    }
  });
});

if (bViolations.length === 0) {
  console.log("✅  All matching_vocabulary entries valid (non-empty term, in-enum term_type).");
} else {
  hardFail = true;
  console.log(`❌  ${bViolations.length} matching_vocabulary entry violation(s):`);
  bViolations.forEach(v => console.log(`     • ${v.ksa_id} [entry ${v.index}]: ${v.problem}`));
}

// ---------------------------------------------------------------------------
// Assertion (c): coverage report (informational)
// ---------------------------------------------------------------------------
console.log("\n── Assertion (c): coverage report (informational) ─────────────────");

const behavioral = ksas.filter(k => BEHAVIORAL_CATEGORIES.includes(k.category));

function mvOf(k) {
  const mv = k.matching_vocabulary;
  return Array.isArray(mv) ? mv : [];
}

const enriched = behavioral.filter(k => mvOf(k).length > 0);
const termCounts = enriched.map(k => mvOf(k).length).sort((a, b) => a - b);

function stat(arr) {
  if (arr.length === 0) return { min: 0, max: 0, mean: 0, median: 0 };
  const min = arr[0];
  const max = arr[arr.length - 1];
  const mean = arr.reduce((s, n) => s + n, 0) / arr.length;
  const mid = Math.floor(arr.length / 2);
  const median = arr.length % 2 === 0 ? (arr[mid - 1] + arr[mid]) / 2 : arr[mid];
  return { min, max, mean: Math.round(mean * 100) / 100, median };
}
const dist = stat(termCounts);

// Per-term_type totals across the behavioral corpus (coverage is scoped to the 45 behavioral records).
const typeTotals = {};
TERM_TYPE_ENUM.forEach(t => (typeTotals[t] = 0));
behavioral.forEach(k => mvOf(k).forEach(e => {
  if (Object.prototype.hasOwnProperty.call(typeTotals, e.term_type)) typeTotals[e.term_type] += 1;
}));

console.log(`Behavioral records:        ${behavioral.length} (expected 45)`);
console.log(`Enriched (non-empty mv):   ${enriched.length} of ${behavioral.length}`);
console.log(`Terms-per-record (enriched): min ${dist.min} · max ${dist.max} · mean ${dist.mean} · median ${dist.median}`);
console.log("Per-term_type totals (behavioral corpus):");
TERM_TYPE_ENUM.forEach(t => {
  const flag = (t === "credential_term" || t === "issuing_body") ? "  ◀ credential-readiness hook" : "";
  console.log(`   ${t.padEnd(16)} ${String(typeTotals[t]).padStart(5)}${flag}`);
});
if (enriched.length === 0) {
  console.log("⚠️  WARNING: zero behavioral records carry matching_vocabulary (no enrichment detected).");
}

// Write the durable report artifact.
fs.mkdirSync(REPORT_DIR, { recursive: true });

const perRecordRows = behavioral
  .slice()
  .sort((a, b) => mvOf(b).length - mvOf(a).length || String(a.ksa_id).localeCompare(String(b.ksa_id)))
  .map(k => `| \`${k.ksa_id}\` | ${k.category} | ${mvOf(k).length} |`)
  .join("\n");

const typeRows = TERM_TYPE_ENUM
  .map(t => {
    const note = (t === "credential_term" || t === "issuing_body") ? "credential-readiness hook (human-authored)" : "";
    return `| \`${t}\` | ${typeTotals[t]} | ${note} |`;
  })
  .join("\n");

const report = `# Matching-Vocabulary Coverage Report

**Workstream:** WS-KSA-PERSONALIZATION-ENRICHMENT
**Generated by:** \`scripts/validate_matching_vocabulary.js\` (assertion (c), informational)
**Generated at:** ${new Date().toISOString()}
**Scope:** the 45 behavioral records (categories: ${BEHAVIORAL_CATEGORIES.join(", ")}); technical KSAs excluded from coverage.

---

## Summary

| Metric | Value |
|---|---|
| Behavioral records | ${behavioral.length} (expected 45) |
| Enriched (non-empty \`matching_vocabulary\`) | ${enriched.length} of ${behavioral.length} |
| Terms per enriched record — min | ${dist.min} |
| Terms per enriched record — max | ${dist.max} |
| Terms per enriched record — mean | ${dist.mean} |
| Terms per enriched record — median | ${dist.median} |
${enriched.length === 0 ? "\n> ⚠️ **WARNING:** zero behavioral records carry \`matching_vocabulary\` — no enrichment detected.\n" : ""}
The soft authoring guideline is 8–20 terms per record (lives in the ID authoring brief, not the schema); eyeball the distribution above against it.

## Per-\`term_type\` totals (behavioral corpus)

\`credential_term\` and \`issuing_body\` are the credential-readiness hooks and are human-authored only (the candidate seed cannot produce them) — they are the most likely to be under-populated and the single most useful signal for the matching-quality review.

| \`term_type\` | Total terms | Note |
|---|---|---|
${typeRows}

## Per-record term counts

| \`ksa_id\` | Category | Term count |
|---|---|---|
${perRecordRows}

---

*Read-only artifact. No Tier 3 scoring (match strength / proficiency / weight) is computed or stored.*
`;

fs.writeFileSync(REPORT_PATH, report, "utf8");
console.log(`📝  Coverage report written → ${REPORT_PATH}`);

// ---------------------------------------------------------------------------
// Assertion (d): crosswalk-integrity
// ---------------------------------------------------------------------------
console.log("\n── Assertion (d): crosswalk-integrity ─────────────────────────────");

const ID_TOKEN = /^[a-z0-9_]+$/; // ksa_id convention: lowercase ASCII letters, digits, underscores

// Parse contiguous pipe-delimited blocks as markdown tables; for each table locate the column whose
// header denotes the mapped ksa_id (header text contains "ksa_id" after normalizing backticks/case);
// extract referenced ids from that column (split multi-id cells on commas/whitespace); check each against master.
function splitRow(line) {
  let s = line.trim();
  if (s.startsWith("|")) s = s.slice(1);
  if (s.endsWith("|")) s = s.slice(0, -1);
  return s.split("|").map(c => c.trim());
}
function isSeparatorRow(line) {
  return /^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$/.test(line) && line.includes("-");
}
function isTableLine(line) {
  return line.trim().startsWith("|");
}

const crosswalkFiles = globSync(CROSSWALK_GLOB);
const orphans = [];
let tablesWithIdColumn = 0;
let idsChecked = 0;

crosswalkFiles.forEach(file => {
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  let i = 0;
  while (i < lines.length) {
    if (!isTableLine(lines[i])) { i++; continue; }
    // Collect a contiguous table block.
    const start = i;
    const block = [];
    while (i < lines.length && isTableLine(lines[i])) { block.push(lines[i]); i++; }
    if (block.length < 2 || !isSeparatorRow(block[1])) continue; // not a real table

    const header = splitRow(block[0]);
    const idCol = header.findIndex(h => h.replace(/`/g, "").trim().toLowerCase().includes("ksa_id"));
    if (idCol === -1) continue; // no mapped-ksa_id column in this table
    tablesWithIdColumn++;

    for (let r = 2; r < block.length; r++) {
      const cells = splitRow(block[r]);
      if (idCol >= cells.length) continue;
      const cell = cells[idCol].replace(/`/g, "");
      const tokens = cell.split(/[\s,]+/).filter(t => ID_TOKEN.test(t));
      tokens.forEach(tok => {
        idsChecked++;
        if (!idSet.has(tok)) {
          orphans.push({ file: file.replace(/\\/g, "/"), line: start + 1 + r, ksa_id: tok });
        }
      });
    }
  }
});

console.log(`Crosswalk files scanned:   ${crosswalkFiles.length}`);
console.log(`Tables with a ksa_id column: ${tablesWithIdColumn}`);
console.log(`ksa_id references checked:  ${idsChecked}`);
if (orphans.length === 0) {
  console.log("✅  No orphans — every crosswalk-referenced ksa_id exists in master_ksa.json.");
} else {
  hardFail = true;
  console.log(`❌  ${orphans.length} orphan ksa_id reference(s) (referenced in a crosswalk, absent from master_ksa.json):`);
  orphans.forEach(o => console.log(`     • ${o.ksa_id}  —  ${o.file}:${o.line}`));
}

// ---------------------------------------------------------------------------
// Verdict
// ---------------------------------------------------------------------------
console.log("\n───────────────────────────────────────────────────────────────────");
if (hardFail) {
  console.error("❌  validate_matching_vocabulary: FAIL (assertion (b) and/or (d) had violations).");
  process.exit(1);
} else {
  console.log("✅  validate_matching_vocabulary: PASS (b, d clean; c report emitted).");
}
