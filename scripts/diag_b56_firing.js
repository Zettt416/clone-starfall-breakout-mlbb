const { spawn } = require('child_process');
const fs = require('fs');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9260;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_diag_b56',
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
      logs.push(d.params.args.map(a => a.value || JSON.stringify(a)).join(' '));
    }
    if (d.method === 'Runtime.exceptionThrown') {
      logs.push('EXCEPTION: ' + JSON.stringify(d.params.exceptionDetails));
    }
  });

  await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
  await new Promise(r => setTimeout(r, 1200));

  // Start game and spawn boss 56
  const eval1 = await send('Runtime.evaluate', {
    expression: `(() => {
      window.startGame();
      window.gameState.difficulty = 'hard';
      const b = window.testBoss(56);
      b.hp = b.maxHp * 0.5; // 50% HP like screenshot
      b.isFiringLaser = true;
      b.laserFireTimer = 2.0;
      b.x = 640;
      b.currentX = 640;
      b.y = 240;
      return {
        name: b.name,
        archetype: b.archetype,
        x: b.x,
        y: b.y,
        currentX: b.currentX,
        actionState: b.actionState
      };
    })()`,
    returnByValue: true
  });
  console.log('Eval 1:', eval1.result.value);

  // Wait a few frames
  await new Promise(r => setTimeout(r, 150));

  const eval2 = await send('Runtime.evaluate', {
    expression: `(() => {
      const b = window.gameState.activeBoss;
      return {
        x: b.x,
        y: b.y,
        currentX: b.currentX,
        isFiringLaser: b.isFiringLaser,
        actionState: b.actionState
      };
    })()`,
    returnByValue: true
  });
  console.log('Eval 2:', eval2.result.value);
  console.log('Browser Logs:', logs);

  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('b56_firing_screenshot.png', Buffer.from(shot.data, 'base64'));
  console.log('Saved b56_diag_screenshot.png');

  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });
