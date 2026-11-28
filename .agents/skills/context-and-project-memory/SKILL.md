---
name: context-and-project-memory
description: Manages persistent markdown/JSON memory ledgers and prevents context rot across long sessions (absorbs context-management, persistent-project-memory, plus ag-kit memory pattern). Use at the start and end of every session or major task milestone.
---

# Context and Project Memory

## Purpose
Keep cross-session truth in versioned repository files (`memory/`) so future sessions resume accurately without repeating discoveries or relying on fragile chat history.

## Activation Conditions
- Session startup, pre-compaction, architecture decision, completed video render, or bug discovery/fix.

## Required Inputs
- Paths in `memory/`: `PROJECT.md`, `ARCHITECTURE.md`, `PROGRESS.md`, `TASKS.md`, `DECISIONS.md`, `CHARACTER_BIBLE.md`, `CONTENT_STRATEGY.md`, `VIDEO_HISTORY.json`, `ANALYTICS_HISTORY.json`, `EXPERIMENTS.md`, `LESSONS_LEARNED.md`, `BUGS.md`, `COST_TRACKER.md`.

## Step-by-Step Workflow
1. Read `memory/PROGRESS.md`, `memory/TASKS.md`, and `memory/BUGS.md` first (economic reading: targeted sections only).
2. Perform work using focused tool calls (`rg`, partial line ranges).
3. Update `memory/PROGRESS.md` and `memory/VIDEO_HISTORY.json` / `DECISIONS.md` **only after** verifying tool output.
4. Keep prose dense; archive completed sprints instead of growing files endlessly.

## Output Format
Appended chronological markdown entry (UTC date, factual change, evidence command output) or JSON record.

## Validation Criteria
- Every claim in `PROGRESS.md` references an observed file or command output; zero credentials stored inside `memory/`.

## Failure Handling
- If memory conflicts with git/disk state, treat actual repository code and API responses as ground truth and repair the stale ledger with a dated correction note.

## Security Restrictions
- Never write API keys, OAuth tokens, passwords, or PII into `memory/`.

## Examples
- Example: Recording OAuth scope upgrade requirement in `memory/BUGS.md` & `memory/TASKS.md` after reading `token.json` scopes.
