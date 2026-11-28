---
name: stickman-master-orchestrator
description: End-to-end controller for Autonomous AI Stickman YouTube Studio (absorbs master-orchestrator, content-production-pipeline, continuous-improvement-engine). Use when running a full production cycle from research through QA, dry-run, analytics learning, and post-mortem iteration.
---

# Stickman Master Orchestrator

## Purpose
Coordinate the 18 specialist roles across the closed-loop workflow (`Research -> Generate 30 Ideas -> Score -> Fact Check -> Script -> Storyboard -> Animate -> Edit -> Quality Check -> Publish [gated] -> Analyze 24h/48h/7d -> Learn -> Improve`) while preserving existing working pipelines.

## Activation Conditions
- Multi-stage video creation, weekly planning, pipeline upgrades, or full self-improvement cycles in `stickman-daily`.
- Do NOT activate for isolated single-file formatting or unrelated repos (`cooking-clip-us`).

## Required Inputs
- `memory/PROJECT.md`, `memory/ARCHITECTURE.md`, `memory/PROGRESS.md`, `memory/TASKS.md`, `memory/LESSONS_LEARNED.md`
- Topic cycle scope or failure log

## Step-by-Step Workflow
1. Read `memory/PROGRESS.md` and `memory/BUGS.md`; confirm current baseline passes (`python agents/run_agents.py --self-test` and unit tests).
2. Route discovery to `youtube-topic-and-trend-intel` (30 ideas) and score using the 100-pt rubric.
3. Require `deep-research-and-fact-check` clearance before scripting.
4. Generate 15-30s script via `hook-script-and-retention`, then invoke `studio-critic-gate` for pre-production veto.
5. Produce scene storyboard + deterministic Remotion/FFmpeg render via `stickman-bible-and-continuity`, `scientific-viz-and-physics-motion`, `voiceover-sfx-and-captions`, and `ffmpeg-render-and-qa`.
6. Execute `ypp-originality-and-compliance` and `ffmpeg-render-and-qa`; hold in `cloud_queue.json` unless publishing is explicitly authorized.
7. Schedule 24h/48h/7d `youtube-growth-and-experiments` review and append findings to `memory/ANALYTICS_HISTORY.json` and `memory/LESSONS_LEARNED.md`.

## Output Format
Checklist state + artifact paths + verified test exit codes in `memory/PROGRESS.md`.

## Validation Criteria
- Every stage leaves verifiable artifacts (storyboard JSON, probed MP4 `1080x1920`, QC report, test logs).
- Zero unverified "done" claims (`verification-before-completion`).

## Failure Handling
- Halt on `BillingHaltError`, failed `audit_security()`, or QC failure; log root cause to `memory/BUGS.md` and invoke `systematic-debugging`.
- Never force-push or bypass quality gates when a stage fails.

## Security Restrictions
- Strict `$0.00` compute/model lock unless paid billing is approved by user.
- Never publish or expose credentials (`token.json`, `client_secret.json`, `.env`).

## Examples
- Input: `"Run one end-to-end production dry-run for a space physics Short."` -> Produces scored brief, verified facts, storyboard JSON, B&W Remotion render, QC report, dry-run queue check.
