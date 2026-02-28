# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Content pipeline for **Mytho Compendium**, Claude Code skills for mythology research and validation, database schemas, and automated data ingestion scripts. This repository is the **data factory** of the Mytho Compendium ecosystem: it produces structured, validated mythology content ready for consumption by the Ktor backend.

## Repository Purpose

This repo is fully independent from the Android app and the Ktor server. It only produces data, it does not serve it. Its three core concerns are:

1. **Skills** - Claude Code skill definitions for repeatable content tasks (research, validation, image prompt generation)
2. **Schemas** - Neo4j graph schema and PostgreSQL relational schema
3. **Ingestion** - Python scripts that populate the databases from validated content

## Repository Structure

```text
skills/                          # Claude Code skill definitions (source of truth for all repos)
│   ├── skill-research-validation/
│   └── skill-image-prompt-gen/
neo4j/                           # Neo4j graph database schema and seed data
postgresql/                      # PostgreSQL relational schema and migrations
ingestion/                       # Python scripts that populate the databases
docs/                            # Design decisions and content standards
```

## Content Standards

All content must conform to strict sourcing and validation rules (see `/docs/content-standards.md`).

**Truth levels:**

| Level | Meaning |
|:---|:---|
| `canonical` | Directly stated in a primary source (original text, inscription, etc.) |
| `widely_accepted` | Consistent across multiple reputable secondary sources |
| `debated` | Conflicting accounts exist between reputable sources |
| `speculative` | Reasonable inference, not directly supported by sources |

**Source tiers:**

| Tier | Examples |
|:---|:---|
| Tier 1 - Primary | Original texts (Iliad, Prose Edda, Book of the Dead), inscriptions |
| Tier 2 - Academic | Peer-reviewed scholarship, university press publications |
| Tier 3 - Reference | Reputable encyclopedias (Larousse, Oxford Companion to World Mythology) |
| Tier 4 - Secondary | Well-researched books, documentaries - used only to corroborate, never as sole source |

## Skills

This repository is the **source of truth for all Claude Code skills** in the Mytho Compendium ecosystem. Skills are consumed by `mytho-compendium-app` and `mytho-compendium-server` via a Git submodule pointing to their respective `.claude/skills/` directories.

Each skill lives in `skills/<skill-name>/` and includes:
- `SKILL.md` - skill instructions, scope, and constraints
- `prompts/` - prompt templates used by the skill
- `examples/` - example outputs for validation

## Tech Stack

| Concern | Technology |
|:---|:---|
| Scripting | Python |
| Graph DB | Neo4j (Cypher) |
| Relational DB | PostgreSQL |
| Migrations | Custom SQL migration runner |
| Dependency management | pip / `requirements.txt` |

## Commands

```bash
pip install -r requirements.txt            # Install dependencies
python ingestion/utils/run_migrations.py   # Apply PostgreSQL migrations
cypher-shell < neo4j/constraints.cypher    # Apply Neo4j constraints
cypher-shell < neo4j/indexes.cypher        # Apply Neo4j indexes
pytest                                     # Run all tests
```

> A `.env` file with Neo4j and PostgreSQL credentials is required to run ingestion scripts. Copy `.env.example` and fill in your values. It is never committed to the repository.

## Related Repositories

- **mytho-compendium-app** - Android app, future KMP; consumes skills via submodule
- **mytho-compendium-server** - Ktor backend that reads from the databases this repo populates; consumes skills via submodule
