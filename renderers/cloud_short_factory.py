"""Autonomous 30fps Remotion + 3D cutaway cloud factory ($0 laptop load)."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.run_agents import STUDIO_VALIDATED_BRIEFS, audit_script, build_offline_script
from renderers.short_builder import OUT_ROOT, VIDEOS_DIR, synthesize_master_audio
from upload_to_youtube import CLOUD_QUEUE_FILE, load_viral_queue, validate_ypp_compliance

CLOUD_PROFILES: dict[str, dict] = {
    "knuckle_cracking": {
        "queue_id": "knuckle_cracking",
        "title": "Bro Thought Cracking Knuckles Breaks Bones… 💀 #shorts",
        "description": "Bro tried to gross out his classmate by popping every knuckle at once, only to find out what actually makes that loud pop inside healthy joint fluid. #shorts #science #stickman #comedy",
        "pinned_comment": "Can you crack your knuckles on command, or does it make your skin crawl? 👇",
        "tags": ["cracking knuckles", "knuckle pop science", "stickman animation", "shorts", "medical facts", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "crack",
        "seed": 118,
        "hook_sfx": "crunch",
        "voice_rate": "+6%",
        "synthetic": True,
        "topBadge": "DO NOT",
        "thumbHeadline": "CRACK IT!",
        "custom_lines": [
            ("NARRATOR", "Too crunchy! Wait—do your fingers actually shatter after forty years of popping?", "1", "alert", 0.06, "TOO CRUNCHY"),
            ("NARRATOR", "Nope. X-rays show finger bones bouncing smoothly without a single scratch.", "2", "doc", 0.06, "ZERO FRACTURE"),
            ("NARRATOR", "Inside each joint sits thick blue fluid cushioning both rounded ends.", "3", "doc", 0.06, "JOINT CUSHION"),
            ("NARRATOR", "Stretch fast, pressure drops, and trapped gas bubbles burst with a snap!", "4", "panic", 0.08, "BUBBLE POP"),
            ("NARRATOR", "So glare straight back at anyone warning you and say...", "5", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", "scenes/knuckle_cracking/scene_1_dark_hook.jpg", "crack", ""),
            ("look_up", "zoom", "scenes/knuckle_cracking/scene_2_xray_bones.jpg", "xray", ""),
            ("casual_stand", "pan", "scenes/knuckle_cracking/scene_3_blue_gel.jpg", "gel", ""),
            ("charge", "shake", "scenes/knuckle_cracking/scene_4_gas_bubble_pop.jpg", "bubble", ""),
            ("pull_door", "push", "scenes/knuckle_cracking/scene_1_dark_hook.jpg", "crack", ""),
        ],
    },
    "hotel_kettle": {
        "queue_id": "hotel_kettle_danger",
        "title": "Bro Thought It Was Regular Tap Water In A Hotel Kettle 😱💀 #shorts",
        "description": "Walking into a cheap motel and boiling tea with zero second thought sounds innocent until you learn what guests illegally wash inside hotel kettles. #shorts #stickman #comedy #science",
        "pinned_comment": "Be honest: do you STILL use hotel kettles when you travel?! 😭🍵👇",
        "tags": ["hotel kettle", "hotel room mistakes", "stickman animation", "shorts", "travel gross facts", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "steam",
        "seed": 211,
        "hook_sfx": "fizz",
        "voice_rate": "+6%",
        "synthetic": True,
        "topBadge": "DO NOT",
        "thumbHeadline": "DRINK IT!",
        "custom_lines": [
            ("NARRATOR", "Hmm, savory! Wait—why does your hotel coffee taste faintly like gym detergent?", "1", "alert", 0.06, "STOP SIPPING"),
            ("NARRATOR", "Because travelers routinely boil dirty socks and underwear inside cheap motel kettles.", "2", "doc", 0.06, "HOTEL SECRET"),
            ("NARRATOR", "Slimy biofilm bacteria cling straight onto that steel heating coil and flake in.", "3", "panic", 0.08, "COIL GRIME"),
            ("NARRATOR", "So dump the first two boils right down the drain because...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", "scenes/hotel_kettle/scene_1_kettle_hook.jpg", "steam", ""),
            ("look_up", "zoom", "scenes/hotel_kettle/scene_2_xray_lint.jpg", "steam", ""),
            ("charge", "shake", None, "steam", ""),
            ("pull_door", "push", "scenes/hotel_kettle/scene_1_kettle_hook.jpg", "steam", ""),
        ],
    },
    "watermelon_seed": {
        "queue_id": "watermelon_seed_myth",
        "title": "Bro Accidentally Swallowed A Watermelon Seed… 🍉😱 #shorts",
        "description": "Every kid panics after gulping down one stray black seed at a picnic, waiting for green leaves to poke out—here is what stomach acid does in seconds. #shorts #stickman #science #mythbusters",
        "pinned_comment": "Who else genuinely believed a tree was growing in their stomach as a kid? 🍉😳👇",
        "tags": ["watermelon seed myth", "swallowed watermelon seed", "stickman comedy", "shorts", "science facts"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "seed",
        "seed": 315,
        "hook_sfx": "squelch",
        "voice_rate": "+7%",
        "topBadge": "WILL IT",
        "thumbHeadline": "SPROUT?!",
        "custom_lines": [
            ("NARRATOR", "Wait—you swallowed a black watermelon seed! Does a vine sprout inside in 7 days?", "1", "alert", 0.06, "SEED ALERT"),
            ("NARRATOR", "No soil, no sunlight, just an acid pool slamming straight into that hard coat.", "2", "doc", 0.06, "ACID BATH"),
            ("NARRATOR", "Instead of growing leaves out your ears, the seed rides safely out untouched.", "3", "panic", 0.08, "ZERO SPROUTS"),
            ("NARRATOR", "Until the whole belly-fruit rumor starts again right when...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", "scenes/watermelon_seed/scene_1_stomach_3d.jpg", "seed", ""),
            ("look_up", "zoom", None, "seed", ""),
            ("casual_stand", "pan", None, "seed", ""),
            ("pull_door", "push", "scenes/watermelon_seed/scene_1_stomach_3d.jpg", "seed", ""),
        ],
        "synthetic": True,
    },
    "bleach_vinegar": {
        "queue_id": "bleach_vinegar_gas",
        "title": "Bro Mixed Bleach And Vinegar To Clean The Shower 💀🧪 #shorts",
        "description": "Mixing two popular household cleaners looks harmless on a stained bathtub tile until your lungs meet yellow chloramine vapor within seconds. #shorts #stickman #chemistry #safety",
        "pinned_comment": "Did you know mixing cleaners makes invisible toxic gas? Stay safe out there 👇",
        "tags": ["bleach and vinegar", "cleaning chemistry", "stickman animation", "shorts", "science", "safety"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "toxic",
        "seed": 419,
        "hook_sfx": "fizz",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "NEVER MIX",
        "thumbHeadline": "CHLORINE!",
        "custom_lines": [
            ("NARRATOR", "Why does your shower air suddenly smell spicy after ten seconds of scrubbing?", "1", "alert", 0.06, "SPICY AIR"),
            ("NARRATOR", "Mixing bleach with acidic vinegar unleashes hot toxic chlorine gas fast.", "2", "doc", 0.06, "GAS CLOUD"),
            ("NARRATOR", "Each deep breath torches tender throat tissue while squeezing your chest tight.", "3", "panic", 0.08, "LUNG STING"),
            ("NARRATOR", "So drop the mop and run outside for fresh air the exact second...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "toxic", "DIY CHEMIST?"),
            ("look_up", "zoom", None, "toxic", "CHLORINE GAS!"),
            ("charge", "shake", None, "toxic", "AIRWAY BURN"),
            ("pull_door", "push", None, "toxic", ""),
        ],
    },
    "nosebleed_tilt": {
        "queue_id": "nosebleed_tilt_mistake",
        "title": "Bro Tilted His Head Back During A Nosebleed… 🩸😬 #shorts",
        "description": "Tilting your head skyward might keep red drops off your hoodie, but gravity pushes warm blood straight down the back of your throat instead of stopping it. #shorts #stickman #medical #firstaid",
        "pinned_comment": "Wait—were you taught tilt BACK or lean FORWARD growing up? 😬👇",
        "tags": ["nosebleed tilt back", "first aid myth", "stickman animation", "shorts", "health", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "chill",
        "seed": 503,
        "hook_sfx": "squelch",
        "voice_rate": "+6%",
        "synthetic": False,
        "topBadge": "STOP TILTING",
        "thumbHeadline": "YOUR HEAD!",
    },
    "stay_awake": {
        "queue_id": "stay_awake_72h",
        "title": "Bro Tried To Stay Awake For 72 Hours Straight… 😵💀 #shorts",
        "description": "Pounding five cups of coffee at two in the morning feels powerful until brain waste forces silent two-second micro-naps while your eyes stay open. #shorts #stickman #sleep #science",
        "pinned_comment": "What is the longest you ever pulled an all-nighter? 😵☕👇",
        "tags": ["72 hours no sleep", "sleep deprivation", "stickman animation", "shorts", "brain science", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "sleep",
        "seed": 607,
        "hook_sfx": "crunch",
        "voice_rate": "+8%",
        "synthetic": False,
        "topBadge": "72 HOURS",
        "thumbHeadline": "NO SLEEP!",
    },
}

DEFAULT_POSES = ("pull_door", "look_up", "casual_stand", "charge", "kneel")
DEFAULT_MOTIONS = ("hook_punch", "zoom", "pan", "shake", "push")


def build_lines_and_scenes(key: str, prof: dict):
    if "custom_lines" in prof:
        raw = prof["custom_lines"]
        lines = [("NARRATOR", txt, sid, mode, gap, "&H0000E6FF&", badge) for _, txt, sid, mode, gap, badge in raw]
        return lines, prof["custom_scenes"]

    brief = STUDIO_VALIDATED_BRIEFS[key]
    lines = [
        ("NARRATOR", f"{brief['mistake_hook']} \"{brief['deadpan_line']}\"", "1", "alert", 0.06, "&H003838FF&", "BAD IDEA"),
        ("NARRATOR", brief["twist_7s"], "2", "doc", 0.06, "&H0000E6FF&", "0:07 TWIST"),
        ("NARRATOR", brief["peak_beat"], "3", "panic", 0.08, "&H003838FF&", "PEAK RISK"),
        ("NARRATOR", brief["loop_bridge"], "4", "loop", 0.00, "&H0000E6FF&", "LOOP CUT"),
    ]
    scenes = [
        (DEFAULT_POSES[i % len(DEFAULT_POSES)], DEFAULT_MOTIONS[i % len(DEFAULT_MOTIONS)], None, prof["fx"], lines[i][6])
        for i in range(len(lines))
    ]
    return lines, scenes


async def build_cloud_short(key: str, enqueue: bool = False) -> dict:
    if key not in CLOUD_PROFILES:
        raise ValueError(f"Unknown cloud profile: {key}")
    prof = CLOUD_PROFILES[key]
    lines, scene_defs = build_lines_and_scenes(key, prof)

    # Compliance audit before rendering a single frame
    audit_payload = {
        "title": prof["title"],
        "lines": [[l[0], l[1], l[2], l[3], l[4], l[5], l[6]] for l in lines],
        "visuals": [[s[2] or f"vec_{key}_{i}", str(i + 1), s[1]] for i, s in enumerate(scene_defs)],
    }
    audit = audit_script(audit_payload)
    if not audit["approved"]:
        raise ValueError(f"Script/YPP audit failed for {key}: {audit['issues']}")

    work_dir = pathlib.Path(OUT_ROOT) / f"{key}_cloud"
    work_dir.mkdir(parents=True, exist_ok=True)
    cfg = {"seed": prof["seed"], "hook_sfx": prof["hook_sfx"], "voice_rate": prof["voice_rate"]}

    words, scene_starts, _, total_dur, norm_master = await synthesize_master_audio(key, lines, cfg, str(work_dir))

    # Build Remotion props synced cleanly to voiceover scene starts
    rem_scenes = []
    for idx, (pose, motion, img_path, fx, callout) in enumerate(scene_defs):
        s_t = scene_starts[idx]
        e_t = scene_starts[idx + 1] if idx + 1 < len(scene_starts) else total_dur
        rem_scenes.append({
            "startSec": round(s_t, 3),
            "endSec": round(e_t, 3),
            "label": lines[idx][6] or "",
            "labelColor": prof["accentHex"],
            "pose": pose,
            "motion": motion,
            "imgPath": img_path,
            "fx": fx,
            "callout": callout if not img_path else "",
        })

    props = {
        "title": prof["title"],
        "bgHex": prof["bgHex"],
        "accentHex": prof["accentHex"],
        "propKind": prof["fx"],
        "durationSec": total_dur,
        "scenes": rem_scenes,
        "words": words,
    }
    props_p = work_dir / "props.json"
    props_p.write_text(json.dumps(props), encoding="utf-8")

    raw_mp4 = work_dir / "remotion_raw.mp4"
    out_mp4_name = f"stickman_{key}_viral.mp4"
    out_mp4 = pathlib.Path(VIDEOS_DIR) / out_mp4_name
    thumb_name = f"stickman_{key}_thumbnail.jpg"
    thumb_p = pathlib.Path(VIDEOS_DIR) / thumb_name

    npx_cmd = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    subprocess.run(
        [npx_cmd, "remotion", "render", "src/index.ts", "CloudShort", str(raw_mp4), f"--props={props_p}", "--crf=22"],
        cwd=str(ROOT),
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_mp4), "-i", norm_master,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4),
        ],
        check=True,
        capture_output=True,
    )

    imgs = list(dict.fromkeys(s[2] for s in scene_defs if s[2]))
    thumb_props = {
        "topBadge": prof["topBadge"],
        "headline": prof["thumbHeadline"],
        "accentHex": prof["accentHex"],
        "primaryImgPath": imgs[0] if len(imgs) >= 1 else None,
        "secondaryImgPath": imgs[-1] if len(imgs) >= 2 else None,
    }
    tprops_p = work_dir / "thumb_props.json"
    tprops_p.write_text(json.dumps(thumb_props), encoding="utf-8")
    subprocess.run(
        [npx_cmd, "remotion", "still", "src/index.ts", "CloudThumbnail", str(thumb_p), f"--props={tprops_p}", "--image-format=jpeg", "--jpeg-quality=88"],
        cwd=str(ROOT),
        check=True,
    )

    entry = {
        "id": prof["queue_id"],
        "contains_synthetic_media": prof["synthetic"],
        "filenames": [out_mp4_name],
        "thumbnail": thumb_name,
        "pinned_comment": prof["pinned_comment"],
        "title": prof["title"],
        "description": prof["description"],
        "tags": prof["tags"],
    }
    if enqueue:
        enqueue_cloud_item(entry)
    size_mb = round(out_mp4.stat().st_size / (1024 * 1024), 2)
    print(f"CLOUD_FACTORY_BUILT: {out_mp4} ({size_mb} MB, {total_dur}s) + thumb {thumb_p.name}")
    return entry


def enqueue_cloud_item(entry: dict) -> None:
    uploaded = []
    hist_p = ROOT / "uploaded_history.json"
    if hist_p.exists():
        uploaded = json.loads(hist_p.read_text(encoding="utf-8"))
    validate_ypp_compliance(entry, uploaded)
    cur = []
    cq = pathlib.Path(CLOUD_QUEUE_FILE)
    if cq.exists():
        cur = json.loads(cq.read_text(encoding="utf-8"))
    existing_ids = {q["id"] for q in load_viral_queue()}
    if entry["id"] not in existing_ids:
        cur.append(entry)
        cq.write_text(json.dumps(cur, indent=2), encoding="utf-8")


def pick_next_unbuilt() -> str | None:
    existing_ids = {q["id"] for q in load_viral_queue()}
    for k, prof in CLOUD_PROFILES.items():
        if prof["queue_id"] not in existing_ids:
            return k
    return None


def main():
    p = argparse.ArgumentParser(description="Autonomous 30fps Remotion + 3D Cloud Factory")
    p.add_argument("--short", choices=list(CLOUD_PROFILES), help="Specific profile key to render")
    p.add_argument("--next", action="store_true", help="Automatically build & enqueue next unbuilt profile")
    p.add_argument("--queue", action="store_true", help="Append validated item into cloud_queue.json")
    p.add_argument("--min-ready", type=int, default=3, help="Minimum queued un-uploaded videos when using --next")
    args = p.parse_args()

    if args.next:
        hist_p = ROOT / "uploaded_history.json"
        uploaded = set(json.loads(hist_p.read_text(encoding="utf-8"))) if hist_p.exists() else set()
        ready_cnt = sum(1 for q in load_viral_queue() if q["id"] not in uploaded)
        if ready_cnt >= args.min_ready:
            print(f"CLOUD_STOCK_OK: {ready_cnt} already ready (>= {args.min_ready}).")
            return
        nxt = pick_next_unbuilt()
        if not nxt:
            print("CLOUD_STOCK_EMPTY: All CLOUD_PROFILES already queued.")
            return
        asyncio.run(build_cloud_short(nxt, enqueue=args.queue))
    elif args.short:
        asyncio.run(build_cloud_short(args.short, enqueue=args.queue))
    else:
        p.error("Specify --short <key> or --next")


if __name__ == "__main__":
    main()
