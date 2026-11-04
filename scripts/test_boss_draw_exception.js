const { spawn } = require('child_process');
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9253;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_eval_errs',
  '--headless',
  '--disable-gpu',
  'about:blank'
]);

async function run() {
  await new Promise(r => setTimeout(r, 1200));
  const res = await fetch(`http://127.0.0.1:${PORT}/json`);
  const list = await res.json();
  const page = list.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 1;
  const send = (m, p={}) => new Promise(res => {
    const cur = id++;
    const h = msg => {
      const d = JSON.parse(msg.data);
      if (d.id === cur) { ws.removeEventListener('message', h); res(d.result); }
    };
    ws.addEventListener('message', h);
    ws.send(JSON.stringify({ id: cur, method: m, params: p }));
  });
  await send('Page.enable');
  await send('Runtime.enable');

  const logs = [];
  ws.addEventListener('message', msg => {
    const d = JSON.parse(msg.data);
    if (d.method === 'Runtime.consoleAPICalled') {
      logs.push(d.params.args.map(a => a.value).join(' '));
    }
    if (d.method === 'Runtime.exceptionThrown') {
      logs.push('EXCEPTION: ' + JSON.stringify(d.params.exceptionDetails));
    }
  });

  await send('Page.navigate', { url: 'http://localhost:8080/index.html?view=megaman_railgun' });
  await new Promise(r => setTimeout(r, 1500));

  const checkRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const canvas = document.getElementById('gameCanvas');
      const ctx = canvas.getContext('2d');
      const boss = window.gameState.activeBoss;
      console.log('Testing boss draw manually...');
      let drawErr = null;
      try {
        boss.draw(ctx);
        console.log('boss.draw passed without throwing!');
      } catch(e) {
        drawErr = e.message + '\\n' + e.stack;
        console.error('boss.draw THREW:', e);
      }
      return {
        drawErr,
        bossPos: { x: boss.x, y: boss.y, currentX: boss.currentX },
        laserTargetY: boss.laserTargetY,
        laserFireTimer: boss.laserFireTimer,
        isFiringLaser: boss.isFiringLaser,
        canvasW: canvas.width,
        canvasH: canvas.height
      };
    })()`,
    returnByValue: true
  });

  console.log('checkRes:', checkRes.result.value);
  console.log('Browser logs:', logs);
  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });
