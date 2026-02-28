# mytho-compendium-content

> Content pipeline for **Mytho Compendium**, Claude Code skills for mythology research and validation, database schemas, and automated data ingestion scripts.

---

## Project Overview

This repository is the **data factory** of Mytho Compendium. It contains everything needed to go from raw research to populated, production-ready databases. It is fully independent from the Android app and the Ktor server, it only produces data, it does not serve it.

The pipeline is built around **Claude Code skills**, focused AI agents designed to perform specific, repeatable tasks with strict content and sourcing standards.

> ⚠️ This repository is in early stages. Structure and tooling will evolve as the pipeline is built out.

---

## Repository Structure

```text
mytho-compendium-content/
│
├── skills/                          # Claude Code skill definitions
│   ├── skill-research-validation/   # Research + source validation
│   │   ├── SKILL.md                 # Skill instructions, scope, constraints
│   │   ├── prompts/                 # Prompt templates used by the skill
│   │   └── examples/               # Example outputs for validation
│   │
│   └── skill-image-prompt-gen/      # Image prompt generation
│       ├── SKILL.md
│       ├── prompts/
│       └── examples/
│
├── neo4j/                           # Neo4j graph database schema
│   ├── schema.md                    # Node labels, relationship types, properties
│   ├── constraints.cypher           # Uniqueness and existence constraints
│   ├── indexes.cypher               # Performance indexes
│   └── seed/                        # Sample Cypher scripts for testing
│
├── postgresql/                      # PostgreSQL relational schema
│   ├── schema.md                    # Tables, columns, types, relationships
│   ├── migrations/                  # Ordered SQL migration files
│   │   ├── V001__initial_schema.sql
│   │   └── ...
│   └── seed/                        # Sample data for local development
│
├── ingestion/                       # Scripts that populate the databases
│   ├── ingest_entities.py           # Reads validated content, writes to Neo4j + PostgreSQL
│   ├── validate_sources.py          # Cross-checks sources before ingestion
│   └── utils/
│
└── docs/
    ├── content-standards.md         # Truth levels, source tiers, validation rules
    ├── graph-design.md              # Rationale for the Neo4j graph model
    └── schema-design.md             # Rationale for the PostgreSQL schema
```

---

## Content Standards

Every piece of content in this pipeline is subject to strict validation rules defined in `/docs/content-standards.md`.

**Truth levels:**

| Level | Meaning |
|:---|:---|
| `canonical` | Directly stated in a primary source (original text, inscription, etc.) |
| `widely_accepted` | Consistent across multiple reputable secondary sources |
| `debated` | Conflicting accounts exist between reputable sources |
| `speculative` | Reasonable inference, not directly supported by sources |

**Source tiers:**

| Tier | Examples                                                                             |
|:---|:-------------------------------------------------------------------------------------|
| Tier 1 - Primary | Original texts (Iliad, Prose Edda, Book of the Dead), inscriptions                   |
| Tier 2 - Academic | Peer-reviewed scholarship, university press publications                             |
| Tier 3 - Reference | Reputable encyclopedias (Larousse, Oxford Companion to World Mythology)              |
| Tier 4 - Secondary | Well-researched books, documentaries, used only to corroborate, never as sole source |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/mytho-compendium-content.git

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Fill in your Neo4j and PostgreSQL credentials

# Apply PostgreSQL migrations
python ingestion/utils/run_migrations.py

# Apply Neo4j constraints and indexes
cypher-shell < neo4j/constraints.cypher
cypher-shell < neo4j/indexes.cypher
```

---

## Related Repositories

| Repository | Purpose                                                        |
|:---|:---------------------------------------------------------------|
| **mytho-compendium-app** | Android app, future KMP                                        |
| **mytho-compendium-server** | Ktor backend that reads from the databases this repo populates |
| **mytho-compendium-content** _(this repo)_ | Content pipeline, Claude Code skills, data ingestion a         |