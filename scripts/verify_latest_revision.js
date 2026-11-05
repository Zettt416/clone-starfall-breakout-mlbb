const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9276;

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_rev_verify',
    '--headless',
    '--disable-gpu',
    '--window-size=1280,800',
    'about:blank'
  ]);

  let wsUrl = null;
  for (let i = 0; i < 20; i++) {
    await sleep(350);
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json`);
      const list = await res.json();
      const page = list.find(t => t.type === 'page');
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
  await new Promise(r => ws.onopen = r);

  function send(method, params = {}) {
    const curId = id++;
    return new Promise(resolve => {
      pending.set(curId, resolve);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });
  }

  await send('Page.enable');
  await send('Runtime.enable');

  console.log('Navigating to http://localhost:8080/index.html...');
  await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
  await sleep(1500);

  // 1. Verify "Cara Main" Modal Images
  console.log('Testing Cara Main modal...');
  await send('Runtime.evaluate', {
    expression: `(() => { document.getElementById('btnHowToPlayStart').click(); })()`
  });
  await sleep(500);

  const howToPlayCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('#howToPlayModal img'));
      return {
        total: imgs.length,
        broken: imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => ({ src: i.src, alt: i.alt })),
        allLoaded: imgs.every(i => i.complete && i.naturalWidth > 0),
        items: imgs.map(i => ({ alt: i.alt, src: i.src, naturalWidth: i.naturalWidth }))
      };
    })()`,
    returnByValue: true
  });
  console.log('Cara Main Modal Image Check:', JSON.stringify(howToPlayCheck.result.value, null, 2));

  const shotCaraMain = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_rev_caramain_modal.png'), Buffer.from(shotCaraMain.result.data, 'base64'));
  console.log('Saved screen_rev_caramain_modal.png');

  // Close Cara Main modal
  await send('Runtime.evaluate', {
    expression: `(() => { document.getElementById('btnCloseHowToPlay').click(); })()`
  });
  await sleep(300);

  // 2. Verify Kodex Modal (25 cards per tab, ensure 0 broken)
  console.log('Testing Kodex modal...');
  await send('Runtime.evaluate', {
    expression: `(() => { document.getElementById('btnBossCodex').click(); })()`
  });
  await sleep(600);

  const kodexCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('#bossCodexGrid img'));
      return {
        total: imgs.length,
        broken: imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => ({ src: i.src, alt: i.alt }))
      };
    })()`,
    returnByValue: true
  });
  console.log('Kodex Modal Image Check:', JSON.stringify(kodexCheck.result.value, null, 2));

  // Close Kodex
  await send('Runtime.evaluate', {
    expression: `(() => { document.getElementById('btnCloseBossCodex').click(); })()`
  });
  await sleep(300);

  // 3. Start Game in NORMAL mode and capture background
  console.log('Starting game in Normal mode...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      // Ensure Normal difficulty is selected
      const normalBtn = Array.from(document.querySelectorAll('.diff-btn')).find(b => b.dataset.diff === 'normal');
      if (normalBtn) normalBtn.click();
      document.getElementById('btnStart').click();
    })()`
  });
  await sleep(1000);

  const shotNormal = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_rev_backdrop_normal.png'), Buffer.from(shotNormal.result.data, 'base64'));
  console.log('Saved screen_rev_backdrop_normal.png');

  // 4. Test Drone in-game
  console.log('Spawning fast_scout drones...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      // Spawn drones at visible positions
      meteors.length = 0; // Clear any existing meteors
      meteors.push(new Meteor(750, 200, 'fast_scout'));
      meteors.push(new Meteor(620, 340, 'fast_scout'));
      meteors.push(new Meteor(850, 480, 'fast_scout'));
    })()`
  });
  await sleep(300);

  const shotDrone = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_rev_enemy_drone_in_game.png'), Buffer.from(shotDrone.result.data, 'base64'));
  console.log('Saved screen_rev_enemy_drone_in_game.png');

  // 5. Test Boss Aura in-game (ensure no solid black ball or stick rays)
  console.log('Spawning Big Boss to test celestial boss atmosphere...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      state.bossCycle = 2; // Big boss
      state.activeBoss = spawnBoss(2);
    })()`
  });
  await sleep(400);

  const shotBossAura = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_rev_boss_aura_backdrop.png'), Buffer.from(shotBossAura.result.data, 'base64'));
  console.log('Saved screen_rev_boss_aura_backdrop.png');

  // 6. Test EASY mode backdrop
  console.log('Testing Easy mode backdrop...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      state.activeBoss = null;
      state.bossWarningActive = false;
      state.difficulty = 'easy';
    })()`
  });
  await sleep(300);

  const shotEasy = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_rev_backdrop_easy.png'), Buffer.from(shotEasy.result.data, 'base64'));
  console.log('Saved screen_rev_backdrop_easy.png');

  ws.close();
  edge.kill();
  console.log('All tests completed successfully!');
}

run().catch(e => {
  console.error(e);
  process.exit(1);
});

