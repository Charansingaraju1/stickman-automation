---
name: youtube-growth-and-experiments
description: Executes 24h/48h/7d YouTube Analytics checks, controlled single-variable A/B tests, US peak scheduling, and evidence-backed growth optimization (absorbs youtube-analytics-intelligence, content-experimentation, intelligent-post-scheduler, analytics-feedback-loop, plus ab-testing discipline). Use after videos publish or when reviewing channel performance.
---

# YouTube Growth and Experiments

## Purpose
Connect real authorized YouTube Analytics data (`24h`, `48h`, `7d`) to controlled creative experiments and US posting schedules without fabricating unavailable metrics.

## Activation Conditions
- Post-publish review intervals (24h, 48h, 7d), designing A/B tests, or tuning upload timing.

## Required Inputs
- `token.json` (`youtube.readonly` + `yt-analytics.readonly`), `memory/VIDEO_HISTORY.json`, `memory/ANALYTICS_HISTORY.json`, `memory/EXPERIMENTS.md`.

## Step-by-Step Workflow
1. Run `python agents/studio_engine.py --analytics` to pull official API metrics (`views`, `engagedViews`, `averageViewDuration`, `averageViewPercentage`, `subscribersGained`, `likes`, `comments`, `shares`, `country`, `insightTrafficSourceType`, `audienceRetention`).
2. Record missing/unavailable fields honestly (`null` + note — note Studio *"Viewed vs. Swiped Away"* is not directly in Analytics API v2; ingest Studio CSV manually if exported).
3. Design single-variable experiments (`hook_style`, `duration_band`, `visual_style`, `title_format`, `post_hour_est`) with fixed evaluation window & minimum sample size (`>=5` Shorts/arm before calling winners — no premature peeking).
4. Adjust publishing windows in `.github/workflows/daily_shorts.yml` strictly from measured US EST/PST performance.

## Output Format
Verified snapshot JSON in `memory/ANALYTICS_HISTORY.json` + hypothesis/verdict entry in `memory/EXPERIMENTS.md`.

## Validation Criteria
- Zero fabricated numbers; missing OAuth scope explicitly flagged cleanly.

## Failure Handling
- If `token.json` lacks `yt-analytics.readonly`, halt metric pull with actionable re-auth instruction (`python upload_to_youtube.py --auth`) instead of guessing.

## Security Restrictions
- Read-only analytics scope only; zero fake engagement, bots, view buying, or sub4sub.

## Examples
- Hypothesis: *"Pure B&W Stickman vector rig on white `#FAFAFA` beats dark 3D JPG scenes on 3-second retention (`averageViewPercentage`)."* Test over 10 paired Shorts before deciding.
