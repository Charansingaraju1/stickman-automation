# Autonomous AI Stickman YouTube Studio — Workspace Instructions

## Core Engineering Discipline
- Follow **Superpowers** (`.agents/skills/using-superpowers/SKILL.md`) as primary engineering methodology: brainstorm -> write plan -> TDD -> independent review -> verify before claiming done.
- Respect `$0.00` operational lock (`agents/run_agents.py` `assert_zero_cost`). Never activate paid services or publish content without explicit user authorization.
- Never store credentials in tracked files or `memory/`. Keep secrets strictly in `.env` (gitignored), `token.json`, `client_secret.json`, or GitHub Secrets.
- Preserve existing working pipelines (`renderers/`, `upload_to_youtube.py`, `upload_to_instagram.py`, Remotion `src/`).

## Workspace Architecture & Memory
Always read `memory/PROGRESS.md`, `memory/TASKS.md`, and `memory/BUGS.md` before starting multi-step tasks, and update them ONLY after tool verification:
- Specialist Team (18 roles): `.agents/roles/STUDIO_TEAM.md`
- Project Memory Files: `memory/PROJECT.md`, `memory/ARCHITECTURE.md`, `memory/PROGRESS.md`, `memory/TASKS.md`, `memory/DECISIONS.md`, `memory/CHARACTER_BIBLE.md`, `memory/CONTENT_STRATEGY.md`, `memory/VIDEO_HISTORY.json`, `memory/ANALYTICS_HISTORY.json`, `memory/EXPERIMENTS.md`, `memory/LESSONS_LEARNED.md`, `memory/BUGS.md`, `memory/COST_TRACKER.md`
- Safety Gate Hook: `.agents/hooks.json` -> `.agents/hooks/validate-tool-call.mjs`

## Self-Improvement Cycle
`Research -> 30 Ideas -> 100-Pt Score -> Fact Check -> Script -> Independent Critic -> Storyboard -> B&W Vector/Remotion Animate -> Edit & Audio (-14 LUFS) -> FFprobe Quality Check -> Gated Publish -> Analyze (24h/48h/7d) -> Learn -> Improve`
