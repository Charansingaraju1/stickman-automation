import asyncio
import edge_tts
import os
import json
import subprocess
import wave
import shutil
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(BASE_DIR, "out", "ear_bug_build")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "ear_bug")

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

SR = 44100

LINES = [
    ("NARRATOR", "If an insect crawls inside your ear, your first instinct could permanently damage your hearing.", "1", "alert", 0.15),
    ("NARRATOR", "Most people immediately grab tweezers or a cotton swab to dig it out. But this is the worst thing you can do.", "2", "doc", 0.20),
    ("STICKMAN", "Wait, so using tweezers pushes it deeper?!", "3", "panic", 0.20),
    ("NARRATOR", "Yes! Poking blindly forces the insect inward, where sharp claws can easily puncture your eardrum.", "4", "alert", 0.20),
    ("NARRATOR", "Instead, doctors tilt your head and pour warm mineral oil to safely float it out.", "5", "doc", 0.20),
    ("NARRATOR", "So before you ever stick anything into your ear...", "6", "loop", 0.10),
]

async def synth_line(text, voice, rate, pitch, mp3_p, max_retries=4):
    clean = text.replace("?!", "!").replace("...", ",")
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

async def render():
    print("=== [CLOUD RENDER] STEP 1: SYNTHESIZING VOICE OVER ===")
    timeline_words = []
    audio_chunks = []
    cursor = 0.05
    audio_chunks.append(np.zeros(int(cursor * SR), dtype=np.float32))

    for idx, (spk, text, scene_id, mode, gap) in enumerate(LINES):
        mp3_p = os.path.join(WORK_DIR, f'line_{idx:02d}.mp3')
        wav_p = os.path.join(WORK_DIR, f'line_{idx:02d}.wav')

        voice = "en-US-GuyNeural" if spk == "STICKMAN" else "en-US-ChristopherNeural"
        rate = "+12%" if spk == "STICKMAN" else "+8%"
        pitch = "+10Hz" if spk == "STICKMAN" else "+0Hz"

        print(f"  Synthesizing [{spk}] Line {idx}: {text}")
        raw_words = await synth_line(text, voice, rate, pitch, mp3_p)
        await asyncio.sleep(0.1)

        subprocess.run(['ffmpeg', '-y', '-i', mp3_p, '-ar', str(SR), '-ac', '1', wav_p], check=True, capture_output=True)
        with wave.open(wav_p, 'rb') as w:
            arr = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

        thresh = 0.015
        nz = np.where(np.abs(arr) > thresh)[0]
        if len(nz) > 0:
            trim_start = max(0, nz[0] - int(0.02 * SR))
            trim_end = min(len(arr), nz[-1] + int(0.05 * SR))
            arr = arr[trim_start:trim_end]
            shift_trim = trim_start / SR
        else:
            shift_trim = 0.0

        pk = np.max(np.abs(arr)) + 1e-6
        arr = (arr / pk) * (0.92 if spk == "STICKMAN" else 0.88)

        seg_start = cursor
        for rw in raw_words:
            ws = max(seg_start, seg_start + rw["start"] - shift_trim)
            we = max(ws + 0.05, seg_start + rw["end"] - shift_trim)
            timeline_words.append({
                "word": rw["word"],
                "start": round(ws, 3),
                "end": round(we, 3),
                "speaker": spk,
                "mode": mode,
                "scene_id": scene_id
            })

        audio_chunks.append(arr)
        cursor += len(arr) / SR
        if gap > 0:
            audio_chunks.append(np.zeros(int(gap * SR), dtype=np.float32))
            cursor += gap

    vo = np.concatenate(audio_chunks)
    TOTAL_DUR = round(len(vo) / SR, 2)
    N = len(vo)
    print(f"Voiceover track ready ({TOTAL_DUR}s).")

    print("=== [CLOUD RENDER] STEP 2: SFX & DYNAMIC AUDIO MIX ===")
    t_full = np.linspace(0, TOTAL_DUR, N, endpoint=False)
    rng = np.random.default_rng(42)

    beat_hz = 120.0 / 60.0
    pulse = np.exp(-((t_full * beat_hz) % 1.0) * 7.0)
    dark_bed = (
        0.45 * np.sin(2 * np.pi * 55.00 * t_full) +
        0.30 * np.sin(2 * np.pi * 82.41 * t_full) +
        0.20 * np.sin(2 * np.pi * 110.00 * t_full) * pulse
    )
    music = dark_bed * 0.12

    sfx = np.zeros(N, dtype=np.float32)
    def add_sfx(start_s, arr, gain=1.0):
        i0 = int(start_s * SR)
        i1 = min(N, i0 + len(arr))
        if i1 > i0:
            sfx[i0:i1] += arr[:i1 - i0] * gain

    # Skittering audio hook
    skit_dur = 0.85
    nt_skit = int(SR * skit_dur)
    tt_skit = np.linspace(0, skit_dur, nt_skit)
    skit_audio = rng.normal(0, 1, nt_skit) * (np.sin(2 * np.pi * 28 * tt_skit) > 0).astype(np.float32) * np.exp(-tt_skit * 1.5) * 0.35
    add_sfx(0.05, skit_audio, 0.85)

    def make_vine_boom(dur=1.1):
        nt = int(SR * dur)
        tt = np.linspace(0, dur, nt)
        f = np.linspace(85, 25, nt)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.8)
        hit = np.sin(2 * np.pi * 160 * tt) * np.exp(-tt * 14.0)
        return sub * 0.85 + hit * 0.35

    add_sfx(3.9, make_vine_boom(1.0), 0.70)
    add_sfx(12.2, make_vine_boom(1.1), 0.75)
    add_sfx(24.8, make_vine_boom(1.2), 0.60)

    mix = vo * 1.10 + music + sfx
    pk = np.max(np.abs(mix))
    if pk > 0.94:
        mix = np.tanh(mix / 0.94) * 0.94
    stereo = np.column_stack((mix, mix))
    raw_master = os.path.join(WORK_DIR, 'master_raw.wav')
    with wave.open(raw_master, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1.0, 1.0) * 32767.0).astype(np.int16).tobytes())

    norm_master = os.path.join(WORK_DIR, 'master_norm.wav')
    subprocess.run(['ffmpeg', '-y', '-i', raw_master, '-af', 'loudnorm=I=-14:TP=-1.2:LRA=7', '-ar', '44100', '-ac', '2', norm_master], check=True, capture_output=True)

    print("=== [CLOUD RENDER] STEP 3: KINETIC ASS SUBTITLES ===")
    def fmt_t(sec):
        sec = max(0.0, sec)
        h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60)
        cs = min(99, int(round((sec - int(sec)) * 100)))
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    chunks = []
    cur = []
    for w in timeline_words:
        if cur and (w["scene_id"] != cur[-1]["scene_id"] or w["speaker"] != cur[-1]["speaker"] or len(cur) >= 4):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)

    ass_lines = [
        "[Script Info]",
        "Title: StickNation 3D Ear Bug Cloud Render",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Impact,88,&H00FFFFFF,&H0000E6FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,9,4,8,45,45,200,1",
        "Style: StickmanTalk,Impact,96,&H0000E6FF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,10,5,8,45,45,190,1",
        "Style: RefTag,Arial,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,-1,0,0,0,100,100,2,0,3,14,0,2,50,50,310,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 1,0:00:00.05,0:00:03.80,RefTag,,0,0,0,,{{\\c&H003838FF&}}DANGER: FOREIGN OBJECT IN CANAL",
        f"Dialogue: 1,0:00:04.00,0:00:08.80,RefTag,,0,0,0,,{{\\c&H0000FFF0&}}ANATOMY: AUDITORY CANAL NARROWING",
        f"Dialogue: 1,0:00:09.00,0:00:12.00,RefTag,,0,0,0,,{{\\c&H0000E6FF&}}HAZARD: BLIND TWEEZER INSERTION",
        f"Dialogue: 1,0:00:12.50,0:00:18.00,RefTag,,0,0,0,,{{\\c&H003838FF&}}COMPLICATION: TYMPANIC PERFORATION",
        f"Dialogue: 1,0:00:18.50,0:00:24.00,RefTag,,0,0,0,,{{\\c&H0000E6FF&}}TREATMENT: WARM MINERAL OIL SUFFOCATION",
    ]

    HL = {"alert": "&H003838FF&", "doc": "&H0000E6FF&", "panic": "&H003838FF&", "loop": "&H0000E6FF&"}

    for ci, ch in enumerate(chunks):
        spk = ch[0]["speaker"]
        mode = ch[0]["mode"]
        style = "StickmanTalk" if spk == "STICKMAN" else "Default"
        base_col = "&H00FFFFFF&"
        hl_col = HL.get(mode, "&H0000E6FF&")
        next_chunk_start = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else TOTAL_DUR

        for j, active in enumerate(ch):
            t_s = active["start"]
            t_e = ch[j + 1]["start"] if j + 1 < len(ch) else min(next_chunk_start, active["end"] + 0.35)
            if mode == "loop" and j == len(ch) - 1:
                t_e = TOTAL_DUR

            line_parts = []
            for k, other in enumerate(ch):
                wtxt = other["word"]
                if k == j:
                    line_parts.append(f"{{\\c{hl_col}\\fscx112\\fscy112}}{wtxt.upper()}{{\\r{style}}}")
                elif k < j:
                    line_parts.append(f"{{\\c{base_col}}}{wtxt}")
                else:
                    line_parts.append(f"{{\\c&H80A0A0A0&}}{wtxt}")
            ass_lines.append(f"Dialogue: 2,{fmt_t(t_s)},{fmt_t(t_e)},{style},,0,0,0,,{' '.join(line_parts)}")

    ass_path = os.path.join(WORK_DIR, 'captions.ass')
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(ass_lines))

    print("=== [CLOUD RENDER] STEP 4: MUXING VIDEO ===")
    img_tunnel = os.path.join(ASSETS_DIR, "tunnel.jpg")
    img_tweezer = os.path.join(ASSETS_DIR, "tweezer.jpg")
    img_clutch = os.path.join(ASSETS_DIR, "clutch.jpg")

    cuts = [
        (img_tunnel, 0.00, 3.90, "push"),
        (img_tweezer, 3.90, 8.80, "pan"),
        (img_clutch, 8.80, 12.20, "zoom"),
        (img_tunnel, 12.20, 17.50, "push"),
        (img_tweezer, 17.50, 23.80, "pan"),
        (img_tunnel, 23.80, TOTAL_DUR, "zoom")
    ]

    clip_files = []
    for idx, (img_p, t_start, t_end, motion) in enumerate(cuts):
        dur = round(t_end - t_start, 2)
        clip_p = os.path.join(WORK_DIR, f"clip_{idx}.mp4")
        zoom_expr = "min(zoom+0.0018,1.18)" if motion == "push" else "max(1.15-0.0015*on,1.0)"
        vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='{zoom_expr}':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", img_p,
            "-vf", vf, "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            clip_p
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        clip_files.append(clip_p)

    concat_txt = os.path.join(WORK_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        for cp in clip_files:
            f.write(f"file '{cp.replace(os.sep, '/')}'\n")

    raw_video = os.path.join(WORK_DIR, "video_raw.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-c", "copy", raw_video
    ], check=True, capture_output=True)

    ass_esc = ass_path.replace("\\", "/").replace(":", "\\:")
    final_mp4 = os.path.join(VIDEOS_DIR, "stickman_ear_bug_viral.mp4")

    cmd_mux = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", norm_master,
        "-vf", f"ass='{ass_esc}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        final_mp4
    ]
    subprocess.run(cmd_mux, check=True, capture_output=True)

    dur_out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", final_mp4
    ]).decode().strip()

    print(f"SUCCESS: Rendered {final_mp4} ({dur_out}s)")
    return final_mp4

if __name__ == "__main__":
    asyncio.run(render())
