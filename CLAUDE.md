# CaliberPath — Claude Code Context

## What Is CaliberPath

CaliberPath is a Learning & Development (L&D) company delivering human-led coaching, workshops, and consulting services. The core IP is the **UPLS competency framework** (Professionalism, Leadership & Influence, and Self-Mastery) plus 400+ technical KSAs across 35 industry sectors.

**Author:** YordsBoy | **Version:** 0.1.0 | **License:** UNLICENSED

## Strategic Context

See **[docs/STRATEGIC_DIRECTION.md](docs/STRATEGIC_DIRECTION.md)** for the authoritative development roadmap.

### Phase Summary

| Phase | Timeframe | Status | Focus |
|-------|-----------|--------|-------|
| **Phase 1** — Human-Delivered | 2026-2027 | **CURRENT** | Coaching, workshops, KSA content, documentation |
| **Phase 2** — Technology-Augmented | 2027-2028 | Planned | Digital intake, assessments, client portal |
| **Phase 3** — AI-Native | 2028+ | Deferred | AI companion, memory integration, tone calibration |

### What's Active vs. Deferred

- **ACTIVE (Phase 1):** `content/Individual_KSAs/`, `schemas/`, `scripts/`, `data/`, `docs/`
- **DEFERRED (Phase 3):** `flows/` — the 7-day AI intake and post-intake companion model. Preserve but do not develop.
- **NEEDS REVIEW:** `components/UserTierContext.js`, Stripe integration, `README.md` — built for SaaS model, may need redesign.

## Tech Stack

- **Framework:** Next.js 13.4 (App Router) + React 18
- **Styling:** Tailwind CSS v4
- **Payments:** Stripe (needs reconfiguration from subscription to invoicing)
- **Exports:** html2pdf.js
- **Schema Validation:** AJV (JSON Schema Draft 7)
- **Markdown Parsing:** gray-matter (YAML front-matter)

## Key Commands

```bash
npm run dev              # Next.js dev server
npm run build            # Production build
npm run lint             # ESLint
npm run format           # Prettier format all files
npm run clean            # Remove .next cache
npm run build:ksas       # Generate data/master_ksa.json from KSA markdown files
npm run validate:ksas    # Build + validate KSA schema compliance
npm run inventory:ksas   # Generate KSA inventory report and validation errors
```

## Project Structure

```
content/Individual_KSAs/       # CORE ASSET — 684 KSA markdown files by sector
  professionalism/             #   15 Professionalism competencies
  leadership_influence/        #   15 Leadership competencies
  self_management_personal_mastery/  #   15+ Self-Mastery competencies
  technical_ksas/              #   Sector-specific KSAs (35 sectors)
schemas/ksa.schema.json        # KSA validation schema
scripts/build_ksa_json.js      # Compiles KSAs → data/master_ksa.json
scripts/validate_ksas.js       # Schema validation
scripts/inventory_ksas.js      # Generates inventory reports
data/master_ksa.json           # Compiled KSA output (regenerate with build:ksas)
docs/policies/                 # Governing policies (ASSESSMENT_FRAMEWORK_POLICY, KSA_CHANGE_MANAGEMENT_PROTOCOL)
docs/architecture/             # System architecture
HORIZON_POLICY.md              # Horizon tier governance
flows/                         # DEFERRED — Phase 3 AI companion content
```

---

## KSA Change Management

### ⚠️ Read This First

**Before modifying any file in `content/Individual_KSAs/`, read:**
```
docs/policies/KSA_CHANGE_MANAGEMENT_PROTOCOL.md
```

This REPO-native document contains the full operational protocol for KSA changes: the six-criterion review, field-by-field guidance for all 11 KSA fields, the REPO-internal downstream impact matrix, OI-09 specific requirements, and the quick-reference execution checklist.

The master protocol with full authorization rules and OPSDIR downstream impact is at:
```
C:\Users\rofam\OneDrive\Desktop\GET IT\CaliberPath\01_Strategic_Documents\AI_Operations\
  2026-03-17_CaliberPath_KSA_Change_Management_Protocol_v1.md
```

The current session's authorized changes are documented in OI entries in the Stream 4 Instrument Design Log:
```
C:\Users\rofam\OneDrive\Desktop\GET IT\CaliberPath\04_Deliverables\Curricula\
  2026-03-16_CaliberPath_Stream4_InstrumentDesignLog_v1.md
```

### Write Authority

**Claude Code is the ONLY agent authorized to write, modify, or delete files in `content/Individual_KSAs/`.** No Claude.ai Project writes directly to this directory.

**Do NOT modify `content/Individual_KSAs/` without explicit written authorization** from a Strategist Decision Memo or OI entry. If no authorization exists for a requested change, stop and surface it to the founder before proceeding.

### KSA File Structure

Every KSA is a Markdown file with YAML front-matter.

**Required fields:** `ksa_id`, `label`, `category`, `description`, `sector`, `horizon`, `proficiency_levels`

**Optional fields (operationally required):** `cluster_tags`, `source_frameworks`, `adjacent_sectors`, `transfer_populations`

Key field constraints:
- `ksa_id` must match the regex pattern `^[a-z0-9_]+$` and **exactly match the filename** (basename without `.md`)
- `sector` must be one of the 36 enum values in `schemas/ksa.schema.json` (35 named sectors + `cross_sector`)
- `horizon` must be one of: `core`, `emerging`, `perennial`, `watch_2030`, `peripheral`, `legacy` — governed by `HORIZON_POLICY.md`
- `cluster_tags` values must be from the Controlled Vocabulary v1.0 — no freeform tags permitted:
  ```
  C:\Users\rofam\OneDrive\Desktop\GET IT\CaliberPath\01_Strategic_Documents\
    2026-03-15_CaliberPath_ClusterTags_ControlledVocabulary_v1.md
  ```
- `adjacent_sectors` values must match the `sector` enum
- `transfer_populations` valid values: `military_transition`, `healthcare_pivot`, `early_career`, `mid_career_change`, `returning_workforce`, `education_to_industry`, `veteran_spouse`, `career_explorer`
- Each proficiency level object requires `level` and `indicator`
- Indicators must describe observable, non-inferential behaviors — no "understands", "appreciates", "is aware of", or trait/disposition language

### Build Chain (run all three in order after every KSA change)

```bash
npm run build:ksas       # Rebuild data/master_ksa.json from all KSA markdown files
npm run validate:ksas    # Schema validation — must return ZERO errors before closing session
npm run inventory:ksas   # Regenerate reports/ksa_inventory.json, ksa_inventory_report.md, validation_errors.json
```

A successful `write_file` return does **not** guarantee valid content. `npm run validate:ksas` is the authority. All three scripts must pass before the session closes.

### cluster_tags and the Adjacency Matrix

`cluster_tags` is the sole computational input to the sector adjacency matrix, which drives career pathway coaching tools and Phase 2 learning path generation. Any `cluster_tags` change requires:

1. Run the full build chain (all three scripts)
2. Recompute adjacency scores for the affected sector pair(s) using the methodology in `content/Individual_KSAs/technical_ksas/_crosswalk/sector_adjacency_matrix.md`
3. Update `sector_adjacency_matrix.md` if any sector pair score changes by one tier or more (e.g., MEDIUM → HIGH, or LOW → NONE)
4. Update the affected sector README Transfer Pathways section(s)

---

## Development Principles

**DO:**
- Maintain and expand KSA content
- Build tools that support human-delivered services
- Create documentation that codifies methodology
- Design with Phase 2 in mind (digital intake, assessments)

**DO NOT:**
- Invest development time in AI companion features (Phase 3)
- Build SaaS subscription infrastructure
- Treat `flows/` as a current priority
- Develop features that bypass human coaches

## Git Conventions

- Branch naming: `feature/your-feature-name`
- One feature/fix per branch
- Commit messages: short, imperative ("Add onboarding walkthrough")
- Always pull before editing
- See `docs/caliberpath-git-manual.md` for full guidelines

## Changelog

- 2026-04-01 (v1.2): Renamed domain directory from universal_professional/ to professionalism/ and updated all 15 category fields. Updated framework name expansion in What Is CaliberPath and Project Structure. Authority: DR_DomainNaming_Professionalism_Correction_v1.
- 2026-03-17 (v1.1): Replaced thin "KSA Authoring Rules" with comprehensive "KSA Change Management" section. Added protocol references (`docs/policies/KSA_CHANGE_MANAGEMENT_PROTOCOL.md` and OPSDIR master). Added write authority rule. Added three-script build chain (`build:ksas`, `validate:ksas`, `inventory:ksas`). Added cluster_tags/adjacency matrix obligation. Added `npm run inventory:ksas` to Key Commands. Updated KSA count from "400+" to 684 in Project Structure. Added `docs/policies/` and `HORIZON_POLICY.md` to Project Structure listing.
- 2026-02-xx (v1.0): Initial configuration.
