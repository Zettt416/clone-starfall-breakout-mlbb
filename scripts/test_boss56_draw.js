// Mock browser environment
global.window = global;
global.window.addEventListener = () => {};
global.requestAnimationFrame = () => {};
global.Audio = class { addEventListener(){} canPlayType(){ return 'probably'; } };
global.AudioContext = class {
  createGain(){ return { gain:{ value:1, setValueAtTime(){}, linearRampToValueAtTime(){}, exponentialRampToValueAtTime(){} }, connect(){} }; }
  createOscillator(){ return { frequency:{ value:440, setValueAtTime(){} }, type:'sine', connect(){}, start(){}, stop(){} }; }
  createBufferSource(){ return { buffer:null, playbackRate:{ value:1 }, connect(){}, start(){}, stop(){} }; }
  destination = {};
  currentTime = 0;
};
global.webkitAudioContext = global.AudioContext;

const mockElem = () => ({
  classList: { add(){}, remove(){}, contains(){ return false; } },
  style: {},
  textContent: '',
  querySelector: () => mockElem(),
  querySelectorAll: () => [],
  addEventListener: () => {},
  appendChild: () => {},
  removeChild: () => {}
});

global.document = {
  getElementById: (id) => {
    if (id === 'gameCanvas') {
      return {
        getContext: () => mockCtx,
        width: 800,
        height: 480,
        getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 480 }),
        addEventListener: () => {}
      };
    }
    return mockElem();
  },
  querySelector: () => mockElem(),
  querySelectorAll: () => [],
  createElement: () => mockElem()
};
global.localStorage = {
  getItem: () => null,
  setItem: () => null
};
global.Image = class { constructor(){ this.complete = true; this.naturalWidth = 1000; this.naturalHeight = 1000; } };

const fs = require('fs');
eval(fs.readFileSync('js/bosses.js', 'utf-8'));
eval(fs.readFileSync('js/audio.js', 'utf-8'));

const mockCtx = {
  save(){}, restore(){},
  translate(x, y){ this.lastTranslate = [x, y]; },
  rotate(){}, scale(){},
  beginPath(){}, closePath(){}, moveTo(){}, lineTo(){}, stroke(){}, fill(){}, quadraticCurveTo(){},
  arc(){}, ellipse(){}, fillRect(){}, strokeRect(){},
  createLinearGradient(){ return { addColorStop(){} }; },
  createRadialGradient(){ return { addColorStop(){} }; },
  drawImage(){ this.drawn = true; },
  setLineDash(){},
  fillText(){}
};

try {
  const gameJs = fs.readFileSync('js/game.js', 'utf-8');
  eval(gameJs);
  console.log('Game loaded successfully!');

  window.gameState.difficulty = 'hard';
  window.startGame();

  const b56 = window.BOSS_CATALOG.find(b => b.id === 56);
  console.log('Spawning Boss 56:', b56);

  window.gameState.activeBoss = new window.gameState.activeBoss.constructor(b56, 2);
  const boss = window.gameState.activeBoss;

  console.log('Boss created:', {
    name: boss.name,
    archetype: boss.archetype,
    isBig: boss.type === 'bigboss',
    width: boss.width,
    height: boss.height,
    x: boss.x,
    y: boss.y,
    targetX: boss.targetX
  });

  for (let f = 0; f < 600; f++) {
    boss.update(1/60);
    boss.draw(mockCtx);
  }
  console.log('Simulated 600 frames of normal update & draw without errors!');

  boss.isFiringLaser = true;
  boss.laserFireTimer = 0.8;
  for (let f = 0; f < 60; f++) {
    boss.update(1/60);
    boss.draw(mockCtx);
  }
  console.log('Simulated laser firing without errors!');

  boss.startSkillTelegraph();
  for (let f = 0; f < 120; f++) {
    boss.update(1/60);
    boss.draw(mockCtx);
  }
  console.log('Simulated skill casting without errors!');

} catch (err) {
  console.error('CRASHED WITH ERROR:', err);
}
