---
name: architecture-and-security-audit
description: Enforces modular design review, secret hygiene, and pre-commit security scanning across workflows and renderers (absorbs architecture-review, security-auditor, plus mattpocock improve-codebase-architecture). Use before modifying pipeline modules, GitHub Actions, OAuth scopes, or external API code.
---

# Architecture and Security Audit

## Purpose
Keep `stickman-daily` modular, dry, leak-free, and strictly bounded by least-privilege credentials and `$0` guardrails.

## Activation Conditions
- Any PR, workflow change, API client edit, or pre-release audit.

## Required Inputs
- Diff or target files + `.gitignore` + `.github/workflows/*.yml`.

## Step-by-Step Workflow
1. Check `agents/run_agents.py` `audit_security()` against `.gitignore` and all tracked files (`.py`, `.ts`, `.tsx`, `.yml`, `.json`, `memory/`).
2. Confirm zero plaintext secrets (`BOT_TOKEN`, `AIza...`, `GOCSPX-...`, `EAAQ...`, `github_pat_...`, `refresh_token`) exist outside gitignored `.env`, `token.json`, `client_secret.json`.
3. Inspect architectural boundaries: keep Python orchestration (`agents/`), renderers (`renderers/`), Remotion UI (`src/`), and publishers (`upload_to_*.py`) decoupled.
4. Run `studio_engine` / `run_agents.py --self-test` and `tsc --noEmit` after edits.

## Output Format
JSON/markdown audit report listing `ok`, `leaks`, `scope_risks`, and `architectural_findings`.

## Validation Criteria
- `audit_security()['ok'] == True` and zero tracked credential files (`git ls-files` clean).

## Failure Handling
- Block commit/push immediately if any token matches; rotate exposed credentials at provider and migrate to environment secrets.

## Security Restrictions
- Never echo `.env`, `token.json`, or `client_secret.json` contents to logs, markdown memory files, or stdout.

## Examples
- Caught plaintext `BOT_TOKEN` in `upload_to_youtube.py` and `token_json` stdout dump in `refresh_auth_token()`; migrated to `.env` + GitHub Secret.
