# CaliberPath Strategic Direction

**Architectural Context for Development**
**Last Updated:** February 2026
**Status:** Authoritative — This document governs all development priorities

---

## Executive Summary

CaliberPath has evolved from its original conception as an AI-powered self-reflection platform into a Learning & Development (L&D) company that delivers human-led coaching, workshops, and consulting services. The competency framework (UPLS + 400+ technical KSAs) remains the core intellectual property, but the delivery model has shifted from AI-first to human-first with technology augmentation.

This document clarifies what is active, what is deferred, and how the codebase should be understood.

---

## The Three Phases of CaliberPath

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: HUMAN-DELIVERED CALIBERPATH (CURRENT — 2026-2027)                    │
│  ══════════════════════════════════════════════════════                     │
│                                                                             │
│  Business Model:                                                            │
│  • B2C: Career coaching, self-mastery workshops, bootcamps                  │
│  • B2B: Leadership academies, competency consulting, custom training        │
│  • Revenue: Service fees, program tuition, consulting retainers             │
│                                                                             │
│  Technology Role:                                                           │
│  • Competency database powers curriculum design                             │
│  • Manual intake → human interpretation → personalized delivery             │
│  • Marketing website, basic booking/payment                                 │
│                                                                             │
│  Active Development:                                                        │
│  • KSA content maintenance and expansion                                    │
│  • Documentation and methodology codification                               │
│  • Basic web presence                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: TECHNOLOGY-AUGMENTED CALIBERPATH (PLANNED — 2027-2028)               │
│  ═════════════════════════════════════════════════════════                  │
│                                                                             │
│  Business Model:                                                            │
│  • Hybrid: Human coaching + online learning platform                        │
│  • Self-paced courses extend reach beyond 1:1 capacity                      │
│  • B2B clients get dashboards and progress tracking                         │
│                                                                             │
│  Technology Role:                                                           │
│  • Digital intake forms with routing logic                                  │
│  • Competency self-assessment tools                                         │
│  • Learning path generator based on gap analysis                            │
│  • Client portal for progress tracking                                      │
│  • Coach/facilitator dashboard                                              │
│                                                                             │
│  Development Focus:                                                         │
│  • Assessment engine                                                        │
│  • Learning management features                                             │
│  • Client and coach interfaces                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: AI-NATIVE CALIBERPATH (FUTURE — 2028+)                               │
│  ════════════════════════════════════════════                               │
│                                                                             │
│  Business Model:                                                            │
│  • AI-augmented coaching at scale                                           │
│  • Human coaches handle complex cases; AI handles ongoing support           │
│  • Tiered access: free AI support → premium human coaching                  │
│                                                                             │
│  Technology Role:                                                           │
│  • AI companion for continuous reflection and growth                        │
│  • Dynamic memory integration across sessions                               │
│  • Tone calibration and emotional intelligence                              │
│  • Automated insight synthesis and pattern recognition                      │
│                                                                             │
│  This is the ORIGINAL VISION — now properly sequenced after                 │
│  establishing credibility and methodology through human delivery.           │
└─────────────────────────────────────────────────────────────────────────────┘
```

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

### PHASE 3 — DEFERRED (Preserve, Do Not Develop)

These directories contain the original AI companion vision. They should be preserved for future use but are not current development priorities:

| Path | Purpose | Status |
|------|---------|--------|
| `flows/intake/` | 7-day AI-guided onboarding journey | DEFERRED — Phase 3 |
| `flows/intake/day1_tone_safety.md` | Day 1: Tone calibration, emotional safety | DEFERRED |
| `flows/intake/day2_adaptive.md` | Day 2: Adaptive conversation paths | DEFERRED |
| `flows/intake/day3_*.md` | Day 3: Belief exploration | DEFERRED |
| `flows/intake/day4_belief_value.md` | Day 4: Value integration | DEFERRED |
| `flows/intake/day5_*.md` | Day 5: Purpose articulation | DEFERRED |
| `flows/intake/day6_*.md` | Day 6: Shadow integration | DEFERRED |
| `flows/intake/day7_closure_future.md` | Day 7: Closure and signal transfer | DEFERRED |
| `flows/post_intake/` | Ongoing AI companion model | DEFERRED — Phase 3 |
| `flows/post_intake/companion_model.md` | Memory integration, cadence, modes | DEFERRED |
| `flows/post_intake/visual_companion_ind.jsx` | React component for companion UI | DEFERRED |
| `docs/architecture/global_memory_map__0_architecture_spec.md` | AI memory system | DEFERRED |
| `docs/architecture/implementation_blueprint.md` | AI UX and memory design | DEFERRED |

### PHASE 2 — TO BE BUILT (Not Yet Present)

These capabilities need to be developed for the technology-augmented phase:

| Capability | Description | Priority |
|------------|-------------|----------|
| Digital Intake Forms | B2C and B2B intake as web forms | HIGH |
| Competency Self-Assessment | Users rate themselves on relevant KSAs | HIGH |
| Gap Analysis Visualizer | Shows competency gaps vs. goals | HIGH |
| Learning Path Generator | Recommends CaliberPath offerings based on gaps | MEDIUM |
| Client Portal | Progress tracking, resource access, scheduling | MEDIUM |
| Coach Dashboard | Client overview, session notes, competency tracking | MEDIUM |
| Assessment Engine | Formal pre/post assessments tied to programs | MEDIUM |
| Organizational Dashboard | B2B aggregate view of team competencies | LOW (Phase 2b) |

### REQUIRES REVIEW (May Need Redesign)

These components were built for the SaaS model and may need reconfiguration:

| Path | Original Purpose | Review Needed |
|------|-----------------|---------------|
| `components/UserTierContext.js` | SaaS tier gating (free/pro/team/enterprise) | Redesign for service model |
| `pages/_app.js` | App wrapper with tier provider | Review tier logic |
| `pages/test.js` | Tier testing page | May be obsolete |
| Stripe integration | Subscription billing | Reconfigure for invoicing |
| `README.md` | Describes "self-reflection platform" | REWRITE for L&D company |

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

- Maintain and expand KSA content
- Build tools that support human-delivered services
- Create documentation that codifies methodology
- Design with Phase 2 in mind (digital intake, assessments)
- Keep Phase 3 code preserved but clearly separated

### DO NOT:

- Invest development time in AI companion features
- Build SaaS subscription infrastructure
- Treat the 7-day intake flow as current priority
- Develop features that bypass human coaches

### ARCHITECTURE GUIDANCE:

- Competency data is the foundation — keep it clean and complete
- Any new features should support coaches/facilitators, not replace them
- Client-facing technology should enhance the human relationship
- Data collection should feed into human decision-making

---

## File Organization Recommendations

### Suggested Restructure

```
CaliberPath/
├── CLAUDE.md                    # Claude Code context (create after this doc)
├── README.md                    # REWRITE for L&D company positioning
├── content/
│   └── Individual_KSAs/         # CORE ASSET — maintain actively
├── schemas/                     # ACTIVE — maintain
├── scripts/                     # ACTIVE — maintain
├── data/                        # ACTIVE — regenerate as needed
├── docs/
│   ├── STRATEGIC_DIRECTION.md   # THIS DOCUMENT
│   ├── methodology/             # L&D methodology documentation
│   ├── offerings/               # Service descriptions
│   └── architecture/            # Technical architecture (review for relevance)
├── _archive/
│   └── phase3_ai_companion/     # MOVE deferred flows/ content here
│       ├── intake/
│       └── post_intake/
├── components/                  # REVIEW — what's needed for Phase 2?
├── pages/                       # REVIEW — what's needed for Phase 2?
└── [Phase 2 directories TBD]
```

### Archiving Phase 3 Content

The `flows/` directory should be moved to `_archive/phase3_ai_companion/` with a README explaining:

```markdown
# Phase 3 Archive — AI Companion System

This directory contains the original AI companion design for CaliberPath.
These features are DEFERRED until Phase 3 (2028+).

## Contents
- intake/ — 7-day AI-guided onboarding journey
- post_intake/ — Ongoing AI companion model

## Status
Preserved for future development. Do not actively develop.
The L&D company must be established (Phase 1) and technology-augmented
(Phase 2) before these features become priority.

## Reactivation
When Phase 3 begins, these designs will be reviewed and updated to
integrate with the competency framework and client data accumulated
in Phases 1-2.
```

---

## Integration Points

### External Systems (Current)

- **Claude.ai Projects** — Strategic content generation, analysis
- **GitHub Repository** — Competency database, version control
- **Claude Code** — Technical implementation, scripts, validation

### External Systems (Phase 2 — Planned)

- **CRM** (HubSpot or similar) — Client management
- **Scheduling tool** (Calendly or similar) — Session booking
- **Payment processor** — Invoicing (not subscription)
- **Learning platform** — Course delivery

### Data Flow

```
Competency Database (GitHub)
         │
         ▼
Claude.ai Projects ←→ Strategic Documents (Handbook, Curriculum)
         │
         ▼
Claude Code → Validation, Reports, Exports
         │
         ▼
[Phase 2] Client Tools → Intake, Assessment, Progress Tracking
         │
         ▼
[Phase 3] AI Companion → Ongoing support, reflection, growth
```

---

## Success Metrics by Phase

### Phase 1 Success (2026-2027)

- [ ] 50+ B2C clients served
- [ ] 5+ B2B organizational clients
- [ ] Revenue covering founder's financial obligations
- [ ] Methodology documented and repeatable
- [ ] Local reputation established in Augusta market

### Phase 2 Success (2027-2028)

- [ ] Digital intake forms operational
- [ ] Self-assessment tools deployed
- [ ] Online learning platform launched
- [ ] Client portal functional
- [ ] 50% of clients using digital tools

### Phase 3 Success (2028+)

- [ ] AI companion MVP launched
- [ ] Hybrid human-AI delivery model proven
- [ ] Scalable beyond founder's personal capacity
- [ ] Original vision realized with sustainable foundation

---

## Governance

This document is authoritative for development priorities.

Updates require:
1. Strategic review in Claude.ai Projects
2. Documentation of rationale
3. Update to `CLAUDE.md` if development priorities change

**Last Reviewed:** February 2026
**Next Review:** Upon Phase 2 initiation

---

## Quick Reference for Claude Code

When working in this repository:

| If you're asked to... | Priority | Action |
|----------------------|----------|--------|
| Modify KSA content | HIGH | Proceed — this is core |
| Run validation scripts | HIGH | Proceed — maintain quality |
| Update documentation | HIGH | Proceed — support methodology |
| Build AI companion features | LOW | Check STRATEGIC_DIRECTION.md first |
| Develop flows/ content | DEFERRED | This is Phase 3 — preserve only |
| Build intake/assessment tools | MEDIUM | This is Phase 2 — plan carefully |

> **When in doubt, reference this document.**
