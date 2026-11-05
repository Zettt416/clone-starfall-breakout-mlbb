const { spawn } = require('child_process');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9270;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_scaling_check',
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

  const check = await send('Runtime.evaluate', {
    expression: `(() => {
      window.startGame();
      window.gameState.survivalTime = 120; // 2 minutes
      window.gameState.score = 6000;
      return {
        diffMult: window.gameState.difficultyMultiplier,
        survivalTime: window.gameState.survivalTime,
        activeBoss: !!window.gameState.activeBoss
      };
    })()`,
    returnByValue: true
  });

  console.log('Test in browser result:', check.result.value);
  await new Promise(r => setTimeout(r, 1200));
  console.log('Logs/Exceptions:', logs);

  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });

