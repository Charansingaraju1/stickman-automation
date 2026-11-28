---
name: deep-research-and-fact-check
description: Multi-source science researcher and independent fact-checker (absorbs deep-research-agent, science-fact-checker). Use before scripting any educational science, anatomy, space, survival, psychology, or history Short to verify factual accuracy and distinguish real science from hypothetical assumptions.
---

# Deep Research and Fact Check

## Purpose
Ground every Stickman Short in verified primary/reputable scientific sources before writing narration or drawing anatomy/physics mechanisms.

## Activation Conditions
- Before finalizing any script or storyboard in Phase 4-5.
- Whenever a scientific claim, physiological mechanism, timeline, or numerical statistic appears in a draft.

## Required Inputs
- Candidate topic, core question, and claims list.

## Step-by-Step Workflow
1. Search primary scientific/educational sources (`search_web` targeting peer-reviewed summaries, university/medical refs like NIH/NASA/Mayo/textbooks).
2. Break the premise into atomic claims (`[REAL FACT]` vs `[HYPOTHETICAL ASSUMPTION]`).
3. Verify concrete numbers (e.g., 15-minute knuckle refractory period, 1700x steam expansion of water in 400F oil, 2-second micro-sleeps).
4. Flag common myths falsely repeated online and clarify mechanism in plain American English (zero opaque jargon).
5. Return cited claim ledger to `hook-script-and-retention`.

## Output Format
Structured claim ledger: `claim`, `label` (`FACT` | `HYPOTHETICAL`), `evidence_url`, `plain_english_explanation`, `status` (`VERIFIED` | `REJECTED`).

## Validation Criteria
- 100% of numerical & medical claims marked `VERIFIED` with cited sources; zero invented stats or citations.

## Failure Handling
- If sources conflict or lack consensus, downgrade or reject the angle and return to `youtube-topic-and-trend-intel`.

## Security Restrictions
- Read-only web/literature lookups only; no credentialed scraping or bypassing paywalls/CAPTCHAs.

## Examples
- Example: Topic *"What happens if you swallow 1 watermelon seed?"* -> Separates `HYPOTHETICAL` kid myth ("sprouts inside stomach") from `FACT` (cellulose hull resists gastric HCl and exits intact in ~24h without sunlight/soil).
