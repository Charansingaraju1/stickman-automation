import asyncio
import argparse
import edge_tts
import json
import os
import subprocess
import wave
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = os.path.join(BASE_DIR, "out")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

SR = 44100

SHORT_CONFIGS = {
    "ear_bug": {
        "title": "StickNation 3D Ear Bug",
        "output_mp4": "stickman_ear_bug_viral.mp4",
        "assets_subdir": "ear_bug",
        "lines": [
            ("NARRATOR", "If an insect crawls inside your ear, your first instinct could permanently damage your hearing.", "1", "alert", 0.12),
            ("NARRATOR", "Most people immediately grab tweezers or a cotton swab to dig it out. But this is the worst thing you can do.", "2", "doc", 0.15),
            ("STICKMAN", "Wait, so using tweezers pushes it deeper?!", "3", "panic", 0.15),
            ("NARRATOR", "Yes! Poking blindly forces the insect inward, where sharp claws can easily puncture your eardrum.", "4", "alert", 0.18),
            ("NARRATOR", "Instead, doctors tilt your head and pour warm mineral oil to safely float it out.", "5", "doc", 0.12),
            ("NARRATOR", "So before you ever stick anything into your ear...", "6", "loop", 0.08),
        ],
        "ref_tags": [
            (0.05, 3.80, "&H003838FF&", "DANGER: FOREIGN OBJECT IN CANAL"),
            (4.00, 8.80, "&H0000FFF0&", "ANATOMY: AUDITORY CANAL NARROWING"),
            (9.00, 12.00, "&H0000E6FF&", "HAZARD: BLIND TWEEZER INSERTION"),
            (12.20, 18.50, "&H003838FF&", "COMPLICATION: TYMPANIC PERFORATION"),
            (18.70, 24.50, "&H0000FFF0&", "SAFE PROTOCOL: WARM MINERAL OIL FLUSH"),
        ],
        "visuals": [
            ("tunnel.jpg", "1", "push"),
            ("tweezer.jpg", "2", "pan"),
            ("clutch.jpg", "3", "zoom"),
            ("tunnel.jpg", "4", "push"),
            ("tweezer.jpg", "5", "pan"),
            ("tunnel.jpg", "6", "zoom"),
        ],
        "seed": 42,
        "intro_skitter": True,
    },
    "fish_bone": {
        "title": "StickNation 3D Fish Bone",
        "output_mp4": "stickman_fish_bone_viral.mp4",
        "assets_subdir": "fish_bone",
        "lines": [
            ("NARRATOR", "If a sharp fish bone gets stuck in your throat, this common dinner trick can tear your esophagus.", "1", "alert", 0.12),
            ("NARRATOR", "Most people quickly swallow balls of dry bread or rice to push it down. That does the exact opposite.", "2", "doc", 0.15),
            ("STICKMAN", "Wait, swallowing bread pushes the needle deeper?!", "3", "panic", 0.15),
            ("NARRATOR", "Yes! Dense food acts like a hammer, snapping the bone horizontal straight through your esophageal wall toward neck arteries.", "4", "alert", 0.18),
            ("NARRATOR", "Instead, cough gently and let an ENT specialist remove it safely.", "5", "doc", 0.12),
            ("NARRATOR", "So before you swallow another bite at dinner...", "6", "loop", 0.08),
        ],
        "ref_tags": [
            (0.05, 3.80, "&H003838FF&", "EMERGENCY: PHARYNGEAL BONE LODGED"),
            (4.00, 8.80, "&H0000E6FF&", "FATAL MYTH: BREAD BOLUS HAMMERING"),
            (9.00, 12.20, "&H003838FF&", "MECHANISM: HORIZONTAL TISSUE LOCK"),
            (12.40, 19.20, "&H003838FF&", "TRAUMA: ESOPHAGEAL PERFORATION"),
            (19.40, 24.50, "&H0000FFF0&", "SAFE PROTOCOL: ENT ENDOSCOPIC EXTRACTION"),
        ],
        "visuals": [
            ("scene_1_clutch.jpg", "1", "push"),
            ("scene_2_bread.jpg", "2", "pan"),
            ("scene_3_perforation.jpg", "3", "zoom"),
            ("scene_3_perforation.jpg", "4", "shake"),
            ("scene_4_ent_fix.jpg", "5", "pan"),
            ("scene_1_clutch.jpg", "6", "push"),
        ],
        "seed": 77,
        "intro_skitter": False,
    },
    "qtip_ear": {
        "title": "StickNation 3D Q-Tip Warning",
        "output_mp4": "stickman_qtip_viral.mp4",
        "assets_subdir": "qtip_ear",
        "lines": [
            ("NARRATOR", "If you clean your ears with cotton swabs, you aren't removing wax—you're ramming it into your eardrum.", "1", "alert", 0.12),
            ("NARRATOR", "Every twist packs hardened debris deeper down a narrow bone tunnel like an airtight piston.", "2", "doc", 0.15),
            ("STICKMAN", "Wait, a soft cotton swab can tear my eardrum?!", "3", "panic", 0.15),
            ("NARRATOR", "Yes! Compacted wax stretches your paper-thin eardrum until it ruptures, risking severe tinnitus and permanent hearing loss.", "4", "alert", 0.18),
            ("NARRATOR", "Instead, warm saline ear drops gently dissolve wax so your ear clears naturally.", "5", "doc", 0.12),
            ("NARRATOR", "So tomorrow morning right after your shower...", "6", "loop", 0.08),
        ],
        "ref_tags": [
            (0.05, 3.80, "&H003838FF&", "HAZARD: PISTON CERUMEN IMPACTION"),
            (4.00, 8.80, "&H0000E6FF&", "ANATOMY: EXTERNAL AUDITORY CANAL"),
            (9.00, 12.20, "&H003838FF&", "PRESSURE: TYMPANIC STRETCH LIMIT"),
            (12.40, 19.20, "&H003838FF&", "INJURY: MEMBRANE PERFORATION"),
            (19.40, 24.50, "&H0000FFF0&", "SAFE PROTOCOL: WARM SALINE DROPS"),
        ],
        "visuals": [
            ("scene_1_macro.jpg", "1", "push"),
            ("scene_2_mirror.jpg", "2", "pan"),
            ("scene_3_rupture.jpg", "3", "zoom"),
            ("scene_3_rupture.jpg", "4", "shake"),
            ("scene_4_saline.jpg", "5", "pan"),
            ("scene_1_macro.jpg", "6", "push"),
        ],
        "seed": 88,
        "intro_skitter": False,
    },
    "skin_tag": {
        "title": "StickNation 3D Skin Tag Warning",
        "output_mp4": "stickman_skin_tag_viral.mp4",
        "assets_subdir": "skin_tag",
        "lines": [
            ("NARRATOR", "If you try snipping a skin tag off with nail clippers, it can trigger unstoppable bleeding in seconds.", "1", "alert", 0.12),
            ("NARRATOR", "Unlike dead surface skin, a skin tag is fed by living blood vessels and active nerve endings.", "2", "doc", 0.15),
            ("STICKMAN", "Wait, that tiny bump has a real blood vessel?!", "3", "panic", 0.15),
            ("NARRATOR", "Yes! Slicing that stalk severs a direct capillary pump, flooding an open dermal wound with bacteria.", "4", "alert", 0.18),
            ("NARRATOR", "Instead, doctors freeze the base off in seconds with cryotherapy without breaking skin.", "5", "doc", 0.12),
            ("NARRATOR", "So next time you spot one in the mirror...", "6", "loop", 0.08),
        ],
        "ref_tags": [
            (0.05, 3.80, "&H003838FF&", "DANGER: VASCULAR STALK TRAUMA"),
            (4.00, 8.80, "&H0000E6FF&", "ANATOMY: LIVING CAPILLARY FEEDER"),
            (9.00, 12.20, "&H003838FF&", "HEMORRHAGE: ARTERIOLE RUPTURE"),
            (12.40, 19.20, "&H003838FF&", "RISK: DEEP CELLULITIS INFECTION"),
            (19.40, 24.50, "&H0000FFF0&", "SAFE PROTOCOL: DERMAL CRYOTHERAPY"),
        ],
        "visuals": [
            ("scene_1_macro.jpg", "1", "push"),
            ("scene_2_mirror.jpg", "2", "pan"),
            ("scene_3_vessel.jpg", "3", "zoom"),
            ("scene_3_vessel.jpg", "4", "shake"),
            ("scene_4_cryo.jpg", "5", "pan"),
            ("scene_1_macro.jpg", "6", "push"),
        ],
        "seed": 91,
        "intro_skitter": False,
    },
    "two_magnets": {
        "title": "StickNation 3D Two Magnets Lethal",
        "output_mp4": "stickman_magnets_viral.mp4",
        "assets_subdir": "two_magnets",
        "lines": [
            ("NARRATOR", "Swallowing one tiny magnet usually passes right through you, but swallowing two can silently tear your gut apart.", "1", "alert", 0.12),
            ("NARRATOR", "Swallowed minutes apart, they slide into separate loops of intestine before snapping magnetically toward each other.", "2", "doc", 0.15),
            ("STICKMAN", "Wait, they clamp onto my organs through tissue?!", "3", "panic", 0.15),
            ("NARRATOR", "Yes! That vise grip crushes blood flow completely, choking tissue until your bowel walls rot and leak acid.", "4", "alert", 0.18),
            ("NARRATOR", "Once clamped inside, only emergency surgery can safely separate them.", "5", "doc", 0.12),
            ("NARRATOR", "So if anyone ever accidentally holds magnets near their mouth...", "6", "loop", 0.08),
        ],
        "ref_tags": [
            (0.05, 3.80, "&H003838FF&", "HAZARD: NEODYMIUM ATTRACTION"),
            (4.00, 8.80, "&H0000E6FF&", "MECHANISM: CROSS-LOOP CLAMPING"),
            (9.00, 12.20, "&H003838FF&", "INJURY: ISCHEMIC TISSUE VISE"),
            (12.40, 19.20, "&H003838FF&", "TRAUMA: BOWEL NECROSIS & LEAK"),
            (19.40, 24.50, "&H0000FFF0&", "INTERVENTION: EMERGENCY SURGERY"),
        ],
        "visuals": [
            ("scene_1_gut_pull.jpg", "1", "push"),
            ("scene_2_swallow.jpg", "2", "pan"),
            ("scene_3_clamp.jpg", "3", "zoom"),
            ("scene_3_clamp.jpg", "4", "shake"),
            ("scene_4_surgery.jpg", "5", "pan"),
            ("scene_1_gut_pull.jpg", "6", "push"),
        ],
        "seed": 99,
        "intro_skitter": False,
    },
}


async def synth_line(text, voice, rate, pitch, mp3_p, max_retries=4):
    clean = text.replace("?!", "!").replace("...", ",").replace("—", ", ")
    for attempt in range(max_retries):
        try:
            comm = edge_tts.Communicate(clean, voice=voice, rate=rate, pitch=pitch, boundary="WordBoundary")
            raw_words = []
            audio_bytes = bytearray()
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio_bytes.extend(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    s = chunk["offset"] / 10_000_000.0
                    d = chunk["duration"] / 10_000_000.0
                    raw_words.append({"word": chunk["text"], "start": s, "end": s + d})
            if len(audio_bytes) > 0 and len(raw_words) > 0:
                with open(mp3_p, "wb") as f:
                    f.write(audio_bytes)
                return raw_words
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}. Retrying...")
            await asyncio.sleep(1.0)
    raise RuntimeError(f"Failed to synth: {text}")


def fmt_t(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = min(99, int(round((sec - int(sec)) * 100)))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def build_audio_mix(vo, total_dur, scene_starts, cfg):
    N = len(vo)
    t_full = np.linspace(0, total_dur, N, endpoint=False)
    rng = np.random.default_rng(cfg["seed"])

    # Tension bass pulse bed
    beat_hz = 122.0 / 60.0
    pulse = np.exp(-((t_full * beat_hz) % 1.0) * 7.5)
    dark_bed = (
        0.48 * np.sin(2 * np.pi * 55.00 * t_full) +
        0.30 * np.sin(2 * np.pi * 82.41 * t_full) +
        0.22 * np.sin(2 * np.pi * 110.00 * t_full) * pulse
    )
    music = dark_bed * 0.13

    sfx = np.zeros(N, dtype=np.float32)

    def add_sfx(start_s, arr, gain=1.0):
        i0 = int(start_s * SR)
        i1 = min(N, i0 + len(arr))
        if i1 > i0:
            sfx[i0:i1] += arr[:i1 - i0] * gain

    def make_vine_boom(dur=1.05):
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        f = np.linspace(88, 26, nt)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.8)
        hit = np.sin(2 * np.pi * 165 * tt) * np.exp(-tt * 14.0)
        return sub * 0.85 + hit * 0.35

    def make_whoosh(dur=0.26, low=160, high=780):
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        n = np.convolve(rng.normal(0, 1, nt), np.ones(25) / 25.0, mode="same")
        env = np.sin(np.pi * tt / dur) ** 1.5
        sw = np.sin(2 * np.pi * np.cumsum(np.linspace(low, high, nt)) / SR) * 0.25
        return (n * 0.9 + sw) * env

    if cfg.get("intro_skitter"):
        skit_dur = 0.85
        nt_skit = int(SR * skit_dur)
        tt_skit = np.linspace(0, skit_dur, nt_skit)
        skit_audio = (
            rng.normal(0, 1, nt_skit)
            * (np.sin(2 * np.pi * 28 * tt_skit) > 0).astype(np.float32)
            * np.exp(-tt_skit * 1.5)
            * 0.35
        )
        add_sfx(0.05, skit_audio, 0.85)
    else:
        # 0:00.05 crisp visual hook snap + sub punch
        add_sfx(0.05, make_vine_boom(0.70), 0.55)

    # 0:03.5-0:04.0 sensory jolt to kill early drop-off cliff + cut whooshes on transitions
    for idx in range(1, len(scene_starts)):
        t_cut = scene_starts[idx]
        add_sfx(max(0.0, t_cut - 0.12), make_whoosh(), 0.40)
        if idx in (1, 3, 5):
            add_sfx(t_cut, make_vine_boom(0.95), 0.72)

    mix = vo * 1.12 + music + sfx
    pk = np.max(np.abs(mix))
    if pk > 0.94:
        mix = np.tanh(mix / 0.94) * 0.94
    return np.column_stack((mix, mix))


def build_ass_subtitles(timeline_words, total_dur, cfg):
    # Strict 1-3 words per beat positioned inside vertical center safe zone (Alignment=2, MarginV=760 -> ~45-58% screen height)
    chunks = []
    cur = []
    for w in timeline_words:
        if cur and (w["scene_id"] != cur[-1]["scene_id"] or w["speaker"] != cur[-1]["speaker"] or len(cur) >= 3):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

    ass_lines = [
        "[Script Info]",
        f"Title: {cfg['title']}",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # Mobile safe zone: Alignment=2 MarginV=760 places heavy captions in vertical center-middle (away from bottom 25% UI & right icons)
        "Style: Default,Impact,92,&H00FFFFFF,&H0000E6FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,10,5,2,60,110,760,1",
        "Style: StickmanTalk,Impact,98,&H0000E6FF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,11,5,2,60,110,760,1",
        # Top clinical tag safely at 140px from top (avoids bottom UI completely)
        "Style: RefTag,Arial,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,-1,0,0,0,100,100,2,0,3,14,0,8,50,50,140,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for rs, re_t, rcol, rtxt in cfg["ref_tags"]:
        if rs < total_dur:
            ass_lines.append(f"Dialogue: 1,{fmt_t(rs)},{fmt_t(min(re_t, total_dur))},RefTag,,0,0,0,,{{\\c{rcol}}}{rtxt}")

    HL = {"alert": "&H003838FF&", "doc": "&H0000E6FF&", "panic": "&H003838FF&", "loop": "&H0000E6FF&"}

    for ci, ch in enumerate(chunks):
        spk = ch[0]["speaker"]
        mode = ch[0]["mode"]
        style = "StickmanTalk" if spk == "STICKMAN" else "Default"
        base_col = "&H00FFFFFF&"
        hl_col = HL.get(mode, "&H0000E6FF&")
        next_chunk_start = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else total_dur

        for j, active in enumerate(ch):
            t_s = active["start"]
            t_e = ch[j + 1]["start"] if j + 1 < len(ch) else min(next_chunk_start, active["end"] + 0.35)
            if mode == "loop" and j == len(ch) - 1:
                t_e = total_dur

            line_parts = []
            for k, other in enumerate(ch):
                wtxt = other["word"].upper()
                if k == j:
                    line_parts.append(f"{{\\c{hl_col}\\fscx112\\fscy112}}{wtxt}{{\\r{style}}}")
                elif k < j:
                    line_parts.append(f"{{\\c{base_col}}}{wtxt}")
                else:
                    line_parts.append(f"{{\\c&H80A0A0A0&}}{wtxt}")
            ass_lines.append(f"Dialogue: 2,{fmt_t(t_s)},{fmt_t(t_e)},{style},,0,0,0,,{' '.join(line_parts)}")

    return "\n".join(ass_lines)


async def render_short(short_key):
    if short_key not in SHORT_CONFIGS:
        raise ValueError(f"Unknown short key: {short_key}. Available: {list(SHORT_CONFIGS.keys())}")

    cfg = SHORT_CONFIGS[short_key]
    work_dir = os.path.join(OUT_ROOT, f"{short_key}_build")
    assets_dir = os.path.join(BASE_DIR, "assets", cfg["assets_subdir"])
    os.makedirs(work_dir, exist_ok=True)

    print(f"\n=== [{short_key}] STEP 1: SYNTHESIZING VOICE OVER ===")
    timeline_words = []
    audio_chunks = []
    scene_starts = []
    scene_ends = {}
    cursor = 0.05
    audio_chunks.append(np.zeros(int(cursor * SR), dtype=np.float32))

    for idx, (spk, text, scene_id, mode, gap) in enumerate(cfg["lines"]):
        mp3_p = os.path.join(work_dir, f"line_{idx:02d}.mp3")
        wav_p = os.path.join(work_dir, f"line_{idx:02d}.wav")

        voice = "en-US-GuyNeural" if spk == "STICKMAN" else "en-US-ChristopherNeural"
        rate = "+12%" if spk == "STICKMAN" else "+8%"
        pitch = "+10Hz" if spk == "STICKMAN" else "+0Hz"

        print(f"  Synthesizing [{spk}] Line {idx}: {text}")
        raw_words = await synth_line(text, voice, rate, pitch, mp3_p)
        await asyncio.sleep(0.1)

        subprocess.run(["ffmpeg", "-y", "-i", mp3_p, "-ar", str(SR), "-ac", "1", wav_p], check=True, capture_output=True)
        with wave.open(wav_p, "rb") as w:
            arr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

        nz = np.where(np.abs(arr) > 0.015)[0]
        if len(nz) > 0:
            trim_start = max(0, nz[0] - int(0.02 * SR))
            trim_end = min(len(arr), nz[-1] + int(0.05 * SR))
            arr = arr[trim_start:trim_end]
            shift_trim = trim_start / SR
        else:
            shift_trim = 0.0

        pk = np.max(np.abs(arr)) + 1e-6
        arr = (arr / pk) * (0.92 if spk == "STICKMAN" else 0.88)

        seg_start = 0.0 if idx == 0 else cursor
        scene_starts.append(seg_start)

        for rw in raw_words:
            ws = max(cursor, cursor + rw["start"] - shift_trim)
            we = max(ws + 0.05, cursor + rw["end"] - shift_trim)
            timeline_words.append({
                "word": rw["word"],
                "start": round(ws, 3),
                "end": round(we, 3),
                "speaker": spk,
                "mode": mode,
                "scene_id": scene_id,
            })

        audio_chunks.append(arr)
        cursor += len(arr) / SR
        if gap > 0:
            audio_chunks.append(np.zeros(int(gap * SR), dtype=np.float32))
            cursor += gap
        scene_ends[scene_id] = cursor

    vo = np.concatenate(audio_chunks)
    total_dur = round(len(vo) / SR, 2)
    print(f"  Voiceover ready: {total_dur}s")

    print(f"=== [{short_key}] STEP 2: AUDIO MIXING (-14 LUFS) ===")
    stereo = build_audio_mix(vo, total_dur, scene_starts, cfg)
    raw_master = os.path.join(work_dir, "master_raw.wav")
    with wave.open(raw_master, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1.0, 1.0) * 32767.0).astype(np.int16).tobytes())

    norm_master = os.path.join(work_dir, "master_norm.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", raw_master, "-af", "loudnorm=I=-14:TP=-1.2:LRA=7", "-ar", "44100", "-ac", "2", norm_master],
        check=True,
        capture_output=True,
    )

    print(f"=== [{short_key}] STEP 3: GENERATING SAFE-ZONE ASS SUBTITLES ===")
    ass_path = os.path.join(work_dir, "captions.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(build_ass_subtitles(timeline_words, total_dur, cfg))

    print(f"=== [{short_key}] STEP 4: RENDERING CLIPS & MUXING ===")
    clip_files = []
    for idx, (img_name, scene_id, motion) in enumerate(cfg["visuals"]):
        t_start = scene_starts[idx]
        t_end = scene_starts[idx + 1] if idx + 1 < len(cfg["visuals"]) else total_dur
        dur = max(0.5, round(t_end - t_start, 2))
        img_p = os.path.join(assets_dir, img_name)
        if not os.path.exists(img_p):
            raise FileNotFoundError(f"Missing visual asset: {img_p}")

        clip_p = os.path.join(work_dir, f"clip_{idx}.mp4")
        frames = int(dur * 30) + 2
        if motion == "push":
            zoom_expr = "min(zoom+0.0020,1.20)"
            xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        elif motion == "shake":
            zoom_expr = "1.08+0.08*on/" + str(max(1, frames))
            xy = "x='iw/2-(iw/zoom/2)+6*sin(on*2.0)':y='ih/2-(ih/zoom/2)+4*cos(on*2.3)'"
        elif motion == "zoom":
            zoom_expr = "min(1.04+0.0022*on,1.22)"
            xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        else:
            zoom_expr = "max(1.16-0.0016*on,1.0)"
            xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"

        vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='{zoom_expr}':d={frames}:{xy}:s=1080x1920:fps=30,format=yuv420p"
        subprocess.run(
            ["ffmpeg", "-y", "-loop", "1", "-i", img_p, "-vf", vf, "-t", f"{dur:.2f}", "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "16", clip_p],
            check=True,
            capture_output=True,
        )
        clip_files.append(clip_p)

    concat_txt = os.path.join(work_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cp in clip_files:
            f.write(f"file '{cp.replace(os.sep, '/')}'\n")

    raw_video = os.path.join(work_dir, "video_raw.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", raw_video], check=True, capture_output=True)

    ass_esc = ass_path.replace("\\", "/").replace(":", "\\:")
    final_mp4 = os.path.join(VIDEOS_DIR, cfg["output_mp4"])
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", raw_video, "-i", norm_master,
            "-vf", f"vignette=PI/10,ass='{ass_esc}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-shortest", final_mp4,
        ],
        check=True,
        capture_output=True,
    )

    dur_out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", final_mp4]
    ).decode().strip()
    mb = os.path.getsize(final_mp4) / (1024 * 1024)
    print(f"SUCCESS [{short_key}]: {final_mp4} ({mb:.2f} MB, {dur_out}s)")
    return final_mp4


async def main():
    parser = argparse.ArgumentParser(description="StickNation Automated Cloud/Local Short Builder")
    parser.add_argument("--short", required=True, help="Short key (fish_bone, qtip_ear, ear_bug, or 'all')")
    args = parser.parse_args()

    targets = list(SHORT_CONFIGS.keys()) if args.short == "all" else [args.short]
    for k in targets:
        await render_short(k)


if __name__ == "__main__":
    asyncio.run(main())
