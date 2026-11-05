const { spawn } = require('child_process');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const PORT = 9277;

const edge = spawn(EDGE_PATH, [
  '--remote-debugging-port=9277',
  '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_check_ship_text',
  '--headless',
  '--disable-gpu',
  'about:blank'
]);

async function run() {
  await new Promise(r => setTimeout(r, 1200));
  const res = await fetch('http://127.0.0.1:9277/json');
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

  const textCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const card = document.getElementById('shipCardActive');
      return {
        cardHtml: card.innerText.trim(),
        avatarSrc: document.getElementById('shipAvatarImg').src
      };
    })()`,
    returnByValue: true
  });
  console.log('Ship Card Content:\n' + textCheck.result.value.cardHtml);
  console.log('Avatar Src:', textCheck.result.value.avatarSrc);

  // Click next for Aether Vanguard
  await send('Runtime.evaluate', { expression: 'document.getElementById("btnShipNext").click()' });
  await new Promise(r => setTimeout(r, 300));
  const textCheck2 = await send('Runtime.evaluate', {
    expression: `(() => {
      const card = document.getElementById('shipCardActive');
      return {
        cardHtml: card.innerText.trim(),
        avatarSrc: document.getElementById('shipAvatarImg').src
      };
    })()`,
    returnByValue: true
  });
  console.log('\nAether Vanguard Card Content:\n' + textCheck2.result.value.cardHtml);
  console.log('Avatar Src:', textCheck2.result.value.avatarSrc);

  ws.close();
  edge.kill();
}

run().catch(e => { console.error(e); edge.kill(); });

