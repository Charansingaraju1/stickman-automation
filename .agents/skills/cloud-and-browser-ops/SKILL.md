---
name: cloud-and-browser-ops
description: Governs headless GitHub Actions scheduling, low-cost cloud evaluation including Azure free grants vs limits, and Antigravity browser inspection (absorbs browser-automation, cloud-deployment). Use when designing zero-laptop cloud workflows or inspecting web UIs safely.
---

# Cloud and Browser Operations

## Purpose
Run rendering, analytics collection, and gated publishing safely with the laptop switched off at minimal/zero monthly cost, and delegate live browser UI tasks safely to Antigravity's built-in `browser` subagent.

## Activation Conditions
- Editing `.github/workflows/*.yml`, evaluating Azure Functions/Blob/GitHub Actions costs, or checking YouTube Studio / Flow UI in browser.

## Required Inputs
- `.github/workflows/*.yml`, `memory/COST_TRACKER.md`, target URL.

## Step-by-Step Workflow
1. Prefer scheduled jobs (`GitHub Actions` public-repo free tier, or `Azure Functions Consumption` 1M exec / 400k GB-s free grant) over idle VMs.
2. Calculate real compute/storage/API estimates before recommending cloud changes; confirm commercial terms (note educational Azure credits typically disallow commercial monetization).
3. Enforce `vars.AUTO_PUBLISH_ENABLED == 'true'` or manual dispatch before live uploads in CI.
4. For browser UI inspections (YouTube Studio CSV exports, Flow web preview), delegate to built-in `browser` subagent and honor all login/CAPTCHA boundaries.

## Output Format
Cost/architecture summary in `memory/COST_TRACKER.md` & `memory/ARCHITECTURE.md`.

## Validation Criteria
- CI workflows pass dry-run / YAML syntax checks; zero plaintext secrets in workflow files.

## Failure Handling
- Keep automated retries bounded; alert Telegram via secret-backed `TELEGRAM_BOT_TOKEN` on failure.

## Security Restrictions
- Never commit secrets; never bypass Cloudflare/CAPTCHA/bot checks or automate unofficial login APIs.

## Examples
- Evaluated `Azure Functions Consumption` ($0 free grant for lightweight Python analytics/scheduling) vs `Azure Blob Storage` (~$0.02/GB/mo paid) + `GitHub Actions` public runner ($0 for Remotion rendering).
