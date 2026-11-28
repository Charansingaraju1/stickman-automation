---
name: hook-script-and-retention
description: Writes 15-30s Zack-style American English Shorts scripts optimized for open-loop retention and seamless looping (absorbs viral-hook-generator, curiosity-gap-optimizer, audience-retention-engine, short-form-scriptwriter, seamless-loop-designer). Use after topic fact-check passes.
---

# Hook, Script, and Retention Engine

## Purpose
Turn fact-checked concepts into tight 15-30s spoken scripts with immediate 0-2s hooks, clean explanatory escalation, surprising payoff, and seamless Frame-0 audio/visual loop.

## Activation Conditions
- Writing or revising any Short script before storyboarding.

## Required Inputs
- Fact-checked claim ledger + chosen concept from `youtube-topic-and-trend-intel`.

## Step-by-Step Workflow
1. Structure narrative beats to match story length (default 15-30s, ~50-85 words):
   - `0-2s`: Immediate curiosity-driven opening (visual conflict or bold question; zero "Hey guys", zero subscribe asks).
   - `2-7s`: Ground scenario & personal stakes in plain American English.
   - `7-15s`: Escalate & explain exact mechanism (visual first, clear science).
   - `15-25s`: Deliver surprising consequence or answer.
   - `Final seconds`: Conclude cleanly or cut mid-clause into Frame 0 for a natural loop.
2. Separate verified `[FACT]` statements from `[HYPOTHETICAL]` premises explicitly.
3. Run deterministic `agents/run_agents.py` `audit_script()` (blocks jargon, template hooks, filler, and trailing outros).

## Output Format
Timed beat array compatible with `renderers/short_builder.py` & storyboard JSON (`duration`, `narration`, `mode`, `badge`, `loop_cut`).

## Validation Criteria
- Natural read time matches target duration; zero banned filler ("actually", "really", "subscribe"); passes `audit_script()`.

## Failure Handling
- Reject & rewrite any hook that spoils the answer before 0:13 or opens slowly.

## Security Restrictions
- Original writing only; never plagiarize scripts from reference creators.

## Examples
- `0-2s`: *"Stop pouring tap water onto a 400-degree pan fire."* -> `2-7s`: Water drops under lighter burning oil -> `7-15s`: Flashes 1,700x into steam -> `15-22s`: Launches flaming oil mushroom while pot lid waits nearby.
