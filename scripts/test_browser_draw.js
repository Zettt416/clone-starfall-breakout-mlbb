const { spawn } = require('child_process');
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9252;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_eval_draw',
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
  await send('Page.navigate', { url: 'http://localhost:8080/index.html?view=megaman_railgun' });
  await new Promise(r => setTimeout(r, 1200));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const boss = window.gameState && window.gameState.activeBoss;
      if (!boss) return { err: "no boss" };
      const imgKey = 'boss_' + (boss.archetype || 'mecha');
      const img = window.assets && window.assets.images ? window.assets.images[imgKey] : null;
      return {
        bossName: boss.name,
        archetype: boss.archetype,
        x: boss.x,
        y: boss.y,
        currentX: boss.currentX,
        isBig: boss.type === 'bigboss',
        hasImg: !!img,
        imgComplete: img ? img.complete : false,
        imgNatWidth: img ? img.naturalWidth : 0
      };
    })()`,
    returnByValue: true
  });
  console.log('Result:', evalRes.result.value);
  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });
