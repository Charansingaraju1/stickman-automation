---
name: youtube-api-and-safe-publishing
description: Manages official YouTube Data API v3 / Analytics API v2 OAuth scopes, duplicate upload locks, disclosure fields, and pre-publish approval gates (absorbs youtube-api-integration, publishing-verification, duplicate-upload-prevention). Use for auth, queue checks, dry-runs, or authorized uploads.
---

# YouTube API and Safe Publishing

## Purpose
Publish only vetted, unique, policy-compliant Shorts via official Google OAuth & Data API v3, saving video IDs cleanly while blocking duplicate uploads and accidental live posts before approval.

## Activation Conditions
- Running `--auth`, `--status`, `--dry-run`, or authorized `upload_to_youtube.py` / workflow triggers.

## Required Inputs
- `client_secret.json`, `token.json` (`youtube.upload`, `youtube.force-ssl`, `youtube.readonly`, `yt-analytics.readonly`), `cloud_queue.json`, `uploaded_history.json`, `memory/VIDEO_HISTORY.json`.

## Step-by-Step Workflow
1. Verify scopes in `token.json`; warn cleanly if `yt-analytics.readonly` is missing.
2. Check duplicate IDs, normalized titles, and story similarity against `uploaded_history.json` + `memory/VIDEO_HISTORY.json`.
3. Verify `validate_ypp_compliance()`, `containsSyntheticMedia`, `selfDeclaredMadeForKids=False`, category `28` (Science & Technology), and custom thumbnail if present.
4. Always run `--dry-run` during testing; never invoke live public publish without explicit user authorization (`AUTO_PUBLISH_ENABLED=true` or manual `workflow_dispatch`).
5. Record returned YouTube `videoId`, publish timestamp, and metadata into `uploaded_history.json` + `memory/VIDEO_HISTORY.json`.

## Output Format
Structured status or publish receipt `{video_id, url, title, published_at_utc, contains_synthetic_media}`.

## Validation Criteria
- Dry-run passes cleanly; live upload verifies `videos().list(id=...)` receipt or HTTP insert response before marking published.

## Failure Handling
- On OAuth expiry/revocation, guide `--auth` re-consent without printing raw token secrets to stdout logs.

## Security Restrictions
- Keep `.env`, `token.json`, and `client_secret.json` strictly gitignored; load `TELEGRAM_BOT_TOKEN` from env only.

## Examples
- `python upload_to_youtube.py --dry-run` validates metadata, thumbnail, and queue order without spending upload quota (`1,600` units/upload skipped).
