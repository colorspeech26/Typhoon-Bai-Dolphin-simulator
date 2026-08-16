#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台风“白海豚”（2026）全生命周期模拟器
运行后自动生成交互式 HTML 并在浏览器中打开
"""

import os
import webbrowser

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>台风「白海豚」全生命周期模拟器 (2026)</title>
<style>
  :root {
    --bg: #0b1220;
    --card: #141e2e;
    --border: #243247;
    --text: #e8eef7;
    --muted: #8b9bb4;
    --accent: #3b82f6;
    --danger: #ef4444;
    --warn: #f59e0b;
    --ok: #22c55e;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.55;
  }
  .container { max-width: 1100px; margin: 0 auto; padding: 20px 16px 50px; }
  header { text-align: center; margin-bottom: 24px; }
  header h1 {
    font-size: 1.8rem;
    background: linear-gradient(90deg, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
  }
  header p { color: var(--muted); font-size: 0.95rem; }
  .grid {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 18px;
  }
  @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
  }
  .card h2 {
    font-size: 1.05rem;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .badge {
    background: var(--accent);
    color: white;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 999px;
  }
  #map-canvas {
    width: 100%;
    height: 420px;
    background: #0a1424;
    border-radius: 10px;
    display: block;
  }
  .controls {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
    align-items: center;
  }
  button {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
  }
  button:hover { background: #2563eb; }
  button.secondary {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
  }
  button:disabled { opacity: 0.45; cursor: not-allowed; }
  .slider-box { flex: 1; min-width: 160px; }
  input[type=range] { width: 100%; }
  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px 14px;
    font-size: 0.9rem;
  }
  .info-grid .label { color: var(--muted); }
  .info-grid .value { font-weight: 600; text-align: right; }
  .intensity-bar {
    height: 12px;
    background: #1e293b;
    border-radius: 6px;
    overflow: hidden;
    margin: 8px 0 4px;
  }
  .intensity-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
    transition: width 0.3s;
  }
  .timeline {
    max-height: 260px;
    overflow-y: auto;
    font-size: 0.85rem;
  }
  .tl-item {
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 10px;
  }
  .tl-item.active { background: rgba(59,130,246,0.12); border-radius: 6px; padding-left: 6px; }
  .tl-date { color: var(--muted); min-width: 70px; }
  .legend {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 10px;
  }
  .legend span::before {
    content: "";
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 4px;
  }
  .leg-ts::before { background: #22c55e; }
  .leg-ty::before { background: #f59e0b; }
  .leg-sty::before { background: #ef4444; }
  footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 28px;
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>台风「白海豚」全生命周期模拟器</h1>
    <p>2026年第13号台风 · Typhoon Dolphin · 国际编号 2613</p>
  </header>

  <div class="grid">
    <!-- 左侧：地图动画 -->
    <div class="card">
      <h2><span class="badge">路径</span> 西北太平洋路径模拟</h2>
      <canvas id="map-canvas" width="700" height="420"></canvas>
      <div class="legend">
        <span class="leg-ts">热带风暴</span>
        <span class="leg-ty">台风</span>
        <span class="leg-sty">强/超强台风</span>
      </div>
      <div class="controls">
        <button id="btn-play" onclick="togglePlay()">▶ 播放</button>
        <button class="secondary" onclick="resetSim()">重置</button>
        <div class="slider-box">
          <input type="range" id="time-slider" min="0" max="100" value="0" oninput="seek(this.value)">
        </div>
        <span id="time-label" style="font-size:0.85rem;color:var(--muted);min-width:90px">7月27日</span>
      </div>
    </div>

    <!-- 右侧：状态面板 -->
    <div class="card">
      <h2><span class="badge">实时</span> 当前状态</h2>
      <div class="info-grid" id="status">
        <div class="label">日期</div><div class="value" id="s-date">—</div>
        <div class="label">中心位置</div><div class="value" id="s-pos">—</div>
        <div class="label">中心气压</div><div class="value" id="s-pres">—</div>
        <div class="label">最大风速</div><div class="value" id="s-wind">—</div>
        <div class="label">强度等级</div><div class="value" id="s-level">—</div>
        <div class="label">移动方向</div><div class="value" id="s-dir">—</div>
      </div>
      <div style="margin-top:12px">
        <div style="font-size:0.85rem;color:var(--muted)">强度指示</div>
        <div class="intensity-bar"><div class="intensity-fill" id="int-bar"></div></div>
      </div>
    </div>
  </div>

  <!-- 时间线与特点 -->
  <div class="card" style="margin-top:18px">
    <h2><span class="badge">关键节点</span> 台风「白海豚」大事记</h2>
    <div class="timeline" id="timeline"></div>
  </div>

  <div class="card" style="margin-top:18px">
    <h2><span class="badge">特点</span> 为什么它特别？</h2>
    <ul style="padding-left:20px;font-size:0.9rem;color:var(--muted);line-height:1.8">
      <li><strong style="color:var(--text)">生命史超长</strong>：从7月27日生成到8月中旬消散，超过15天（普通台风约5-7天）</li>
      <li><strong style="color:var(--text)">生成位置极东</strong>：靠近国际日期变更线（约177°E），登陆前移动距离超过6000公里</li>
      <li><strong style="color:var(--text)">爆发增强</strong>：生成后48小时内迅速增强为超强台风，极值风速达65 m/s（17级以上）</li>
      <li><strong style="color:var(--text)">环流庞大</strong>：强盛时7级风圈半径达420-450公里，环流直径约1300公里</li>
      <li><strong style="color:var(--text)">登陆中国</strong>：8月9日先后在浙江玉环、乐清登陆，是有记录以来生成位置最偏东并登陆我国的台风之一</li>
    </ul>
  </div>

  <footer>
    数据综合自中央气象台、JTWC、维基百科公开资料 · 本模拟仅用于科普教育 · 路径与强度为简化示意
  </footer>
</div>

<script>
// ========== 关键路径数据（简化但贴近真实） ==========
// 时间：从 7月27日 到 8月12日，共约17天
const path = [
  // day, lat, lon, wind(m/s), pressure, level, note
  {d:0,  lat:13.2, lon:176.9, wind:18, p:1000, lv:"热带风暴", note:"在日界线附近生成"},
  {d:1,  lat:13.8, lon:172.5, wind:28, p:985,  lv:"强热带风暴", note:"快速增强中"},
  {d:2,  lat:14.5, lon:168.0, wind:42, p:955,  lv:"台风", note:"达到台风级"},
  {d:3,  lat:15.2, lon:163.5, wind:55, p:930,  lv:"强台风", note:"继续增强"},
  {d:4,  lat:16.0, lon:158.8, wind:65, p:910,  lv:"超强台风", note:"达到生命史巅峰（65m/s）"},
  {d:5,  lat:17.0, lon:154.0, wind:62, p:915,  lv:"超强台风", note:"维持超强台风"},
  {d:6,  lat:18.5, lon:149.0, wind:58, p:920,  lv:"超强台风", note:"眼壁置换过程"},
  {d:7,  lat:20.5, lon:143.5, wind:52, p:935,  lv:"强台风", note:"强度略有波动"},
  {d:8,  lat:22.8, lon:138.0, wind:48, p:945,  lv:"强台风", note:"向西偏北移动"},
  {d:9,  lat:24.5, lon:132.5, wind:45, p:950,  lv:"强台风", note:"接近琉球群岛"},
  {d:10, lat:26.2, lon:127.5, wind:45, p:950,  lv:"强台风", note:"进入东海"},
  {d:11, lat:27.5, lon:124.0, wind:45, p:950,  lv:"强台风", note:"逼近浙江沿海"},
  {d:12, lat:28.1, lon:121.5, wind:42, p:960,  lv:"强台风", note:"登陆浙江玉环（强台风级）"},
  {d:13, lat:28.5, lon:120.8, wind:38, p:970,  lv:"台风", note:"二次登陆乐清"},
  {d:14, lat:29.5, lon:118.5, wind:28, p:985,  lv:"强热带风暴", note:"深入内陆减弱"},
  {d:15, lat:31.0, lon:116.0, wind:20, p:995,  lv:"热带风暴", note:"继续北上减弱"},
  {d:16, lat:32.5, lon:114.5, wind:15, p:1000, lv:"热带低压", note:"逐渐消散"},
];

const keyEvents = [
  {d:0,  text:"7月27日：在日界线附近生成，成为有记录以来生成位置最偏东的登陆我国台风之一"},
  {d:2,  text:"7月29日：迅速增强为台风"},
  {d:4,  text:"7月31日前后：达到巅峰强度，中心附近最大风速65 m/s（超强台风），最低气压约910 hPa"},
  {d:6,  text:"多次经历眼壁置换，强度出现波动但仍维持高强度"},
  {d:10, text:"8月6-7日：进入东海，环流庞大（7级风圈半径超400公里）"},
  {d:12, text:"8月9日17时30分：在浙江玉环登陆（强台风级，约42 m/s）"},
  {d:13, text:"约70分钟后：在温州乐清二次登陆"},
  {d:16, text:"8月11日前后：中央气象台停止编号，残余环流继续影响华北等地"},
];

// 地图投影（简化墨卡托风格，适合西太平洋）
const canvas = document.getElementById("map-canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;

// 经纬度范围：覆盖日界线到中国东部
const lonMin = 110, lonMax = 180;
const latMin = 8,   latMax = 40;

function proj(lon, lat) {
  const x = ((lon - lonMin) / (lonMax - lonMin)) * W;
  const y = H - ((lat - latMin) / (latMax - latMin)) * H;
  return [x, y];
}

function drawBaseMap() {
  ctx.fillStyle = "#0a1424";
  ctx.fillRect(0, 0, W, H);

  // 简单大陆轮廓（示意）
  ctx.strokeStyle = "#1e3a5f";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  // 中国东部 + 日本大致轮廓
  const coast = [
    [110,22],[112,21],[116,22],[118,24],[120,25],[121,26],[122,28],
    [122,30],[121,32],[120,34],[118,36],[116,38],[114,39],[110,40]
  ];
  coast.forEach((p,i) => {
    const [x,y] = proj(p[0],p[1]);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();

  // 台湾示意
  ctx.beginPath();
  const tw = [[120,22],[121,22],[121.5,24],[120.5,25],[120,23.5]];
  tw.forEach((p,i)=>{const [x,y]=proj(p[0],p[1]);i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});
  ctx.closePath();
  ctx.stroke();

  // 网格
  ctx.strokeStyle = "#152033";
  ctx.lineWidth = 0.5;
  for(let lon=120; lon<=180; lon+=10){
    const [x1,y1]=proj(lon,latMin), [x2,y2]=proj(lon,latMax);
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
  }
  for(let lat=10; lat<=40; lat+=5){
    const [x1,y1]=proj(lonMin,lat), [x2,y2]=proj(lonMax,lat);
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
  }

  // 标注
  ctx.fillStyle = "#4b6a8a";
  ctx.font = "11px sans-serif";
  ctx.fillText("中国大陆", proj(115,32)[0], proj(115,32)[1]);
  ctx.fillText("日本", proj(138,36)[0], proj(138,36)[1]);
  ctx.fillText("日界线附近", proj(172,14)[0], proj(172,14)[1]);
}

function windColor(wind) {
  if (wind >= 51) return "#ef4444";      // 超强/强台风
  if (wind >= 32.7) return "#f59e0b";    // 台风
  return "#22c55e";                      // 热带风暴及以下
}

function drawPath(upto) {
  drawBaseMap();
  // 画已走过的路径
  ctx.beginPath();
  for (let i = 0; i <= upto; i++) {
    const [x,y] = proj(path[i].lon, path[i].lat);
    if (i === 0) ctx.moveTo(x,y);
    else ctx.lineTo(x,y);
  }
  ctx.strokeStyle = "#3b82f6";
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // 画每个点
  for (let i = 0; i <= upto; i++) {
    const p = path[i];
    const [x,y] = proj(p.lon, p.lat);
    ctx.beginPath();
    ctx.arc(x, y, i === upto ? 7 : 4, 0, Math.PI*2);
    ctx.fillStyle = windColor(p.wind);
    ctx.fill();
    if (i === upto) {
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }
}

// 状态更新
function updateStatus(idx) {
  const p = path[idx];
  const date = new Date(2026, 6, 27);
  date.setDate(date.getDate() + p.d);
  const dateStr = `${date.getMonth()+1}月${date.getDate()}日`;

  document.getElementById("s-date").textContent = dateStr;
  document.getElementById("s-pos").textContent = `${p.lat.toFixed(1)}°N, ${p.lon.toFixed(1)}°E`;
  document.getElementById("s-pres").textContent = p.p + " hPa";
  document.getElementById("s-wind").textContent = p.wind + " m/s";
  document.getElementById("s-level").textContent = p.lv;
  document.getElementById("s-dir").textContent = idx < 12 ? "西偏北" : (idx < 15 ? "西北" : "北转");

  const pct = Math.min(100, (p.wind / 65) * 100);
  document.getElementById("int-bar").style.width = pct + "%";

  document.getElementById("time-label").textContent = dateStr;
  document.getElementById("time-slider").value = Math.round(idx / (path.length-1) * 100);

  // 高亮时间线
  document.querySelectorAll(".tl-item").forEach((el,i) => {
    el.classList.toggle("active", keyEvents[i] && keyEvents[i].d === p.d);
  });
}

function buildTimeline() {
  const box = document.getElementById("timeline");
  box.innerHTML = keyEvents.map(e => `
    <div class="tl-item" data-d="${e.d}">
      <div class="tl-date">Day ${e.d}</div>
      <div>${e.text}</div>
    </div>
  `).join("");
}

// 播放控制
let playing = false;
let current = 0;
let timer = null;

function togglePlay() {
  playing = !playing;
  document.getElementById("btn-play").textContent = playing ? "⏸ 暂停" : "▶ 播放";
  if (playing) {
    timer = setInterval(() => {
      if (current >= path.length - 1) {
        playing = false;
        document.getElementById("btn-play").textContent = "▶ 播放";
        clearInterval(timer);
        return;
      }
      current++;
      drawPath(current);
      updateStatus(current);
    }, 700);
  } else {
    clearInterval(timer);
  }
}

function seek(val) {
  current = Math.round(val / 100 * (path.length - 1));
  drawPath(current);
  updateStatus(current);
}

function resetSim() {
  playing = false;
  clearInterval(timer);
  document.getElementById("btn-play").textContent = "▶ 播放";
  current = 0;
  drawPath(0);
  updateStatus(0);
}

// 初始化
buildTimeline();
drawPath(0);
updateStatus(0);
</script>
</body>
</html>
'''

def main():
    filename = "typhoon_dolphin_2026.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(HTML)
    
    abs_path = os.path.abspath(filename)
    print(f"✅ 已生成模拟页面：{abs_path}")
    print("正在自动打开浏览器……")
    webbrowser.open(f"file://{abs_path}")
    print("完成！可以在页面中播放台风「白海豚」的完整路径与强度变化。")

if __name__ == "__main__":
    main()