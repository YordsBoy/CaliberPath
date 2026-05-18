# CaliberPath — Claude Code Context

## What Is CaliberPath

CaliberPath is a Learning & Development (L&D) company delivering human-led coaching, workshops, and consulting services. The core IP is the **UPLS competency framework** (Professionalism, Leadership & Influence, and Self-Mastery) plus 691 technical KSAs across 35 active industry sectors.

> **KSA inventory:** 691 technical KSAs distributed across 35 active industry sectors at the `content/Individual_KSAs/technical_ksas/` substrate. The schema `sector.enum` totals 36 values — 35 industry sectors + 1 `cross_sector` meta-classification reserved for cross-cutting KSAs spanning multiple sectors. Reconciled at v1.5 from v1.4's "36 industry sectors" framing per Strategist Path C empirical investigation 2026-05-17 (LSA v4.76 governing; founder Tier 1 architectural disposition on schema cleanup).

**Author:** YordsBoy | **Version:** 0.1.0 | **License:** UNLICENSED

## Strategic Context

See **[docs/STRATEGIC_DIRECTION.md](docs/STRATEGIC_DIRECTION.md)** for the authoritative development roadmap.

Under the Hybrid repository architecture (DR_WebPlatform_RepoArchitecture_v1, 2026-04-24, registered LSA v4.17), this repo (KSA-REPO) becomes the application surface at `app.caliberpath.com`. The Digital-First Decision Memo (2026-04-20) pulled the application phase forward from 2027–2028 to 2026 Q2–Q3, replacing the previous three-phase roadmap with the four-phase framework below.

### Phase Summary

| Phase | Timeframe | Status | Focus |
|-------|-----------|--------|-------|
| **Phase 1** — Content & Pipeline Foundation | 2026 (now) | **CURRENT — Phase 1B (Dual-Market Validation) operational** | KSA content authoring, schemas, documentation, ReportLab pipeline integration preparation; WS-CIG-UPLS-DRIFT-REVIEW lifecycle (Phases 0–3 closed 2026-05-15; Phase 4 active under Info/Tech substrate authority; Phase 5 MARCOM Brand Review forthcoming); Phase 3 Production Cycle in flight (graduated batching architecture; sector 1 `admin_support` canonical; sector 2 `digital_content_creation` iter3 close + canonicalization in flight) |
| **Phase 2** — Application Surface (pulled forward) | 2026 Q2–Q3 | **NEAR-TERM CRITICAL PATH** — scaffolding sequenced after Web Platform Architecture Specification + Layer 3 integration path + Supabase schema design decisions (two residual deferred decisions per LSA v4.74) | `app.caliberpath.com`: intake, assessment, payment ($97 automated tier), delivery dashboard, Layer 3 rendering integration |
| **Phase 3** — AI-Assisted Tier | 2026 Q3–Q4 | Planned — OI-GAR-V2-IMPL workstream **COMPLETE** 2026-05-01 (Layer 2 architecture committed); $197 AI-assisted tier launch pending Phase 2 application surface scaffolding | $197 AI-assisted tier; Layer 2 integration via OI-GAR-V2; coach-portal surfaces |
| **Phase 4** — Scale & Expansion | Longer-term | Future | B2B aggregate tier; geographic expansion templating; advanced analytics |

### What's Active vs. Deferred

- **ACTIVE (Phase 1):** `content/Individual_KSAs/`, `schemas/`, `scripts/`, `data/`, `docs/`. WS-CIG-UPLS-DRIFT-REVIEW workstream contribution scope (KSA-REPO content substrate read scope for Phase 4 verification deliverable; admin_support cascade dual-attested PREVENTIVE-NULL at upstream substrate per 2026-05-15 close). Phase 3 Production Cycle scope (CIG markdown source authoring at OPSDIR `Sector_Modules\` layer — CC author-direct, NOT KSA-REPO content writes).
- **NEAR-TERM (Phase 2 — pulled forward):** Next.js application surface at `app.caliberpath.com` — intake, assessment, $97 automated-tier payment, delivery dashboard, Layer 3 rendering integration. Scaffolding work is sequenced after the full Web Platform Architecture Specification is filed AND the two residual deferred decisions registered at LSA v4.74 (Layer 3 integration path; Supabase schema design) are resolved; do not begin implementation until those gates clear.
- **PRESERVED:** `flows/` — the 7-day AI intake and post-intake companion model originated under the prior AI-first conception. Preserve as reference; reassess against the four-phase framework when Phase 3 (AI-assisted tier) work begins.
- **NEEDS REVIEW:** `components/UserTierContext.js`, Stripe integration, `README.md` — built for the prior subscription-SaaS framing. Under Option C the repo IS becoming an application (Next.js), but not "SaaS" in the subscription sense — payment is per-tier ($97 automated, $197 AI-assisted), not recurring subscription. These components likely need redesign for the tier-purchase model.

### Substrate-Tier Architectural Distinction (UPLS-01 Canonical Labels)

Per LSA v4.74 Part X observation d, three substrate tiers carry UPLS-01 career-track priority mappings and other canonical-label-bearing scope. The tiers are **upstream-orthogonal at current operational maturity** — labels DO NOT automatically propagate between them. Each substrate must independently consult the canonical UPLS-01 authority (Decision Records governing UPLS-01 + career-track priority mappings) at authoring time.

1. **OPSDIR `Sector_Modules\` CIG markdown layer** — CC author-direct at OPSDIR `08_Production_Pipeline\Sector_Modules\` (or equivalent path). **Operative substrate at Phase 3 maturity** for UPLS-01 career-track priority mappings. ID authors CIG Full markdown source per CIG Full Source-Authoring Guidance; CC executes downstream rendering pipeline.

2. **KSA-REPO content substrate (`content/Individual_KSAs/`)** — CC exclusive write authority per existing governance. **Currently empty of UPLS-01 career-track priority mappings** (cascade preventive-null upstream of CIG markdown layer at Phase 3 maturity, per 2026-05-15 WS-CIG-UPLS-DRIFT-REVIEW dual-attested close). Upstream-orthogonal to the CIG markdown layer: KSA-REPO content does NOT inherit Phase 3 sector-module cluster-pattern decisions.

3. **Phase 2 application surface (forthcoming `app.caliberpath.com`)** — Next.js application surface forthcoming. **Canonical-from-inception locus** — SHOULD encode canonical UPLS-01 labels at scaffolding time, NOT retrofit later. Phase 2 scaffolding sessions must consult the canonical UPLS-01 label authority directly; do not assume Phase 3 CIG markdown sector-module labels are applicable.

**Operational significance:** Phase 2 scaffolding sessions risk cross-substrate label drift if they assume Phase 3 CIG markdown labels are canonical for the application surface. Both substrates must independently consult the canonical UPLS-01 authority.

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
content/Individual_KSAs/       # CORE ASSET — 691 KSA markdown files by sector
  professionalism/             #   15 Professionalism competencies
  leadership_influence/        #   15 Leadership competencies
  self_management_personal_mastery/  #   15+ Self-Mastery competencies
  technical_ksas/              #   Sector-specific KSAs (35 active sectors)
schemas/ksa.schema.json        # KSA validation schema
scripts/build_ksa_json.js      # Compiles KSAs → data/master_ksa.json
scripts/validate_ksas.js       # Schema validation
scripts/inventory_ksas.js      # Generates inventory reports
data/master_ksa.json           # Compiled KSA output (regenerate with build:ksas)
docs/policies/                 # Governing policies (ASSESSMENT_FRAMEWORK_POLICY, KSA_CHANGE_MANAGEMENT_PROTOCOL)
docs/architecture/             # System architecture
HORIZON_POLICY.md              # Horizon tier governance
flows/                         # PRESERVED — pre-revision AI companion content; reassess at Phase 3
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
- `sector` must be one of the 36 enum values in `schemas/ksa.schema.json` (35 named industry sectors + `cross_sector`)
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
- Maintain and expand KSA content (Phase 1 core)
- Prepare schemas, content structure, and data outputs for ReportLab pipeline integration
- Create documentation that codifies methodology
- Design content and data outputs so Phase 2 (intake, assessment, $97 automated tier) can consume them directly

**DO NOT:**
- Begin Next.js application scaffolding for `app.caliberpath.com` until the full Web Platform Architecture Specification is filed
- Build subscription-SaaS billing infrastructure — Phase 2 payment is per-tier purchase ($97 automated, $197 AI-assisted), not recurring subscription
- Treat `flows/` as current Phase 2 work — it predates the four-phase revision and will be reassessed at Phase 3
- Develop features that bypass the human coach surface in Phase 1 deliveries

## Git Conventions

- Branch naming: `feature/your-feature-name`
- One feature/fix per branch
- Commit messages: short, imperative ("Add onboarding walkthrough")
- Always pull before editing
- See `docs/caliberpath-git-manual.md` for full guidelines

## Changelog

- 2026-05-17 (v1.5): Sector count reconciliation. Reverts v1.4's "36 industry sectors" framing → **"35 active industry sectors"** (at lines 5, 72, and 125 of the v1.4 baseline). Adds an inline KSA inventory clarification block under §"What Is CaliberPath" registering the 35 active sectors at filesystem substrate vs. 36 schema-enum values (35 industry + `cross_sector` meta-classification). Authority: Strategist→CC handoff `2026-05-17_Strategist-to-CC_KSARepo_SectorCountReconciliation_CLAUDEmd_v15_v1`; LSA v4.76; founder Tier 1 architectural disposition on schema cleanup. **Substantive reasoning correction:** v1.4 (commit `8c26526`) reasoned that the 36th industry sector was `digital_content_creation_creator_economy`, inferring "post-addition state" from operational context. Strategist Path C empirical investigation (2026-05-17) established that `digital_content_creation_creator_economy` IS fully populated at the active substrate, and that the actually-unmatched enum value is `skilled_trades` — an architectural artifact slated for removal per founder canonical ("those skills/competencies are embedded in their respective sectors, vice the catch-all theme of skilled trades"). The schema enum cleanup removing `skilled_trades` is executed in a sibling commit. **Discipline candidate registered (advisory):** Substrate-Empirical-Verification-Before-Inference — when substrate count discrepancies surface across operational context vs. canonical substrate, empirical verification at the relevant substrate (filesystem listing for content presence; schema inspection for enum scope) precedes any inference-based reconciliation.
- 2026-05-15 (v1.4): Phase 1B operational picture revision. Empirical numeric reconciliation: KSA count 684 → 691 (schema-valid figure from `npm run inventory:ksas`; 3 schema-invalid `_crosswalk/` documentation artifacts excluded), industry sector count 35 → 36 (37 enum values including `cross_sector`; reflects post-`digital_content_creation_creator_economy`-addition schema state). Phase Summary updated: Phase 1 row marked "Phase 1B (Dual-Market Validation) operational" with WS-CIG-UPLS-DRIFT-REVIEW lifecycle + Phase 3 Production Cycle in flight; Phase 2 row notes Layer 3 integration path + Supabase schema design as residual deferred decisions per LSA v4.74; Phase 3 row notes OI-GAR-V2-IMPL workstream COMPLETE 2026-05-01. What's Active vs. Deferred updated with WS-CIG-UPLS-DRIFT-REVIEW contribution scope + Phase 3 Production Cycle OPSDIR-layer-not-KSA-REPO clarification. Added new "Substrate-Tier Architectural Distinction (UPLS-01 Canonical Labels)" subsection under Strategic Context per LSA v4.74 Part X observation d (three-tier substrate architecture: OPSDIR CIG markdown layer / KSA-REPO content substrate / Phase 2 application surface; upstream-orthogonal at current maturity). Authority: Strategist → CC handoff `2026-05-15_Strategist-to-CC_KSARepo_CLAUDEmd_Phase1B_Operational_Picture_Revision_v1` (WS-PI-OPERATIONAL-PICTURE-REVISION, LSA v4.74).
- 2026-04-24 (v1.3): Revised Phase framework from three-phase (2026–2028+) to four-phase model. Phase 2 (application surface at `app.caliberpath.com`) pulled forward from 2027–2028 to 2026 Q2–Q3 per Digital-First Decision Memo (2026-04-20) and Hybrid architecture decision DR_WebPlatform_RepoArchitecture_v1 (2026-04-24, registered LSA v4.17). Updated Phase Summary table, Active/Deferred section, Project Structure flows/ note, and Development Principles. Qualified "SaaS" framing — repo IS becoming a Next.js application but with per-tier purchase, not subscription billing. Authority: Strategist → CC handoff 2026-04-24_Strategist-to-CC_KSARepo_CLAUDEmd_PhaseFrameworkRevision_v1.
- 2026-04-01 (v1.2): Renamed domain directory from universal_professional/ to professionalism/ and updated all 15 category fields. Updated framework name expansion in What Is CaliberPath and Project Structure. Authority: DR_DomainNaming_Professionalism_Correction_v1.
- 2026-03-17 (v1.1): Replaced thin "KSA Authoring Rules" with comprehensive "KSA Change Management" section. Added protocol references (`docs/policies/KSA_CHANGE_MANAGEMENT_PROTOCOL.md` and OPSDIR master). Added write authority rule. Added three-script build chain (`build:ksas`, `validate:ksas`, `inventory:ksas`). Added cluster_tags/adjacency matrix obligation. Added `npm run inventory:ksas` to Key Commands. Updated KSA count from "400+" to 684 in Project Structure. Added `docs/policies/` and `HORIZON_POLICY.md` to Project Structure listing.
- 2026-02-xx (v1.0): Initial configuration.
