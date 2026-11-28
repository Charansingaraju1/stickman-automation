# AI Specialist Team (18 Logical Roles)

Execution model in Antigravity: Use `invoke_subagent` / `define_subagent` (`research`, `browser`, `self`) where parallel separation adds independent skepticism (e.g., Independent Critic, Security Reviewer, Viral/Science Researcher); otherwise execute sequentially in strict role handoff order without skipping gates.

| # | Role | Owning Skill(s) | Execution Mode | Primary Artifact / Gate |
|---:|---|---|---|---|
| 1 | **Master Orchestrator** | `stickman-master-orchestrator`, `using-superpowers` | Main coordinator | End-to-end run state in `memory/PROGRESS.md` |
| 2 | **Viral Researcher** | `youtube-topic-and-trend-intel` | `research` subagent / sequential | 30 raw original concepts + public trend evidence |
| 3 | **Science Researcher** | `deep-research-and-fact-check` | `research` subagent / sequential | Scientific mechanism notes (`[FACT]` vs `[HYPOTHETICAL]`) |
| 4 | **Fact Checker** | `deep-research-and-fact-check` | Independent `research` pass | Cited source verification; vetoes unverified stats |
| 5 | **Scriptwriter** | `hook-script-and-retention`, `youtube-packaging-and-seo` | Sequential | 15-30s US English beat script + mobile-safe title |
| 6 | **Creative Director** | `stickman-bible-and-continuity` | Sequential | Scene-by-scene storyboard matching `CHARACTER_BIBLE.md` |
| 7 | **Stickman Animator** | `scientific-viz-and-physics-motion` | Sequential (`src/` Remotion SVG) | B&W + selective-color vector poses, props, physics scenes |
| 8 | **Google Flow Specialist** | `flow-and-gemini-prompt-craft` | Optional (`browser` / prompt out) | Frame-anchored Flow prompts (only when vector isn't enough) |
| 9 | **Remotion Developer** | `remotion-best-practices`, `scientific-viz-and-physics-motion` | Sequential (`src/`) | TSX compositions, springs, zoom/pan choreography, stills |
| 10 | **Voiceover Specialist** | `voiceover-sfx-and-captions` | Sequential (`short_builder.py`) | Natural US EdgeTTS WAV + word timestamps |
| 11 | **Video Editor** | `ffmpeg-render-and-qa`, `voiceover-sfx-and-captions` | Sequential (`renderers/`) | `-14 LUFS` audio mux, SFX, safe-zone captions, 1080x1920 MP4 |
| 12 | **Quality Inspector** | `ffmpeg-render-and-qa` | Automated + visual check | `studio_engine.py --qc` + sample frame inspection |
| 13 | **YouTube Growth Analyst** | `youtube-growth-and-experiments` | Scheduled / sequential | Real API `24h`/`48h`/`7d` pull -> `ANALYTICS_HISTORY.json` |
| 14 | **Publishing Manager** | `youtube-api-and-safe-publishing`, `ypp-originality-and-compliance` | Gated sequential | Duplicate check, synthetic disclosure, dry-run / authorized upload |
| 15 | **Software Engineer** | `test-driven-development`, `systematic-debugging` | Main / `self` subagent | Tested Python/TS modules, bug fixes, self-checks |
| 16 | **Cloud Engineer** | `cloud-and-browser-ops`, `reliability-and-performance` | Main / sequential | GitHub Actions, Azure cost analysis, Telegram alerts |
| 17 | **Security Reviewer** | `architecture-and-security-audit` | Independent review pass | `audit_security()`, `.gitignore` hygiene, least-privilege OAuth |
| 18 | **Independent Critic** | `studio-critic-gate`, `requesting-code-review` | Mandatory veto pass | Challenges weak hooks/science/visuals before script & publish |
