#!/usr/bin/env node
// scripts/export_upls_reference.js
//
// Exports all 45 UPLS competencies (Professionalism, Leadership & Influence, Self-Mastery)
// to a .docx reference document for Handbook integration.
//
// Output: docs/UPLS_Competency_Reference.docx
//
// Usage: node scripts/export_upls_reference.js

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
} = require("docx");
const fs   = require("fs");
const path = require("path");
const yaml = require("js-yaml");

// ── Config ────────────────────────────────────────────────────────────────────
const ROOT = path.resolve(__dirname, "..");

const SECTIONS = [
  {
    title: "Professionalism Competencies (15)",
    subtitle: "Foundational skills for all professionals regardless of industry or role.",
    dir: "content/Individual_KSAs/professionalism",
  },
  {
    title: "Leadership & Influence Competencies (15)",
    subtitle: "Skills for leading people and driving outcomes in any organization.",
    dir: "content/Individual_KSAs/leadership_influence",
  },
  {
    title: "Self-Mastery Competencies (15)",
    subtitle: "Internal capabilities for personal excellence and well-being.",
    dir: "content/Individual_KSAs/self_management_personal_mastery",
  },
];

// ── Helpers ───────────────────────────────────────────────────────────────────
function parseKSAFile(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  try {
    return yaml.load(match[1]);
  } catch (e) {
    console.error(`  ⚠ YAML parse error in ${path.basename(filePath)}: ${e.message}`);
    return null;
  }
}

function collectKSAs(dir) {
  const absDir = path.join(ROOT, dir);
  if (!fs.existsSync(absDir)) {
    console.warn(`  ⚠ Directory not found: ${dir}`);
    return [];
  }
  const ksas = [];
  const walk = (d) => {
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (entry.name.endsWith(".md") && entry.name.toLowerCase() !== "readme.md") {
        const ksa = parseKSAFile(full);
        if (ksa && ksa.label) ksas.push(ksa);
      }
    }
  };
  walk(absDir);
  return ksas.sort((a, b) => a.label.localeCompare(b.label));
}

function border(color = "CCCCCC") {
  return { style: BorderStyle.SINGLE, size: 1, color };
}
const BORDERS = { top: border(), bottom: border(), left: border(), right: border() };

function proficiencyTable(levels) {
  const headerRow = new TableRow({
    children: [
      new TableCell({
        borders: BORDERS,
        width: { size: 1500, type: WidthType.DXA },
        shading: { fill: "E8E8E8", type: ShadingType.CLEAR },
        children: [new Paragraph({ children: [new TextRun({ text: "Level", bold: true, size: 20 })] })],
      }),
      new TableCell({
        borders: BORDERS,
        width: { size: 7860, type: WidthType.DXA },
        shading: { fill: "E8E8E8", type: ShadingType.CLEAR },
        children: [new Paragraph({ children: [new TextRun({ text: "Behavioral Indicator", bold: true, size: 20 })] })],
      }),
    ],
  });

  const dataRows = (levels || []).map(
    (lvl) =>
      new TableRow({
        children: [
          new TableCell({
            borders: BORDERS,
            width: { size: 1500, type: WidthType.DXA },
            children: [new Paragraph({ children: [new TextRun({ text: lvl.level || "", bold: true, size: 20 })] })],
          }),
          new TableCell({
            borders: BORDERS,
            width: { size: 7860, type: WidthType.DXA },
            children: [new Paragraph({ children: [new TextRun({ text: lvl.indicator || "", size: 20 })] })],
          }),
        ],
      })
  );

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1500, 7860],
    rows: [headerRow, ...dataRows],
  });
}

function spacer() {
  return new Paragraph({ children: [] });
}

// ── Build ─────────────────────────────────────────────────────────────────────
async function buildDocument() {
  const children = [];

  // Cover
  children.push(
    new Paragraph({
      heading: HeadingLevel.TITLE,
      children: [new TextRun({ text: "UPLS Competency Reference", bold: true, size: 48 })],
    }),
    new Paragraph({
      children: [new TextRun({ text: "Professionalism, Leadership & Influence, and Self-Mastery Framework", italics: true, size: 24 })],
    }),
    new Paragraph({
      children: [new TextRun({ text: `Generated: ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}`, size: 20 })],
    }),
    spacer()
  );

  for (const section of SECTIONS) {
    const ksas = collectKSAs(section.dir);
    console.log(`  ${section.title}: ${ksas.length} KSAs found`);

    children.push(
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun({ text: section.title, bold: true })],
      }),
      new Paragraph({ children: [new TextRun({ text: section.subtitle, italics: true })] }),
      spacer()
    );

    for (const ksa of ksas) {
      children.push(
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun({ text: ksa.label, bold: true })],
        }),
        new Paragraph({
          children: [new TextRun({ text: (ksa.description || "No description available.").trim(), size: 22 })],
        })
      );

      if (ksa.proficiency_levels && ksa.proficiency_levels.length) {
        children.push(proficiencyTable(ksa.proficiency_levels));
      }

      children.push(spacer());
    }
  }

  children.push(
    new Paragraph({
      children: [
        new TextRun({
          text: "© CaliberPath L&D. Competencies adapted from public-domain frameworks including U.S. OPM, O*NET (CC BY 4.0), and WEF. No source organization endorses these adaptations.",
          italics: true,
          size: 18,
        }),
      ],
    })
  );

  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: "Arial", size: 24 } },
      },
    },
    sections: [
      {
        properties: {
          page: {
            size: { width: 12240, height: 15840 },
            margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          },
        },
        children,
      },
    ],
  });

  const outPath = path.join(ROOT, "docs", "UPLS_Competency_Reference.docx");
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outPath, buffer);
  console.log(`\n✅  Created: docs/UPLS_Competency_Reference.docx  (${(buffer.length / 1024).toFixed(1)} KB)`);
}

buildDocument().catch((err) => {
  console.error("❌ Export failed:", err);
  process.exit(1);
});
