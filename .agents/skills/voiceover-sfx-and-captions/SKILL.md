---
name: voiceover-sfx-and-captions
description: Generates natural American English narration, synced word-level timestamps, -14 LUFS sound design, and safe-zone captions (absorbs narration-generator, voiceover-timing-controller, sound-design-engineer, subtitle-generator). Use whenever synthesizing audio or captions for any Short.
---

# Voiceover, SFX, and Captions

## Purpose
Deliver crisp natural US English narration, expressive cadence, impactful sound effects, and high-contrast word-by-word captions cleanly inside vertical Shorts safe zones (`y=430–650px` above bottom edge, away from right-edge icons).

## Activation Conditions
- Building audio beds or timing captions in `renderers/short_builder.py`, `cloud_short_factory.py`, or TSX caption components.

## Required Inputs
- Script lines with beat modes (`hook`, `alert`, `doc`, `panic`, `loop`) and seed/voice config.

## Step-by-Step Workflow
1. Synthesize lines with `edge-tts` (`en-US-ChristopherNeural`, `en-US-GuyNeural`, `en-US-BrianNeural`, multi-voice automatic fallback on `NoAudioReceived`!).
2. Keep speaking rate brisk (`+5%` to `+9%`), zero dead pauses between sentences (`0.05s` beat gaps, `0.00s` on Frame-0 loop transition).
3. Layer varied per-short procedural BGM + contextual SFX (`whoosh`, `fizz`, `crunch`, `squelch`, `zap`, `heartbeat`) mixed below speech and normalized via FFmpeg `loudnorm=I=-14:TP=-1.5:LRA=7`.
4. Emit word-level start/end timestamps aligned to caption chunks (max 2-3 bold Impact words at once inside safe zone).

## Output Format
Normalized WAV/AAC master audio + JSON `words[]` timeline (`{word, start, end, mode, scene_id}`).

## Validation Criteria
- Voice peaks clear over BGM; loudness near `-14 LUFS`; zero truncated final syllables; zero caption overlap with bottom title/right icons.

## Failure Handling
- Retry transient EdgeTTS failures across backup US Neural voices; fail loudly if output duration `< 5s`.

## Security Restrictions
- Only procedural/self-synthesized audio or verified royalty-free/CC0 SFX (`public/*.wav`); never copyrighted music clips.

## Examples
- `short_builder.py` `AUDIO_PALETTES` selects distinct key/tempo per seed so consecutive uploads avoid repetitive YPP audio fingerprints.
