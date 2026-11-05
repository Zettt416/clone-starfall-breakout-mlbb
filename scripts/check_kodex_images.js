const { spawn } = require('child_process');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9276;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_dom_query',
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
  await new Promise(r => setTimeout(r, 1200));

  await send('Runtime.evaluate', { expression: 'document.getElementById("btnBossCodex").click()' });
  await new Promise(r => setTimeout(r, 800));

  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const imgs = Array.from(document.querySelectorAll('#bossCodexGrid img'));
      return {
        total: imgs.length,
        broken: imgs.filter(i => !i.complete || i.naturalWidth === 0).length,
        firstThree: imgs.slice(0, 3).map(i => ({ src: i.src, naturalWidth: i.naturalWidth, naturalHeight: i.naturalHeight }))
      };
    })()`,
    returnByValue: true
  });
  console.log('Result:', JSON.stringify(evalRes.result.value, null, 2));
  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });

