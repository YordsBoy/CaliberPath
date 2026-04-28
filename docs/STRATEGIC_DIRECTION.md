# CaliberPath Strategic Direction

**Architectural Context for Development**
**Last Updated:** April 2026
**Status:** Authoritative — This document governs all development priorities

---

## Executive Summary

CaliberPath has evolved from its original conception as an AI-powered self-reflection platform into a Learning & Development (L&D) company built around the UPLS competency framework + 400+ technical KSAs. The delivery model centers on human coaching and workshops, augmented by a digital application surface for intake, assessment, and tiered delivery.

The Digital-First Decision Memo (2026-04-20) and the Hybrid Repository Architecture decision DR_WebPlatform_RepoArchitecture_v1 (2026-04-24, registered LSA v4.17) pulled the application phase forward from 2027–2028 to 2026 Q2–Q3. This document was previously organized around a three-phase roadmap (Human-Delivered → Technology-Augmented → AI-Native, ending 2028+); it is now organized around a four-phase framework with the application surface as the near-term critical path.

Under the Hybrid architecture, this repo (KSA-REPO) becomes the application at `app.caliberpath.com`.

This document clarifies what is active, what is near-term, and how the codebase should be understood.

---

## The Four Phases of CaliberPath

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: CONTENT & PIPELINE FOUNDATION (CURRENT — 2026)                    │
│  ══════════════════════════════════════════════════════                     │
│                                                                             │
│  Business Model:                                                            │
│  • B2C: Career coaching, self-mastery workshops, bootcamps                  │
│  • B2B: Leadership academies, competency consulting, custom training        │
│  • Revenue: Service fees, program tuition, consulting retainers             │
│                                                                             │
│  Technology Role:                                                           │
│  • Competency database (UPLS + technical KSAs) powers curriculum design     │
│  • Manual intake → human interpretation → personalized delivery             │
│  • ReportLab pipeline integration prepared (Layer 3 rendering)              │
│                                                                             │
│  Active Development:                                                        │
│  • KSA content maintenance and expansion                                    │
│  • Schemas, validation, build chain                                         │
│  • Documentation and methodology codification                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: APPLICATION SURFACE — PULLED FORWARD (2026 Q2–Q3)                 │
│  ════════════════════════════════════════════════════════                   │
│                                                                             │
│  Business Model:                                                            │
│  • Self-serve $97 automated tier via app.caliberpath.com                    │
│  • Coaching and workshops continue alongside the digital surface            │
│  • Per-tier purchase model (NOT recurring subscription SaaS)                │
│                                                                             │
│  Technology Role:                                                           │
│  • Next.js application at app.caliberpath.com (this repo, under Hybrid)     │
│  • Digital intake forms with routing logic                                  │
│  • Competency self-assessment                                               │
│  • Payment processing for $97 automated tier                                │
│  • Delivery dashboard for client output                                     │
│  • Layer 3 rendering integration (ReportLab pipeline)                       │
│                                                                             │
│  Development Focus:                                                         │
│  • Application scaffolding (after full Web Platform Architecture Spec)      │
│  • Intake → assessment → payment → delivery flow                            │
│  • Schema and data outputs consumed by the application surface              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: AI-ASSISTED TIER (NEAR-TERM — 2026 Q3–Q4)                         │
│  ════════════════════════════════════════════════                           │
│                                                                             │
│  Business Model:                                                            │
│  • $197 AI-assisted tier layered on the Phase 2 application surface         │
│  • Coach-portal surfaces support human coaching alongside AI assistance     │
│                                                                             │
│  Technology Role:                                                           │
│  • Layer 2 integration via OI-GAR-V2                                        │
│  • AI assistance integrated into intake / assessment / delivery flows       │
│  • Coach-portal surfaces for facilitator workflows                          │
│                                                                             │
│  Development Focus:                                                         │
│  • Layer 2 integration                                                      │
│  • Coach-portal feature set                                                 │
│  • AI-assisted tier productization                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: SCALE & EXPANSION (LONGER-TERM)                                   │
│  ═══════════════════════════════════════                                    │
│                                                                             │
│  Business Model:                                                            │
│  • B2B aggregate tier for organizational clients                            │
│  • Geographic expansion templating beyond Augusta market                    │
│                                                                             │
│  Technology Role:                                                           │
│  • B2B aggregate dashboards and reporting                                   │
│  • Geographic expansion templating                                          │
│  • Advanced analytics across cohorts and tiers                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

> The `flows/` directory in this repo (7-day AI intake + post-intake companion model) was authored under the prior AI-first conception of CaliberPath. It is preserved as reference material and will be reassessed against the four-phase framework when Phase 3 work begins — it is no longer the canonical Phase 3 design.

---

## Codebase Inventory by Phase

### PHASE 1 — ACTIVE (Maintain & Develop)

These directories and files are the current operational core:

| Path | Purpose | Status |
|------|---------|--------|
| `content/Individual_KSAs/` | 400+ competency definitions (UPLS + technical) | CORE ASSET — Active maintenance |
| `content/Individual_KSAs/professionalism/` | 15 Professionalism Competencies | CORE ASSET |
| `content/Individual_KSAs/leadership_influence/` | 15 Leadership Competencies | CORE ASSET |
| `content/Individual_KSAs/self_management_personal_mastery/` | 15+ Self-Mastery Competencies | CORE ASSET |
| `content/Individual_KSAs/technical_ksas/` | Sector-specific competencies (35 sectors) | CORE ASSET |
| `schemas/ksa.schema.json` | KSA validation schema | ACTIVE — Maintain |
| `scripts/build_ksa_json.js` | Compiles KSAs to master JSON | ACTIVE — Maintain |
| `scripts/validate_ksas.js` | Schema validation | ACTIVE — Maintain |
| `data/master_ksa.json` | Compiled KSA output | ACTIVE — Regenerate as needed |
| `docs/` | Documentation (architecture, guides) | ACTIVE — Update for L&D focus |

### PRESERVED — Pre-Revision AI Companion Content

These directories contain the AI companion design from the prior AI-first conception. They are preserved as reference material and will be reassessed against the four-phase framework when Phase 3 (AI-assisted tier) work begins. They are **not** the canonical Phase 3 design under the current framework.

| Path | Purpose | Status |
|------|---------|--------|
| `flows/intake/` | 7-day AI-guided onboarding journey | PRESERVED — reassess at Phase 3 |
| `flows/intake/day1_tone_safety.md` | Day 1: Tone calibration, emotional safety | PRESERVED |
| `flows/intake/day2_adaptive.md` | Day 2: Adaptive conversation paths | PRESERVED |
| `flows/intake/day3_*.md` | Day 3: Belief exploration | PRESERVED |
| `flows/intake/day4_belief_value.md` | Day 4: Value integration | PRESERVED |
| `flows/intake/day5_*.md` | Day 5: Purpose articulation | PRESERVED |
| `flows/intake/day6_*.md` | Day 6: Shadow integration | PRESERVED |
| `flows/intake/day7_closure_future.md` | Day 7: Closure and signal transfer | PRESERVED |
| `flows/post_intake/` | Ongoing AI companion model | PRESERVED — reassess at Phase 3 |
| `flows/post_intake/companion_model.md` | Memory integration, cadence, modes | PRESERVED |
| `flows/post_intake/visual_companion_ind.jsx` | React component for companion UI | PRESERVED |
| `docs/architecture/global_memory_map__0_architecture_spec.md` | AI memory system | PRESERVED |
| `docs/architecture/implementation_blueprint.md` | AI UX and memory design | PRESERVED |

### PHASE 2 — TO BE BUILT (Pulled forward to 2026 Q2–Q3)

These capabilities form the application surface at `app.caliberpath.com`. Scaffolding work is sequenced after the full Web Platform Architecture Specification is filed; do not begin implementation until that specification is in hand.

| Capability | Description | Priority |
|------------|-------------|----------|
| Digital Intake Forms | B2C and B2B intake as web forms | HIGH |
| Competency Self-Assessment | Users rate themselves on relevant KSAs | HIGH |
| $97 Automated-Tier Payment | Per-tier purchase processing (not subscription) | HIGH |
| Delivery Dashboard | Client-facing output of automated tier | HIGH |
| Layer 3 Rendering Integration | ReportLab pipeline integration | HIGH |
| Gap Analysis Visualizer | Shows competency gaps vs. goals | MEDIUM |
| Learning Path Generator | Recommends CaliberPath offerings based on gaps | MEDIUM |
| Client Portal | Progress tracking, resource access, scheduling | MEDIUM |

### PHASE 3 — TO BE BUILT (2026 Q3–Q4)

| Capability | Description | Priority |
|------------|-------------|----------|
| $197 AI-Assisted Tier | AI assistance layered on the Phase 2 application | HIGH |
| Layer 2 Integration | OI-GAR-V2 integration | HIGH |
| Coach Portal | Facilitator workflows alongside AI-assisted tier | HIGH |

### PHASE 4 — TO BE BUILT (Longer-term)

| Capability | Description | Priority |
|------------|-------------|----------|
| B2B Aggregate Tier | Organizational dashboards and reporting | TBD |
| Geographic Expansion Templating | Templating beyond Augusta market | TBD |
| Advanced Analytics | Cross-cohort and cross-tier analytics | TBD |

### REQUIRES REVIEW (May Need Redesign)

These components were built for the prior subscription-SaaS framing. Under Option C (Hybrid architecture), this repo IS becoming a Next.js application — but with per-tier purchase ($97 automated, $197 AI-assisted), not recurring subscription. These components likely need redesign for the tier-purchase model.

| Path | Original Purpose | Review Needed |
|------|-----------------|---------------|
| `components/UserTierContext.js` | SaaS tier gating (free/pro/team/enterprise) | Redesign for tier-purchase model |
| `pages/_app.js` | App wrapper with tier provider | Review tier logic |
| `pages/test.js` | Tier testing page | May be obsolete |
| Stripe integration | Subscription billing | Reconfigure for per-tier purchase |
| `README.md` | Describes "self-reflection platform" | REWRITE for L&D company with application surface |

---

## UPLS Framework — The Core Methodology

The **Professionalism, Leadership & Influence, and Self-Mastery (UPLS)** competency framework is CaliberPath's signature methodology. It consists of:

### Professionalism Competencies (15)

Foundational skills for all professionals:

- Accountability
- Adaptability
- Attention to Detail
- Collaboration
- Creative Thinking
- Critical Thinking
- Digital Literacy
- Effective Communication
- Emotional Intelligence
- Initiative
- Learning Agility
- Professionalism
- Resilience
- Self-Motivation
- Time Management

### Leadership & Influence Competencies (15)

Skills for leading people and driving outcomes:

- Change Analytics & Sentiment Monitoring
- Change Leadership
- Conflict Resolution
- Crisis Leadership
- Delegation & Empowerment
- Ethical Governance
- Inclusive Leadership
- Mentoring & Coaching
- Persuasion & Negotiation
- Remote & Hybrid Team Leadership
- Stakeholder Coalition Building
- Strategic Communication
- Strategic Thinking
- Team Building
- Vision Setting

### Self-Mastery Competencies (15+)

Internal capabilities for personal excellence:

- **Habits & Productivity:** Deep Work Practice, Digital Minimalism, Energy Management
- **Intrinsic Motivation:** Purpose Articulation
- **Self-Awareness:** Identity Self-Authorship, Metacognition, Self-Reflective Insight
- **Self-Regulation:** Attention Switching & Focus, Impulse Control
- **Values & Ethics:** Ethical Reflection & Reasoning, Integrity Alignment, Moral Courage
- **Well-Being & Resilience:** Growth Mindset, Sensory Mindfulness, Stress Management

---

## CaliberPath Offerings (Phase 1)

### B2C Services

| Offering | Description | Competency Focus |
|----------|-------------|-----------------|
| Career Compass Coaching | 1:1 coaching program (6-12 sessions) | Full UPLS assessment and development |
| Self-Mastery Workshop Series | Group workshops (4-8 weeks) | Self-Mastery competencies |
| Career Accelerator Bootcamp | Intensive cohort program | Professionalism + Leadership |
| Alumni Mastermind | Ongoing peer support | Continued growth |

### B2B Services

| Offering | Description | Competency Focus |
|----------|-------------|-----------------|
| Rising Leaders Academy | Leadership development cohort | Leadership competencies |
| Competency Consulting | Custom competency model development | Client-specific + UPLS integration |
| Custom Training Design | Curriculum for client needs | Sector-specific technical KSAs |
| Executive Coaching | 1:1 coaching for leaders | Leadership + Self-Mastery |

---

## Market Context

**Primary Market:** Augusta, GA region (CSRA)

**Priority Verticals:**

- **Healthcare** — Augusta University Health, regional hospitals
- **Cybersecurity/IT** — Fort Gordon, Army Cyber Command ecosystem
- **Manufacturing** — Regional manufacturing base
- **Military/Veteran** — Transition services, military spouse support

**Competitive Advantage:**

- Local presence and cultural understanding
- Comprehensive competency framework (not just generic coaching)
- ADDIE-grounded instructional design methodology
- Accessible pricing for regional market

---

## Development Principles for Current Phase

### DO:

- Maintain and expand KSA content (Phase 1 core)
- Prepare schemas, content structure, and data outputs for ReportLab pipeline integration (Layer 3)
- Create documentation that codifies methodology
- Design content and data outputs so the Phase 2 application surface (intake, assessment, $97 automated tier) can consume them directly
- Keep `flows/` preserved as reference for the eventual Phase 3 reassessment

### DO NOT:

- Begin Next.js application scaffolding for `app.caliberpath.com` until the full Web Platform Architecture Specification is filed
- Build subscription-SaaS billing infrastructure — Phase 2 payment is per-tier purchase ($97 automated, $197 AI-assisted), not recurring subscription
- Treat the 7-day intake flow as the canonical Phase 3 design — it predates the four-phase revision and will be reassessed
- Develop features that bypass the human coach surface in Phase 1 deliveries

### ARCHITECTURE GUIDANCE:

- Competency data is the foundation — keep it clean and complete
- Phase 2 application surface and Phase 3 coach portal should both treat KSA-REPO data as authoritative
- Client-facing technology should enhance the human coaching relationship, not replace it
- Schema and data outputs are the contract between this repo and downstream consumers (Layer 2 / Layer 3 / application surface)

---

## File Organization Recommendations

### Suggested Layout

```
CaliberPath/
├── CLAUDE.md                    # Claude Code context
├── README.md                    # REWRITE — L&D company with application surface
├── content/
│   └── Individual_KSAs/         # CORE ASSET — maintain actively
├── schemas/                     # ACTIVE — maintain
├── scripts/                     # ACTIVE — maintain
├── data/                        # ACTIVE — regenerate as needed
├── docs/
│   ├── STRATEGIC_DIRECTION.md   # THIS DOCUMENT
│   ├── methodology/             # L&D methodology documentation
│   ├── offerings/               # Service descriptions
│   └── architecture/            # Technical architecture
├── flows/                       # PRESERVED — reassess at Phase 3 (see note below)
├── components/                  # REVIEW — needs redesign for tier-purchase model
├── pages/                       # REVIEW — needs redesign for tier-purchase model
└── [Phase 2 application directories TBD per Web Platform Architecture Spec]
```

### Note on `flows/` Disposition

The `flows/` directory contains the original AI companion design (7-day intake + post-intake companion model) authored under the prior AI-first conception of CaliberPath.

Under the four-phase framework, "Phase 3" refers to the AI-assisted tier ($197) layered on the Phase 2 application surface — **not** the AI companion model in `flows/`. The companion design is preserved as reference material and will be reassessed against the new framework when Phase 3 work begins. Do not archive or delete it preemptively, but do not treat it as the canonical Phase 3 design.

---

## Integration Points

### External Systems (Current)

- **Claude.ai Projects** — Strategic content generation, analysis
- **GitHub Repository** — Competency database, version control
- **Claude Code** — Technical implementation, scripts, validation

### External Systems (Phase 2 — 2026 Q2–Q3)

- **CRM** (HubSpot or similar) — Client management
- **Scheduling tool** (Calendly or similar) — Session booking
- **Payment processor** — Per-tier purchase ($97 automated tier; $197 AI-assisted at Phase 3) — not recurring subscription
- **ReportLab pipeline** — Layer 3 rendering integration

### External Systems (Phase 3 — 2026 Q3–Q4)

- **OI-GAR-V2** — Layer 2 integration for AI-assisted tier

### Data Flow

```
Competency Database (KSA-REPO / GitHub)
         │
         ▼
Claude.ai Projects ←→ Strategic Documents (Handbook, Curriculum)
         │
         ▼
Claude Code → Validation, Reports, Exports, ReportLab pipeline prep
         │
         ▼
[Phase 2] app.caliberpath.com → Intake, Assessment, $97 Payment, Delivery Dashboard, Layer 3 Rendering
         │
         ▼
[Phase 3] AI-Assisted Tier ($197) + Coach Portal → Layer 2 (OI-GAR-V2)
         │
         ▼
[Phase 4] B2B Aggregate Tier, Geographic Expansion, Advanced Analytics
```

---

## Success Metrics by Phase

### Phase 1 Success (2026)

- [ ] KSA content complete and validated (build chain green)
- [ ] Schemas and data outputs ready to feed the Phase 2 application surface
- [ ] ReportLab pipeline integration prepared (Layer 3)
- [ ] Methodology documented and repeatable
- [ ] Initial coaching/workshop revenue established

### Phase 2 Success (2026 Q2–Q3)

- [ ] `app.caliberpath.com` live (Next.js application surface, this repo)
- [ ] Digital intake operational
- [ ] Self-assessment tools deployed
- [ ] $97 automated-tier payment flow operational (per-tier purchase, not subscription)
- [ ] Delivery dashboard rendering output via Layer 3
- [ ] First clients served through the digital surface

### Phase 3 Success (2026 Q3–Q4)

- [ ] $197 AI-assisted tier launched
- [ ] Layer 2 integration (OI-GAR-V2) operational
- [ ] Coach portal in production use by facilitators
- [ ] Hybrid human + AI-assisted delivery model proven

### Phase 4 Success (Longer-term)

- [ ] B2B aggregate tier serving organizational clients
- [ ] Geographic expansion templating in use beyond Augusta
- [ ] Advanced analytics across cohorts and tiers

---

## Governance

This document is authoritative for development priorities.

Updates require:
1. Strategic review in Claude.ai Projects
2. Documentation of rationale
3. Update to `CLAUDE.md` if development priorities change

### Authority Trail

- Digital-First Decision Memo (2026-04-20) — pulled the application phase forward
- DR_WebPlatform_RepoArchitecture_v1 (2026-04-24, registered LSA v4.17) — adopted Hybrid (Option C); KSA-REPO becomes the application surface at `app.caliberpath.com`
- Strategist → Claude Code handoff `2026-04-24_Strategist-to-CC_KSARepo_CLAUDEmd_PhaseFrameworkRevision_v1` — authorized this revision

**Last Reviewed:** April 2026
**Next Review:** Upon filing of the full Web Platform Architecture Specification (precondition for Phase 2 scaffolding)

---

## Quick Reference for Claude Code

When working in this repository:

| If you're asked to... | Priority | Action |
|----------------------|----------|--------|
| Modify KSA content | HIGH | Proceed — Phase 1 core |
| Run validation scripts | HIGH | Proceed — maintain quality |
| Update documentation | HIGH | Proceed — support methodology |
| Prepare schemas/data outputs for ReportLab pipeline | HIGH | Proceed — Phase 1 critical |
| Begin Next.js application scaffolding for `app.caliberpath.com` | BLOCKED | Wait — requires Web Platform Architecture Specification first |
| Build intake / assessment / payment / delivery for $97 tier | NEAR-TERM | Phase 2 (2026 Q2–Q3) — plan against the Web Platform Architecture Spec |
| Develop AI-assisted tier or coach portal | PLANNED | Phase 3 (2026 Q3–Q4) — defer until Phase 2 ships |
| Develop `flows/` content | DO NOT | Pre-revision AI companion design — preserve only; reassess at Phase 3 |
| Build subscription-SaaS billing | DO NOT | Payment is per-tier purchase, not recurring subscription |

> **When in doubt, reference this document.**
