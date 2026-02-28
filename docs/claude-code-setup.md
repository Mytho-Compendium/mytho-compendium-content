# Claude Code Setup Guide

This document describes how Claude Code is configured for the `mytho-compendium-content` repository and how to reproduce the setup from scratch.

---

## Prerequisites

- Anthropic account with Claude Pro or API access
- Node.js installed (required for Claude Code CLI)
- Notion workspace access (for MCP integration)
- `mytho-compendium-content` repository cloned locally

---

## 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify the installation:

```bash
claude --version
```

---

## 2. Authenticate

```bash
claude login
```

Follow the browser prompt to authenticate with your Anthropic account.

---

## 3. Notion MCP Server

Claude Code integrates with the Notion workspace via the official Notion MCP server. This enables reading tickets, updating task status, fetching documentation, and managing the backlog directly from the terminal.

### Add the Notion MCP server

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

This registers the server in the project config (`.claude.json`).

### Verify the connection

Start a new Claude Code session. The Notion server connection status is shown at session startup. On first use, a browser prompt will ask you to authorize the Notion OAuth connection.

> **Note:** Running `claude mcp list` from within an active session may return no output. This is expected — use a fresh session to see connection status.

---

## 4. CLAUDE.md

The `CLAUDE.md` file at the repository root provides Claude Code with persistent project context: content standards, repository structure, tech stack, commands, and the skills architecture. It is committed to the repository and loaded automatically on every Claude Code session.

No manual setup required, it is already present in the repository.

---

## 5. Skills

This repository **is the source of truth for skills**. The `skills/` directory contains all Claude Code skill definitions used across the Mytho Compendium ecosystem.

Skills from this repo are consumed by `mytho-compendium-app` and `mytho-compendium-server` via a Git submodule:

```bash
# In mytho-compendium-app or mytho-compendium-server:
git submodule add <mytho-compendium-content-url> .claude/skills
```

When working on skills in this repo, Claude Code picks them up directly from `skills/` — no submodule setup needed here.

---

## 6. Environment Setup

A `.env` file is required to run ingestion scripts against real databases:

```bash
cp .env.example .env
# Fill in your Neo4j and PostgreSQL credentials
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

The `.env` file is listed in `.gitignore` and must never be committed.

---

## 7. Common Workflows

### Start work on a ticket

```
Read ticket GCR-XX from Notion, then help me implement it.
```

### Research and validate a mythology entry

```
Use the research-validation skill to research [entity] from [mythology].
```

### Check ticket status

```
Fetch GCR-XX from Notion and show me the current status and acceptance criteria.
```

### Update a ticket

```
Mark the following acceptance criteria as done in GCR-XX: [list items]
```

---

## 8. Troubleshooting

**`claude: command not found`**
Ensure npm global binaries are on your PATH. Add `$(npm bin -g)` to your shell profile.

**Notion MCP shows as disconnected**
Re-run `claude mcp add --transport http notion https://mcp.notion.com/mcp` and re-authorize via the browser prompt.

**Ingestion scripts fail to connect**
Check that your `.env` file exists and contains valid Neo4j/PostgreSQL credentials.

---

## Related

- [CLAUDE.md](../CLAUDE.md) — Project context for Claude Code
- [Notion: Working with Claude](https://www.notion.so/308d468a7a7e81369d71fbd29cffc6d5)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
