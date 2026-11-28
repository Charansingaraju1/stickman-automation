# KNOWN BUGS & TECH DEBT

| ID | Severity | Component | Description | Status |
|---|---|---|---|---|
| **BUG-001** | **CRITICAL (Code Fixed / Rotation Needed)** | `upload_to_youtube.py` | Previously committed plaintext Telegram `BOT_TOKEN` on `main`. Moved to `.env` + expanded `audit_security()`. **User must still revoke/rotate token via BotFather & update GitHub Secret `TELEGRAM_BOT_TOKEN`.** | Code fixed; waiting token rotation |
| **BUG-002** | **HIGH** | `token.json` | Current OAuth token only authorizes `youtube.upload` + `youtube.force-ssl`; missing `youtube.readonly` and `yt-analytics.readonly`. Analytics pulls cannot succeed until user runs `python upload_to_youtube.py --auth`. | Scopes updated in code; awaiting re-auth |
| **BUG-003** | **MEDIUM** | `daily_shorts.yml` & `weekly_compilations.yml` | Workflows use Python `3.10` while local is `3.15` / `3.11.9`. Also cron runs now gated safely behind `vars.AUTO_PUBLISH_ENABLED == 'true'` (`--dry-run` default). | Cron gated; Python alignment open |
| **BUG-004** | **LOW** | `.agents/skills/remotion-best-practices/` | Duplicate nested reference folders (`remotion-maps` inside `remotion-markup`) inherited from `npx skills` install; no nested `SKILL.md` conflicts, keep tracked via `skills-lock.json`. | Monitored |
