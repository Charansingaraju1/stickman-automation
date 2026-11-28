---
name: ffmpeg-render-and-qa
description: Executes 1080x1920 vertical rendering and strict ffprobe/visual Quality Inspector gates before any upload (absorbs ffmpeg-video-editor, video-quality-inspector, plus Reality Checker proof criteria). Use before accepting any rendered MP4.
---

# FFmpeg Render and QA Inspector

## Purpose
Ensure every rendered Short passes deterministic technical, visual, and editorial inspection (`1080x1920`, `9:16`, clear audio, zero unintended silence, zero distortion, safe captions) before entering `cloud_queue.json`.

## Activation Conditions
- After rendering any MP4 (`cloud_short_factory.py`, `short_builder.py`, `compile_longform.py`) or modifying Remotion TSX.

## Required Inputs
- Rendered MP4 path + optional thumbnail JPEG + expected target duration.

## Step-by-Step Workflow
1. Mux Remotion visual MP4 (`crf <= 22`, `yuv420p`) with `-14 LUFS` normalized AAC `192k` audio cleanly via FFmpeg `-shortest -movflags +faststart`.
2. Run `agents/studio_engine.py --qc <video.mp4>` which probes with `ffprobe` (`width==1080`, `height==1920`, `fps>=30`, audio stream present, duration in `[10, 59]`, silence detection check via `silencedetect`).
3. Extract verification sample frames (`0%`, `25%`, `60%`, `95%`) using `ffmpeg` when inspecting visually (`read_file` on PNG/JPG) — default verdict is **NEEDS WORK** until frames + metrics actually pass!
4. Emit structured QC report saved to `agents/out/qc_<id>.json`.

## Output Format
JSON QC report: `{passed, resolution, duration_s, fps, has_audio, max_silence_gap_s, errors[]}`.

## Validation Criteria
- `passed == True`, exact `1080x1920` (unless 16:9 `1280x720`/`1920x1080` compilation explicitly requested), `max_silence_gap_s <= 0.8s`.

## Failure Handling
- Reject failed renders immediately; do NOT append failed MP4s to `cloud_queue.json`.

## Security Restrictions
- Read/process local workspace media only; remove temporary render artifacts gracefully.

## Examples
- Running `python agents/studio_engine.py --qc videos/stickman_knuckle_cracking_viral.mp4` validates live MP4 specs directly from `ffprobe`.
