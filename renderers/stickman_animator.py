"""2.5D animated clay Stickman + live anatomical HUD cutaway renderer (30fps NVENC / x264)."""

from __future__ import annotations

import math
import pathlib
import subprocess
import wave
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in (
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if pathlib.Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def extract_lipsync_from_wav(wav_path: str | pathlib.Path, word_timings: list[dict[str, Any]], fps: int = 30) -> list[dict[str, Any]]:
    """Computes per-frame audio RMS openness & vowel viseme (closed/mbp/round/wide/half)."""
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        raw = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        raw = raw.reshape(-1, ch).mean(axis=1)

    total_dur = len(raw) / sr
    n_frames = max(int(math.ceil(total_dur * fps)), 1)
    spf = max(int(sr / fps), 1)

    w_idx = 0
    track: list[dict[str, Any]] = []
    for f in range(n_frames):
        t = f / fps
        i0 = f * spf
        chunk = raw[i0 : i0 + spf]
        rms = float(np.sqrt(np.mean(chunk * chunk))) if len(chunk) else 0.0
        openness = min(1.0, rms * 6.5)

        while w_idx + 1 < len(word_timings) and word_timings[w_idx]["end"] < t:
            w_idx += 1
        word_txt = ""
        if w_idx < len(word_timings) and word_timings[w_idx]["start"] <= t <= word_timings[w_idx]["end"]:
            word_txt = word_timings[w_idx]["word"].lower()

        if openness < 0.08:
            viseme = "closed"
        elif any(c in word_txt for c in ("m", "b", "p")) and openness < 0.35:
            viseme = "mbp"
        elif any(c in word_txt for c in ("o", "u", "w")):
            viseme = "round"
        elif openness > 0.52 or any(c in word_txt for c in ("a", "e", "i")):
            viseme = "wide"
        else:
            viseme = "half"

        track.append({"openness": openness, "viseme": viseme})
    return track


def _build_medical_backdrop() -> Image.Image:
    """Pre-renders deep charcoal (#12131A) clinical lab backdrop with volumetric spotlight."""
    bg = Image.new("RGBA", (W, H), (14, 16, 24, 255))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    for gx in range(90, W, 180):
        d.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 7), width=2)
    for gy in range(120, H, 180):
        d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 7), width=2)

    d.polygon([(W // 2 - 140, 0), (W // 2 + 140, 0), (W + 220, H), (-220, H)], fill=(70, 120, 185, 22))
    d.ellipse([120, 220, 960, 1360], fill=(45, 75, 130, 26))
    ov = ov.filter(ImageFilter.GaussianBlur(14))

    comp = Image.alpha_composite(bg, ov)
    d2 = ImageDraw.Draw(comp)
    d2.rounded_rectangle([38, 44, 385, 90], radius=12, fill=(20, 24, 34, 235), outline=(65, 82, 110, 220), width=2)
    d2.text((211, 67), "STICK NATION • 3D LAB", fill=(210, 224, 244, 255), font=_load_font(22), anchor="mm")
    return comp.convert("RGB")


def _draw_capsule(d: ImageDraw.ImageDraw, pts: list[tuple[int, int]], w: int, fill: tuple[int, int, int]) -> None:
    """Draws smooth round-capped clay limb segments with circular joint fillets."""
    r = max(2, w // 2)
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=fill, width=w)
    for px, py in pts:
        d.ellipse([px - r, py - r, px + r, py + r], fill=fill)


def _draw_clay_limb(d: ImageDraw.ImageDraw, pts: list[tuple[int, int]], w: int, base=(244, 247, 252), shade=(168, 178, 194)) -> None:
    _draw_capsule(d, [(x + 4, y + 4) for x, y in pts], w + 6, shade)
    _draw_capsule(d, pts, w, base)


def _draw_stickman_character(
    d: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    scale: float,
    t: float,
    lip: dict[str, Any],
    scene_idx: int,
    short_key: str,
) -> tuple[int, int]:
    """Draws 2.5D sculpted clay white Stickman with live gestures, blinks, lip-sync & cutaway anchor."""
    def S(v: float) -> int:
        return int(round(v * scale))

    openness = lip.get("openness", 0.0)
    viseme = lip.get("viseme", "closed")
    is_danger = scene_idx in (0, 2, 3)
    is_safe = scene_idx == 4

    breathe_y = int(S(5) * math.sin(t * 2.4))
    shiver_x = int(S(5) * math.sin(t * 16.0)) if scene_idx == 3 else int(S(3) * math.sin(t * 2.0))
    bx = cx + shiver_x
    by = cy + breathe_y

    clay = (244, 247, 252)
    clay_sh = (165, 175, 192)
    clay_hi = (255, 255, 255)

    torso_top = by + S(122)
    hip_y = torso_top + S(235)

    # Smooth rounded clay legs + rounded feet
    l_foot = (bx - S(72), hip_y + S(235))
    r_foot = (bx + S(72), hip_y + S(235))
    _draw_clay_limb(d, [(bx - S(38), hip_y - S(8)), (bx - S(58), hip_y + S(115)), l_foot], S(42), clay, clay_sh)
    _draw_clay_limb(d, [(bx + S(38), hip_y - S(8)), (bx + S(58), hip_y + S(115)), r_foot], S(42), clay, clay_sh)
    for fx, fy in (l_foot, r_foot):
        d.ellipse([fx - S(34), fy - S(16), fx + S(34), fy + S(22)], fill=clay_sh)
        d.ellipse([fx - S(32), fy - S(18), fx + S(30), fy + S(18)], fill=clay)

    # Sculpted capsule torso with subtle rim highlight
    d.rounded_rectangle([bx - S(86), torso_top - S(10), bx + S(90), hip_y + S(22)], radius=S(74), fill=clay_sh)
    d.rounded_rectangle([bx - S(84), torso_top - S(10), bx + S(80), hip_y + S(16)], radius=S(70), fill=clay)
    d.arc([bx - S(72), torso_top + S(6), bx + S(68), torso_top + S(96)], 190, 325, fill=clay_hi, width=max(3, S(5)))

    # Smooth tapered neck
    _draw_clay_limb(d, [(bx, by + S(72)), (bx, torso_top + S(12))], S(42), clay, clay_sh)

    # Head with subtle tilt synced to speech
    head_tilt = int(S(4) * math.sin(t * 3.1))
    hx = bx + head_tilt
    hy = by - S(16)
    r_head = S(124)
    d.ellipse([hx - r_head - S(5), hy - r_head, hx + r_head + S(7), hy + r_head + S(8)], fill=clay_sh)
    d.ellipse([hx - r_head, hy - r_head, hx + r_head - S(4), hy + r_head - S(4)], fill=clay)
    d.arc([hx - r_head + S(18), hy - r_head + S(14), hx + S(20), hy - S(8)], 190, 285, fill=clay_hi, width=max(4, S(6)))

    # Eyes + periodic blinks + emotional squash
    is_blinking = (t % 3.2) > 3.07
    eye_y = hy - S(22)
    if short_key == "superglue_eyes" and scene_idx in (1, 2, 3):
        for side in (-1, 1):
            ex = hx + side * S(44)
            if side == 1:
                d.line([(ex - S(24), eye_y - S(8)), (ex + S(20), eye_y + S(8))], fill=(255, 50, 68), width=max(6, S(9)))
                d.line([(ex - S(24), eye_y + S(8)), (ex + S(20), eye_y - S(8))], fill=(30, 34, 44), width=max(4, S(7)))
            else:
                d.ellipse([ex - S(22), eye_y - S(20), ex + S(22), eye_y + S(20)], fill=(255, 255, 255), outline=(28, 32, 42), width=3)
                d.ellipse([ex - S(9) + S(5), eye_y - S(9), ex + S(9) + S(5), eye_y + S(9)], fill=(22, 26, 36))
    else:
        for side in (-1, 1):
            ex = hx + side * S(44)
            if is_blinking or (is_danger and (t % 1.4 > 1.25)):
                d.line([(ex - S(22), eye_y), (ex + S(22), eye_y)], fill=(30, 34, 46), width=max(5, S(7)))
            else:
                d.ellipse([ex - S(22), eye_y - S(22), ex + S(22), eye_y + S(22)], fill=(255, 255, 255), outline=(28, 32, 42), width=max(3, S(4)))
                look_dx = int(S(6) * math.sin(t * 2.2))
                d.ellipse([ex - S(9) + look_dx, eye_y - S(9), ex + S(9) + look_dx, eye_y + S(9)], fill=(20, 24, 34))
                d.ellipse([ex - S(4) + look_dx, eye_y - S(4), ex + S(2) + look_dx, eye_y + S(1)], fill=(255, 255, 255))

    # Expressive eyebrows
    for side in (-1, 1):
        ex = hx + side * S(44)
        brow_ang = -S(11) * side if (is_danger or scene_idx == 1) else S(7) * side
        by_pos = eye_y - S(34) - (S(5) if is_safe else 0)
        d.line([(ex - S(24), by_pos - brow_ang), (ex + S(24), by_pos + brow_ang)], fill=(30, 34, 46), width=max(5, S(8)))

    # Audio-synced Lip-Sync Mouth
    my = hy + S(48)
    if viseme == "closed":
        arc_start, arc_end = (10, 170) if is_safe else (195, 345)
        d.arc([hx - S(32), my - S(10), hx + S(32), my + S(14)], arc_start, arc_end, fill=(32, 36, 48), width=max(5, S(7)))
    elif viseme == "mbp":
        d.line([(hx - S(28), my), (hx + S(28), my)], fill=(32, 36, 48), width=max(5, S(7)))
    elif viseme == "round":
        d.ellipse([hx - S(16), my - S(14), hx + S(16), my + S(18)], fill=(75, 22, 32), outline=(28, 32, 42), width=3)
    elif viseme == "wide":
        d.rounded_rectangle([hx - S(34), my - S(14), hx + S(34), my + S(22)], radius=S(11), fill=(78, 22, 32), outline=(28, 32, 42), width=3)
        d.rectangle([hx - S(24), my - S(11), hx + S(24), my - S(2)], fill=(248, 248, 252))
    else:
        d.rounded_rectangle([hx - S(26), my - S(8), hx + S(26), my + S(12)], radius=S(7), fill=(78, 22, 32), outline=(28, 32, 42), width=3)

    # Articulated Arms (kept clear of HUD lens to avoid clipping)
    if short_key == "splinter_tweezers":
        finger_x, finger_y = bx + S(140), torso_top + S(75) + int(S(7) * math.sin(t * 5.0))
        _draw_clay_limb(d, [(bx + S(66), torso_top + S(38)), (bx + S(108), torso_top + S(110)), (finger_x, finger_y)], S(34), clay, clay_sh)
        d.ellipse([finger_x - S(21), finger_y - S(21), finger_x + S(21), finger_y + S(21)], fill=clay, outline=clay_sh, width=3)

        # Left arm reaches across holding tweezers visibly!
        tw_x = finger_x - S(48) + int(S(10) * math.sin(t * 6.5))
        tw_y = finger_y - S(62) + int(S(8) * math.cos(t * 6.5))
        _draw_clay_limb(d, [(bx - S(66), torso_top + S(38)), (bx - S(95), torso_top + S(130)), (tw_x, tw_y)], S(34), clay, clay_sh)
        d.ellipse([tw_x - S(20), tw_y - S(20), tw_x + S(20), tw_y + S(20)], fill=clay, outline=clay_sh, width=3)
        d.line([(tw_x + S(6), tw_y - S(10)), (finger_x - S(8), finger_y - S(6))], fill=(215, 224, 236), width=max(4, S(6)))
        d.line([(tw_x + S(2), tw_y + S(2)), (finger_x - S(10), finger_y + S(4))], fill=(155, 166, 182), width=max(4, S(6)))

        pulse_r = S(22) + int(S(9) * abs(math.sin(t * 7.0)))
        ring_col = (0, 235, 210) if is_safe else (255, 42, 62)
        d.ellipse([finger_x - pulse_r, finger_y - pulse_r, finger_x + pulse_r, finger_y + pulse_r], outline=ring_col, width=max(4, S(6)))
        return finger_x, finger_y
    else:
        target_x, target_y = hx + S(44), eye_y
        hand_y = eye_y + S(72) - int(S(16) * abs(math.sin(t * 5.0)))
        _draw_clay_limb(d, [(bx + S(66), torso_top + S(38)), (bx + S(135), torso_top + S(10)), (target_x + S(28), hand_y)], S(34), clay, clay_sh)
        d.ellipse([target_x + S(10), hand_y - S(18), target_x + S(46), hand_y + S(18)], fill=clay, outline=clay_sh, width=3)

        lhand_x, lhand_y = bx - S(128), torso_top + S(125) + int(S(14) * math.sin(t * 3.5))
        _draw_clay_limb(d, [(bx - S(66), torso_top + S(38)), (bx - S(118), torso_top + S(85)), (lhand_x, lhand_y)], S(34), clay, clay_sh)
        d.ellipse([lhand_x - S(20), lhand_y - S(20), lhand_x + S(20), lhand_y + S(20)], fill=clay, outline=clay_sh, width=3)

        ring_col = (0, 235, 210) if is_safe else (255, 42, 62)
        pulse_r = S(30) + int(S(8) * abs(math.sin(t * 7.0)))
        d.ellipse([target_x - pulse_r, target_y - pulse_r, target_x + pulse_r, target_y + pulse_r], outline=ring_col, width=max(4, S(6)))
        return target_x, target_y


def _draw_cutaway_lens(
    frame: Image.Image,
    d: ImageDraw.ImageDraw,
    t: float,
    scene_idx: int,
    short_key: str,
    anchor: tuple[int, int],
    lx: int,
    ly: int,
    radius: int,
) -> None:
    """Renders animated 30fps internal anatomical cross-section inside a circular HUD lens."""
    is_safe = scene_idx == 4
    ring_rgb = (0, 230, 210) if is_safe else (255, 44, 68)
    glow_rgb = (18, 175, 165) if is_safe else (255, 185, 0)

    d.line([anchor, (lx, ly)], fill=ring_rgb, width=6)
    d.ellipse([lx - radius - 14, ly - radius - 14, lx + radius + 14, ly + radius + 14], fill=(14, 16, 22), outline=glow_rgb, width=9)
    d.ellipse([lx - radius - 4, ly - radius - 4, lx + radius + 4, ly + radius + 4], outline=ring_rgb, width=7)

    sz = radius * 2
    sub = Image.new("RGBA", (sz, sz), (24, 18, 26, 255))
    sd = ImageDraw.Draw(sub)
    cx, cy = radius, radius

    if short_key == "splinter_tweezers":
        sd.rectangle([0, 0, sz, int(sz * 0.30)], fill=(18, 22, 32, 255))
        sd.rectangle([0, int(sz * 0.30), sz, int(sz * 0.42)], fill=(235, 178, 146, 255))
        sd.rectangle([0, int(sz * 0.42), sz, sz], fill=(208, 92, 112, 255))

        cap_pulse = int(6 * abs(math.sin(t * 7.5)))
        sd.line([(0, int(sz * 0.78)), (int(sz * 0.48), int(sz * 0.72)), (sz, int(sz * 0.80))], fill=(185, 18, 36, 255), width=26 + cap_pulse)
        sd.line([(0, int(sz * 0.78)), (int(sz * 0.48), int(sz * 0.72)), (sz, int(sz * 0.80))], fill=(255, 65, 82, 255), width=11)

        if scene_idx in (0, 1):
            squeeze = abs(math.sin(t * 4.5))
            depth = int(squeeze * 34)
            sx0, sy0 = cx - 42, int(sz * 0.24) + depth
            sx1, sy1 = cx + 48, int(sz * 0.64) + depth
            sd.polygon([(sx0, sy0), (sx0 + 24, sy0 - 12), (sx1 + 10, sy1), (sx1 - 6, sy1 + 10)], fill=(138, 86, 44, 255))
            jaw_gap = 12 + int((1.0 - squeeze) * 26)
            sd.line([(cx - 105, 0), (sx0 + 10, sy0 - jaw_gap)], fill=(215, 222, 234, 255), width=15)
            sd.line([(cx - 35, 0), (sx0 + 22, sy0 + jaw_gap)], fill=(170, 178, 192, 255), width=15)
        elif scene_idx in (2, 3):
            ab_r = int(80 + 22 * abs(math.sin(t * 6.5))) if scene_idx == 3 else 52
            sd.ellipse([cx - ab_r, int(sz * 0.44), cx + ab_r, int(sz * 0.44) + ab_r * 1.25], fill=(255, 48, 48, 170))
            for dx, dy in [(-18, 38), (16, 64), (-6, 95)]:
                sd.polygon([(cx + dx, int(sz * 0.46) + dy), (cx + dx + 34, int(sz * 0.56) + dy), (cx + dx + 10, int(sz * 0.60) + dy)], fill=(112, 64, 30, 255))
            for bi in range(8):
                ang = t * 2.4 + bi * 0.78
                bx_b = int(cx + 15 + (50 + 32 * math.sin(t * 3 + bi)) * math.cos(ang))
                by_b = int(sz * 0.58 + (32 + 22 * math.cos(t * 2.5 + bi)) * math.sin(ang))
                sd.ellipse([bx_b - 10, by_b - 10, bx_b + 10, by_b + 10], fill=(175, 255, 55, 235), outline=(45, 95, 20, 255), width=2)
        elif scene_idx == 4:
            lift = int(80 * abs(math.sin(t * 1.8)))
            sx0, sy0 = cx - 38, int(sz * 0.24) - lift
            sx1, sy1 = cx + 44, int(sz * 0.58) - lift
            sd.polygon([(sx0, sy0), (sx0 + 22, sy0 - 11), (sx1 + 8, sy1), (sx1 - 6, sy1 + 9)], fill=(146, 94, 48, 255))
            sd.line([(cx + 140, 10), (sx0 + 32, sy0 + 16)], fill=(0, 235, 220, 255), width=11)
        else:
            sd.polygon([(cx - 42, int(sz * 0.26)), (cx - 16, int(sz * 0.14)), (cx + 50, int(sz * 0.62)), (cx + 38, int(sz * 0.72))], fill=(138, 86, 44, 255))
    else:
        # Crisp recognizable FRONTAL HUMAN EYE cutaway: skin around socket -> almond sclera -> iris -> pupil -> Animated Eyelids + Glue!
        sd.rectangle([0, 0, sz, sz], fill=(238, 178, 158, 255))
        # Eye socket shading
        sd.ellipse([cx - int(radius * 0.88), cy - int(radius * 0.58), cx + int(radius * 0.88), cy + int(radius * 0.58)], fill=(215, 130, 128, 255))

        # White eyeball almond + blue iris + black pupil
        eye_open = 0.92 if scene_idx == 0 else (0.78 if scene_idx == 4 else 0.26)
        eh = int(radius * 0.44 * eye_open)
        sd.ellipse([cx - int(radius * 0.78), cy - max(28, eh), cx + int(radius * 0.78), cy + max(28, eh)], fill=(250, 252, 255, 255), outline=(145, 50, 60, 255), width=6)

        # Irritated crimson veins on sclera in trauma beats
        if scene_idx in (1, 2, 3):
            for vx, vy in [(-140, -15), (-110, 18), (105, -18), (135, 12)]:
                sd.line([(cx + vx, cy + vy), (cx + vx // 2, cy)], fill=(255, 42, 62, 220), width=4)

        iris_r = int(radius * 0.30)
        sd.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=(42, 126, 212, 255), outline=(24, 72, 132, 255), width=5)
        pup_r = int(radius * 0.13)
        sd.ellipse([cx - pup_r, cy - pup_r, cx + pup_r, cy + pup_r], fill=(16, 20, 28, 255))
        sd.ellipse([cx - pup_r + 12, cy - pup_r + 8, cx - pup_r + 32, cy - pup_r + 28], fill=(255, 255, 255, 230))

        # Eyelid skin flaps covering top & bottom of eyeball according to eye_open
        sd.chord([cx - sz, cy - sz, cx + sz, cy - eh + 24], 0, 180, fill=(238, 178, 158, 255))
        sd.rectangle([0, 0, sz, max(10, cy - eh)], fill=(238, 178, 158, 255))
        sd.rectangle([0, min(sz - 10, cy + eh), sz, sz], fill=(238, 178, 158, 255))

        # Upper & lower eyelashes
        for lx_off in range(-int(radius * 0.65), int(radius * 0.66), 28):
            sd.line([(cx + lx_off, cy - eh), (cx + lx_off + lx_off // 12, cy - eh - 22)], fill=(26, 22, 24, 255), width=5)
            sd.line([(cx + lx_off, cy + eh), (cx + lx_off + lx_off // 12, cy + eh + 18)], fill=(26, 22, 24, 255), width=4)

        if scene_idx == 0:
            # Bottle dropper nozzle + falling glowing superglue drop hitting lash rim
            drop_y = int((t * 140) % max(40, cy - eh)) + 15
            sd.polygon([(cx - 18, 0), (cx + 18, 0), (cx + 6, 48), (cx - 6, 48)], fill=(225, 232, 242, 255))
            sd.ellipse([cx - 16, drop_y - 20, cx + 16, drop_y + 20], fill=(140, 235, 255, 230), outline=(255, 255, 255, 255), width=3)
        elif scene_idx in (1, 2, 3):
            # Hardened glowing cyan superglue polymer bond locking upper & lower lashes + tug tears!
            tug = int(12 * abs(math.sin(t * 10.0))) if scene_idx in (2, 3) else 0
            for gx in range(-int(radius * 0.55), int(radius * 0.56), 34):
                sd.polygon(
                    [(cx + gx - 10, cy - eh - tug), (cx + gx + 10, cy - eh - tug), (cx + gx + 14, cy + eh), (cx + gx - 14, cy + eh)],
                    fill=(155, 242, 255, 215),
                )
            if scene_idx in (2, 3):
                # Red abrasion scratches across cornea when pried
                for sc in (-24, 0, 24):
                    sd.line([(cx - 48, cy + sc - 10), (cx + 48, cy + sc + 10)], fill=(255, 38, 56, 235), width=6)
        elif scene_idx == 4:
            # Emerald/cyan ophthalmic ointment soothing coat dissolving glue seal
            sd.rounded_rectangle([cx - 145, cy - eh - 14, cx + 145, cy - eh + 16], radius=14, fill=(0, 238, 215, 190))

    mask = Image.new("L", (sz, sz), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, sz, sz), fill=255)
    frame.paste(sub.convert("RGB"), (lx - radius, ly - radius), mask)


def render_animated_short(
    short_key: str,
    duration: float,
    lip_track: list[dict[str, Any]],
    scene_starts: list[float],
    out_raw_mp4: str | pathlib.Path,
    use_nvenc: bool = True,
    fps: int = 30,
) -> pathlib.Path:
    """Streams live 30fps Stickman + animated anatomical cutaway frames directly to FFmpeg."""
    out_p = pathlib.Path(out_raw_mp4)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    backdrop = _build_medical_backdrop()

    def get_scene_idx(t: float) -> int:
        idx = 0
        for i, st in enumerate(scene_starts):
            if t >= st:
                idx = i
        return idx

    enc_args = (
        ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "20"]
        if use_nvenc
        else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19"]
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "pipe:0",
        *enc_args, "-pix_fmt", "yuv420p", "-r", str(fps), str(out_p),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    total_frames = max(int(math.ceil(duration * fps)), fps)

    try:
        for f in range(total_frames):
            t = f / fps
            lip = lip_track[f] if f < len(lip_track) else {"openness": 0.0, "viseme": "closed"}
            s_idx = get_scene_idx(t)

            if f < 36:
                char_scale = 0.88 + 0.10 * (f / 36.0)
            elif s_idx in (2, 3):
                char_scale = 0.94 + 0.03 * math.sin(t * 2.2)
            else:
                char_scale = 0.96

            frame = backdrop.copy()
            d = ImageDraw.Draw(frame)

            # Stickman in upper-mid left; cutaway lens upper-mid right; leaves y=1140..1360 clear for captions!
            anchor = _draw_stickman_character(d, 290, 560, char_scale, t, lip, s_idx, short_key)
            _draw_cutaway_lens(frame, d, t, s_idx, short_key, anchor, 765, 650, 232)

            if s_idx in (0, 3):
                d.rectangle([0, 0, W, 10], fill=(255, 42, 68))

            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
    except Exception:
        proc.kill()
        raise

    _, stderr = proc.communicate(timeout=180)
    if proc.returncode != 0:
        if use_nvenc:
            return render_animated_short(short_key, duration, lip_track, scene_starts, out_p, use_nvenc=False, fps=fps)
        raise RuntimeError(f"Animated render failed: {stderr.decode('utf-8', errors='ignore')[-400:]}")
    return out_p


def export_hybrid_thumbnail(short_key: str, top_text: str, out_jpg: str | pathlib.Path) -> pathlib.Path:
    """Renders crisp Integrated Hybrid 9:16 thumbnail (white clay Stickman + HUD cutaway + top headline)."""
    backdrop = _build_medical_backdrop()
    frame = backdrop.copy()
    d = ImageDraw.Draw(frame)

    anchor = _draw_stickman_character(d, 285, 760, 0.98, 1.2, {"openness": 0.55, "viseme": "wide"}, 3, short_key)
    _draw_cutaway_lens(frame, d, 1.2, 3, short_key, anchor, 760, 860, 250)

    font_big = _load_font(124)
    words = top_text.split()
    lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [top_text]
    y_cursor = 185
    for idx, line_txt in enumerate(lines):
        col = (255, 255, 255) if idx == 0 else (255, 230, 0)
        d.text((W // 2, y_cursor), line_txt, font=font_big, fill=col, stroke_width=14, stroke_fill=(0, 0, 0), anchor="mm")
        y_cursor += 132

    out_p = pathlib.Path(out_jpg)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    frame.convert("RGB").save(out_p, "JPEG", quality=94)
    return out_p
