---
name: reliability-and-performance
description: Handles pipeline failures, Remotion/FFmpeg optimization, automated monitoring, and strict $0 cost tracking (absorbs failure-recovery, performance-optimization, cost-optimization, automated-monitoring). Use when builds stall, render times spike, GitHub Actions fail, or evaluating compute/API budgets.
---

# Reliability and Performance

## Purpose
Keep rendering fast, monitor workflow health via Telegram, enforce `$0.00` operational spend, and maintain verified recovery paths.

## Activation Conditions
- Render failures, EdgeTTS `NoAudioReceived` retries, GitHub Actions errors, slow Chromium frame renders, or cost audits.

## Required Inputs
- Failing log/stacktrace, `memory/COST_TRACKER.md`, `memory/LESSONS_LEARNED.md`.

## Step-by-Step Workflow
1. Inspect actual stderr / workflow logs; diagnose root cause (`systematic-debugging`) before retrying.
2. Profile bottlenecks (Remotion concurrency, SVG complexity vs heavy raster blurs, EdgeTTS fallback voices).
3. Verify zero paid endpoints are touched (`assert_zero_cost()`); log compute/API units in `memory/COST_TRACKER.md`.
4. Send crisp failure/recovery alerts using `upload_to_youtube.send_telegram_alert` when `TELEGRAM_BOT_TOKEN` is configured.

## Output Format
Incident entry in `memory/BUGS.md` + updated `memory/COST_TRACKER.md` monthly row.

## Validation Criteria
- Reproduction test added before fix; `$0.00` verified spend unless explicitly pre-approved.

## Failure Handling
- On EdgeTTS errors: auto-cycle `DEFAULT_VOICES`. On HTTP 402/429 quota/billing signals: trigger `BillingHaltError` immediately.

## Security Restrictions
- Never expose workflow tokens when reporting CI tracebacks to Telegram or markdown logs.

## Examples
- Resolved `cloud_auto_stock` crash (`8056fba`) by lazy-importing Google OAuth clients inside consuming functions.
