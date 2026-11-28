---
name: stickman-bible-and-continuity
description: Maintains StickNation B&W visual identity, character proportions, selective color rules, and complete scene-by-scene storyboards (absorbs cinematic-storyboard-director, stickman-character-designer, character-continuity-controller, scene-continuity-controller). Use before generating scenes or editing animations.
---

# Stickman Bible and Continuity Controller

## Purpose
Enforce visual consistency across every frame and episode using `memory/CHARACTER_BIBLE.md` so videos have an unmistakable channel identity (mostly B&W + selective signal colors).

## Activation Conditions
- Creating storyboards or adding components/props to `src/`.

## Required Inputs
- Script beat sheet, `memory/CHARACTER_BIBLE.md`, `studio_engine` storyboard schema.

## Step-by-Step Workflow
1. Lock character geometry (`headRadius=38` at `1080x1920`, `spine strokeWidth=16`, `limb strokeWidth=14`, pure `#000000` ink on crisp light `#FAFAFA` or high-contrast diagrammatic backdrops).
2. Restrict selective accent colors strictly to pedagogical focal objects (`#FF3B30` hazard/blood/heat, `#00E5FF` electric/X-ray, `#2ECC71` chemical, `#FFD60A` warning/energy).
3. Emit structured scene storyboard before rendering: `duration`, `narration`, `action`, `expression`, `camera_pos`, `camera_motion`, `background`, `objects`, `selective_colors`, `sfx`, `start_frame`, `end_frame`, `transition`.
4. Verify consecutive scenes connect without random props, broken character heights, or sudden lighting flips (`validate_storyboard`).

## Output Format
Validated storyboard JSON consumed by `ZackStickmanShort` or `CloudShort`.

## Validation Criteria
- Scene sum duration matches audio length within `0.15s`; all 13 storyboard fields non-empty per beat.

## Failure Handling
- Reject storyboards with missing continuity anchors (`start_frame` != prior `end_frame` state) and repair affected scene only.

## Security Restrictions
- Original visual designs only; never trace/copy another creator's branded mascot verbatim.

## Examples
- Scene 1 ends kneeling with red spark on cotton shirt -> Scene 2 `start_frame` zooms directly onto that exact red spark at `centerX=540`, no teleporting character.
