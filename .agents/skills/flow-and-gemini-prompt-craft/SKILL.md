---
name: flow-and-gemini-prompt-craft
description: Crafts continuity-locked prompts for optional Google Flow video or Gemini images when organic texture is specifically needed (absorbs google-flow-prompt-engineer, gemini-image-prompt-engineer). Use only when programmatic SVG/Remotion cannot depict a visual cleanly.
---

# Google Flow and Gemini Prompt Craft

## Purpose
Produce continuity-preserving video/image prompts referencing actual prior final frames without triggering hallucinations, character drift, or unauthorized scraping.

## Activation Conditions
- Only when storyboard explicitly requests optional AI raster/video assets (`Flow` manual/Vertex or Antigravity `image-generator` / `gemini-api` free quota).

## Required Inputs
- Storyboard beat, `CHARACTER_BIBLE.md` palette/camera spec, actual last-frame image path from previous clip.

## Step-by-Step Workflow
1. Check programmatic feasibility first: can Remotion SVG / Manim / Pillow draw this cleanly at `$0`? If yes, skip AI generation.
2. When AI generation is warranted and authorized: pass previous clip's actual extracted final frame (`ffmpeg -sseof -0.1 ... last_frame.png`) as reference anchor (do not restart scene from scratch).
3. Lock style tokens ("minimalist black-and-white matte stickman ink illustration, sparse selective accent color, identical lighting and camera angle, zero unrelated watermarks").
4. Generate separate narration via `voiceover-sfx-and-captions` (`EdgeTTS`) for crisp US pronunciation instead of relying on video-generated speech.
5. Inspect output frame-by-frame; regenerate only failed scenes.

## Output Format
Structured prompt JSON `{scene_id, start_frame_ref, positive_prompt, negative_constraints, camera_lock}`.

## Validation Criteria
- Explicit `start_frame_ref` continuity on scenes >=2; `contains_synthetic_media=True` automatically flagged if used.

## Failure Handling
- If character drifts, objects teleport, or daily free credits exhaust, fall back cleanly to deterministic `StickmanPhysicsStage` SVG scene.

## Security Restrictions
- **Never** automate consumer Google Flow web UI headlessly via scraped cookies/ToS bypasses. Use official Vertex/Gemini APIs (paid approval required if billed) or manual Flow UI only.

## Examples
- Generating `agents/studio_engine.py --flow-prompts` output anchored to `scene_1_end.png` while preserving camera angle and character line weight.
