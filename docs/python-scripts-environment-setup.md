# Python Scripts Environment Setup

This document explains how to configure the `.env` file required to run the Python developer workflow scripts in `tools/workflow/`.

---

## Why a `.env` file?

The workflow scripts call external APIs (Notion) using secret credentials/tokens that identify you and grant access to your workspace. These credentials must never be hardcoded in source code or committed to the repository.

The solution is a `.env` file: a local file, ignored by git, that holds your real credentials. The scripts load it at runtime using `python-dotenv`.

---

## `.env` vs `.env.example`

| File | Purpose | Committed?                 |
|:---|:---|:---------------------------|
| `.env` | Your real credentials. Never shared. | No, listed in `.gitignore` |
| `.env.example` | Placeholder template showing required variables. | Yes, safe to commit        |

`.env.example` exists so that anyone cloning the repository knows exactly what variables to set, without ever seeing a real secret.

---

## Setup

```bash
cp .env.example .env
```

Then open `.env` and fill in your values (see below).

---

## Required Variables

### `NOTION_TOKEN`

Your Notion integration token. Used to authenticate API requests to your Notion workspace.

**How to get it:**

1. Go to [https://www.notion.so/profile/integrations/internal](https://www.notion.so/profile/integrations/internal)
2. Click **New integration**
3. Give it a name (e.g. `mytho-compendium-content`) and select your workspace
4. Copy the **Internal Integration Token**, it starts with `ntn_` or `secret_`

> The token grants access to your workspace. Treat it like a password.

**Then connect your integration to your database:**

1. Open your Notion database page
2. Click the `...` menu (top right) → **Connections** → **Add a connection**
3. Select the integration you just created

Without this step, API calls will return a 404 even with a valid token.

---

### `NOTION_DATABASE_ID`

The ID of the Notion database the scripts interact with (your ticket backlog).

**How to find it:**

Open the database page in your browser. The URL looks like:

```
https://www.notion.so/7f3a9c2d1e4b8056f7a3c91d2e5b8047?v=b5e1d8f2a0c34791e6b2d059f3a8c147
```

The database ID is the 32-character hex string **before** the `?v=`:

```
7f3a9c2d1e4b8056f7a3c91d2e5b8047
```

Notion sometimes omits hyphens in URLs. The API accepts both formats, so use the ID as-is.

---

## Final `.env`

```env
NOTION_TOKEN=ntn_your_token_here
NOTION_DATABASE_ID=your_database_id_here
```

---

## Security

- `.env` is listed in `.gitignore`, it will never be staged or committed
- `.env.example` contains only placeholders, it is safe to commit and is already tracked
- Never paste your real token in a chat, a PR description, or a commit message
- If a token is accidentally exposed, regenerate it immediately from [Notion integrations](https://www.notion.so/profile/integrations)

---

## Related

- [workflow-tooling.md](./workflow-tooling.md) : How the scripts use these credentials
- [claude-code-setup.md](./claude-code-setup.md) : Full environment setup for Claude Code
