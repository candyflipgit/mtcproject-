def get_speedtest_html(coef, intercept):
    coef_str = str(coef)
    intercept_str = str(round(intercept, 8))

    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: linear-gradient(160deg, #0d0d1f 0%, #12122b 50%, #0d1f2d 100%);
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
}
.title {
  font-size: 1.1em;
  font-weight: 300;
  letter-spacing: 4px;
  color: #7788cc;
  margin-bottom: 4px;
  text-transform: uppercase;
}
.subtitle {
  font-size: 0.68em;
  color: #444466;
  letter-spacing: 2px;
  margin-bottom: 20px;
}
.gauge-wrap {
  position: relative;
  width: 240px;
  height: 240px;
}
.speed-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.speed-number {
  font-size: 2.8em;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
  letter-spacing: -1px;
  min-width: 120px;
  display: inline-block;
}
.speed-unit { font-size: 0.75em; color: #6677aa; letter-spacing: 3px; margin-top: 2px; }
.phase-label { font-size: 0.65em; color: #5566ff; letter-spacing: 2px; margin-top: 6px; text-transform: uppercase; }

.metrics {
  display: flex;
  gap: 36px;
  margin: 16px 0 8px;
  justify-content: center;
}
.metric { text-align: center; }
.metric-value { font-size: 1.3em; font-weight: 600; color: #55ddff; }
.metric-label { font-size: 0.62em; color: #555577; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

.progress-wrap {
  width: 280px;
  height: 3px;
  background: #1a1a33;
  border-radius: 2px;
  margin: 10px auto;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #5533ff, #33aaff);
  width: 0%;
  transition: width 0.4s ease;
  border-radius: 2px;
}

.phases {
  display: flex;
  gap: 8px;
  margin: 10px 0 4px;
  justify-content: center;
  align-items: center;
}
.phase-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.phase-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #1e1e3a;
  border: 1px solid #2a2a4a;
  transition: all 0.4s;
}
.phase-dot.active {
  background: #5533ff;
  border-color: #5533ff;
  box-shadow: 0 0 8px #5533ff;
}
.phase-dot.done {
  background: #33ffaa;
  border-color: #33ffaa;
}
.phase-name { font-size: 0.55em; color: #333355; letter-spacing: 1px; text-transform: uppercase; }
.phase-sep { width: 20px; height: 1px; background: #1e1e3a; margin-bottom: 10px; }

.start-btn {
  background: linear-gradient(135deg, #5533ff 0%, #33aaff 100%);
  border: none;
  color: white;
  padding: 14px 54px;
  font-size: 0.95em;
  border-radius: 40px;
  cursor: pointer;
  letter-spacing: 3px;
  margin: 18px 0 10px;
  text-transform: uppercase;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(85, 51, 255, 0.3);
}
.start-btn:hover:not(:disabled) {
  transform: scale(1.04);
  box-shadow: 0 6px 28px rgba(85, 51, 255, 0.5);
}
.start-btn:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }

.results-panel {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 18px 26px;
  margin-top: 16px;
  width: 340px;
  display: none;
  animation: fadeIn 0.5s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.results-title {
  font-size: 0.65em;
  color: #444466;
  letter-spacing: 3px;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 14px;
}
.result-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 9px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.result-row:last-of-type { border-bottom: none; }
.result-label { color: #555577; font-size: 0.8em; }
.result-value { font-weight: 600; color: #44ffcc; font-size: 0.9em; }

.quality-badge {
  text-align: center;
  padding: 10px;
  border-radius: 10px;
  margin-top: 14px;
  font-size: 1.05em;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
}
.q-excellent { background: rgba(50,220,100,0.12); color: #44ee88; border: 1px solid rgba(50,220,100,0.3); }
.q-good      { background: rgba(255,190,0,0.12);  color: #ffcc33; border: 1px solid rgba(255,190,0,0.3); }
.q-poor      { background: rgba(255,80,80,0.12);  color: #ff6666; border: 1px solid rgba(255,80,80,0.3); }

.signal-section { text-align: center; margin-top: 14px; }
.signal-label { font-size: 0.6em; color: #333355; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.signal-bars { display: flex; gap: 4px; align-items: flex-end; height: 32px; justify-content: center; }
.sig-bar { width: 10px; border-radius: 3px; background: #1a1a33; transition: background 0.5s, box-shadow 0.5s; }
.sig-bar.lit { background: linear-gradient(180deg, #33aaff, #5533ff); box-shadow: 0 0 6px rgba(51,170,255,0.4); }

.error-msg { color: #ff6666; font-size: 0.75em; text-align: center; margin-top: 8px; display: none; }
</style>
</head>
<body>

<div class="title">Network Channel Analyser</div>
<div class="subtitle">Mini ML Model &nbsp;·&nbsp; MTC Project 10</div>

<!-- SVG Gauge -->
<div class="gauge-wrap">
  <svg width="240" height="240" viewBox="0 0 240 240" style="position:absolute;top:0;left:0;">
    <defs>
      <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%"   style="stop-color:#5533ff;stop-opacity:1"/>
        <stop offset="100%" style="stop-color:#33aaff;stop-opacity:1"/>
      </linearGradient>
    </defs>
    <path id="arc-bg" stroke="#1a1a33" stroke-width="14" fill="none" stroke-linecap="round"/>
    <path id="arc-fill" stroke="url(#arcGrad)" stroke-width="14" fill="none"
          stroke-linecap="round" stroke-dasharray="0 1000"/>
  </svg>
  <div class="speed-display">
    <div class="speed-number" id="spd-num">—</div>
    <div class="speed-unit">Mbps</div>
    <div class="phase-label" id="phase-lbl">READY</div>
  </div>
</div>

<!-- Phase indicators -->
<div class="phases">
  <div class="phase-step"><div class="phase-dot" id="d-ping"></div><div class="phase-name">Ping</div></div>
  <div class="phase-sep"></div>
  <div class="phase-step"><div class="phase-dot" id="d-dl"></div><div class="phase-name">Down</div></div>
  <div class="phase-sep"></div>
  <div class="phase-step"><div class="phase-dot" id="d-ul"></div><div class="phase-name">Up</div></div>
  <div class="phase-sep"></div>
  <div class="phase-step"><div class="phase-dot" id="d-done"></div><div class="phase-name">Done</div></div>
</div>

<!-- Progress bar -->
<div class="progress-wrap"><div class="progress-fill" id="prog"></div></div>

<!-- Live metrics -->
<div class="metrics">
  <div class="metric"><div class="metric-value" id="m-ping">—</div><div class="metric-label">Ping ms</div></div>
  <div class="metric"><div class="metric-value" id="m-dl">—</div><div class="metric-label">Download</div></div>
  <div class="metric"><div class="metric-value" id="m-ul">—</div><div class="metric-label">Upload</div></div>
</div>

<button class="start-btn" id="start-btn" onclick="startTest()">Start Test</button>
<div class="error-msg" id="err-msg">Could not reach speed server. Check your connection.</div>

<!-- Results panel -->
<div class="results-panel" id="results-panel">
  <div class="results-title">Channel Analysis · ML Prediction</div>
  <div class="result-row"><span class="result-label">Estimated SNR</span><span class="result-value" id="r-snr">—</span></div>
  <div class="result-row"><span class="result-label">Predicted BER</span><span class="result-value" id="r-ber">—</span></div>
  <div class="result-row"><span class="result-label">TX Power Est.</span><span class="result-value" id="r-txp">—</span></div>
  <div class="result-row"><span class="result-label">Frequency Band</span><span class="result-value" id="r-freq">—</span></div>
  <div class="quality-badge" id="q-badge">—</div>
  <div class="signal-section">
    <div class="signal-label">Signal Strength</div>
    <div class="signal-bars">
      <div class="sig-bar" id="b1" style="height:7px"></div>
      <div class="sig-bar" id="b2" style="height:12px"></div>
      <div class="sig-bar" id="b3" style="height:18px"></div>
      <div class="sig-bar" id="b4" style="height:24px"></div>
      <div class="sig-bar" id="b5" style="height:30px"></div>
    </div>
  </div>
</div>

<script>
// ML coefficients pre-computed in Python
// Features order: [SNR_dB, Distance_km, TX_Power_mW, Frequency_GHz]
const COEF = __COEF__;
const INTERCEPT = __INTERCEPT__;

// ── Gauge ──────────────────────────────────────────────────────────────────────
const CX = 120, CY = 120, R = 100;
const A_START = 215, A_SWEEP = 290; // degrees

function toRad(deg) { return (deg - 90) * Math.PI / 180; }
function pt(angle, r) {
  const rad = toRad(angle);
  return [CX + r * Math.cos(rad), CY + r * Math.sin(rad)];
}
function arcD(start, sweep, r) {
  if (sweep <= 0) return '';
  const [sx, sy] = pt(start, r);
  const end = start + sweep;
  const [ex, ey] = pt(end, r);
  const large = sweep > 180 ? 1 : 0;
  return `M ${sx.toFixed(2)} ${sy.toFixed(2)} A ${r} ${r} 0 ${large} 1 ${ex.toFixed(2)} ${ey.toFixed(2)}`;
}

document.getElementById('arc-bg').setAttribute('d', arcD(A_START, A_SWEEP, R));

function setGauge(mbps, maxMbps) {
  const pct = Math.min(Math.max(mbps / maxMbps, 0), 1);
  const d = arcD(A_START, A_SWEEP * pct, R);
  document.getElementById('arc-fill').setAttribute('d', d || '');
}

// ── Helpers ────────────────────────────────────────────────────────────────────
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function dot(id, state) {
  const el = document.getElementById(id);
  el.className = 'phase-dot' + (state ? ' ' + state : '');
}
function prog(pct) { document.getElementById('prog').style.width = pct + '%'; }
function numEl(id) { return document.getElementById(id); }

function animNum(el, to, decimals, suffix, ms) {
  const from = parseFloat(el.textContent) || 0;
  const t0 = performance.now();
  function step(now) {
    const p = Math.min((now - t0) / ms, 1);
    el.textContent = (from + (to - from) * p).toFixed(decimals) + (suffix || '');
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ── Speed Test Core ────────────────────────────────────────────────────────────
const CF_SMALL = 'https://speed.cloudflare.com/__down?bytes=100&nocache=';
const CF_DOWN  = 'https://speed.cloudflare.com/__down?bytes=30000000&nocache=';
const CF_UP    = 'https://speed.cloudflare.com/__up';

async function measurePing() {
  const times = [];
  for (let i = 0; i < 10; i++) {
    const t0 = performance.now();
    await fetch(CF_SMALL + Math.random(), { cache: 'no-store' });
    times.push(performance.now() - t0);
    await sleep(150);
  }
  times.sort((a, b) => a - b);
  const trimmed = times.slice(2, 8);
  return trimmed.reduce((a, b) => a + b, 0) / trimmed.length;
}

async function measureDownload(onProgress) {
  const t0 = performance.now();
  const resp = await fetch(CF_DOWN + Math.random(), { cache: 'no-store' });
  const reader = resp.body.getReader();
  let loaded = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    loaded += value.length;
    const elapsed = (performance.now() - t0) / 1000;
    if (elapsed > 0.1) onProgress(loaded * 8 / elapsed / 1e6, elapsed);
  }
  const elapsed = (performance.now() - t0) / 1000;
  return loaded * 8 / elapsed / 1e6;
}

async function measureUpload(onProgress) {
  const SIZE = 8 * 1024 * 1024; // 8 MB
  const data = new Uint8Array(SIZE);
  // fill first chunk randomly
  crypto.getRandomValues(data.subarray(0, Math.min(65536, SIZE)));
  const blob = new Blob([data]);
  const t0 = performance.now();
  try {
    await fetch(CF_UP, { method: 'POST', body: blob, cache: 'no-store' });
  } catch (_) {}
  const elapsed = (performance.now() - t0) / 1000;
  const speed = elapsed > 0 ? (SIZE * 8 / elapsed / 1e6) : 0;
  // animate the display during upload (post-hoc since we can't stream POST progress)
  for (let i = 0; i <= 12; i++) {
    onProgress(speed * (i / 12), elapsed * (i / 12));
    await sleep(80);
  }
  return speed;
}

// ── ML Prediction ──────────────────────────────────────────────────────────────
function mapToCommParams(dlMbps, ulMbps, pingMs) {
  // Map real network metrics to communication channel parameters
  const snr      = Math.min(30, Math.max(0, dlMbps * 30 / 100));   // 0-100 Mbps → 0-30 dB
  const distance = Math.min(10, Math.max(0.1, pingMs / 50));        // ping → distance proxy
  const txPower  = Math.min(100, Math.max(10, ulMbps * 1.8 + 10)); // upload → TX power
  const freq     = 2.4;                                              // typical WiFi band
  return { snr, distance, txPower, freq };
}

function predictBER(snr, distance, txPower, freq) {
  const raw = INTERCEPT + COEF[0]*snr + COEF[1]*distance + COEF[2]*txPower + COEF[3]*freq;
  return Math.max(0, raw);
}

// ── Main Flow ─────────────────────────────────────────────────────────────────
let running = false;

async function startTest() {
  if (running) return;
  running = true;
  const btn = document.getElementById('start-btn');
  const errEl = document.getElementById('err-msg');
  btn.disabled = true;
  btn.textContent = 'Testing…';
  errEl.style.display = 'none';
  document.getElementById('results-panel').style.display = 'none';

  // reset
  ['m-ping','m-dl','m-ul'].forEach(id => numEl(id).textContent = '—');
  numEl('spd-num').textContent = '0';
  ['d-ping','d-dl','d-ul','d-done'].forEach(id => dot(id, ''));
  prog(0);
  setGauge(0, 100);

  try {
    // ── Ping phase ────────────────────────────────────────────────────────────
    dot('d-ping', 'active');
    numEl('phase-lbl').textContent = 'MEASURING PING';
    numEl('spd-num').textContent = '…';

    let pingMs = 999;
    try { pingMs = await measurePing(); } catch (_) {}
    numEl('m-ping').textContent = pingMs.toFixed(0);
    dot('d-ping', 'done');
    prog(20);
    await sleep(300);

    // ── Download phase ────────────────────────────────────────────────────────
    dot('d-dl', 'active');
    numEl('phase-lbl').textContent = 'DOWNLOAD';
    numEl('spd-num').textContent = '0.0';
    setGauge(0, 100);

    let dlMbps = 0;
    try {
      dlMbps = await measureDownload((speed, elapsed) => {
        const s = speed.toFixed(1);
        numEl('spd-num').textContent = s;
        numEl('m-dl').textContent = s + ' Mbps';
        setGauge(speed, 100);
        prog(Math.min(65, 20 + (elapsed / 14) * 45));
      });
    } catch (_) {}

    numEl('m-dl').textContent = dlMbps.toFixed(1) + ' Mbps';
    dot('d-dl', 'done');
    prog(65);
    setGauge(0, 50);
    await sleep(300);

    // ── Upload phase ──────────────────────────────────────────────────────────
    dot('d-ul', 'active');
    numEl('phase-lbl').textContent = 'UPLOAD';
    numEl('spd-num').textContent = '0.0';

    let ulMbps = 0;
    try {
      ulMbps = await measureUpload((speed, elapsed) => {
        const s = speed.toFixed(1);
        numEl('spd-num').textContent = s;
        numEl('m-ul').textContent = s + ' Mbps';
        setGauge(speed, 50);
        prog(Math.min(95, 65 + (elapsed / 3) * 30));
      });
    } catch (_) {
      ulMbps = dlMbps * 0.25; // fallback estimate
      numEl('m-ul').textContent = ulMbps.toFixed(1) + ' Mbps';
    }

    dot('d-ul', 'done');
    dot('d-done', 'done');
    prog(100);
    await sleep(300);

    // ── Results ───────────────────────────────────────────────────────────────
    numEl('phase-lbl').textContent = 'COMPLETE';
    setGauge(dlMbps, 100);
    numEl('spd-num').textContent = dlMbps.toFixed(1);

    const p = mapToCommParams(dlMbps, ulMbps, pingMs);
    const ber = predictBER(p.snr, p.distance, p.txPower, p.freq);

    numEl('r-snr').textContent  = p.snr.toFixed(2) + ' dB';
    numEl('r-ber').textContent  = ber.toExponential(3);
    numEl('r-txp').textContent  = p.txPower.toFixed(1) + ' mW';
    numEl('r-freq').textContent = p.freq + ' GHz (WiFi)';

    // Quality thresholds
    let label, cls, bars;
    if (dlMbps >= 25 && pingMs < 60) {
      label = 'EXCELLENT'; cls = 'q-excellent'; bars = 5;
    } else if (dlMbps >= 10 && pingMs < 150) {
      label = 'GOOD';      cls = 'q-good';      bars = 3;
    } else {
      label = 'POOR';      cls = 'q-poor';      bars = 1;
    }
    const badge = document.getElementById('q-badge');
    badge.textContent = label;
    badge.className = 'quality-badge ' + cls;

    for (let i = 1; i <= 5; i++) {
      document.getElementById('b' + i).className = 'sig-bar' + (i <= bars ? ' lit' : '');
    }

    document.getElementById('results-panel').style.display = 'block';

  } catch (err) {
    errEl.style.display = 'block';
    numEl('phase-lbl').textContent = 'ERROR';
  }

  btn.disabled = false;
  btn.textContent = 'Run Again';
  running = false;
}
</script>
</body>
</html>
""".replace('__COEF__', coef_str).replace('__INTERCEPT__', intercept_str)
