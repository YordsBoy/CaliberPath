# KSA Inventory Report

**Generated:** Thu, 02 Apr 2026 00:58:18 GMT
**Repository:** CaliberPath

---

## 1. Summary

| Metric | Value |
| ----------------------------------------- | ----- |
| Total KSA files scanned                   | **694** |
| Schema-valid                              | **691** (100%) |
| Schema-invalid                            | **3** (0%) |
| Missing `cluster_tags` (optional)         | 3 |
| Missing `source_frameworks` (optional)    | 3 |
| Missing both optional fields              | 3 |

---

## 2. KSAs by Category

| Category                                      | Count |
| --------------------------------------------- | ----- |
| Technical                                     |   646 |
| Self Management                               |    15 |
| Professionalism                               |    15 |
| Leadership                                    |    15 |
| __missing__                                   |     3 |

---

## 3. KSAs by Sector

| Sector                                        | Count |
| --------------------------------------------- | ----- |
| cross_sector                                  |    56 |
| mining_extraction                             |    26 |
| maker_economy_creative_crafts                 |    25 |
| wholesale_retail_trade                        |    24 |
| nonprofit_ngos                                |    24 |
| healthcare_social_assistance                  |    24 |
| construction_infrastructure                   |    24 |
| hospitality_tourism                           |    23 |
| core_it_cloud                                 |    23 |
| administrative_support_services               |    23 |
| personal_other_services                       |    22 |
| government_public_administration              |    22 |
| media_arts_entertainment                      |    21 |
| informal_gray_economy                         |    20 |
| ai_data_quantum                               |    20 |
| environmental_energy_advanced                 |    19 |
| energy_utilities                              |    19 |
| manufacturing                                 |    18 |
| immersive_media_ar_vr_metaverse               |    18 |
| transportation_logistics                      |    17 |
| space_economy_aerospace                       |    17 |
| finance_insurance                             |    17 |
| education_training                            |    17 |
| agriculture_natural_resources                 |    17 |
| telecommunications                            |    16 |
| public_safety_security                        |    15 |
| arts_recreation_services                      |    15 |
| biotechnology_synthetic_biology               |    14 |
| real_estate_property                          |    13 |
| professional_scientific_services              |    13 |
| digital_content_creation_creator_economy      |    13 |
| blockchain_web3                               |    13 |
| unpaid_caregiving_domestic_work               |    12 |
| customer_experience_service                   |    11 |
| gig_platform_economy                          |    10 |
| creative_cultural_industries                  |    10 |
| __missing__                                   |     3 |

---

## 4. KSAs by Horizon

| Horizon                                       | Count |
| --------------------------------------------- | ----- |
| core                                          |   446 |
| emerging                                      |   186 |
| perennial                                     |    53 |
| watch_2030                                    |     6 |
| __missing__                                   |     3 |

---

## 5. Missing Optional Fields

Fields checked: `cluster_tags`, `source_frameworks`

| KSA ID | Label | Missing Fields |
| --- | --- | --- |
| `sector_adjacency_matrix` | ? | cluster_tags, source_frameworks |
| `military_to_civilian` | ? | cluster_tags, source_frameworks |
| `career_transition_explorer` | ? | cluster_tags, source_frameworks |

---

## 6. Validation Errors

### `content\Individual_KSAs\technical_ksas\_crosswalk\sector_adjacency_matrix.md`
**KSA ID:** `sector_adjacency_matrix` | **Label:** missing

  - `label`: must have required property 'label'
  - `category`: must have required property 'category'
  - `description`: must have required property 'description'
  - `sector`: must have required property 'sector'
  - `horizon`: must have required property 'horizon'
  - `proficiency_levels`: must have required property 'proficiency_levels'

### `content\Individual_KSAs\technical_ksas\_crosswalk\population_pathways\military_to_civilian.md`
**KSA ID:** `military_to_civilian` | **Label:** missing

  - `label`: must have required property 'label'
  - `category`: must have required property 'category'
  - `description`: must have required property 'description'
  - `sector`: must have required property 'sector'
  - `horizon`: must have required property 'horizon'
  - `proficiency_levels`: must have required property 'proficiency_levels'

### `content\Individual_KSAs\technical_ksas\_crosswalk\population_pathways\career_transition_explorer.md`
**KSA ID:** `career_transition_explorer` | **Label:** missing

  - `label`: must have required property 'label'
  - `category`: must have required property 'category'
  - `description`: must have required property 'description'
  - `sector`: must have required property 'sector'
  - `horizon`: must have required property 'horizon'
  - `proficiency_levels`: must have required property 'proficiency_levels'

---

## 7. Output Files

| File | Description |
| ---- | ----------- |
| `reports/ksa_inventory.json` | Full structured inventory (all 694 KSAs) |
| `reports/ksa_inventory_report.md` | This document |
| `reports/validation_errors.json` | 3 schema violation(s) with details |
