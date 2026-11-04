const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9230;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_debug_profile_anim_test',
    '--headless',
    '--disable-gpu',
    '--window-size=1280,720',
    'about:blank'
  ]);

  let wsUrl = null;
  for (let i = 0; i < 20; i++) {
    await sleep(400);
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json`);
      const list = await res.json();
      const page = list && list.find(t => t.type === 'page');
      if (page && page.webSocketDebuggerUrl) {
        wsUrl = page.webSocketDebuggerUrl;
        break;
      }
    } catch (e) {}
  }

  if (!wsUrl) {
    console.error('Failed to get WebSocket debugger URL');
    edge.kill();
    process.exit(1);
  }

  const ws = new WebSocket(wsUrl);
  let id = 1;
  const pending = new Map();

  ws.onmessage = msg => {
    const data = JSON.parse(msg.data);
    if (data.id && pending.has(data.id)) {
      pending.get(data.id)(data);
      pending.delete(data.id);
    }
  };

  await new Promise(resolve => (ws.onopen = resolve));

  function send(method, params = {}) {
    const curId = id++;
    return new Promise(resolve => {
      pending.set(curId, resolve);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });
  }

  await send('Page.enable');
  await send('Runtime.enable');

  async function snap(url, filename) {
    console.log(`Navigating to ${url}...`);
    await send('Page.navigate', { url });
    await sleep(1800);
    const result = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(result.result.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buf);
    console.log(`Saved screenshot: ${filename} (${buf.length} bytes)`);
  }

  // 1. Valkyrie Twirling Staff & Angelic Wings (Idle)
  await snap('http://localhost:8080/index.html?view=bossvalkyrie', 'screen_valkyrie_natural_staff.png');

  // 2. Valkyrie Overdrive Twirling Vortex (Charging Lance)
  await snap('http://localhost:8080/index.html?view=valkyriecharge', 'screen_valkyrie_natural_vortex.png');

  // 3. Mecha Titan Aiming Railgun & Overdrive Arc Reactor
  await snap('http://localhost:8080/index.html?view=mechacharge', 'screen_mecha_natural_railgun.png');

  // 4. Alien Eldritch Eye with Tracking Pupil & Undulating Tendrils
  await snap('http://localhost:8080/index.html?view=bossalien', 'screen_alien_natural_eye.png');

  ws.close();
  edge.kill();
  console.log('All animation screenshots captured!');
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});

