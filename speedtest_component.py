def get_speedtest_html(coef, intercept, means, stds):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:linear-gradient(160deg,#0b0b1e 0%,#111228 60%,#0c1a22 100%);
  color:#fff;font-family:'Segoe UI',sans-serif;
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;padding:18px 12px 30px;
}

/* ── Info Bar ── */
.info-bar{
  display:flex;flex-wrap:wrap;gap:6px 14px;
  justify-content:center;align-items:center;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:30px;padding:7px 18px;
  margin-bottom:16px;width:100%;max-width:600px;
  font-size:0.72em;color:#6677aa;
}
.info-pill{display:flex;align-items:center;gap:5px;}
.info-pill .lbl{color:#333355;}
.info-pill .val{color:#8899cc;font-weight:600;}

/* ── Title ── */
.title{font-size:1.05em;font-weight:300;letter-spacing:4px;color:#6677bb;text-transform:uppercase;}
.subtitle{font-size:0.65em;color:#333355;letter-spacing:2px;margin-bottom:16px;}

/* ── Gauge ── */
.gauge-wrap{position:relative;width:220px;height:220px;}
.gauge-wrap svg{position:absolute;top:0;left:0;}
.spd-display{
  position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);text-align:center;
}
.spd-num{font-size:2.6em;font-weight:700;line-height:1;letter-spacing:-1px;}
.spd-unit{font-size:0.72em;color:#556688;letter-spacing:3px;margin-top:2px;}
.phase-lbl{font-size:0.6em;color:#4455ff;letter-spacing:2px;margin-top:5px;text-transform:uppercase;}

/* ── Phases ── */
.phases{display:flex;align-items:center;gap:0;margin:12px 0 4px;}
.ph-step{display:flex;flex-direction:column;align-items:center;gap:3px;}
.ph-dot{
  width:8px;height:8px;border-radius:50%;
  background:#111133;border:1px solid #222244;
  transition:all .4s;
}
.ph-dot.active{background:#5533ff;border-color:#5533ff;box-shadow:0 0 8px #5533ff;}
.ph-dot.done{background:#33ffaa;border-color:#33ffaa;}
.ph-name{font-size:0.55em;color:#2a2a44;letter-spacing:1px;text-transform:uppercase;}
.ph-line{width:22px;height:1px;background:#1a1a33;margin-bottom:11px;}

/* ── Progress ── */
.prog-wrap{width:270px;height:3px;background:#111133;border-radius:2px;margin:8px auto;overflow:hidden;}
.prog-fill{height:100%;background:linear-gradient(90deg,#5533ff,#33aaff);width:0%;transition:width .4s ease;border-radius:2px;}

/* ── Metrics ── */
.metrics{display:flex;gap:32px;margin:10px 0 6px;justify-content:center;}
.metric{text-align:center;}
.metric .val{font-size:1.25em;font-weight:600;color:#44ccff;}
.metric .lbl{font-size:0.6em;color:#333355;letter-spacing:1px;text-transform:uppercase;margin-top:2px;}

/* ── Button ── */
.start-btn{
  background:linear-gradient(135deg,#5533ff,#33aaff);
  border:none;color:#fff;padding:13px 52px;
  font-size:0.9em;border-radius:40px;cursor:pointer;
  letter-spacing:3px;margin:14px 0 8px;text-transform:uppercase;font-weight:600;
  transition:all .3s;box-shadow:0 4px 18px rgba(85,51,255,.3);
}
.start-btn:hover:not(:disabled){transform:scale(1.04);box-shadow:0 6px 26px rgba(85,51,255,.5);}
.start-btn:disabled{opacity:.4;cursor:not-allowed;transform:none;}
.err-msg{color:#ff6666;font-size:0.72em;text-align:center;margin-top:6px;display:none;}

/* ── Results ── */
.results-wrap{width:100%;max-width:620px;margin-top:18px;animation:fadeUp .5s ease;}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

/* Narrative card */
.narrative-card{
  background:rgba(85,51,255,0.08);
  border:1px solid rgba(85,51,255,0.2);
  border-radius:14px;padding:14px 18px;
  font-size:0.82em;line-height:1.6;color:#aabbdd;
  margin-bottom:14px;
}
.narrative-card strong{color:#99bbff;}

/* Charts row */
.charts-row{display:flex;gap:12px;margin-bottom:14px;}
.chart-card{
  flex:1;background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:12px;padding:12px;
}
.chart-title{font-size:0.65em;color:#445566;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.chart-stat{font-size:0.7em;color:#556677;margin-top:6px;text-align:center;}
.chart-stat span{color:#44ddaa;font-weight:600;}

/* Feature table */
.feat-section{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:12px;padding:12px 14px;margin-bottom:14px;
}
.feat-title{font-size:0.65em;color:#445566;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;}
.feat-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:6px;}
.feat-row{
  display:flex;justify-content:space-between;align-items:center;
  padding:5px 8px;background:rgba(255,255,255,0.03);border-radius:7px;
}
.feat-row .fn{font-size:0.72em;color:#445566;}
.feat-row .fv{font-size:0.75em;color:#55ddbb;font-weight:600;}

/* Prediction card */
.pred-card{
  background:linear-gradient(135deg,rgba(85,51,255,0.12),rgba(51,170,255,0.12));
  border:1px solid rgba(85,51,255,0.25);
  border-radius:14px;padding:16px 20px;
  text-align:center;margin-bottom:14px;
}
.pred-label{font-size:0.65em;color:#6677aa;letter-spacing:3px;text-transform:uppercase;}
.pred-value{font-size:2.2em;font-weight:700;color:#fff;margin:6px 0 2px;}
.pred-sub{font-size:0.78em;color:#7788aa;}
.eff-bar-wrap{width:100%;height:6px;background:#111133;border-radius:3px;margin:10px 0 4px;overflow:hidden;}
.eff-bar-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,#5533ff,#33ffaa);transition:width 1s ease;}
.eff-pct{font-size:0.75em;color:#556677;}

/* Use cases */
.uc-title{font-size:0.65em;color:#445566;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.uc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.uc-item{
  padding:9px 6px;border-radius:10px;text-align:center;
  font-size:0.72em;font-weight:600;letter-spacing:0.5px;
}
.uc-ok{background:rgba(50,220,100,0.1);color:#44ee88;border:1px solid rgba(50,220,100,0.2);}
.uc-warn{background:rgba(255,190,0,0.1);color:#ffcc33;border:1px solid rgba(255,190,0,0.2);}
.uc-fail{background:rgba(255,80,80,0.1);color:#ff6666;border:1px solid rgba(255,80,80,0.2);}
.uc-icon{font-size:1.3em;display:block;margin-bottom:3px;}

canvas{width:100%;height:140px;display:block;}
</style>
</head>
<body>

<!-- Info bar -->
<div class="info-bar" id="info-bar">
  <div class="info-pill"><span class="lbl">ISP</span><span class="val" id="ib-isp">Detecting…</span></div>
  <div class="info-pill"><span class="lbl">OS</span><span class="val" id="ib-os">…</span></div>
  <div class="info-pill"><span class="lbl">RAM</span><span class="val" id="ib-ram">…</span></div>
  <div class="info-pill"><span class="lbl">Cores</span><span class="val" id="ib-cores">…</span></div>
  <div class="info-pill"><span class="lbl">Link</span><span class="val" id="ib-conn">…</span></div>
</div>

<div class="title">Network Channel Analyser</div>
<div class="subtitle">MTC Project 10 &nbsp;·&nbsp; ML-Powered Speed Analysis</div>

<!-- Gauge -->
<div class="gauge-wrap">
  <svg width="220" height="220" viewBox="0 0 220 220">
    <defs>
      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#5533ff"/>
        <stop offset="100%" style="stop-color:#33aaff"/>
      </linearGradient>
    </defs>
    <path id="arc-bg"   stroke="#111133" stroke-width="13" fill="none" stroke-linecap="round"/>
    <path id="arc-fill" stroke="url(#g1)" stroke-width="13" fill="none"
          stroke-linecap="round" stroke-dasharray="0 1000"/>
  </svg>
  <div class="spd-display">
    <div class="spd-num" id="spd-num">—</div>
    <div class="spd-unit">Mbps</div>
    <div class="phase-lbl" id="phase-lbl">READY</div>
  </div>
</div>

<!-- Phase indicators -->
<div class="phases">
  <div class="ph-step"><div class="ph-dot" id="d-ping"></div><div class="ph-name">Ping</div></div>
  <div class="ph-line"></div>
  <div class="ph-step"><div class="ph-dot" id="d-dl"></div><div class="ph-name">Down</div></div>
  <div class="ph-line"></div>
  <div class="ph-step"><div class="ph-dot" id="d-ul"></div><div class="ph-name">Up</div></div>
  <div class="ph-line"></div>
  <div class="ph-step"><div class="ph-dot" id="d-done"></div><div class="ph-name">ML</div></div>
</div>

<div class="prog-wrap"><div class="prog-fill" id="prog"></div></div>

<div class="metrics">
  <div class="metric"><div class="val" id="m-ping">—</div><div class="lbl">Ping ms</div></div>
  <div class="metric"><div class="val" id="m-dl">—</div><div class="lbl">Download</div></div>
  <div class="metric"><div class="val" id="m-ul">—</div><div class="lbl">Upload</div></div>
</div>

<button class="start-btn" id="start-btn" onclick="startTest()">Start Test</button>
<div class="err-msg" id="err-msg">Could not reach test server. Check connection.</div>

<!-- Results (hidden until test done) -->
<div class="results-wrap" id="results-wrap" style="display:none">

  <!-- Narrative -->
  <div class="narrative-card" id="narrative-card">…</div>

  <!-- Charts -->
  <div class="charts-row">
    <div class="chart-card">
      <div class="chart-title">Download Speed Over Time</div>
      <canvas id="chart-speed" width="280" height="140"></canvas>
      <div class="chart-stat" id="stab-stat">Stability: <span>—</span></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">Loaded Ping vs Speed (Correlation)</div>
      <canvas id="chart-corr" width="280" height="140"></canvas>
      <div class="chart-stat" id="corr-stat">Pearson r: <span>—</span></div>
    </div>
  </div>

  <!-- Feature table -->
  <div class="feat-section">
    <div class="feat-title">Feature Vector extracted (fed to ML model)</div>
    <div class="feat-grid" id="feat-grid"></div>
  </div>

  <!-- ML Prediction -->
  <div class="pred-card">
    <div class="pred-label">ML Predicted Effective Throughput</div>
    <div class="pred-value" id="pred-val">— Mbps</div>
    <div class="pred-sub" id="pred-sub">—</div>
    <div class="eff-bar-wrap"><div class="eff-bar-fill" id="eff-bar" style="width:0%"></div></div>
    <div class="eff-pct" id="eff-pct">—</div>
  </div>

  <!-- Use cases -->
  <div class="uc-title">What your connection supports</div>
  <div class="uc-grid" id="uc-grid"></div>

</div>

<script>
// ── ML model params (injected from Python) ─────────────────────────────────────
const COEF      = __COEF__;
const INTERCEPT = __INTERCEPT__;
const MEANS     = __MEANS__;
const STDS      = __STDS__;
const FEAT_NAMES = [
  'Avg Download','Stability','Avg Ping','Ping Jitter',
  'Upload','DL/UL Ratio','Speed Trend','RAM (GB)','CPU Cores','Conn Score'
];

// ── Gauge ──────────────────────────────────────────────────────────────────────
const CX=110, CY=110, R=92, A_START=215, A_SWEEP=290;
function pt(a,r){const rad=(a-90)*Math.PI/180;return[CX+r*Math.cos(rad),CY+r*Math.sin(rad)];}
function arcD(s,sw,r){
  if(sw<=0)return '';
  const [sx,sy]=pt(s,r),[ex,ey]=pt(s+sw,r);
  return `M${sx.toFixed(1)} ${sy.toFixed(1)} A${r} ${r} 0 ${sw>180?1:0} 1 ${ex.toFixed(1)} ${ey.toFixed(1)}`;
}
document.getElementById('arc-bg').setAttribute('d',arcD(A_START,A_SWEEP,R));
function setGauge(mbps,max){
  document.getElementById('arc-fill').setAttribute('d',arcD(A_START,A_SWEEP*Math.min(mbps/max,1),R));
}

// ── Helpers ────────────────────────────────────────────────────────────────────
const $=id=>document.getElementById(id);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function dot(id,s){$('d-'+id).className='ph-dot'+(s?' '+s:'');}
function prog(p){$('prog').style.width=p+'%';}
function setNum(id,v,dec=1){$(id).textContent=typeof v==='number'?v.toFixed(dec):v;}

// ── Device info ────────────────────────────────────────────────────────────────
function getDeviceInfo(){
  const ua=navigator.userAgent;
  const os=/Windows/.test(ua)?'Windows':/Mac OS/.test(ua)?'macOS':/Android/.test(ua)?'Android':/iPhone|iPad/.test(ua)?'iOS':'Linux';
  const ram=navigator.deviceMemory||4;
  const cores=navigator.hardwareConcurrency||4;
  const connAPI=navigator.connection||navigator.mozConnection||navigator.webkitConnection;
  const connType=connAPI?(connAPI.type||'wifi'):'wifi';
  return{os,ram,cores,connType,connAPI};
}

function inferGHz(dlMbps,connType){
  if(connType==='ethernet')return 'Ethernet';
  if(connType==='cellular')return '4G/5G Cellular';
  if(dlMbps>150)return '5/6 GHz WiFi';
  if(dlMbps>60)return '5 GHz WiFi';
  if(dlMbps>20)return '2.4/5 GHz WiFi';
  return '2.4 GHz WiFi';
}

function connScore(connType,dlMbps){
  if(connType==='ethernet')return 1.0;
  if(connType==='cellular')return 0.3;
  return dlMbps>60?0.8:0.6;
}

// ── ISP detection ──────────────────────────────────────────────────────────────
async function fetchISP(){
  try{
    const r=await Promise.race([
      fetch('https://ipapi.co/json/',{cache:'no-store'}),
      new Promise((_,rj)=>setTimeout(()=>rj('timeout'),4000))
    ]);
    return await r.json();
  }catch(_){return null;}
}

// ── Stats helpers ──────────────────────────────────────────────────────────────
function mean(arr){return arr.length?arr.reduce((a,b)=>a+b,0)/arr.length:0;}
function std(arr){
  const m=mean(arr);
  return arr.length?Math.sqrt(arr.reduce((s,v)=>s+(v-m)**2,0)/arr.length):0;
}
function pearsonR(xs,ys){
  const n=Math.min(xs.length,ys.length);
  if(n<3)return null;
  const mx=mean(xs.slice(0,n)),my=mean(ys.slice(0,n));
  let num=0,dx2=0,dy2=0;
  for(let i=0;i<n;i++){num+=(xs[i]-mx)*(ys[i]-my);dx2+=(xs[i]-mx)**2;dy2+=(ys[i]-my)**2;}
  const denom=Math.sqrt(dx2*dy2);
  return denom>0?num/denom:0;
}
function linReg(xs,ys){
  const n=xs.length,mx=mean(xs),my=mean(ys);
  let num=0,den=0;
  for(let i=0;i<n;i++){num+=(xs[i]-mx)*(ys[i]-my);den+=(xs[i]-mx)**2;}
  const s=den?num/den:0,b=my-s*mx;
  return{slope:s,intercept:b};
}
function speedTrend(samples){
  if(samples.length<3)return 0;
  const xs=samples.map((_,i)=>i);
  const{slope}=linReg(xs,samples);
  const range=Math.max(...samples)-Math.min(...samples);
  return range>0?Math.max(-1,Math.min(1,slope/range*samples.length)):0;
}

// Remove outliers: keep values within [0.1×median, 4×median]
function cleanSamples(arr){
  if(arr.length<3)return arr;
  const sorted=[...arr].sort((a,b)=>a-b);
  const med=sorted[Math.floor(sorted.length/2)];
  if(med<=0)return arr;
  return arr.filter(v=>v>=med*0.1&&v<=med*4);
}

// ── ML prediction ──────────────────────────────────────────────────────────────
function predictEffective(featArr){
  const scaled=featArr.map((v,i)=>(v-MEANS[i])/STDS[i]);
  const p=INTERCEPT+scaled.reduce((s,v,i)=>s+v*COEF[i],0);
  const floor=featArr[0]*0.30;  // at least 30% of raw download (guards against extrapolation)
  return Math.max(floor,p);
}

// ── Canvas charts ──────────────────────────────────────────────────────────────
function drawLine(canvasId,data,color='#5533ff',yLabel='Mbps'){
  const cv=$(canvasId),ctx=cv.getContext('2d');
  const W=cv.clientWidth||cv.width,H=cv.clientHeight||cv.height;
  cv.width=W;cv.height=H;
  const pad={t:14,r:8,b:26,l:42};
  ctx.clearRect(0,0,W,H);
  if(data.length<2){
    ctx.fillStyle='#2a2a44';ctx.font='11px sans-serif';ctx.textAlign='center';
    ctx.fillText('Collecting data…',W/2,H/2);return;
  }
  const mx=Math.max(...data)*1.1||1,mn=0;
  const sx=i=>pad.l+(i/(data.length-1))*(W-pad.l-pad.r);
  const sy=v=>H-pad.b-((v-mn)/(mx-mn))*(H-pad.t-pad.b);
  // axes
  ctx.strokeStyle='#1e1e38';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(pad.l,pad.t);ctx.lineTo(pad.l,H-pad.b);ctx.lineTo(W-pad.r,H-pad.b);ctx.stroke();
  // grid
  [0.25,0.5,0.75,1].forEach(f=>{
    ctx.strokeStyle='#151528';ctx.lineWidth=1;ctx.setLineDash([2,4]);
    ctx.beginPath();ctx.moveTo(pad.l,sy(mx*f));ctx.lineTo(W-pad.r,sy(mx*f));ctx.stroke();
    ctx.fillStyle='#333355';ctx.font='9px sans-serif';ctx.textAlign='right';
    ctx.fillText((mx*f).toFixed(0),pad.l-3,sy(mx*f)+3);
  });
  ctx.setLineDash([]);
  // fill
  ctx.fillStyle=color+'18';
  ctx.beginPath();
  data.forEach((v,i)=>i?ctx.lineTo(sx(i),sy(v)):ctx.moveTo(sx(i),sy(v)));
  ctx.lineTo(sx(data.length-1),sy(0));ctx.lineTo(sx(0),sy(0));
  ctx.closePath();ctx.fill();
  // line
  ctx.strokeStyle=color;ctx.lineWidth=2;ctx.lineJoin='round';
  ctx.beginPath();
  data.forEach((v,i)=>i?ctx.lineTo(sx(i),sy(v)):ctx.moveTo(sx(i),sy(v)));
  ctx.stroke();
  // axis label
  ctx.fillStyle='#334455';ctx.font='9px sans-serif';ctx.textAlign='center';
  ctx.fillText('Time →',W/2,H-4);
}

function drawScatter(canvasId,pairs,color='#33aaff'){
  const cv=$(canvasId),ctx=cv.getContext('2d');
  const W=cv.clientWidth||cv.width,H=cv.clientHeight||cv.height;
  cv.width=W;cv.height=H;
  const pad={t:14,r:8,b:26,l:42};
  ctx.clearRect(0,0,W,H);
  if(!pairs||pairs.length<2){
    ctx.fillStyle='#2a2a44';ctx.font='11px sans-serif';ctx.textAlign='center';
    ctx.fillText('Need ≥ 2 data points',W/2,H/2);return;
  }
  const xs=pairs.map(p=>p.x),ys=pairs.map(p=>p.y);
  const mxX=Math.max(...xs)*1.1,mnX=Math.min(...xs)*0.9||0;
  const mxY=Math.max(...ys)*1.1||1,mnY=0;
  const sx=v=>pad.l+((v-mnX)/(mxX-mnX||1))*(W-pad.l-pad.r);
  const sy=v=>H-pad.b-((v-mnY)/(mxY-mnY||1))*(H-pad.t-pad.b);
  // axes
  ctx.strokeStyle='#1e1e38';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(pad.l,pad.t);ctx.lineTo(pad.l,H-pad.b);ctx.lineTo(W-pad.r,H-pad.b);ctx.stroke();
  // regression line
  const{slope,intercept}=linReg(xs,ys);
  ctx.strokeStyle='#ff444488';ctx.lineWidth=1;ctx.setLineDash([3,3]);
  ctx.beginPath();ctx.moveTo(sx(mnX),sy(slope*mnX+intercept));ctx.lineTo(sx(mxX),sy(slope*mxX+intercept));ctx.stroke();
  ctx.setLineDash([]);
  // points
  pairs.forEach(p=>{
    ctx.fillStyle=color;ctx.beginPath();ctx.arc(sx(p.x),sy(p.y),5,0,Math.PI*2);ctx.fill();
  });
  // axis labels
  ctx.fillStyle='#334455';ctx.font='9px sans-serif';ctx.textAlign='center';
  ctx.fillText('Loaded Ping (ms) →',W/2,H-4);
  ctx.save();ctx.translate(10,H/2);ctx.rotate(-Math.PI/2);ctx.fillText('Speed (Mbps)',0,0);ctx.restore();
  // axis ticks
  ctx.fillStyle='#333355';ctx.textAlign='center';
  [mnX,(mnX+mxX)/2,mxX].forEach(v=>{ctx.fillText(v.toFixed(0),sx(v),H-pad.b+12);});
}

// ── Speed test core ─────────────────────────────────────────────────────────────
const CF_TINY  = 'https://speed.cloudflare.com/__down?bytes=100&r=';
const CF_SMALL = 'https://speed.cloudflare.com/__down?bytes=3000000&r=';
const CF_DOWN  = 'https://speed.cloudflare.com/__down?bytes=50000000&r=';
const CF_UP    = 'https://speed.cloudflare.com/__up';

async function measurePing(){
  const times=[];
  for(let i=0;i<10;i++){
    const t=performance.now();
    await fetch(CF_TINY+Math.random(),{cache:'no-store'});
    times.push(performance.now()-t);
    await sleep(120);
  }
  times.sort((a,b)=>a-b);
  return{avg:mean(times.slice(2,8)),jitter:std(times.slice(2,8)),samples:times};
}

const speedSamples=[];
const loadedPingPairs=[];

async function measureDownload(onProgress){
  speedSamples.length=0;
  loadedPingPairs.length=0;
  const resp=await fetch(CF_DOWN+Math.random(),{cache:'no-store'});
  const reader=resp.body.getReader();
  let loaded=0;
  const t0=performance.now();
  let lastPing=t0-1200; // fire first loaded-ping after 1.2s

  while(true){
    const{done,value}=await reader.read();
    if(done)break;
    loaded+=value.length;
    const now=performance.now();
    const elapsed=(now-t0)/1000;
    // Skip first 0.5s warmup — avoids the near-zero division spike
    if(elapsed<0.5){onProgress(0,elapsed);continue;}
    const spd=loaded*8/elapsed/1e6;
    speedSamples.push(parseFloat(spd.toFixed(2)));
    onProgress(spd,elapsed);
    // Async loaded-ping every 1.5s
    if(now-lastPing>1500){
      lastPing=now;
      const pt0=performance.now();
      const snapLoaded=loaded,snapElap=elapsed;
      fetch(CF_TINY+Math.random(),{cache:'no-store'}).then(()=>{
        const pms=performance.now()-pt0;
        const spd2=snapLoaded*8/snapElap/1e6;
        loadedPingPairs.push({x:parseFloat(pms.toFixed(1)),y:parseFloat(spd2.toFixed(2))});
      });
    }
  }
  const elapsed=(performance.now()-t0)/1000;
  return loaded*8/elapsed/1e6;
}

// Fallback: run 5 short parallel (download + ping) rounds for correlation data
async function gatherCorrelationData(){
  for(let i=0;i<5;i++){
    const t0=performance.now();
    let pingMs=0;
    const pingP=fetch(CF_TINY+Math.random(),{cache:'no-store'})
      .then(()=>{pingMs=performance.now()-t0;});
    const dlP=fetch(CF_SMALL+Math.random(),{cache:'no-store'})
      .then(r=>r.arrayBuffer())
      .then(buf=>{
        const elapsed=(performance.now()-t0)/1000;
        return buf.byteLength*8/elapsed/1e6;
      }).catch(()=>0);
    const[,speed]=await Promise.all([pingP,dlP]);
    if(pingMs>0&&speed>0)
      loadedPingPairs.push({x:parseFloat(pingMs.toFixed(1)),y:parseFloat(speed.toFixed(2))});
    await sleep(300);
  }
}

async function measureUpload(onProgress){
  const SIZE=8*1024*1024;
  const data=new Uint8Array(SIZE);
  crypto.getRandomValues(data.subarray(0,Math.min(65536,SIZE)));
  const t0=performance.now();
  try{await fetch(CF_UP,{method:'POST',body:new Blob([data]),cache:'no-store'});}catch(_){}
  const elapsed=(performance.now()-t0)/1000;
  const spd=elapsed>0?(SIZE*8/elapsed/1e6):0;
  for(let i=0;i<=10;i++){onProgress(spd*(i/10));await sleep(70);}
  return spd;
}

// ── Render results ─────────────────────────────────────────────────────────────
function renderResults(dlMbps,ulMbps,pingAvg,pingJitter,device,ispName){
  // Clean outliers first
  const clean=cleanSamples(speedSamples);
  // Use only the last 60% of samples (steady-state phase, after TCP ramp-up)
  // This avoids counting the slow-start period as "instability"
  const steadySamples=clean.length>4?clean.slice(Math.floor(clean.length*0.4)):clean;
  const stability=steadySamples.length>1
    ?Math.max(0,Math.min(1,1-std(steadySamples)/mean(steadySamples)))
    :0.85;
  const dlUlRatio=dlMbps/Math.max(ulMbps,0.1);
  const trend=speedTrend(speedSamples);
  const cs=connScore(device.connType,dlMbps);
  const ghz=inferGHz(dlMbps,device.connType);

  // Feature vector
  const featVals=[
    parseFloat(dlMbps.toFixed(2)),
    parseFloat(stability.toFixed(3)),
    parseFloat(pingAvg.toFixed(1)),
    parseFloat(pingJitter.toFixed(1)),
    parseFloat(ulMbps.toFixed(2)),
    parseFloat(dlUlRatio.toFixed(2)),
    parseFloat(trend.toFixed(3)),
    device.ram,
    device.cores,
    cs
  ];
  const featDisplay=[
    dlMbps.toFixed(1)+' Mbps',
    (stability*100).toFixed(1)+'%',
    pingAvg.toFixed(1)+' ms',
    pingJitter.toFixed(1)+' ms',
    ulMbps.toFixed(1)+' Mbps',
    dlUlRatio.toFixed(2)+'x',
    (trend>=0?'+':'')+trend.toFixed(2),
    device.ram+' GB',
    device.cores,
    cs.toFixed(1)+' ('+ghz+')'
  ];

  // ML prediction
  const effMbps=Math.min(predictEffective(featVals),dlMbps*0.99);
  const effPct=(effMbps/dlMbps*100).toFixed(1);

  // Charts — use cleaned samples for display
  drawLine('chart-speed',clean.length>2?clean:speedSamples,'#5533ff');
  drawScatter('chart-corr',loadedPingPairs,'#33aaff');

  // Stability stat
  const peak=clean.length>0?Math.max(...clean):Math.max(...speedSamples);
  $('stab-stat').innerHTML='Stability: <span>'+(stability*100).toFixed(1)+'%</span>'
    +' &nbsp;|&nbsp; Peak: <span>'+peak.toFixed(1)+' Mbps</span>';

  // Correlation stat
  const r=pearsonR(loadedPingPairs.map(p=>p.x),loadedPingPairs.map(p=>p.y));
  if(r!==null){
    const rLabel=r<-0.5?'Strong negative':r<-0.2?'Moderate negative':'Weak';
    $('corr-stat').innerHTML='Pearson r: <span>'+r.toFixed(3)+'</span> &nbsp;('
      +rLabel+' — higher ping → '+(r<-0.2?'lower':'minimal effect on')+' speed)';
  } else {
    $('corr-stat').innerHTML='<span>Not enough loaded-ping pairs collected</span>';
  }

  // Feature grid
  const fg=$('feat-grid');fg.innerHTML='';
  FEAT_NAMES.forEach((n,i)=>{
    fg.innerHTML+=`<div class="feat-row"><span class="fn">${n}</span><span class="fv">${featDisplay[i]}</span></div>`;
  });

  // Prediction card
  $('pred-val').textContent=effMbps.toFixed(1)+' Mbps';
  $('pred-sub').textContent='from '+dlMbps.toFixed(1)+' Mbps raw download';
  $('eff-bar').style.width=effPct+'%';
  $('eff-pct').textContent=effPct+'% efficiency — '+(effPct>85?'Excellent':'effPct'>70?'Good':'Room for improvement');

  // Narrative
  $('narrative-card').innerHTML=
    'Based on your <strong>'+device.os+'</strong> device with '
    +'<strong>'+device.ram+'GB RAM</strong> &amp; <strong>'+device.cores+'-core CPU</strong>, '
    +'connected via <strong>'+ghz+'</strong> on '
    +'<strong>'+(ispName||'your ISP')+'</strong> — '
    +'with a download of <strong>'+dlMbps.toFixed(1)+'Mbps</strong>, '
    +'ping of <strong>'+pingAvg.toFixed(0)+'ms</strong>, '
    +'and jitter of <strong>'+pingJitter.toFixed(1)+'ms</strong>, '
    +'the ML model predicts your real-time effective throughput will be '
    +'<strong>'+effMbps.toFixed(1)+' Mbps</strong> ('+(stability*100).toFixed(0)+'% connection stability).';

  // Use cases
  const cases=[
    {icon:'📺',name:'4K Streaming',ok:effMbps>=25&&pingAvg<200},
    {icon:'🎮',name:'Online Gaming',ok:pingAvg<80,warn:pingAvg<120},
    {icon:'📹',name:'HD Video Call',ok:effMbps>=4&&ulMbps>=2&&pingAvg<150},
    {icon:'🎬',name:'1080p Stream',ok:effMbps>=8},
    {icon:'📁',name:'Large Downloads',ok:effMbps>=10},
    {icon:'🎵',name:'Music Stream',ok:effMbps>=0.5},
  ];
  $('uc-grid').innerHTML=cases.map(c=>{
    const cls=c.ok?'uc-ok':(c.warn?'uc-warn':'uc-fail');
    const badge=c.ok?'✅':(c.warn?'⚠️':'❌');
    return`<div class="uc-item ${cls}"><span class="uc-icon">${c.icon}</span>${c.name} ${badge}</div>`;
  }).join('');

  $('results-wrap').style.display='block';
}

// ── Main test ──────────────────────────────────────────────────────────────────
let running=false;
let ispData=null;
const device=getDeviceInfo();

async function init(){
  $('ib-os').textContent=device.os;
  $('ib-ram').textContent=(navigator.deviceMemory||'?')+' GB';
  $('ib-cores').textContent=(navigator.hardwareConcurrency||'?')+' cores';
  $('ib-conn').textContent=device.connType;
  ispData=await fetchISP();
  if(ispData){
    const raw=ispData.org||ispData.isp||'Unknown'; $('ib-isp').textContent=raw.replace(/^AS[0-9]+ /,'').slice(0,22);
  } else {
    $('ib-isp').textContent='Unknown';
  }
}

async function startTest(){
  if(running)return;
  running=true;
  const btn=$('start-btn');
  btn.disabled=true;btn.textContent='Testing…';
  $('err-msg').style.display='none';
  $('results-wrap').style.display='none';
  ['ping','dl','ul','done'].forEach(id=>dot(id,''));
  ['m-ping','m-dl','m-ul'].forEach(id=>$(id).textContent='—');
  $('spd-num').textContent='0';
  setGauge(0,100);prog(0);

  try{
    // ── Ping ──────────────────────────────────────────────────────────────────
    dot('ping','active');$('phase-lbl').textContent='MEASURING PING';
    const{avg:pingAvg,jitter:pingJitter}=await measurePing();
    setNum('m-ping',pingAvg,0);
    dot('ping','done');prog(18);await sleep(250);

    // ── Download ──────────────────────────────────────────────────────────────
    dot('dl','active');$('phase-lbl').textContent='DOWNLOAD';$('spd-num').textContent='0.0';
    let dlMbps=0;
    try{
      dlMbps=await measureDownload((spd,elapsed)=>{
        $('spd-num').textContent=spd.toFixed(1);
        $('m-dl').textContent=spd.toFixed(1)+' Mbps';
        setGauge(spd,100);
        prog(Math.min(68,18+(elapsed/13)*50));
      });
    }catch(_){}
    $('m-dl').textContent=dlMbps.toFixed(1)+' Mbps';
    dot('dl','done');prog(68);setGauge(0,50);await sleep(250);

    // ── Upload ────────────────────────────────────────────────────────────────
    dot('ul','active');$('phase-lbl').textContent='UPLOAD';$('spd-num').textContent='0.0';
    let ulMbps=0;
    try{
      ulMbps=await measureUpload(spd=>{
        $('spd-num').textContent=spd.toFixed(1);
        $('m-ul').textContent=spd.toFixed(1)+' Mbps';
        setGauge(spd,50);
        prog(Math.min(90,68+22*0.5));
      });
    }catch(_){ulMbps=dlMbps*0.25;}
    $('m-ul').textContent=ulMbps.toFixed(1)+' Mbps';
    dot('ul','done');prog(90);await sleep(250);

    // ── Correlation fallback (for fast connections) ────────────────────────────
    if(loadedPingPairs.length<2){
      dot('done','active');$('phase-lbl').textContent='CORRELATION…';
      await gatherCorrelationData();
    }

    // ── ML Analysis ───────────────────────────────────────────────────────────
    dot('done','active');$('phase-lbl').textContent='ANALYSING…';
    await sleep(600);
    setGauge(dlMbps,100);$('spd-num').textContent=dlMbps.toFixed(1);
    prog(100);dot('done','done');$('phase-lbl').textContent='COMPLETE';

    const ispName=ispData?(ispData.org||ispData.isp||''):'' ;
    renderResults(dlMbps,ulMbps,pingAvg,pingJitter,device,ispName);

  }catch(e){
    $('err-msg').style.display='block';
    $('phase-lbl').textContent='ERROR';
  }

  btn.disabled=false;btn.textContent='Run Again';running=false;
}

init();
</script>
</body>
</html>"""
    return (html
        .replace('__COEF__',      str(coef))
        .replace('__INTERCEPT__', str(round(intercept, 6)))
        .replace('__MEANS__',     str(means))
        .replace('__STDS__',      str(stds)))
