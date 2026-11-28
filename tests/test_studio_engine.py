"""TDD verification suite for studio_engine.py, security audit, and pipeline contracts."""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.run_agents import audit_security
from agents.studio_engine import (
    TOPIC_WEIGHTS,
    build_flow_prompts,
    fetch_youtube_analytics,
    generate_research_pack,
    inspect_video_qc,
    score_topic,
    validate_storyboard,
)


def _sample_storyboard():
    return [
        {
            "duration_sec": 3.5,
            "narration": "Stop pouring water on flaming 400F pan oil.",
            "action": "Stickman holds water cup over stove pan.",
            "expression": "shock",
            "camera_pos": "medium 9:16 front",
            "camera_motion": "push in 1.0x->1.1x",
            "background": "minimalist white #FAFAFA kitchen outline",
            "objects": ["pan", "water_cup", "orange_flame"],
            "selective_colors": ["#FF3B30"],
            "sfx": "fizz",
            "start_frame": "stickman_cup_above_pan",
            "end_frame": "droplets_enter_oil",
            "transition": "cut_on_splash",
        },
        {
            "duration_sec": 7.0,
            "narration": "Water sinks straight beneath lighter hot oil and flashes 1,700 times bigger.",
            "action": "Zoom macro inside pan cross-section as steam expands violently.",
            "expression": "panic",
            "camera_pos": "macro cutaway",
            "camera_motion": "shake_and_zoom",
            "background": "clean B&W diagram cross-section",
            "objects": ["oil_layer", "steam_bubble", "flaming_droplets"],
            "selective_colors": ["#FF3B30", "#FFD60A"],
            "sfx": "whoosh_explosion_safe",
            "start_frame": "droplets_enter_oil",
            "end_frame": "oil_cloud_mushroom",
            "transition": "zoom_out",
        },
        {
            "duration_sec": 5.5,
            "narration": "Slide a flat metal lid sideways instead so fire starves in seconds.",
            "action": "Stickman calmly slides metal lid over pan, starving red flames.",
            "expression": "curious",
            "camera_pos": "wide 9:16",
            "camera_motion": "smooth_pullback_loop",
            "background": "minimalist white #FAFAFA kitchen outline",
            "objects": ["metal_lid", "extinguished_pan"],
            "selective_colors": ["#FF3B30"],
            "sfx": "chime",
            "start_frame": "oil_cloud_mushroom",
            "end_frame": "stickman_cup_above_pan",
            "transition": "loop_match",
        },
    ]


class StudioEngineTests(unittest.TestCase):
    def test_topic_weights_sum_to_100(self):
        self.assertEqual(sum(TOPIC_WEIGHTS.values()), 100)

    def test_score_topic_valid_and_bounds(self):
        good = score_topic({k: v for k, v in TOPIC_WEIGHTS.items()})
        self.assertEqual(good["total"], 100)
        self.assertTrue(good["editorial_estimate_only"])
        self.assertTrue(good["passes_editorial_gate"])

        bad_scores = dict(TOPIC_WEIGHTS)
        bad_scores["opening_hook"] = 25
        with self.assertRaises(ValueError):
            score_topic(bad_scores)

    def test_research_pack_generates_30_ranked_ideas(self):
        pack = generate_research_pack()
        self.assertEqual(len(pack), 30)
        self.assertTrue(all(item["editorial_estimate_only"] for item in pack))
        self.assertGreaterEqual(pack[0]["total"], pack[-1]["total"])

    def test_storyboard_and_flow_continuity(self):
        sb = _sample_storyboard()
        val = validate_storyboard(sb)
        self.assertTrue(val["valid"], val["issues"])
        prompts = build_flow_prompts(sb)
        self.assertEqual(len(prompts), 3)
        self.assertEqual(prompts[1]["start_frame_anchor"], sb[0]["end_frame"])
        self.assertFalse(prompts[1]["paid_api_executed"])

        broken = _sample_storyboard()[:1]
        self.assertFalse(validate_storyboard(broken)["valid"])

    def test_security_audit_passes_with_zero_leaks(self):
        sec = audit_security(ROOT)
        self.assertTrue(sec["ok"], sec)

    def test_analytics_does_not_fabricate_when_scope_missing(self):
        res = fetch_youtube_analytics(days=7)
        if not res["ok"]:
            self.assertIn(res["error"], ("MISSING_ANALYTICS_SCOPE", "MISSING_TOKEN_JSON"))

    def test_qc_gate_on_real_video(self):
        sample_mp4 = ROOT / "videos" / "stickman_knuckle_cracking_viral.mp4"
        if sample_mp4.exists():
            qc = inspect_video_qc(sample_mp4)
            self.assertEqual(qc["width"], 1080)
            self.assertEqual(qc["height"], 1920)
            self.assertTrue(qc["has_audio"])


if __name__ == "__main__":
    unittest.main()
