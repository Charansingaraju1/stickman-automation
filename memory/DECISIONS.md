# DECISIONS (Architecture Decision Records)

## ADR-001: Primary Methodology = `obra/superpowers`
- **Decision:** Adopt `obra/superpowers` core workflow (`brainstorming` -> `writing-plans` -> `tdd` -> `verification-before-completion`) and reject overlapping heavy harnesses (`everything-claude-code` runtime, `gstack`, bulk `antigravity-awesome-skills`).
- **Why:** Prevents context rot (already 53 global skills) and avoids hook conflicts on Windows without Bun.

## ADR-002: Consolidated Workspace `.agents/skills/` (18 Skills + 13 Remotion Skills)
- **Decision:** Consolidate the 60 requested skill domains into 18 domain-focused skills inside `.agents/skills/` instead of 60 tiny standalone files.
- **Why:** Matches Antigravity progressive-disclosure budget while retaining 100% of required rules and workflows.

## ADR-003: Deterministic B&W Vector Animation First (`$0`) over AI Video Generation
- **Decision:** Prioritize reusable Remotion SVG stickman + physics/anatomy components (`ZackStickmanShort`, `Stickman.tsx`) and treat Google Flow / Vertex Veo as optional/manual due to paid per-second Vertex pricing (`$0.05–$0.60+/s`) and lack of official free Flow API.
- **Why:** Better character continuity, instant programmatic edits, exact YPP safety, `$0.00` cost.

## ADR-004: Safety Gate Before Auto-Publishing
- **Decision:** Scheduled crons default to `--dry-run` unless GitHub Repo Variable `AUTO_PUBLISH_ENABLED=true` is explicitly set (manual `workflow_dispatch` also allowed).
- **Why:** Honors pre-authorization publishing policy and prevents untested drafts from publishing.
