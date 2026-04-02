# CaliberPath

**CaliberPath** is a Learning & Development company that transforms individuals and organizations through competency-based coaching, training, and consulting. Our methodology is powered by the **UPLS Framework** — a comprehensive competency architecture spanning Professionalism, Leadership & Influence, and Self-Mastery.

---

## Our Approach

We believe development should be:
- **Competency-grounded** — Every program maps to specific, measurable capabilities
- **Experiential** — Learning happens through application, not just instruction
- **Human-centered** — Technology augments but never replaces the coaching relationship
- **Outcomes-focused** — Success is defined by behavioral change and real-world results

> *"Reflection without integration is memory. Reflection with intention becomes wisdom."*

---

## The UPLS Framework

Our signature methodology organizes human capability into three domains:

### Professionalism Competencies (15)
Foundational skills every professional needs:
- Accountability, Adaptability, Attention to Detail, Collaboration, Creative Thinking
- Critical Thinking, Digital Literacy, Effective Communication, Emotional Intelligence
- Initiative, Learning Agility, Professionalism, Resilience, Self-Motivation, Time Management

### Leadership & Influence Competencies (15)
Skills for leading people and driving outcomes:
- Change Leadership, Conflict Resolution, Crisis Leadership, Delegation & Empowerment
- Ethical Governance, Inclusive Leadership, Mentoring & Coaching, Persuasion & Negotiation
- Remote & Hybrid Team Leadership, Stakeholder Coalition Building, Strategic Communication
- Strategic Thinking, Team Building, Vision Setting, Change Analytics & Sentiment Monitoring

### Self-Mastery Competencies (15+)
Internal capabilities for personal excellence:
- **Habits & Productivity:** Deep Work Practice, Digital Minimalism, Energy Management
- **Self-Awareness:** Identity Self-Authorship, Metacognition, Self-Reflective Insight
- **Self-Regulation:** Attention Switching & Focus, Impulse Control
- **Values & Ethics:** Ethical Reflection & Reasoning, Integrity Alignment, Moral Courage
- **Well-Being & Resilience:** Growth Mindset, Sensory Mindfulness, Stress Management
- **Intrinsic Motivation:** Purpose Articulation

Beyond UPLS, our repository contains **400+ sector-specific technical competencies** across 35 industries.

---

## Services

### For Individuals (B2C)

| Program | Description |
|---------|-------------|
| **Career Compass Coaching** | 1:1 coaching for career clarity, confidence, and growth |
| **Self-Mastery Workshop Series** | Group workshops on habits, resilience, and personal effectiveness |
| **Career Accelerator Bootcamp** | Intensive cohort program for professional development |

### For Organizations (B2B)

| Program | Description |
|---------|-------------|
| **Rising Leaders Academy** | Leadership development cohort for emerging leaders |
| **Competency Consulting** | Custom competency model development and integration |
| **Custom Training Design** | Curriculum design using ADDIE methodology |
| **Executive Coaching** | 1:1 coaching for senior leaders |

---

## Repository Structure

This repository contains CaliberPath's competency database and supporting tools:

```
CaliberPath/
├── content/
│   └── Individual_KSAs/           # Competency definitions
│       ├── professionalism/       # Professionalism (15)
│       ├── leadership_influence/  # Leadership (15)
│       ├── self_management_personal_mastery/  # Self-Mastery (15+)
│       └── technical_ksas/        # Sector-specific (400+)
├── schemas/
│   └── ksa.schema.json            # Validation schema
├── scripts/
│   ├── build_ksa_json.js          # Compile to master JSON
│   └── validate_ksas.js           # Schema validation
├── data/
│   └── master_ksa.json            # Compiled output
├── docs/
│   ├── STRATEGIC_DIRECTION.md     # Development priorities
│   └── [methodology docs]
└── [application code]
```

### Competency File Format

Each competency is a Markdown file with YAML front matter:

```yaml
---
ksa_id: adaptability
label: Adaptability
category: General
sector: cross_sector
horizon: perennial
cluster_tags:
  - "Change Management"
  - "Resilience"
description: >
  Adjusts effectively to new information, shifting priorities, 
  and evolving circumstances while remaining productive.
source_frameworks:
  - "Adapted from O*NET Work Style (USDOL/ETA, CC BY 4.0)"
proficiency_levels:
  - level: Awareness
    indicator: Accepts changes in tasks or schedules when directed.
  - level: Basic
    indicator: Modifies personal work methods when priorities shift.
  - level: Intermediate
    indicator: Reprioritizes workload independently when conditions change.
  - level: Advanced
    indicator: Anticipates change drivers; helps team adjust proactively.
  - level: Expert
    indicator: Champions adaptive culture; designs resilient processes.
---
```

---

## Development

### Prerequisites
- Node.js 18+
- npm

### Installation
```bash
git clone https://github.com/YordsBoy/CaliberPath.git
cd CaliberPath
npm install
```

### Key Commands

| Command | Purpose |
|---------|---------|
| `npm run build:ksas` | Generate `data/master_ksa.json` from KSA files |
| `npm run validate:ksas` | Validate all KSAs against schema |
| `npm run lint` | Run ESLint |
| `npm run format` | Run Prettier |

### Adding or Editing Competencies

1. Create/edit `.md` file in appropriate `content/Individual_KSAs/` subdirectory
2. Follow YAML schema (see `schemas/ksa.schema.json`)
3. Run `npm run validate:ksas` to check compliance
4. Run `npm run build:ksas` to regenerate master JSON

### Schema Requirements

**Required fields:** `ksa_id`, `label`, `category`, `description`, `sector`, `horizon`, `proficiency_levels`

**Horizon values:** `core`, `emerging`, `perennial`, `watch_2030`, `peripheral`

**Proficiency levels:** Each must have `level` (Awareness/Basic/Intermediate/Advanced/Expert) and `indicator`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 13 (App Router) |
| UI | React 18, Tailwind CSS v4, shadcn/ui |
| Validation | AJV (JSON Schema), gray-matter (YAML) |
| Build | Node.js scripts |

---

## Philosophy

CaliberPath exists to make professional development accessible, rigorous, and transformative. We believe:

- **Everyone deserves access to quality development** — not just those in large corporations
- **Competencies create clarity** — knowing what "good" looks like enables growth
- **Human connection matters** — technology should enhance, not replace, the coaching relationship
- **Growth is a practice** — sustainable change comes from consistent, intentional effort

---

## Project Status

CaliberPath is in **Phase 1: Human-Delivered Services**. 

We are establishing our coaching and training practice while maintaining and expanding the competency database. Technology-augmented delivery (Phase 2) and AI-native features (Phase 3) are planned for future development.

See `docs/STRATEGIC_DIRECTION.md` for full architectural context.

---

## Contributing

This repository is in active development. Key guidelines:

- Follow existing file structures and naming conventions
- Run validation before committing KSA changes
- Reference `docs/STRATEGIC_DIRECTION.md` for development priorities
- See `docs/caliberpath-dev_contributor-guide.md` for detailed guidance

---

## License

This project is currently **UNLICENSED**. The competency content and methodology are proprietary to CaliberPath. Forks for personal learning are welcome; commercial use requires written consent.

---

## Contact

- **GitHub Issues** — For repository questions
- **GitHub Discussions** — For methodology discussion

---

*CaliberPath: Competency-powered development for individuals and organizations.*