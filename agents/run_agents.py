"""Autonomous $0 multi-agent crew (Scout -> Comedy Writer -> Retention Auditor -> Billing Guard)."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.prompts import AGENT_ROLES
from upload_to_youtube import send_telegram_alert

FREE_ENDPOINT = "https://models.github.ai/inference/chat/completions"
FREE_MODELS = {"openai/gpt-4o-mini"}
STUDIO_VALIDATED_BRIEFS: dict[str, dict[str, str]] = {
    "hotel_kettle": {
        "scenario_id": "hotel_kettle",
        "title": "Bro Thought It Was Regular Tap Water In A Hotel Kettle 😱💀 #shorts",
        "mistake_hook": "Stickman pours hotel electric kettle straight into a mug, takes a confident sip, freezes one eyebrow raised.",
        "deadpan_line": "Hmm. Savory.",
        "twist_7s": "Snap-zoom inside glowing heating coil as submerged fabric fibers bubble into green sock soup.",
        "peak_beat": "Biofilm scales flake off the steel element straight into his mug while he stares at the lid.",
        "loop_bridge": "...so always boil and dump a hotel kettle twice because...",
    },
    "bleach_vinegar": {
        "scenario_id": "bleach_vinegar",
        "title": "Bro Mixed Bleach And Vinegar To Clean The Shower 💀🧪 #shorts",
        "mistake_hook": "Stickman in oversized dish gloves mixes two bottles like a proud chemist, leans in to sniff.",
        "deadpan_line": "Why does the air taste spicy?",
        "twist_7s": "Bathroom tile cuts to lung X-ray as yellow chloramine gas clouds squeeze stick-figure ribs inward.",
        "peak_beat": "Every extra scrub stirs faster yellow vapor up the glass door until the exhaust fan rattles.",
        "loop_bridge": "...the exact second...",
    },
    "grease_fire": {
        "scenario_id": "grease_fire",
        "title": "Bro Tried To Put Out A Grease Fire With Water 🔥💀 #shorts",
        "mistake_hook": "Stickman calmly holds a plastic cup of water over a tiny pan flame.",
        "deadpan_line": "Easy fix.",
        "twist_7s": "Macro inside pan bottom: water sinks under 400F oil, flashes 1,700x into steam, launches flaming oil volcano.",
        "peak_beat": "Burning oil droplets rain across the stove hood in slow motion while a pot lid sits two inches away.",
        "loop_bridge": "...so never grab a cup of water when...",
    },
    "reaper_water": {
        "scenario_id": "reaper_water",
        "title": "Bro Used Ice Water To Cool A Carolina Reaper 🌶️💀 #shorts",
        "mistake_hook": "Sweating Stickman chugs an entire pitcher of ice water in one gulp, pauses half a second.",
        "deadpan_line": "Oh. That made it worse.",
        "twist_7s": "Tongue cross-section: water droplets bounce off oily capsaicin like bowling balls across double the pain nerves.",
        "peak_beat": "Cold water flushes oil from the tip straight into the throat while a glass of milk waits ignored.",
        "loop_bridge": "...because water spreads the oil around while...",
    },
    "superglue_shirt": {
        "scenario_id": "superglue_shirt",
        "title": "Bro Bit Open A Super Glue Cap With His Teeth 😬🔥 #shorts",
        "mistake_hook": "Stickman bites a metal glue tube between molars with a squeak; one drop lands on cotton t-shirt and smokes.",
        "deadpan_line": "Why is my chest warm?",
        "twist_7s": "Macro cotton weave hits 200F exothermic spark—ember grows while Stickman pats it with paper towel (making it worse).",
        "peak_beat": "Tissue paper feeds the chemical reaction faster, turning one tiny glue drip into a smoking char ring.",
        "loop_bridge": "...because the fastest way to ignite your shirt is...",
    },
    "knuckle_cracking": {
        "scenario_id": "knuckle_cracking",
        "title": "What Actually Happens Inside Your Joints When You Crack Your Knuckles 🤔🦴 #shorts",
        "mistake_hook": "Stickman bends all ten fingers before a quiet exam—ECHO CRACK—while everyone turns to stare.",
        "deadpan_line": "Wait, was that bone?",
        "twist_7s": "X-ray cut between finger joints shows dissolved gas collapsing a fluid bubble at supersonic pop speed.",
        "peak_beat": "Joint fluid takes fifteen minutes to re-dissolve that gas before the next pop can fire.",
        "loop_bridge": "...which is why you cannot re-crack a knuckle until...",
    },
    "watermelon_seed": {
        "scenario_id": "watermelon_seed",
        "title": "Bro Accidentally Swallowed A Watermelon Seed… 🍉😱 #shorts",
        "mistake_hook": "Stickman swallows one black seed mid-bite and waits for a vine to sprout out his ears.",
        "deadpan_line": "Am I a garden now?",
        "twist_7s": "Stomach plunge: acid bath hits the hard seed coat, zero soil, zero sunlight, total false alarm.",
        "peak_beat": "Instead of sprouting roots, the smooth hull rides straight down the digestive slide untouched.",
        "loop_bridge": "...until the whole belly-vine rumor starts again when...",
    },
    "nosebleed_tilt": {
        "scenario_id": "nosebleed_tilt",
        "title": "Bro Tilted His Head Back During A Nosebleed… 🩸😬 #shorts",
        "mistake_hook": "Stickman tilts his chin sky-high with tissue plugs, proud of saving his white hoodie.",
        "deadpan_line": "Wait, wrong direction.",
        "twist_7s": "Throat cut shows blood draining backward toward his stomach while pinching the soft nostrils forward works.",
        "peak_beat": "Tilting up just hides the drip down your throat and stirs nausea before it spills out.",
        "loop_bridge": "...instead of leaning slightly forward and pinching because...",
    },
    "stay_awake": {
        "scenario_id": "stay_awake",
        "title": "Bro Tried To Stay Awake For 72 Hours Straight… 😵💀 #shorts",
        "mistake_hook": "Stickman lines up five espressos at 2 AM thinking sleep is optional.",
        "deadpan_line": "Still totally fine.",
        "twist_7s": "Brain scan flickers as 2-second micro-sleeps hijack his eyes open while his hands stall mid-blink.",
        "peak_beat": "Waste proteins pile between neurons until his brain force-reboots right over his keyboard.",
        "loop_bridge": "...because cheating sleep always triggers involuntary micro-naps when...",
    },
}


class BillingHaltError(RuntimeError):
    """Raised whenever any paid service, billing trigger, or non-free tier is detected."""


def _halt_billing(reason: str, notify: bool = True) -> None:
    alert = (
        "🚨 WARNING: billing is created — open the laptop\n\n"
        f"Stopped all agents & renders immediately ($0 lock triggered).\nReason: {reason}"
    )
    if notify:
        send_telegram_alert(alert)
    raise BillingHaltError(reason)


def assert_zero_cost(endpoint: str, model: str, notify: bool = True) -> None:
    if endpoint != FREE_ENDPOINT or model not in FREE_MODELS:
        _halt_billing(f"Blocked non-free inference target: {endpoint} / {model}", notify=notify)


def audit_security(root_dir: pathlib.Path = ROOT) -> dict[str, Any]:
    """Security Agent: checks .gitignore secret rules and scans code for exposed tokens."""
    gi = (root_dir / ".gitignore").read_text(encoding="utf-8", errors="ignore") if (root_dir / ".gitignore").exists() else ""
    missing_ignores = [p for p in (".env", "token.json", "client_secret.json") if p not in gi]
    leaks: list[str] = []
    token_re = re.compile(r"(?:EAAQ[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{16,}|cfut_[A-Za-z0-9_]{16,})")
    for p in list((root_dir / "agents").glob("*.py")) + list((root_dir / "renderers").glob("*.py")) + [root_dir / "upload_to_youtube.py"]:
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if token_re.search(txt):
                leaks.append(str(p.relative_to(root_dir)))
    return {"ok": not missing_ignores and not leaks, "missing_ignores": missing_ignores, "leaks": leaks}


def call_free_llm(role: str, user_msg: str, token: str | None) -> dict[str, Any]:
    spec = AGENT_ROLES[role]
    assert_zero_cost(FREE_ENDPOINT, spec["model"])
    if not token:
        raise RuntimeError("NO_TOKEN")

    payload = json.dumps({
        "model": spec["model"],
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": spec["prompt"]},
            {"role": "user", "content": user_msg},
        ],
    }).encode("utf-8")
    req = urllib.request.Request(
        FREE_ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "StickNation-FreeAgents/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return json.loads(body["choices"][0]["message"]["content"])
    except urllib.error.HTTPError as exc:
        err_txt = exc.read().decode("utf-8", errors="ignore")
        if exc.code in (402, 429) or "billing" in err_txt.lower() or "quota" in err_txt.lower():
            _halt_billing(f"HTTP {exc.code} from {FREE_ENDPOINT}: {err_txt[:160]}")
        raise


def audit_script(script_data: dict[str, Any]) -> dict[str, Any]:
    """Deterministic retention, Studio, and YPP Inauthentic Content compliance check."""
    issues: list[str] = []
    lines = script_data.get("lines", [])
    visuals = script_data.get("visuals", [])
    title = script_data.get("title", "").lower()
    if not lines or len(lines) < 4:
        issues.append("Need at least 4 brisk visual beats.")
    if visuals and visuals[0][0] == "diagram_only":
        issues.append("Frame 0 must open on character action, not anatomy diagram.")
    if any(visuals[i][0] == visuals[i + 1][0] for i in range(len(visuals) - 1)):
        issues.append("Avoid adjacent repeated visual assets (YPP variety rule).")
    if title.startswith("why you should never"):
        issues.append("Vary title hook; avoid repeating 'Why You Should NEVER...' template.")
    last_text = (lines[-1][1] if lines else "").lower()
    if any(b in last_text for b in ("so next time", "before you", "don't forget to")):
        issues.append("Remove trailing generic outro; end mid-clause for loop.")
    jargon = ("macrophage", "cerumen", "nucleation", "cyanoacrylate", "subdermal")
    boilerplate = ("spikes violently with nowhere to escape",)
    full_txt = " ".join(x[1].lower() for x in lines)
    if any(j in full_txt for j in jargon):
        issues.append("Replace clinical jargon with plain deadpan speech.")
    if any(b in full_txt for b in boilerplate):
        issues.append("Remove boilerplate fallback text for YPP originality.")
    score = max(0, 100 - 25 * len(issues))
    return {"approved": len(issues) == 0, "score": score, "issues": issues}


def build_offline_script(brief: dict[str, str]) -> dict[str, Any]:
    """Zero-token deterministic script matching WriterAgent rules (no shared boilerplate)."""
    return {
        "title": brief["title"],
        "voice": "en-US-AndrewMultilingualNeural",
        "voice_rate": "+3%",
        "lines": [
            ["NARRATOR", f"{brief['mistake_hook']} \"{brief['deadpan_line']}\"", "1", "alert", 0.10, "&H003838FF&", "BAD IDEA"],
            ["NARRATOR", brief["twist_7s"], "2", "doc", 0.08, "&H0000E6FF&", "0:07 TWIST"],
            ["NARRATOR", brief["peak_beat"], "3", "panic", 0.08, "&H003838FF&", "PEAK RISK"],
            ["NARRATOR", brief["loop_bridge"], "4", "panic", 0.00, "&H003838FF&", "LOOP"],
        ],
        "visuals": [
            ["char_frame0", "1", "hook_punch"],
            ["twist_7s", "2", "punch4"],
            ["peak_reaction", "3", "shake"],
            ["loop_return", "4", "push"],
        ],
    }


def run_crew(scenario: str, offline: bool = False, notify: bool = False) -> dict[str, Any]:
    token = None if offline else os.environ.get("GITHUB_TOKEN")

    if token:
        script_out = call_free_llm("script_agent", f"Create a deadpan script & brief for: {scenario}", token)
        scout_out = STUDIO_VALIDATED_BRIEFS.get(scenario, STUDIO_VALIDATED_BRIEFS["hotel_kettle"])
    else:
        scout_out = STUDIO_VALIDATED_BRIEFS.get(scenario, STUDIO_VALIDATED_BRIEFS["hotel_kettle"])
        script_out = build_offline_script(scout_out)

    det_audit = audit_script(script_out)
    pub_review = call_free_llm("publisher", json.dumps(script_out), token) if token else {"approved": det_audit["approved"]}
    approved = bool(det_audit["approved"] and pub_review.get("approved", True))

    sec = audit_security()
    result = {
        "scout": scout_out,
        "script_agent": script_out,
        "publisher_review": det_audit,
        "security_audit": sec,
        "approved": approved and sec["ok"],
    }
    out_dir = ROOT / "agents" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest_crew_handoff.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    if notify:
        send_telegram_alert(
            f"🤖 5-Agent Draft Ready ($0 Cloud)\n\n"
            f"🎬 {scout_out['title']}\n"
            f"💬 Hook: {scout_out['deadpan_line']}\n"
            f"✅ Publisher Review: {det_audit['score']}/100\n\n"
            f"Held locally/draft — awaiting your go-ahead."
        )
    return result


def send_c_assistant_daily_brief(scenario: str = "hotel_kettle", offline: bool = False) -> str:
    """C Assistant delegates to Script -> Editor -> Publisher -> Social Manager and sends Boss's brief."""
    req = urllib.request.Request(
        "https://sticknation-bot.sticknation.workers.dev/?check=live",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    subs, views, top_title, ready_cnt = "?", "?", "Bro Thought It Was a Mint… 😱💀 #shorts", 0
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            live = json.loads(r.read().decode("utf-8"))
        yt = live.get("yt", {})
        subs = yt.get("subscribers", "?")
        views = yt.get("channelTotalViews", "?")
        top_title = (yt.get("topShort") or {}).get("title", top_title)
        ready_cnt = len(live.get("gh", {}).get("readyOnDeck", []))
    except Exception:
        pass

    crew = run_crew(scenario, offline=offline, notify=False)
    assert_zero_cost(FREE_ENDPOINT, AGENT_ROLES["c_assistant"]["model"])
    msg = (
        f"📋 Daily Update — C Assistant\n\n"
        f"📱 Social Manager (@StickNationDaily): {subs} | {views}\n"
        f"🏆 Top Short: {top_title}\n"
        f"⏰ Publisher Slot: 2:30 PM EST daily (1/day) | {ready_cnt} queued\n"
        f"✍️ Script + Review ({crew['publisher_review']['score']}/100 APV-ready): {crew['scout']['title']}\n"
        f"💬 Deadpan Hook: \"{crew['scout']['deadpan_line']}\"\n"
        f"💸 Billing Guard: $0.00 (Free Cloud Only)\n\n"
        f"— C Assistant"
    )
    send_telegram_alert(msg)
    return msg


def self_test() -> None:
    # 1. BillingGuard must reject non-free endpoints without firing live Telegram alerts
    try:
        assert_zero_cost("https://api.openai.com/v1/chat/completions", "gpt-4o", notify=False)
        raise AssertionError("Expected BillingHaltError for paid OpenAI URL")
    except BillingHaltError:
        pass
    # 2. Publisher review must flag clinical jargon, generic outro, and YPP template patterns
    bad = audit_script({
        "title": "Why You Should NEVER Test This",
        "lines": [["N", "So next time macrophage spikes violently with nowhere to escape.", "1", "doc", 0.1, None, None]],
        "visuals": [["diagram_only", "1", "pan"], ["diagram_only", "2", "zoom"]],
    })
    assert not bad["approved"] and len(bad["issues"]) >= 5
    # 3. Full offline crew run must pass 100/100 across all validated briefs + exact 7 agents + security pass
    for key in STUDIO_VALIDATED_BRIEFS:
        ok = run_crew(key, offline=True, notify=False)
        assert ok["approved"] and ok["publisher_review"]["score"] == 100 and ok["security_audit"]["ok"]
    assert set(AGENT_ROLES.keys()) == {"c_assistant", "script_agent", "editor", "publisher", "social_manager", "watchdog", "security_agent"}
    # 4. Validate cloud_queue & every CLOUD_PROFILE passes YPP compliance + offline audit
    from upload_to_youtube import load_viral_queue, validate_ypp_compliance
    from renderers.cloud_short_factory import CLOUD_PROFILES, build_lines_and_scenes
    q_items = load_viral_queue()
    for qi in q_items[8:]:
        validate_ypp_compliance(qi, [q["id"] for q in q_items[:8]])
    for ck, cp in CLOUD_PROFILES.items():
        ls, sc = build_lines_and_scenes(ck, cp)
        res = audit_script({
            "title": cp["title"],
            "lines": [[l[0], l[1], l[2], l[3], l[4], l[5], l[6]] for l in ls],
            "visuals": [[s[2] or f"vec_{ck}_{i}", str(i + 1), s[1]] for i, s in enumerate(sc)],
        })
        assert res["approved"], f"CLOUD_PROFILE {ck} failed YPP audit: {res['issues']}"
    print("SELF_TEST_PASSED: All 7 Agents + Cloud Factory + YPP Compliance verified ($0).")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", default="hotel_kettle", choices=list(STUDIO_VALIDATED_BRIEFS))
    p.add_argument("--offline", action="store_true")
    p.add_argument("--notify", action="store_true")
    p.add_argument("--daily-brief", action="store_true")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--test-billing-alert", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
    elif args.daily_brief:
        print(send_c_assistant_daily_brief(args.scenario, offline=args.offline))
    elif args.test_billing_alert:
        send_telegram_alert(
            "🧪 [TEST CHECK — NO REAL CHARGE]\n"
            "🚨 WARNING: billing is created — open the laptop\n\n"
            "Halted all AI agents, video generation & uploads immediately.\n"
            "Reason: Sample test check requested by Boss."
        )
    else:
        print(json.dumps(run_crew(args.scenario, offline=args.offline, notify=args.notify), indent=2))
