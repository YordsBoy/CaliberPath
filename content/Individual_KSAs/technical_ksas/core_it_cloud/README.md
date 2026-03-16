# Core IT & Cloud Infrastructure

## Sector Overview  
Gartner projects **global public-cloud spend to top $723 billion in 2025** as hybrid and multi-cloud strategies become the enterprise default.  HashiCorp’s *2025 Cloud Complexity Report* finds that **94 % of organizations are multi-cloud** and cite skill gaps and security as top hurdles.  The **AWS Well-Architected Framework** (six pillars) and analogous Azure/GCP guides remain the dominant reference for cloud design.  **FinOps** adoption is surging: 70 % of teams rank cost-optimization as their #1 cloud priority in the *State of FinOps 2025* survey.  Reliability culture is cemented by Google’s SRE principles, now widely implemented beyond hyperscalers.  

On the technology front, **Kubernetes powers >80 % of new cloud-native workloads** per CNCF research, while **Zero-Trust Architecture (NIST SP 800-207)** guides cloud-security transformations.  ISO/IEC 27017 and sovereign-cloud regulations drive heightened data-residency governance.  Edge-computing spend will exceed **$261 billion by 2025** according to IDC, amplifying the need for orchestration skills across the core–edge continuum.

## Sub-domains & Representative KSAs  

| Code | Sub-Domain                     | Example KSAs                                                  |
|------|--------------------------------|---------------------------------------------------------------|
| **CA** | Cloud Architecture               | Cloud-Infrastructure Architecture · Serverless Architecture   |
| **CO** | Cloud Operations & Observability | Cloud Observability Monitoring · Site-Reliability Engineering |
| **DB** | Databases & Data Stores          | Database Management                                           |
| **DV** | DevOps & Automation              | Infrastructure as Code · Kubernetes Orchestration             |
| **EC** | Edge & Distributed Computing     | Edge-Cloud Orchestration                                      |
| **FN** | FinOps & Green-Ops               | Cloud FinOps Cost Optimisation · Green-Cloud Optimisation |
| **GV** | Governance & Residency           | Cloud-Data Governance & Residency                             |
| **NW** | Networking Fundamentals          | Network Basics                                                |
| **SC** | Security & Confidential Compute  | Cloud Security Architecture · Confidential-Computing Services |
| **FD** | Fundamentals                     | Cybersecurity Fundamentals · Programming Fundamentals · Version Control |
| **SA** | System Administration & Helpdesk | System Admin · IT Support & Helpdesk Ops                      |

## Horizon Key  

| Horizon | Meaning                                           |
|---------|---------------------------------------------------|
| **core** | Widely implemented practice or mandated control   |
| **emerging** | High-growth or specialised skill (< 40 % adoption) |

## KSA Inventory  

| ID                                   | Label                                                     | Horizon   |
|--------------------------------------|-----------------------------------------------------------|-----------|
| cloud_infrastructure_architecture     | Cloud-Infrastructure Architecture                         | core      |
| serverless_architecture               | Serverless Architecture                                   | core      |
| cloud_infrastructure_management       | Cloud-Infrastructure Management                           | core      |
| cloud_observability_monitoring        | Cloud Observability & Monitoring                          | core      |
| site_reliability_engineering_practices| Site-Reliability Engineering Practices                    | core      |
| ai_ops_autonomous_remediation         | AIOps – Predictive Scaling & Autonomous Remediation       | emerging  |
| database_management                   | Database Management                                       | core      |
| devops_tooling                        | DevOps Tooling                                            | core      |
| infrastructure_as_code                | Infrastructure as Code                                    | core      |
| kubernetes_container_orchestration    | Kubernetes Container Orchestration                        | core      |
| edge_cloud_orchestration              | Edge-Cloud Orchestration                                  | core      |
| cloud_finops_cost_optimization        | Cloud FinOps Cost Optimisation                            | core      |
| green_cloud_optimisation              | Green-Cloud Optimisation                                  | emerging  |
| cloud_data_governance_residency       | Cloud-Data Governance & Residency                         | core      |
| network_basics                        | Network Basics                                            | core      |
| cloud_security_architecture           | Cloud Security Architecture                               | core      |
| identity_access_management_cloud      | Identity & Access Management (Cloud)                      | core      |
| confidential_computing_services       | Confidential-Computing Services                           | emerging  |
| it_support_helpdesk_operations        | IT Support & Helpdesk Operations                          | core      |
| system_admin                          | System Administration                                     | core      |
| cybersecurity_fundamentals            | Cybersecurity Fundamentals                                | perennial |
| programming_fundamentals              | Programming Fundamentals                                  | core      |
| version_control                       | Version Control & Collaboration                           | core      |

## Referenced Frameworks & Standards  

- **Gartner Market Guide for AIOps Platforms 2024** – five functional pillars for AIOps platforms.
- **Google Cloud predictive-autoscaling docs 2025** – ML-based scaling patterns for cloud ops.
- **BigQuery Anomaly-Detection overview** – cloud telemetry ML detection. 
- **Confidential Computing Consortium specifications (2024)** – enclave architecture & attestation flows. 
- **NIST SP 800-207A (draft)** – Zero-Trust patterns incorporating confidential compute. 
- **Azure confidential-VM portfolio update 2025** – market adoption evidence for confidential services.
- **Green Software Foundation – Carbon-Awareness principles (2024)** – dynamic workload scheduling by grid intensity.
- **Microsoft & UBS Carbon-Aware Computing white paper 2023** – operational tactics for green-ops pipelines.
- **EU Energy-Efficiency Directive 2023 (Data-center clauses)** – mandatory carbon reporting; drives green-cloud KPIs.
- **FinOps Foundation State of FinOps 2025** – carbon + cost metrics in cloud-financial-ops.
- **Gartner Cloud-Spending Forecast 2025 —** Predicts worldwide public-cloud end-user spending will reach **USD 723 billion in 2025**, with every service segment posting double-digit growth; underpins FinOps cost-optimization KPIs.
- **HashiCorp *Cloud Complexity Report* 2025 —** Survey of 1 100 IT leaders: 86 % run multi-cloud, with skills gaps and security cited as top complexity drivers—context for AIOps and Governance KSAs.
- **AWS Well-Architected Framework (2023) —** Six pillars—operational excellence, security, reliability, performance efficiency, cost optimization, sustainability—provide design guardrails for Cloud Architecture KSAs. 
- **Google *Site Reliability Engineering* (2023) —** Google’s SRE handbook detailing SLIs/SLOs, error budgets, and toil reduction; forms the foundation of Site-Reliability Engineering Practices.
- **FinOps Foundation *State of FinOps 2025* —** Benchmarks from 1 200+ practitioners on cloud-cost optimization and emerging carbon-aware metrics, informing both FinOps and Green-Ops KSAs.  
- **CNCF Kubernetes Adoption Survey 2025 —** Reports over 96 % of large enterprises run Kubernetes in production, with AI/ML workloads the fastest-growing use-case—validates Kubernetes Orchestration KSA maturity.
- **NIST SP 800-207 *Zero-Trust Architecture* —** Defines abstract ZTA model, deployment use-cases, and implementation guidelines leveraged in Confidential-Computing and Cloud-Security Architecture KSAs.
- **ISO/IEC 27017 — Cloud Security Controls —** Adds cloud-specific implementation guidance to ISO 27002, covering multi-tenancy, virtualisation, and shared-responsibility—baseline for Cloud-Security Architecture.
- **IDC Edge-Computing Spending Guide 2025 —** Forecasts **USD 261 billion** in global edge-computing spend for 2025, rising at a 13.8 % CAGR—supports Edge-Cloud Orchestration horizon classification.

## Future-Expansion  

| Area | Why it matters |
|------|----------------|
| **Quantum-Safe Cloud Networking** | Preparing TLS, VPN, and key management for post-quantum crypto algorithms. |
| **Autonomous Cloud Recovery via Reinforcement Learning** | RL agents that learn rollback vs. roll-forward strategies to minimise downtime. |
| **Sovereign-Cloud Trust Frameworks** | Policy-defined controls for data residency and lawful-access segmentation. |
| **Serverless on the Edge (WASM)** | Lightweight WebAssembly workloads deployed to micro edge-locations for ultra-low latency. |

> *All sources cited for conceptual alignment. No proprietary text copied.*

_Last updated: 17 Oct 2025_
## Labor Market Context
*Populated by T-README-02 | Data source: BLS OES + O\*NET + sector workforce studies*

**BLS Total Employment (current):** ~5.6 million in Computer and Information Technology Occupations (SOC 15-0000, estimated from BLS OES May 2024). Largest sub-groups: Software developers and QA analysts (~2.0M); Computer systems analysts (~650K); Information security analysts (~180K); Computer and information systems managers (~900K); Network architects and administrators (~500K); Computer support specialists (~770K).

**BLS 10-Year Projected Growth (% / absolute jobs):** Overall computer and IT occupations: much faster than average 2024–2034; ~317,700 openings projected per year (BLS OOH). Key sub-group projections: Information security analysts: +29% / +57,200 jobs; Computer and information systems managers: +15% / +136,400 jobs; Computer systems analysts: +9%; Software developers: +17% / +327,300 jobs. Cloud-specific roles are fastest-growing sub-segment, driven by AI workload migration to cloud infrastructure.

**Median Annual Wage:** $105,990 (Computer and IT Occupations group median, BLS OOH May 2024). By sub-group: Computer and information systems managers: $171,200; Information security analysts: $124,910; Cloud architects/network architects: ~$130,000–$145,000; Systems administrators: ~$90,520; IT support specialists: ~$60,000–$75,000.

**Top O\*NET SOC Codes and Titles (5–8):**
- 11-3021.00 — Computer and Information Systems Managers
- 15-1211.00 — Computer Systems Analysts
- 15-1212.00 — Information Security Analysts
- 15-1241.00 — Computer Network Architects
- 15-1244.00 — Network and Computer Systems Administrators
- 15-1252.00 — Software Developers
- 15-1232.00 — Computer User Support Specialists
- 15-1231.00 — Computer Network Support Specialists

**Common Entry-Level Titles:** IT Support Specialist (Tier 1/2), Cloud Support Associate, Junior Systems Administrator, DevOps Associate, Network Technician, Junior Security Analyst

**Common Mid-Career / Senior Titles:** Cloud Architect, Site Reliability Engineer, DevOps Engineer, Senior Network Engineer, Cloud Security Engineer, IT Director, Principal Systems Engineer

**Emerging / watch_2030 Roles:** FinOps Engineer (cloud cost optimization), Green Cloud Specialist (sustainability-optimized compute), Confidential Computing Engineer (privacy-preserving cloud workloads)

**CSRA Employment Density:** Georgia Cyber Center (~300+ cybersecurity professionals and trainers), Fort Gordon GS civilians in IT/cyber roles (~3,000+), defense contractors (SAIC, Leidos, Booz Allen, ManTech) with Augusta presence (~4,000–6,000 IT/cyber workers combined), Augusta University IT staff (~400). Estimated 8,000–12,000 IT/cloud workers in Augusta MSA. Georgia statewide computer/IT occupations: ~250,000–280,000 (BLS OES 2024 estimate).

**Data Last Verified:** 2026-03-15

## Transfer Pathways
*Populated by T-CROSSWALK-03 | Data source: Sector Adjacency Matrix (_crosswalk/sector_adjacency_matrix.md)*

**Top Adjacent Sectors — Inbound (sectors that transfer into this one readily):**
AI, Data & Quantum (Score: MEDIUM, 4 shared tags) — Data engineers and ML practitioners bring cloud architecture, DevOps, and platform engineering skills that map directly to IT infrastructure and cloud operations roles.
Mining & Extraction (Score: LOW, 3 shared tags) — OT/IT integration specialists from industrial environments bring operational technology, systems management, and infrastructure maintenance skills applicable to enterprise IT.
Telecommunications (Score: LOW, 2 shared tags) — Network engineers and systems integrators transition into cloud networking, infrastructure architecture, and managed services roles.

**Top Adjacent Sectors — Outbound (sectors this one transfers out to readily):**
AI, Data & Quantum (Score: MEDIUM, 4 shared tags) — Cloud architects and DevOps engineers transition into AI/ML platform engineering, data infrastructure development, and MLOps roles.
Mining & Extraction (Score: LOW, 3 shared tags) — IT specialists and systems administrators move into OT/IT convergence, industrial IoT, and smart operations roles in resource-intensive industries.
Telecommunications (Score: LOW, 2 shared tags) — Network architects and systems engineers transition into telecommunications infrastructure, software-defined networking, and carrier technology roles.

**Bridging Cluster Tags:**
Cloud Architecture, Cybersecurity, DevOps

**Common Transition Populations:**
military_transition, mid_career_change, education_to_industry

**Typical Entry Roles for Career Changers:**
Cloud Administrator, Network Administrator, IT Support Specialist
