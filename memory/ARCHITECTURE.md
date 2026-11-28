# ARCHITECTURE

```text
[18 Specialist Roles / Workspace Skills (.agents/skills + .agents/roles/STUDIO_TEAM.md)]
        |
        v
Research & Scoring Engine (agents/studio_engine.py)
  - 30 original ideas/cycle scored out of 100 (editorial estimate)
  - Science Fact Checker ledger + Independent Critic gate
        |
        v
Script & Storyboard Builder (agents/run_agents.py + agents/prompts.py)
  - 15-30s 5-beat narrative + seamless loop + YPP/originality check
        |
        +--> Programmatic Vector Renderer (PRIMARY, $0):
        |      src/Stickman.tsx + src/components/StickmanPhysicsStage.tsx
        |      + src/ZackStickmanShort.tsx + src/CloudShort.tsx -> Remotion @1080x1920
        |
        +--> Optional Frame-Anchored Prompt Exporter (Google Flow / Gemini):
               studio_engine.py --flow-prompts (manual/paid-gated only)
        |
        v
Audio, Captions & Mux (renderers/short_builder.py + FFmpeg)
  - EdgeTTS US voices -> SFX + procedural BGM (-14 LUFS) -> AAC/H.264 faststart
        |
        v
Quality Inspector & Safe Publisher (studio_engine.py --qc + upload_to_youtube.py)
  - ffprobe resolution/audio/silence check -> duplicate check -> dry-run / authorized upload
        |
        v
Analytics & Self-Improvement (studio_engine.py --analytics -> ANALYTICS_HISTORY.json)
  - 24h / 48h / 7d YouTube Analytics API v2 -> EXPERIMENTS.md -> LESSONS_LEARNED.md
```
