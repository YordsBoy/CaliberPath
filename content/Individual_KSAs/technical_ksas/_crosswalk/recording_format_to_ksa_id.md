# CaliberPath — Recording Format Slot → KSA-ID Crosswalk

**Substrate class:** Documentation file (excluded from KSA-classification scope per `_crosswalk/` directory exclusion in `scripts/inventory_ksas.js` and `scripts/build_ksa_json.js`).
**Authority:** Strategist Tier 2 disposition 2026-05-17 (Path B — centralized REPO-side crosswalk) per WS-CIG-UPLS-DRIFT-REVIEW Phase 4 closure surface. Operationalizes CC PERS-MOD-01 Decision F1 REPO-Side Attestation Disposition v1 (2026-05-17) §4 forward observation.
**Last updated:** 2026-05-17 (initial creation; PERS-MOD-01 BizFin cluster only)

---

## Purpose

This file is the canonical crosswalk between **sector-module recording-format slots** (the presentation-layer coach-facing shorthand labels used in CIG instrument recording-format blocks) and **KSA-REPO `ksa_id` files** (the REPO-substrate descriptive labels).

The two surfaces use different naming conventions by design:

- **Recording format slots** are coach-facing, terse, and optimized for in-session note-taking (e.g., `BIZ-FINANCE[level]`, `CHEM-SAFETY[level]`).
- **KSA-REPO `ksa_id` files** are descriptive, sector-specific, and optimized for content authorship + schema integrity (e.g., `small_business_finance_pricing_personal_services`).

Without an explicit crosswalk, the slot-to-`ksa_id` mapping is inferred via semantic correspondence — usable now, but latently fragile: any future `ksa_id` rename, sub-domain reorganization, or recording-format slot rename could decouple the mapping without surfacing an error at either substrate. This file removes that fragility by registering the mapping explicitly.

---

## PERS-MOD-01 — Personal & Other Services

**Source authority:** [OPSDIR] `04_Deliverables\Curricula\Instruments\Sector_Modules\2026-03-20_CaliberPath_PERS_MOD_01_PersonalOtherServices_CIG_v1.md` §1 Recording Format
**KSA-REPO sector:** `personal_other_services`
**Cluster covered:** BizFin (Business / Compliance / Finance)

| Recording-format slot | KSA-REPO file (relative to `content/Individual_KSAs/technical_ksas/`) | `ksa_id` | Cluster tags | Notes |
|---|---|---|---|---|
| `BIZ-OPS[level]` | `personal_other_services/business_compliance_finance/personal_business_operations.md` | `personal_business_operations` | (see file) | Business operations anchor |
| `BIZ-COMPLIANCE[level]` | `personal_other_services/business_compliance_finance/small_business_compliance.md` | `small_business_compliance` | (see file) | Business compliance anchor |
| `BIZ-FINANCE[level]` | `personal_other_services/business_compliance_finance/small_business_finance_pricing_personal_services.md` | `small_business_finance_pricing_personal_services` | Finance, Pricing | **Canonical Decision F1 relocation anchor per ID Phase 3 Source-Content Correction Resolution v1 §6.2.** Salon/Studio Owner financial-acumen requirements source from this KSA at session execution. |
| `MOBILE-PAY[level]` | `personal_other_services/business_compliance_finance/mobile_payment_processing_personal_services.md` | `mobile_payment_processing_personal_services` | (see file) | Emerging-horizon KSA per PERS-MOD-01 §1 |

PERS-MOD-01 has additional recording-format clusters (GovComp, CX-Sales, Ops, Safety, Sustain) that are not yet registered here. Append additional sub-sections as those clusters are dispositioned through forward strategist routings.

---

## Forward-Extension Pattern

As Phase 3 production cycle progresses and additional sector modules surface recording-format slot conventions, append each sector-module's mapping as a new `## <MODULE-ID> — <Sector Name>` section, mirroring the PERS-MOD-01 section above. Organize by sector-module identifier (`ADMIN-MOD-01`, `HC-MOD-02`, etc.) so the file remains a single canonical surface for slot integrity across the catalog. Strategist Tier 2 routes incremental amendment requests as patterns surface; CC applies them under standing KSA-REPO write authority. A sector-module recording-format slot that lacks a corresponding row here is by-construction a candidate for decoupling-risk audit — the absence is itself the detection signal.

---

## Maintenance Notes

- **Slot rename or `ksa_id` rename:** update the affected row in lockstep with the underlying change. If the change crosses substrates (PERS-MOD-01 source ↔ KSA-REPO), the routing that authorizes the rename should explicitly call out this crosswalk file as a dependent edit.
- **New sector-module section:** add a new `## <MODULE-ID>` section in alphabetical order by module identifier; include source-authority path + KSA-REPO sector pointer in the section header block, then the per-slot table.
- **Validation discipline:** there is no automated validator for this file at present. Verification is empirical — spot-grep for the recording-format slot label in the linked sector-module source markdown; spot-Read the linked `ksa_id` file to confirm `cluster_tags` / `proficiency_levels` align with the slot's intended semantic.

---

*CaliberPath KSA-REPO — `_crosswalk/recording_format_to_ksa_id.md` | initial creation 2026-05-17 | Authority: Strategist Tier 2 disposition 2026-05-17 (Path B); CC Tier 1 implementation per KSA-REPO write authority.*
