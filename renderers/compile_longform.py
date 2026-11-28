"""Combine stocked 9:16 Shorts into 16:9 compilations + 1280x720 thumbnails for 4,000 Watch Hours."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from upload_to_youtube import load_viral_queue, send_telegram_alert, upload_video

OUT_MP4 = ROOT / "out" / "sticknation_compilation_16x9.mp4"
OUT_THUMB = ROOT / "out" / "sticknation_compilation_thumb.jpg"
OUT_CHAPTERS = ROOT / "out" / "sticknation_compilation_chapters.txt"
COMP_HISTORY = ROOT / "compilation_history.json"

THEMES = [
    {
        "key": "everyday_physics_vol1",
        "title": "7 Harmless Habits Turning Toxic In 15s!",
        "topBadge": "7 HABITS",
        "headline": "DON'T BLINK!",
        "primary": "scenes/mentos_cola/scene_3_eruption.jpg",
        "secondary": "scenes/knuckle_cracking/scene_2_xray_bones.jpg",
        "order": ["mentos_cola_danger", "knuckle_cracking", "hotel_kettle_danger", "watermelon_seed_myth", "bleach_vinegar_gas", "nosebleed_tilt_mistake", "stay_awake_72h"],
    },
    {
        "key": "hidden_body_traps_vol2",
        "title": "Why Body Tricks Backfire Under 30 Secs!",
        "topBadge": "ZERO PAIN?",
        "headline": "WAIT 15S!",
        "primary": "scenes/knuckle_cracking/scene_1_dark_hook.jpg",
        "secondary": "scenes/watermelon_seed/scene_1_stomach_3d.jpg",
        "order": ["knuckle_cracking", "nosebleed_tilt_mistake", "stay_awake_72h", "watermelon_seed_myth", "reaper_water_burn", "hotel_kettle_danger"],
    },
    {
        "key": "home_chemical_mistakes_vol3",
        "title": "5 Everyday Mistakes Heating Past 200F!",
        "topBadge": "STOP NOW",
        "headline": "DEADLY MIX!",
        "primary": "scenes/hotel_kettle/scene_1_kettle_hook.jpg",
        "secondary": "scenes/mentos_cola/scene_4_geyser_burp.jpg",
        "order": ["bleach_vinegar_gas", "grease_fire_volcano", "superglue_cotton_fire", "hotel_kettle_danger", "mentos_cola_danger"],
    },
]


def _probe_duration(path: pathlib.Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def _select_theme(theme_key: str | None = None) -> dict:
    done = set(json.loads(COMP_HISTORY.read_text(encoding="utf-8"))) if COMP_HISTORY.exists() else set()
    if theme_key:
        for t in THEMES:
            if t["key"] == theme_key:
                return t
        raise ValueError(f"Unknown compilation theme: {theme_key}")
    return next((t for t in THEMES if t["key"] not in done), THEMES[0])


def build_compilation(theme_key: str | None = None, publish: bool = False) -> tuple[pathlib.Path, pathlib.Path]:
    theme = _select_theme(theme_key)
    by_id = {q["id"]: q for q in load_viral_queue()}
    ordered_ids = theme["order"] + [qid for qid in by_id if qid not in theme["order"]]

    clips: list[tuple[dict, pathlib.Path, float]] = []
    for qid in ordered_ids:
        item = by_id.get(qid)
        fname = (item.get("filenames") or [None])[0] if item else None
        if not fname:
            continue
        p = ROOT / "videos" / fname
        if p.exists():
            clips.append((item, p, _probe_duration(p)))
        if len(clips) >= 12:
            break
    if len(clips) < 2:
        raise RuntimeError(f"Need at least 2 MP4s in videos/; found {len(clips)}")

    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    filter_parts: list[str] = []
    concat_inputs: list[str] = []
    chapters: list[str] = []
    cursor = 0.0

    for idx, (item, path, dur) in enumerate(clips):
        mins, secs = divmod(int(cursor), 60)
        chapters.append(f"{mins:02d}:{secs:02d} {item['title']}")
        cursor += dur
        inputs.extend(["-i", str(path)])
        # Blur scaled down to 480x270 first for 10x faster cloud encoding with identical soft cinema look
        filter_parts.append(
            f"[{idx}:v]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,boxblur=6:2,scale=1920:1080,eq=brightness=-0.20[bg{idx}];"
            f"[{idx}:v]scale=608:1080:force_original_aspect_ratio=decrease[fg{idx}];"
            f"[bg{idx}][fg{idx}]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v{idx}];"
            f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo[a{idx}]"
        )
        concat_inputs.extend([f"[v{idx}]", f"[a{idx}]"])

    filter_complex = ";".join(filter_parts) + f";{''.join(concat_inputs)}concat=n={len(clips)}:v=1:a=1[vout][aout]"
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", filter_complex,
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
            "-c:a", "aac", "-b:a", "192k", str(OUT_MP4),
        ],
        check=True,
    )
    OUT_CHAPTERS.write_text("\n".join(chapters) + "\n", encoding="utf-8")

    # Render matched 1280x720 high-contrast thumbnail
    tprops = OUT_MP4.parent / "long_thumb_props.json"
    tprops.write_text(json.dumps({
        "topBadge": theme["topBadge"],
        "headline": theme["headline"],
        "accentHex": "#FFD60A",
        "primaryImgPath": theme["primary"],
        "secondaryImgPath": theme["secondary"],
    }), encoding="utf-8")
    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    subprocess.run(
        [npx_cmd, "remotion", "still", "src/index.ts", "CloudLongThumbnail", str(OUT_THUMB), f"--props={tprops}", "--image-format=jpeg", "--jpeg-quality=90"],
        cwd=str(ROOT),
        check=True,
    )

    total_dur = _probe_duration(OUT_MP4)
    print(f"COMPILATION_BUILT: {OUT_MP4} ({round(total_dur, 1)}s, {len(clips)} clips) + thumb {OUT_THUMB.name}")

    if publish:
        done = json.loads(COMP_HISTORY.read_text(encoding="utf-8")) if COMP_HISTORY.exists() else []
        if theme["key"] in set(done):
            print(f"COMPILATION_SKIP: {theme['key']} already published.")
            return OUT_MP4, OUT_THUMB
        desc = (
            f"All {len(clips)} 3D physics breakdowns in one uninterrupted watch-along:\n\n"
            + "\n".join(chapters)
            + "\n\nWhich habit surprised you the most? #stickman #science #anatomy #facts"
        )
        res = upload_video(
            str(OUT_MP4),
            theme["title"],
            desc,
            ["stickman animation", "science facts", "everyday physics", "medical myths", "compilation"],
            thumbnail_path=str(OUT_THUMB),
            comment_text=f"Which of these {len(clips)} experiments fooled you the hardest? Timestamp yours below 👇",
            contains_synthetic_media=True,
        )
        done.append(theme["key"])
        COMP_HISTORY.write_text(json.dumps(done, indent=2), encoding="utf-8")
        send_telegram_alert(
            f"📺 Weekly 16:9 Compilation LIVE on YouTube!\n\n"
            f"🎬 {theme['title']}\n🔗 https://youtube.com/watch?v={res.get('id')}\n⏱️ {round(total_dur, 1)}s ({len(clips)} clips)"
        )
    return OUT_MP4, OUT_THUMB


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", choices=[t["key"] for t in THEMES], default=None)
    ap.add_argument("--publish", action="store_true")
    args = ap.parse_args()
    build_compilation(theme_key=args.theme, publish=args.publish)
