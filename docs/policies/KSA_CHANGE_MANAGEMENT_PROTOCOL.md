# CaliberPath — KSA Change Management Protocol
## Claude Code Operational Reference

**Version:** 1.0 (REPO copy — adapted for Claude Code execution context)
**Date:** 2026-03-17
**Master document (full detail):**
```
C:\Users\rofam\OneDrive\Desktop\GET IT\CaliberPath\01_Strategic_Documents\AI_Operations\
  2026-03-17_CaliberPath_KSA_Change_Management_Protocol_v1.md
```
This document is the Claude Code-facing operational reference. It contains the full six-criterion review, field-by-field guidance, execution sequence, and checklist — adapted to Claude Code's role as the sole execution agent for REPO writes. Authorization, OPSDIR document updates, and Project-level decision records are handled by the Claude.ai Projects (Strategist, Instructional Designer), not by Claude Code.

---

## WRITE AUTHORITY RULE

**Claude Code is the ONLY agent authorized to write, modify, or delete files within `content/Individual_KSAs/`.** No Claude.ai Project (Strategist, Instructional Designer, MARCOM, Operations & QA, Info/Tech) writes directly to this directory. This is an architectural hard boundary.

**Claude Code does NOT modify `content/Individual_KSAs/` without explicit written authorization.** Authorization takes the form of a Strategist Decision Memo or OI (Open Item) entry in the Stream 4 Instrument Design Log. If no written authorization exists for a change, stop and request it before proceeding.

---

## CHANGE TYPES

| Type | Definition |
|---|---|
| **Create** | New KSA file; new sector subdirectory |
| **Revise Minor** | Citation format, behavioral language refinement, horizon update, cluster_tag normalization |
| **Revise Substantive** | label, ksa_id, description rewrite, indicator rewrite, sector change, cluster_tag addition/removal |
| **Delete** | File removal from repository |

All four types require the full protocol. There is no abbreviated path.

---

## THE SIX-CRITERION REVIEW (C1–C6)

Every KSA file — whether newly created or revised — must pass all six criteria before Claude Code writes any content to the repository.

| # | Code | Criterion | Failure Mode |
|---|---|---|---|
| 1 | **C1** | **Behavioral language** — Every indicator at every proficiency level describes an observable, non-inferential behavior a third party could confirm without asking about intentions or internal experience. Prohibited verbs: "understands", "appreciates", "knows", "recognizes the importance of", "is familiar with", "is aware of". Prohibited framing: trait language ("is organized"), disposition language ("values learning"), mental state language ("feels confident"). | Rewrite indicator to describe an observable behavioral action |
| 2 | **C2** | **Source citation format** — Every `source_frameworks` entry is a full proper citation: Author/Organization, Full Document Title, Publishing Body (if different), Year, and access/license notes. No abbreviations, shortcodes (`authority:standard`), bare organization names, or bare standard numbers. | Expand to full citation |
| 3 | **C3** | **Horizon accuracy** — The `horizon` value is consistent with the KSA's actual adoption/maturity profile per `HORIZON_POLICY.md`. | Propose revised horizon with evidence |
| 4 | **C4** | **Source currency** — Every cited source is the current, live version. No archived standards, superseded guidelines, or broken URLs. | Identify and substitute current version |
| 5 | **C5** | **Copyright/trademark integrity** — No indicator language reproduces verbatim text from proprietary frameworks (SHRM BASK, PMI competency content, ICF competencies, proprietary certification body materials). All sources are public domain, CC-licensed, or referenced for conceptual alignment only. | Rewrite using public domain analogues |
| 6 | **C6** | **No proprietary tool/platform names in indicators** — Use generic functional language ("uses a project tracking system") not commercial product names ("uses Jira"). Exception: when the named tool IS the industry standard (e.g., Epic EHR in healthcare informatics) — document the exception explicitly. | Replace with generic functional language |

---

## FIELD-BY-FIELD GUIDANCE

### `ksa_id` (Required)
- Pattern: `^[a-z0-9_]+$`
- **Must exactly match the filename** (basename without `.md` extension)
- Changing a `ksa_id` requires renaming the file; search all OPSDIR documents for the old `ksa_id` before renaming (Projects handle the OPSDIR updates)
- Confirm no existing file shares this `ksa_id` by checking `data/master_ksa.json`

### `label` (Required)
- Free string; used as the human-readable display name in coaching materials and instruments
- Changes cascade to: sector README KSA inventory table; Stream 4 instruments that reference this label; `docs/reference/` individual/institutional reference documents
- Projects update OPSDIR instruments; Claude Code updates REPO documents (README, `docs/reference/`)

### `category` (Required)
- Established values: "Technical", "Professionalism", "Leadership & Influence", "Self-Mastery"
- A category change typically requires moving the file to a different directory
- UPLS domain reclassification (into Professionalism/Leadership & Influence/Self-Mastery) brings the file under the UPLS Readiness Report gate — requires Strategist authorization before Claude Code proceeds
- **Domain name correction (2026-04-01):** "Universal Professional" was renamed to "Professionalism" across all REPO files per DR_DomainNaming_Professionalism_Correction_v1. The REPO directory is now at content/Individual_KSAs/professionalism/. All 15 category fields updated. Authority: OI-DOMAIN-01 Tier 3 (git f19791c).

### `description` (Required)
- 1–3 sentence domain scope statement
- Apply C1 (behavioral, factual) and C5 (no proprietary language)
- Update sector README if description appears there

### `sector` (Required)
- Must be one of the 36 enum values in `schemas/ksa.schema.json`
- A sector change requires: (1) moving the file to the matching directory, (2) updating both the old and new sector READMEs, (3) adjacency matrix recomputation
- `sector` field value must match the directory exactly

### `horizon` (Required)
- Enum values: `core`, `emerging`, `watch_2030`, `perennial`, `peripheral`, `legacy`
- Governed by `HORIZON_POLICY.md` (REPO root) — promotion/demotion gates defined there
- `watch_2030` → `emerging` for quantum_tech cluster files triggers OI-07 (Strategist evaluates AI-MOD-01 absorption) — flag before executing
- Run C3 check on every horizon field

### `proficiency_levels` (Required — highest-stakes field)
- Array of five objects: Awareness, Basic, Intermediate, Advanced, Expert
- **Any change to an indicator in a certified KSA that has been instrumented requires Strategist authorization AND triggers a corresponding update to every Stream 4 instrument that contains that indicator** (Projects handle instrument updates; Claude Code handles REPO write)
- Apply C1 rigorously — every indicator must describe an observable behavioral action
- Apply C6 — no proprietary platform names
- **OI-09 specific:** All 35 indicators (5 levels × 7 files) are FR-09-xx and require individual founder approval before Claude Code writes any file. Wait for complete founder sign-off on all 35 before executing any write.

**Source authority references in indicators (added 2026-03-17):** Named authorities (CDC, ANA, ISMP, Joint Commission, OSHA, CMS, etc.) belong in `source_frameworks` only — not in indicator text. Indicators at Awareness, Basic, and Intermediate must use generalized behavioral language: "consistent with current evidence-based practice," "per applicable clinical standards," "following institutional protocol." Exception: at Advanced and Expert levels, naming an authority is appropriate only when direct engagement with that authority — evaluating, aligning, influencing, leading accreditation — is itself the observable behavior. Industry-standard behavioral terms (SBAR, Standard Precautions, PDSA, chain of command) are not authority citations and may appear at any level. Full rationale: master protocol Section 5.7.

### `cluster_tags` (Optional — but operationally required; highest adjacency impact)
- **All values must be from the Controlled Vocabulary v1.0:**
  ```
  C:\Users\rofam\OneDrive\Desktop\GET IT\CaliberPath\01_Strategic_Documents\
    2026-03-15_CaliberPath_ClusterTags_ControlledVocabulary_v1.md
  ```
- No freeform tags. If a needed tag isn't in the vocabulary, route to Strategist for vocabulary amendment before authoring.
- Any cluster_tag change triggers adjacency matrix recomputation:
  1. Run `npm run build:ksas` after writing the file
  2. Recompute the adjacency matrix (T-CROSSWALK-01 methodology in `_crosswalk/sector_adjacency_matrix.md`)
  3. Compare old vs new scores for affected sector pairs
  4. Update `_crosswalk/sector_adjacency_matrix.md` if any pair changes by one tier or more
  5. Update affected sector README Transfer Pathways sections
  6. Projects review and update `_crosswalk/population_pathways/` documents if needed

### `source_frameworks` (Optional — but operationally required)
- Apply C2 (full proper citations), C4 (current versions), C5 (IP integrity)
- For OI-09 clinical KSAs: cite open-access government/professional publications only (QSEN, ANA, NCLEX NGN, CDC, OSHA, CMS, Joint Commission)
- Minimum 1–3 authoritative sources per KSA

### `adjacent_sectors` (Optional)
- All values must be from the same 36-value enum as `sector`
- KSA-level annotation only — does not affect adjacency matrix computation
- No required downstream document updates from this field alone

### `transfer_populations` (Optional)
- Enum values: `military_transition`, `healthcare_pivot`, `early_career`, `mid_career_change`, `returning_workforce`, `education_to_industry`, `veteran_spouse`, `career_explorer`
- No instrument or adjacency impact — coaching intake signal only

---

## EXECUTION SEQUENCE

### Phase 1 — Pre-Execution Verification
1. Confirm written authorization exists (Strategist OI or Decision Memo) — if absent, stop
2. Read the full KSA file(s) immediately before writing — never write from memory
3. Complete C1–C6 review for every file in scope; document any flags
4. For `cluster_tags` changes: run `npm run build:ksas` to establish pre-change adjacency baseline
5. Check `data/master_ksa.json` to confirm no existing KSA shares the new `ksa_id`
6. For OI-09: confirm all FR-09-xx items are founder-approved before proceeding

### Phase 2 — REPO Execution
7. Write/edit/delete file(s) via filesystem tools
8. **Post-write read-back**: read each modified file to confirm content is correct
9. Verify file size via `list_directory_with_sizes` — size must be consistent with content added
10. Run `npm run build:ksas` — rebuild `data/master_ksa.json`
11. Run `npm run validate:ksas` — **must return zero errors before proceeding**
12. Run `npm run inventory:ksas` — regenerates `reports/ksa_inventory.json`, `reports/ksa_inventory_report.md`, `reports/validation_errors.json`

### Phase 3 — REPO-Internal Downstream Updates
13. **Sector README(s)** — update KSA inventory table row(s); update Transfer Pathways section if adjacency scores changed
14. **`_crosswalk/sector_adjacency_matrix.md`** — recompute and update if `cluster_tags` changed
15. **`docs/reference/ksas-individual/` and `docs/reference/ksas-institutional/`** — update if UPLS KSA labels or descriptions changed
16. **`_crosswalk/population_pathways/`** — flag for Projects to review if adjacency scores affecting Fort Gordon MOS profiles or domain pathways changed

### Phase 4 — Sign-Off
17. Confirm all validation scripts pass (zero errors)
18. Confirm all REPO-internal documents updated
19. Commit to Git with descriptive message per `docs/caliberpath-git-manual.md`
20. Projects handle OPSDIR document updates (Technical KSA Review Master Index, Stream 4 Design Log, instrument files, handoffs) — Claude Code does not update OPSDIR documents

---

## REPO-INTERNAL DOWNSTREAM IMPACT MATRIX

For every change type, these REPO documents must be reviewed and updated as indicated.

| REPO Document | Create | Revise Minor | Revise Substantive | Delete |
|---|---|---|---|---|
| `data/master_ksa.json` | **Required** — `npm run build:ksas` | **Required** | **Required** | **Required** |
| `reports/` (3 files) | **Required** — `npm run inventory:ksas` | Conditional | **Required** | **Required** |
| `reports/validation_errors.json` | **Required** — `npm run validate:ksas` | **Required** | **Required** | **Required** |
| `[sector]/README.md` — KSA Inventory table | **Required** | Conditional (label/description) | **Required** if label, description, or horizon changes | **Required** |
| `[sector]/README.md` — Transfer Pathways | **Required** if cluster_tags affect adjacency | Not required | **Required** if cluster_tags change | **Required** |
| `_crosswalk/sector_adjacency_matrix.md` | **Required** if cluster_tags added | Not required | **Required** if cluster_tags change | **Required** |
| `_crosswalk/population_pathways/` | Flag for Projects if adjacency changes | Not required | Flag for Projects if adjacency changes | Flag for Projects |
| `docs/reference/ksas-individual/` (3 files) | **Required** for UPLS creates | Conditional | **Required** if label/description changes (UPLS) | **Required** for UPLS |
| `docs/reference/ksas-institutional/` (3 files) | Conditional | Conditional | Conditional | Conditional |

**OPSDIR document updates** (Technical KSA Review Master Index, Stream 4 Design Log, instrument files, Sector Coverage Map, active handoffs) are handled by the **Instructional Designer and Strategist Projects**, not by Claude Code.

---

## OI-09 SPECIFIC REQUIREMENTS

**Authorized files:** 7 new KSA files in a new subdirectory:
```
content/Individual_KSAs/technical_ksas/healthcare_social_assistance/direct_clinical_practice/
```

**Pre-execution gate:** All 35 proficiency level indicators (5 × 7) are FR-09-xx (Founder Review). Wait for explicit founder approval of every indicator before writing any file. This is a hard stop — no partial execution.

**Field pre-authorizations for all 7 files:**
- `category`: "Technical"
- `sector`: "healthcare_social_assistance"
- `horizon`: "core"
- `transfer_populations`: `military_transition`, `early_career`, `mid_career_change`

**Cluster tags:** Draw only from Controlled Vocabulary v1.0. Verify `Patient Care` and `Clinical Practice` exist in the vocabulary before assigning. If absent, route to Strategist for vocabulary amendment first.

**Post-write tasks:**
- Create the `direct_clinical_practice\` subdirectory before writing the first file
- After all 7 files written and validated: update `healthcare_social_assistance/README.md` to add the new subdirectory to the Sub-Domains table and add 7 rows to the KSA Inventory table
- Run adjacency matrix recomputation — new tags may affect healthcare adjacency scores
- Report post-write verification back to the Instructional Designer

---

## QUICK-REFERENCE CHECKLIST

**Before writing:**
- [ ] Written authorization confirmed (OI or Decision Memo)
- [ ] Target file(s) read in full immediately before write
- [ ] C1–C6 six-criterion review complete for all files
- [ ] All FR-xx-xx founder review items approved (OI-09: all 35)
- [ ] `cluster_tags` values confirmed against Controlled Vocabulary v1.0
- [ ] Pre-change `master_ksa.json` baseline established if cluster_tags are changing

**After writing:**
- [ ] Post-write read-back confirms content is correct
- [ ] File size consistent with expected content via `list_directory_with_sizes`
- [ ] `npm run build:ksas` — zero errors
- [ ] `npm run validate:ksas` — zero schema violations
- [ ] `npm run inventory:ksas` — reports regenerated
- [ ] Sector README(s) updated
- [ ] Adjacency matrix recomputed if cluster_tags changed
- [ ] `docs/reference/` updated if UPLS KSA changed
- [ ] Git commit with descriptive message

---

*KSA_CHANGE_MANAGEMENT_PROTOCOL.md | Claude Code operational reference | v1.0 | 2026-03-17*
*Master document: `[OPSDIR]\01_Strategic_Documents\AI_Operations\2026-03-17_CaliberPath_KSA_Change_Management_Protocol_v1.md`*
*Read this document at the start of any session that modifies `content/Individual_KSAs/`.*
