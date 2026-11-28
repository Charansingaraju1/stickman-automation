# EXPERIMENTS

Rules: Change 1 primary variable per test, collect minimum 5 videos per variant across 24h / 48h / 7d windows, never peek early or invent metrics.

## Active / Planned Backlog

| ID | Hypothesis | Controlled Variable | Success Metric | Status |
|---|---|---|---|---|
| **EXP-001** | Minimalist B&W SVG `ZackStickmanShort` on `#FAFAFA` outperforms dark AI-JPG `CloudShort` on initial retention (`averageViewPercentage`) | Visual style (`B&W Vector` vs `Dark 3D JPG`) | 48h & 7d `engagedViews` / `views` + `averageViewPercentage` | **Pending OAuth analytics re-auth & first B&W pilot** |
| **EXP-002** | Tight 16–20s pacing beats 24–28s pacing on replay / `averageViewPercentage` | Duration band (`16–20s` vs `24–28s`) | `averageViewPercentage` & `subscribersGained` | Queued after EXP-001 |
| **EXP-003** | Curiosity-question titles (`<=35` chars) beat statement hooks on feed discovery | Title syntax | First-24h `engagedViews` | Queued after EXP-002 |
