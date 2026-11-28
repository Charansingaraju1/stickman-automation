---
name: scientific-viz-and-physics-motion
description: Builds deterministic B&W vector stickman poses, physics trajectories, anatomy cross-sections, space environments, and kinetic camera choreography in Remotion/SVG/Python/Manim (absorbs scientific-visualization, remotion-animation-engineer, physics-animation-controller, camera-motion-director, visual-pacing-optimizer). Use when building or upgrading visual animation scenes.
---

# Scientific Visualization and Physics Motion

## Purpose
Deliver smooth, zero-cost (`$0`) deterministic animations in `src/` (Remotion + SVG) — preferring vector components over paid AI video wherever programmatic motion achieves higher visual consistency.

## Activation Conditions
- Implementing new Stickman scenes, physics/gravity/anatomy/explosion/space visuals, camera pan/zoom rigs, or evaluating Manim CE additions.

## Required Inputs
- Validated storyboard JSON + `src/components/Stickman.tsx` / `AnatomyDiagram.tsx` / `StickmanPhysicsStage.tsx`.

## Step-by-Step Workflow
1. Check `Stickman.tsx` & `StickmanPhysicsStage.tsx` for existing reusable motions (`walk`, `casual_walk`, `run`, `push`, `charge`, `kneel`, `look_up`, `fall`, `jump`, `point`, `think`, plus `space`, `gravity`, `explosion_safe`, `anatomy`, `diagram` layers).
2. Read relevant installed `remotion-*` skill rules (`remotion-best-practices`, `remotion-captions`) before modifying TSX compositions.
3. Animate camera motion (`interpolate` + `spring`, clamp extrapolated bounds) with fast visual changes every `2-4s` to hold retention without jarring spam transitions.
4. Keep visual palette strictly B&W ink + max 1-2 selective focal colors per beat.
5. Check `npx tsc --noEmit` + test render a still frame or clip via `npx remotion still` / `render`.

## Output Format
Clean TSX components + compiled bundle passing `tsc` and Remotion preview/render.

## Validation Criteria
- Zero static dead stills >2s; TypeScript compiles cleanly (`exit 0`); visual check passes on `1080x1920`.

## Failure Handling
- If Remotion WebGL/Chromium lags on complex shaders, simplify to crisp GPU-friendly SVG paths.

## Security Restrictions
- Only use locally bundled assets (`staticFile(...)`) or open-source MIT/CC0 SVGs.

## Examples
- Button battery Short uses animated SVG zoom (`1.0 -> 1.35`) into `AnatomyDiagram.tsx` showing electric arc flicker & caustic bubble physics without any paid AI video calls.
