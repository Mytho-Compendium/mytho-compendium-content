# Workflow Tooling — Implementation Approach

This document explains the technical choices behind the `/mc-workflow` developer tooling scripts in `tools/workflow/`.

---

## The Two Options

When calling an external API from Python, there are generally two options:

**Option A — Use an SDK**
A third-party library that wraps the API. Less code, more abstraction.

**Option B — Use `requests` directly**
Raw HTTP calls to the API. More verbose, but the endpoint, the headers, and the payload are all visible.

---

## Notion API → `requests`

I call the Notion API using the `requests` library directly, without the `notion-client` SDK.

**Why:**
- Every script is self-explanatory — the endpoint, the headers, and the payload are all visible
- No extra dependency to install or learn
- Scripts serve as concrete examples of how the Notion REST API works
- Anyone can read the code and understand what API call is being made, without knowing any SDK

**What it looks like:**

```python
import requests

response = requests.get(
    "https://api.notion.com/v1/pages/316d468a-7a7e-8183-bfdd-d6a03e116e34",
    headers={
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }
)
page = response.json()
```

---

## GitHub → `subprocess` with `git`

I interact with GitHub using `subprocess` to call `git` commands directly, without the `PyGithub` SDK or raw GitHub API calls.

**Why:**
- `git` is already installed and configured on my development machine
- The commands mirror exactly what I would type in my terminal
- No token management, no SDK, no extra dependency
- Scripts read like a terminal session — immediately familiar to any developer

**What it looks like:**

```python
import subprocess

subprocess.run(["git", "checkout", "-b", "feat/GCR-11-init-..."], check=True)
```

---

## Dependencies

This approach keeps `requirements.txt` minimal:

```
requests        # HTTP calls to the Notion API
python-dotenv   # Load credentials from .env
```

---

## Credentials

API tokens are never hardcoded. They are loaded from a `.env` file at the root of the repository:

```
NOTION_TOKEN=secret_xxx
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
```

The `.env` file is listed in `.gitignore` and is never committed.
