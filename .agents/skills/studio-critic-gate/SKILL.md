---
name: studio-critic-gate
description: Independent adversarial critic that challenges weak hooks, bad science, repetitive pacing, visual continuity breaks, or premature completion claims (paired with msitarzewski Reality Checker & Superpowers verification-before-completion). Use before scripting and before publishing.
---

# Independent Studio Critic Gate

## Purpose
Act as a ruthless second set of eyes defaulting to `NEEDS WORK` — catching unverified claims, slow openings, ugly visual breaks, YPP originality hazards, or rushed "done" verdicts before anything ships.

## Activation Conditions
- Stage Gate 1: Before scripting top topic candidates.
- Stage Gate 2: After FFmpeg/Remotion render, before enabling queue/publish.

## Required Inputs
- Script/storyboard OR rendered MP4 + QC report + source claim ledger.

## Step-by-Step Workflow
1. Challenge scientific claims: Could a skeptical viewer or doctor/physicist disprove the central claim? Is speculation clearly separated from fact?
2. Challenge retention & mobile clarity: Does Frame 0 hook visually in `<2s`? Would you scroll past it silently with sound off? Can captions be read cleanly?
3. Challenge continuity & identity: Does every cut match `CHARACTER_BIBLE.md` (mostly B&W + selective signal colors), or did objects/styles clash randomly?
4. Challenge YPP & originality: Is this clearly distinct from Zack D. Films or prior `stickman-daily` uploads?
5. Challenge test evidence: Refuse approval unless actual command exit codes, `ffprobe` metrics, and visual inspection exist.

## Output Format
Structured verdict: `NEEDS_WORK` | `APPROVED`, `critical_flaws[]`, `required_fixes[]`.

## Validation Criteria
- Zero unaddressed critical flaws before moving a draft to `ready` queue.

## Failure Handling
- Reject explicitly with exact line/frame fix instructions; never rubber-stamp low-quality scripts just to meet a daily quota.

## Security Restrictions
- Strictly objective internal audit; never inflate scores or fabricate verification runs.

## Examples
- Rejecting a prototype where Frame 0 opens on a static title card for 1.8s instead of immediate stickman hazard motion.
