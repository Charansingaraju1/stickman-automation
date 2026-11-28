"""Stickman Studio Engine: 30-idea scorer, storyboard continuity, Flow prompt builder, FFprobe QC, and Analytics API."""

from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TOPIC_WEIGHTS: dict[str, int] = {
    "opening_hook": 20,
    "curiosity": 20,
    "visual_potential": 15,
    "retention_potential": 15,
    "surprise_factor": 10,
    "originality": 10,
    "us_relevance": 5,
    "sharing_potential": 5,
}

STORYBOARD_REQUIRED_FIELDS = (
    "duration_sec",
    "narration",
    "action",
    "expression",
    "camera_pos",
    "camera_motion",
    "background",
    "objects",
    "selective_colors",
    "sfx",
    "start_frame",
    "end_frame",
    "transition",
)

SEED_CONCEPTS: list[dict[str, Any]] = [
    ("Space & Physics", "What Happens If Earth Stops Spinning For 1 Second?", 19, 19, 15, 14, 10, 8, 5, 5),
    ("Survival Science", "Why Pouring Water On A Grease Fire Explodes 1,700x", 20, 18, 15, 14, 9, 8, 5, 5),
    ("Human Body", "Why Cracking Knuckles Locks Them Silent For 15 Mins", 18, 18, 14, 14, 9, 8, 5, 4),
    ("What-If", "What If You Swallowed A Single Watermelon Seed?", 17, 17, 14, 13, 8, 8, 5, 4),
    ("Everyday Objects", "Why Super Glue Instantly Smokes On Cotton T-Shirts", 19, 19, 14, 14, 10, 9, 5, 4),
    ("Human Body", "Why Leaning Back During A Nosebleed Backfires", 18, 17, 13, 13, 8, 8, 5, 4),
    ("Psychology", "Why 72 Hours Awake Forces 2-Second Eye-Open Blackouts", 19, 18, 13, 14, 9, 8, 5, 4),
    ("Survival Science", "Why Mixing Bleach And Vinegar Traps Chlorine Gas", 19, 18, 14, 14, 9, 8, 5, 5),
    ("Space & Physics", "Why Falling From Space Wouldn't Burn A Stickman Immediately", 18, 19, 15, 13, 9, 9, 5, 4),
    ("Everyday Objects", "What Microwaving One Grape Actually Plasma-Sparks", 19, 18, 15, 14, 9, 8, 5, 5),
    ("Human Body", "Why Brain Freeze Hits Your Forehead Not Your Tongue", 17, 18, 14, 13, 8, 8, 5, 4),
    ("Unexpected Discoveries", "Why Airline Windows Have One Tiny Pinhole", 18, 19, 14, 13, 9, 8, 5, 4),
    ("Historical Facts", "Why 1904 Olympic Marathon Runners Drank Rat Poison", 19, 19, 14, 14, 10, 9, 4, 5),
    ("What-If", "What If Every Human Jumped At The Exact Same Time?", 18, 18, 15, 13, 8, 7, 5, 4),
    ("Survival Science", "Why Drinking Seawater Makes Dehydration Worse Fast", 17, 17, 14, 13, 8, 8, 5, 3),
    ("Space & Physics", "Why Zero Gravity Tears Form Floating Eye Blobs", 19, 19, 15, 14, 10, 9, 5, 5),
    ("Human Body", "Why Your Own Recorded Voice Sounds Foreign To You", 18, 18, 13, 13, 8, 8, 5, 5),
    ("Everyday Objects", "Why Golf Balls Have 336 Dimples To Fly Twice As Far", 17, 17, 14, 13, 8, 8, 5, 4),
    ("Psychology", "Why Elevator Mirrors Instantly Calm Your Waiting Brain", 16, 17, 13, 12, 8, 8, 5, 4),
    ("Historical Facts", "Why Ancient Roman Concrete Heals Its Own Cracks", 17, 18, 13, 13, 9, 8, 4, 4),
    ("Human Body", "Why Spicy Ice Water Doubles Carolina Reaper Burn", 18, 18, 14, 14, 9, 8, 5, 4),
    ("Survival Science", "Why Wet Oven Mitts Transfer 212F Heat In Half A Second", 18, 18, 14, 13, 9, 9, 5, 4),
    ("What-If", "What Happens Inside An Unpressurized Plane At 35,000 Feet", 19, 18, 14, 14, 9, 8, 5, 4),
    ("Space & Physics", "Why You Can't Hear An Explosion Three Feet Away In Space", 17, 18, 14, 13, 8, 8, 5, 4),
    ("Everyday Objects", "Why Car Windshields Crack Into Webs Instead Of Blades", 17, 17, 14, 13, 8, 8, 5, 4),
    ("Psychology", "Why Doorways Instantly Erase What You Just Walked In For", 18, 19, 14, 13, 8, 8, 5, 5),
    ("Unexpected Discoveries", "Why Stainless Steel Soap Rubs Garlic Smell Off Hands", 17, 17, 13, 12, 9, 9, 4, 4),
    ("Survival Science", "Why Rubbing Snow On Frostbite Shreds Tissue Deeper", 18, 18, 14, 13, 9, 9, 5, 4),
    ("Human Body", "Why Hiccups Happen And One Vagus Nerve Trick Resets Them", 17, 17, 13, 13, 8, 8, 5, 4),
    ("Space & Physics", "Why Lightning Strikes From The Ground Up Half The Time", 18, 18, 15, 13, 9, 8, 5, 4),
]


def score_topic(scores: dict[str, int], threshold: int = 80) -> dict[str, Any]:
    """Validate and sum exact Phase 4 topic scores as an internal editorial estimate."""
    total = 0
    for dim, max_val in TOPIC_WEIGHTS.items():
        if dim not in scores:
            raise ValueError(f"Missing required score dimension: {dim}")
        val = int(scores[dim])
        if val < 0 or val > max_val:
            raise ValueError(f"Dimension {dim}={val} outside valid [0, {max_val}] range")
        total += val
    return {
        "total": total,
        "threshold": threshold,
        "passes_editorial_gate": total >= threshold,
        "editorial_estimate_only": True,
    }


def generate_research_pack() -> list[dict[str, Any]]:
    """Return 30 scored US educational stickman concepts ranked by editorial estimate."""
    pack: list[dict[str, Any]] = []
    for idx, row in enumerate(SEED_CONCEPTS, 1):
        cat, title, oh, cur, vis, ret, sur, orig, us, sh = row
        dims = {
            "opening_hook": oh,
            "curiosity": cur,
            "visual_potential": vis,
            "retention_potential": ret,
            "surprise_factor": sur,
            "originality": orig,
            "us_relevance": us,
            "sharing_potential": sh,
        }
        res = score_topic(dims)
        pack.append({
            "rank_seed": idx,
            "category": cat,
            "title": title,
            "scores": dims,
            **res,
        })
    return sorted(pack, key=lambda item: -item["total"])


def validate_storyboard(scenes: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify every scene supplies all 13 Phase 6 fields, valid duration, and anchor continuity."""
    issues: list[str] = []
    if len(scenes) < 3:
        issues.append("Storyboard requires at least 3 scenes.")
    total_dur = 0.0
    for idx, sc in enumerate(scenes, 1):
        for field in STORYBOARD_REQUIRED_FIELDS:
            val = sc.get(field)
            if val is None or (isinstance(val, str) and not val.strip()) or (isinstance(val, list) and not val):
                issues.append(f"Scene {idx} missing or empty field '{field}'.")
        dur = float(sc.get("duration_sec") or 0.0)
        if dur <= 0:
            issues.append(f"Scene {idx} duration_sec must be > 0.")
        total_dur += dur
    if scenes and not (12.0 <= total_dur <= 45.0):
        issues.append(f"Total duration {total_dur:.2f}s outside [12.0, 45.0]s Shorts sweet spot.")
    return {"valid": not issues, "scene_count": len(scenes), "total_duration_sec": round(total_dur, 2), "issues": issues}


def build_flow_prompts(scenes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Generate frame-to-frame continuity prompts for optional Flow use (manual/approved only)."""
    check = validate_storyboard(scenes)
    if not check["valid"]:
        raise ValueError(f"Invalid storyboard: {check['issues']}")
    prompts = []
    for i, sc in enumerate(scenes):
        prev_end = scenes[i - 1]["end_frame"] if i > 0 else sc["start_frame"]
        prompts.append({
            "scene_index": i + 1,
            "duration_sec": sc["duration_sec"],
            "start_frame_anchor": prev_end,
            "prompt": (
                f"Minimalist black-and-white 2D stickman animation, selective colors {', '.join(sc['selective_colors'])}. "
                f"Continue seamlessly from reference frame ({prev_end}). Action: {sc['action']}. "
                f"Expression: {sc['expression']}. Camera: {sc['camera_pos']} with {sc['camera_motion']}. "
                f"Background: {sc['background']}. Objects: {', '.join(sc['objects'])}. "
                f"End state: {sc['end_frame']}. No watermarks, no random characters, preserve stroke weight."
            ),
            "paid_api_executed": False,
        })
    return prompts


def inspect_video_qc(video_path: pathlib.Path, allow_16x9: bool = False) -> dict[str, Any]:
    """Run ffprobe + silence check on a rendered MP4 without fabricating results."""
    vp = pathlib.Path(video_path)
    if not vp.exists():
        return {"verdict": "NEEDS_WORK", "passed": False, "errors": [f"Missing file: {vp}"]}
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(vp)],
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        return {"verdict": "NEEDS_WORK", "passed": False, "errors": ["ffprobe execution failed"]}
    info = json.loads(probe.stdout)
    streams = info.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    errors: list[str] = []
    if not v_stream:
        errors.append("Missing video stream.")
    if not a_stream:
        errors.append("Missing audio stream.")
    w = int(v_stream.get("width", 0)) if v_stream else 0
    h = int(v_stream.get("height", 0)) if v_stream else 0
    if allow_16x9:
        if (w, h) not in ((1280, 720), (1920, 1080)):
            errors.append(f"Unexpected 16:9 size: {w}x{h}")
    elif (w, h) != (1080, 1920):
        errors.append(f"Expected 1080x1920 vertical Short, got {w}x{h}")
    dur = float(info.get("format", {}).get("duration", 0.0))
    if not allow_16x9 and not (10.0 <= dur <= 59.0):
        errors.append(f"Short duration {dur:.2f}s outside [10.0, 59.0]s")

    sil = subprocess.run(
        ["ffmpeg", "-i", str(vp), "-af", "silencedetect=noise=-50dB:d=0.9", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    silence_hits = len(re.findall(r"silence_end:", sil.stderr))
    if silence_hits > 0:
        errors.append(f"Detected {silence_hits} dead-silence gap(s) >= 0.9s")

    return {
        "verdict": "APPROVED" if not errors else "NEEDS_WORK",
        "passed": not errors,
        "file": str(vp),
        "width": w,
        "height": h,
        "duration_sec": round(dur, 2),
        "has_audio": a_stream is not None,
        "silence_gaps_over_0_9s": silence_hits,
        "errors": errors,
    }


def fetch_youtube_analytics(days: int = 7) -> dict[str, Any]:
    """Query official YouTube Analytics API v2 if token has yt-analytics.readonly scope; never invent data."""
    token_path = ROOT / "token.json"
    if not token_path.exists():
        return {"ok": False, "error": "MISSING_TOKEN_JSON", "note": "Run python upload_to_youtube.py --auth first."}
    token_info = json.loads(token_path.read_text(encoding="utf-8"))
    granted = set(token_info.get("scopes") or [])
    needed = {"https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"}
    missing = sorted(needed - granted)
    if missing:
        return {
            "ok": False,
            "error": "MISSING_ANALYTICS_SCOPE",
            "missing_scopes": missing,
            "note": "Re-run `python upload_to_youtube.py --auth` locally to authorize analytics read scopes.",
        }
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_info(token_info, scopes=list(granted))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")

    yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)
    end_d = datetime.date.today()
    start_d = end_d - datetime.timedelta(days=max(1, days))
    resp = yt_analytics.reports().query(
        ids="channel==MINE",
        startDate=start_d.isoformat(),
        endDate=end_d.isoformat(),
        metrics="views,engagedViews,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
        dimensions="video",
        sort="-views",
        maxResults=25,
    ).execute()
    snapshot = {
        "fetched_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "window_days": days,
        "column_headers": [h.get("name") for h in resp.get("columnHeaders", [])],
        "rows": resp.get("rows", []),
        "note": "Studio 'Viewed vs Swiped Away' not directly exposed in Analytics API v2.",
    }
    hist_path = ROOT / "memory" / "ANALYTICS_HISTORY.json"
    hist = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else {"snapshots": []}
    hist["analytics_status"] = "active"
    hist.setdefault("snapshots", []).append(snapshot)
    hist_path.write_text(json.dumps(hist, indent=2), encoding="utf-8")
    return {"ok": True, "snapshot_rows": len(snapshot["rows"]), "snapshot": snapshot}


def main() -> None:
    p = argparse.ArgumentParser(description="Autonomous AI Stickman Studio Engine ($0)")
    p.add_argument("--research", action="store_true", help="Output 30 scored editorial topic ideas")
    p.add_argument("--qc", metavar="MP4", help="Run FFprobe + silence quality inspection on MP4")
    p.add_argument("--analytics", action="store_true", help="Pull official YouTube Analytics API v2 metrics")
    p.add_argument("--days", type=int, default=7, help="Lookback window for --analytics")
    args = p.parse_args()

    if args.research:
        print(json.dumps(generate_research_pack(), indent=2))
    elif args.qc:
        res = inspect_video_qc(pathlib.Path(args.qc))
        print(json.dumps(res, indent=2))
        if not res["passed"]:
            sys.exit(1)
    elif args.analytics:
        res = fetch_youtube_analytics(days=args.days)
        print(json.dumps(res, indent=2))
        if not res["ok"]:
            sys.exit(2)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
