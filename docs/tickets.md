# Ticket Structure

## Ticket Creation

When creating a ticket in Notion:
- Always use the Notion API to create the ticket directly, never output plain text.
- Apply the Notion Block Structure defined in this file from the first attempt, without waiting for a correction.
- If a previous ticket (e.g. GCR-11, GCR-12) was successfully created with correct formatting, use it as a reference.

## Anatomy

Each ticket should follow this structure as much as possible:

- **Description / Context**
- **Steps**
  - 1. Environment & tools setup (if applicable) → **1 commit** *(no test step — nothing testable is produced)*
  - 2. Test `<what step 3 will implement>` → **1 commit** *(RED — tests fail, implementation does not exist yet)*
  - 3. Implement `<what step 2 tests>` → **1 commit** *(GREEN — implementation makes step 2 tests pass)*
  - 4. Test `<what step 5 will implement>` → **1 commit** *(RED)*
  - 5. Implement `<what step 4 tests>` → **1 commit** *(GREEN)*
  - … (alternate test / implementation pairs as needed)
  - N. Document → **1 commit**

Reference example: GCR-11 → https://www.notion.so/316d468a7a7e8114b854d024fffab9a7

## Commit Strategy

Each step in a ticket maps to **one commit**. The rules:

- Every **test step** immediately precedes its implementation step. Tests are written first, before the implementation exists. This is the TDD Red-Green cycle: the test commit is RED (failing), the implementation commit is GREEN (passing).
- **Setup steps** (environment, tooling) have no paired test step — they produce no testable unit.
- The **final step is always Document**, one commit for all documentation written for the ticket.
- There is no case where an implementation step comes before its test step.

This produces a clean, readable git history that honestly reflects TDD order: every test was written before the code it covers.

### Commit message conventions

- **feat** / **chore** / **fix** → implementation steps
- **test** → test steps
- **docs** → document step
- Format: **type(scope): short description**

## Notion Block Structure

Tickets are written using the following Notion block types:

- **heading_2** (**##**) for top-level sections: **Description** and **Steps**
- **divider** (**---**) between the Description section and the Steps section
- **heading_3** (**###**) for each numbered step title (e.g. **### 1. Environment & tools setup**, **### 2. Test workflow_start.py**, **### 3. Implement workflow_start.py**)
- **to_do** (**- [ ]**) for every task item, all tasks are checkboxes, never bullet points
- **bold** for key terms: file paths, commands, CLI tools, module names - never backtick syntax

### Step title naming

- Test steps: describe what will be tested (e.g. **### 2. Test workflow_start.py**) — not the step number, not "Test step 3"
- Implementation steps: describe what is being built (e.g. **### 3. Implement workflow_start.py**) — mirrors the test step title above it
- Setup steps: describe what is being set up (e.g. **### 1. Environment & tools setup**)
- Document step: always just **### N. Document**

## Complexity Assessment

Always assess complexity before creating a ticket:

- **Simple** (clear scope, no architecture decisions) → ticket with Description + Steps is enough
- **Complex** (multiple approaches, full feature/module, UI component, architectural decision) → ticket stays lean, but include a step to write a dedicated spec page (Technical Spec, ADR, or Component Spec) and link it from the ticket
