const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:\\Users\\Zeke\\.gemini\\antigravity\\brain\\dda2e00e-0c43-42a4-a266-c0ea76b4a578';
const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const HTML_PATH = 'file:///c:/Users/Zeke/Documents/code/clone-starfall-breakout-mlbb/index.html';
const PORT = 9222;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const edge = spawn(EDGE_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--user-data-dir=C:\\Users\\Zeke\\AppData\\Local\\Temp\\edge_debug_profile',
    '--headless',
    '--disable-gpu',
    '--window-size=1280,720',
    HTML_PATH
  ]);

  edge.stderr.on('data', d => {});

  let wsUrl = null;
  for (let i = 0; i < 20; i++) {
    await sleep(400);
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json`);
      const list = await res.json();
      if (list && list.length > 0 && list[0].webSocketDebuggerUrl) {
        wsUrl = list[0].webSocketDebuggerUrl;
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

  await new Promise(resolve => (ws.onopen = resolve));

  function send(method, params = {}) {
    const curId = id++;
    return new Promise(resolve => {
      pending.set(curId, resolve);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });
  }

  await send('Page.enable');
  await send('Runtime.enable');
  await sleep(1000);

  async function takeScreenshot(filename) {
    const result = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(result.result.data, 'base64');
    const outPath = path.join(ARTIFACT_DIR, filename);
    fs.writeFileSync(outPath, buf);
    console.log(`Saved screenshot: ${outPath}`);
    return outPath;
  }

  // 1. In-game HUD
  await send('Runtime.evaluate', {
    expression: `
      document.getElementById('startScreen').classList.remove('active');
      document.getElementById('scoreVal').textContent = '3453';
      document.getElementById('highScoreVal').textContent = '22374';
      document.getElementById('timerVal').textContent = '00:20';
      document.getElementById('hudDiffBadge').textContent = 'HARD';
      document.getElementById('hudDiffBadge').className = 'hud-diff-badge diff-hard';
    `
  });
  await sleep(500);
  await takeScreenshot('screen_hud.png');

  // 2. Leaderboard Modal
  await send('Runtime.evaluate', {
    expression: `
      document.getElementById('leaderboardModal').classList.remove('hidden');
      document.getElementById('leaderboardLoading').classList.add('hidden');
      document.getElementById('leaderboardTable').classList.remove('hidden');
      document.getElementById('leaderboardBody').innerHTML = \`
        <tr class="rank-badge-1">
          <td class="col-rank">🥇 1</td>
          <td class="col-name">CELENK</td>
          <td class="col-diff"><span class="diff-tag diff-tag-normal">NORMAL</span></td>
          <td class="col-score">22.374</td>
          <td class="col-time">02:41</td>
        </tr>
        <tr class="rank-badge-2">
          <td class="col-rank">🥈 2</td>
          <td class="col-name">STELLA_ACE</td>
          <td class="col-diff"><span class="diff-tag diff-tag-hard">HARD</span></td>
          <td class="col-score">18.920</td>
          <td class="col-time">02:15</td>
        </tr>
        <tr class="rank-badge-3">
          <td class="col-rank">🥉 3</td>
          <td class="col-name">CYBER_PILOT</td>
          <td class="col-diff"><span class="diff-tag diff-tag-easy">EASY</span></td>
          <td class="col-score">14.500</td>
          <td class="col-time">01:50</td>
        </tr>
      \`;
    `
  });
  await sleep(500);
  await takeScreenshot('screen_leaderboard.png');

  // 3. Game Over Screen
  await send('Runtime.evaluate', {
    expression: `
      document.getElementById('leaderboardModal').classList.add('hidden');
      document.getElementById('gameOverScreen').classList.add('active');
      document.getElementById('finalDiff').textContent = 'HARDCOREZ';
      document.getElementById('finalDiff').className = 'result-val highlight diff-tag-hardcorez';
      document.getElementById('finalTime').textContent = '00:08';
      document.getElementById('finalBestTime').textContent = '02:41';
      document.getElementById('finalScore').textContent = '2464';
      document.getElementById('finalHighScore').textContent = '22374';
      document.getElementById('pilotNameInput').value = 'CELENK';
    `
  });
  await sleep(500);
  await takeScreenshot('screen_gameover.png');

  ws.close();
  edge.kill();
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
