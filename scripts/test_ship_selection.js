const { spawn } = require('child_process');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9265;

const edge = spawn(EDGE_PATH, [
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_char_select_test',
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

  const testRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const img = document.getElementById('shipAvatarImg');
      const name = document.getElementById('shipNameText');
      const btnNext = document.getElementById('btnShipNext');

      const s1 = { name: name.textContent, src: img.src };
      btnNext.click();
      const s2 = { name: name.textContent, src: img.src };
      btnNext.click();
      const s3 = { name: name.textContent, src: img.src };

      return { s1, s2, s3 };
    })()`,
    returnByValue: true
  });

  console.log('Ship selection test result:', JSON.stringify(testRes.result.value, null, 2));
  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });
