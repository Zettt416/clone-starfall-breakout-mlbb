const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9272;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_verify_rev2',
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

  async function snap(url, filename, evalFn) {
    console.log(`Navigating to ${url}...`);
    await send('Page.navigate', { url });
    await sleep(1400);
    if (evalFn) {
      await send('Runtime.evaluate', { expression: evalFn });
      await sleep(500);
    }
    const result = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(result.result.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buf);
    console.log(`Saved screenshot: ${filename} (${buf.length} bytes)`);
  }

  // 1. Ship 1: Stella Nova (Menu & In-Game with Hyperdrive)
  await snap('http://localhost:8080/index.html', 'screen_rev_ship1_stella.png', `(() => {
    window.selectShip('stella_nova');
    window.startGame();
    const p = window.getPlayer();
    if (p) p.buffs.hyperdrive = 10.0;
  })()`);

  // 2. Ship 2: Aether Vanguard (In-Game with Heavy Flak & Tesla Coil)
  await snap('http://localhost:8080/index.html', 'screen_rev_ship2_aether.png', `(() => {
    window.selectShip('aether_vanguard');
    window.setDifficulty('hard');
    window.startGame();
    const p = window.getPlayer();
    if (p) {
      p.buffs.heavy_flak = 10.0;
      p.buffs.tesla_coil = 10.0;
    }
  })()`);

  // 3. Ship 3: Chrono Phantom (In-Game with Quantum Clones)
  await snap('http://localhost:8080/index.html', 'screen_rev_ship3_chrono.png', `(() => {
    window.selectShip('chrono_phantom');
    window.setDifficulty('normal');
    window.startGame();
    const p = window.getPlayer();
    if (p) {
      p.buffs.quantum_clones = 10.0;
      p.buffs.void_needle = 10.0;
    }
  })()`);

  // 4. Hardcorez Stage Backdrop: Event Horizon Black Hole
  await snap('http://localhost:8080/index.html', 'screen_rev_stage_hardcorez.png', `(() => {
    window.setDifficulty('hardcorez');
    window.startGame();
  })()`);

  // 5. Unique Big Boss: Crimson Annihilator
  await snap('http://localhost:8080/index.html', 'screen_rev_boss_crimson.png', `(() => {
    window.setDifficulty('hard');
    window.startGame();
    const boss = window.testBoss ? window.testBoss(52) : null;
    if (boss) {
      boss.name = 'Crimson Annihilator';
      boss.x = 560;
      boss.currentX = 560;
      boss.y = 240;
    }
  })()`);

  // 6. Unique Big Boss: Astraea Archon Valkyrie
  await snap('http://localhost:8080/index.html', 'screen_rev_boss_astraea.png', `(() => {
    window.setDifficulty('easy');
    window.startGame();
    const boss = window.testBoss ? window.testBoss(20) : null;
    if (boss) {
      boss.name = 'Astraea Archon';
      boss.x = 560;
      boss.currentX = 560;
      boss.y = 240;
    }
  })()`);

  ws.close();
  edge.kill();
  console.log('All revision screenshots successfully captured!');
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
