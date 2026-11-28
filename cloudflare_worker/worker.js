function buildWebDashboardHtml() {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>StickNation • Agent Control Room</title>
<style>
  :root{
    --bg:#060911;--panel:#0e1525;--panel2:#131c31;--bd:#1f2c47;--txt:#eef2ff;--mut:#8b9bb8;
    --cyan:#22d3ee;--amber:#fbbf24;--violet:#a78bfa;--emerald:#34d399;--rose:#fb7185;--sky:#38bdf8;--slate:#94a3b8;
  }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 520px at 50% -120px,#172554 0%,var(--bg) 60%);color:var(--txt);font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;padding:24px 18px 48px;line-height:1.5}
  .wrap{max-width:1120px;margin:0 auto}
  .hdr{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px;padding-bottom:18px;border-bottom:1px solid var(--bd);margin-bottom:18px}
  .title{font-size:22px;font-weight:800;letter-spacing:-.02em;margin:0}
  .sub{font-size:13px;color:var(--mut);margin-top:3px}
  .hdr-r{display:flex;gap:10px;align-items:center}
  .cost-pill{display:inline-flex;align-items:center;gap:7px;background:rgba(16,185,129,.12);border:1px solid rgba(52,211,153,.35);color:var(--emerald);padding:7px 13px;border-radius:999px;font-size:12px;font-weight:700}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--emerald);box-shadow:0 0 10px var(--emerald)}
  .btn{background:var(--panel2);color:var(--txt);border:1px solid var(--bd);padding:8px 14px;border-radius:9px;font-size:13px;font-weight:600;cursor:pointer;transition:.15s}
  .btn:hover{border-color:var(--cyan);color:#fff}

  .mcard{background:linear-gradient(135deg,rgba(34,211,238,.09),rgba(16,185,129,.05) 55%,rgba(14,21,37,.95));border:1px solid rgba(34,211,238,.35);border-radius:14px;padding:18px 20px;margin-bottom:18px}
  .mcard-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px}
  .mtitle{font-size:16px;font-weight:800;letter-spacing:-.01em}
  .msub{font-size:12.5px;color:var(--mut)}
  .mgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
  @media(max-width:760px){.mgrid{grid-template-columns:1fr}}
  .mbox{background:rgba(6,9,17,.6);border:1px solid var(--bd);border-radius:11px;padding:14px}
  .mbox-hdr{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
  .mlbl{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--cyan);font-weight:700}
  .mpct{font-size:12px;font-weight:700;color:var(--emerald)}
  .mnum{font-size:24px;font-weight:800;margin:4px 0}
  .mmeta{font-size:12px;color:var(--mut)}
  .pbar{height:8px;background:#0b1220;border:1px solid var(--bd);border-radius:999px;overflow:hidden;margin-top:10px}
  .pfill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--emerald));min-width:4px;border-radius:999px}

  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
  @media(max-width:860px){.kpis{grid-template-columns:repeat(2,1fr)}}
  .kpi{background:linear-gradient(180deg,rgba(255,255,255,.025),rgba(255,255,255,0));background-color:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:14px 16px}
  .kpi .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);font-weight:700}
  .kpi .val{font-size:20px;font-weight:800;margin-top:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .kpi .hint{font-size:12px;color:var(--mut);margin-top:2px}

  .tier-wrap{margin-bottom:18px}
  .tier-hdr{display:flex;align-items:center;gap:8px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--mut);font-weight:700;margin:0 0 10px}
  .tier-bar{height:1px;flex:1;background:var(--bd)}
  .tier-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}

  .acard{background:var(--panel);border:1px solid var(--bd);border-top:3px solid var(--ac,var(--cyan));border-radius:12px;padding:15px;cursor:pointer;transition:transform .14s,border-color .14s,box-shadow .14s;text-align:left;width:100%;color:inherit}
  .acard:hover{transform:translateY(-2px);border-color:var(--ac,var(--cyan));background:var(--panel2)}
  .acard.active{border-color:var(--ac,var(--cyan));background:var(--panel2);box-shadow:0 0 0 1px var(--ac,var(--cyan)),0 12px 28px -12px rgba(0,0,0,.85)}
  .acard-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px}
  .aname{font-size:15px;font-weight:700}
  .abadge{font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;background:rgba(255,255,255,.06);color:var(--ac,var(--cyan))}
  .asummary{font-size:12.5px;color:var(--mut);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .aclick{font-size:11px;color:var(--ac,var(--cyan));margin-top:10px;font-weight:600;opacity:.85}

  .inspector{background:var(--panel2);border:1px solid var(--bd);border-left:4px solid var(--cyan);border-radius:14px;padding:20px;margin:22px 0}
  .insp-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding-bottom:14px;border-bottom:1px solid var(--bd);margin-bottom:16px}
  .insp-cols{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  @media(max-width:860px){.insp-cols{grid-template-columns:1fr}}
  .ibox{background:rgba(6,9,17,.55);border:1px solid var(--bd);border-radius:10px;padding:14px}
  .ibox h3{margin:0 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);display:flex;align-items:center;gap:6px}
  .ibox p,.ibox ul{margin:0;font-size:13.5px;color:#dbe5f8}
  .ibox ul{padding-left:18px;display:flex;flex-direction:column;gap:6px}

  .tabs-card{background:var(--panel);border:1px solid var(--bd);border-radius:14px;overflow:hidden}
  .tabs-bar{display:flex;gap:6px;padding:12px 16px;border-bottom:1px solid var(--bd);background:rgba(255,255,255,.015)}
  .tab{background:transparent;color:var(--mut);border:1px solid transparent;padding:6px 12px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer}
  .tab.active{background:var(--panel2);color:var(--txt);border-color:var(--bd)}
  .tbl-wrap{overflow-x:auto}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{text-align:left;padding:11px 16px;border-bottom:1px solid var(--bd)}
  th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut)}
  tr:last-child td{border-bottom:0}
  a{color:var(--sky);text-decoration:none}a:hover{text-decoration:underline}
  .foot{margin-top:16px;font-size:12px;color:var(--mut);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <div>
      <h1 class="title">StickNation • Control Room</h1>
      <div class="sub">5 Core Cloud Agents + 2 Safety Guards • Click any agent below to inspect live &amp; past work</div>
    </div>
    <div class="hdr-r">
      <span class="cost-pill"><span class="dot"></span>$0.00 FREE TIER ACTIVE</span>
      <button class="btn" onclick="loadLive()">↻ Refresh Live Data</button>
    </div>
  </div>

  <section class="mcard" id="monetization">
    <div class="mcard-top">
      <div>
        <div class="mtitle">YouTube Partner Program • Monetization Goal Tracker</div>
        <div class="msub">First Goal (Early YPP Fan Funding): <b>500 subscribers</b> + <b>3M Shorts views (90d)</b> • Full Ad Share Goal: <b>1,000 subscribers</b> + <b>10M Shorts views (90d)</b></div>
      </div>
      <span class="cost-pill" id="ypp-stage">Syncing exact YouTube counts...</span>
    </div>
    <div class="mgrid" id="monetization-grid">
      <div class="mbox"><div class="mlbl">Subscribers vs First Goal</div><div class="mnum">Loading...</div></div>
      <div class="mbox"><div class="mlbl">Total Views vs Shorts Monetization</div><div class="mnum">Loading...</div></div>
    </div>
  </section>

  <div class="kpis" id="kpis">
    <div class="kpi"><div class="lbl">Loading</div><div class="val">Syncing...</div></div>
  </div>

  <div id="crew-layers"></div>

  <div class="inspector" id="inspector">
    <div class="insp-head">
      <div>
        <div style="font-size:12px;color:var(--mut);text-transform:uppercase;font-weight:700">Agent Inspector</div>
        <div style="font-size:19px;font-weight:800;margin-top:2px" id="insp-title">Loading crew...</div>
      </div>
      <span class="abadge" id="insp-badge">...</span>
    </div>
    <div class="insp-cols">
      <div class="ibox"><h3>🟢 Doing Right Now</h3><p id="insp-now">—</p></div>
      <div class="ibox"><h3>🕘 Did In The Past</h3><ul id="insp-past"></ul></div>
      <div class="ibox"><h3>⚡ Why It's Useful</h3><p id="insp-why">—</p></div>
    </div>
  </div>

  <div class="tabs-card">
    <div class="tabs-bar">
      <button class="tab active" id="tab-shorts" onclick="setTab('shorts')">YouTube Shorts Performance</button>
      <button class="tab" id="tab-runs" onclick="setTab('runs')">Cloud Actions History</button>
      <button class="tab" id="tab-commits" onclick="setTab('commits')">Recent System Changes</button>
    </div>
    <div class="tbl-wrap"><table id="data-table"></table></div>
  </div>

  <div class="foot">
    <span id="updated">Connecting to Cloudflare edge...</span>
    <span>Cloudflare Workers Free + GitHub Actions Free • 0% Laptop Dependency</span>
  </div>
</div>

<script>
let STATE = { yt: {}, gh: {}, selectedId: 'c_assistant', tab: 'shorts', agents: [] };

function buildAgents(d) {
  const yt = d.yt || {}, gh = d.gh || {};
  const commits = gh.commits || [];
  const uploaded = gh.uploaded || [];
  const readyCnt = (gh.readyOnDeck || []).length;
  const lastRun = gh.lastRun ? (gh.lastRun.conclusion || gh.lastRun.status) + ' (' + gh.lastRun.name + ')' : 'idle';
  const topTitle = yt.topShort ? yt.topShort.title + ' (' + yt.topShort.viewsText + ')' : 'N/A';
  const commitBullets = commits.slice(0, 3).map(c => c.sha + ' — ' + c.msg);

  return [
    {
      tier: 'Core 5 Production Agents',
      id: 'c_assistant',
      name: '1. C Assistant',
      badge: 'Team Lead • Active',
      color: 'var(--cyan)',
      summary: 'Coordinates daily handoffs across the crew and sends 7:00 PM IST Telegram briefs.',
      now: 'Coordinating crew specialists, tracking ' + readyCnt + ' ready Shorts in queue, and dispatching updates when triggers complete.',
      past: commitBullets.slice(0, 2).length ? commitBullets.slice(0, 2) : ['Coordinating repository runs and cloud alerts.'],
      why: 'Gives you one command interface across scripts, rendering, publishing, and growth telemetry.'
    },
    {
      tier: 'Core 5 Production Agents',
      id: 'script_agent',
      name: '2. Scriptwriter',
      badge: 'APV >= 90% Mode',
      color: 'var(--amber)',
      summary: 'Writes 15–30s open-loop stickman hooks, <=38-char titles, and tight visual beats.',
      now: 'Applying 100-point topic scoring and open-loop script rules (hook at 0:00, reveal withheld to 0:13+, seamless loop).',
      past: ['Top Short performer: ' + topTitle + '.'],
      why: 'Drives higher average percentage viewed so Shorts graduate out of small initial test pools.'
    },
    {
      tier: 'Core 5 Production Agents',
      id: 'editor',
      name: '3. Editor',
      badge: 'Render Ready',
      color: 'var(--violet)',
      summary: 'Renders 9:16 B&W + selective-color vector Shorts, 16:9 compilations, -14 LUFS audio, and captions.',
      now: 'Running Remotion ZackStickmanShort & CloudShort compositions plus FFprobe QC gating before upload.',
      past: ['Built automated 9:16 queue & 16:9 compilation builder in renderers/.'],
      why: 'Maintains fast visual pacing, readable safe-zone text, and audio loudness parity without local laptop load.'
    },
    {
      tier: 'Core 5 Production Agents',
      id: 'publisher',
      name: '4. Publisher',
      badge: readyCnt ? readyCnt + ' Queued' : 'Queue Clear',
      color: 'var(--sky)',
      summary: 'Runs YPP compliance checks, de-duplicates uploads, and publishes at US peak slots.',
      now: 'Holding ' + readyCnt + ' queued Shorts behind AUTO_PUBLISH_ENABLED safety gate (' + lastRun + ').',
      past: ['Published ' + uploaded.length + ' Shorts tracked in uploaded_history.json.'],
      why: 'Prevents duplicate templates, thin descriptions, and accidental unapproved uploads.'
    },
    {
      tier: 'Core 5 Production Agents',
      id: 'social_manager',
      name: '5. Social Manager',
      badge: 'YT + IG Sync',
      color: 'var(--slate)',
      summary: 'Tracks exact YouTube channel subscribers/views, cross-posts IG Reels, and schedules feedback loops.',
      now: 'Monitoring @StickNationDaily (' + (yt.subscribers || '0 subscribers') + ', ' + (yt.channelTotalViews || '0 views') + ').',
      past: ['Cross-posting workflow wired in upload_to_instagram.py with pinned comment automation.'],
      why: 'Connects live YouTube & Instagram audience counts back into topic selection and monetization milestones.'
    },
    {
      tier: 'Automated Safety & Cost Guards',
      id: 'watchdog',
      name: '6. Watchdog',
      badge: '$0.00 Enforced',
      color: 'var(--emerald)',
      summary: 'Locks GitHub Models to free endpoints and halts pipelines via BillingHaltError if paid triggers appear.',
      now: 'Enforcing $0 free-tier lock across GitHub Actions, Cloudflare Workers Free, EdgeTTS, and FFmpeg.',
      past: ['Verified zero-cost guardrails in agents/run_agents.py --self-test.'],
      why: 'Guarantees zero accidental API charges while automating daily workflows.'
    },
    {
      tier: 'Automated Safety & Cost Guards',
      id: 'security_agent',
      name: '7. Security Agent',
      badge: 'Audit Clean',
      color: 'var(--rose)',
      summary: 'Scans source & workflows for leaked OAuth/Telegram/GitHub secrets and enforces .gitignore hygiene.',
      now: 'Enforcing environment-only secrets (env.BOT_TOKEN, env.GH_TOKEN, .gitignore rules).',
      past: ['Removed plaintext tokens from tracked scripts and workflows.'],
      why: 'Protects YouTube OAuth, Telegram bot control, and GitHub tokens from exposure.'
    }
  ];
}

function renderMonetization(yt) {
  const subs = Number(yt.subscriberCount || 0);
  const officialViews = Number(yt.channelTotalViewsCount || 0);
  const sumShorts = Number(yt.sumShortsViews || 0);

  const firstSubsGoal = 500;
  const fullSubsGoal = 1000;
  const firstShortsViewsGoal = 3000000;
  const fullShortsViewsGoal = 10000000;

  const subsPctFirst = Math.min(100, (subs / firstSubsGoal) * 100);
  const viewsPctFirst = Math.min(100, (officialViews / firstShortsViewsGoal) * 100);
  const stageEl = document.getElementById('ypp-stage');
  stageEl.textContent = subs >= fullSubsGoal ? 'Tier 2 Sub Goal Met' : subs >= firstSubsGoal ? 'Tier 1 Sub Goal Met' : 'Stage: Building First 500 Subs';

  document.getElementById('monetization-grid').innerHTML =
    '<div class="mbox">' +
      '<div class="mbox-hdr"><span class="mlbl">Subscribers (First Goal: 500 • Full YPP: 1,000)</span><span class="mpct">' + subsPctFirst.toFixed(2) + '% of 500</span></div>' +
      '<div class="mnum">' + subs.toLocaleString() + ' <span style="font-size:14px;color:var(--mut);font-weight:600">/ 500 (First Goal)</span></div>' +
      '<div class="mmeta">Exact YouTube text: <b>' + (yt.subscribers || 'Unavailable') + '</b> • ' + Math.max(0, firstSubsGoal - subs).toLocaleString() + ' needed for Tier 1 • ' + Math.max(0, fullSubsGoal - subs).toLocaleString() + ' for 1,000 Ad Share</div>' +
      '<div class="pbar"><div class="pfill" style="width:' + Math.max(subs > 0 ? 2 : 0, subsPctFirst) + '%"></div></div>' +
    '</div>' +
    '<div class="mbox">' +
      '<div class="mbox-hdr"><span class="mlbl">Total Views (First Goal: 3M Shorts Views / 90d)</span><span class="mpct">' + viewsPctFirst.toFixed(4) + '% of 3M</span></div>' +
      '<div class="mnum">' + officialViews.toLocaleString() + ' <span style="font-size:14px;color:var(--mut);font-weight:600">/ 3,000,000 (First Goal)</span></div>' +
      '<div class="mmeta">Official /about: <b>' + (yt.channelTotalViews || 'Unavailable') + '</b> (Sum across ' + (yt.shorts || []).length + ' Shorts: <b>' + sumShorts.toLocaleString() + '</b>) • Full Ad Share: 10M</div>' +
      '<div class="pbar"><div class="pfill" style="width:' + Math.max(officialViews > 0 ? 1.5 : 0, viewsPctFirst) + '%"></div></div>' +
    '</div>';
}

function renderCrew() {
  const tiers = [...new Set(STATE.agents.map(a => a.tier))];
  document.getElementById('crew-layers').innerHTML = tiers.map(tier => {
    const cards = STATE.agents.filter(a => a.tier === tier).map(a => {
      const act = a.id === STATE.selectedId ? 'active' : '';
      return '<button class="acard ' + act + '" style="--ac:' + a.color + '" data-id="' + a.id + '" onclick="selectAgent(this.dataset.id)">' +
        '<div class="acard-top"><span class="aname">' + a.name + '</span><span class="abadge">' + a.badge + '</span></div>' +
        '<div class="asummary">' + a.summary + '</div>' +
        '<div class="aclick">' + (act ? '▼ Viewing details below' : 'Click to inspect →') + '</div>' +
      '</button>';
    }).join('');
    return '<div class="tier-wrap"><div class="tier-hdr"><span>' + tier + '</span><span class="tier-bar"></span></div><div class="tier-grid">' + cards + '</div></div>';
  }).join('');
  renderInspector();
}

function renderInspector() {
  const a = STATE.agents.find(x => x.id === STATE.selectedId) || STATE.agents[0];
  if (!a) return;
  const insp = document.getElementById('inspector');
  insp.style.borderLeftColor = a.color;
  document.getElementById('insp-title').textContent = a.name;
  const b = document.getElementById('insp-badge');
  b.textContent = a.badge;
  b.style.color = a.color;
  document.getElementById('insp-now').textContent = a.now;
  document.getElementById('insp-past').innerHTML = a.past.map(p => '<li>' + p + '</li>').join('');
  document.getElementById('insp-why').textContent = a.why;
}

function selectAgent(id) {
  STATE.selectedId = id;
  renderCrew();
}

function setTab(t) {
  STATE.tab = t;
  ['shorts','runs','commits'].forEach(k => document.getElementById('tab-' + k).classList.toggle('active', k === t));
  renderTable();
}

function renderTable() {
  const el = document.getElementById('data-table');
  if (STATE.tab === 'shorts') {
    el.innerHTML = '<tr><th>#</th><th>Short Title</th><th>Live Views</th></tr>' +
      (STATE.yt.shorts || []).map((s, i) =>
        '<tr><td>' + (i + 1) + '</td><td><a target="_blank" href="https://youtube.com/shorts/' + s.id + '">' + s.title + '</a></td><td><b>' + s.viewsText + '</b></td></tr>'
      ).join('');
  } else if (STATE.tab === 'runs') {
    el.innerHTML = '<tr><th>Workflow</th><th>Outcome</th><th>Trigger</th><th>Started (UTC)</th></tr>' +
      (STATE.gh.runs || []).map(r =>
        '<tr><td><a target="_blank" href="' + r.html_url + '">' + r.name + '</a></td><td><b>' + (r.conclusion || r.status) + '</b></td><td>' + r.event + '</td><td>' + (r.created_at || '').slice(0,16).replace('T',' ') + '</td></tr>'
      ).join('');
  } else {
    el.innerHTML = '<tr><th>Commit</th><th>Description</th><th>Timestamp (UTC)</th></tr>' +
      (STATE.gh.commits || []).map(c =>
        '<tr><td><code>' + c.sha + '</code></td><td>' + c.msg + '</td><td>' + (c.date || '').slice(0,16).replace('T',' ') + '</td></tr>'
      ).join('');
  }
}

async function loadLive() {
  const res = await fetch('/?check=live');
  const d = await res.json();
  STATE.yt = d.yt || {};
  STATE.gh = d.gh || {};
  STATE.agents = buildAgents(d);

  renderMonetization(STATE.yt);

  const qCnt = (STATE.gh.readyOnDeck || []).length;
  const pubCnt = (STATE.gh.uploaded || []).length;
  const lastRun = STATE.gh.lastRun ? (STATE.gh.lastRun.conclusion || STATE.gh.lastRun.status).toUpperCase() : 'IDLE';
  const topV = STATE.yt.topShort ? STATE.yt.topShort.viewsText : '—';

  document.getElementById('kpis').innerHTML = [
    ['YouTube Subscribers', STATE.yt.subscribers || '—', (STATE.yt.videoCount || '—') + ' total'],
    ['YouTube Total Views', STATE.yt.channelTotalViews || '—', 'Shorts sum: ' + Number(STATE.yt.sumShortsViews || 0).toLocaleString()],
    ['Top Outlier Short', topV, STATE.yt.topShort ? STATE.yt.topShort.title : 'N/A'],
    ['Upload Pipeline', pubCnt + ' Published', qCnt + ' queued • ' + lastRun]
  ].map(([l,v,h]) => '<div class="kpi"><div class="lbl">' + l + '</div><div class="val">' + v + '</div><div class="hint">' + h + '</div></div>').join('');

  renderCrew();
  renderTable();
  document.getElementById('updated').textContent = 'Synced live at ' + new Date().toLocaleTimeString() + ' • @StickNationDaily';
}

loadLive();
setInterval(loadLive, 30000);
</script>
</body></html>`;
}

const GH_REPO = "Charansingaraju1/stickman-automation";
const YT_HANDLE = "@StickNationDaily";

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function parseViewNum(text) {
  if (!text) return 0;
  const s = String(text).toLowerCase().replace(/,/g, "").trim();
  if (s.includes("no views")) return 0;
  const m = s.match(/([\d.]+)\s*([kmb])?/);
  if (!m) return 0;
  let n = parseFloat(m[1]);
  if (m[2] === "k") n *= 1e3;
  else if (m[2] === "m") n *= 1e6;
  else if (m[2] === "b") n *= 1e9;
  return Math.round(n);
}

async function fetchYouTubeLive() {
  const headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "SOCS=CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg"
  };

  const [aboutRes, shortsRes] = await Promise.all([
    fetch(`https://www.youtube.com/${YT_HANDLE}/about`, { headers }),
    fetch(`https://www.youtube.com/${YT_HANDLE}/shorts`, { headers })
  ]);

  const [aboutHtml, shortsHtml] = await Promise.all([aboutRes.text(), shortsRes.text()]);

  const subMatch = aboutHtml.match(/"subscriberCountText"\s*:\s*[^}]*"([^"]*subscriber[^"]*)"/i);
  const viewsMatch = aboutHtml.match(/"viewCountText"\s*:\s*"([^"]*view[^"]*)"/i);
  const vidsMatch = aboutHtml.match(/"videoCountText"\s*:\s*"([^"]*video[^"]*)"/i);

  const shorts = [];
  const seen = new Set();
  const itemRegex = /"entityId"\s*:\s*"shorts-shelf-item-([^"]+)"[\s\S]{0,1200}?"accessibilityText"\s*:\s*"((?:[^"\\]|\\.)*)"/g;
  let m;
  while ((m = itemRegex.exec(shortsHtml)) !== null) {
    const id = m[1];
    if (seen.has(id)) continue;
    seen.add(id);
    const acc = m[2].replace(/\\"/g, '"').replace(/\\u0026/g, "&");
    const vm = acc.match(/^(.*),\s*(No views|[\d.,]+\s*[KMBkmb]?\s*views?)\s*-\s*play Short$/i);
    const title = vm ? vm[1].trim() : acc.replace(/\s*-\s*play Short$/i, "");
    const viewsText = vm ? vm[2].trim() : "0 views";
    shorts.push({ id, title, viewsText, views: parseViewNum(viewsText) });
  }

  if (shorts.length === 0) {
    while ((m = itemRegex.exec(aboutHtml)) !== null) {
      const id = m[1];
      if (seen.has(id)) continue;
      seen.add(id);
      const acc = m[2].replace(/\\"/g, '"').replace(/\\u0026/g, "&");
      const vm = acc.match(/^(.*),\s*(No views|[\d.,]+\s*[KMBkmb]?\s*views?)\s*-\s*play Short$/i);
      const title = vm ? vm[1].trim() : acc.replace(/\s*-\s*play Short$/i, "");
      const viewsText = vm ? vm[2].trim() : "0 views";
      shorts.push({ id, title, viewsText, views: parseViewNum(viewsText) });
    }
  }

  const sumViews = shorts.reduce((acc, s) => acc + s.views, 0);
  const topShort = shorts.reduce((best, s) => (!best || s.views > best.views ? s : best), null);
  const subscribers = subMatch ? subMatch[1] : "Unavailable";
  const channelTotalViews = viewsMatch ? viewsMatch[1] : `${sumViews} views`;

  return {
    subscribers,
    subscriberCount: parseViewNum(subscribers),
    channelTotalViews,
    channelTotalViewsCount: parseViewNum(channelTotalViews),
    sumShortsViews: sumViews,
    videoCount: vidsMatch ? vidsMatch[1] : `${shorts.length} videos`,
    shorts,
    topShort
  };
}

async function fetchGitHubQueue(env) {
  const ghHeaders = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "StickNation-Cloudflare-Bot"
  };
  if (env?.GH_TOKEN) {
    ghHeaders["Authorization"] = `Bearer ${env.GH_TOKEN}`;
  }
  const rawBust = Date.now();
  const [histRes, queueRes, pyRes, vidsRes, runsRes, commitsRes] = await Promise.all([
    fetch(`https://raw.githubusercontent.com/${GH_REPO}/main/uploaded_history.json?t=${rawBust}`),
    fetch(`https://raw.githubusercontent.com/${GH_REPO}/main/cloud_queue.json?t=${rawBust}`),
    fetch(`https://raw.githubusercontent.com/${GH_REPO}/main/upload_to_youtube.py?t=${rawBust}`),
    fetch(`https://api.github.com/repos/${GH_REPO}/contents/videos`, { headers: ghHeaders }),
    fetch(`https://api.github.com/repos/${GH_REPO}/actions/runs?per_page=8`, { headers: ghHeaders }),
    fetch(`https://api.github.com/repos/${GH_REPO}/commits?per_page=8`, { headers: ghHeaders })
  ]);

  const uploaded = histRes.ok ? await histRes.json() : [];
  const cloudQueue = queueRes.ok ? await queueRes.json() : [];
  const pyText = pyRes.ok ? await pyRes.text() : "";
  const videoFiles = vidsRes.ok ? (await vidsRes.json()).map(f => f.name) : [];
  const runsJson = runsRes.ok ? await runsRes.json() : {};
  const lastRun = runsJson.workflow_runs?.[0] || null;

  const seenIds = new Set();
  const queueItems = [];
  const blockRegex = /\{\s*"id":\s*"([^"]+)"[\s\S]*?"filenames":\s*\[([^\]]+)\][\s\S]*?"title":\s*"([^"]+)"/g;
  let bm;
  while ((bm = blockRegex.exec(pyText)) !== null) {
    const id = bm[1];
    seenIds.add(id);
    const files = [...bm[2].matchAll(/"([^"]+)"/g)].map(x => x[1]);
    queueItems.push({ id, files, title: bm[3], isUploaded: uploaded.includes(id), hasFile: files.some(fn => videoFiles.includes(fn)) });
  }
  for (const q of (Array.isArray(cloudQueue) ? cloudQueue : [])) {
    if (!q?.id || seenIds.has(q.id)) continue;
    seenIds.add(q.id);
    const files = q.filenames || [];
    queueItems.push({ id: q.id, files, title: q.title, isUploaded: uploaded.includes(q.id), hasFile: files.some(fn => videoFiles.includes(fn)) });
  }

  const readyOnDeck = queueItems.filter(q => !q.isUploaded && q.hasFile);
  const pendingRender = queueItems.filter(q => !q.isUploaded && !q.hasFile);

  const commitsRaw = commitsRes.ok ? await commitsRes.json() : [];
  const commits = Array.isArray(commitsRaw) ? commitsRaw.slice(0, 8).map(c => ({
    sha: (c.sha || "").slice(0, 7),
    msg: (c.commit?.message || "").split("\n")[0],
    date: c.commit?.author?.date || ""
  })) : [];
  return { uploaded, readyOnDeck, pendingRender, lastRun, runs: (runsJson.workflow_runs || []).slice(0, 8), commits };
}

function buildDashHtml(yt, gh) {
  let msg = `📊 <b>STICKNATION LIVE CHANNEL DASHBOARD</b>\n`;
  msg += `━━━━━━━━━━━━━━━━━━━━━━\n`;
  msg += `👤 <b>Channel:</b> <a href="https://youtube.com/@StickNationDaily">@StickNationDaily</a>\n`;
  msg += `👥 <b>Subscribers:</b> <code>${esc(yt.subscribers)}</code> (Goal 1: 500 | Full YPP: 1,000)\n`;
  msg += `👀 <b>Official Total Views:</b> <code>${esc(yt.channelTotalViews)}</code>`;
  if (yt.sumShortsViews > 0) {
    msg += ` (Live Shorts sum: <code>${yt.sumShortsViews.toLocaleString()}</code>)`;
  }
  msg += `\n🎬 <b>Total Videos:</b> <code>${esc(yt.videoCount)}</code>\n`;
  if (yt.topShort) {
    msg += `🔥 <b>Top Performer:</b> <a href="https://youtube.com/shorts/${yt.topShort.id}">${esc(yt.topShort.title)}</a> (<code>${esc(yt.topShort.viewsText)}</code>)\n`;
  }
  msg += `\n🚀 <b>Cloud Queue (${gh.readyOnDeck.length} Ready on Deck):</b>\n`;
  gh.readyOnDeck.forEach((q, i) => {
    msg += `• Next #${i + 1}: <b>${esc(q.title)}</b>\n`;
  });
  return msg;
}

export { buildWebDashboardHtml, parseViewNum };

export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      const url = new URL(request.url);
      if (url.searchParams.get("check") === "live") {
        const [yt, gh] = await Promise.all([fetchYouTubeLive(), fetchGitHubQueue(env)]);
        return new Response(JSON.stringify({ yt, gh }, null, 2), {
          status: 200,
          headers: { "Content-Type": "application/json" }
        });
      }
      return new Response(buildWebDashboardHtml(), { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
    }

    const botToken = env?.BOT_TOKEN || "";
    const allowedChatId = Number(env?.ALLOWED_CHAT_ID || 6236827164);
    if (!botToken) {
      return new Response("Missing BOT_TOKEN secret", { status: 500 });
    }

    try {
      const update = await request.json();
      if (!update.message || !update.message.text) {
        return new Response("OK", { status: 200 });
      }
      const chatId = update.message.chat.id;
      if (chatId !== allowedChatId) {
        return new Response("Unauthorized", { status: 200 });
      }

      const lower = update.message.text.trim().toLowerCase();
      let replyHtml = "";

      if (lower.startsWith("/dash") || lower === "dash") {
        const [yt, gh] = await Promise.all([fetchYouTubeLive(), fetchGitHubQueue(env)]);
        replyHtml = buildDashHtml(yt, gh);
      } else if (lower.startsWith("/status") || lower === "status") {
        const gh = await fetchGitHubQueue(env);
        const runStatus = gh.lastRun ? `${gh.lastRun.status} (${gh.lastRun.conclusion || "running"})` : "unknown";
        replyHtml = `🟢 <b>24/7 CLOUD SYSTEM: ONLINE</b>\n` +
          `• <b>Published:</b> <code>${gh.uploaded.length}</code>\n` +
          `• <b>Ready on Deck:</b> <code>${gh.readyOnDeck.length} Shorts</code>\n` +
          `• <b>Last GitHub Action:</b> <code>${esc(runStatus)}</code>`;
      } else if (lower.startsWith("/videos") || lower === "videos") {
        const yt = await fetchYouTubeLive();
        replyHtml = `🎥 <b>LIVE YOUTUBE SHORTS (${esc(yt.subscribers)} | ${esc(yt.channelTotalViews)})</b>\n` +
          yt.shorts.map((s, i) => `${i + 1}. <a href="https://youtube.com/shorts/${s.id}">${esc(s.title)}</a> — <b>${esc(s.viewsText)}</b>`).join("\n");
      } else if (lower.startsWith("/upload") || lower === "upload") {
        if (!env?.GH_TOKEN) {
          replyHtml = `⚠️ Configure Cloudflare secret <code>GH_TOKEN</code> before triggering dispatches.`;
        } else {
          const ghResp = await fetch(`https://api.github.com/repos/${GH_REPO}/actions/workflows/daily_shorts.yml/dispatches`, {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.GH_TOKEN}`,
              "Accept": "application/vnd.github.v3+json",
              "User-Agent": "StickNation-Cloudflare-Bot"
            },
            body: JSON.stringify({ ref: "main" })
          });
          replyHtml = ghResp.status === 204
            ? `🚀 <b>Cloud Upload Dispatched to YouTube!</b>`
            : `⚠️ <b>GitHub Dispatch returned status ${ghResp.status}.</b>`;
        }
      } else {
        replyHtml = `🤖 <b>StickNation Cloud Assistant</b>\n• /dash\n• /videos\n• /status\n• /upload`;
      }

      await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text: replyHtml, parse_mode: "HTML", disable_web_page_preview: true })
      });
      return new Response("OK", { status: 200 });
    } catch (err) {
      await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: allowedChatId, text: `⚠️ Bot error: ${err.message}` })
      }).catch(() => {});
      return new Response("Error: " + err.message, { status: 200 });
    }
  }
};
