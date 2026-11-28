---
name: ypp-originality-and-compliance
description: Audits scripts, renders, metadata, and channel milestones against YouTube Partner Program policies, copyright rules, and synthetic-media disclosure rules (absorbs monetization-readiness, originality-and-copyright-checker). Use before queuing, compiling, or requesting monetization review.
---

# YPP Originality and Compliance

## Purpose
Ensure every Short & compilation satisfies YouTube Partner Program (YPP) originality rules, avoids reused/mass-produced templates, respects copyright, and declares `containsSyntheticMedia` accurately.

## Activation Conditions
- Before queuing videos into `cloud_queue.json`, building 16:9 compilations, or reviewing YPP milestones.

## Required Inputs
- Script payload, audio/visual asset manifest, `uploaded_history.json`, `memory/VIDEO_HISTORY.json`, `memory/ANALYTICS_HISTORY.json`.

## Step-by-Step Workflow
1. Verify 100% original narration, procedural/custom stickman visuals or licensed/owned assets, and zero third-party copyrighted audio tracks or unrelated watermarks.
2. Confirm per-video variety (`validate_ypp_compliance`): unique narrative descriptions (>100 chars), zero consecutive template titles, distinct audio palettes & visual beats.
3. Audit `containsSyntheticMedia`: `True` whenever photorealistic AI/3D imagery renders in `CloudShort`; `False` for pure B&W vector stickman + diagrammatic educational renders.
4. Track channel progress vs. official YPP tiers (Early Access: 500 subs + 3 uploads/90d + 3M Shorts views or 3k watch hrs; Full Ads: 1,000 subs + 10M Shorts views or 4k watch hrs; noting Feb 2027 higher new-applicant thresholds — never guarantee monetization).

## Output Format
Compliance verdict `{approved, synthetic_flag, copyright_clear, blockers[]}`.

## Validation Criteria
- Zero reused clips, zero unlicensed music, accurate `contains_synthetic_media` boolean.

## Failure Handling
- Block queuing immediately if any violation triggers; rewrite or replace assets before re-testing.

## Security Restrictions
- Never bypass YouTube Content ID, copyright rules, or disclosure fields.

## Examples
- Caught & replaced repetitive `"Why You Should NEVER..."` title spam and identical BGM tracks in `run_agents.py`.
