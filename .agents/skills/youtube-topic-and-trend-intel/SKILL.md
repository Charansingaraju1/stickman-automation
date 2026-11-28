---
name: youtube-topic-and-trend-intel
description: Generates and scores 30 original US-targeted stickman science/curiosity ideas per cycle (absorbs viral-topic-discovery, competitor-intelligence, youtube-trend-research, content-gap-analysis, us-audience-research). Use when brainstorming new Shorts or running weekly research cycles.
---

# YouTube Topic and Trend Intelligence

## Purpose
Research public educational Shorts patterns, US audience curiosity triggers, and content gaps, then generate and score 30 original video concepts per cycle using the 100-pt editorial rubric.

## Activation Conditions
- Topic brainstorming, queue restocking, or monthly US science/what-if content calendar planning.

## Required Inputs
- `memory/VIDEO_HISTORY.json`, `memory/CONTENT_STRATEGY.md`, optional public trend search results.

## Step-by-Step Workflow
1. Research trending questions and public outlier themes in US short-form science/what-if/anatomy using `search_web` and authorized public tools (never fabricate metrics or copy competitor scripts).
2. Generate 30 original candidates across core pillars (physics, what-if, body mysteries, space, survival, everyday objects, psychology, history) that translate cleanly to B&W + selective-color stickman visuals.
3. Deduplicate against `memory/VIDEO_HISTORY.json` and `cloud_queue.json`.
4. Score every candidate out of 100 using `agents/studio_engine.py`:
   - Opening hook (20), Curiosity (20), Visual potential (15), Retention potential (15), Surprise factor (10), Originality (10), US relevance (5), Sharing potential (5).
5. Pass top concepts (`>=80` editorial heuristic) to `deep-research-and-fact-check` and `studio-critic-gate`.

## Output Format
JSON list of 30 scored candidates sorted descending, labeled strictly as **internal editorial estimates** (never view guarantees).

## Validation Criteria
- Exact weight sums = 100; zero copied competitor scripts; no claim that a concept has "never appeared on the internet" unless genuinely verified.

## Failure Handling
- If external trend APIs (`vidiq`/search) rate-limit, fall back to offline curated science backlog flagged `source=offline_curated`.

## Security Restrictions
- Read-only public trend research; no unauthorized scraping tools or credential leaks.

## Examples
- Scoring `400F Grease Fire + 1 Cup Water`: strong immediate visual (`15/15`), high US kitchen curiosity (`19/20`), high surprise (`9/10`).
