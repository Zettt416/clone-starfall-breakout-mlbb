const { spawn } = require('child_process');

async function run() {
  const edge = spawn('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', [
    '--remote-debugging-port=9278',
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_verify_imgs',
    '--headless',
    '--disable-gpu',
    'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1000));
  const res = await (await fetch('http://127.0.0.1:9278/json')).json();
  const ws = new WebSocket(res[0].webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 1;
  const send = (m, p) => new Promise(r => {
    const cur = id++;
    const h = e => { const d = JSON.parse(e.data); if (d.id === cur) { ws.removeEventListener('message', h); r(d); } };
    ws.addEventListener('message', h);
    ws.send(JSON.stringify({ id: cur, method: m, params: p }));
  });
  await send('Page.navigate', { url: 'http://localhost:8080/index.html' });
  await new Promise(r => setTimeout(r, 1200));
  const val = await send('Runtime.evaluate', {
    expression: '(() => { const imgs = Array.from(document.querySelectorAll("#howToPlayModal img")); return imgs.map(i => ({ src: i.src, naturalWidth: i.naturalWidth, complete: i.complete })); })()',
    returnByValue: true
  });
  console.log('Result:', JSON.stringify(val.result.result.value, null, 2));
  ws.close();
  edge.kill();
}
run();

