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

DEFAULT_VOICES = (
    "en-US-ChristopherNeural",
    "en-US-GuyNeural",
    "en-US-BrianNeural",
)

# Varied per-short harmonic keys & tempos to avoid mass-produced identical audio tracks (YPP compliance)
AUDIO_PALETTES = (
    (118.0, 55.00, 82.41, 110.00, 0.12),   # A minor low pulse
    (124.0, 61.74, 92.50, 123.47, 0.11),   # B tension groove
    (130.0, 65.41, 98.00, 130.81, 0.12),   # C kinetic drive
    (122.0, 49.00, 73.42, 98.00, 0.13),    # G sub suspense
    (134.0, 73.42, 110.00, 146.83, 0.11),  # D brisk comedy pulse
)

SHORT_CONFIGS = {
    "fish_bone": {
        "title": "StickNation 3D Fish Bone",
        "output_mp4": "stickman_fish_bone_viral.mp4",
        "assets_subdir": "fish_bone",
        # (speaker, text, scene_id, mode, gap_s, ref_tag_color, ref_tag_text)
        "lines": [
            ("NARRATOR", "A tiny fish bone wedged in your throat can slice straight through your esophagus if you swallow the wrong food.", "1", "alert", 0.08, "&H003838FF&", "EMERGENCY: PHARYNGEAL BONE LODGED"),
            ("NARRATOR", "Most people panic and force down balls of dry bread or rice, thinking it washes the needle into the stomach.", "2", "doc", 0.08, "&H0000E6FF&", "FATAL MYTH: BREAD BOLUS HAMMERING"),
            ("NARRATOR", "Instead, dense food acts like a solid hammer, slamming into the trapped bone and snapping it sideways.", "3", "alert", 0.08, "&H003838FF&", "MECHANISM: HORIZONTAL TISSUE LOCK"),
            ("NARRATOR", "Violent throat spasms drive its razor tip deeper through muscle, dangerously close to major neck arteries.", "4", "panic", 0.10, "&H003838FF&", "TRAUMA: ESOPHAGEAL PERFORATION"),
            ("NARRATOR", "Instead of pushing it down, cough gently and let an ENT specialist lift it out cleanly under scope guidance.", "5", "doc", 0.08, "&H0000FFF0&", "SAFE PROTOCOL: ENT ENDOSCOPIC REMOVAL"),
            ("NARRATOR", "So the next time you feel a sharp poke at dinner...", "6", "loop", 0.05, None, None),
        ],
        # Frame-0 internal anatomy hook (scene_3_perforation first, NEVER slow exterior table opening!)
        "visuals": [
            ("scene_3_perforation.jpg", "1", "hook_punch"),
            ("scene_2_bread.jpg", "2", "pan"),
            ("scene_1_clutch.jpg", "3", "zoom"),
            ("scene_3_perforation.jpg", "4", "shake"),
            ("scene_4_ent_fix.jpg", "5", "pan"),
            ("scene_3_perforation.jpg", "6", "push"),
        ],
        "seed": 77,
        "allow_legacy_repeats": True,
        "hook_sfx": "crunch",
    },
    "qtip_ear": {
        "title": "StickNation 3D Q-Tip Warning",
        "output_mp4": "stickman_qtip_viral.mp4",
        "assets_subdir": "qtip_ear",
        "lines": [
            ("NARRATOR", "Every twist of a cotton swab acts like a piston, slamming hardened earwax deeper against your delicate eardrum.", "1", "alert", 0.08, "&H003838FF&", "HAZARD: PISTON CERUMEN IMPACTION"),
            ("NARRATOR", "Instead of lifting debris out, the blunt tip seals a tight concrete wall inside a dead-end bone tunnel.", "2", "doc", 0.08, "&H0000E6FF&", "ANATOMY: EXTERNAL AUDITORY CANAL"),
            ("NARRATOR", "As pressure builds, compacted wax traps bacteria in place and bends your paper-thin membrane inward.", "3", "alert", 0.08, "&H003838FF&", "PRESSURE: TYMPANIC STRETCH LIMIT"),
            ("NARRATOR", "Pushing one millimeter too far tears the membrane open, rattling middle-ear bones and risking permanent hearing loss.", "4", "panic", 0.10, "&H003838FF&", "INJURY: MEMBRANE PERFORATION"),
            ("NARRATOR", "Instead, warm saline ear drops liquefy trapped wax so your canal flushes itself clean without trauma.", "5", "doc", 0.08, "&H0000FFF0&", "SAFE PROTOCOL: WARM SALINE DROPS"),
            ("NARRATOR", "So tomorrow morning right after your shower...", "6", "loop", 0.05, None, None),
        ],
        "visuals": [
            ("scene_1_macro.jpg", "1", "hook_punch"),
            ("scene_2_mirror.jpg", "2", "pan"),
            ("scene_3_rupture.jpg", "3", "zoom"),
            ("scene_3_rupture.jpg", "4", "shake"),
            ("scene_4_saline.jpg", "5", "pan"),
            ("scene_1_macro.jpg", "6", "push"),
        ],
        "seed": 88,
        "hook_sfx": "squelch",
    },
    "mentos_cola": {
        "title": "StickNation 3D Mentos + Cola Explosion",
        "output_mp4": "stickman_mentos_cola_viral.mp4",
        "assets_subdir": "mentos_cola",
        "voice": "en-US-AndrewMultilingualNeural",
        "voice_rate": "+3%",
        "sub_margin_v": 480,
        "loop_visual_tail": True,
        "lines": [
            ("NARRATOR", "Bro really ate Mentos and chased it with Coke.", "1", "alert", 0.10, "&H003838FF&", "DON'T MIX"),
            ("NARRATOR", "Tiny craters on each mint dump the gas instantly.", "2", "doc", 0.08, "&H0000E6FF&", "GAS SURGE"),
            ("NARRATOR", "In a bottle it flies—inside your belly, it's trapped.", "3", "doc", 0.08, "&H0000E6FF&", "NO EXIT"),
            ("NARRATOR", "Foam swells your gut tighter than a party balloon—", "4", "alert", 0.08, "&H003838FF&", "BALLOON MODE"),
            ("NARRATOR", "until your abs panic into a walking soda volcano!", "5", "panic", 0.10, "&H003838FF&", "SODA VOLCANO"),
            ("NARRATOR", "Your stomach won't pop—it just rockets back up because...", "6", "panic", 0.00, "&H003838FF&", "LOOP WARNING"),
        ],
        "visuals": [
            ("scene_2_gulp.jpg", "1", "hook_punch"),
            ("scene_3_eruption.jpg", "2", "punch4"),
            ("scene_1_stomach_shock.jpg", "3", "pan"),
            ("scene_3_eruption.jpg", "4", "shake"),
            ("scene_4_geyser_burp.jpg", "5", "punch4"),
            ("scene_1_stomach_shock.jpg", "6", "push"),
        ],
        "seed": 124,
        "hook_sfx": "fizz",
    },
}


async def synth_line(text, voice, rate, pitch, mp3_p, max_retries=2):
    clean = text.replace("?!", "!").replace("...", ",").replace("—", ", ")
    candidates = list(dict.fromkeys([voice, *DEFAULT_VOICES]))
    for cand_voice in candidates:
        for attempt in range(max_retries):
            try:
                comm = edge_tts.Communicate(clean, voice=cand_voice, rate=rate, pitch=pitch, boundary="WordBoundary")
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
                print(f"  Attempt {attempt+1} ({cand_voice}) failed: {e}. Retrying...")
                await asyncio.sleep(0.8)
    raise RuntimeError(f"Failed to synth across all voices: {text}")


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

    bpm, f1, f2, f3, bed_gain = AUDIO_PALETTES[cfg["seed"] % len(AUDIO_PALETTES)]
    beat_hz = bpm / 60.0
    pulse = np.exp(-((t_full * beat_hz) % 1.0) * (6.5 + (cfg["seed"] % 3)))
    phrase_mod = 0.85 + 0.15 * np.sin(2 * np.pi * (beat_hz / 4.0) * t_full)
    varied_bed = (
        0.46 * np.sin(2 * np.pi * f1 * t_full) * phrase_mod +
        0.30 * np.sin(2 * np.pi * f2 * t_full) +
        0.24 * np.sin(2 * np.pi * f3 * t_full) * pulse
    )
    music = varied_bed * bed_gain

    sfx = np.zeros(N, dtype=np.float32)

    def add_sfx(start_s, arr, gain=1.0):
        i0 = int(start_s * SR)
        i1 = min(N, i0 + len(arr))
        if i1 > i0:
            sfx[i0:i1] += arr[:i1 - i0] * gain

    def make_vine_boom(dur=0.95):
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        f = np.linspace(92, 26, nt)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.0)
        hit = np.sin(2 * np.pi * 175 * tt) * np.exp(-tt * 15.0)
        return sub * 0.85 + hit * 0.35

    def make_whoosh(dur=0.24, low=170, high=820):
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        n = np.convolve(rng.normal(0, 1, nt), np.ones(24) / 24.0, mode="same")
        env = np.sin(np.pi * tt / dur) ** 1.5
        sw = np.sin(2 * np.pi * np.cumsum(np.linspace(low, high, nt)) / SR) * 0.25
        return (n * 0.9 + sw) * env

    def make_organic_jolt(kind="crunch"):
        dur = 0.45
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        if kind == "crunch":
            bursts = (np.sin(2 * np.pi * 32 * tt) > 0.2).astype(np.float32)
            crackle = rng.normal(0, 1, nt) * bursts * np.exp(-tt * 5.0)
            snap = np.sin(2 * np.pi * 920 * tt) * np.exp(-tt * 28.0)
            return crackle * 0.65 + snap * 0.40
        elif kind == "fizz":
            sizzle = np.diff(rng.normal(0, 1, nt), prepend=0.0) * 0.42
            pops = rng.normal(0, 1, nt) * (rng.random(nt) > 0.92).astype(np.float32) * 1.6
            rise = np.sin(2 * np.pi * np.cumsum(np.linspace(180, 620, nt)) / SR) * 0.28
            return (sizzle + pops + rise) * np.exp(-tt * 2.5)
        else:
            # Wet piston squelch + sub thud
            f = np.linspace(480, 120, nt)
            res = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 8.0)
            wet = np.convolve(rng.normal(0, 1, nt), np.ones(18) / 18.0, mode="same") * np.exp(-tt * 6.5)
            return res * 0.55 + wet * 0.50

    # Immediate Frame-0 hook jolt (kills 0:00-0:02 scroll-by!)
    add_sfx(0.02, make_organic_jolt(cfg.get("hook_sfx", "crunch")), 0.78)
    add_sfx(0.02, make_vine_boom(0.65), 0.55)

    # 0:03.5 sensory jolt + cut transitions across escalation beats
    for idx in range(1, len(scene_starts)):
        t_cut = scene_starts[idx]
        add_sfx(max(0.0, t_cut - 0.12), make_whoosh(), 0.42)
        if idx == 1:
            # Vital 0:03.5-0:04.0 sensory reset cue
            add_sfx(t_cut, make_organic_jolt(cfg.get("hook_sfx", "crunch")), 0.60)
            add_sfx(t_cut, make_vine_boom(0.85), 0.72)
        elif idx in (3, 5):
            add_sfx(t_cut, make_vine_boom(0.90), 0.70)

    mix = vo * 1.12 + music + sfx
    pk = np.max(np.abs(mix))
    if pk > 0.94:
        mix = np.tanh(mix / 0.94) * 0.94
    return np.column_stack((mix, mix))


def build_ass_subtitles(timeline_words, ref_intervals, total_dur, cfg):
    chunks = []
    cur = []
    for w in timeline_words:
        if cur and (w["scene_id"] != cur[-1]["scene_id"] or len(cur) >= 3):
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
        f"Style: Default,Impact,92,&H00FFFFFF,&H0000E6FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,10,5,2,60,110,{cfg.get('sub_margin_v', 760)},1",
        "Style: RefTag,Arial,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,-1,0,0,0,100,100,2,0,3,14,0,8,50,50,140,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for rs, re_t, rcol, rtxt in ref_intervals:
        ass_lines.append(f"Dialogue: 1,{fmt_t(rs)},{fmt_t(re_t)},RefTag,,0,0,0,,{{\\c{rcol}}}{rtxt}")

    HL = {"alert": "&H003838FF&", "doc": "&H0000E6FF&", "panic": "&H003838FF&", "loop": "&H0000E6FF&"}

    for ci, ch in enumerate(chunks):
        mode = ch[0]["mode"]
        base_col = "&H00FFFFFF&"
        hl_col = HL.get(mode, "&H0000E6FF&")
        next_chunk_start = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else total_dur

        for j, active in enumerate(ch):
            t_s = active["start"]
            t_e = ch[j + 1]["start"] if j + 1 < len(ch) else min(next_chunk_start, active["end"] + 0.25)
            if mode == "loop" and j == len(ch) - 1:
                t_e = total_dur

            line_parts = []
            for k, other in enumerate(ch):
                wtxt = other["word"].upper()
                if k == j:
                    line_parts.append(f"{{\\c{hl_col}\\fscx112\\fscy112}}{wtxt}{{\\rDefault}}")
                elif k < j:
                    line_parts.append(f"{{\\c{base_col}}}{wtxt}")
                else:
                    line_parts.append(f"{{\\c&H80A0A0A0&}}{wtxt}")
            ass_lines.append(f"Dialogue: 2,{fmt_t(t_s)},{fmt_t(t_e)},Default,,0,0,0,,{' '.join(line_parts)}")

    return "\n".join(ass_lines)


async def synthesize_master_audio(short_key, lines, cfg, work_dir):
    """Synthesize trimmed WordBoundary EdgeTTS voiceover, varied music/SFX bed, and -14 LUFS master."""
    os.makedirs(work_dir, exist_ok=True)
    timeline_words = []
    audio_chunks = []
    scene_starts = []
    ref_intervals = []
    cursor = 0.03
    audio_chunks.append(np.zeros(int(cursor * SR), dtype=np.float32))

    voice = cfg.get("voice") or DEFAULT_VOICES[cfg["seed"] % len(DEFAULT_VOICES)]
    rate = cfg.get("voice_rate", "+8%")
    pitch = "+0Hz"

    for idx, (_spk, text, scene_id, mode, gap, rcol, rtxt) in enumerate(lines):
        mp3_p = os.path.join(work_dir, f"line_{idx:02d}.mp3")
        wav_p = os.path.join(work_dir, f"line_{idx:02d}.wav")

        print(f"  Synthesizing Line {idx} ({voice}): {text}")
        raw_words = await synth_line(text, voice, rate, pitch, mp3_p)
        await asyncio.sleep(0.08)

        subprocess.run(["ffmpeg", "-y", "-i", mp3_p, "-ar", str(SR), "-ac", "1", wav_p], check=True, capture_output=True)
        with wave.open(wav_p, "rb") as w:
            arr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

        nz = np.where(np.abs(arr) > 0.015)[0]
        if len(nz) > 0:
            trim_start = max(0, nz[0] - int(0.015 * SR))
            trim_end = min(len(arr), nz[-1] + int(0.04 * SR))
            arr = arr[trim_start:trim_end]
            shift_trim = trim_start / SR
        else:
            shift_trim = 0.0

        pk = np.max(np.abs(arr)) + 1e-6
        arr = (arr / pk) * 0.90

        seg_start = 0.0 if idx == 0 else cursor
        scene_starts.append(seg_start)

        for rw in raw_words:
            ws = max(cursor, cursor + rw["start"] - shift_trim)
            we = max(ws + 0.05, cursor + rw["end"] - shift_trim)
            timeline_words.append({
                "word": rw["word"],
                "start": round(ws, 3),
                "end": round(we, 3),
                "mode": mode,
                "scene_id": scene_id,
            })

        audio_chunks.append(arr)
        cursor += len(arr) / SR
        if gap > 0:
            audio_chunks.append(np.zeros(int(gap * SR), dtype=np.float32))
            cursor += gap

        if rtxt:
            ref_intervals.append((seg_start, cursor, rcol, rtxt))

    vo = np.concatenate(audio_chunks)
    total_dur = round(len(vo) / SR, 2)
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
    return timeline_words, scene_starts, ref_intervals, total_dur, norm_master


async def render_short(short_key):
    if short_key not in SHORT_CONFIGS:
        raise ValueError(f"Unknown short key: {short_key}. Available: {list(SHORT_CONFIGS.keys())}")

    cfg = SHORT_CONFIGS[short_key]
    vis_imgs = [v[0] for v in cfg["visuals"]]
    if not cfg.get("allow_legacy_repeats") and max(vis_imgs.count(x) for x in vis_imgs) > 2:
        raise ValueError(f"YPP Compliance Block [{short_key}]: static frame reused >2 times.")
    work_dir = os.path.join(OUT_ROOT, f"{short_key}_build")
    assets_dir = os.path.join(BASE_DIR, "assets", cfg["assets_subdir"])
    os.makedirs(work_dir, exist_ok=True)

    print(f"\n=== [{short_key}] STEP 1 & 2: VOICEOVER + AUDIO MIX (-14 LUFS) ===")
    timeline_words, scene_starts, ref_intervals, total_dur, norm_master = await synthesize_master_audio(
        short_key, cfg["lines"], cfg, work_dir
    )
    print(f"  Audio ready: {total_dur}s")

    print(f"=== [{short_key}] STEP 3: GENERATING SAFE-ZONE ASS SUBTITLES ===")
    ass_path = os.path.join(work_dir, "captions.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(build_ass_subtitles(timeline_words, ref_intervals, total_dur, cfg))

    print(f"=== [{short_key}] STEP 4: RENDERING CLIPS & MUXING ===")
    clip_specs = []
    for idx, (img_name, scene_id, motion) in enumerate(cfg["visuals"]):
        t_start = scene_starts[idx]
        t_end = scene_starts[idx + 1] if idx + 1 < len(cfg["visuals"]) else total_dur
        dur = max(0.5, round(t_end - t_start, 2))
        clip_specs.append((img_name, motion, dur))
    if cfg.get("loop_visual_tail") and clip_specs and clip_specs[-1][2] > 1.0:
        img_last, mot_last, d_last = clip_specs[-1]
        clip_specs[-1] = (img_last, mot_last, round(d_last - 0.50, 2))
        clip_specs.append((cfg["visuals"][0][0], "push", 0.50))

    clip_files = []
    for idx, (img_name, motion, dur) in enumerate(clip_specs):
        img_p = os.path.join(assets_dir, img_name)
        if not os.path.exists(img_p):
            raise FileNotFoundError(f"Missing visual asset: {img_p}")

        clip_p = os.path.join(work_dir, f"clip_{idx}.mp4")
        frames = int(dur * 30) + 2
        if motion == "hook_punch":
            # Rapid opening 4-frame scale punch-in + micro tremble to stop scroll immediately!
            zoom_expr = "min(1.00+0.18*min(1,on/4)+0.0008*on,1.26)"
            xy = "x='iw/2-(iw/zoom/2)+3*sin(on*1.8)*exp(-on/30)':y='ih/2-(ih/zoom/2)+3*cos(on*2.1)*exp(-on/30)'"
        elif motion == "punch4":
            zoom_expr = "min(1.00+0.18*min(1,on/4)+0.001*on,1.24)"
            xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        elif motion == "push":
            zoom_expr = "min(zoom+0.0022,1.22)"
            xy = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        elif motion == "shake":
            zoom_expr = "1.08+0.08*on/" + str(max(1, frames))
            xy = "x='iw/2-(iw/zoom/2)+6*sin(on*2.0)':y='ih/2-(ih/zoom/2)+4*cos(on*2.3)'"
        elif motion == "zoom":
            zoom_expr = "min(1.04+0.0024*on,1.24)"
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
    parser.add_argument("--short", required=True, help="Short key (fish_bone, qtip_ear, skin_tag, two_magnets, or 'all')")
    args = parser.parse_args()

    targets = [k for k in SHORT_CONFIGS if args.short == "all"] if args.short == "all" else [args.short]
    for k in targets:
        await render_short(k)


if __name__ == "__main__":
    asyncio.run(main())
