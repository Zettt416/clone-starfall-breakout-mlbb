const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9275;

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_ui_verify',
    '--headless',
    '--disable-gpu',
    '--window-size=1200,800',
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
  await sleep(1200);

  // 1. Capture Main Menu with Aether Vanguard selected (like Gambar 2)
  await send('Runtime.evaluate', {
    expression: `(() => {
      document.getElementById('btnShipNext').click(); // Select Aether Vanguard
    })()`
  });
  await sleep(400);

  const shotMenu = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_redesign_ship_card.png'), Buffer.from(shotMenu.result.data, 'base64'));
  console.log('Saved screen_redesign_ship_card.png');

  // 2. Open Boss Codex Modal (like Gambar 1)
  await send('Runtime.evaluate', {
    expression: `(() => {
      document.getElementById('btnBossCodex').click();
    })()`
  });
  await sleep(600);

  const shotCodex = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'screen_redesign_boss_codex.png'), Buffer.from(shotCodex.result.data, 'base64'));
  console.log('Saved screen_redesign_boss_codex.png');

  // Check for any broken images in the document
  const imgCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('#bossCodexGrid img'));
      return {
        totalBossImgs: imgs.length,
        brokenImgs: imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => ({ src: i.src, alt: i.alt })),
        firstFiveSrcs: imgs.slice(0, 5).map(i => ({ alt: i.alt, src: i.src, naturalWidth: i.naturalWidth }))
      };
    })()`,
    returnByValue: true
  });
  console.log('Image check in Kodex:', JSON.stringify(imgCheck.result.value, null, 2));

  ws.close();
  edge.kill();
  console.log('Verification finished successfully!');
}

run().catch(e => {
  console.error(e);
  process.exit(1);
});

