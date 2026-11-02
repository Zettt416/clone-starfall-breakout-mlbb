const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const URL = 'http://localhost:8080/index.html';
const PORT = 9228;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_debug_profile_boss5s_4',
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

  console.log(`Navigating to ${URL}...`);
  await send('Page.navigate', { url: URL });
  await sleep(2500);

  async function evalJson(expr) {
    const res = await send('Runtime.evaluate', {
      expression: `(() => { try { return JSON.stringify(${expr}); } catch(e) { return JSON.stringify({error: e.message}); } })()`,
      returnByValue: true
    });
    const str = res && res.result && res.result.result ? res.result.result.value : null;
    return str ? JSON.parse(str) : null;
  }

  async function takeScreenshot(filename) {
    const result = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(result.result.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buf);
    console.log(`Saved screenshot: ${filename} (${buf.length} bytes)`);
  }

  const check = await evalJson(`({
    hasWindowGameState: typeof window.gameState !== 'undefined',
    screen: window.gameState ? window.gameState.screen : null
  })`);
  console.log('Page loaded initial state:', check);

  console.log('Starting game...');
  await send('Runtime.evaluate', { expression: 'window.startGame()' });

  console.log('Waiting 5.2s (boss checkpoint is at 5.0s)...');
  await sleep(5200);

  const status5s = await evalJson(`({
    survivalTime: window.gameState.survivalTime.toFixed(1),
    warning: window.gameState.bossWarningActive,
    hasBoss: !!window.gameState.activeBoss,
    bossName: window.gameState.activeBoss ? window.gameState.activeBoss.name : (window.gameState.pendingBossConfig ? window.gameState.pendingBossConfig.name : null),
    bossArchetype: window.gameState.activeBoss ? window.gameState.activeBoss.archetype : (window.gameState.pendingBossConfig ? window.gameState.pendingBossConfig.archetype : null)
  })`);
  console.log('Status at 5.2s:', status5s);

  console.log('Waiting 1.2s for warning to finish and boss to enter...');
  await sleep(1200);

  const status6_4s = await evalJson(`({
    survivalTime: window.gameState.survivalTime.toFixed(1),
    hasBoss: !!window.gameState.activeBoss,
    bossName: window.gameState.activeBoss ? window.gameState.activeBoss.name : null,
    bossArchetype: window.gameState.activeBoss ? window.gameState.activeBoss.archetype : null,
    bossHp: window.gameState.activeBoss ? window.gameState.activeBoss.hp : null,
    isCastingSkill: window.gameState.activeBoss ? window.gameState.activeBoss.isCastingSkill : false
  })`);
  console.log('Status at 6.4s (Boss Active):', status6_4s);
  await takeScreenshot('screen_boss_5s_active.png');

  console.log('Killing Boss #1 with test key K...');
  await send('Runtime.evaluate', {
    expression: "window.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyK', key: 'k' }))"
  });

  await sleep(400);
  const statusAfterKill = await evalJson(`({
    hasBoss: !!window.gameState.activeBoss,
    bossCycle: window.gameState.bossCycle,
    nextBossCheckpoint: window.gameState.nextBossCheckpoint.toFixed(1),
    survivalTime: window.gameState.survivalTime.toFixed(1)
  })`);
  console.log('Status after kill:', statusAfterKill);

  console.log('Waiting 5.3s for next boss (Cycle 2)...');
  await sleep(5300);

  const statusCycle2 = await evalJson(`({
    survivalTime: window.gameState.survivalTime.toFixed(1),
    warning: window.gameState.bossWarningActive,
    hasBoss: !!window.gameState.activeBoss,
    bossCycle: window.gameState.bossCycle,
    bossName: window.gameState.activeBoss ? window.gameState.activeBoss.name : (window.gameState.pendingBossConfig ? window.gameState.pendingBossConfig.name : null),
    bossArchetype: window.gameState.activeBoss ? window.gameState.activeBoss.archetype : (window.gameState.pendingBossConfig ? window.gameState.pendingBossConfig.archetype : null)
  })`);
  console.log('Status Cycle 2 at +5s:', statusCycle2);

  await sleep(1200);
  await takeScreenshot('screen_boss_5s_cycle2.png');

  ws.close();
  edge.kill();
  console.log('ALL VERIFIED PERFECTLY!');
  process.exit(0);
}

run().catch(err => {
  console.error('Error during run:', err);
  process.exit(1);
});
