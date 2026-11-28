"""Standalone Graph API v21.0 Instagram Reels uploader for @stick_man_nation."""

from __future__ import annotations

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from upload_to_youtube import load_viral_queue, send_telegram_alert

ROOT = pathlib.Path(__file__).resolve().parent
IG_HISTORY_FILE = ROOT / "ig_uploaded_history.json"
RAW_BASE = "https://raw.githubusercontent.com/Charansingaraju1/stickman-automation/main/videos"


def _load_env_fallback() -> tuple[str, str]:
    tok = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    ig_id = os.environ.get("IG_ACCOUNT_ID", "17841451949000745").strip() or "17841451949000745"
    env_p = ROOT / ".env"
    if not tok and env_p.exists():
        for line in env_p.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("IG_ACCESS_TOKEN="):
                tok = s.split("=", 1)[1].strip()
            elif s.startswith("IG_ACCOUNT_ID="):
                ig_id = s.split("=", 1)[1].strip() or ig_id
    return tok, ig_id


def _graph_req(path: str, token: str, params: dict | None = None, post: bool = False) -> dict:
    q = dict(params or {})
    q["access_token"] = token
    encoded = urllib.parse.urlencode(q)
    url = f"https://graph.facebook.com/v21.0/{path}" + ("" if post else f"?{encoded}")
    req = urllib.request.Request(url, data=(encoded.encode("utf-8") if post else None))
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def upload_next_reel(dry_run: bool = False) -> dict | None:
    token, ig_id = _load_env_fallback()
    if not token:
        print("IG_SKIP: IG_ACCESS_TOKEN not configured; skipping Instagram Reels publish cleanly.")
        return None

    posted = json.loads(IG_HISTORY_FILE.read_text(encoding="utf-8")) if IG_HISTORY_FILE.exists() else []
    posted_set = set(posted)

    for item in load_viral_queue():
        if item["id"] in posted_set:
            continue
        fname = (item.get("filenames") or [None])[0]
        if not fname or not (ROOT / "videos" / fname).exists():
            continue

        video_url = f"{RAW_BASE}/{urllib.parse.quote(fname)}"
        caption = f"{item['title']}\n\n{item['description']}\n\n#reels #stickman #science #shorts"[:2150]
        head_req = urllib.request.Request(video_url, method="HEAD", headers={"User-Agent": "StickNation-IG/1.0"})
        with urllib.request.urlopen(head_req, timeout=15) as r:
            if r.status != 200:
                raise RuntimeError(f"Public GitHub MP4 not ready ({r.status}): {video_url}")

        if dry_run:
            acct = _graph_req(ig_id, token, {"fields": "id,username"})
            print(f"[IG DRY RUN] Account @{acct.get('username')} ready -> {item['id']} ({video_url})")
            return {"dry_run": True, "id": item["id"], "username": acct.get("username")}

        container = _graph_req(
            f"{ig_id}/media",
            token,
            {"media_type": "REELS", "video_url": video_url, "caption": caption, "share_to_feed": "true"},
            post=True,
        )
        cid = container["id"]
        for _ in range(24):
            st = _graph_req(cid, token, {"fields": "status_code"})
            code = st.get("status_code")
            if code == "FINISHED":
                break
            if code == "ERROR":
                raise RuntimeError(f"IG media processing failed: {st}")
            time.sleep(5)
        else:
            raise TimeoutError(f"IG media container timed out: {cid}")

        pub = _graph_req(f"{ig_id}/media_publish", token, {"creation_id": cid}, post=True)
        posted.append(item["id"])
        IG_HISTORY_FILE.write_text(json.dumps(posted, indent=2), encoding="utf-8")
        send_telegram_alert(
            f"📱 Reel LIVE on Instagram (@stick_man_nation)!\n\n🎬 {item['title']}\n🆔 IG Media ID: {pub.get('id')}"
        )
        print(f"IG_PUBLISHED: {item['id']} -> {pub.get('id')}")
        return pub

    print("IG_QUEUE_EMPTY: All stocked videos already published to Instagram.")
    return None


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    if "--status" in sys.argv:
        posted = set(json.loads(IG_HISTORY_FILE.read_text(encoding="utf-8"))) if IG_HISTORY_FILE.exists() else set()
        for q in load_viral_queue():
            f = (q.get("filenames") or [""])[0]
            if (ROOT / "videos" / f).exists():
                print(("IG_POSTED " if q["id"] in posted else "IG_READY  "), q["id"], "|", q["title"])
    else:
        upload_next_reel(dry_run=dry)
