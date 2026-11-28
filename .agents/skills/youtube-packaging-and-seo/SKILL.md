---
name: youtube-packaging-and-seo
description: Optimizes mobile-safe US YouTube Shorts titles, descriptions, hashtags, and thumbnail pairings without deceptive clickbait (absorbs youtube-seo-specialist, title-optimization, plus msitarzewski Video Optimization Specialist checklists). Use before queuing or publishing any Short.
---

# YouTube Packaging and SEO

## Purpose
Maximize authentic feed CTR and search discoverability for US viewers using crisp titles paired with matching Frame-0 visuals and honest metadata.

## Activation Conditions
- Creating metadata in `cloud_queue.json` or auditing low-CTR Shorts (`yt-package`, `yt-seo`).

## Required Inputs
- Verified script, core topic keyword, and Frame-0 thumbnail frame.

## Step-by-Step Workflow
1. Draft <=40-char mobile-safe title (max ~3 words on thumbnail badge/headline when generated, concrete number or visual tension, zero `#shorts` clutter inside short mobile titles).
2. Ensure title + opening visual never lie about what happens in the video (anti-clickbait rule).
3. Write natural American English description (>100 chars, 2-sentence story summary + engaging viewer question + 3-5 focused hashtags `#shorts`).
4. Cross-check against `uploaded_history.json` so consecutive uploads never repeat identical title templates.

## Output Format
Metadata object `{title, description, tags, pinned_comment, thumbnail_headline}`.

## Validation Criteria
- Title <=45 chars (target <=38), unique vs history, passes `validate_ypp_compliance()`.

## Failure Handling
- Trim or rewrite titles truncated before key noun/number on mobile feeds.

## Security Restrictions
- Public metadata only; zero keyword stuffing or misleading medical/emergency falsehoods.

## Examples
- Weak: `"Why You Should NEVER Touch Water In A Hot Cooking Oil Fire Explained #shorts"` -> Strong: `"400F Oil + 1 Cup Water?"`
