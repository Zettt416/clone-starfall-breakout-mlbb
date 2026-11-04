const { spawn } = require('child_process');
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9261;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_eval_gameplay2',
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

  await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
  await new Promise(r => setTimeout(r, 1500));

  const simRes = await send('Runtime.evaluate', {
    expression: `(() => {
      try {
        if (typeof window.selectDifficulty === 'function') {
          window.selectDifficulty('hard');
        }
        if (typeof window.startGame === 'function') {
          window.startGame();
        }
        const boss = window.testBoss ? window.testBoss(56) : null;
        if (!boss) return { error: 'no testBoss' };

        const stateHistory = [];
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        for (let i = 0; i < 720; i++) {
          boss.update(1/60);
          boss.draw(ctx);
          if (!stateHistory.includes(boss.actionState)) {
            stateHistory.push(boss.actionState);
          }
        }

        return {
          bossName: boss.name,
          archetype: boss.archetype,
          actionStatesVisited: stateHistory,
          finalActionState: boss.actionState,
          finalPos: { x: boss.x, y: boss.y, currentX: boss.currentX },
          hp: boss.hp,
          maxHp: boss.maxHp
        };
      } catch (err) {
        return { error: err.message, stack: err.stack };
      }
    })()`,
    returnByValue: true
  });

  console.log('simRes:', JSON.stringify(simRes, null, 2));

  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });
