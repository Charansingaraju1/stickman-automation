# CHARACTER BIBLE — StickNation Minimalist Identity

## Visual Standard (Inspired by Zack-style Clarity, Original Design)
- **Canvas & Palette:** Crisp matte off-white `#FAFAFA` / `#FFFFFF` (`1080×1920`) for classic scientific explainers, or stark `#090D16` high-contrast cutaway dark stage strictly when X-ray/bioluminescent anatomy requires contrast.
- **Ink & Line Weight (Canonical Rig at `1080×1920`):**
  - Head radius: `38px` (`#000000` solid fill, subtle expressive white eyes `#FFFFFF` with `8px` pupils when reaction expression active)
  - Spine torso: `90px` segment (`-270` neck to `-180` hip relative to ground), `strokeWidth=16`, `strokeLinecap="round"`
  - Limbs (upper/lower arms & legs): `strokeWidth=14`, `strokeLinecap="round"`, `strokeLinejoin="round"`
  - Ground line: `#000000` `strokeWidth=6` at `y=1450` (full-body baseline scale `1.0`)
- **Selective Accent Palette (Max 2 focal accents per scene):**
  - Hazard / Blood / Heat: `#FF3B30`
  - Electricity / X-Ray / Neural Signal: `#00E5FF`
  - Chemical / Bio-Hazard: `#2ECC71`
  - Kinetic Callout / Force Vector: `#FFD60A`
- **Continuity Rules:**
  1. Never change character stroke weight or head ratio mid-cut without explicit camera zoom scale.
  2. Scene `N+1` `start_frame` must preserve props, camera vector, and position from Scene `N` `end_frame`.
  3. Avoid random background clutter or external watermarks.
