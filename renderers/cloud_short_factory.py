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
        "title": "Why Knuckles Fail For 15 Mins?",
        "description": "Most people think cracking all 10 knuckles snaps cartilage bones, yet X-rays caught your joint silently locking for 15 straight minutes right after each pop. Here is what bursts inside your finger capsule in 24 seconds. #shorts #science #stickman #anatomy",
        "pinned_comment": "How long do YOUR knuckles take before they pop a second time — 15 minutes or longer? 👇",
        "tags": ["cracking knuckles", "knuckle pop 15 minutes", "stickman animation", "shorts", "medical facts", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "crack",
        "seed": 118,
        "hook_sfx": "crunch",
        "voice_rate": "+7%",
        "synthetic": True,
        "topBadge": "ZERO",
        "thumbHeadline": "BONE BREAKS?!",
        "custom_lines": [
            ("NARRATOR", "Stop cracking your 10 knuckles right now—before 15 minutes pass, what fails inside if you try again?", "1", "alert", 0.05, "LOCKED 15M"),
            ("NARRATOR", "In a dead-silent exam room that loud snap sounds terrible, yet X-rays show zero bone scratches.", "2", "doc", 0.05, "NO FRACTURE"),
            ("NARRATOR", "Fast pulling drops capsule pressure hard, sucking dissolved gas straight out of thick joint oil.", "3", "doc", 0.05, "PRESSURE DROP"),
            ("NARRATOR", "A microscopic gas bubble bursts at supersonic speed, locking your joint silent 15 full minutes until...", "4", "panic", 0.06, "GAS BURST"),
            ("NARRATOR", "...your muscles dissolve every trace cleanly right until you snap again and...", "5", "loop", 0.00, "LOOP CUT"),
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
        "title": "Never Drink 1st Hotel Kettle Boil?",
        "description": "Stopping before your hand pours water inside 1 cheap motel kettle might save your stomach, especially when room 204 coffee tastes slightly off. Watch what survives even boiling temperature inside that steel element. #shorts #stickman #travel #science",
        "pinned_comment": "Be honest: do you STILL brew coffee in hotel kettles without dumping the first boil? 😭👇",
        "tags": ["hotel kettle", "hotel room mistakes", "stickman animation", "shorts", "travel gross facts", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "steam",
        "seed": 211,
        "hook_sfx": "fizz",
        "voice_rate": "+7%",
        "synthetic": True,
        "topBadge": "DO NOT",
        "thumbHeadline": "TASTE IT!",
        "custom_lines": [
            ("NARRATOR", "Stop before you touch 1 hotel kettle—did you notice why your midnight coffee tastes weirdly savory?", "1", "alert", 0.05, "HOLD THAT SIP"),
            ("NARRATOR", "Wait before dumping tea bags inside that harmless pot—something nasty soaked there overnight yesterday.", "2", "doc", 0.05, "ROOM 204 RISK"),
            ("NARRATOR", "Guests routinely boil dirty travel socks and underwear inside cheap motel kettles after dark.", "3", "panic", 0.06, "BIOFILM COIL"),
            ("NARRATOR", "Slimy scales glue onto that steel heater element and flake straight back into cup two before...", "4", "loop", 0.00, "LOOP CUT"),
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
        "title": "What 1 Seed Does Inside In 24h?",
        "description": "Every kid panics after swallowing 1 black watermelon seed at a summer picnic, waiting 7 days to see if green sprouts show up. Follow that tough dark seed down through stomach chemistry in 22 seconds. #shorts #stickman #science #mythbusters",
        "pinned_comment": "Who else genuinely believed a whole watermelon grew in their stomach as a kid? 🍉👇",
        "tags": ["watermelon seed myth", "swallowed watermelon seed", "stickman comedy", "shorts", "science facts"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "seed",
        "seed": 315,
        "hook_sfx": "squelch",
        "voice_rate": "+7%",
        "topBadge": "ZERO",
        "thumbHeadline": "VINES GROW?!",
        "custom_lines": [
            ("NARRATOR", "Wait before you spit 1 black seed out—could green vines risk growing inside you within 7 days?", "1", "alert", 0.05, "7-DAY RISK?"),
            ("NARRATOR", "Gulp one seed down mid-bite and childhood panic hits fast while it sinks past your ribs.", "2", "doc", 0.05, "PITCH DARK"),
            ("NARRATOR", "No soil, zero sunlight, just a brutal acid bath slamming straight into that slick dark armor.", "3", "panic", 0.06, "ACID TEST"),
            ("NARRATOR", "That tough shell rides cleanly out untouched twenty-four hours later right when you...", "4", "loop", 0.00, "LOOP CUT"),
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
        "title": "Bleach + Vinegar: 10s Lung Risk?",
        "description": "Mixing 2 everyday bathroom bottles sounds spotless until sharp fumes burn both eyes in 10 seconds inside a closed shower stall. Watch the invisible gas trap before scrubbing tile. #shorts #stickman #chemistry #safety",
        "pinned_comment": "Wait—did anyone ever warn you NOT to mix bleach and vinegar before today? 👇",
        "tags": ["bleach and vinegar", "cleaning chemistry", "stickman animation", "shorts", "science", "safety"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "toxic",
        "seed": 419,
        "hook_sfx": "fizz",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "TOXIC",
        "thumbHeadline": "SPICY AIR!",
        "custom_lines": [
            ("NARRATOR", "Stop scrubbing your shower if the air stings—why do 2 safe bottles turn deadly in 10 seconds?", "1", "alert", 0.05, "10s WARNING"),
            ("NARRATOR", "Splash bleach onto acidic vinegar and your closed bathroom fills fast with stinging yellow fog.", "2", "doc", 0.05, "SHOWER TRAP"),
            ("NARRATOR", "Hot chlorine vapor torches wet lung tissue hard while squeezing chest ribs tighter every breath.", "3", "panic", 0.06, "GAS CLOUD"),
            ("NARRATOR", "Drop that mop and bolt outdoors for cold air the exact second...", "4", "loop", 0.00, "LOOP CUT"),
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
        "title": "Nosebleed? Never Tilt Back 10m!",
        "description": "Tipping your chin skyward keeps blood off your hoodie for 10 seconds, while gravity sends something far worse straight into your airway and stomach. Learn the real 10-minute forward pinch fix. #shorts #stickman #medical #firstaid",
        "pinned_comment": "Be honest: were you told to tilt BACK or lean FORWARD as a kid? 😬👇",
        "tags": ["nosebleed tilt back", "first aid myth", "stickman animation", "shorts", "health", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "chill",
        "seed": 503,
        "hook_sfx": "squelch",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "WRONG",
        "thumbHeadline": "LEAN DOWN!",
        "custom_lines": [
            ("NARRATOR", "Never tip your head up during a 10-second nosebleed—what hidden risk hits your throat before you stop?", "1", "alert", 0.05, "WRONG MOVE"),
            ("NARRATOR", "Leaning skyward keeps crimson stains off white hoodies, fooling you into thinking bleeding slowed down.", "2", "doc", 0.05, "HIDDEN DRIP"),
            ("NARRATOR", "Instead warm blood floods straight down backward toward your stomach and blocks air fast.", "3", "panic", 0.06, "NAUSEA WAVE"),
            ("NARRATOR", "Pinch soft nostrils forward for 10 calm minutes unless you want to...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "chill", "SAVE HOODIE?"),
            ("look_up", "zoom", None, "chill", "BACKWARD DRIP"),
            ("charge", "shake", None, "chill", "LEAN FORWARD"),
            ("pull_door", "push", None, "chill", ""),
        ],
    },
    "stay_awake": {
        "queue_id": "stay_awake_72h",
        "title": "72 Hours Awake? 2s Blackout!",
        "description": "Pounding five espressos to survive 72 hours with zero sleep keeps both eyelids pried wide open while brain waste forces silent 2-second micro-sleeps mid-task. Watch what shuts down inside. #shorts #stickman #sleep #science",
        "pinned_comment": "What is the longest all-nighter streak you ever survived — 24h, 48h, or 72h? ☕👇",
        "tags": ["72 hours no sleep", "sleep deprivation", "stickman animation", "shorts", "brain science", "comedy"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "sleep",
        "seed": 607,
        "hook_sfx": "crunch",
        "voice_rate": "+8%",
        "synthetic": False,
        "topBadge": "MICRO",
        "thumbHeadline": "SLEEP TRAP!",
        "custom_lines": [
            ("NARRATOR", "Never force your body 72 hours without sleep—why does your brain fail for 2 seconds with eyes open?", "1", "alert", 0.05, "HOUR 72"),
            ("NARRATOR", "Five strong espressos pry both tired eyelids wide at 3 AM while toxic proteins flood every wire.", "2", "doc", 0.05, "CAFFEINE MASK"),
            ("NARRATOR", "Suddenly your cortex pulls the plug in 2-second micro-sleeps, freezing your hands blind mid-scroll.", "3", "panic", 0.06, "2S BLACKOUT"),
            ("NARRATOR", "Coffee hides exhaustion right up until your brain force-reboots over the desk and says...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "sleep", "5 ESPRESSOS"),
            ("look_up", "zoom", None, "sleep", "MICRO-SLEEP"),
            ("charge", "shake", None, "sleep", "BRAIN REBOOT"),
            ("pull_door", "push", None, "sleep", ""),
        ],
    },
    "grease_fire": {
        "queue_id": "grease_fire_volcano",
        "title": "400F Grease Fire: 1 Cup Mistake?",
        "description": "Pouring 1 plastic cup of tap water onto flaming 400F cooking oil never puts out a kitchen pan fire—trapped droplets flash 1,700 times bigger into an explosive oil cloud in under a second. #shorts #stickman #safety #physics",
        "pinned_comment": "Honest question: would your first instinct on a stove fire be water, salt, or a metal lid? 👇",
        "tags": ["grease fire water", "kitchen physics", "stickman animation", "shorts", "fire safety"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "fire",
        "seed": 709,
        "hook_sfx": "fizz",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "NEVER POUR",
        "thumbHeadline": "WATER!",
        "custom_lines": [
            ("NARRATOR", "Stop holding that water cup over 400F pan flames—why does 1 splash fail inside seconds?", "1", "alert", 0.05, "400F PAN"),
            ("NARRATOR", "Tap water sinks straight beneath hot cooking oil right onto blazing stove steel underneath.", "2", "doc", 0.05, "1700X STEAM"),
            ("NARRATOR", "It flashes instantly into expanding gas, launching burning oil droplets across your hood until...", "3", "panic", 0.06, "OIL VOLCANO"),
            ("NARRATOR", "you forget a flat metal lid sits right beside your stove hand when...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "fire", "PAN FIRE"),
            ("look_up", "zoom", None, "fire", "STEAM FLASH"),
            ("charge", "shake", None, "fire", "OIL VOLCANO"),
            ("pull_door", "push", None, "fire", ""),
        ],
    },
    "reaper_water": {
        "queue_id": "reaper_water_burn",
        "title": "Carolina Reaper? Why Ice Fails 2x",
        "description": "Chugging cold water after biting a Carolina Reaper cools your lips for half a second while oily capsaicin laughs and spreads across double the pain nerves down your throat. #shorts #stickman #science #food",
        "pinned_comment": "What is the hottest pepper or dish you ever tried, and what actually saved your tongue? 🌶️👇",
        "tags": ["carolina reaper water", "spicy oil science", "stickman animation", "shorts", "biology"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "fire",
        "seed": 811,
        "hook_sfx": "squelch",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "ZERO",
        "thumbHeadline": "RELIEF!",
        "custom_lines": [
            ("NARRATOR", "Never chug cold water after burning spices hit your tongue—what makes mouth heat spike 2 times worse?", "1", "alert", 0.05, "2X WORSE"),
            ("NARRATOR", "Ice water feels helpful for one quick blink while stubborn pepper oil refuses to budge.", "2", "doc", 0.05, "OIL TRAP"),
            ("NARRATOR", "Each gulp splashes spicy oil straight backward across double the throat nerves while...", "3", "panic", 0.06, "THROAT FIRE"),
            ("NARRATOR", "cold whole milk waits untouched right beside your burning plate until...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "fire", "SPICY TRAP"),
            ("look_up", "zoom", None, "fire", "OIL SPREAD"),
            ("charge", "shake", None, "fire", "MILK RESCUE"),
            ("pull_door", "push", None, "fire", ""),
        ],
    },
    "superglue_shirt": {
        "queue_id": "superglue_cotton_fire",
        "title": "1 Super Glue Drop Ignites In 3s?",
        "description": "Spilling 1 liquid drop of super glue onto pure cotton jeans or t-shirts triggers an exothermic shock wave past 200F in 3 seconds, turning harmless craft glue into a skin burn. #shorts #stickman #chemistry #safety",
        "pinned_comment": "Wait—have you ever felt super glue suddenly get scalding hot on fabric or tissue? 😳👇",
        "tags": ["super glue cotton fire", "exothermic reaction", "stickman animation", "shorts", "chemistry"],
        "bgHex": "#090D16",
        "accentHex": "#FFD60A",
        "fx": "toxic",
        "seed": 907,
        "hook_sfx": "crunch",
        "voice_rate": "+7%",
        "synthetic": False,
        "topBadge": "200F",
        "thumbHeadline": "SHIRT BURN!",
        "custom_lines": [
            ("NARRATOR", "Stop wiping 1 sticky glue spill off cotton tees—why does cloth risk smoking past 200F?", "1", "alert", 0.05, "200F SPARK"),
            ("NARRATOR", "Tight cotton fibers drink liquid glue instantly while tissue wiping doubles every reaction surface.", "2", "doc", 0.05, "HEAT WAVE"),
            ("NARRATOR", "Sudden chemical energy heats fabric past boiling water, blistering chest skin fast until...", "3", "panic", 0.06, "CLOTH CHAR"),
            ("NARRATOR", "your instinct still grabs another dry napkin to scrub faster while...", "4", "loop", 0.00, "LOOP CUT"),
        ],
        "custom_scenes": [
            ("pull_door", "hook_punch", None, "toxic", "GLUE DROP"),
            ("look_up", "zoom", None, "toxic", "COTTON SPARK"),
            ("charge", "shake", None, "toxic", "200F BURN"),
            ("pull_door", "push", None, "toxic", ""),
        ],
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
    uploaded_set = set(uploaded)
    cur = []
    cq = pathlib.Path(CLOUD_QUEUE_FILE)
    if cq.exists():
        cur = json.loads(cq.read_text(encoding="utf-8"))
    idx = next((i for i, q in enumerate(cur) if q.get("id") == entry["id"]), None)
    if idx is not None and entry["id"] not in uploaded_set:
        cur[idx] = entry
        cq.write_text(json.dumps(cur, indent=2), encoding="utf-8")
    elif entry["id"] not in {q["id"] for q in load_viral_queue()}:
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
