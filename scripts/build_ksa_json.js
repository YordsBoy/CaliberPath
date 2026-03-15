#!/usr/bin/env node
// scripts/build_ksa_json.js

const fs       = require("fs");
const path     = require("path");
const glob     = require("glob");
const matter   = require("gray-matter");

const SRC_GLOB = "content/Individual_KSAs/**/*.md";     // adjust if you move your MD files
const OUT_DIR  = "data";
const OUT_FILE = path.join(OUT_DIR, "master_ksa.json");

async function build() {
    console.log("🔧  Running build_ksa_json.js");
    console.log("🔍  Looking for Markdown with glob:", SRC_GLOB);

  // 1) Ensure output dir exists (Node ≥10.12)
  fs.mkdirSync(OUT_DIR, { recursive: true });

  // 2) Find all markdown files, excluding README.md files
  const allFiles = glob.sync(SRC_GLOB);
  const files = allFiles.filter(f =>
    path.basename(f).toLowerCase() !== "readme.md" &&
    !f.includes("_crosswalk") &&
    !f.includes("_archive")
  );
  console.log(`📄  Found ${files.length} KSA file(s) (${allFiles.length - files.length} READMEs excluded)`);

  if (!files.length) {
    console.error(`❌  No Markdown found under ${SRC_GLOB}`);
    process.exit(1);
  }

  // 3) Parse each file's front-matter
  const ksas = files.map((filePath) => {
    console.log("   • Parsing", filePath);
    const raw     = fs.readFileSync(filePath, "utf8");
    const parsed  = matter(raw);
    console.log("  parsed.data:", parsed.data);
   
    const data    = parsed.data;
   // map "levels" → "proficiency_levels" to satisfy schema
    if (data.levels) {
     data.proficiency_levels = data.levels;
     delete data.levels;
   }

    // backfill ksa_id if missing
    if (!data.ksa_id) {
        data.ksa_id = path.basename(filePath, ".md")
          .replace(/\s+/g, "_")
          .toLowerCase();
        console.warn(`⚠️  ksa_id missing—set to "${data.ksa_id}"`);
    }

    return data;
  });

  // 4) Write JSON
  fs.writeFileSync(OUT_FILE, JSON.stringify(ksas, null, 2), "utf8");
  console.log(`✅  Built ${ksas.length} KSAs → ${OUT_FILE}`);
}

build().catch((err) => {
  console.error(err);
  process.exit(1);
});
