# CaliberPath — Sector Adjacency Matrix
**Stream:** 3.8 — Cross-Sector Transferability Architecture
**Computed by:** T-CROSSWALK-01
**Computation date:** 2026-03-19
**Data source:** master_ksa.json — 691 KSAs across 35 sectors
**cluster_tags basis:** Controlled Vocabulary v1.0 (post-T-README-02 normalization; OI-09 direct_clinical_practice tags incorporated)

---

## Section 1 — Methodology Notes

**Data source:** master_ksa.json — 691 KSAs across 35 technical sectors (45 cross_sector KSAs excluded from sector tag sets)
**Computation approach:** For each sector, collected the union of all distinct cluster_tags across all KSAs in that sector. For every sector pair (A, B) where A ≠ B, computed `|tag_set(A) ∩ tag_set(B)|`. Matrix is symmetric.
**Sector field normalization:** Two KSA files used abbreviated sector field values — `government_public_admin` → `government_public_administration`; `env_energy_advanced` → `environmental_energy_advanced`. Normalization applied in computation. Flagged as Claude Code cleanup item.
**Tag set size range:** 19 to 48 unique tags per sector
**Total unique tags in corpus:** 897 (post-T-README-02 Controlled Vocabulary v1.0 normalization; OI-09 tags included)
**Total pairwise computations:** 595 (35×34/2)
**Non-zero adjacency pairs:** 370 (62.2% of total)
**Zero-adjacency pairs:** 225 (37.8% of total)

**Shared tag count distribution:**
- 7 shared tags: 1 pairs
- 6 shared tags: 7 pairs
- 5 shared tags: 12 pairs
- 4 shared tags: 25 pairs
- 3 shared tags: 48 pairs
- 2 shared tags: 111 pairs
- 1 shared tags: 166 pairs

**Threshold calibration:** Standard thresholds applied without adjustment. The calibration override rule does NOT trigger — maximum shared count in corpus is 7, far below the 15-tag trigger. No pairs achieve VERY HIGH (10+). Effective ceiling is HIGH (score 3), achieved by 1 pair only.

| Shared Count | Score | Label | Pair Count |
|---|---|---|---|
| 10+ | 4 | VERY HIGH | 0 |
| 7–9 | 3 | HIGH | 1 |
| 4–6 | 2 | MEDIUM | 44 |
| 2–3 | 1 | LOW | 159 |
| 1 | 0 | MARGINAL | 166 |
| 0 | — | NONE | 225 |

**Interpretation:** The sparse adjacency pattern (37.8% NONE pairs) reflects intentional KSA tag specificity. Shared backbone tags (Safety, Compliance, Finance, Sustainability, Analytics, Automation, Maintenance, Risk Management) drive the majority of adjacency signals at scores 1–2. The OI-09 addition of 7 direct clinical practice KSAs to healthcare_social_assistance introduced backbone tags (Safety, Compliance) and domain-specific tags (OSHA 1910, PPE, Infection Control) that significantly broadened healthcare's adjacency profile from 10 non-zero pairs to 28. HIGH-scoring pairs share 7 tags combining backbone and sector-specific signals.

---

## Section 2 — Ranked Adjacency Reference (Top 5 Per Sector)

*For T-CROSSWALK-02 and T-CROSSWALK-03 use. Ties at the boundary included.*

**government_public_administration** *(tag set: 42 unique tags)*
  1. real_estate_property — 4 shared tags — MEDIUM (score 2)
  2. public_safety_security — 4 shared tags — MEDIUM (score 2)
  3. ai_data_quantum — 4 shared tags — MEDIUM (score 2)
  4. media_arts_entertainment — 3 shared tags — LOW (score 1)
  5. informal_gray_economy — 3 shared tags — LOW (score 1)
  6. immersive_media_ar_vr_metaverse — 3 shared tags — LOW (score 1)
  7. gig_platform_economy — 3 shared tags — LOW (score 1)
  8. energy_utilities — 3 shared tags — LOW (score 1)
  9. education_training — 3 shared tags — LOW (score 1)
  10. blockchain_web3 — 3 shared tags — LOW (score 1)
  11. agriculture_natural_resources — 3 shared tags — LOW (score 1)

**public_safety_security** *(tag set: 29 unique tags)*
  1. government_public_administration — 4 shared tags — MEDIUM (score 2)
  2. real_estate_property — 2 shared tags — LOW (score 1)
  3. mining_extraction — 2 shared tags — LOW (score 1)
  4. blockchain_web3 — 2 shared tags — LOW (score 1)
  5. transportation_logistics — 1 shared tags — MARGINAL (score 0)

**education_training** *(tag set: 34 unique tags)*
  1. professional_scientific_services — 3 shared tags — LOW (score 1)
  2. government_public_administration — 3 shared tags — LOW (score 1)
  3. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  4. personal_other_services — 2 shared tags — LOW (score 1)
  5. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  6. hospitality_tourism — 2 shared tags — LOW (score 1)
  7. healthcare_social_assistance — 2 shared tags — LOW (score 1)
  8. energy_utilities — 2 shared tags — LOW (score 1)
  9. customer_experience_service — 2 shared tags — LOW (score 1)

**core_it_cloud** *(tag set: 43 unique tags)*
  1. ai_data_quantum — 4 shared tags — MEDIUM (score 2)
  2. mining_extraction — 3 shared tags — LOW (score 1)
  3. telecommunications — 2 shared tags — LOW (score 1)
  4. manufacturing — 2 shared tags — LOW (score 1)
  5. finance_insurance — 2 shared tags — LOW (score 1)
  6. blockchain_web3 — 2 shared tags — LOW (score 1)

**ai_data_quantum** *(tag set: 40 unique tags)*
  1. government_public_administration — 4 shared tags — MEDIUM (score 2)
  2. core_it_cloud — 4 shared tags — MEDIUM (score 2)
  3. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  4. real_estate_property — 2 shared tags — LOW (score 1)
  5. manufacturing — 2 shared tags — LOW (score 1)
  6. immersive_media_ar_vr_metaverse — 2 shared tags — LOW (score 1)
  7. finance_insurance — 2 shared tags — LOW (score 1)
  8. digital_content_creation_creator_economy — 2 shared tags — LOW (score 1)

**finance_insurance** *(tag set: 47 unique tags)*
  1. personal_other_services — 4 shared tags — MEDIUM (score 2)
  2. mining_extraction — 4 shared tags — MEDIUM (score 2)
  3. agriculture_natural_resources — 4 shared tags — MEDIUM (score 2)
  4. space_economy_aerospace — 3 shared tags — LOW (score 1)
  5. real_estate_property — 3 shared tags — LOW (score 1)
  6. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)
  7. hospitality_tourism — 3 shared tags — LOW (score 1)
  8. gig_platform_economy — 3 shared tags — LOW (score 1)

**healthcare_social_assistance** *(tag set: 42 unique tags)*
  1. personal_other_services — 5 shared tags — MEDIUM (score 2)
  2. wholesale_retail_trade — 5 shared tags — MEDIUM (score 2)
  3. energy_utilities — 4 shared tags — MEDIUM (score 2)
  4. manufacturing — 3 shared tags — LOW (score 1)
  5. unpaid_caregiving_domestic_work — 3 shared tags — LOW (score 1)
  6. agriculture_natural_resources — 2 shared tags — LOW (score 1)
  7. blockchain_web3 — 2 shared tags — LOW (score 1)
  8. construction_infrastructure — 2 shared tags — LOW (score 1)
  9. customer_experience_service — 2 shared tags — LOW (score 1)
  10. education_training — 2 shared tags — LOW (score 1)
  11. finance_insurance — 2 shared tags — LOW (score 1)
  12. immersive_media_ar_vr_metaverse — 2 shared tags — LOW (score 1)
  13. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  14. mining_extraction — 2 shared tags — LOW (score 1)
  15. telecommunications — 2 shared tags — LOW (score 1)
  16. transportation_logistics — 2 shared tags — LOW (score 1)

**nonprofit_ngos** *(tag set: 39 unique tags)*
  1. personal_other_services — 4 shared tags — MEDIUM (score 2)
  2. informal_gray_economy — 4 shared tags — MEDIUM (score 2)
  3. gig_platform_economy — 4 shared tags — MEDIUM (score 2)
  4. administrative_support_services — 4 shared tags — MEDIUM (score 2)
  5. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)

**professional_scientific_services** *(tag set: 29 unique tags)*
  1. education_training — 3 shared tags — LOW (score 1)
  2. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  3. transportation_logistics — 2 shared tags — LOW (score 1)
  4. personal_other_services — 2 shared tags — LOW (score 1)
  5. manufacturing — 2 shared tags — LOW (score 1)
  6. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  7. government_public_administration — 2 shared tags — LOW (score 1)
  8. construction_infrastructure — 2 shared tags — LOW (score 1)
  9. blockchain_web3 — 2 shared tags — LOW (score 1)

**manufacturing** *(tag set: 36 unique tags)*
  1. transportation_logistics — 7 shared tags — HIGH (score 3)
  2. mining_extraction — 6 shared tags — MEDIUM (score 2)
  3. construction_infrastructure — 6 shared tags — MEDIUM (score 2)
  4. maker_economy_creative_crafts — 5 shared tags — MEDIUM (score 2)
  5. agriculture_natural_resources — 4 shared tags — MEDIUM (score 2)

**telecommunications** *(tag set: 30 unique tags)*
  1. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  2. manufacturing — 2 shared tags — LOW (score 1)
  3. healthcare_social_assistance — 2 shared tags — LOW (score 1)
  4. core_it_cloud — 2 shared tags — LOW (score 1)
  5. transportation_logistics — 1 shared tags — MARGINAL (score 0)

**construction_infrastructure** *(tag set: 43 unique tags)*
  1. transportation_logistics — 6 shared tags — MEDIUM (score 2)
  2. manufacturing — 6 shared tags — MEDIUM (score 2)
  3. maker_economy_creative_crafts — 6 shared tags — MEDIUM (score 2)
  4. personal_other_services — 5 shared tags — MEDIUM (score 2)
  5. mining_extraction — 4 shared tags — MEDIUM (score 2)
  6. agriculture_natural_resources — 4 shared tags — MEDIUM (score 2)

**energy_utilities** *(tag set: 30 unique tags)*
  1. personal_other_services — 5 shared tags — MEDIUM (score 2)
  2. environmental_energy_advanced — 5 shared tags — MEDIUM (score 2)
  3. mining_extraction — 4 shared tags — MEDIUM (score 2)
  4. agriculture_natural_resources — 4 shared tags — MEDIUM (score 2)
  5. healthcare_social_assistance — 4 shared tags — MEDIUM (score 2)
  6. wholesale_retail_trade — 3 shared tags — LOW (score 1)
  7. space_economy_aerospace — 3 shared tags — LOW (score 1)
  8. manufacturing — 3 shared tags — LOW (score 1)
  9. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)
  10. government_public_administration — 3 shared tags — LOW (score 1)
  11. gig_platform_economy — 3 shared tags — LOW (score 1)

**environmental_energy_advanced** *(tag set: 39 unique tags)*
  1. energy_utilities — 5 shared tags — MEDIUM (score 2)
  2. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)
  3. agriculture_natural_resources — 3 shared tags — LOW (score 1)
  4. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  5. transportation_logistics — 2 shared tags — LOW (score 1)
  6. real_estate_property — 2 shared tags — LOW (score 1)
  7. mining_extraction — 2 shared tags — LOW (score 1)
  8. informal_gray_economy — 2 shared tags — LOW (score 1)
  9. hospitality_tourism — 2 shared tags — LOW (score 1)

**transportation_logistics** *(tag set: 33 unique tags)*
  1. manufacturing — 7 shared tags — HIGH (score 3)
  2. maker_economy_creative_crafts — 6 shared tags — MEDIUM (score 2)
  3. construction_infrastructure — 6 shared tags — MEDIUM (score 2)
  4. mining_extraction — 5 shared tags — MEDIUM (score 2)
  5. agriculture_natural_resources — 5 shared tags — MEDIUM (score 2)

**wholesale_retail_trade** *(tag set: 45 unique tags)*
  1. personal_other_services — 6 shared tags — MEDIUM (score 2)
  2. healthcare_social_assistance — 5 shared tags — MEDIUM (score 2)
  3. maker_economy_creative_crafts — 4 shared tags — MEDIUM (score 2)
  4. transportation_logistics — 3 shared tags — LOW (score 1)
  5. manufacturing — 3 shared tags — LOW (score 1)
  6. immersive_media_ar_vr_metaverse — 3 shared tags — LOW (score 1)
  7. energy_utilities — 3 shared tags — LOW (score 1)
  8. customer_experience_service — 3 shared tags — LOW (score 1)
  9. construction_infrastructure — 3 shared tags — LOW (score 1)
  10. agriculture_natural_resources — 3 shared tags — LOW (score 1)

**administrative_support_services** *(tag set: 43 unique tags)*
  1. nonprofit_ngos — 4 shared tags — MEDIUM (score 2)
  2. manufacturing — 3 shared tags — LOW (score 1)
  3. construction_infrastructure — 3 shared tags — LOW (score 1)
  4. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  5. unpaid_caregiving_domestic_work — 2 shared tags — LOW (score 1)
  6. transportation_logistics — 2 shared tags — LOW (score 1)
  7. personal_other_services — 2 shared tags — LOW (score 1)
  8. media_arts_entertainment — 2 shared tags — LOW (score 1)
  9. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  10. government_public_administration — 2 shared tags — LOW (score 1)
  11. finance_insurance — 2 shared tags — LOW (score 1)
  12. customer_experience_service — 2 shared tags — LOW (score 1)
  13. agriculture_natural_resources — 2 shared tags — LOW (score 1)

**agriculture_natural_resources** *(tag set: 24 unique tags)*
  1. maker_economy_creative_crafts — 6 shared tags — MEDIUM (score 2)
  2. transportation_logistics — 5 shared tags — MEDIUM (score 2)
  3. personal_other_services — 4 shared tags — MEDIUM (score 2)
  4. mining_extraction — 4 shared tags — MEDIUM (score 2)
  5. manufacturing — 4 shared tags — MEDIUM (score 2)
  6. finance_insurance — 4 shared tags — MEDIUM (score 2)
  7. energy_utilities — 4 shared tags — MEDIUM (score 2)
  8. construction_infrastructure — 4 shared tags — MEDIUM (score 2)

**biotechnology_synthetic_biology** *(tag set: 25 unique tags)*
  1. informal_gray_economy — 2 shared tags — LOW (score 1)
  2. energy_utilities — 2 shared tags — LOW (score 1)
  3. public_safety_security — 1 shared tags — MARGINAL (score 0)
  4. professional_scientific_services — 1 shared tags — MARGINAL (score 0)
  5. personal_other_services — 1 shared tags — MARGINAL (score 0)

**customer_experience_service** *(tag set: 23 unique tags)*
  1. personal_other_services — 6 shared tags — MEDIUM (score 2)
  2. wholesale_retail_trade — 3 shared tags — LOW (score 1)
  3. unpaid_caregiving_domestic_work — 2 shared tags — LOW (score 1)
  4. manufacturing — 2 shared tags — LOW (score 1)
  5. hospitality_tourism — 2 shared tags — LOW (score 1)
  6. healthcare_social_assistance — 2 shared tags — LOW (score 1)
  7. energy_utilities — 2 shared tags — LOW (score 1)
  8. education_training — 2 shared tags — LOW (score 1)
  9. administrative_support_services — 2 shared tags — LOW (score 1)

**real_estate_property** *(tag set: 26 unique tags)*
  1. government_public_administration — 4 shared tags — MEDIUM (score 2)
  2. mining_extraction — 3 shared tags — LOW (score 1)
  3. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)
  4. finance_insurance — 3 shared tags — LOW (score 1)
  5. agriculture_natural_resources — 3 shared tags — LOW (score 1)

**hospitality_tourism** *(tag set: 40 unique tags)*
  1. personal_other_services — 5 shared tags — MEDIUM (score 2)
  2. maker_economy_creative_crafts — 4 shared tags — MEDIUM (score 2)
  3. gig_platform_economy — 4 shared tags — MEDIUM (score 2)
  4. mining_extraction — 3 shared tags — LOW (score 1)
  5. media_arts_entertainment — 3 shared tags — LOW (score 1)
  6. informal_gray_economy — 3 shared tags — LOW (score 1)
  7. finance_insurance — 3 shared tags — LOW (score 1)

**personal_other_services** *(tag set: 43 unique tags)*
  1. maker_economy_creative_crafts — 7 shared tags — HIGH (score 3)
  2. wholesale_retail_trade — 6 shared tags — MEDIUM (score 2)
  3. customer_experience_service — 6 shared tags — MEDIUM (score 2)
  4. hospitality_tourism — 5 shared tags — MEDIUM (score 2)
  5. energy_utilities — 5 shared tags — MEDIUM (score 2)
  6. healthcare_social_assistance — 5 shared tags — MEDIUM (score 2)
  7. construction_infrastructure — 5 shared tags — MEDIUM (score 2)

**unpaid_caregiving_domestic_work** *(tag set: 24 unique tags)*
  1. healthcare_social_assistance — 3 shared tags — LOW (score 1)
  2. customer_experience_service — 2 shared tags — LOW (score 1)
  3. administrative_support_services — 2 shared tags — LOW (score 1)
  4. personal_other_services — 1 shared tags — MARGINAL (score 0)
  5. nonprofit_ngos — 1 shared tags — MARGINAL (score 0)
  6. media_arts_entertainment — 1 shared tags — MARGINAL (score 0)
  7. government_public_administration — 1 shared tags — MARGINAL (score 0)

**immersive_media_ar_vr_metaverse** *(tag set: 36 unique tags)*
  1. media_arts_entertainment — 5 shared tags — MEDIUM (score 2)
  2. wholesale_retail_trade — 3 shared tags — LOW (score 1)
  3. government_public_administration — 3 shared tags — LOW (score 1)
  4. personal_other_services — 2 shared tags — LOW (score 1)
  5. manufacturing — 2 shared tags — LOW (score 1)
  6. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  7. energy_utilities — 2 shared tags — LOW (score 1)
  8. ai_data_quantum — 2 shared tags — LOW (score 1)

**blockchain_web3** *(tag set: 25 unique tags)*
  1. government_public_administration — 3 shared tags — LOW (score 1)
  2. public_safety_security — 2 shared tags — LOW (score 1)
  3. professional_scientific_services — 2 shared tags — LOW (score 1)
  4. healthcare_social_assistance — 2 shared tags — LOW (score 1)
  5. finance_insurance — 2 shared tags — LOW (score 1)
  6. energy_utilities — 2 shared tags — LOW (score 1)
  7. core_it_cloud — 2 shared tags — LOW (score 1)

**digital_content_creation_creator_economy** *(tag set: 23 unique tags)*
  1. media_arts_entertainment — 3 shared tags — LOW (score 1)
  2. wholesale_retail_trade — 2 shared tags — LOW (score 1)
  3. ai_data_quantum — 2 shared tags — LOW (score 1)
  4. maker_economy_creative_crafts — 1 shared tags — MARGINAL (score 0)
  5. creative_cultural_industries — 1 shared tags — MARGINAL (score 0)

**gig_platform_economy** *(tag set: 21 unique tags)*
  1. maker_economy_creative_crafts — 5 shared tags — MEDIUM (score 2)
  2. personal_other_services — 4 shared tags — MEDIUM (score 2)
  3. nonprofit_ngos — 4 shared tags — MEDIUM (score 2)
  4. hospitality_tourism — 4 shared tags — MEDIUM (score 2)
  5. transportation_logistics — 3 shared tags — LOW (score 1)
  6. space_economy_aerospace — 3 shared tags — LOW (score 1)
  7. informal_gray_economy — 3 shared tags — LOW (score 1)
  8. government_public_administration — 3 shared tags — LOW (score 1)
  9. finance_insurance — 3 shared tags — LOW (score 1)
  10. energy_utilities — 3 shared tags — LOW (score 1)
  11. agriculture_natural_resources — 3 shared tags — LOW (score 1)

**media_arts_entertainment** *(tag set: 39 unique tags)*
  1. immersive_media_ar_vr_metaverse — 5 shared tags — MEDIUM (score 2)
  2. creative_cultural_industries — 4 shared tags — MEDIUM (score 2)
  3. hospitality_tourism — 3 shared tags — LOW (score 1)
  4. government_public_administration — 3 shared tags — LOW (score 1)
  5. digital_content_creation_creator_economy — 3 shared tags — LOW (score 1)

**space_economy_aerospace** *(tag set: 34 unique tags)*
  1. personal_other_services — 4 shared tags — MEDIUM (score 2)
  2. maker_economy_creative_crafts — 3 shared tags — LOW (score 1)
  3. gig_platform_economy — 3 shared tags — LOW (score 1)
  4. finance_insurance — 3 shared tags — LOW (score 1)
  5. energy_utilities — 3 shared tags — LOW (score 1)

**informal_gray_economy** *(tag set: 38 unique tags)*
  1. nonprofit_ngos — 4 shared tags — MEDIUM (score 2)
  2. maker_economy_creative_crafts — 4 shared tags — MEDIUM (score 2)
  3. transportation_logistics — 3 shared tags — LOW (score 1)
  4. personal_other_services — 3 shared tags — LOW (score 1)
  5. hospitality_tourism — 3 shared tags — LOW (score 1)
  6. government_public_administration — 3 shared tags — LOW (score 1)
  7. gig_platform_economy — 3 shared tags — LOW (score 1)

**maker_economy_creative_crafts** *(tag set: 48 unique tags)*
  1. personal_other_services — 7 shared tags — HIGH (score 3)
  2. transportation_logistics — 6 shared tags — MEDIUM (score 2)
  3. construction_infrastructure — 6 shared tags — MEDIUM (score 2)
  4. agriculture_natural_resources — 6 shared tags — MEDIUM (score 2)
  5. manufacturing — 5 shared tags — MEDIUM (score 2)
  6. gig_platform_economy — 5 shared tags — MEDIUM (score 2)

**arts_recreation_services** *(tag set: 21 unique tags)*
  1. personal_other_services — 3 shared tags — LOW (score 1)
  2. mining_extraction — 3 shared tags — LOW (score 1)
  3. transportation_logistics — 2 shared tags — LOW (score 1)
  4. media_arts_entertainment — 2 shared tags — LOW (score 1)
  5. manufacturing — 2 shared tags — LOW (score 1)
  6. maker_economy_creative_crafts — 2 shared tags — LOW (score 1)
  7. hospitality_tourism — 2 shared tags — LOW (score 1)
  8. construction_infrastructure — 2 shared tags — LOW (score 1)

**creative_cultural_industries** *(tag set: 21 unique tags)*
  1. media_arts_entertainment — 4 shared tags — MEDIUM (score 2)
  2. nonprofit_ngos — 1 shared tags — MARGINAL (score 0)
  3. maker_economy_creative_crafts — 1 shared tags — MARGINAL (score 0)
  4. immersive_media_ar_vr_metaverse — 1 shared tags — MARGINAL (score 0)
  5. hospitality_tourism — 1 shared tags — MARGINAL (score 0)

**mining_extraction** *(tag set: 41 unique tags)*
  1. manufacturing — 6 shared tags — MEDIUM (score 2)
  2. transportation_logistics — 5 shared tags — MEDIUM (score 2)
  3. personal_other_services — 4 shared tags — MEDIUM (score 2)
  4. finance_insurance — 4 shared tags — MEDIUM (score 2)
  5. energy_utilities — 4 shared tags — MEDIUM (score 2)
  6. construction_infrastructure — 4 shared tags — MEDIUM (score 2)
  7. agriculture_natural_resources — 4 shared tags — MEDIUM (score 2)

---

## Section 3 — Full 35×35 Adjacency Matrix

Score key: 4 = VERY HIGH | 3 = HIGH | 2 = MEDIUM | 1 = LOW | 0 = MARGINAL | — = NONE or diagonal

| Sector | gov | pub_saf | edu | it | ai | fin | hc | ngo | pss | mfg | tel | con | eng | env | tra | wrt | adm | agr | bio | cxs | re | hos | pos | ucd | imm | bcw | dcc | gig | mae | sae | ige | mkr | ars | cci | mnx |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **gov** | — | 2 | 1 | 0 | 2 | 1 | 0 | 1 | 1 | 1 | — | — | 1 | 0 | — | 0 | 1 | 1 | 0 | — | 2 | — | 0 | 0 | 1 | 1 | — | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| **pub_saf** | 2 | — | — | 0 | 0 | 0 | 0 | — | 0 | 0 | — | — | 0 | — | 0 | — | — | 0 | 0 | — | 1 | — | — | — | — | 1 | — | 0 | — | 0 | 0 | 0 | — | — | 1 |
| **edu** | 1 | — | — | — | — | — | 1 | — | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | — | 0 | 0 | 1 | — | 1 | 1 | — | 0 | — | — | — | 0 | — | 0 | 1 | — | — | — |
| **it** | 0 | 0 | — | — | 2 | 1 | 0 | — | 0 | 1 | 1 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — | — | — | — | 1 | — | 0 | — | — | 0 | — | — | — | 1 |
| **ai** | 2 | 0 | — | 2 | — | 1 | 0 | 0 | — | 1 | 0 | — | — | — | — | 1 | 0 | 0 | 0 | — | 1 | — | — | — | 1 | 0 | 1 | — | 0 | — | — | — | — | — | 0 |
| **fin** | 1 | 0 | — | 1 | 1 | — | 1 | 1 | — | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 2 | — | 0 | 1 | 1 | 2 | — | — | 1 | — | 1 | 0 | 1 | 0 | 1 | — | — | 2 |
| **hc** | 0 | 0 | 1 | 0 | 0 | 1 | — | 0 | 0 | 1 | 1 | 1 | 2 | — | 1 | 2 | — | 1 | 0 | 1 | — | 0 | 2 | 1 | 1 | 1 | — | 0 | 0 | 0 | — | 1 | 0 | — | 1 |
| **ngo** | 1 | — | — | — | 0 | 1 | 0 | — | — | — | — | 0 | 1 | — | 1 | 1 | 2 | 1 | — | 0 | 0 | 1 | 2 | 0 | — | — | — | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 0 |
| **pss** | 1 | 0 | 1 | 0 | — | — | 0 | — | — | 1 | 0 | 1 | 0 | 0 | 1 | 1 | — | 0 | 0 | 0 | — | 0 | 1 | — | 0 | 1 | — | 0 | — | — | 0 | 1 | — | — | 0 |
| **mfg** | 1 | 0 | 0 | 1 | 1 | 1 | 1 | — | 1 | — | 1 | 2 | 1 | 0 | 3 | 1 | 1 | 2 | — | 1 | 1 | — | 1 | — | 1 | — | — | 0 | — | — | 1 | 2 | 1 | — | 2 |
| **tel** | — | — | 0 | 1 | 0 | 0 | 1 | — | 0 | 1 | — | 0 | 0 | — | 0 | 1 | — | — | — | 0 | — | — | 0 | — | 0 | 0 | — | — | — | — | — | — | — | — | 0 |
| **con** | — | — | 0 | 0 | — | 0 | 1 | 0 | 1 | 2 | 0 | — | 1 | 0 | 2 | 1 | 1 | 2 | — | — | 1 | 1 | 2 | — | 1 | — | — | 1 | — | 0 | 0 | 2 | 1 | — | 2 |
| **eng** | 1 | 0 | 1 | — | — | 1 | 2 | 1 | 0 | 1 | 0 | 1 | — | 2 | 1 | 1 | 0 | 2 | 1 | 1 | 1 | 0 | 2 | — | 1 | 1 | — | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 2 |
| **env** | 0 | — | 0 | 0 | — | 0 | — | — | 0 | 0 | — | 0 | 2 | — | 1 | 1 | 0 | 1 | — | — | 1 | 1 | — | — | — | — | — | — | 0 | — | 1 | 1 | — | 0 | 1 |
| **tra** | — | 0 | 0 | 0 | — | 1 | 1 | 1 | 1 | 3 | 0 | 2 | 1 | 1 | — | 1 | 1 | 2 | — | — | — | — | 1 | — | — | — | — | 1 | — | 0 | 1 | 2 | 1 | — | 2 |
| **wrt** | 0 | — | 1 | 0 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | — | 1 | 1 | — | 1 | 1 | 1 | 2 | — | 1 | — | 1 | 1 | — | 0 | — | 2 | 0 | — | 1 |
| **adm** | 1 | — | — | 0 | 0 | 1 | — | 2 | — | 1 | — | 1 | 0 | 0 | 1 | 1 | — | 1 | — | 1 | — | — | 1 | 1 | — | — | 0 | — | 1 | 0 | 0 | 1 | — | 0 | 0 |
| **agr** | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 2 | — | 2 | 2 | 1 | 2 | 1 | 1 | — | — | — | 1 | — | 2 | — | — | — | — | 1 | 0 | 1 | 1 | 2 | 0 | — | 2 |
| **bio** | 0 | 0 | 0 | 0 | 0 | — | 0 | — | 0 | — | — | — | 1 | — | — | — | — | — | — | — | — | — | 0 | — | — | 0 | — | 0 | 0 | — | 1 | 0 | — | — | — |
| **cxs** | — | — | 1 | 0 | — | 0 | 1 | 0 | 0 | 1 | 0 | — | 1 | — | — | 1 | 1 | — | — | — | — | 1 | 2 | 1 | — | — | — | — | 0 | — | — | — | — | — | — |
| **re** | 2 | 1 | — | — | 1 | 1 | — | 0 | — | 1 | — | 1 | 1 | 1 | — | 1 | — | 1 | — | — | — | — | 1 | — | — | — | — | — | 0 | 1 | 0 | 1 | 0 | — | 1 |
| **hos** | — | — | 1 | — | — | 1 | 0 | 1 | 0 | — | — | 1 | 0 | 1 | — | 1 | — | — | — | 1 | — | — | 2 | — | — | — | — | 2 | 1 | 1 | 1 | 2 | 1 | 0 | 1 |
| **pos** | 0 | — | 1 | — | — | 2 | 2 | 2 | 1 | 1 | 0 | 2 | 2 | — | 1 | 2 | 1 | 2 | 0 | 2 | 1 | 2 | — | 0 | 1 | — | — | 2 | 1 | 2 | 1 | 3 | 1 | — | 2 |
| **ucd** | 0 | — | — | — | — | — | 1 | 0 | — | — | — | — | — | — | — | — | 1 | — | — | 1 | — | — | 0 | — | — | — | — | — | 0 | — | — | — | — | — | — |
| **imm** | 1 | — | 0 | — | 1 | — | 1 | — | 0 | 1 | 0 | 1 | 1 | — | — | 1 | — | — | — | — | — | — | 1 | — | — | — | — | — | 2 | — | — | 1 | 0 | 0 | — |
| **bcw** | 1 | 1 | — | 1 | 0 | 1 | 1 | — | 1 | — | 0 | — | 1 | — | — | — | — | — | 0 | — | — | — | — | — | — | — | — | — | — | — | 0 | — | — | — | — |
| **dcc** | — | — | — | — | 1 | — | — | — | — | — | — | — | — | — | — | 1 | 0 | — | — | — | — | — | — | — | — | — | — | — | 1 | — | — | 0 | 0 | 0 | — |
| **gig** | 1 | 0 | — | 0 | — | 1 | 0 | 2 | 0 | 0 | — | 1 | 1 | — | 1 | 1 | 0 | 1 | 0 | — | 0 | 2 | 2 | — | 0 | 0 | — | — | 1 | 1 | 1 | 2 | 0 | — | 1 |
| **mae** | 1 | — | 0 | — | 0 | 0 | 0 | 1 | — | — | — | — | 1 | 0 | — | — | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 2 | — | 1 | 1 | — | 1 | 0 | 1 | 1 | 2 | 0 |
| **sae** | 1 | 0 | — | — | — | 1 | 0 | 1 | — | — | — | 0 | 1 | — | 0 | 0 | 0 | 1 | — | — | 1 | 1 | 2 | — | — | — | — | 1 | 1 | — | 0 | 1 | — | — | 0 |
| **ige** | 1 | 0 | 0 | 0 | — | 0 | — | 2 | 0 | 1 | — | 0 | 1 | 1 | 1 | — | 0 | 1 | 1 | — | 0 | 1 | 1 | — | — | 0 | — | 1 | 0 | 0 | — | 2 | — | — | 0 |
| **mkr** | 0 | 0 | 1 | — | — | 1 | 1 | 1 | 1 | 2 | — | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 0 | — | 1 | 2 | 3 | — | 1 | — | 0 | 2 | 1 | 1 | 2 | — | 1 | 0 | 1 |
| **ars** | 0 | — | — | — | — | — | 0 | 0 | — | 1 | — | 1 | 0 | — | 1 | 0 | — | 0 | — | — | 0 | 1 | 1 | — | 0 | — | 0 | 0 | 1 | — | — | 1 | — | — | 1 |
| **cci** | 0 | — | — | — | — | — | — | 0 | — | — | — | — | — | 0 | — | — | 0 | — | — | — | — | 0 | — | — | 0 | — | 0 | — | 2 | — | — | 0 | — | — | — |
| **mnx** | 0 | 1 | — | 1 | 0 | 2 | 1 | 0 | 0 | 2 | 0 | 2 | 2 | 1 | 2 | 1 | 0 | 2 | — | 0 | 1 | 1 | 2 | — | — | — | — | 1 | 0 | 0 | 0 | 1 | 1 | — | — |

---

*sector_adjacency_matrix.md | Computed: T-CROSSWALK-01 | 2026-03-19 (recomputed for OI-09) | Stream 3.8*
