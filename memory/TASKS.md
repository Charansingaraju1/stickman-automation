# TASKS

## Immediate Security & Auth (Requires User Action)
- [ ] Revoke exposed Telegram bot token via `@BotFather` (`/revoke`), put new token in local `.env` and GitHub Repo Secret `TELEGRAM_BOT_TOKEN` (+ `TELEGRAM_CHAT_ID`).
- [ ] Run `python upload_to_youtube.py --auth` locally once to authorize `youtube.readonly` + `yt-analytics.readonly`, and update GitHub Secret `YOUTUBE_TOKEN_JSON`.

## Engineering & Studio Backlog
- [x] Security cleanup (`upload_to_youtube.py` + `audit_security()`) and safe workflow gating (`--dry-run` default on cron).
- [x] Install Superpowers + complementary skills + 18 consolidated studio skills + 18 roles + 13 memory files.
- [x] Build `agents/studio_engine.py` (30-concept 100-pt scorer, storyboard continuity validator, Flow continuity prompt builder, ffprobe QC gate, YouTube Analytics API v2 puller).
- [x] Upgrade reusable B&W vector stickman library (`StickmanPhysicsStage.tsx` + `ZackStickmanShort.tsx` + `tests/test_studio_engine.py`).
- [ ] Render and inspect first pure B&W vector `ZackStickmanShort` pilot MP4 before authorizing cron auto-publish (`AUTO_PUBLISH_ENABLED=true`).
- [ ] Collect first 24h / 48h / 7d analytics snapshots after re-authed OAuth and start Experiment EXP-001.
