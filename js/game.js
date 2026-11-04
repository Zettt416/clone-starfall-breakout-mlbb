/**
 * Starfall Breakout: Retro Space Runner
 * Horizontal Side-Scroller Arcade Runner (Left to Right)
 * Philosophy: Pure Vanilla JS, Zero external dependencies, offline-ready, instant replay.
 */

(function () {
  'use strict';

  // --- Constants & Config ---
  const CANVAS_WIDTH = 800;
  const CANVAS_HEIGHT = 480;

  // --- Asset Loader (Real 32-bit Transparent PNG Arcade Assets) ---
  const assets = {
    images: {}
  };

  function loadAsset(name, src) {
    const img = new Image();
    img.src = src;
    img.onload = () => {
      assets.images[name] = img;
    };
    img.onerror = () => {
      assets.images[name] = null;
    };
  }

  // Preload real 32-bit transparent PNG arcade assets
  loadAsset('player_ship', 'assets/images/player_ship.png');
  loadAsset('meteor', 'assets/images/meteor.png');
  loadAsset('armored_meteor', 'assets/images/armored_meteor.png');
  loadAsset('ult_icon', 'assets/images/ult_icon.png');
  loadAsset('cyber_heart', 'assets/images/cyber_heart.png');
  loadAsset('stellar_star', 'assets/images/stellar_star.png');
  loadAsset('shield_icon', 'assets/images/shield_icon.png');
  loadAsset('powerup_rapid', 'assets/images/powerup_rapid.png');
  loadAsset('powerup_multi', 'assets/images/powerup_multi.png');
  loadAsset('powerup_pierce', 'assets/images/powerup_pierce.png');
  loadAsset('powerup_burst', 'assets/images/powerup_burst.png');
  loadAsset('miniboss', 'assets/images/miniboss.png');
  loadAsset('bigboss', 'assets/images/bigboss.png');
  loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');
  loadAsset('boss_mecha', 'assets/images/boss_mecha_titan.png');
  loadAsset('boss_monster', 'assets/images/boss_alien_leviathan.png');
  loadAsset('boss_humanoid', 'assets/images/boss_humanoid_valkyrie.png');
  loadAsset('boss_alien', 'assets/images/boss_eldritch_eye.png');
  loadAsset('explosion_sheet', 'assets/images/explosion_sheet.png');

  // Dedicated Playable Ship Sprites
  loadAsset('ship_stella_nova', 'assets/images/ship_stella_nova.png');
  loadAsset('ship_aether_vanguard', 'assets/images/ship_aether_vanguard.png');
  loadAsset('ship_chrono_phantom', 'assets/images/ship_chrono_phantom.png');

  // Dedicated Big Boss Sprites
  loadAsset('boss_crimson_annihilator', 'assets/images/boss_crimson_annihilator.png');
  loadAsset('boss_void_singularity', 'assets/images/boss_void_singularity.png');
  loadAsset('boss_astraea_archon', 'assets/images/boss_astraea_archon.png');

  // Dedicated Character Power-Up Icons
  loadAsset('powerup_hyperdrive', 'assets/images/powerup_hyperdrive.png');
  loadAsset('powerup_plasma_spread', 'assets/images/powerup_plasma_spread.png');
  loadAsset('powerup_heavy_flak', 'assets/images/powerup_heavy_flak.png');
  loadAsset('powerup_tesla_coil', 'assets/images/powerup_tesla_coil.png');
  loadAsset('powerup_quantum_clones', 'assets/images/powerup_quantum_clones.png');
  loadAsset('powerup_void_needle', 'assets/images/powerup_void_needle.png');

  // Power-up types
  const BUFF_TYPES = {
    RAPID: { id: 'rapid', name: 'RAPID', color: '#ff2a85', symbol: '⚡', duration: 8.0 },
    MULTI: { id: 'multi', name: 'MULTI', color: '#00f3ff', symbol: '✦', duration: 9.0 },
    PIERCE: { id: 'pierce', name: 'PIERCE', color: '#ffd000', symbol: '➤', duration: 7.0 },
    BURST: { id: 'burst', name: 'BURST', color: '#ff7700', symbol: '💥', duration: 8.0 },
    SHIELD: { id: 'shield', name: 'SHIELD', color: '#00f3ff', symbol: '🛡️', duration: 12.0 },
    // Stella Nova Unique Powerups
    HYPERDRIVE: { id: 'hyperdrive', name: 'HYPERDRIVE', color: '#ff2a85', symbol: '⚡', duration: 7.0, iconAsset: 'powerup_hyperdrive' },
    PLASMA_SPREAD: { id: 'plasma_spread', name: '5-WAY PLASMA', color: '#00f3ff', symbol: '💥', duration: 8.0, iconAsset: 'powerup_plasma_spread' },
    // Aether Vanguard Unique Powerups
    HEAVY_FLAK: { id: 'heavy_flak', name: 'CLUSTER FLAK', color: '#ffaa00', symbol: '💣', duration: 8.0, iconAsset: 'powerup_heavy_flak' },
    TESLA_COIL: { id: 'tesla_coil', name: 'TESLA DISCHARGE', color: '#ffd000', symbol: '⚡', duration: 7.5, iconAsset: 'powerup_tesla_coil' },
    // Chrono Phantom Unique Powerups
    QUANTUM_CLONES: { id: 'quantum_clones', name: 'QUANTUM CLONES', color: '#e0aaff', symbol: '👥', duration: 8.5, iconAsset: 'powerup_quantum_clones' },
    VOID_NEEDLE: { id: 'void_needle', name: 'VOID NEEDLES', color: '#b5179e', symbol: '🗡️', duration: 7.0, iconAsset: 'powerup_void_needle' }
  };

  // Difficulty Level Configurations (Tuning Powerups, Enemy HP, Speed & Fast Scouts)
  const DIFFICULTY_CONFIGS = {
    easy: {
      label: 'EASY',
      icon: '🟢',
      lives: 4,
      scoreMultiplier: 0.8,
      powerupDropRate: 0.35,
      meteorHpMult: 0.8,
      meteorSpeedMult: 0.82,
      meteorSpawnRateMult: 1.25,
      bossHpMult: 0.75,
      bossShootIntervalMult: 1.35,
      heartDropWeight: 0.22,
      survivalDropWeight: 0.22,
      fastEnemySpawnRate: 0.05,
      revengeBullets: false,
      touhouDanmaku: false,
      hurtboxScale: 0.75
    },
    normal: {
      label: 'NORMAL',
      icon: '🔵',
      lives: 3,
      scoreMultiplier: 1.0,
      powerupDropRate: 0.25,
      meteorHpMult: 1.0,
      meteorSpeedMult: 1.0,
      meteorSpawnRateMult: 1.0,
      bossHpMult: 1.0,
      bossShootIntervalMult: 1.0,
      heartDropWeight: 0.12,
      survivalDropWeight: 0.16,
      fastEnemySpawnRate: 0.14,
      revengeBullets: false,
      touhouDanmaku: false,
      hurtboxScale: 0.7
    },
    hard: {
      label: 'HARD',
      icon: '🔴',
      lives: 3,
      scoreMultiplier: 1.5,
      powerupDropRate: 0.18,
      meteorHpMult: 1.35,
      meteorSpeedMult: 1.22,
      meteorSpawnRateMult: 0.82,
      bossHpMult: 1.3,
      bossShootIntervalMult: 0.8,
      heartDropWeight: 0.08,
      survivalDropWeight: 0.12,
      fastEnemySpawnRate: 0.25,
      revengeBullets: true,
      touhouDanmaku: false,
      hurtboxScale: 0.65
    },
    hardcorez: {
      label: 'HARDCOREZ',
      icon: '🟣',
      lives: 2,
      scoreMultiplier: 2.5,
      powerupDropRate: 0.12,
      meteorHpMult: 1.75,
      meteorSpeedMult: 1.38,
      meteorSpawnRateMult: 0.68,
      bossHpMult: 1.6,
      bossShootIntervalMult: 0.65,
      heartDropWeight: 0.04,
      survivalDropWeight: 0.08,
      fastEnemySpawnRate: 0.38,
      revengeBullets: true,
      touhouDanmaku: true,
      hurtboxScale: 0.45,
      drawHitboxCore: true
    }
  };

  // Starship / Character Roster (Unique Real Arcade Sprites, Dedicated Power-Ups & Skills)
  const SHIPS_CONFIG = {
    stella_nova: {
      id: 'stella_nova',
      name: 'STELLA NOVA',
      class: 'INTERCEPTOR',
      badgeClass: 'badge-interceptor',
      color: '#00f3ff',
      filter: 'none',
      avatarSrc: 'assets/images/ship_stella_nova.png',
      spriteKey: 'ship_stella_nova',
      speed: 330,
      firepowerLabel: 'TWIN PLASMA CANNON',
      hpLabel: 'STANDARD (3 LIVES)',
      extraLives: 0,
      uniquePowerups: ['HYPERDRIVE', 'PLASMA_SPREAD'],
      surviveName: 'COSMIC SHIELD',
      surviveDesc: 'COSMIC AEGIS SHIELD (3D FORCEFIELD)',
      ultName: 'STELLAR BLASTER',
      ultDesc: 'STELLAR BLASTER HORIZONTAL BEAM'
    },
    aether_vanguard: {
      id: 'aether_vanguard',
      name: 'AETHER VANGUARD',
      class: 'DREADNOUGHT',
      badgeClass: 'badge-dreadnought',
      color: '#ffd000',
      filter: 'none',
      avatarSrc: 'assets/images/ship_aether_vanguard.png',
      spriteKey: 'ship_aether_vanguard',
      speed: 275,
      firepowerLabel: 'EXPLOSIVE FLAK SPREAD',
      hpLabel: '+1 ARMOR LIFE (4 LIVES)',
      extraLives: 1,
      uniquePowerups: ['HEAVY_FLAK', 'TESLA_COIL'],
      surviveName: 'NANITE MATRIX',
      surviveDesc: 'NANITE PHASE BARRIER (EMP PULSE CLEAR)',
      ultName: 'CLUSTER BARRAGE',
      ultDesc: 'HEAVY CLUSTER BARRAGE BOMBS'
    },
    chrono_phantom: {
      id: 'chrono_phantom',
      name: 'CHRONO PHANTOM',
      class: 'RECON GHOST',
      badgeClass: 'badge-ghost',
      color: '#b844ff',
      filter: 'none',
      avatarSrc: 'assets/images/ship_chrono_phantom.png',
      spriteKey: 'ship_chrono_phantom',
      speed: 395,
      firepowerLabel: 'TACHYON NEEDLE BEAM',
      hpLabel: 'HIGH MOBILITY (3 LIVES)',
      extraLives: 0,
      uniquePowerups: ['QUANTUM_CLONES', 'VOID_NEEDLE'],
      surviveName: 'CHRONO WARP',
      surviveDesc: 'TEMPORAL WARP (70% TIME DILATION)',
      ultName: 'SINGULARITY RIFT',
      ultDesc: 'SINGULARITY VORTEX FIELD'
    }
  };

  // Multi-Language Localization Dictionary (i18n)
  const TRANSLATIONS = {
    id: {
      subTitle: 'RETRO ARCADE SPACE RUNNER',
      shipBadge: 'PESAWAT : STELLA NOVA',
      howToPlayTitle: 'CARA MAIN',
      howToPlay1: '🎮 <strong>W / S</strong> atau <strong>Panah Atas / Bawah</strong> : Naik / Turun',
      howToPlay2: '🕹️ <strong>A / D</strong> atau <strong>Panah Kiri / Kanan</strong> : Mundur / Maju',
      howToPlay3: '💥 <strong>Tembakan Otomatis</strong> meluncur terus ke arah kanan',
      howToPlay4: '🌟 <strong>SPACE / SHIFT / Tombol Ult</strong> : Stellar Blaster (Laser Horizontal Layar Penuh)',
      howToPlay5: '⏱️ Bertahanlah selama mungkin untuk mencatat rekor waktu!',
      diffSelectLabel: 'PILIH TINGKAT KESULITAN:',
      diffEasyMeta: '4 Nyawa • 0.8x',
      diffNormalMeta: 'Standar • 1.0x',
      diffHardMeta: 'Agresif • 1.5x',
      diffHardcorezMeta: 'Touhou Danmaku • 2.5x',
      btnStart: 'MULAI MAIN',
      btnLeaderboard: '🏆 TOP PILOT',
      btnHowToPlay: '❓ CARA MAIN',
      btnFullscreen: 'LAYAR PENUH',
      quickAutoFire: 'Auto-Fire',
      quickUlt: 'Ult: SPACE',
      startHint: 'Tekan [SPACE] / [ENTER] untuk mulai • [V] Ganti Mode Layar • [F] Layar Penuh',

      howToPlayModalTitle: 'PANDUAN KONTROL & CARA MAIN',
      helpSecControls: '🎮 KONTROL PENERBANGAN',
      helpUpDown: 'Manuver Naik / Turun (atau Panah Atas/Bawah)',
      helpLeftRight: 'Maju / Mundur (atau Panah Kiri/Kanan)',
      helpAutoFire: 'Tembakan otomatis meluncur ke kanan non-stop',
      helpUlt: 'Stellar Blaster (Laser Layar Penuh saat Ult penuh)',
      helpSecPowerups: '⚡ POWER-UP & ITEM',
      powerupHeartDesc: 'Memulihkan 1 nyawa pesawat',
      powerupNovaDesc: 'Menambah tembakan menyebar (Spread Shot)',
      powerupShieldDesc: 'Perisai kebal dari tabrakan meteor & proyektil',
      btnCloseHelp: 'SIAP TERBANG 🚀',

      hudScore: 'SKOR',
      hudSurvived: 'BERTAHAN',
      hudHiScore: 'HI-SKOR',

      bossWarningTitle: '⚠️ PERINGATAN BOS ⚠️',
      bossWarningMini: 'VOID DESTROYER MENDEKAT!',
      bossWarningBig: 'GOLIATH MOTHERSHIP MENDEKAT!',

      lblFinalDiff: 'Tingkat Kesulitan:',
      lblFinalTime: '⏱️ Waktu Bertahan:',
      lblFinalBestTime: '👑 Waktu Terbaik:',
      lblFinalScore: 'Skor Akhir:',
      lblFinalHighScore: 'Skor Tertinggi:',
      newRecordBadge: '🏆 REKOR BARU DICAPAI! 🏆',
      submitTitle: '📡 CATAT REKOR KE HALL OF FAME:',
      pilotInputPlaceholder: 'NAMA PILOT',
      btnSubmit: 'KIRIM 🚀',
      btnRestart: 'MAIN LAGI',
      btnMenu: '🏠 MENU / LEVEL',
      gameOverHint: 'Tekan [SPACE] / [ENTER] / [R] untuk restart, [M] untuk Menu',

      pauseTitle: 'GAME DIJEDA',
      pauseDesc: 'Tekan [P] atau [ESC] untuk melanjutkan',
      btnResume: 'LANJUTKAN',
      btnMenuPause: '🏠 MENU / GANTI LEVEL',
      pauseHint: 'Tekan [M] untuk kembali ke Menu Utama',

      modalTitle: '🏆 TOP 10 PILOT GLOBAL',
      colPilot: 'PILOT',
      colDiff: 'MODE',
      colScore: 'SKOR',
      colSurvived: 'BERTAHAN',
      loadingText: '📡 MENGAMBIL DATA DARI SATELIT...',
      emptyText: 'Belum ada rekor yang tercatat. Jadilah yang pertama!',
      btnRefresh: '↻ REFRESH',
      btnClose: '✕ TUTUP',

      textLife: '+1 NYAWA ❤️',
      textUltReady: 'ULT SIAP! [SPACE]',
      textNewRecord: 'REKOR BARU! 🏆'
    },
    en: {
      subTitle: 'RETRO ARCADE SPACE RUNNER',
      shipBadge: 'SHIP : STELLA NOVA',
      howToPlayTitle: 'HOW TO PLAY',
      howToPlay1: '🎮 <strong>W / S</strong> or <strong>Up / Down Arrows</strong> : Fly Up / Down',
      howToPlay2: '🕹️ <strong>A / D</strong> or <strong>Left / Right Arrows</strong> : Move Back / Forward',
      howToPlay3: '💥 <strong>Auto-Fire</strong> continuously shoots to the right',
      howToPlay4: '🌟 <strong>SPACE / SHIFT / Ult Button</strong> : Stellar Blaster (Full-Screen Beam)',
      howToPlay5: '⏱️ Survive as long as you can to set high score records!',
      diffSelectLabel: 'SELECT DIFFICULTY:',
      diffEasyMeta: '4 Lives • 0.8x',
      diffNormalMeta: 'Standard • 1.0x',
      diffHardMeta: 'Aggressive • 1.5x',
      diffHardcorezMeta: 'Touhou Danmaku • 2.5x',
      btnStart: 'PLAY NOW',
      btnLeaderboard: '🏆 TOP PILOTS',
      btnHowToPlay: '❓ HOW TO PLAY',
      btnFullscreen: 'FULLSCREEN',
      quickAutoFire: 'Auto-Fire',
      quickUlt: 'Ult: SPACE',
      startHint: 'Press [SPACE] / [ENTER] to start • [V] Switch Display Mode • [F] Fullscreen',

      howToPlayModalTitle: 'FLIGHT MANUAL & CONTROLS',
      helpSecControls: '🎮 FLIGHT CONTROLS',
      helpUpDown: 'Fly Up / Down (or Up/Down Arrows)',
      helpLeftRight: 'Move Forward / Back (or Left/Right Arrows)',
      helpAutoFire: 'Auto-fires continuously to the right',
      helpUlt: 'Stellar Blaster (Full-Screen Beam when Ult is full)',
      helpSecPowerups: '⚡ POWER-UPS & ITEMS',
      powerupHeartDesc: 'Restores 1 ship life',
      powerupNovaDesc: 'Upgrades weapon with Spread Shot',
      powerupShieldDesc: 'Invulnerable shield against enemies & meteors',
      btnCloseHelp: 'READY TO FLY 🚀',

      hudScore: 'SCORE',
      hudSurvived: 'SURVIVED',
      hudHiScore: 'HI-SCORE',

      bossWarningTitle: '⚠️ BOSS WARNING ⚠️',
      bossWarningMini: 'VOID DESTROYER APPROACHING!',
      bossWarningBig: 'GOLIATH MOTHERSHIP APPROACHING!',

      lblFinalDiff: 'Difficulty:',
      lblFinalTime: '⏱️ Survived Time:',
      lblFinalBestTime: '👑 Best Record:',
      lblFinalScore: 'Final Score:',
      lblFinalHighScore: 'High Score:',
      newRecordBadge: '🏆 NEW RECORD ACHIEVED! 🏆',
      submitTitle: '📡 SUBMIT RECORD TO HALL OF FAME:',
      pilotInputPlaceholder: 'PILOT NAME',
      btnSubmit: 'SUBMIT 🚀',
      btnRestart: 'PLAY AGAIN',
      btnMenu: '🏠 MAIN MENU',
      gameOverHint: 'Press [SPACE] / [ENTER] / [R] to restart, [M] for Menu',

      pauseTitle: 'GAME PAUSED',
      pauseDesc: 'Press [P] or [ESC] to resume',
      btnResume: 'RESUME',
      btnMenuPause: '🏠 MAIN MENU',
      pauseHint: 'Press [M] to return to Main Menu',

      modalTitle: '🏆 GLOBAL TOP 10 PILOTS',
      colPilot: 'PILOT',
      colDiff: 'MODE',
      colScore: 'SCORE',
      colSurvived: 'SURVIVED',
      loadingText: '📡 RETRIEVING SATELLITE DATA...',
      emptyText: 'No records recorded yet. Be the first pilot!',
      btnRefresh: '↻ REFRESH',
      btnClose: '✕ CLOSE',

      textLife: '+1 LIFE ❤️',
      textUltReady: 'ULT READY! [SPACE]',
      textNewRecord: 'NEW RECORD! 🏆'
    }
  };

  // --- Game Engine State ---
  const state = {
    lang: 'id',
    difficulty: 'normal',
    displayMode: 'immersive', // 'immersive' (full view) | 'cabinet' (retro arcade cabinet)
    screen: 'start', // 'start', 'playing', 'paused', 'gameover'
    score: 0,
    highScore: 0,
    survivalTime: 0, // in seconds
    bestSurvivalTime: 0, // in seconds
    lives: 3,
    maxLives: 3,
    ultCharge: 0,
    maxUltCharge: 100,
    isUltActive: false,
    ultDuration: 0,
    screenShake: 0,
    difficultyMultiplier: 1.0,
    lastTime: 0,
    meteorSpawnTimer: 0,
    wallSpawnTimer: 0,
    nextBossCheckpoint: 60,
    bossCycle: 1,
    activeBoss: null,
    bossWarningActive: false,
    warningTimer: 0,
    selectedShip: localStorage.getItem('starfall_selected_ship') || 'stella_nova',
    surviveSkillCooldown: 0,
    surviveSkillMaxCooldown: 25,
    chronoSlowMotionTimer: 0,
    bgCurrent: { r: 10, g: 8, b: 20 },
    bgTarget: { r: 10, g: 8, b: 20 },
  };

  // Input states (Up, Down, Left, Right)
  const input = {
    up: false,
    down: false,
    left: false,
    right: false,
    touchTarget: null // { x, y }
  };

  // Entities
  let player;
  let projectiles = [];
  let meteors = [];
  let powerUps = [];
  let particles = [];
  let explosionAnims = [];
  let floatingTexts = [];
  let stars = [];
  let enemyBullets = [];

  // Canvas elements
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // HUD elements
  const scoreVal = document.getElementById('scoreVal');
  const highScoreVal = document.getElementById('highScoreVal');
  const timerVal = document.getElementById('timerVal');
  const heartsContainer = document.getElementById('heartsContainer');
  const ultProgressBar = document.getElementById('ultProgressBar');
  const ultContainer = document.querySelector('.ult-bar-container');
  const activeBuffsEl = document.getElementById('activeBuffs');

  // Boss UI elements
  const bossBarContainer = document.getElementById('bossBarContainer');
  const bossBarAvatar = document.getElementById('bossBarAvatar');
  const bossName = document.getElementById('bossName');
  const bossHpPercent = document.getElementById('bossHpPercent');
  const bossHpFill = document.getElementById('bossHpFill');
  const bossWarningBanner = document.getElementById('bossWarningBanner');
  const bossWarningAvatar = document.getElementById('bossWarningAvatar');
  const warningSub = document.getElementById('warningSub');

  function showBossBar(boss) {
    if (bossBarContainer) bossBarContainer.classList.remove('hidden');
    const isObj = (typeof boss === 'object' && boss !== null);
    const title = isObj ? `#${String(boss.id).padStart(3, '0')} ${boss.name.toUpperCase()}` : boss;
    if (bossName) bossName.textContent = title;
    const bossSubtitle = document.getElementById('bossSubtitle');
    if (bossSubtitle) {
      if (isObj && boss.title) {
        bossSubtitle.textContent = boss.title.toUpperCase();
        bossSubtitle.style.color = boss.color || '#ff0055';
      } else {
        bossSubtitle.textContent = '';
      }
    }
    if (bossBarAvatar) {
      const arch = (isObj && boss.archetype) ? boss.archetype : (isObj && boss.type === 'bigboss' ? 'mecha' : 'monster');
      const avatarMap = {
        spaceship: 'assets/images/boss_spaceship_dreadnought.png',
        mecha: 'assets/images/boss_mecha_titan.png',
        monster: 'assets/images/boss_alien_leviathan.png',
        humanoid: 'assets/images/boss_humanoid_valkyrie.png',
        alien: 'assets/images/boss_eldritch_eye.png'
      };
      bossBarAvatar.src = avatarMap[arch] || (isObj && boss.type === 'bigboss' ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png');
      if (isObj && boss.color) bossBarAvatar.style.borderColor = boss.color;
    }
    updateBossHpBar(isObj ? boss.hp : 1, isObj ? boss.maxHp : 1);
  }

  function updateBossHpBar(current, max) {
    if (!bossHpFill || !bossHpPercent) return;
    const pct = Math.max(0, Math.min(100, (current / max) * 100));
    bossHpFill.style.width = `${pct}%`;
    bossHpPercent.textContent = `${Math.ceil(pct)}%`;
  }

  function hideBossBar() {
    if (bossBarContainer) bossBarContainer.classList.add('hidden');
  }

  // Screen overlays
  const startScreen = document.getElementById('startScreen');
  const gameOverScreen = document.getElementById('gameOverScreen');
  const pauseScreen = document.getElementById('pauseScreen');
  const finalScore = document.getElementById('finalScore');
  const finalHighScore = document.getElementById('finalHighScore');
  const finalTime = document.getElementById('finalTime');
  const finalBestTime = document.getElementById('finalBestTime');
  const newRecordBadge = document.getElementById('newRecordBadge');

  // Buttons
  const btnStart = document.getElementById('btnStart');
  const btnRestart = document.getElementById('btnRestart');
  const btnResume = document.getElementById('btnResume');
  const btnMenuGameOver = document.getElementById('btnMenuGameOver');
  const btnMenuPause = document.getElementById('btnMenuPause');
  const btnToggleSound = document.getElementById('btnToggleSound');
  const btnTogglePause = document.getElementById('btnTogglePause');
  const btnToggleLang = document.getElementById('btnToggleLang');
  const btnToggleDisplay = document.getElementById('btnToggleDisplay');
  const btnToggleFullscreen = document.getElementById('btnToggleFullscreen');
  const btnTouchUp = document.getElementById('btnTouchUp');
  const btnTouchDown = document.getElementById('btnTouchDown');
  const btnTouchLeft = document.getElementById('btnTouchLeft');
  const btnTouchRight = document.getElementById('btnTouchRight');
  const btnTouchUlt = document.getElementById('btnTouchUlt');

  // Leaderboard & Submit Elements
  const leaderboardModal = document.getElementById('leaderboardModal');
  const btnCloseLeaderboard = document.getElementById('btnCloseLeaderboard');
  const btnCloseLeaderboardBottom = document.getElementById('btnCloseLeaderboardBottom');
  const btnLeaderboardStart = document.getElementById('btnLeaderboardStart');
  const btnLeaderboardGameOver = document.getElementById('btnLeaderboardGameOver');
  const btnRefreshLeaderboard = document.getElementById('btnRefreshLeaderboard');
  const leaderboardLoading = document.getElementById('leaderboardLoading');
  const leaderboardTable = document.getElementById('leaderboardTable');
  const leaderboardBody = document.getElementById('leaderboardBody');
  const leaderboardEmpty = document.getElementById('leaderboardEmpty');

  // How to Play Modal Elements
  const howToPlayModal = document.getElementById('howToPlayModal');
  const btnHowToPlayStart = document.getElementById('btnHowToPlayStart');
  const btnCloseHowToPlay = document.getElementById('btnCloseHowToPlay');
  const btnCloseHowToPlayBottom = document.getElementById('btnCloseHowToPlayBottom');
  const btnFullscreenStart = document.getElementById('btnFullscreenStart');

  const submitScoreSection = document.getElementById('submitScoreSection');
  const pilotNameInput = document.getElementById('pilotNameInput');
  const btnSubmitScore = document.getElementById('btnSubmitScore');
  const submitStatusMsg = document.getElementById('submitStatusMsg');

  // Difficulty HUD & Overlays
  const hudDiffBadge = document.getElementById('hudDiffBadge');
  const finalDiff = document.getElementById('finalDiff');

  let isSubmittingScore = false;

  // Format seconds to mm:ss
  function formatTime(totalSeconds) {
    const mins = Math.floor(totalSeconds / 60);
    const secs = Math.floor(totalSeconds % 60);
    const mStr = mins < 10 ? '0' + mins : mins;
    const sStr = secs < 10 ? '0' + secs : secs;
    return `${mStr}:${sStr}`;
  }

  // --- Difficulty Functions ---
  function updateHudDifficultyBadge() {
    if (!hudDiffBadge) return;
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    hudDiffBadge.textContent = conf.label;
    hudDiffBadge.className = `hud-diff-badge diff-${state.difficulty}`;
  }

  function setDifficulty(diffKey) {
    if (!DIFFICULTY_CONFIGS[diffKey]) return;
    state.difficulty = diffKey;
    localStorage.setItem('starfall_difficulty', diffKey);

    document.querySelectorAll('.diff-btn').forEach(btn => {
      if (btn.dataset.diff === diffKey) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    updateHudDifficultyBadge();
    const conf = DIFFICULTY_CONFIGS[diffKey];
    state.lives = conf.lives;
    state.maxLives = conf.lives;
    updateHeartsDisplay();
  }

  function setLanguage(lang) {
    if (!TRANSLATIONS[lang]) lang = 'id';
    state.lang = lang;
    localStorage.setItem('starfall_lang', lang);

    const t = TRANSLATIONS[lang];

    // Update all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) {
        el.innerHTML = t[key];
      }
    });

    // Update input placeholder
    if (pilotNameInput && t.pilotInputPlaceholder) {
      pilotNameInput.placeholder = t.pilotInputPlaceholder;
    }

    // Update active lang buttons
    document.querySelectorAll('.lang-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });

    if (btnToggleLang) {
      btnToggleLang.title = lang === 'id' ? 'Ganti Bahasa (English)' : 'Switch Language (Bahasa Indonesia)';
      btnToggleLang.textContent = lang === 'id' ? 'ID' : 'EN';
    }

    updateHudDifficultyBadge();
  }

  function toggleFullscreen() {
    const container = document.getElementById('game-container');
    if (!container) return;
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {
      if (container.requestFullscreen) {
        container.requestFullscreen().catch(() => {});
      } else if (container.webkitRequestFullscreen) {
        container.webkitRequestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      }
    }
  }

  function setDisplayMode(mode) {
    if (mode !== 'cabinet' && mode !== 'immersive') {
      mode = 'immersive';
    }
    state.displayMode = mode;
    localStorage.setItem('starfall_display_mode', mode);

    const container = document.getElementById('game-container');
    if (container) {
      container.classList.remove('mode-immersive', 'mode-cabinet');
      container.classList.add(mode === 'cabinet' ? 'mode-cabinet' : 'mode-immersive');
    }

    document.querySelectorAll('.mode-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-mode') === mode);
    });

    if (btnToggleDisplay) {
      const isCabinet = (mode === 'cabinet');
      btnToggleDisplay.textContent = isCabinet ? '📺' : '⛶';
      btnToggleDisplay.title = isCabinet
        ? (state.lang === 'id' ? 'Mode: Arcade Cabinet (Klik untuk Layar Penuh)' : 'Mode: Arcade Cabinet (Click for Full View)')
        : (state.lang === 'id' ? 'Mode: Layar Penuh (Klik untuk Arcade Cabinet)' : 'Mode: Full View (Click for Arcade Cabinet)');
    }
  }

  function toggleDisplayMode() {
    const nextMode = state.displayMode === 'cabinet' ? 'immersive' : 'cabinet';
    setDisplayMode(nextMode);
  }

  // --- Leaderboard System ---

  // --- Boss Codex (100 Bosses Catalog Modal) ---
  let activeCodexTier = 'easy';

  function openBossCodex() {
    const modal = document.getElementById('bossCodexModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    renderBossCodex(activeCodexTier);
    if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
  }

  function closeBossCodex() {
    const modal = document.getElementById('bossCodexModal');
    if (modal) modal.classList.add('hidden');
  }

  function renderBossCodex(tier) {
    activeCodexTier = tier;
    const grid = document.getElementById('bossCodexGrid');
    if (!grid || !window.BOSS_CATALOG) return;

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tier === tier);
    });

    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
    const archBadges = {
      spaceship: '🛸 KAPAL',
      mecha: '🤖 MECHA',
      monster: '👾 MONSTER',
      humanoid: '👤 ORANG',
      alien: '👁️ ALIEN'
    };

    grid.innerHTML = tierBosses.map(b => {
      const isBig = b.isBig;
      const badgeClass = isBig ? 'codex-badge-big' : 'codex-badge-mini';
      const tierText = isBig ? '👑 BIG' : '👾 MINI';
      const archText = archBadges[b.archetype] || '👾 ENEMY';
      return `
        <div class="codex-card" style="border-left: 3px solid ${b.color};">
          <div class="codex-card-top">
            <span class="codex-id" style="color: ${b.color};">#${String(b.id).padStart(3, '0')}</span>
            <div style="display: flex; gap: 4px;">
              <span class="codex-badge" style="background: rgba(255,255,255,0.08); color: #fff;">${archText}</span>
              <span class="codex-badge ${badgeClass}">${tierText}</span>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;">
            <img src="assets/images/boss_${b.archetype}.png" alt="${b.name}" style="width: 44px; height: 32px; object-fit: contain; filter: drop-shadow(0 0 4px ${b.color});">
            <div>
              <div class="codex-name">${b.name}</div>
              <div class="codex-title">${b.title}</div>
            </div>
          </div>
          <div class="codex-stats-row">
            <span>HP: <strong>${b.baseHp}</strong></span>
            <span>ATK: <strong>${b.attack.toUpperCase()}</strong></span>
          </div>
        </div>
      `;
    }).join('');
  }

  function openLeaderboard() {
    if (!leaderboardModal) return;
    leaderboardModal.classList.remove('hidden');
    if (document.activeElement && document.activeElement.blur) {
      document.activeElement.blur();
    }
    fetchLeaderboard();
  }

  function closeLeaderboard() {
    if (!leaderboardModal) return;
    leaderboardModal.classList.add('hidden');
  }

  // --- Flight Academy (How to Play) Modal ---
  function openHowToPlay() {
    if (!howToPlayModal) return;
    howToPlayModal.classList.remove('hidden');
    if (document.activeElement && document.activeElement.blur) {
      document.activeElement.blur();
    }
    if (window.soundFx) window.soundFx.playPowerup();
  }

  function closeHowToPlay() {
    if (!howToPlayModal) return;
    howToPlayModal.classList.add('hidden');
  }

  async function fetchLeaderboard() {
    if (!leaderboardBody) return;
    leaderboardLoading.classList.remove('hidden');
    leaderboardTable.classList.add('hidden');
    leaderboardEmpty.classList.add('hidden');

    try {
      const response = await fetch('/api/leaderboard');
      if (!response.ok) throw new Error('API request failed');
      const data = await response.json();
      renderLeaderboardRows(data.leaderboard || []);
    } catch (err) {
      // Offline fallback: display local device record
      const savedHi = parseInt(localStorage.getItem('starfall_high_score'), 10) || 0;
      const savedTime = parseFloat(localStorage.getItem('starfall_best_time')) || 0;
      const savedName = localStorage.getItem('starfall_pilot_name') || 'YOU (LOCAL)';

      if (savedHi > 0) {
        renderLeaderboardRows([
          { rank: 1, name: savedName, score: savedHi, formattedTime: formatTime(savedTime) }
        ]);
      } else {
        leaderboardLoading.classList.add('hidden');
        leaderboardEmpty.classList.remove('hidden');
      }
    }
  }

  function renderLeaderboardRows(entries) {
    leaderboardLoading.classList.add('hidden');
    if (!entries || entries.length === 0) {
      leaderboardTable.classList.add('hidden');
      leaderboardEmpty.classList.remove('hidden');
      return;
    }

    leaderboardEmpty.classList.add('hidden');
    leaderboardBody.innerHTML = '';
    entries.forEach((item, index) => {
      const tr = document.createElement('tr');
      const rank = item.rank || (index + 1);
      if (rank === 1) tr.className = 'rank-badge-1';
      else if (rank === 2) tr.className = 'rank-badge-2';
      else if (rank === 3) tr.className = 'rank-badge-3';

      const rankBadge = rank === 1 ? '🥇 1' : rank === 2 ? '🥈 2' : rank === 3 ? '🥉 3' : `${rank}`;
      const diffKey = item.diff || 'normal';
      const diffLabel = diffKey === 'hardcorez' ? 'HARDCOREZ' : diffKey.toUpperCase();
      const diffTag = `<span class="diff-tag diff-tag-${diffKey}">${diffLabel}</span>`;

      tr.innerHTML = `
        <td class="col-rank">${rankBadge}</td>
        <td class="col-name">${item.name}</td>
        <td class="col-diff">${diffTag}</td>
        <td class="col-score">${(Number(item.score) || 0).toLocaleString()}</td>
        <td class="col-time">${item.formattedTime || formatTime(item.time || 0)}</td>
      `;
      leaderboardBody.appendChild(tr);
    });

    leaderboardTable.classList.remove('hidden');
  }

  async function submitPilotScore() {
    if (isSubmittingScore) return;
    const name = (pilotNameInput.value || '').trim().toUpperCase();
    if (name.length < 2) {
      showSubmitStatus('Nama pilot minimal 2 karakter!', 'error');
      pilotNameInput.focus();
      return;
    }

    if (state.score <= 0) {
      showSubmitStatus('Skor harus lebih dari 0 untuk dicatat!', 'error');
      return;
    }

    isSubmittingScore = true;
    btnSubmitScore.disabled = true;
    showSubmitStatus('📡 Menghubungkan ke satelit...', 'loading');

    localStorage.setItem('starfall_pilot_name', name);

    try {
      const response = await fetch('/api/leaderboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          score: state.score,
          time: Math.floor(state.survivalTime),
          diff: state.difficulty
        })
      });

      const resData = await response.json();
      if (!response.ok) {
        throw new Error(resData.error || 'Gagal mengirim skor');
      }

      showSubmitStatus('✅ Skor berhasil tercatat di Hall of Fame!', 'success');
      setTimeout(() => {
        openLeaderboard();
      }, 1100);
    } catch (err) {
      showSubmitStatus('⚠️ Tersimpan di rekor lokal (mode offline).', 'success');
      btnSubmitScore.disabled = false;
      isSubmittingScore = false;
    }
  }

  function showSubmitStatus(text, type) {
    if (!submitStatusMsg) return;
    submitStatusMsg.textContent = text;
    submitStatusMsg.className = `submit-status-msg ${type}`;
  }

  // --- Starfield Background (Horizontal Motion) ---
  function initStarfield() {
    stars = [];
    for (let i = 0; i < 90; i++) {
      stars.push({
        x: Math.random() * CANVAS_WIDTH,
        y: Math.random() * CANVAS_HEIGHT,
        size: Math.random() < 0.2 ? 2.5 : Math.random() < 0.5 ? 1.5 : 1,
        speed: 1.2 + Math.random() * 3.5,
        alpha: 0.3 + Math.random() * 0.7,
        color: Math.random() < 0.25 ? '#00f3ff' : Math.random() < 0.35 ? '#ff2a85' : '#ffffff'
      });
    }
  }

  // --- Player Object (Starfighter Ship) ---
  class Player {
    constructor() {
      const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;
      this.shipId = shipConf.id;
      this.width = 46;
      this.height = 38;
      this.x = 90;
      this.y = CANVAS_HEIGHT / 2;
      this.speed = shipConf.speed;
      this.shootCooldown = 0;
      this.baseFireInterval = shipConf.id === 'aether_vanguard' ? 0.24 : shipConf.id === 'chrono_phantom' ? 0.13 : 0.18;
      this.invulnerableTimer = 0;
      this.buffs = {
        rapid: 0,
        multi: 0,
        pierce: shipConf.id === 'chrono_phantom' ? 999999 : 0,
        burst: shipConf.id === 'aether_vanguard' ? 999999 : 0,
        shield: 0,
        // Character-Specific Unique Powerups
        hyperdrive: 0,
        plasma_spread: 0,
        heavy_flak: 0,
        tesla_coil: 0,
        quantum_clones: 0,
        void_needle: 0
      };
      this.teslaTimer = 0;
      this.tilt = 0; // vertical banking angle
    }

    update(dt) {
      let moveX = 0;
      let moveY = 0;

      if (input.up) moveY -= 1;
      if (input.down) moveY += 1;
      if (input.left) moveX -= 1;
      if (input.right) moveX += 1;

      // Touch / pointer direct tracking
      if (input.touchTarget) {
        const dx = input.touchTarget.x - this.x;
        const dy = input.touchTarget.y - this.y;
        if (Math.abs(dx) > 6) moveX = Math.sign(dx);
        if (Math.abs(dy) > 6) moveY = Math.sign(dy);
      }

      this.x += moveX * this.speed * dt;
      this.y += moveY * this.speed * dt;
      this.tilt = moveY * 0.18;

      // Clamping within play bounds (full screen movement)
      const halfW = this.width / 2;
      const halfH = this.height / 2;
      if (this.x < halfW + 15) this.x = halfW + 15;
      if (this.x > CANVAS_WIDTH - halfW - 20) this.x = CANVAS_WIDTH - halfW - 20;
      if (this.y < halfH + 20) this.y = halfH + 20;
      if (this.y > CANVAS_HEIGHT - halfH - 20) this.y = CANVAS_HEIGHT - halfH - 20;

      // Buff timers
      for (const buff in this.buffs) {
        if (this.buffs[buff] > 0 && this.buffs[buff] < 9999) {
          this.buffs[buff] -= dt;
          if (this.buffs[buff] <= 0) this.buffs[buff] = 0;
        }
      }

      // Invulnerability blink timer
      if (this.invulnerableTimer > 0) {
        this.invulnerableTimer -= dt;
      }

      // Automatic Tesla Coil Zap (Aether Vanguard)
      if (this.buffs.tesla_coil > 0) {
        this.teslaTimer -= dt;
        if (this.teslaTimer <= 0) {
          this.teslaTimer = 0.26;
          fireTeslaChainLightning(this.x, this.y);
        }
      }

      // Auto-Shooting towards RIGHT (Tuned for Hyperdrive / Rapid)
      let currentFireInterval = this.baseFireInterval;
      if (this.buffs.hyperdrive > 0) {
        currentFireInterval = this.baseFireInterval * 0.35; // 3x speed overdrive
      } else if (this.buffs.rapid > 0) {
        currentFireInterval = this.baseFireInterval * 0.5;
      }

      this.shootCooldown -= dt;
      if (this.shootCooldown <= 0) {
        this.shoot();
        this.shootCooldown = currentFireInterval;
      }
    }

    shoot() {
      const isPierce = this.buffs.pierce > 0 || this.buffs.void_needle > 0;
      const isMulti = this.buffs.multi > 0 || this.buffs.plasma_spread > 0;
      const isBurst = this.buffs.burst > 0 || this.buffs.heavy_flak > 0;
      const isRapid = this.buffs.rapid > 0 || this.buffs.hyperdrive > 0;
      const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;

      window.soundFx.playShoot();
      const cannonX = this.x + 20;

      // Helper for shooting a cluster of shots (supports Quantum Clones)
      const spawnShotCluster = (originX, originY, scale = 1.0) => {
        if (shipConf.id === 'aether_vanguard') {
          // AETHER VANGUARD: Heavy Flak Explosive Artillery
          if (this.buffs.heavy_flak > 0) {
            projectiles.push(new Projectile(originX, originY, 680, 0, false, true, true, true));
            projectiles.push(new Projectile(originX - 6, originY - 18, 640, -140, false, true, false, true));
            projectiles.push(new Projectile(originX - 6, originY + 18, 640, 140, false, true, false, true));
            projectiles.push(new Projectile(originX - 12, originY - 32, 600, -260, false, true, false, true));
            projectiles.push(new Projectile(originX - 12, originY + 32, 600, 260, false, true, false, true));
          } else {
            projectiles.push(new Projectile(originX, originY, 650, 0, isPierce, true, isRapid, true));
            projectiles.push(new Projectile(originX - 4, originY - 14, 620, -110, isPierce, true, isRapid, true));
            projectiles.push(new Projectile(originX - 4, originY + 14, 620, 110, isPierce, true, isRapid, true));
          }
        } else if (shipConf.id === 'chrono_phantom') {
          // CHRONO PHANTOM: Infinite Piercing Tachyon Needle Laser
          if (this.buffs.void_needle > 0) {
            projectiles.push(new Projectile(originX, originY, 1150, 0, true, false, true, false));
            projectiles.push(new Projectile(originX, originY - 8, 1100, -45, true, false, true, false));
            projectiles.push(new Projectile(originX, originY + 8, 1100, 45, true, false, true, false));
          } else {
            projectiles.push(new Projectile(originX, originY - 6, 920, 0, true, isBurst, isRapid, false));
            projectiles.push(new Projectile(originX, originY + 6, 920, 0, true, isBurst, isRapid, false));
          }
        } else {
          // STELLA NOVA: Rapid Twin Cannon / 5-Way Plasma Spread
          if (this.buffs.plasma_spread > 0) {
            const angles = [-0.32, -0.16, 0, 0.16, 0.32];
            angles.forEach(ang => {
              projectiles.push(new Projectile(originX, originY, Math.cos(ang) * 760, Math.sin(ang) * 760, isPierce, isBurst, isRapid, true));
            });
          } else if (this.buffs.hyperdrive > 0) {
            projectiles.push(new Projectile(originX + 6, originY - 10, 880, 0, true, isBurst, true, false));
            projectiles.push(new Projectile(originX + 6, originY + 10, 880, 0, true, isBurst, true, false));
            projectiles.push(new Projectile(originX - 4, originY, 820, 0, false, false, true, true));
          } else if (isMulti) {
            projectiles.push(new Projectile(originX, originY, 750, 0, isPierce, isBurst, isRapid, true));
            projectiles.push(new Projectile(originX - 4, originY - 12, 700, -140, isPierce, isBurst, isRapid, true));
            projectiles.push(new Projectile(originX - 4, originY + 12, 700, 140, isPierce, isBurst, isRapid, true));
          } else {
            projectiles.push(new Projectile(originX, originY - 8, 750, 0, isPierce, isBurst, isRapid, false));
            projectiles.push(new Projectile(originX, originY + 8, 750, 0, isPierce, isBurst, isRapid, false));
          }
        }
      };

      spawnShotCluster(cannonX, this.y);

      // Quantum Hologram Clones: Dual flanking shadow ships mirror the attack!
      if (this.buffs.quantum_clones > 0) {
        spawnShotCluster(cannonX - 12, this.y - 34, 0.7);
        spawnShotCluster(cannonX - 12, this.y + 34, 0.7);
      }

      createMuzzleSparks(cannonX + 4, this.y);
    }

    draw(ctx) {
      if (this.invulnerableTimer > 0 && Math.floor(Date.now() / 80) % 2 === 0) {
        return;
      }

      // 3D Cosmic Shield Back Half (Behind Ship)
      if (this.buffs.shield > 0) {
        draw3DShieldBack(ctx, this.x, this.y, this.buffs.shield);
      }

      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.tilt);

      // 1. Jet Thruster Flames (Blasting out to the LEFT)
      const flameLen = 14 + Math.random() * 10;
      const grad = ctx.createLinearGradient(-18, 0, -18 - flameLen, 0);
      grad.addColorStop(0, '#00f3ff');
      grad.addColorStop(0.5, '#ff2a85');
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.moveTo(-16, -7);
      ctx.lineTo(-16 - flameLen, 0);
      ctx.lineTo(-16, 7);
      ctx.closePath();
      ctx.fill();

      // 2. Starfighter Hull (Unique High-Res Arcade Sprites for Each Ship)
      const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;
      const spriteKey = 'ship_' + (shipConf.id || 'stella_nova');
      const shipImg = assets.images[spriteKey] || assets.images['player_ship'];

      if (shipImg && shipImg.complete && shipImg.naturalWidth > 0) {
        const targetW = shipConf.id === 'aether_vanguard' ? 68 : shipConf.id === 'chrono_phantom' ? 64 : 60;
        const nw = shipImg.naturalWidth || shipImg.width;
        const nh = shipImg.naturalHeight || shipImg.height;
        const targetH = targetW * (nh / nw);

        ctx.save();
        ctx.drawImage(shipImg, -targetW / 2 + 2, -targetH / 2, targetW, targetH);
        ctx.restore();

        // Draw Quantum Clones (Translucent Holographic Shadow Ships)
        if (this.buffs.quantum_clones > 0) {
          [-34, 34].forEach(offsetY => {
            ctx.save();
            ctx.globalAlpha = 0.55 + Math.sin(Date.now() * 0.01 + offsetY) * 0.15;
            ctx.translate(-12, offsetY);
            ctx.shadowColor = '#e0aaff';
            ctx.shadowBlur = 12;
            ctx.drawImage(shipImg, -targetW * 0.4, -targetH * 0.4, targetW * 0.8, targetH * 0.8);
            ctx.restore();
          });
        }
      } else {
        // Procedural Starfighter Wings & Stabilizers
        ctx.fillStyle = '#ff2a85';
        ctx.beginPath();
        ctx.moveTo(-6, -8);
        ctx.quadraticCurveTo(-18, -20, -28, -14);
        ctx.quadraticCurveTo(-16, -8, -6, -3);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(-6, 8);
        ctx.quadraticCurveTo(-18, 20, -28, 14);
        ctx.quadraticCurveTo(-16, 8, -6, 3);
        ctx.fill();

        // Hull
        ctx.fillStyle = '#f0eeff';
        ctx.beginPath();
        ctx.roundRect(-16, -14, 32, 28, 8);
        ctx.fill();
        ctx.strokeStyle = '#2b1b4d';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Cockpit Visor
        ctx.fillStyle = '#00f3ff';
        ctx.beginPath();
        ctx.arc(4, 0, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(6, -3, 3, 0, Math.PI * 2);
        ctx.fill();

        // Blaster Cannons
        ctx.fillStyle = '#ffd000';
        ctx.fillRect(8, -15, 14, 5);
        ctx.fillRect(8, 10, 14, 5);
        ctx.fillStyle = '#ff2a85';
        ctx.fillRect(20, -16, 5, 7);
        ctx.fillRect(20, 9, 5, 7);
      }

      // Star emblem on hull
      ctx.fillStyle = '#ffd000';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('★', -4, 4);

      // Force-field glow during Ultimate
      if (state.isUltActive) {
        ctx.strokeStyle = '#00f3ff';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.arc(0, 0, 30, 0, Math.PI * 2);
        ctx.stroke();
      }

      // 3. Touhou Danmaku Hitbox Soul Core (Active in HARDCOREZ mode)
      const diffConf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      if (diffConf.drawHitboxCore) {
        const pulse = (Math.sin(Date.now() / 60) + 1) / 2;
        ctx.save();
        // Outer rotating/pulsing ring
        ctx.strokeStyle = '#00f3ff';
        ctx.lineWidth = 1.5;
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(0, 0, 7 + pulse * 2.5, 0, Math.PI * 2);
        ctx.stroke();

        // Inner glowing core dot (exact hurtbox location)
        ctx.fillStyle = '#ff00ff';
        ctx.shadowColor = '#ff00ff';
        ctx.shadowBlur = 10;
        ctx.beginPath();
        ctx.arc(0, 0, 3.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(0, 0, 1.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      ctx.restore();

      // 3D Cosmic Shield Front Half (In Front of Ship)
      if (this.buffs.shield > 0) {
        draw3DShieldFront(ctx, this.x, this.y, this.buffs.shield);
      }
    }
  }

  // --- Projectile Class (Travels Right) ---
  class Projectile {
    constructor(x, y, vx, vy, isPierce = false, isBurst = false, isRapid = false, isMulti = false) {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.radius = isPierce ? 5 : (isBurst ? 6 : 4);
      this.isPierce = isPierce;
      this.isBurst = isBurst;
      this.isRapid = isRapid;
      this.isMulti = isMulti;
      this.toRemove = false;
      this.pierceHits = 0;
      this.maxHits = isPierce ? 4 : 1;
      this.time = 0;
    }

    update(dt) {
      this.time += dt;
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      if (this.x > CANVAS_WIDTH + 30 || this.y < -30 || this.y > CANVAS_HEIGHT + 30) {
        this.toRemove = true;
      }
    }

    draw(ctx) {
      ctx.save();
      const angle = Math.atan2(this.vy, this.vx);
      ctx.translate(this.x, this.y);
      ctx.rotate(angle);

      if (this.isPierce) {
        // --- Golden Solar Rail-Lance ---
        const spearLen = 22;
        ctx.shadowColor = '#ffd000';
        ctx.shadowBlur = 12;

        ctx.fillStyle = '#ffea00';
        ctx.beginPath();
        ctx.moveTo(spearLen, 0);
        ctx.lineTo(-spearLen * 0.4, -4.5);
        ctx.lineTo(-spearLen * 0.2, 0);
        ctx.lineTo(-spearLen * 0.4, 4.5);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(spearLen * 0.85, 0);
        ctx.lineTo(-spearLen * 0.1, -1.8);
        ctx.lineTo(-spearLen * 0.1, 1.8);
        ctx.closePath();
        ctx.fill();

        const wave = Math.sin(this.time * 25) * 5;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(spearLen * 0.5, wave);
        ctx.quadraticCurveTo(0, -wave, -spearLen * 0.5, wave);
        ctx.stroke();

        ctx.strokeStyle = '#ff8800';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-spearLen * 0.2, 0);
        ctx.lineTo(-spearLen * 1.2, 0);
        ctx.stroke();

      } else if (this.isBurst) {
        // --- Fiery Nova Warhead ---
        const pulse = Math.sin(this.time * 20) * 1.5;
        ctx.shadowColor = '#ff5500';
        ctx.shadowBlur = 14;

        const grad = ctx.createRadialGradient(2, 0, 1, 0, 0, 9 + pulse);
        grad.addColorStop(0, '#ffffff');
        grad.addColorStop(0.3, '#ffd000');
        grad.addColorStop(0.7, '#ff4400');
        grad.addColorStop(1, 'rgba(255, 40, 0, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, 8 + pulse, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(6, 0);
        ctx.lineTo(0, -3.5);
        ctx.lineTo(-5, 0);
        ctx.lineTo(0, 3.5);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = 'rgba(255, 120, 0, 0.7)';
        ctx.beginPath();
        ctx.moveTo(-2, -4);
        ctx.lineTo(-18 - Math.random() * 8, 0);
        ctx.lineTo(-2, 4);
        ctx.closePath();
        ctx.fill();

      } else if (this.isMulti) {
        // --- Crystalline Starburst Darts ---
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 10;

        ctx.fillStyle = '#00f3ff';
        ctx.beginPath();
        ctx.moveTo(12, 0);
        ctx.lineTo(0, -4);
        ctx.lineTo(-8, 0);
        ctx.lineTo(0, 4);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(8, 0);
        ctx.lineTo(0, -1.8);
        ctx.lineTo(-4, 0);
        ctx.lineTo(0, 1.8);
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = 'rgba(0, 243, 255, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(0, -4);
        ctx.lineTo(-14, -7);
        ctx.moveTo(0, 4);
        ctx.lineTo(-14, 7);
        ctx.stroke();

      } else if (this.isRapid) {
        // --- Hyper-Frequency Tachyon Needle ---
        ctx.shadowColor = '#ff2a85';
        ctx.shadowBlur = 12;

        ctx.strokeStyle = '#ff2a85';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(14, 0);
        ctx.lineTo(-18, 0);
        ctx.stroke();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(14, 0);
        ctx.lineTo(-12, 0);
        ctx.stroke();

        ctx.fillStyle = '#ff77ff';
        ctx.fillRect(-2, -3, 8, 1);
        ctx.fillRect(-2, 2, 8, 1);

      } else {
        // --- Standard Dual Photon Torpedo ---
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 10;

        ctx.fillStyle = '#00f3ff';
        ctx.beginPath();
        ctx.ellipse(2, 0, 9, 3.5, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.ellipse(3, 0, 5, 1.8, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = 'rgba(0, 243, 255, 0.4)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-5, 0);
        ctx.lineTo(-16, 0);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  // --- Meteor / Asteroid Class (Travels Left) ---
  class Meteor {
    constructor(x, y, type = 'normal') {
      this.x = x;
      this.y = y;
      this.type = type; // 'normal', 'medium', 'armored', 'star', 'wall_block'
      this.toRemove = false;
      this.rotation = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - 0.5) * 2;

      if (type === 'normal') {
        this.radius = 18;
        this.hp = 1;
        this.maxHp = 1;
        this.speed = 150 + Math.random() * 70;
        this.vy = (Math.random() - 0.5) * 30;
        this.score = 15;
        this.color = '#7c6f9e';
      } else if (type === 'medium') {
        this.radius = 28;
        this.hp = 3;
        this.maxHp = 3;
        this.speed = 110 + Math.random() * 45;
        this.vy = (Math.random() - 0.5) * 25;
        this.score = 40;
        this.color = '#5d4e80';
      } else if (type === 'armored') {
        this.radius = 36;
        this.hp = 7;
        this.maxHp = 7;
        this.speed = 80 + Math.random() * 30;
        this.vy = 0;
        this.score = 100;
        this.color = '#a83258';
      } else if (type === 'star') {
        this.radius = 20;
        this.hp = 2;
        this.maxHp = 2;
        this.speed = 170;
        this.vy = (Math.random() - 0.5) * 40;
        this.score = 60;
        this.color = '#ffd000';
      } else if (type === 'wall_block') {
        this.radius = 24;
        this.hp = 5;
        this.maxHp = 5;
        this.speed = 75;
        this.vy = 0;
        this.score = 50;
        this.color = '#452b69';
      }

      this.speed *= state.difficultyMultiplier;
    }

    update(dt) {
      this.time = (this.time || 0) + dt;
      this.x -= this.speed * dt;
      this.y += this.vy * dt;
      if (this.isDrone) {
        this.y += Math.sin(this.time * 6.5) * 2.2;
      }
      this.rotation += this.rotSpeed * dt;

      if (this.x < -60) {
        this.toRemove = true;
      }
    }

    hit(damage = 1) {
      this.hp -= damage;
      window.soundFx.playHit();
      if (this.hp <= 0) {
        this.destroy();
      }
    }

    destroy(byUlt = false) {
      if (this.toRemove) return;
      this.toRemove = true;

      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const earnedScore = Math.floor(this.score * conf.scoreMultiplier);
      state.score += earnedScore;

      // Charge ultimate gauge (faster in hardcorez)
      const ultBoost = conf.touhouDanmaku ? 1.4 : 1.0;
      chargeUltimate((this.type === 'armored' ? 6 : this.type === 'star' ? 12 : 2.5) * ultBoost);

      window.soundFx.playExplosion();
      createExplosion(this.x, this.y, this.radius, this.color);
      createFloatingText(`+${earnedScore}`, this.x, this.y, this.type === 'star' ? '#ffd000' : '#fff');

      if (this.type === 'armored' || byUlt) {
        state.screenShake = 6;
      }

      // Hardcorez Touhou Danmaku: Revenge Bullets (Danmaku Kaeshi)
      if (conf.revengeBullets && !byUlt && ['medium', 'armored', 'wall_block'].includes(this.type)) {
        const count = this.type === 'armored' ? 4 : 2;
        for (let i = 0; i < count; i++) {
          const offset = count === 4 ? -0.45 + i * 0.3 : (i === 0 ? -0.25 : 0.25);
          const a = Math.PI + offset;
          const spd = 160;
          enemyBullets.push(new EnemyBullet(this.x, this.y, Math.cos(a) * spd, Math.sin(a) * spd, 'revenge', 4, '#ff0077'));
        }
      }

      // Medium meteor splits into 2 small chunks drifting up/down
      if (this.type === 'medium' && !byUlt) {
        const m1 = new Meteor(this.x, this.y - 15, 'normal');
        const m2 = new Meteor(this.x, this.y + 15, 'normal');
        m1.vy = -60;
        m2.vy = 60;
        meteors.push(m1, m2);
      }

      rollPowerUpDrop(this.x, this.y, this.type);
    }

    draw(ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);

      if (this.isDrone) {
        // Fast Robotic Scout Interceptor Drone
        ctx.fillStyle = '#ff0055';
        ctx.shadowColor = '#ff0055';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.moveTo(-16, 0);
        ctx.lineTo(14, -10);
        ctx.lineTo(8, 0);
        ctx.lineTo(14, 10);
        ctx.closePath();
        ctx.fill();

        // Glowing Core
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(0, 0, 4, 0, Math.PI * 2);
        ctx.fill();

        // Twin Thruster Jet Exhaust
        ctx.fillStyle = '#00f3ff';
        ctx.beginPath();
        ctx.moveTo(14, -4);
        ctx.lineTo(24 + Math.random() * 8, 0);
        ctx.lineTo(14, 4);
        ctx.closePath();
        ctx.fill();
      } else if (this.type === 'star') {
        if (assets.images['stellar_star'] && assets.images['stellar_star'].complete && assets.images['stellar_star'].naturalWidth > 0) {
          const d = this.radius * 2.4;
          ctx.drawImage(assets.images['stellar_star'], -d / 2, -d / 2, d, d);
        } else {
          ctx.shadowColor = '#ffd000';
          ctx.shadowBlur = 12;
          ctx.fillStyle = '#ffd000';
          drawPolygon(ctx, 0, 0, this.radius, 5, 0.5);
          ctx.fillStyle = '#fff';
          drawPolygon(ctx, 0, 0, this.radius * 0.5, 5, 0.5);
        }
      } else if ((this.type === 'armored' || this.type === 'wall_block') && assets.images['armored_meteor'] && assets.images['armored_meteor'].complete && assets.images['armored_meteor'].naturalWidth > 0) {
        const d = this.radius * 2.4;
        ctx.drawImage(assets.images['armored_meteor'], -d / 2, -d / 2, d, d);
      } else if (assets.images['meteor'] && assets.images['meteor'].complete && assets.images['meteor'].naturalWidth > 0) {
        const d = this.radius * 2.3;
        ctx.drawImage(assets.images['meteor'], -d / 2, -d / 2, d, d);
      } else {
        ctx.fillStyle = this.color;
        ctx.strokeStyle = '#1b122e';
        ctx.lineWidth = 2.5;

        drawJaggedCircle(ctx, 0, 0, this.radius);

        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.beginPath();
        ctx.arc(-this.radius * 0.3, -this.radius * 0.2, this.radius * 0.25, 0, Math.PI * 2);
        ctx.arc(this.radius * 0.35, this.radius * 0.25, this.radius * 0.2, 0, Math.PI * 2);
        ctx.fill();

        // HP bar for tough obstacles
        if (this.maxHp > 1 && this.hp < this.maxHp) {
          ctx.restore();
          ctx.save();
          const barW = this.radius * 1.8;
          const barH = 4;
          const barX = this.x - barW / 2;
          const barY = this.y - this.radius - 8;
          ctx.fillStyle = 'rgba(0,0,0,0.6)';
          ctx.fillRect(barX, barY, barW, barH);
          ctx.fillStyle = this.hp <= 1 ? '#ff3344' : '#00ff88';
          ctx.fillRect(barX, barY, barW * (this.hp / this.maxHp), barH);
        }
      }

      ctx.restore();
    }
  }

  // --- PowerUp Drop Class (Travels Left) ---
  class PowerUp {
    constructor(x, y, kind) {
      this.x = x;
      this.y = y;
      this.kind = kind; // 'RAPID', 'MULTI', 'PIERCE', 'BURST', 'HEART', 'STAR'
      this.radius = 14;
      this.speed = 100;
      this.toRemove = false;
      this.bobble = Math.random() * Math.PI;
    }

    update(dt) {
      this.x -= this.speed * dt;
      this.bobble += dt * 4;
      if (this.x < -40) {
        this.toRemove = true;
      }
    }

    collect() {
      this.toRemove = true;
      window.soundFx.playPowerup();

      const t = TRANSLATIONS[state.lang] || TRANSLATIONS.id;
      if (this.kind === 'HEART') {
        if (state.lives < state.maxLives) {
          state.lives++;
          updateHeartsDisplay();
          createFloatingText(t.textLife, this.x, this.y - 10, '#ff3344');
        } else {
          state.score += 200;
          createFloatingText('+200', this.x, this.y - 10, '#ffd000');
        }
      } else if (this.kind === 'STAR') {
        chargeUltimate(25);
        state.score += 300;
        createFloatingText('+300 STELLAR ★', this.x, this.y - 10, '#ffd000');
      } else if (this.kind === 'SHIELD') {
        player.buffs.shield = BUFF_TYPES.SHIELD.duration;
        createFloatingText('COSMIC SHIELD! 🛡️', this.x, this.y - 12, '#00f3ff');
        window.soundFx.playShieldPickup();
      } else {
        const buffKey = this.kind.toLowerCase();
        const duration = (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].duration) || 10.0;
        player.buffs[buffKey] = duration;
        const displayName = (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].name) || this.kind;
        const color = (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].color) || '#00f3ff';
        createFloatingText(`${displayName}!`, this.x, this.y - 10, color);
      }
      updateBuffDisplay();
    }

    draw(ctx) {
      ctx.save();
      const currentY = this.y + Math.sin(this.bobble) * 4;
      ctx.translate(this.x, currentY);

      let color = '#fff';
      let icon = '★';
      if (this.kind === 'HEART') {
        color = '#ff3344';
        icon = '❤️';
      } else if (this.kind === 'STAR') {
        color = '#ffd000';
        icon = '⭐';
      } else if (BUFF_TYPES[this.kind]) {
        color = BUFF_TYPES[this.kind].color;
        icon = BUFF_TYPES[this.kind].symbol;
      }

      ctx.shadowColor = color;
      ctx.shadowBlur = 10;
      ctx.fillStyle = 'rgba(15, 10, 30, 0.9)';
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Check if custom AI icon image is loaded
      let iconImg = null;
      if (this.kind === 'HEART') iconImg = assets.images['cyber_heart'];
      else if (this.kind === 'STAR') iconImg = assets.images['stellar_star'];
      else if (this.kind === 'SHIELD') iconImg = assets.images['shield_icon'];
      else if (this.kind === 'RAPID') iconImg = assets.images['powerup_rapid'];
      else if (this.kind === 'MULTI') iconImg = assets.images['powerup_multi'];
      else if (this.kind === 'PIERCE') iconImg = assets.images['powerup_pierce'];
      else if (this.kind === 'BURST') iconImg = assets.images['powerup_burst'];
      else if (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].iconAsset) {
        iconImg = assets.images[BUFF_TYPES[this.kind].iconAsset];
      }

      if (iconImg && iconImg.complete && iconImg.naturalWidth > 0) {
        const d = (this.radius - 2.5) * 2;
        ctx.drawImage(iconImg, -d / 2, -d / 2, d, d);
      } else {
        ctx.font = '12px "Press Start 2P", sans-serif';
        ctx.fillStyle = color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(icon, 0, 1);
      }

      ctx.restore();
    }
  }

  // --- Boss & Enemy Projectiles ---
  class EnemyBullet {
    constructor(x, y, vx, vy, type = 'plasma', radius = 5, color = '#ff2a85') {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.type = type;
      this.radius = radius;
      this.color = color;
      this.toRemove = false;
    }

    update(dt) {
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      if (this.x < -40 || this.x > CANVAS_WIDTH + 50 || this.y < -40 || this.y > CANVAS_HEIGHT + 40) {
        this.toRemove = true;
      }
    }

    draw(ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      const angle = Math.atan2(this.vy, this.vx);

      if (this.type === 'danmaku') {
        // --- Touhou Danmaku Jewel Talisman ---
        ctx.rotate(this.x * 0.05 + this.y * 0.05);
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 12;

        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(0, -this.radius * 1.3);
        ctx.lineTo(this.radius, 0);
        ctx.lineTo(0, this.radius * 1.3);
        ctx.lineTo(-this.radius, 0);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(0, -this.radius * 0.6);
        ctx.lineTo(this.radius * 0.4, 0);
        ctx.lineTo(0, this.radius * 0.6);
        ctx.lineTo(-this.radius * 0.4, 0);
        ctx.closePath();
        ctx.fill();

      } else if (this.type === 'spread') {
        // --- Heavy Kinetic Flak Shell ---
        ctx.rotate(angle);
        ctx.shadowColor = '#ff4400';
        ctx.shadowBlur = 12;

        ctx.fillStyle = '#ff3344';
        ctx.beginPath();
        ctx.ellipse(1, 0, this.radius * 1.4, this.radius * 0.9, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffd000';
        ctx.beginPath();
        ctx.arc(2, 0, this.radius * 0.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = 'rgba(255, 100, 0, 0.6)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-this.radius, 0);
        ctx.lineTo(-this.radius * 2.5, 0);
        ctx.stroke();

      } else {
        // --- Void Plasma Orb ---
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;

        const pulse = Math.sin(Date.now() / 60) * 1.2;
        const grad = ctx.createRadialGradient(0, 0, 1, 0, 0, this.radius + pulse);
        grad.addColorStop(0, '#ffffff');
        grad.addColorStop(0.4, this.color);
        grad.addColorStop(1, 'rgba(20, 0, 40, 0)');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, this.radius + pulse, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = this.color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(0, 0, this.radius * 1.3, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  // Helper to convert hex color to HSL hue degrees for Canvas ctx.filter
  function hexToHue(hex) {
    if (!hex || hex[0] !== '#') return 0;
    const r = parseInt(hex.slice(1,3), 16) / 255;
    const g = parseInt(hex.slice(3,5), 16) / 255;
    const b = parseInt(hex.slice(5,7), 16) / 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0;
    if (max === min) h = 0;
    else if (max === r) h = (60 * ((g - b) / (max - min)) + 360) % 360;
    else if (max === g) h = (60 * ((b - r) / (max - min)) + 120) % 360;
    else h = (60 * ((r - g) / (max - min)) + 240) % 360;
    return Math.round(h);
  }

  class Boss {
    constructor(bossData = null, cycle = 1) {
      if (!bossData || typeof bossData === 'string') {
        const isBig = (bossData === 'bigboss') || (cycle % 2 === 0);
        bossData = {
          id: cycle,
          name: isBig ? 'TITAN APEX' : 'VOID LEVIATHAN',
          title: isBig ? 'COLOSSAL CELESTIAL MECHA' : 'ASTRAL STAR-DEVOURER',
          isBig: isBig,
          color: isBig ? '#ffd000' : '#00f3ff',
          baseHp: isBig ? 180 : 70,
          attack: isBig ? 'railgun_heavy' : 'plasma_twin'
        };
      }

      this.data = bossData;
      this.type = bossData.isBig ? 'bigboss' : 'miniboss';
      this.id = bossData.id || cycle;
      this.name = bossData.name || (this.type === 'bigboss' ? 'TITAN APEX' : 'VOID DESTROYER');
      this.title = bossData.title || (this.type === 'bigboss' ? 'COLOSSAL MECHA' : 'VOID DESTROYER');
      this.color = bossData.color || (this.type === 'bigboss' ? '#ffd000' : '#00f3ff');
      this.attackType = bossData.attack || (this.type === 'bigboss' ? 'railgun_heavy' : 'plasma_twin');
      this.archetype = bossData.archetype || (this.type === 'bigboss' ? 'mecha' : 'monster');
      this.cycle = cycle;
      const isBig = (this.type === 'bigboss');

      // Native proportions per archetype
      const sizeMult = isBig ? 1.25 : 1.0;
      if (this.archetype === 'spaceship') {
        this.width = Math.round(195 * sizeMult);
        this.height = Math.round(81 * sizeMult);
        this.baseHue = 183;
      } else if (this.archetype === 'mecha') {
        this.width = Math.round(180 * sizeMult);
        this.height = Math.round(172 * sizeMult);
        this.baseHue = 183;
      } else if (this.archetype === 'humanoid') {
        this.width = Math.round(160 * sizeMult);
        this.height = Math.round(130 * sizeMult);
        this.baseHue = 227;
      } else if (this.archetype === 'alien') {
        this.width = Math.round(168 * sizeMult);
        this.height = Math.round(128 * sizeMult);
        this.baseHue = 270;
      } else { // 'monster'
        this.width = Math.round(175 * sizeMult);
        this.height = Math.round(91 * sizeMult);
        this.baseHue = 318;
      }
      this.baseTargetX = CANVAS_WIDTH - (isBig ? 170 : 140);
      this.targetX = this.baseTargetX;
      this.dashTargetX = 220;
      this.jumpTargetX = 500;
      this.jumpTargetY = 85;
      this.diveTargetY = CANVAS_HEIGHT / 2;
      this.x = CANVAS_WIDTH + 140;
      this.y = CANVAS_HEIGHT / 2;
      this.prevY = this.y;
      this.currentX = this.x;
      this.tilt = 0;

      // Mega Man Style Action State Machine
      // States: 'enter' | 'hover' | 'dash_windup' | 'dash_strike' | 'dash_brake' | 'jump_up' | 'jump_apex' | 'dive_slam'
      this.actionState = 'enter';
      this.actionTimer = 0.9;
      this.afterimages = [];
      this.afterimageTimer = 0;

      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const baseHp = (bossData.baseHp || (isBig ? 180 : 70)) + (cycle - 1) * (isBig ? 45 : 25);
      this.maxHp = Math.floor(baseHp * conf.bossHpMult);
      this.hp = this.maxHp;

      this.time = 0;
      this.flashTimer = 0;
      this.shootTimer = 1.0 * conf.bossShootIntervalMult;
      this.specialTimer = (isBig ? 3.8 : 4.5) * conf.bossShootIntervalMult;

      // Universal Telegraphed Signature Skill System
      this.isCastingSkill = false;
      this.castSkillTimer = 0;
      this.castSkillDuration = 1.25;
      this.skillTargetY = CANVAS_HEIGHT / 2;
      this.currentSkillName = '';

      // Laser / Lance beam firing
      this.isChargingLaser = false;
      this.laserChargeTimer = 0;
      this.isFiringLaser = false;
      this.laserFireTimer = 0;
      this.laserTargetY = CANVAS_HEIGHT / 2;

      this.toRemove = false;
    }

    hit(damage) {
      if (this.toRemove) return;
      this.hp -= damage;
      this.flashTimer = 0.08;
      if (window.soundFx.playBossHit) window.soundFx.playBossHit();
      else window.soundFx.playHit();
      updateBossHpBar(this.hp, this.maxHp);

      if (this.hp <= 0) {
        this.destroy();
      }
    }

    spawnAfterimage(initialAlpha = 0.65) {
      this.afterimageTimer -= 0.016;
      if (this.afterimageTimer <= 0) {
        this.afterimageTimer = 0.038;
        this.afterimages.push({
          x: this.currentX || this.x,
          y: this.y,
          tilt: this.tilt || 0,
          alpha: initialAlpha,
          color: this.color || '#00f3ff'
        });
      }
    }

    update(dt) {
      this.time += dt;
      this.prevY = this.y;
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const isBig = (this.type === 'bigboss');

      // Strict Safe Altitude Boundary (Boss never leaves screen or clips into bottom/top HUD)
      const halfH = this.height * 0.5;
      const safeMinY = Math.max(75, Math.round(halfH + 15));
      const safeMaxY = Math.min(CANVAS_HEIGHT - 35, CANVAS_HEIGHT - Math.round(halfH + 15));

      // --- MEGA MAN BOSS COMBAT & MOVEMENT STATE MACHINE ---
      switch (this.actionState) {
        case 'enter':
          // Smooth glide into arena
          this.x -= 220 * dt;
          this.y += ((CANVAS_HEIGHT / 2) - this.y) * dt * 3.0;
          this.tilt = -0.15;
          if (this.x <= this.baseTargetX) {
            this.x = this.baseTargetX;
            this.actionState = 'hover';
            this.actionTimer = 2.4;
            this.tilt = 0;
            state.screenShake = 6;
          }
          break;

        case 'hover':
          // Dynamic combat hover: tracks player vertically with smooth agility
          const playerY = player ? player.y : (CANVAS_HEIGHT / 2);
          const yWave = Math.sin(this.time * (isBig ? 1.6 : 2.2)) * (isBig ? 55 : 75)
                      + Math.cos(this.time * 0.9) * 15;
          const desiredY = playerY + yWave * 0.55;
          const clampedTargetY = Math.max(safeMinY, Math.min(safeMaxY, desiredY));
          this.y += (clampedTargetY - this.y) * dt * (isBig ? 2.5 : 3.2);

          // Horizontal breathing drift near base anchor
          const xDrift = Math.sin(this.time * 1.5) * (isBig ? 14 : 20);
          this.x = this.baseTargetX + xDrift;

          // Banking tilt based on vertical movement
          const vy = (this.y - this.prevY) / Math.max(0.001, dt);
          const targetTilt = Math.max(-0.25, Math.min(0.25, (vy / 380) * 0.35));
          this.tilt += (targetTilt - this.tilt) * dt * 7;

          // Regular shooting timer
          this.shootTimer -= dt;
          if (this.shootTimer <= 0) {
            if (this.type === 'miniboss') {
              this.shootMinibossPlasma();
              this.shootTimer = 1.3 * conf.bossShootIntervalMult;
            } else {
              this.shootBigbossSpread();
              this.shootTimer = 1.8 * conf.bossShootIntervalMult;
            }
          }

          // Special Skill Timer
          this.specialTimer -= dt;
          if (this.specialTimer <= 0) {
            this.startSkillTelegraph();
            this.specialTimer = (isBig ? 7.5 : 6.5) * conf.bossShootIntervalMult;
            break;
          }

          // Action decision timer (Mega Man Maverick Dash vs Jump Slam)
          this.actionTimer -= dt;
          if (this.actionTimer <= 0 && !this.isCastingSkill && !this.isFiringLaser) {
            // Roll between Dash Attack (60%) and High Jump Slam (40%)
            if (Math.random() < 0.60) {
              this.actionState = 'dash_windup';
              this.actionTimer = 0.65;
              this.tilt = -0.32;
              window.soundFx.playBossWarning();
            } else {
              this.actionState = 'jump_up';
              this.actionTimer = 0.55;
              this.jumpTargetY = Math.max(safeMinY, 75);
              this.jumpTargetX = Math.max(480, this.baseTargetX - 120);
              window.soundFx.playPowerup();
            }
          }
          break;

        case 'dash_windup':
          // Mega Man Dash Telegraph: Pulls back, revs thrusters, sparks fly!
          this.x += 65 * dt;
          this.tilt = -0.35;
          this.actionTimer -= dt;

          if (Math.random() < 0.8) {
            particles.push({
              x: this.x + this.width * 0.45,
              y: this.y + (Math.random() - 0.5) * (this.height * 0.6),
              vx: 180 + Math.random() * 120,
              vy: (Math.random() - 0.5) * 80,
              size: 3.5,
              color: '#ffd000',
              life: 0.22,
              maxLife: 0.22
            });
          }

          if (this.actionTimer <= 0) {
            this.actionState = 'dash_strike';
            this.actionTimer = 0.85;
            window.soundFx.playExplosion();
            state.screenShake = 6;
          }
          break;

        case 'dash_strike':
          // MEGA MAN ROCKET DASH: Surges forward at 650 px/s!
          this.x -= 650 * dt;
          this.tilt = -0.42;

          this.spawnAfterimage(isBig ? 0.75 : 0.65);

          // Ram collision check with player
          if (player && player.invulnerableTimer <= 0 && !state.isUltActive) {
            const distX = Math.abs(player.x - this.x);
            const distY = Math.abs(player.y - this.y);
            if (distX < (this.width * 0.42 + player.width * 0.45) && distY < (this.height * 0.38 + player.height * 0.45)) {
              playerTakeDamage();
            }
          }

          // Reach dash destination (near player area x ~ 210)
          if (this.x <= this.dashTargetX) {
            this.x = this.dashTargetX;
            this.actionState = 'dash_brake';
            this.actionTimer = 0.35;
            state.screenShake = 8;
            window.soundFx.playBossHit();

            // Parting brake burst at player!
            const count = isBig ? 5 : 3;
            for (let i = 0; i < count; i++) {
              const a = Math.PI - 0.4 + (i / Math.max(1, count - 1)) * 0.8;
              enemyBullets.push(new EnemyBullet(this.x - 20, this.y, Math.cos(a) * 220, Math.sin(a) * 220, 'danmaku', 5, this.color));
            }
          }
          break;

        case 'dash_brake':
          this.tilt = 0.25;
          this.actionTimer -= dt;
          if (this.actionTimer <= 0) {
            this.actionState = 'retreat';
            this.actionTimer = 1.0;
          }
          break;

        case 'retreat':
          // Air-dashes smoothly backward to baseTargetX
          this.x += 440 * dt;
          this.tilt = 0.20;
          this.spawnAfterimage(0.5);

          if (this.x >= this.baseTargetX) {
            this.x = this.baseTargetX;
            this.actionState = 'hover';
            this.actionTimer = 2.6 + Math.random() * 1.0;
            this.tilt = 0;
          }
          break;

        case 'jump_up':
          // Mega Man High Jump / Ascend
          this.x += (this.jumpTargetX - this.x) * dt * 5.0;
          this.y += (this.jumpTargetY - this.y) * dt * 6.5;
          this.tilt = -0.25;
          this.spawnAfterimage(0.55);

          this.actionTimer -= dt;
          if (this.actionTimer <= 0 || (Math.abs(this.y - this.jumpTargetY) < 15)) {
            this.actionState = 'jump_apex';
            this.actionTimer = 0.32;
            this.diveTargetY = Math.max(safeMinY, Math.min(safeMaxY, player ? player.y : (CANVAS_HEIGHT / 2)));
          }
          break;

        case 'jump_apex':
          this.tilt = 0.05;
          this.actionTimer -= dt;
          if (this.actionTimer <= 0) {
            this.actionState = 'dive_slam';
            this.actionTimer = 0.75;
            window.soundFx.playBossWarning();
          }
          break;

        case 'dive_slam':
          // DIAGONAL DIVE SLAM toward player altitude
          this.y += 560 * dt;
          this.x += ((this.baseTargetX - 60) - this.x) * dt * 4.0;
          this.tilt = 0.40;
          this.spawnAfterimage(0.7);

          if (this.y >= this.diveTargetY) {
            this.y = this.diveTargetY;
            this.actionState = 'retreat';
            this.actionTimer = 0.8;
            state.screenShake = 14;
            window.soundFx.playExplosion();

            for (let d = 0; d < 6; d++) {
              const a = (d / 6) * Math.PI * 2;
              enemyBullets.push(new EnemyBullet(this.x, this.y, Math.cos(a) * 210, Math.sin(a) * 210, 'danmaku_heavy', 5.5, '#ffd000'));
            }
          }
          break;
      }

      // Safe bounds enforcement
      this.y = Math.max(safeMinY, Math.min(safeMaxY, this.y));
      this.currentX = this.x;

      if (this.flashTimer > 0) {
        this.flashTimer -= dt;
      }

      // Update ghost afterimages
      this.afterimages.forEach(g => {
        g.alpha -= dt * 3.4;
      });
      this.afterimages = this.afterimages.filter(g => g.alpha > 0);

      // Signature Skill Wind-up / Casting Telegraph Handling
      if (this.isCastingSkill) {
        // Smooth vertical lock-on tracking towards skillTargetY
        this.y += (this.skillTargetY - this.y) * dt * 3.8;
        this.castSkillTimer -= dt;

        // Recoil pull-back pose
        const pullProgress = 1 - (this.castSkillTimer / this.castSkillDuration);
        this.currentX = this.x + pullProgress * 24;

        // Rhythmic screen rumble
        state.screenShake = Math.max(state.screenShake, 3.5 * pullProgress);

        // Suction energy particles into charging focal point
        if (Math.random() < 0.7) {
          const muzzleX = (this.currentX || this.x) - this.width * 0.48;
          const beamY = this.y;
          const angle = Math.random() * Math.PI * 2;
          const dist = 35 + Math.random() * 45;
          particles.push({
            x: muzzleX + Math.cos(angle) * dist,
            y: beamY + Math.sin(angle) * dist,
            vx: -Math.cos(angle) * 140,
            vy: -Math.sin(angle) * 140,
            size: 2.5,
            color: Math.random() < 0.5 ? (this.color || '#00f3ff') : '#ffffff',
            life: 0.25,
            maxLife: 0.25
          });
        }

        if (this.castSkillTimer <= 0) {
          this.isCastingSkill = false;
          this.executeSkillRelease();
        }
      }

      // Beam / Railgun / Lance Firing Active
      if (this.isFiringLaser) {
        this.laserFireTimer -= dt;
        this.laserTargetY = this.y;
        if (player.invulnerableTimer <= 0 && !state.isUltActive) {
          if (player.x < (this.currentX || this.x) && Math.abs(player.y - this.y) < 28 + player.height / 2) {
            playerTakeDamage();
          }
        }
        if (this.laserFireTimer <= 0) {
          this.isFiringLaser = false;
        }
      }

// Attack timers handled inside action states

      // Dynamic Exhaust / Spore Particles
      if (Math.random() < 0.65) {
        const pColor = isBig ? (Math.random() < 0.5 ? this.color : '#ffd000') : (Math.random() < 0.5 ? this.color : '#9d4edd');
        particles.push({
          x: this.currentX + this.width / 2 - 8,
          y: this.y + (Math.random() - 0.5) * (this.height * 0.55),
          vx: 85 + Math.random() * 95,
          vy: (Math.random() - 0.5) * 35,
          size: 2 + Math.random() * 3,
          color: pColor,
          life: 0.28,
          maxLife: 0.28
        });
      }
    }

    shootMinibossPlasma() {
      window.soundFx.playBossShoot();
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

      if (conf.touhouDanmaku) {
        const baseAngle = this.time * 2.8;
        const count = 6;
        const speed = 195;
        for (let i = 0; i < count; i++) {
          const angle = baseAngle + (i * Math.PI * 2 / count);
          const col = i % 2 === 0 ? this.color : '#ff00ff';
          enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'danmaku', 4.5, col));
        }
      } else if (state.difficulty === 'hard') {
        const dx = player.x - this.currentX;
        const dy = player.y - this.y;
        const mainA = Math.atan2(dy, dx);
        [-0.18, 0, 0.18].forEach(off => {
          const a = mainA + off;
          enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y, Math.cos(a) * 235, Math.sin(a) * 235, 'plasma', 5, this.color));
        });
      } else {
        const dx = player.x - this.currentX;
        const dy = player.y - this.y;
        const dist = Math.hypot(dx, dy) || 1;
        const speed = 230;
        const vx = (dx / dist) * speed;
        const vy = (dy / dist) * speed;

        if (state.difficulty === 'easy') {
          enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y, vx, vy, 'plasma', 5, this.color));
        } else {
          enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y - 16, vx, vy, 'plasma', 5, this.color));
          enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y + 16, vx, vy, 'plasma', 5, this.color));
        }
      }
    }

    spawnEscortMeteors() {
      meteors.push(new Meteor(this.currentX - 30, this.y - 35, 'armored'));
      meteors.push(new Meteor(this.currentX - 30, this.y + 35, 'armored'));
      createFloatingText('SHIELD ESCORTS!', this.currentX - 40, this.y - 45, this.color);
    }

    shootBigbossSpread() {
      window.soundFx.playBossShoot();
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

      if (conf.touhouDanmaku) {
        const count = 10;
        const speed = 205;
        for (let i = 0; i < count; i++) {
          const offset = -0.75 + (i / (count - 1)) * 1.5;
          const angle = Math.PI + offset;
          const col = i % 2 === 0 ? this.color : '#ffd000';
          enemyBullets.push(new EnemyBullet(this.currentX - 30, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'danmaku_heavy', 5.5, col));
        }
      } else if (state.difficulty === 'hard') {
        const angles = [-0.48, -0.32, -0.16, 0, 0.16, 0.32, 0.48];
        const speed = 215;
        angles.forEach(offsetAngle => {
          const angle = Math.PI + offsetAngle;
          enemyBullets.push(new EnemyBullet(this.currentX - 30, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'heavy_plasma', 6, this.color));
        });
      } else if (state.difficulty === 'easy') {
        const angles = [-0.25, 0, 0.25];
        const speed = 190;
        angles.forEach(offsetAngle => {
          const angle = Math.PI + offsetAngle;
          enemyBullets.push(new EnemyBullet(this.currentX - 30, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'heavy_plasma', 6, this.color));
        });
      } else {
        const angles = [-0.4, -0.2, 0, 0.2, 0.4];
        const speed = 210;
        angles.forEach(offsetAngle => {
          const angle = Math.PI + offsetAngle;
          enemyBullets.push(new EnemyBullet(this.currentX - 30, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'heavy_plasma', 6.5, this.color));
        });
      }
    }

    startSkillTelegraph() {
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      this.isCastingSkill = true;
      this.castSkillDuration = conf.touhouDanmaku ? 0.95 : state.difficulty === 'hard' ? 1.1 : state.difficulty === 'easy' ? 1.4 : 1.25;
      this.castSkillTimer = this.castSkillDuration;
      const halfH = this.height * 0.5;
      const safeMinY = Math.max(75, Math.round(halfH + 15));
      const safeMaxY = Math.min(CANVAS_HEIGHT - 35, CANVAS_HEIGHT - Math.round(halfH + 15));
      this.skillTargetY = Math.max(safeMinY, Math.min(safeMaxY, player ? player.y : CANVAS_HEIGHT / 2));
      window.soundFx.playBossWarning();

      const skillNames = {
        humanoid: '⚔️ ASTRAL LANCE OF LONGINUS ⚔️',
        mecha: '⚡ TITAN OVERDRIVE RAILGUN ⚡',
        alien: '👁️ PSYCHIC SUPERNOVA BLAST 👁️',
        spaceship: '🛸 SIEGE CANNON BOMBARDMENT 🛸',
        monster: '👾 VOID MAW ROAR 👾'
      };
      this.currentSkillName = skillNames[this.archetype] || '⚡ SPECIAL ATTACK ⚡';
      createFloatingText(this.currentSkillName, CANVAS_WIDTH / 2, 70, this.color || '#ff0055');
    }

    executeSkillRelease() {
      state.screenShake = 16;
      window.soundFx.playBossShoot();

      if (this.archetype === 'humanoid') {
        // Celestial Lance of Longinus Beam + Star Danmaku Swords
        this.isFiringLaser = true;
        this.laserFireTimer = 0.8;
        this.laserTargetY = this.y;

        // 6 Radiating Holy Danmaku Swords
        const count = 6;
        for (let i = 0; i < count; i++) {
          const angle = Math.PI - 0.65 + (i / (count - 1)) * 1.3;
          enemyBullets.push(new EnemyBullet(this.currentX - 40, this.y, Math.cos(angle) * 230, Math.sin(angle) * 230, 'danmaku', 5.5, this.color || '#ff00aa'));
        }
      } else if (this.archetype === 'mecha') {
        // Titan Hyper Railgun + Rocket Salvo
        this.isFiringLaser = true;
        this.laserFireTimer = 0.8;
        this.laserTargetY = this.y;

        // Shoulder Rockets
        enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y - 30, -220, -70, 'heavy_plasma', 6.5, '#ffd000'));
        enemyBullets.push(new EnemyBullet(this.currentX - 20, this.y + 30, -220, 70, 'heavy_plasma', 6.5, '#ffd000'));
      } else if (this.archetype === 'alien') {
        // 12-way Psychic Supernova Ring
        const count = 12;
        const speed = 210;
        for (let i = 0; i < count; i++) {
          const angle = (i * Math.PI * 2 / count) + (this.time * 2);
          enemyBullets.push(new EnemyBullet(this.currentX - 25, this.y, Math.cos(angle) * speed, Math.sin(angle) * speed, 'danmaku', 5, this.color || '#b844ff'));
        }
      } else if (this.archetype === 'spaceship') {
        // 7-way Heavy Artillery Spread + Escort Asteroids
        const angles = [-0.48, -0.32, -0.16, 0, 0.16, 0.32, 0.48];
        angles.forEach(offsetAngle => {
          const angle = Math.PI + offsetAngle;
          enemyBullets.push(new EnemyBullet(this.currentX - 35, this.y, Math.cos(angle) * 225, Math.sin(angle) * 225, 'heavy_plasma', 6, this.color || '#00f3ff'));
        });
        meteors.push(new Meteor(this.currentX - 30, this.y - 40, 'armored'));
        meteors.push(new Meteor(this.currentX - 30, this.y + 40, 'armored'));
      } else {
        // Monster Leviathan: 2 Armored Escorts + 6 Homing Plasma Fireballs
        this.spawnEscortMeteors();
        [-0.35, -0.18, 0, 0.18, 0.35].forEach(off => {
          const angle = Math.PI + off;
          enemyBullets.push(new EnemyBullet(this.currentX - 30, this.y, Math.cos(angle) * 220, Math.sin(angle) * 220, 'plasma', 5, this.color || '#00f3ff'));
        });
      }
    }

    drawSkillTelegraph(ctx) {
      const bossX = this.currentX || this.x;
      const targetY = this.skillTargetY || this.y;
      const pullProgress = 1 - Math.max(0, this.castSkillTimer / this.castSkillDuration);

      ctx.save();

      // 1. Universal Telegraphed Danger Aiming Laser
      ctx.strokeStyle = this.color || '#ff0055';
      ctx.lineWidth = 1.8 + Math.sin(this.time * 20) * 0.8;
      ctx.shadowColor = this.color || '#ff0055';
      ctx.shadowBlur = 10;
      ctx.setLineDash([10, 6]);
      ctx.lineDashOffset = -this.time * 60;
      ctx.beginPath();
      ctx.moveTo(bossX - 40, targetY);
      ctx.lineTo(0, targetY);
      ctx.stroke();
      ctx.setLineDash([]);

      // 2. Archetype-specific Telegraphed Charge Graphics
      if (this.archetype === 'humanoid') {
        // Celestial Rune Circle (8-pointed sacred glyph)
        const runeX = bossX - 50;
        const runeR = 34 + pullProgress * 18;
        ctx.save();
        ctx.translate(runeX, targetY);
        ctx.rotate(this.time * 5.0);

        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.arc(0, 0, runeR, 0, Math.PI * 2);
        ctx.stroke();

        for (let p = 0; p < 8; p++) {
          const a = (p / 8) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * (runeR * 0.4), Math.sin(a) * (runeR * 0.4));
          ctx.lineTo(Math.cos(a) * runeR, Math.sin(a) * runeR);
          ctx.stroke();
        }
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // Digital Targeting Lock-On Reticle at Player Position
        const reticleX = player ? player.x : 100;
        const reticleR = 24 * (1.6 - pullProgress * 0.6);
        ctx.strokeStyle = '#ff0044';
        ctx.lineWidth = 2.0;
        ctx.strokeRect(reticleX - reticleR, targetY - reticleR, reticleR * 2, reticleR * 2);

        // Reticle crosshair
        ctx.beginPath();
        ctx.moveTo(reticleX - reticleR - 8, targetY);
        ctx.lineTo(reticleX + reticleR + 8, targetY);
        ctx.moveTo(reticleX, targetY - reticleR - 8);
        ctx.lineTo(reticleX, targetY + reticleR + 8);
        ctx.stroke();

        // Lock text
        ctx.fillStyle = '#ff0044';
        ctx.font = 'bold 10px monospace';
        ctx.fillText(`TARGET LOCK ${Math.floor(pullProgress * 100)}%`, reticleX - 35, targetY - reticleR - 4);

      } else if (this.archetype === 'alien') {
        // Psychic Sonar Ripples Expanding Outward
        for (let r = 1; r <= 3; r++) {
          const ripplePhase = (this.time * 4 + r * 0.8) % 3;
          const rippleR = ripplePhase * 45;
          ctx.strokeStyle = `${this.color || '#b844ff'}${Math.floor((1 - ripplePhase / 3) * 255).toString(16).padStart(2, '0')}`;
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          ctx.arc(bossX - 30, targetY, rippleR, Math.PI * 0.5, Math.PI * 1.5);
          ctx.stroke();
        }
      }

      ctx.restore();
    }

    destroy() {
      this.toRemove = true;
      hideBossBar();
      window.soundFx.playBossExplosion();
      window.soundFx.playBGM('stage');
      state.screenShake = 22;

      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const isBig = this.type === 'bigboss';
      const baseBonus = isBig ? 6000 : 2500;
      const bonusScore = Math.floor(baseBonus * conf.scoreMultiplier);
      state.score += bonusScore;
      scoreVal.textContent = state.score;

      createFloatingText(
        `#${String(this.id).padStart(3, '0')} ${this.name.toUpperCase()} DESTROYED! +${bonusScore}`,
        CANVAS_WIDTH / 2,
        this.y,
        '#ffd000'
      );

      // Cascading explosions
      createExplosion(this.currentX, this.y, 65, isBig ? '#ff0055' : '#00f3ff');
      createExplosion(this.currentX - 30, this.y - 25, 50, '#ffd000');
      createExplosion(this.currentX + 25, this.y + 20, 50, '#ffffff');
      createExplosion(this.currentX - 15, this.y + 30, 45, '#ff3344');

      // Power-Up Drops
      const drops = isBig ? ['RAPID', 'MULTI', 'BURST', 'HEART'] : ['MULTI', 'RAPID', 'HEART'];
      drops.forEach((kind, i) => {
        const ox = -25 + (i % 2) * 40;
        const oy = -30 + i * 22;
        powerUps.push(new PowerUp(this.currentX + ox, this.y + oy, kind));
      });

      // Star Shower
      const starCount = isBig ? 6 : 4;
      for (let s = 0; s < starCount; s++) {
        const sx = this.currentX - 40 + Math.random() * 80;
        const sy = this.y - 40 + Math.random() * 80;
        powerUps.push(new PowerUp(sx, sy, 'STAR'));
      }

      state.bossCycle++;
      state.nextBossCheckpoint = Math.floor(state.survivalTime / 60) * 60 + 60;
    }

    drawBackAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'humanoid') {
        // --- 1. Celestial Valkyrie: 3-Layered Radiant Angelic Starlight Wings ---
        const wingFlap = Math.sin(this.time * 3.8);
        const wingSpread = 0.85 + wingFlap * 0.18;
        const wingCount = 3;

        for (let side = -1; side <= 1; side += 2) {
          for (let w = 0; w < wingCount; w++) {
            const wingAngle = (-0.45 + w * 0.35 + wingFlap * 0.12) * side;
            const wingLen = (halfW * 0.72 + w * 18) * wingSpread;
            const wingOriginX = halfW * 0.08;
            const wingOriginY = -halfH * 0.22 + side * (w * 10);

            ctx.save();
            ctx.translate(wingOriginX, wingOriginY);
            ctx.rotate(wingAngle);

            const wingGrad = ctx.createLinearGradient(0, 0, wingLen, 0);
            wingGrad.addColorStop(0, '#ffffff');
            wingGrad.addColorStop(0.3, this.color || '#ff00aa');
            wingGrad.addColorStop(0.7, '#9d4edd');
            wingGrad.addColorStop(1, 'transparent');

            ctx.fillStyle = wingGrad;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.quadraticCurveTo(wingLen * 0.5, -14 * side, wingLen, 0);
            ctx.quadraticCurveTo(wingLen * 0.6, 12 * side, 0, 0);
            ctx.fill();

            // Luminous Feather Spine
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.4;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(wingLen * 0.85, 0);
            ctx.stroke();

            ctx.restore();
          }
        }

        // Sacred Revolving Halo Ring behind head
        const haloX = halfW * 0.08;
        const haloY = -halfH * 0.24;
        const haloR = 26 + Math.sin(this.time * 3) * 3;
        ctx.save();
        ctx.translate(haloX, haloY);
        ctx.rotate(this.time * 0.85);
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.2;
        ctx.shadowColor = '#ffd000';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(0, 0, haloR, 0, Math.PI * 2);
        ctx.stroke();
        // Halo Runes
        for (let r = 0; r < 6; r++) {
          const a = (r / 6) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * (haloR - 4), Math.sin(a) * (haloR - 4));
          ctx.lineTo(Math.cos(a) * (haloR + 4), Math.sin(a) * (haloR + 4));
          ctx.stroke();
        }
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // --- 2. Mecha Titan: Heavy Supersonic Rocket Thrusters with Shock Diamonds ---
        const thrusterOrigins = [
          { x: halfW * 0.52, y: -halfH * 0.38 },
          { x: halfW * 0.55, y: halfH * 0.35 }
        ];

        thrusterOrigins.forEach((th, idx) => {
          const flameLen = 38 + Math.sin(this.time * 22 + idx * 2.5) * 16 + Math.random() * 8;
          const flameW = 12;

          const flameGrad = ctx.createLinearGradient(th.x, th.y, th.x + flameLen, th.y);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.2, '#00f3ff');
          flameGrad.addColorStop(0.65, '#0066ff');
          flameGrad.addColorStop(1, 'transparent');

          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(th.x, th.y - flameW);
          ctx.lineTo(th.x + flameLen, th.y);
          ctx.lineTo(th.x, th.y + flameW);
          ctx.closePath();
          ctx.fill();

          // Shock Diamonds
          ctx.fillStyle = '#ffffff';
          for (let d = 1; d <= 3; d++) {
            const dx = th.x + d * (flameLen * 0.22);
            ctx.beginPath();
            ctx.arc(dx, th.y, 2.5, 0, Math.PI * 2);
            ctx.fill();
          }
        });

      } else if (this.archetype === 'monster' || this.archetype === 'alien') {
        // --- 3. Monster / Alien: Deep Background Undulating Bioluminescent Tentacles ---
        const tendrilCount = this.archetype === 'alien' ? 6 : 5;
        const rootX = halfW * 0.65;
        const segmentCount = 7;
        const segLen = 15;

        ctx.lineWidth = 3.5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        for (let t = 0; t < tendrilCount; t++) {
          const rootY = -halfH * 0.45 + (t / (tendrilCount - 1)) * (halfH * 0.9);
          const phaseOffset = t * 1.35;
          const tendrilGrad = ctx.createLinearGradient(rootX, rootY, rootX + 110, rootY);
          tendrilGrad.addColorStop(0, this.color || '#00f3ff');
          tendrilGrad.addColorStop(0.6, '#9d4edd');
          tendrilGrad.addColorStop(1, 'transparent');
          ctx.strokeStyle = tendrilGrad;

          ctx.beginPath();
          ctx.moveTo(rootX, rootY);
          let cx = rootX;
          let cy = rootY;
          for (let s = 1; s <= segmentCount; s++) {
            const wave = Math.sin(this.time * 5.2 + phaseOffset + s * 0.72) * (9 + s * 2.8);
            cx += segLen;
            cy += wave * 0.35;
            ctx.lineTo(cx, cy);
          }
          ctx.stroke();

          ctx.fillStyle = this.color || '#00f3ff';
          ctx.beginPath();
          ctx.arc(cx, cy, 3.0, 0, Math.PI * 2);
          ctx.fill();
        }
      } else {
        // --- 4. Spaceship: High-Output Twin Plasma Thruster Jets ---
        const thrusterCount = 2;
        const rootX = halfW * 0.82;
        for (let i = 0; i < thrusterCount; i++) {
          const thrusterY = -halfH * 0.3 + i * (halfH * 0.6);
          const flameLen = 32 + Math.sin(this.time * 20 + i * 3) * 16 + Math.random() * 8;
          const flameGrad = ctx.createLinearGradient(rootX, thrusterY, rootX + flameLen, thrusterY);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.3, this.color || '#00f3ff');
          flameGrad.addColorStop(0.7, '#ff0055');
          flameGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(rootX, thrusterY - 7);
          ctx.lineTo(rootX + flameLen, thrusterY);
          ctx.lineTo(rootX, thrusterY + 7);
          ctx.closePath();
          ctx.fill();
        }
      }
      ctx.restore();
    }

    drawFrontAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'humanoid') {
        // =========================================================================
        // VALKYRIE: ANIMASI PUTAR TONGKAT / CELESTIAL LANCE SPIN & HAND ARTICULATION
        // =========================================================================
        const handBaseX = -halfW * 0.28;
        const handBaseY = halfH * 0.05;
        // Natural arm/hand floating breathing sway
        const handSwayX = Math.cos(this.time * 3.2) * 5;
        const handSwayY = Math.sin(this.time * 3.2) * 5;
        const hx = handBaseX + handSwayX;
        const hy = handBaseY + handSwayY;

        ctx.save();
        ctx.translate(hx, hy);

        // Staff Spin Speed & Angle:
        // Idle: elegant continuous spin (3.8 rad/s)
        // Charging Skill / Laser: Blazing kinetic propeller whirl (26 rad/s)
        // Firing Beam: Locked horizontal thrusting forward
        let spinAngle = (this.time * 3.8);
        const isCharging = (this.isCastingSkill || this.isChargingLaser);
        const isFiring = this.isFiringLaser;

        if (isCharging) {
          spinAngle = this.time * 26.0;
        } else if (isFiring) {
          spinAngle = Math.PI; // Locked aiming forward
        }

        ctx.rotate(spinAngle);

        const staffLen = 110;
        const halfStaff = staffLen / 2;

        // 1. Kinetic Motion Blur Disc / Energy Trail during fast twirl
        if (isCharging) {
          const vortexGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, halfStaff + 12);
          vortexGrad.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
          vortexGrad.addColorStop(0.45, `${this.color || '#ff00aa'}44`);
          vortexGrad.addColorStop(0.85, 'rgba(255, 220, 100, 0.55)');
          vortexGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = vortexGrad;
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 10, 0, Math.PI * 2);
          ctx.fill();

          // High-speed whirling speed arcs
          ctx.strokeStyle = '#ffd000';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 2, 0, Math.PI * 0.85);
          ctx.stroke();
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 2, Math.PI, Math.PI * 1.85);
          ctx.stroke();
        }

        // 2. Staff Shaft (Gold & Crystalline Core)
        const shaftGrad = ctx.createLinearGradient(-halfStaff, 0, halfStaff, 0);
        shaftGrad.addColorStop(0, '#ffd000');
        shaftGrad.addColorStop(0.5, '#ffffff');
        shaftGrad.addColorStop(1, '#ffd000');
        ctx.strokeStyle = shaftGrad;
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        ctx.moveTo(-halfStaff, 0);
        ctx.lineTo(halfStaff, 0);
        ctx.stroke();

        // 3. Ornate Double-Ended Celestial Spear Tips
        [-1, 1].forEach(dir => {
          const tipX = dir * halfStaff;
          ctx.save();
          ctx.translate(tipX, 0);
          ctx.rotate(dir === 1 ? 0 : Math.PI);

          // Diamond Spear Head
          ctx.fillStyle = '#ffffff';
          ctx.shadowColor = this.color || '#ff00aa';
          ctx.shadowBlur = 10;
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.lineTo(-14, -6);
          ctx.lineTo(16, 0);
          ctx.lineTo(-14, 6);
          ctx.closePath();
          ctx.fill();

          // Mini Angelic Winglets on Spearhead
          ctx.strokeStyle = '#ffd000';
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.moveTo(-8, -5);
          ctx.lineTo(-16, -11);
          ctx.lineTo(-12, -2);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(-8, 5);
          ctx.lineTo(-16, 11);
          ctx.lineTo(-12, 2);
          ctx.stroke();

          // Blazing Starlight Flare at Tip
          ctx.fillStyle = '#ffd000';
          ctx.beginPath();
          ctx.arc(16, 0, 3.5, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();
        });

        // 4. Center Celestial Gripping Jewel & Hand Rune
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 14;
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        // Floating Rune Circle in Hand Palm
        ctx.save();
        ctx.translate(hx, hy);
        ctx.rotate(-this.time * 2.0);
        ctx.strokeStyle = `${this.color || '#ff00aa'}aa`;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.arc(0, 0, 18, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // =========================================================================
        // MECHA TITAN: AIMING HEAVY RAILGUN CANNON ARM & RECOIL PISTON SYSTEM
        // =========================================================================
        const shoulderX = -halfW * 0.18;
        const shoulderY = -halfH * 0.05;

        // Dynamic Aim Tracking toward Player Ship!
        const targetY = player ? player.y : (CANVAS_HEIGHT / 2);
        const targetX = player ? player.x : 80;
        const rawAim = Math.atan2(targetY - (this.y + shoulderY), targetX - ((this.currentX || this.x) + shoulderX));
        // Clamp elevation between -22 deg and +22 deg
        const aimAngle = Math.max(-0.38, Math.min(0.38, rawAim + Math.PI)); // Relative to facing left

        // Hydraulic Recoil displacement when firing
        const isRecoil = (this.shootTimer < 0.22) || this.isFiringLaser;
        const recoilDist = isRecoil ? Math.sin(this.time * 30) * 8 : 0;

        ctx.save();
        ctx.translate(shoulderX, shoulderY);
        ctx.rotate(-aimAngle); // Aim towards player

        // 1. Arm Hydraulic Upper Bracket & Piston
        ctx.fillStyle = '#1e2433';
        ctx.strokeStyle = '#4a5568';
        ctx.lineWidth = 2.0;
        ctx.fillRect(-10, -8, 22, 16);
        ctx.strokeRect(-10, -8, 22, 16);

        // Chrome Hydraulic Piston Shaft
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(-22 + recoilDist, -4, 14, 8);

        // 2. Forearm Dual Heavy Railgun Barrels (Sliding on Recoil)
        const barrelX = -36 + recoilDist;
        ctx.fillStyle = '#2d3748';
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 1.5;
        // Upper Barrel
        ctx.fillRect(barrelX, -10, 32, 6);
        ctx.strokeRect(barrelX, -10, 32, 6);
        // Lower Barrel
        ctx.fillRect(barrelX, 4, 32, 6);
        ctx.strokeRect(barrelX, 4, 32, 6);

        // Glowing Rail Accelerator Coils
        ctx.fillStyle = this.color || '#00f3ff';
        for (let c = 0; c < 3; c++) {
          const cx = barrelX + 6 + c * 8;
          ctx.fillRect(cx, -11, 3, 8);
          ctx.fillRect(cx, 3, 3, 8);
        }

        // Muzzle Heat Glow / Smoke
        if (isRecoil) {
          ctx.fillStyle = '#ff7700';
          ctx.shadowColor = '#ff2200';
          ctx.shadowBlur = 12;
          ctx.beginPath();
          ctx.arc(barrelX - 3, -7, 5, 0, Math.PI * 2);
          ctx.arc(barrelX - 3, 7, 5, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();

        // 3. Center Chest Overdrive Arc Reactor (Turbine Core & Lightning Arcs)
        const coreX = -halfW * 0.02;
        const coreY = halfH * 0.04;
        const coreR = 18;

        ctx.save();
        ctx.translate(coreX, coreY);

        // Radiant Core Plasma Aura
        const coreAura = ctx.createRadialGradient(0, 0, 4, 0, 0, coreR * 1.8);
        coreAura.addColorStop(0, '#ffffff');
        coreAura.addColorStop(0.35, this.color || '#00f3ff');
        coreAura.addColorStop(0.8, 'rgba(0, 100, 255, 0.25)');
        coreAura.addColorStop(1, 'transparent');
        ctx.fillStyle = coreAura;
        ctx.beginPath();
        ctx.arc(0, 0, coreR * 1.8, 0, Math.PI * 2);
        ctx.fill();

        // Rotating Turbine Aperture Blades
        ctx.rotate(this.time * 5.5);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.0;
        for (let b = 0; b < 6; b++) {
          const a = (b / 6) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * 3, Math.sin(a) * 3);
          ctx.lineTo(Math.cos(a + 0.3) * (coreR - 3), Math.sin(a + 0.3) * (coreR - 3));
          ctx.stroke();
        }

        // Outer Titanium Armored Core Ring
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(0, 0, coreR, 0, Math.PI * 2);
        ctx.stroke();

        ctx.restore();

        // Crackling Electrical Lightning Filament to Shoulders
        if (Math.random() < 0.45) {
          ctx.strokeStyle = '#00f3ff';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(coreX, coreY);
          const midX = (coreX + shoulderX) * 0.5 + (Math.random() - 0.5) * 8;
          const midY = (coreY + shoulderY) * 0.5 + (Math.random() - 0.5) * 8;
          ctx.lineTo(midX, midY);
          ctx.lineTo(shoulderX, shoulderY);
          ctx.stroke();
        }

      } else if (this.archetype === 'alien') {
        // =========================================================================
        // ALIEN ELDRITCH EYE: LIVING TRACKING PUPIL & SMOOTH EYELID BLINK
        // =========================================================================
        const eyeX = -halfW * 0.12;
        const eyeY = -halfH * 0.04;
        const eyeR = 22;

        // Player tracking angle
        const targetY = player ? player.y : (CANVAS_HEIGHT / 2);
        const targetX = player ? player.x : 80;
        const pAngle = Math.atan2(targetY - (this.y + eyeY), targetX - ((this.currentX || this.x) + eyeX));
        const pupilDist = 6.0;

        // Eyelid Blinking every 4.0 seconds for 0.25s
        const blinkCycle = (this.time % 4.0);
        const isBlinking = blinkCycle > 3.75;
        const blinkAmount = isBlinking ? Math.sin((blinkCycle - 3.75) / 0.25 * Math.PI) : 0;

        ctx.save();
        ctx.translate(eyeX, eyeY);

        // Clip eye area
        ctx.beginPath();
        ctx.ellipse(0, 0, eyeR, eyeR * (1 - blinkAmount * 0.95), 0, 0, Math.PI * 2);
        ctx.clip();

        // Sclera with pulsing void veins
        const eyeGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, eyeR);
        eyeGrad.addColorStop(0, '#ffffff');
        eyeGrad.addColorStop(0.5, '#ffd000');
        eyeGrad.addColorStop(0.85, '#ff0055');
        eyeGrad.addColorStop(1, '#140024');
        ctx.fillStyle = eyeGrad;
        ctx.fillRect(-eyeR - 2, -eyeR - 2, (eyeR + 2) * 2, (eyeR + 2) * 2);

        // Tracking Cyclopean Pupil (Slit / Eldritch Diamond)
        const relPupilX = Math.cos(pAngle) * pupilDist;
        const relPupilY = Math.sin(pAngle) * (pupilDist * 0.65);
        ctx.fillStyle = '#05000a';
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.ellipse(relPupilX, relPupilY, 3.5, 9, 0, 0, Math.PI * 2);
        ctx.fill();

        // Eye Cornea Light Reflection Spark
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(relPupilX - 2.5, relPupilY - 3, 2.0, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        // Eyelid Outlines & Creases
        ctx.strokeStyle = '#2b0938';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.ellipse(eyeX, eyeY, eyeR + 1, (eyeR + 1) * (1 - blinkAmount * 0.95), 0, 0, Math.PI * 2);
        ctx.stroke();

      } else if (this.archetype === 'spaceship') {
        // --- 4. Spaceship: Shield Matrix Shimmer & Bow Armor Shimmer ---
        const shieldPulse = Math.sin(this.time * 4) * 0.2 + 0.35;
        ctx.strokeStyle = `rgba(0, 243, 255, ${shieldPulse})`;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.arc(-halfW * 0.35, 0, halfH * 0.85, Math.PI * 0.55, Math.PI * 1.45);
        ctx.stroke();
      }
      ctx.restore();
    }

    drawAfterimages(ctx) {
      if (!this.afterimages || this.afterimages.length === 0) return;
      ctx.save();
      const w = this.width;
      const h = this.height;
      const spriteKey = 'boss_' + (this.archetype || (this.type === 'miniboss' ? 'monster' : 'mecha'));
      const sprite = assets.images[spriteKey] || (this.type === 'miniboss' ? assets.images.miniboss : assets.images.boss);

      this.afterimages.forEach(ghost => {
        if (ghost.alpha <= 0.02) return;
        ctx.save();
        ctx.globalAlpha = Math.max(0, Math.min(0.65, ghost.alpha * 0.6));
        ctx.translate(ghost.x, ghost.y);
        ctx.rotate(ghost.tilt || 0);

        if (sprite && sprite.complete && sprite.naturalWidth > 0) {
          ctx.shadowColor = ghost.color || this.color || '#00f3ff';
          ctx.shadowBlur = 14;
          ctx.filter = 'brightness(1.5) contrast(1.2)';
          ctx.drawImage(sprite, -w / 2, -h / 2, w, h);
        } else {
          ctx.fillStyle = ghost.color || this.color || '#00f3ff';
          ctx.fillRect(-w / 2, -h / 2, w, h);
        }
        ctx.restore();
      });
      ctx.restore();
    }

    draw(ctx) {
      ctx.save();

      // Mega Man Dash Ghost Afterimages (Motion Blur Trails)
      if (this.afterimages && this.afterimages.length > 0) {
        this.drawAfterimages(ctx);
      }

      // Telegraphed Signature Skill Charging Animation
      if (this.isCastingSkill) {
        this.drawSkillTelegraph(ctx);
      }

      // Active Firing Beam (Lance of Longinus or Hyper Railgun)
      if (this.isFiringLaser) {
        if (this.archetype === 'humanoid') {
          drawValkyrieCelestialLanceBeam(ctx, this);
        } else {
          drawBossHyperRailgunBeam(ctx, this);
        }
      }

      // Draw Boss with dynamic tilt and natural breathing pulse
      ctx.translate(this.currentX || this.x, this.y);
      ctx.rotate(this.tilt || 0);

      const breathFreq = this.type === 'bigboss' ? 2.2 : 3.4;
      const breathMag = this.type === 'bigboss' ? 0.025 : 0.04;
      const pulseX = 1 + Math.sin(this.time * breathFreq) * breathMag;
      const pulseY = 1 - Math.sin(this.time * breathFreq) * (breathMag * 0.8);
      ctx.scale(pulseX, pulseY);

      // Back Layer: Flapping wings, halo, vector thruster plumes, rear tentacles
      this.drawBackAppendages(ctx);

      // Middle Layer: Boss sprite with dynamic hue-rotation & 22-slice undulation
      if (this.type === 'miniboss') {
        this.drawMinibossShip(ctx);
      } else {
        this.drawBigbossShip(ctx);
      }

      // Front Layer: Valkyrie spinning lance/staff, Mecha aiming & recoiling cannon arm, Alien pupil & eyelids
      this.drawFrontAppendages(ctx);

      ctx.restore();
    }

    drawMinibossShip(ctx) {
      const w = this.width;
      const h = this.height;
      const halfW = w / 2;
      const halfH = h / 2;

      const spriteKey = 'boss_' + (this.archetype || 'monster');
      const sprite = assets.images[spriteKey] || assets.images.miniboss;
      if (sprite && sprite.complete && sprite.naturalWidth > 0) {
        const auraGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, halfW * 0.95);
        auraGrad.addColorStop(0, `${this.color || '#00f3ff'}44`);
        auraGrad.addColorStop(0.65, `${this.color || '#9d4edd'}14`);
        auraGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(0, 0, halfW * 0.95, 0, Math.PI * 2);
        ctx.fill();

        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#00f3ff');
          const baseHue = this.baseHue || 318;
          const hueDiff = (targetHue - baseHue + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.35)`;
        }
        if (this.archetype === 'monster' || this.archetype === 'alien') {
          // Organic Spine Undulation / Tentacle Slither Mesh Slicer
          const slices = 22;
          const sliceW = w / slices;
          const srcSliceW = sprite.naturalWidth / slices;
          for (let i = 0; i < slices; i++) {
            const progress = i / (slices - 1);
            const amp = Math.pow(progress, 1.4) * (this.archetype === 'alien' ? 14 : 18);
            const waveY = Math.sin(this.time * 6.5 + i * 0.42) * amp;
            const waveScaleY = 1 + Math.cos(this.time * 6.5 + i * 0.42) * (progress * 0.08);

            const dx = -halfW + i * sliceW;
            const dy = -halfH * waveScaleY + waveY;
            const dw = sliceW + 0.6;
            const dh = h * waveScaleY;

            const sx = i * srcSliceW;
            const sy = 0;
            const sw = srcSliceW;
            const sh = sprite.naturalHeight;

            ctx.drawImage(sprite, sx, sy, sw, sh, dx, dy, dw, dh);
          }
        } else {
          ctx.drawImage(sprite, -halfW, -halfH, w, h);
        }
        ctx.restore();
        return;
      }

      // Procedural fallback
      ctx.fillStyle = this.flashTimer > 0 ? '#ffffff' : '#140c24';
      ctx.strokeStyle = this.color || '#ff0055';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(0, 0, halfH, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    drawBigbossShip(ctx) {
      const w = this.width;
      const h = this.height;
      const halfW = w / 2;
      const halfH = h / 2;

      // Select Dedicated Unique Big Boss Sprite Assets
      let spriteKey = 'boss_' + (this.archetype || 'mecha');
      const bName = this.name || '';

      if (bName.includes('Annihilator') || bName.includes('Dreadnought') || bName.includes('Apex') || bName.includes('Flagship') || bName.includes('Warlord') || bName.includes('Carrier')) {
        spriteKey = 'boss_crimson_annihilator';
      } else if (this.archetype === 'monster' || bName.includes('Singularity') || bName.includes('Leviathan') || bName.includes('Maw') || bName.includes('Goliath')) {
        spriteKey = 'boss_void_singularity';
      } else if (this.archetype === 'humanoid' || bName.includes('Astraea') || bName.includes('Archon') || bName.includes('Ex-Machina') || bName.includes('Zephyr')) {
        spriteKey = 'boss_astraea_archon';
      }

      const sprite = assets.images[spriteKey] || assets.images['boss_' + (this.archetype || 'mecha')] || assets.images.bigboss;
      if (sprite && sprite.complete && sprite.naturalWidth > 0) {
        // Soft radiant aura behind the celestial mecha titan
        const auraGrad = ctx.createRadialGradient(0, 0, 20, 0, 0, halfW * 0.95);
        auraGrad.addColorStop(0, this.isChargingLaser ? 'rgba(0, 243, 255, 0.35)' : 'rgba(255, 180, 0, 0.28)');
        auraGrad.addColorStop(0.65, this.isChargingLaser ? 'rgba(0, 180, 255, 0.1)' : 'rgba(255, 60, 0, 0.08)');
        auraGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(0, 0, halfW * 0.95, 0, Math.PI * 2);
        ctx.fill();

        // Draw sprite with silky brightness hit flash
        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#ffd000');
          const baseHue = this.baseHue || 183;
          const hueDiff = (targetHue - baseHue + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.4)`;
        }
        if (this.archetype === 'monster' || this.archetype === 'alien') {
          // Organic Spine Undulation / Tentacle Slither Mesh Slicer
          const slices = 22;
          const sliceW = w / slices;
          const srcSliceW = sprite.naturalWidth / slices;
          for (let i = 0; i < slices; i++) {
            const progress = i / (slices - 1);
            const amp = Math.pow(progress, 1.4) * (this.archetype === 'alien' ? 14 : 18);
            const waveY = Math.sin(this.time * 6.5 + i * 0.42) * amp;
            const waveScaleY = 1 + Math.cos(this.time * 6.5 + i * 0.42) * (progress * 0.08);

            const dx = -halfW + i * sliceW;
            const dy = -halfH * waveScaleY + waveY;
            const dw = sliceW + 0.6;
            const dh = h * waveScaleY;

            const sx = i * srcSliceW;
            const sy = 0;
            const sw = srcSliceW;
            const sh = sprite.naturalHeight;

            ctx.drawImage(sprite, sx, sy, sw, sh, dx, dy, dw, dh);
          }
        } else {
          ctx.drawImage(sprite, -halfW, -halfH, w, h);
        }
        ctx.restore();
        return;
      }

      // Procedural fallback
      ctx.fillStyle = this.flashTimer > 0 ? '#ffffff' : '#12091f';
      ctx.strokeStyle = this.color || '#ffd000';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(0, 0, halfH, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }
  }

  // --- Ultimate Mechanism ---
  function chargeUltimate(amount) {
    state.ultCharge = Math.min(state.maxUltCharge, state.ultCharge + amount);
    updateUltBar();
  }

  function triggerUltimate() {
    if (state.screen !== 'playing') return;
    if (state.ultCharge < state.maxUltCharge || state.isUltActive) return;

    state.isUltActive = true;
    state.ultDuration = 2.0; // horizontal beam lasts 2s
    state.ultCharge = 0;
    updateUltBar();

    window.soundFx.playUltimate();
    state.screenShake = 16;
    createFloatingText('STELLAR BLASTER!!', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 40, '#00f3ff');
  }

  function updateUltBar() {
    const pct = (state.ultCharge / state.maxUltCharge) * 100;
    ultProgressBar.style.width = `${pct}%`;

    const isReady = state.ultCharge >= state.maxUltCharge;
    if (isReady) {
      ultContainer.classList.add('ult-ready');
      btnTouchUlt.classList.add('ready');
    } else {
      ultContainer.classList.remove('ult-ready');
      btnTouchUlt.classList.remove('ready');
    }
  }

  // --- 100 Boss Progression Catalog Lookup ---
  function getNextBossConfig(difficulty, cycle) {
    if (!window.BOSS_CATALOG || window.BOSS_CATALOG.length === 0) {
      const isBig = (cycle % 2 === 0);
      return {
        id: cycle,
        tier: difficulty || 'normal',
        name: isBig ? 'TITAN APEX' : 'VOID DESTROYER',
        title: isBig ? 'COLOSSAL CELESTIAL MECHA' : 'ASTRAL STAR-DEVOURER',
        isBig: isBig,
        color: isBig ? '#ffd000' : '#00f3ff',
        baseHp: isBig ? 180 : 70,
        attack: isBig ? 'railgun_heavy' : 'plasma_twin'
      };
    }

    const tierMap = {
      easy: 'easy',
      normal: 'normal',
      hard: 'hard',
      hardcorez: 'hardcorez'
    };
    const targetTier = tierMap[difficulty] || 'normal';
    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === targetTier);

    if (tierBosses.length === 0) return window.BOSS_CATALOG[0];

    // Interleave archetypes so player tests all 5 types back-to-back:
    // Cycle 1: Spaceship, Cycle 2: Mecha, Cycle 3: Monster, Cycle 4: Humanoid, Cycle 5: Alien
    const archetypes = ['spaceship', 'mecha', 'monster', 'humanoid', 'alien'];
    const chosenArchetype = archetypes[(cycle - 1) % archetypes.length];
    const pool = tierBosses.filter(b => b.archetype === chosenArchetype);

    if (pool.length > 0) {
      const archIndex = Math.floor((cycle - 1) / archetypes.length) % pool.length;
      return pool[archIndex];
    }

    const index = (cycle - 1) % tierBosses.length;
    return tierBosses[index];
  }

  // --- Survive Skill Execution & Cooldown UI ---
  function activateSurviveSkill() {
    if (state.screen !== 'playing') return;
    if (state.surviveSkillCooldown > 0) return;
    if (!player) return;

    const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;
    state.surviveSkillCooldown = shipConf.id === 'aether_vanguard' ? 15 : shipConf.id === 'chrono_phantom' ? 16 : 18;

    if (shipConf.id === 'aether_vanguard') {
      // Nanite Phase Barrier + EMP Blast clearing bullets
      player.buffs.shield = Math.max(player.buffs.shield, 4.0);
      player.invulnerableTimer = 1.2;
      window.soundFx.playExplosion();
      state.screenShake = 10;
      createFloatingText('NANITE MATRIX ACTIVE!', player.x, player.y - 30, '#ffd000');

      for (const b of enemyBullets) {
        if (!b.toRemove && Math.hypot(b.x - player.x, b.y - player.y) < 280) {
          b.toRemove = true;
          createExplosion(b.x, b.y, 10, '#ffd000');
        }
      }
      particles.push({
        x: player.x,
        y: player.y,
        vx: 0,
        vy: 0,
        size: 20,
        growth: 260,
        isRing: true,
        ringWidth: 4,
        color: '#ffd000',
        life: 0.45,
        maxLife: 0.45
      });
    } else if (shipConf.id === 'chrono_phantom') {
      // Temporal Warp: 4s of 70% slow motion + ghost invulnerability
      state.chronoSlowMotionTimer = 4.0;
      player.invulnerableTimer = 4.0;
      if (window.soundFx.playPowerup) window.soundFx.playPowerup();
      createFloatingText('CHRONO WARP DILATION!', player.x, player.y - 30, '#b844ff');

      particles.push({
        x: player.x,
        y: player.y,
        vx: 0,
        vy: 0,
        size: 30,
        growth: 240,
        isRing: true,
        ringWidth: 3,
        color: '#b844ff',
        life: 0.6,
        maxLife: 0.6
      });
    } else {
      // Stella Nova: Cosmic Aegis Shield (10s 3D forcefield)
      player.buffs.shield = Math.max(player.buffs.shield, 10.0);
      if (window.soundFx.playPowerup) window.soundFx.playPowerup();
      createFloatingText('COSMIC SHIELD DEPLOYED!', player.x, player.y - 30, '#00f3ff');

      particles.push({
        x: player.x,
        y: player.y,
        vx: 0,
        vy: 0,
        size: 25,
        growth: 160,
        isRing: true,
        ringWidth: 3,
        color: '#00f3ff',
        life: 0.5,
        maxLife: 0.5
      });
    }
    updateSurviveButtonUI();
  }

  function updateSurviveButtonUI() {
    const btn = document.getElementById('btnTouchSurvive');
    if (!btn) return;

    if (state.surviveSkillCooldown <= 0) {
      btn.classList.add('ready');
      btn.disabled = false;
      const textSpan = btn.querySelector('span:last-child');
      if (textSpan) textSpan.textContent = 'DEF';
    } else {
      btn.classList.remove('ready');
      const textSpan = btn.querySelector('span:last-child');
      if (textSpan) textSpan.textContent = `${Math.ceil(state.surviveSkillCooldown)}s`;
    }
  }

  // --- Dynamic Atmosphere Atmosphere Background Lerp ---
  function updateAtmosphereColors(dt) {
    if (state.isUltActive) {
      state.bgTarget = { r: 4, g: 26, b: 42 };
    } else if (state.activeBoss) {
      if (state.activeBoss.type === 'bigboss') {
        state.bgTarget = { r: 30, g: 4, b: 16 };
      } else {
        state.bgTarget = { r: 8, g: 14, b: 36 };
      }
    } else if (state.bossWarningActive) {
      const sirenPulse = (Math.sin(state.survivalTime * 14) + 1) * 0.5;
      state.bgTarget = {
        r: Math.round(14 + sirenPulse * 28),
        g: 6,
        b: Math.round(18 + sirenPulse * 8)
      };
    } else {
      state.bgTarget = { r: 10, g: 8, b: 20 };
    }

    const lerpSpeed = 3.5 * dt;
    state.bgCurrent.r += (state.bgTarget.r - state.bgCurrent.r) * lerpSpeed;
    state.bgCurrent.g += (state.bgTarget.g - state.bgCurrent.g) * lerpSpeed;
    state.bgCurrent.b += (state.bgTarget.b - state.bgCurrent.b) * lerpSpeed;
  }

  // --- Dynamic Multi-Layer Parallax Stage Environments per Level ---
  function drawStageParallaxBackdrop(ctx) {
    if (state.activeBoss || state.bossWarningActive) return; // Boss arena overrides backdrop
    const t = Date.now() * 0.0004;

    ctx.save();
    if (state.difficulty === 'easy') {
      // --- Level 1 (EASY): Azure Sector & Ringed Gas Giant Planet ---
      const planetX = CANVAS_WIDTH * 0.82;
      const planetY = 130;
      const planetR = 48;

      // Atmospheric Glow
      const atmGrad = ctx.createRadialGradient(planetX, planetY, planetR * 0.8, planetX, planetY, planetR * 1.5);
      atmGrad.addColorStop(0, 'rgba(0, 243, 255, 0.22)');
      atmGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = atmGrad;
      ctx.beginPath();
      ctx.arc(planetX, planetY, planetR * 1.5, 0, Math.PI * 2);
      ctx.fill();

      // Planet Sphere
      const pGrad = ctx.createLinearGradient(planetX - planetR, planetY - planetR, planetX + planetR, planetY + planetR);
      pGrad.addColorStop(0, '#0a2540');
      pGrad.addColorStop(0.5, '#00d2ff');
      pGrad.addColorStop(1, '#001a33');
      ctx.fillStyle = pGrad;
      ctx.beginPath();
      ctx.arc(planetX, planetY, planetR, 0, Math.PI * 2);
      ctx.fill();

      // Translucent Planetary Ring
      ctx.save();
      ctx.translate(planetX, planetY);
      ctx.rotate(-0.35);
      ctx.strokeStyle = 'rgba(0, 243, 255, 0.35)';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.ellipse(0, 0, planetR * 2.1, 14, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

    } else if (state.difficulty === 'normal') {
      // --- Level 2 (NORMAL): Solar Nebula & Cratered Moon ---
      const neb1 = ctx.createRadialGradient(CANVAS_WIDTH * 0.75, 140, 10, CANVAS_WIDTH * 0.75, 140, 220);
      neb1.addColorStop(0, 'rgba(184, 68, 255, 0.18)');
      neb1.addColorStop(0.5, 'rgba(255, 42, 133, 0.08)');
      neb1.addColorStop(1, 'transparent');
      ctx.fillStyle = neb1;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.75, 140, 220, 0, Math.PI * 2);
      ctx.fill();

      // Distant Cratered Asteroid Moon
      const moonX = CANVAS_WIDTH * 0.80;
      const moonY = 320;
      const moonR = 38;
      const mGrad = ctx.createLinearGradient(moonX - moonR, moonY, moonX + moonR, moonY);
      mGrad.addColorStop(0, '#2d1840');
      mGrad.addColorStop(0.6, '#ffd000');
      mGrad.addColorStop(1, '#11051a');
      ctx.fillStyle = mGrad;
      ctx.beginPath();
      ctx.arc(moonX, moonY, moonR, 0, Math.PI * 2);
      ctx.fill();

    } else if (state.difficulty === 'hard') {
      // --- Level 3 (HARD): Crimson Supernova Core & Solar Flares ---
      const starX = CANVAS_WIDTH * 0.84;
      const starY = 240;
      const starR = 55;

      // Pulsating Supernova Corona
      const sGrad = ctx.createRadialGradient(starX, starY, starR * 0.6, starX, starY, starR * 2.5);
      sGrad.addColorStop(0, 'rgba(255, 100, 0, 0.32)');
      sGrad.addColorStop(0.45, 'rgba(255, 0, 85, 0.14)');
      sGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = sGrad;
      ctx.beginPath();
      ctx.arc(starX, starY, starR * 2.5, 0, Math.PI * 2);
      ctx.fill();

      // Blazing Core
      ctx.fillStyle = '#ff2200';
      ctx.beginPath();
      ctx.arc(starX, starY, starR, 0, Math.PI * 2);
      ctx.fill();

      // Solar Corona Spikes
      ctx.strokeStyle = 'rgba(255, 140, 0, 0.18)';
      ctx.lineWidth = 2;
      for (let s = 0; s < 8; s++) {
        const a = t * 2 + (s * Math.PI / 4);
        ctx.beginPath();
        ctx.moveTo(starX + Math.cos(a) * starR, starY + Math.sin(a) * starR);
        ctx.lineTo(starX + Math.cos(a) * (starR + 45), starY + Math.sin(a) * (starR + 45));
        ctx.stroke();
      }

    } else {
      // --- Level 4 (HARDCOREZ): Void Singularity / Event Horizon Black Hole ---
      const bhX = CANVAS_WIDTH * 0.80;
      const bhY = 240;
      const bhR = 48;

      // Accretion Disk Swirl
      const diskGrad = ctx.createRadialGradient(bhX, bhY, bhR, bhX, bhY, bhR * 3.2);
      diskGrad.addColorStop(0, 'rgba(224, 170, 255, 0.35)');
      diskGrad.addColorStop(0.4, 'rgba(123, 44, 191, 0.18)');
      diskGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = diskGrad;
      ctx.beginPath();
      ctx.arc(bhX, bhY, bhR * 3.2, 0, Math.PI * 2);
      ctx.fill();

      // Relativistic Ultraviolet Photon Ring
      ctx.strokeStyle = '#e0aaff';
      ctx.lineWidth = 3;
      ctx.shadowColor = '#e0aaff';
      ctx.shadowBlur = 16;
      ctx.beginPath();
      ctx.arc(bhX, bhY, bhR + 4, 0, Math.PI * 2);
      ctx.stroke();

      // Pitch Black Singularity Void Core
      ctx.fillStyle = '#020108';
      ctx.beginPath();
      ctx.arc(bhX, bhY, bhR, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  function drawBossAtmosphereBackdrop(ctx) {
    if (!state.activeBoss && !state.bossWarningActive) return;
    const isBig = state.activeBoss ? (state.activeBoss.type === 'bigboss') : (state.bossCycle % 2 === 0);
    const arenaX = CANVAS_WIDTH * 0.78;
    const arenaY = CANVAS_HEIGHT * 0.5;

    ctx.save();
    if (isBig) {
      // Blood Eclipse Dark Sun & Corona Flares
      const coronaGrad = ctx.createRadialGradient(arenaX, arenaY, 40, arenaX, arenaY, 320);
      coronaGrad.addColorStop(0, 'rgba(255, 0, 85, 0.28)');
      coronaGrad.addColorStop(0.4, 'rgba(255, 120, 0, 0.12)');
      coronaGrad.addColorStop(0.75, 'rgba(80, 0, 120, 0.05)');
      coronaGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = coronaGrad;
      ctx.beginPath();
      ctx.arc(arenaX, arenaY, 320, 0, Math.PI * 2);
      ctx.fill();

      // Rotating Solar Corona Ray Spikes
      const rayAngle = Date.now() * 0.0006;
      ctx.strokeStyle = 'rgba(255, 60, 0, 0.12)';
      ctx.lineWidth = 1.8;
      for (let i = 0; i < 12; i++) {
        const a = rayAngle + (i * Math.PI * 2 / 12);
        ctx.beginPath();
        ctx.moveTo(arenaX + Math.cos(a) * 60, arenaY + Math.sin(a) * 60);
        ctx.lineTo(arenaX + Math.cos(a) * (180 + Math.sin(Date.now() * 0.004 + i) * 30), arenaY + Math.sin(a) * (180 + Math.sin(Date.now() * 0.004 + i) * 30));
        ctx.stroke();
      }

      // Dark Eclipse Body Silhouette
      ctx.fillStyle = '#06020c';
      ctx.beginPath();
      ctx.arc(arenaX, arenaY, 55, 0, Math.PI * 2);
      ctx.fill();
    } else {
      // Miniboss: Swirling Electric Ion Storm Clouds
      const stormGrad = ctx.createRadialGradient(arenaX, arenaY, 30, arenaX, arenaY, 260);
      stormGrad.addColorStop(0, 'rgba(0, 243, 255, 0.22)');
      stormGrad.addColorStop(0.5, 'rgba(120, 0, 255, 0.1)');
      stormGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = stormGrad;
      ctx.beginPath();
      ctx.arc(arenaX, arenaY, 260, 0, Math.PI * 2);
      ctx.fill();

      // Distant Ambient Lightning Flashes
      if (Math.random() < 0.035) {
        ctx.strokeStyle = 'rgba(0, 243, 255, 0.35)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        let lx = arenaX - 80 + Math.random() * 160;
        let ly = arenaY - 120;
        ctx.moveTo(lx, ly);
        for (let j = 0; j < 5; j++) {
          lx += (Math.random() - 0.5) * 45;
          ly += 45;
          ctx.lineTo(lx, ly);
        }
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  // --- VFX & Helpers ---
  class ExplosionAnim {
    constructor(x, y, radius = 24, color = '#ff7700') {
      this.x = x;
      this.y = y;
      // Scale sprite appropriately: radius 12 (small) -> ~34px, radius 28 (armored) -> ~78px, boss -> up to 240px
      this.size = Math.min(260, Math.max(30, radius * 2.8));
      this.rotation = Math.random() * Math.PI * 2;
      this.totalDuration = 0.42; // ~420ms total animation across 16 frames (~26ms per frame)
      this.life = this.totalDuration;
      this.color = color;
    }

    update(dt) {
      this.life -= dt;
    }

    draw(ctx) {
      if (this.life <= 0) return;
      const progress = Math.max(0, Math.min(1, 1 - (this.life / this.totalDuration)));
      const frameIndex = Math.min(15, Math.floor(progress * 16));
      const col = frameIndex % 4;
      const row = Math.floor(frameIndex / 4);

      const img = assets.images['explosion_sheet'];
      if (img && img.complete && img.naturalWidth > 0) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);

        if (progress < 0.6) {
          ctx.shadowBlur = 12;
          ctx.shadowColor = progress < 0.25 ? '#ffffff' : '#ff9900';
        }

        const halfSize = this.size / 2;
        ctx.drawImage(
          img,
          col * 128, row * 128, 128, 128,
          -halfSize, -halfSize, this.size, this.size
        );
        ctx.restore();
      } else {
        ctx.save();
        ctx.globalAlpha = Math.max(0, this.life / this.totalDuration);
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 0.4 * (1 - progress * 0.5), 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }
  }

  function createExplosion(x, y, radius, color) {
    // 1. Spawn animated explosion sprite sheet instance
    explosionAnims.push(new ExplosionAnim(x, y, radius, color));

    // 2. Shockwave blast ring for noticeable detonations
    if (radius >= 14) {
      particles.push({
        x: x,
        y: y,
        vx: 0,
        vy: 0,
        size: radius * 0.4,
        growth: radius * 2.2,
        isRing: true,
        ringWidth: radius > 30 ? 3 : 2,
        color: '#ffcc00',
        life: 0.22,
        maxLife: 0.22
      });
    }

    // 3. Fast high-velocity incendiary sparks/embers (replaces the floaty circular bubbles)
    const sparkCount = Math.min(8, 3 + Math.floor(radius * 0.2));
    for (let i = 0; i < sparkCount; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 120 + Math.random() * 160;
      particles.push({
        x: x,
        y: y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: 1.2 + Math.random() * 1.4,
        color: Math.random() < 0.5 ? '#ffffff' : Math.random() < 0.8 ? '#ffd000' : '#ff4400',
        life: 0.16 + Math.random() * 0.14,
        maxLife: 0.3
      });
    }
  }

  function createMuzzleSparks(x, y) {
    for (let i = 0; i < 3; i++) {
      particles.push({
        x: x,
        y: y + (Math.random() - 0.5) * 8,
        vx: 150 + Math.random() * 90,
        vy: (Math.random() - 0.5) * 70,
        size: 2,
        color: '#00f3ff',
        life: 0.12,
        maxLife: 0.12
      });
    }
  }

  function createFloatingText(text, x, y, color = '#fff') {
    floatingTexts.push({
      text,
      x,
      y,
      color,
      alpha: 1,
      life: 0.85
    });
  }

  function drawPolygon(ctx, x, y, radius, sides, pointiness = 0.5) {
    ctx.beginPath();
    for (let i = 0; i < sides * 2; i++) {
      const r = i % 2 === 0 ? radius : radius * pointiness;
      const a = (i * Math.PI) / sides - Math.PI / 2;
      const px = x + Math.cos(a) * r;
      const py = y + Math.sin(a) * r;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fill();
  }

  function drawJaggedCircle(ctx, x, y, radius) {
    ctx.beginPath();
    const points = 8;
    for (let i = 0; i < points; i++) {
      const a = (i * Math.PI * 2) / points;
      const offset = (Math.sin(i * 3.7) * 0.18 + 0.95);
      const px = x + Math.cos(a) * radius * offset;
      const py = y + Math.sin(a) * radius * offset;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  function rollPowerUpDrop(x, y, meteorType) {
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    let baseDropRate = conf.powerupDropRate || 0.22;

    if (meteorType === 'star') baseDropRate = 1.0;
    else if (meteorType === 'armored') baseDropRate = Math.min(1.0, baseDropRate * 2.2);
    else if (meteorType === 'wall_block') baseDropRate = baseDropRate * 0.45;

    if (Math.random() < baseDropRate) {
      let kind;
      if (meteorType === 'star') {
        kind = 'STAR';
      } else {
        const roll = Math.random();
        const heartThreshold = conf.heartDropWeight || 0.12;
        const shieldThreshold = heartThreshold + (conf.survivalDropWeight || 0.15);

        if (roll < heartThreshold) {
          kind = 'HEART';
        } else if (roll < shieldThreshold) {
          kind = 'SHIELD';
        } else {
          // 65% chance to drop character-specific powerups, 35% generic powerup
          const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;
          const charPool = shipConf.uniquePowerups || ['RAPID', 'MULTI'];

          if (Math.random() < 0.65 && charPool.length > 0) {
            kind = charPool[Math.floor(Math.random() * charPool.length)];
          } else {
            const genericPool = ['RAPID', 'MULTI', 'PIERCE', 'BURST'];
            kind = genericPool[Math.floor(Math.random() * genericPool.length)];
          }
        }
      }
      powerUps.push(new PowerUp(x, y, kind));
    }
  }

  // --- Spawner Logic (From Right Edge) ---
  function updateSpawners(dt) {
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

    // Checkpoint Boss Trigger (every 60s: 60s, 120s, 180s, ...)
    if (!state.activeBoss && !state.bossWarningActive && state.survivalTime >= state.nextBossCheckpoint) {
      triggerBossEncounter();
    }

    // During Boss encounter or warning, pause heavy meteor spawns
    if (state.activeBoss || state.bossWarningActive) {
      state.meteorSpawnTimer -= dt;
      if (state.meteorSpawnTimer <= 0) {
        state.meteorSpawnTimer = 3.5;
        const spawnY = 40 + Math.random() * (CANVAS_HEIGHT - 80);
        meteors.push(new Meteor(CANVAS_WIDTH + 30, spawnY, Math.random() < 0.6 ? 'star' : 'normal'));
      }
      return;
    }

    state.difficultyMultiplier = (1.0 + Math.min(2.5, state.score / 2500)) * conf.meteorSpeedMult;

    state.meteorSpawnTimer -= dt;
    const baseSpawnRate = Math.max(0.28, (1.1 / state.difficultyMultiplier) * conf.meteorSpawnRateMult);

    if (state.meteorSpawnTimer <= 0) {
      state.meteorSpawnTimer = baseSpawnRate;

      const spawnY = 30 + Math.random() * (CANVAS_HEIGHT - 60);
      const spawnX = CANVAS_WIDTH + 40;
      const roll = Math.random();

      const fastRate = (conf.fastEnemySpawnRate || 0.12) * Math.min(2.0, 1.0 + state.survivalTime * 0.007);
      if (roll < fastRate) {
        meteors.push(new Meteor(spawnX, spawnY, 'fast_scout'));
      } else if (roll < fastRate + 0.08) {
        meteors.push(new Meteor(spawnX, spawnY, 'star'));
      } else if (roll < fastRate + 0.28) {
        meteors.push(new Meteor(spawnX, spawnY, 'armored'));
      } else if (roll < fastRate + 0.58) {
        meteors.push(new Meteor(spawnX, spawnY, 'medium'));
      } else {
        meteors.push(new Meteor(spawnX, spawnY, 'normal'));
      }
    }

    // Periodic Wall Barrier (Vertical column on the right edge)
    state.wallSpawnTimer += dt;
    if (state.wallSpawnTimer > (conf.touhouDanmaku ? 14 : 18)) {
      state.wallSpawnTimer = 0;
      spawnWallFormation();
    }
  }

  function triggerBossEncounter() {
    const bossConfig = getNextBossConfig(state.difficulty, state.bossCycle);
    const isBig = bossConfig.isBig;
    const t = TRANSLATIONS[state.lang] || TRANSLATIONS.id;

    state.bossWarningActive = true;
    state.warningTimer = 2.4;
    state.pendingBossConfig = bossConfig;

    if (bossWarningBanner) {
      bossWarningBanner.classList.remove('hidden');
      const titleEl = bossWarningBanner.querySelector('.warning-title');
      if (titleEl) titleEl.textContent = t.bossWarningTitle;
    }
    if (bossWarningAvatar) {
      const archetypeAvatars = {
        spaceship: 'assets/images/boss_spaceship_dreadnought.png',
        mecha: 'assets/images/boss_mecha_titan.png',
        monster: 'assets/images/boss_alien_leviathan.png',
        humanoid: 'assets/images/boss_humanoid_valkyrie.png',
        alien: 'assets/images/boss_eldritch_eye.png'
      };
      bossWarningAvatar.src = archetypeAvatars[bossConfig.archetype] || (isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png');
      bossWarningAvatar.style.borderColor = bossConfig.color || '#ff0055';
    }
    if (warningSub) {
      warningSub.textContent = `#${String(bossConfig.id).padStart(3, '0')} ${bossConfig.name.toUpperCase()} - ${bossConfig.title.toUpperCase()}`;
    }
    window.soundFx.playBossWarning();
    window.soundFx.playBGM(isBig ? 'boss' : 'miniboss');

    // Clear normal meteors to prepare the duel arena
    meteors.forEach(m => m.destroy(false));
  }

  function spawnWallFormation() {
    createFloatingText('⚠️ METEOR WALL AHEAD! ⚠️', CANVAS_WIDTH / 2, 70, '#ff2a85');
    const rows = 8;
    const rowHeight = CANVAS_HEIGHT / rows;
    // Leave 1-2 random opening rows to dodge through
    const gapRow = Math.floor(Math.random() * (rows - 1));

    for (let i = 0; i < rows; i++) {
      if (i === gapRow || i === gapRow + 1) continue;
      const y = i * rowHeight + rowHeight / 2;
      meteors.push(new Meteor(CANVAS_WIDTH + 40, y, 'wall_block'));
    }
  }

  // --- Collisions & Damage ---
  function checkCollisions(dt) {
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    const hurtboxR = (player.height / 2) * conf.hurtboxScale;

    // 1. Ultimate Horizontal Laser Beam vs Meteors, Bullets & Boss
    if (state.isUltActive) {
      const beamHalfH = 85;
      const beamY = player.y;

      for (const m of meteors) {
        if (!m.toRemove && m.x >= player.x && Math.abs(m.y - beamY) < beamHalfH + m.radius) {
          m.destroy(true);
        }
      }

      // Ult obliterates enemy bullets in beam
      for (const b of enemyBullets) {
        if (!b.toRemove && b.x >= player.x && Math.abs(b.y - beamY) < beamHalfH + b.radius) {
          b.toRemove = true;
          createExplosion(b.x, b.y, 8, '#00f3ff');
        }
      }

      // Ult deals continuous high damage to Boss
      if (state.activeBoss && !state.activeBoss.toRemove) {
        const boss = state.activeBoss;
        if (boss.x >= player.x && Math.abs(boss.y - beamY) < beamHalfH + boss.height / 2) {
          boss.hit(45 * (dt || 0.016));
          if (Math.random() < 0.35) {
            createExplosion(boss.x - 20, boss.y + (Math.random() - 0.5) * 40, 10, '#00f3ff');
          }
        }
      }
    }

    // 2. Projectiles vs Meteors
    for (const p of projectiles) {
      if (p.toRemove) continue;
      for (const m of meteors) {
        if (m.toRemove) continue;
        const dx = p.x - m.x;
        const dy = p.y - m.y;
        const dist = Math.hypot(dx, dy);

        if (dist < p.radius + m.radius) {
          m.hit(1);

          if (p.isBurst) {
            triggerAoEBurst(m.x, m.y, 80);
          }

          p.pierceHits++;
          if (p.pierceHits >= p.maxHits) {
            p.toRemove = true;
            break;
          }
        }
      }
    }

    // 3. Projectiles vs Boss
    if (state.activeBoss && !state.activeBoss.toRemove) {
      const boss = state.activeBoss;
      for (const p of projectiles) {
        if (p.toRemove) continue;
        const dx = Math.abs(p.x - boss.x);
        const dy = Math.abs(p.y - boss.y);

        if (dx < (boss.width / 2) + p.radius && dy < (boss.height / 2) + p.radius) {
          boss.hit(1);

          if (p.isBurst) {
            triggerAoEBurst(boss.x, boss.y, 80);
          }

          p.pierceHits++;
          if (p.pierceHits >= p.maxHits) {
            p.toRemove = true;
          }
        }
      }
    }

    // 4. Enemy Bullets vs Player (Precision hurtbox scale)
    if (player.invulnerableTimer <= 0 && !state.isUltActive) {
      for (const b of enemyBullets) {
        if (b.toRemove) continue;
        const dist = Math.hypot(player.x - b.x, player.y - b.y);
        if (dist < hurtboxR + b.radius) {
          b.toRemove = true;
          playerTakeDamage();
          createExplosion(b.x, b.y, 14, '#ff3344');
          break;
        }
      }
    }

    // 5. Player vs Boss Body Collision
    if (player.invulnerableTimer <= 0 && !state.isUltActive && state.activeBoss && !state.activeBoss.toRemove) {
      const boss = state.activeBoss;
      const dx = Math.abs(player.x - boss.x);
      const dy = Math.abs(player.y - boss.y);
      if (dx < (boss.width / 2) + hurtboxR && dy < (boss.height / 2) + hurtboxR) {
        playerTakeDamage();
        boss.hit(5);
      }
    }

    // 6. Player vs Meteors
    if (player.invulnerableTimer <= 0 && !state.isUltActive) {
      for (const m of meteors) {
        if (m.toRemove) continue;
        const dx = player.x - m.x;
        const dy = player.y - m.y;
        const dist = Math.hypot(dx, dy);

        if (dist < hurtboxR + m.radius * 0.75) {
          playerTakeDamage();
          m.destroy();
          break;
        }
      }
    }

    // 7. Player vs Power-ups
    for (const pup of powerUps) {
      if (pup.toRemove) continue;
      const dx = player.x - pup.x;
      const dy = player.y - pup.y;
      const dist = Math.hypot(dx, dy);

      if (dist < (player.height / 2) + pup.radius) {
        pup.collect();
      }
    }
  }

  function triggerAoEBurst(x, y, radius) {
    createExplosion(x, y, radius * 0.8, '#ff7700');
    window.soundFx.playExplosion();
    for (const m of meteors) {
      if (!m.toRemove) {
        const d = Math.hypot(m.x - x, m.y - y);
        if (d <= radius) {
          m.hit(2);
        }
      }
    }
  }

  function playerTakeDamage() {
    // 3D Cosmic Forcefield Shield Absorption Check
    if (player.buffs && player.buffs.shield > 0) {
      player.buffs.shield = 0;
      player.invulnerableTimer = 1.2;
      createShieldDeflectFx(player.x, player.y);
      updateBuffDisplay();
      return;
    }

    state.lives--;
    updateHeartsDisplay();
    state.screenShake = 12;
    window.soundFx.playHurt();
    player.invulnerableTimer = 2.0;

    if (state.lives <= 0) {
      triggerGameOver();
    }
  }

  function updateHeartsDisplay() {
    if (!heartsContainer) return;
    heartsContainer.innerHTML = '';
    for (let i = 0; i < state.maxLives; i++) {
      const img = document.createElement('img');
      img.src = 'assets/images/cyber_heart.png';
      img.className = 'heart-img' + (i < state.lives ? ' active' : ' lost');
      img.alt = `Life ${i + 1}`;
      heartsContainer.appendChild(img);
    }
  }

  function updateBuffDisplay() {
    activeBuffsEl.innerHTML = '';
    for (const buffKey in player.buffs) {
      const remaining = player.buffs[buffKey];
      if (remaining > 0) {
        const upper = buffKey.toUpperCase();
        const conf = BUFF_TYPES[upper];
        if (conf) {
          const badge = document.createElement('div');
          badge.className = 'buff-badge';
          badge.style.borderColor = conf.color;
          badge.innerHTML = `<span>${conf.symbol}</span> <span>${conf.name} ${remaining.toFixed(0)}s</span>`;
          activeBuffsEl.appendChild(badge);
        }
      }
    }
  }

  // --- Game Flow ---
  function startGame() {
    // Blur any focused button so pressing Space never triggers a button click
    if (document.activeElement && document.activeElement.blur) {
      document.activeElement.blur();
    }

    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;

    state.screen = 'playing';
    state.score = 0;
    state.survivalTime = 0;
    state.maxLives = conf.lives + shipConf.extraLives;
    state.lives = state.maxLives;
    state.surviveSkillCooldown = 0;
    state.chronoSlowMotionTimer = 0;
    state.bgCurrent = { r: 10, g: 8, b: 20 };
    state.bgTarget = { r: 10, g: 8, b: 20 };
    updateSurviveButtonUI();
    state.ultCharge = 0;
    state.isUltActive = false;
    state.difficultyMultiplier = conf.meteorSpeedMult;
    state.meteorSpawnTimer = 0.5;
    state.wallSpawnTimer = 0;
    state.nextBossCheckpoint = 60;
    state.bossCycle = 1;
    state.activeBoss = null;
    state.bossWarningActive = false;
    state.warningTimer = 0;

    projectiles = [];
    meteors = [];
    powerUps = [];
    particles = [];
    explosionAnims = [];
    floatingTexts = [];
    enemyBullets = [];

    if (bossBarContainer) bossBarContainer.classList.add('hidden');
    if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
    closeLeaderboard();

    player = new Player();
    initStarfield();
    updateHeartsDisplay();
    updateUltBar();
    updateBuffDisplay();
    updateHudDifficultyBadge();
    timerVal.textContent = '00:00';

    startScreen.classList.remove('active');
    gameOverScreen.classList.remove('active');
    pauseScreen.classList.remove('active');

    window.soundFx.init();
    window.soundFx.rotateTrackIfEnabled();
    window.soundFx.playBGM('stage');
  }

  function triggerGameOver() {
    state.screen = 'gameover';
    window.soundFx.stopBGM();
    window.soundFx.playGameOver();

    if (bossBarContainer) bossBarContainer.classList.add('hidden');
    if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
    state.activeBoss = null;
    enemyBullets = [];

    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    if (finalDiff) {
      finalDiff.textContent = `${conf.icon} ${conf.label}`;
    }

    let isNewScoreRecord = false;
    let isNewTimeRecord = false;

    if (state.score > state.highScore) {
      state.highScore = state.score;
      localStorage.setItem('starfall_high_score', state.highScore);
      isNewScoreRecord = true;
    }

    if (state.survivalTime > state.bestSurvivalTime) {
      state.bestSurvivalTime = state.survivalTime;
      localStorage.setItem('starfall_best_time', state.bestSurvivalTime);
      isNewTimeRecord = true;
    }

    finalScore.textContent = state.score;
    finalHighScore.textContent = state.highScore;
    highScoreVal.textContent = state.highScore;

    finalTime.textContent = formatTime(state.survivalTime);
    finalBestTime.textContent = formatTime(state.bestSurvivalTime);

    if ((isNewScoreRecord || isNewTimeRecord) && state.score > 0) {
      newRecordBadge.classList.remove('hidden');
    } else {
      newRecordBadge.classList.add('hidden');
    }

    // Configure Submit Score to Global Hall of Fame
    if (submitScoreSection) {
      if (state.score > 0) {
        submitScoreSection.classList.remove('hidden');
        if (btnSubmitScore) btnSubmitScore.disabled = false;
        isSubmittingScore = false;
        if (submitStatusMsg) {
          submitStatusMsg.textContent = '';
          submitStatusMsg.className = 'submit-status-msg';
        }
        const savedName = localStorage.getItem('starfall_pilot_name');
        if (savedName && pilotNameInput) pilotNameInput.value = savedName;
      } else {
        submitScoreSection.classList.add('hidden');
      }
    }

    gameOverScreen.classList.add('active');
  }

  function togglePause() {
    if (state.screen === 'playing') {
      state.screen = 'paused';
      window.soundFx.pauseBGM();
      pauseScreen.classList.add('active');
    } else if (state.screen === 'paused') {
      state.screen = 'playing';
      window.soundFx.resumeBGM();
      pauseScreen.classList.remove('active');
      state.lastTime = performance.now();
    }
  }

  function goToMenu() {
    if (document.activeElement && document.activeElement.blur) {
      document.activeElement.blur();
    }
    state.screen = 'start';
    window.soundFx.stopBGM();
    gameOverScreen.classList.remove('active');
    pauseScreen.classList.remove('active');
    startScreen.classList.add('active');

    // Clean up active gameplay entities
    meteors = [];
    projectiles = [];
    enemyBullets = [];
    powerUps = [];
    particles = [];
    explosionAnims = [];
    floatingTexts = [];
    state.activeBoss = null;
    state.bossPending = null;
    state.bossActive = false;
    state.isUltActive = false;
    state.ultCharge = 0;
    updateUltBar();
    if (bossBarContainer) bossBarContainer.classList.add('hidden');
    if (bossWarningBanner) bossWarningBanner.classList.add('hidden');

    // Reset player position and buffs
    if (player) {
      player.x = 80;
      player.y = canvas.height / 2;
      player.vx = 0;
      player.vy = 0;
      player.invulnerableTimer = 0;
      player.buffs = {};
    }
    updateBuffDisplay();

    // Reset timer & score displays
    timerVal.textContent = '00:00';
    scoreVal.textContent = '0';
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    state.lives = conf.lives;
    state.maxLives = conf.lives;
    updateHeartsDisplay();
    updateHudDifficultyBadge();
  }

  // --- Main Loop ---
  function gameLoop(timestamp) {
    if (!state.lastTime) state.lastTime = timestamp;
    const dt = Math.min((timestamp - state.lastTime) / 1000, 0.05);
    state.lastTime = timestamp;

    if (state.screen === 'playing') {
      update(dt);
    } else {
      // Ambient starfield drift in menu / gameover / pause
      for (const star of stars) {
        star.x -= star.speed * 18 * dt;
        if (star.x < 0) {
          star.x = CANVAS_WIDTH;
          star.y = Math.random() * CANVAS_HEIGHT;
        }
      }
    }

    render();
    requestAnimationFrame(gameLoop);
  }

  function update(dt) {
    // 1. Survival time counting (seconds and minutes)
    state.survivalTime += dt;
    timerVal.textContent = formatTime(state.survivalTime);

    // Dynamic Atmosphere Lerp
    updateAtmosphereColors(dt);

    // Survive Skill Cooldown
    if (state.surviveSkillCooldown > 0) {
      state.surviveSkillCooldown = Math.max(0, state.surviveSkillCooldown - dt);
      updateSurviveButtonUI();
    }

    // Chrono Slow Motion Time Dilation (70% slow-mo)
    let hazardDt = dt;
    if (state.chronoSlowMotionTimer > 0) {
      state.chronoSlowMotionTimer = Math.max(0, state.chronoSlowMotionTimer - dt);
      hazardDt = dt * 0.35;
    }

    // 2. Starfield scroll from Right to Left
    for (const star of stars) {
      star.x -= star.speed * (state.isUltActive ? 4 : 1) * 60 * dt;
      if (star.x < 0) {
        star.x = CANVAS_WIDTH;
        star.y = Math.random() * CANVAS_HEIGHT;
      }
    }

    // Screenshake decay
    if (state.screenShake > 0) {
      state.screenShake -= dt * 25;
      if (state.screenShake < 0) state.screenShake = 0;
    }

    // Ultimate timer
    if (state.isUltActive) {
      state.ultDuration -= dt;
      if (state.ultDuration <= 0) {
        state.isUltActive = false;
      }
    }

    // Boss Warning Timer Countdown
    if (state.bossWarningActive) {
      state.warningTimer -= dt;
      if (state.warningTimer <= 0) {
        state.bossWarningActive = false;
        if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
        const bConf = state.pendingBossConfig || getNextBossConfig(state.difficulty, state.bossCycle);
        state.activeBoss = new Boss(bConf, state.bossCycle);
        showBossBar(state.activeBoss);
      }
    }

    // Boss & Enemy Bullets Update
    if (state.activeBoss) {
      state.activeBoss.update(dt);
      if (state.activeBoss && state.activeBoss.toRemove) {
        state.activeBoss = null;
      }
    }

    enemyBullets.forEach(b => b.update(dt));
    enemyBullets = enemyBullets.filter(b => !b.toRemove);

    // Player update
    player.update(dt);

    // Spawners & Entities
    updateSpawners(dt);

    projectiles.forEach(p => p.update(dt));
    projectiles = projectiles.filter(p => !p.toRemove);

    meteors.forEach(m => m.update(dt));
    meteors = meteors.filter(m => !m.toRemove);

    powerUps.forEach(pup => pup.update(dt));
    powerUps = powerUps.filter(pup => !pup.toRemove);

    checkCollisions(dt);

    // Particles update
    particles.forEach(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
    });
    particles = particles.filter(p => p.life > 0);

    // Explosion animations update
    explosionAnims.forEach(exp => exp.update(dt));
    explosionAnims = explosionAnims.filter(exp => exp.life > 0);

    // Floating text update
    floatingTexts.forEach(ft => {
      ft.y -= 25 * dt;
      ft.life -= dt;
      ft.alpha = ft.life / 0.85;
    });
    floatingTexts = floatingTexts.filter(ft => ft.life > 0);

    // Passive score trickle (scaled by difficulty)
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    state.score += Math.floor(dt * 10 * conf.scoreMultiplier);
    scoreVal.textContent = state.score;

    if (Math.floor(Date.now() / 250) % 2 === 0) {
      updateBuffDisplay();
    }
  }

  function render() {
    ctx.save();

    if (state.screenShake > 0) {
      const shakeX = (Math.random() - 0.5) * state.screenShake * 2;
      const shakeY = (Math.random() - 0.5) * state.screenShake * 2;
      ctx.translate(shakeX, shakeY);
    }

    // Dynamic Atmosphere Background
    const bgR = Math.round(state.bgCurrent.r);
    const bgG = Math.round(state.bgCurrent.g);
    const bgB = Math.round(state.bgCurrent.b);
    ctx.fillStyle = `rgb(${bgR}, ${bgG}, ${bgB})`;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Dynamic Multi-Layer Parallax Stage Backdrop per Level
    drawStageParallaxBackdrop(ctx);

    // Celestial Boss Arena Backdrop (Eclipse / Ion Storm)
    if (state.activeBoss || state.bossWarningActive) {
      drawBossAtmosphereBackdrop(ctx);
    }

    // Starfield
    for (const star of stars) {
      ctx.fillStyle = star.color;
      ctx.globalAlpha = star.alpha;
      ctx.fillRect(star.x, star.y, star.size, star.size);
    }
    ctx.globalAlpha = 1.0;

    // Power-ups
    powerUps.forEach(pup => pup.draw(ctx));

    // Meteors
    meteors.forEach(m => m.draw(ctx));

    // Enemy Bullets
    enemyBullets.forEach(b => b.draw(ctx));

    // Boss
    if (state.activeBoss) {
      state.activeBoss.draw(ctx);
    }

    // Projectiles
    projectiles.forEach(p => p.draw(ctx));

    // Horizontal Stellar Blaster Ultimate Beam
    if (state.isUltActive) {
      drawHorizontalUltimateBeam(ctx);
    }

    // Player
    if (player && state.screen !== 'start') {
      player.draw(ctx);
    }

    // Explosion Animations
    for (const exp of explosionAnims) {
      exp.draw(ctx);
    }

    // Particles
    for (const p of particles) {
      if (p.isRing) {
        ctx.save();
        ctx.strokeStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.life / p.maxLife);
        ctx.lineWidth = p.ringWidth || 2;
        ctx.beginPath();
        const curR = p.size + (1 - p.life / p.maxLife) * (p.growth || 60);
        ctx.arc(p.x, p.y, curR, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
        continue;
      }
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0, p.life / p.maxLife);
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1.0;

    // Floating Text
    for (const ft of floatingTexts) {
      ctx.save();
      ctx.font = '10px "Press Start 2P", sans-serif';
      ctx.fillStyle = ft.color;
      ctx.globalAlpha = Math.max(0, ft.alpha);
      ctx.textAlign = 'center';
      ctx.shadowColor = '#000';
      ctx.shadowBlur = 4;
      ctx.fillText(ft.text, ft.x, ft.y);
      ctx.restore();
    }

    ctx.restore();
  }

  // Draw Horizontal Ultimate Laser Beam from ship to right screen edge
  function drawHorizontalUltimateBeam(ctx) {
    ctx.save();
    const beamH = 80 + Math.sin(Date.now() / 25) * 15;
    const beamY = player.y;
    const startX = player.x + 15;
    const beamLen = CANVAS_WIDTH - startX;

    // Outer glow
    const grad = ctx.createLinearGradient(0, beamY - beamH / 2, 0, beamY + beamH / 2);
    grad.addColorStop(0, 'rgba(0, 243, 255, 0)');
    grad.addColorStop(0.2, 'rgba(0, 243, 255, 0.45)');
    grad.addColorStop(0.5, 'rgba(255, 255, 255, 0.95)');
    grad.addColorStop(0.8, 'rgba(255, 42, 133, 0.45)');
    grad.addColorStop(1, 'rgba(255, 42, 133, 0)');

    ctx.fillStyle = grad;
    ctx.fillRect(startX, beamY - beamH / 2, beamLen, beamH);

    // Inner bright core
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 22;
    ctx.fillRect(startX, beamY - 14, beamLen, 28);

    // Moving energy pulse rings along beam
    const ringOffset = (Date.now() * 0.9) % 80;
    ctx.strokeStyle = '#ffd000';
    ctx.lineWidth = 3;
    for (let rx = startX + ringOffset; rx < CANVAS_WIDTH; rx += 80) {
      ctx.beginPath();
      ctx.ellipse(rx, beamY, 8, Math.max(0.1, beamH * 0.45), 0, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Nova energy core at laser muzzle
    if (assets.images['ult_icon']) {
      const coreSize = 56 + Math.sin(Date.now() / 20) * 10;
      ctx.drawImage(assets.images['ult_icon'], startX - coreSize / 2, beamY - coreSize / 2, coreSize, coreSize);
    }

    ctx.restore();
  }


  // --- Radiant Valkyrie Celestial Lance of Longinus Beam ---
  function drawValkyrieCelestialLanceBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.44;
    const beamY = boss.laserTargetY || boss.y;
    const endX = -40;
    const beamLen = muzzleX - endX;
    const t = Date.now() * 0.008;

    const fireProgress = Math.max(0, boss.laserFireTimer / 0.8);
    const beamPulse = (Math.sin(t * 22) + 1) * 0.5;
    const baseH = (46 + beamPulse * 16) * Math.min(1.0, fireProgress * 3.5);

    // 1. Broad Celestial Magenta/Gold Radiant Aura
    const grad = ctx.createLinearGradient(0, beamY - baseH * 1.5, 0, beamY + baseH * 1.5);
    grad.addColorStop(0, 'rgba(255, 0, 170, 0)');
    grad.addColorStop(0.25, 'rgba(255, 0, 170, 0.45)');
    grad.addColorStop(0.5, 'rgba(255, 220, 100, 0.85)');
    grad.addColorStop(0.75, 'rgba(255, 0, 170, 0.45)');
    grad.addColorStop(1, 'rgba(255, 0, 170, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(endX, beamY - baseH * 1.5, beamLen, baseH * 3.0);

    // 2. Pure White Starlight Core Lance
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#ffd000';
    ctx.shadowBlur = 24;
    ctx.fillRect(endX, beamY - baseH * 0.22, beamLen, baseH * 0.44);

    // 3. Rotating Sacred Diamond Glyph Rings Along Beam Path
    const ringSpacing = 85;
    const ringPhase = (Date.now() * 0.35) % ringSpacing;
    ctx.strokeStyle = '#ffd000';
    ctx.lineWidth = 2.5;
    for (let rx = endX + ringPhase; rx < muzzleX; rx += ringSpacing) {
      const dR = baseH * 0.85;
      ctx.beginPath();
      ctx.moveTo(rx, beamY - dR);
      ctx.lineTo(rx + 10, beamY);
      ctx.lineTo(rx, beamY + dR);
      ctx.lineTo(rx - 10, beamY);
      ctx.closePath();
      ctx.stroke();
    }

    ctx.restore();
  }

  // --- Colossal Boss Hyper-Railgun Laser Beam (Organic, Smooth, Cinematic) ---
  function drawBossHyperRailgunBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.44;
    const beamY = boss.laserTargetY || boss.y;
    const endX = -40;
    const beamLen = muzzleX - endX;
    const t = Date.now() * 0.007;

    // Fire progress curve
    const fireProgress = Math.max(0, boss.laserFireTimer / 0.75);
    const beamPulse = (Math.sin(t * 24) + 1) * 0.5;
    const baseH = (44 + beamPulse * 14) * Math.min(1.0, fireProgress * 3.5);

    // 1. Broad Volumetric Atmospheric Glow (Smooth Bezier Plasma Tube, NOT fillRect!)
    const auraH = baseH * 2.8;
    const steps = 36;
    const stepDx = beamLen / steps;

    ctx.save();
    const auraGrad = ctx.createLinearGradient(0, beamY - auraH / 2, 0, beamY + auraH / 2);
    auraGrad.addColorStop(0, 'rgba(255, 0, 85, 0)');
    auraGrad.addColorStop(0.25, 'rgba(255, 0, 85, 0.18)');
    auraGrad.addColorStop(0.5, 'rgba(255, 60, 140, 0.38)');
    auraGrad.addColorStop(0.75, 'rgba(255, 0, 85, 0.18)');
    auraGrad.addColorStop(1, 'rgba(255, 0, 85, 0)');
    ctx.fillStyle = auraGrad;
    ctx.beginPath();
    ctx.moveTo(muzzleX, beamY);
    for (let i = 0; i <= steps; i++) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.03 - t * 12) * 5.0;
      ctx.lineTo(curX, beamY - (auraH * 0.5) + wave);
    }
    for (let i = steps; i >= 0; i--) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.03 + t * 10 + 1.5) * 5.0;
      ctx.lineTo(curX, beamY + (auraH * 0.5) + wave);
    }
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // 2. Organic Rippling Plasma Envelope (Waved Contours)
    ctx.save();
    ctx.fillStyle = 'rgba(255, 10, 80, 0.8)';
    ctx.shadowColor = '#ff0055';
    ctx.shadowBlur = 24;
    ctx.beginPath();
    ctx.moveTo(muzzleX, beamY);

    for (let i = 0; i <= steps; i++) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.04 - t * 16) * 4.5 + Math.cos(curX * 0.07 + t * 10) * 2.5;
      const curY = beamY - (baseH * 0.5) + wave;
      ctx.lineTo(curX, curY);
    }
    for (let i = steps; i >= 0; i--) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.04 + t * 14 + 1.2) * 4.5 + Math.sin(curX * 0.08 - t * 11) * 2.5;
      const curY = beamY + (baseH * 0.5) + wave;
      ctx.lineTo(curX, curY);
    }
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // 3. Ultra-Dense Hot Corona Stream
    const coronaH = baseH * 0.55;
    const coronaGrad = ctx.createLinearGradient(0, beamY - coronaH / 2, 0, beamY + coronaH / 2);
    coronaGrad.addColorStop(0, 'rgba(255, 80, 160, 0.1)');
    coronaGrad.addColorStop(0.25, '#ff2a85');
    coronaGrad.addColorStop(0.5, '#ffffff');
    coronaGrad.addColorStop(0.75, '#00f3ff');
    coronaGrad.addColorStop(1, 'rgba(0, 243, 255, 0.1)');

    ctx.fillStyle = coronaGrad;
    ctx.beginPath();
    ctx.moveTo(muzzleX, beamY);
    for (let i = 0; i <= steps; i++) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.06 - t * 22) * 2.5;
      ctx.lineTo(curX, beamY - (coronaH * 0.5) + wave);
    }
    for (let i = steps; i >= 0; i--) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.06 + t * 20 + 2.0) * 2.5;
      ctx.lineTo(curX, beamY + (coronaH * 0.5) + wave);
    }
    ctx.closePath();
    ctx.fill();

    // 4. Pure White-Hot Center Laser Beam Core (Organic Wave, NOT fillRect!)
    const coreH = Math.max(7, baseH * 0.22);
    ctx.save();
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 18;
    ctx.beginPath();
    ctx.moveTo(muzzleX, beamY);
    for (let i = 0; i <= steps; i++) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.08 - t * 28) * 1.5;
      ctx.lineTo(curX, beamY - (coreH * 0.5) + wave);
    }
    for (let i = steps; i >= 0; i--) {
      const curX = muzzleX - i * stepDx;
      const wave = Math.sin(curX * 0.08 + t * 26 + 1.0) * 1.5;
      ctx.lineTo(curX, beamY + (coreH * 0.5) + wave);
    }
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // 5. Supersonic 3D Compression Rings / Shock Diamonds
    const ringSpacing = 52;
    const ringOffset = (Date.now() * 0.35) % ringSpacing;
    ctx.strokeStyle = '#00f3ff';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 12;

    for (let rx = muzzleX - ringOffset; rx > endX; rx -= ringSpacing) {
      const ringPulse = Math.sin((rx + t * 50) * 0.05) * 3;
      ctx.beginPath();
      const ringRadiusY = Math.max(0.1, (baseH * 0.48) + ringPulse);
      ctx.ellipse(rx, beamY, 7, ringRadiusY, 0, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(rx, beamY, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // 6. Jagged Electric Lightning Filaments Crawling along Beam
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.8;
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 8;
    ctx.beginPath();
    let lx = muzzleX;
    let ly = beamY;
    ctx.moveTo(lx, ly);
    while (lx > endX) {
      lx -= 30 + Math.random() * 25;
      ly = beamY + (Math.random() - 0.5) * (baseH * 0.7);
      ctx.lineTo(lx, ly);
    }
    ctx.stroke();

    // 7. Colossal Muzzle Blast (Spherical Solar Corona Flare, NOT a diamond star!)
    const flareR = 30 + beamPulse * 12;
    ctx.save();
    ctx.translate(muzzleX, beamY);

    // Blinding spherical plasma flare core
    const muzzleGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, flareR);
    muzzleGrad.addColorStop(0, '#ffffff');
    muzzleGrad.addColorStop(0.35, '#00f3ff');
    muzzleGrad.addColorStop(0.7, '#ff0055');
    muzzleGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = muzzleGrad;
    ctx.beginPath();
    ctx.arc(0, 0, flareR, 0, Math.PI * 2);
    ctx.fill();

    // Outer corona ring
    ctx.strokeStyle = 'rgba(0, 243, 255, 0.7)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(0, 0, flareR * 1.25, 0, Math.PI * 2);
    ctx.stroke();

    // Soft radial rays
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 12;
    for (let a = 0; a < 6; a++) {
      const angle = (a * Math.PI) / 3 + t * 2;
      const rayLen = flareR * (1.25 + (a % 2 === 0 ? 0.35 : 0.15));
      ctx.beginPath();
      ctx.moveTo(Math.cos(angle - 0.1) * 5, Math.sin(angle - 0.1) * 5);
      ctx.lineTo(Math.cos(angle) * rayLen, Math.sin(angle) * rayLen);
      ctx.lineTo(Math.cos(angle + 0.1) * 5, Math.sin(angle + 0.1) * 5);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    // 8. Screen Left Impact Flare & Energetic Sparks
    ctx.save();
    ctx.fillStyle = '#00f3ff';
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 18;
    ctx.beginPath();
    ctx.ellipse(0, beamY, 14, Math.max(0.1, baseH * 0.8), 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.ellipse(0, beamY, 6, Math.max(0.1, baseH * 0.45), 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    ctx.restore();
  }

  // --- 3D Spherical Forcefield Shield System ---
  function draw3DShieldBack(ctx, px, py, shieldRemaining) {
    if (shieldRemaining <= 0) return;
    const t = Date.now() * 0.0025;
    const isLow = shieldRemaining < 3.0;
    const flicker = isLow ? (Math.sin(Date.now() * 0.025) > 0 ? 0.35 : 0.95) : 1.0;
    const baseRadius = 38;

    ctx.save();
    ctx.globalAlpha = flicker;

    // Translucent Back Plasma Bubble
    const grad = ctx.createRadialGradient(px, py, 4, px, py, baseRadius);
    grad.addColorStop(0, 'rgba(0, 243, 255, 0.04)');
    grad.addColorStop(0.7, 'rgba(0, 180, 255, 0.12)');
    grad.addColorStop(1, 'rgba(0, 243, 255, 0.22)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(px, py, baseRadius, 0, Math.PI * 2);
    ctx.fill();

    // 3D Orbital Rings - Back Arcs (z < 0)
    draw3DOrbitRing(ctx, px, py, baseRadius, 0.6, t, false);
    draw3DOrbitRing(ctx, px, py, baseRadius + 3, -0.8, -t * 1.15, false);
    draw3DOrbitRing(ctx, px, py, baseRadius - 2, 1.2, t * 0.75 + 1.5, false);

    // 3D Orbiting Energy Crystals - Back Half (z < 0)
    draw3DShieldCrystals(ctx, px, py, baseRadius, t, false);

    ctx.restore();
  }

  function draw3DShieldFront(ctx, px, py, shieldRemaining) {
    if (shieldRemaining <= 0) return;
    const t = Date.now() * 0.0025;
    const isLow = shieldRemaining < 3.0;
    const flicker = isLow ? (Math.sin(Date.now() * 0.025) > 0 ? 0.35 : 0.95) : 1.0;
    const baseRadius = 38;

    ctx.save();
    ctx.globalAlpha = flicker;

    // 3D Orbital Rings - Front Arcs (z >= 0)
    draw3DOrbitRing(ctx, px, py, baseRadius, 0.6, t, true);
    draw3DOrbitRing(ctx, px, py, baseRadius + 3, -0.8, -t * 1.15, true);
    draw3DOrbitRing(ctx, px, py, baseRadius - 2, 1.2, t * 0.75 + 1.5, true);

    // 3D Hexagonal / Geodesic Grid Pulses on Front Hemisphere
    draw3DShieldHexLattice(ctx, px, py, baseRadius, t);

    // 3D Orbiting Energy Crystals - Front Half (z >= 0)
    draw3DShieldCrystals(ctx, px, py, baseRadius, t, true);

    // Outer Equator Rim Glow
    ctx.strokeStyle = '#00f3ff';
    ctx.lineWidth = 1.5;
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.arc(px, py, baseRadius, 0, Math.PI * 2);
    ctx.stroke();

    ctx.restore();
  }

  function draw3DOrbitRing(ctx, px, py, radius, pitch, yaw, frontHalf) {
    const steps = 40;
    ctx.lineWidth = frontHalf ? 2.2 : 1.2;
    ctx.strokeStyle = frontHalf ? '#00f3ff' : 'rgba(0, 243, 255, 0.35)';
    if (frontHalf) {
      ctx.shadowColor = '#00f3ff';
      ctx.shadowBlur = 8;
    } else {
      ctx.shadowBlur = 0;
    }

    const cosP = Math.cos(pitch);
    const sinP = Math.sin(pitch);
    const cosY = Math.cos(yaw);
    const sinY = Math.sin(yaw);

    let drawing = false;

    for (let i = 0; i <= steps; i++) {
      const phi = (i / steps) * Math.PI * 2;
      const cx = radius * Math.cos(phi);
      const cy = radius * Math.sin(phi);

      const y1 = cy * cosP;
      const z1 = cy * sinP;

      const x2 = cx * cosY + z1 * sinY;
      const z2 = -cx * sinY + z1 * cosY;
      const y2 = y1;

      const isFront = (z2 >= 0);

      if (isFront === frontHalf) {
        const sx = px + x2;
        const sy = py + y2;
        if (!drawing) {
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          drawing = true;
        } else {
          ctx.lineTo(sx, sy);
        }
      } else {
        if (drawing) {
          ctx.stroke();
          drawing = false;
        }
      }
    }
    if (drawing) {
      ctx.stroke();
    }
  }

  function draw3DShieldCrystals(ctx, px, py, radius, t, frontHalf) {
    const crystalCount = 4;
    const cosP = Math.cos(0.5);
    const sinP = Math.sin(0.5);

    for (let c = 0; c < crystalCount; c++) {
      const angle = (c / crystalCount) * Math.PI * 2 + t * 1.5;
      const cx = (radius + 2) * Math.cos(angle);
      const cy = (radius + 2) * Math.sin(angle);

      const y1 = cy * cosP;
      const z1 = cy * sinP;

      const x2 = cx * Math.cos(t * 0.5) + z1 * Math.sin(t * 0.5);
      const z2 = -cx * Math.sin(t * 0.5) + z1 * Math.cos(t * 0.5);
      const y2 = y1;

      const isFront = (z2 >= 0);
      if (isFront === frontHalf) {
        const sx = px + x2;
        const sy = py + y2;
        const depthScale = 1 + (z2 / radius) * 0.35;
        const size = (frontHalf ? 4.5 : 2.8) * depthScale;

        ctx.save();
        ctx.translate(sx, sy);
        ctx.rotate(t * 3 + c);

        if (frontHalf) {
          ctx.fillStyle = '#ffffff';
          ctx.shadowColor = '#00f3ff';
          ctx.shadowBlur = 12;
        } else {
          ctx.fillStyle = 'rgba(0, 243, 255, 0.4)';
          ctx.shadowBlur = 0;
        }

        ctx.beginPath();
        ctx.moveTo(0, -size);
        ctx.lineTo(size * 0.7, 0);
        ctx.lineTo(0, size);
        ctx.lineTo(-size * 0.7, 0);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
      }
    }
  }

  function draw3DShieldHexLattice(ctx, px, py, radius, t) {
    const hexPulse = (Math.sin(t * 4) + 1) * 0.5;
    ctx.strokeStyle = `rgba(0, 243, 255, ${0.2 + hexPulse * 0.25})`;
    ctx.lineWidth = 1.2;
    ctx.shadowColor = '#00f3ff';
    ctx.shadowBlur = 6;

    const hexOffsets = [
      { x: 12, y: -8, r: 9 },
      { x: -10, y: 12, r: 8 },
      { x: 8, y: 14, r: 7 }
    ];

    hexOffsets.forEach(h => {
      ctx.beginPath();
      for (let s = 0; s < 6; s++) {
        const a = (s * Math.PI) / 3 + t * 0.5;
        const hx = px + h.x + Math.cos(a) * h.r;
        const hy = py + h.y + Math.sin(a) * h.r;
        if (s === 0) ctx.moveTo(hx, hy);
        else ctx.lineTo(hx, hy);
      }
      ctx.closePath();
      ctx.stroke();
    });
  }

  function createShieldDeflectFx(x, y) {
    window.soundFx.playShieldDeflect();
    state.screenShake = 6;

    // Expand shockwave rings
    for (let r = 0; r < 2; r++) {
      particles.push({
        x: x,
        y: y,
        vx: 0,
        vy: 0,
        size: 30 + r * 15,
        color: '#00f3ff',
        isRing: true,
        ringWidth: 3.5,
        growth: 120,
        life: 0.28,
        maxLife: 0.28
      });
    }

    // Hexagonal crystal fragments flying outwards
    for (let i = 0; i < 22; i++) {
      const angle = (i / 22) * Math.PI * 2 + (Math.random() - 0.5) * 0.3;
      const speed = 120 + Math.random() * 220;
      particles.push({
        x: x + Math.cos(angle) * 36,
        y: y + Math.sin(angle) * 36,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: 2.5 + Math.random() * 3.5,
        color: Math.random() < 0.6 ? '#00f3ff' : '#ffffff',
        life: 0.4 + Math.random() * 0.3,
        maxLife: 0.7
      });
    }

    createFloatingText('SHIELD BLOCKED! 🛡️', x, y - 24, '#00f3ff');
  }

  // --- Input Handlers ---

  // --- Ship / Character Selection Carousel ---
  const shipKeys = Object.keys(SHIPS_CONFIG);
  function updateShipCardUI() {
    const shipId = state.selectedShip || 'stella_nova';
    const conf = SHIPS_CONFIG[shipId] || SHIPS_CONFIG.stella_nova;

    const shipAvatarImg = document.getElementById('shipAvatarImg');
    const shipClassBadge = document.getElementById('shipClassBadge');
    const shipNameText = document.getElementById('shipNameText');
    const statSpeedVal = document.getElementById('statSpeedVal');
    const statFireVal = document.getElementById('statFireVal');
    const statHpVal = document.getElementById('statHpVal');
    const shipSurviveDesc = document.getElementById('shipSurviveDesc');
    const shipUltDesc = document.getElementById('shipUltDesc');

    if (shipNameText) shipNameText.textContent = conf.name;
    if (shipClassBadge) {
      shipClassBadge.className = 'ship-class-badge ' + conf.badgeClass;
      shipClassBadge.textContent = conf.class;
    }
    if (statSpeedVal) {
      const speedLabel = conf.speed > 350 ? `HIGH (${conf.speed})` : conf.speed > 300 ? `BALANCED (${conf.speed})` : `HEAVY (${conf.speed})`;
      statSpeedVal.textContent = speedLabel;
    }
    if (statFireVal) statFireVal.textContent = conf.firepowerLabel;
    if (statHpVal) statHpVal.textContent = conf.hpLabel;
    if (shipSurviveDesc) shipSurviveDesc.textContent = conf.surviveDesc;
    if (shipUltDesc) shipUltDesc.textContent = conf.ultDesc;
    if (shipAvatarImg) {
      if (conf.avatarSrc) {
        shipAvatarImg.src = conf.avatarSrc;
        shipAvatarImg.style.filter = 'none';
      } else {
        shipAvatarImg.style.filter = conf.filter;
      }
    }

    const btnTouchSurvive = document.getElementById('btnTouchSurvive');
    if (btnTouchSurvive) {
      btnTouchSurvive.title = `Survive Skill: ${conf.surviveName} [C]`;
    }
  }

  function initShipSelection() {
    updateShipCardUI();

    const btnShipPrev = document.getElementById('btnShipPrev');
    const btnShipNext = document.getElementById('btnShipNext');

    if (btnShipPrev) {
      btnShipPrev.addEventListener('click', () => {
        let curIdx = shipKeys.indexOf(state.selectedShip);
        if (curIdx === -1) curIdx = 0;
        const prevIdx = (curIdx - 1 + shipKeys.length) % shipKeys.length;
        state.selectedShip = shipKeys[prevIdx];
        localStorage.setItem('starfall_selected_ship', state.selectedShip);
        if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
        updateShipCardUI();
      });
    }

    if (btnShipNext) {
      btnShipNext.addEventListener('click', () => {
        let curIdx = shipKeys.indexOf(state.selectedShip);
        if (curIdx === -1) curIdx = 0;
        const nextIdx = (curIdx + 1) % shipKeys.length;
        state.selectedShip = shipKeys[nextIdx];
        localStorage.setItem('starfall_selected_ship', state.selectedShip);
        if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
        updateShipCardUI();
      });
    }
  }

  function setupInputs() {
    window.addEventListener('keydown', e => {
      // If user is typing in the pilot name input, let them type freely
      if (e.target === pilotNameInput) {
        if (e.key === 'Enter') {
          e.preventDefault();
          submitPilotScore();
        }
        return;
      }

      // Close Modals on Escape
      if (e.code === 'Escape') {
        if (howToPlayModal && !howToPlayModal.classList.contains('hidden')) {
          e.preventDefault();
          closeHowToPlay();
          return;
        }
        if (leaderboardModal && !leaderboardModal.classList.contains('hidden')) {
          e.preventDefault();
          closeLeaderboard();
          return;
        }
      }

      // Fullscreen toggle on KeyF outside playing
      if (e.code === 'KeyF' && state.screen !== 'playing') {
        e.preventDefault();
        toggleFullscreen();
        return;
      }

      // Display Mode toggle on KeyV outside playing
      if (e.code === 'KeyV' && state.screen !== 'playing') {
        e.preventDefault();
        toggleDisplayMode();
        if (window.soundFx) window.soundFx.playPowerup();
        return;
      }

      // Prevent browser default actions (page scroll & triggering focused buttons)
      if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
        e.preventDefault();
      }

      // Movement
      if (e.code === 'KeyW' || e.code === 'ArrowUp') input.up = true;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') input.down = true;
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') input.left = true;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') input.right = true;

      // In-Game Ultimate (Space, Shift, E, or F)
      if (e.code === 'Space' || e.code === 'ShiftLeft' || e.code === 'ShiftRight' || e.code === 'KeyE' || e.code === 'KeyF') {
        if (state.screen === 'playing') {
          triggerUltimate();
        }
      }
      if (e.code === 'KeyC' || e.key === 'c' || e.key === 'C') {
        if (state.screen === 'playing') {
          activateSurviveSkill();
        }
      }

      // Quick Test Keys: B = Spawn Boss Now, K = Defeat Boss Instantly
      if (e.code === 'KeyB' || e.key === 'b' || e.key === 'B') {
        if (state.screen === 'playing') {
          if (state.activeBoss) state.activeBoss.destroy();
          state.bossWarningActive = false;
          triggerBossEncounter();
        }
      }
      if (e.code === 'KeyK' || e.key === 'k' || e.key === 'K') {
        if (state.screen === 'playing' && state.activeBoss) {
          state.activeBoss.hit(999999);
        }
      }

      // Menu Start / Restart (Space, Enter, or R)
      if (e.code === 'Space' || e.code === 'Enter' || e.code === 'KeyR') {
        if (state.screen === 'start' || state.screen === 'gameover') {
          startGame();
        }
      }

      // Return to Menu / Change Level (Key M) from GameOver or Paused
      if (e.code === 'KeyM') {
        if (state.screen === 'gameover' || state.screen === 'paused') {
          e.preventDefault();
          goToMenu();
        }
      }

      if (e.code === 'KeyP' || e.code === 'Escape') {
        e.preventDefault();
        togglePause();
      }
    });

    window.addEventListener('keyup', e => {
      if (e.code === 'KeyW' || e.code === 'ArrowUp') input.up = false;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') input.down = false;
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') input.left = false;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') input.right = false;
    });

    // Pointer / Touch direct drag tracking
    function getCanvasCoords(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      return {
        x: (clientX - rect.left) * scaleX,
        y: (clientY - rect.top) * scaleY
      };
    }

    canvas.addEventListener('pointerdown', e => {
      input.touchTarget = getCanvasCoords(e.clientX, e.clientY);
    });

    canvas.addEventListener('pointermove', e => {
      if (e.buttons > 0 || e.pointerType === 'touch') {
        input.touchTarget = getCanvasCoords(e.clientX, e.clientY);
      }
    });

    window.addEventListener('pointerup', () => {
      input.touchTarget = null;
    });

    // Touch D-Pad Buttons
    const bindTouchDir = (btn, dirKey) => {
      if (!btn) return;
      btn.addEventListener('pointerdown', e => {
        e.preventDefault();
        input[dirKey] = true;
      });
      btn.addEventListener('pointerup', e => {
        e.preventDefault();
        input[dirKey] = false;
      });
      btn.addEventListener('pointerleave', () => {
        input[dirKey] = false;
      });
    };

    bindTouchDir(btnTouchUp, 'up');
    bindTouchDir(btnTouchDown, 'down');
    bindTouchDir(btnTouchLeft, 'left');
    bindTouchDir(btnTouchRight, 'right');

    if (btnTouchUlt) {
      btnTouchUlt.addEventListener('pointerdown', e => {
        e.preventDefault();
        triggerUltimate();
      });
    }

    const btnTouchSurvive = document.getElementById('btnTouchSurvive');
    if (btnTouchSurvive) {
      btnTouchSurvive.addEventListener('pointerdown', e => {
        e.preventDefault();
        activateSurviveSkill();
      });
    }

    // Screen Buttons
    btnStart.addEventListener('click', startGame);
    btnRestart.addEventListener('click', startGame);
    btnResume.addEventListener('click', togglePause);
    if (btnMenuGameOver) btnMenuGameOver.addEventListener('click', goToMenu);
    if (btnMenuPause) btnMenuPause.addEventListener('click', goToMenu);

    btnToggleSound.addEventListener('click', () => {
      const muted = window.soundFx.toggleMute();
      btnToggleSound.textContent = muted ? '🔇' : '🔊';
    });

    btnTogglePause.addEventListener('click', togglePause);

    // Leaderboard & Submit Buttons
    if (btnLeaderboardStart) btnLeaderboardStart.addEventListener('click', openLeaderboard);
    if (btnLeaderboardGameOver) btnLeaderboardGameOver.addEventListener('click', openLeaderboard);
    if (btnCloseLeaderboard) btnCloseLeaderboard.addEventListener('click', closeLeaderboard);
    if (btnCloseLeaderboardBottom) btnCloseLeaderboardBottom.addEventListener('click', closeLeaderboard);
    if (btnRefreshLeaderboard) btnRefreshLeaderboard.addEventListener('click', fetchLeaderboard);
    if (btnSubmitScore) btnSubmitScore.addEventListener('click', submitPilotScore);

    // Flight Academy (How to Play) & Fullscreen Start Buttons
    if (btnHowToPlayStart) btnHowToPlayStart.addEventListener('click', openHowToPlay);
    const btnBossCodex = document.getElementById('btnBossCodex');
    if (btnBossCodex) btnBossCodex.addEventListener('click', openBossCodex);
    const btnCloseBossCodex = document.getElementById('btnCloseBossCodex');
    if (btnCloseBossCodex) btnCloseBossCodex.addEventListener('click', closeBossCodex);
    const btnCloseBossCodexBottom = document.getElementById('btnCloseBossCodexBottom');
    if (btnCloseBossCodexBottom) btnCloseBossCodexBottom.addEventListener('click', closeBossCodex);

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tier = btn.dataset.tier;
        if (tier) {
          renderBossCodex(tier);
          if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
        }
      });
    });
    if (btnCloseHowToPlay) btnCloseHowToPlay.addEventListener('click', closeHowToPlay);
    if (btnCloseHowToPlayBottom) btnCloseHowToPlayBottom.addEventListener('click', closeHowToPlay);
    if (btnFullscreenStart) {
      btnFullscreenStart.addEventListener('click', () => {
        toggleFullscreen();
        window.soundFx.playPowerup();
      });
    }

    // Difficulty Selector Buttons
    document.querySelectorAll('.diff-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        const diff = btn.dataset.diff;
        if (diff) {
          setDifficulty(diff);
          window.soundFx.playPowerup();
        }
      });
    });

    // Language Selector Buttons
    document.querySelectorAll('.lang-pill-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        const lang = btn.dataset.lang;
        if (lang) {
          setLanguage(lang);
          window.soundFx.playPowerup();
        }
      });
    });

    if (btnToggleLang) {
      btnToggleLang.addEventListener('click', () => {
        const nextLang = state.lang === 'id' ? 'en' : 'id';
        setLanguage(nextLang);
        window.soundFx.playPowerup();
      });
    }

    if (btnToggleFullscreen) {
      btnToggleFullscreen.addEventListener('click', () => {
        toggleFullscreen();
        window.soundFx.playPowerup();
      });
    }

    // Display Mode Switcher (Pill buttons & HUD toggle)
    document.querySelectorAll('.mode-pill-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        const mode = btn.dataset.mode;
        if (mode) {
          setDisplayMode(mode);
          if (window.soundFx) window.soundFx.playPowerup();
        }
      });
    });

    if (btnToggleDisplay) {
      btnToggleDisplay.addEventListener('click', () => {
        toggleDisplayMode();
        if (window.soundFx) window.soundFx.playPowerup();
      });
    }

    // Auto-blur all buttons after click/touch so Space never triggers native button click
    document.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => btn.blur());
      btn.addEventListener('pointerup', () => btn.blur());
    });
  }

  // --- Initialization ---
  function init() {
    const savedHi = localStorage.getItem('starfall_high_score');
    if (savedHi) {
      state.highScore = parseInt(savedHi, 10) || 0;
      highScoreVal.textContent = state.highScore;
    }

    const savedBestTime = localStorage.getItem('starfall_best_time');
    if (savedBestTime) {
      state.bestSurvivalTime = parseFloat(savedBestTime) || 0;
    }

    const savedLang = localStorage.getItem('starfall_lang') || 'id';
    setLanguage(savedLang);

    const savedDisplayMode = localStorage.getItem('starfall_display_mode') || 'immersive';
    setDisplayMode(savedDisplayMode);

    initStarfield();
    initShipSelection();
    setupInputs();
    window.gameState = state;
    window.startGame = startGame;
    window.selectShip = function(id) {
      if (SHIPS_CONFIG[id]) {
        state.selectedShip = id;
        localStorage.setItem('starfall_selected_ship', id);
        updateShipCardUI();
      }
    };
    window.setDifficulty = setDifficulty;
    window.selectDifficulty = setDifficulty;
    window.getPlayer = function() { return player; };

    const savedDiff = localStorage.getItem('starfall_difficulty');
    if (savedDiff && DIFFICULTY_CONFIGS[savedDiff]) {
      setDifficulty(savedDiff);
    } else {
      setDifficulty('normal');
    }

    // Debug / Preview mode via URL query parameter (?view=gameover | leaderboard | hud)
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const viewParam = urlParams.get('view');
      if (viewParam === 'gameover') {
        if (startScreen) startScreen.classList.remove('active');
        if (gameOverScreen) gameOverScreen.classList.add('active');
        if (finalDiff) {
          finalDiff.textContent = 'HARDCOREZ';
          finalDiff.className = 'result-val highlight diff-tag-hardcorez';
        }
        if (finalTime) finalTime.textContent = '00:08';
        if (finalBestTime) finalBestTime.textContent = '02:41';
        if (finalScore) finalScore.textContent = '2464';
        if (finalHighScore) finalHighScore.textContent = '22374';
        if (pilotNameInput) pilotNameInput.value = 'CELENK';
      } else if (viewParam === 'codex') {
        if (startScreen) startScreen.classList.remove('active');
        openBossCodex();
      } else if (viewParam === 'leaderboard') {
        if (startScreen) startScreen.classList.remove('active');
        if (leaderboardModal) leaderboardModal.classList.remove('hidden');
        if (leaderboardLoading) leaderboardLoading.classList.add('hidden');
        if (leaderboardTable) leaderboardTable.classList.remove('hidden');
        const tbody = document.getElementById('leaderboardBody');
        if (tbody) {
          tbody.innerHTML = `
            <tr class="rank-badge-1"><td class="col-rank">🥇 1</td><td class="col-name">CELENK</td><td class="col-diff"><span class="diff-tag diff-tag-normal">NORMAL</span></td><td class="col-score">22.374</td><td class="col-time">02:41</td></tr>
            <tr class="rank-badge-2"><td class="col-rank">🥈 2</td><td class="col-name">STELLA_ACE</td><td class="col-diff"><span class="diff-tag diff-tag-hard">HARD</span></td><td class="col-score">18.920</td><td class="col-time">02:15</td></tr>
            <tr class="rank-badge-3"><td class="col-rank">🥉 3</td><td class="col-name">CYBER_PILOT</td><td class="col-diff"><span class="diff-tag diff-tag-easy">EASY</span></td><td class="col-score">14.500</td><td class="col-time">01:50</td></tr>
          `;
        }
      } else if (viewParam === 'pause') {
        if (startScreen) startScreen.classList.remove('active');
        if (pauseScreen) pauseScreen.classList.add('active');
      } else if (viewParam === 'hud') {
        if (startScreen) startScreen.classList.remove('active');
        if (scoreVal) scoreVal.textContent = '3453';
        if (highScoreVal) highScoreVal.textContent = '22374';
        if (timerVal) timerVal.textContent = '00:20';
        if (hudDiffBadge) {
          hudDiffBadge.textContent = 'HARD';
          hudDiffBadge.className = 'hud-diff-badge diff-hard';
        }
      } else if (viewParam === 'shield') {
        startGame();
        player.buffs.shield = 10.0;
        player.x = 240;
        player.y = 240;
        powerUps.push(new PowerUp(420, 240, 'SHIELD'));
      } else if (viewParam === 'bosslaser') {
        startGame();
        player.x = 100;
        player.y = 360;
        const testBoss = new Boss('bigboss', 1);
        testBoss.x = 640;
        testBoss.y = 220;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        testBoss.laserTargetY = 220;
        testBoss.isFiringLaser = true;
        testBoss.laserFireTimer = 0.55;
        state.activeBoss = testBoss;
      } else if (viewParam === 'bossship') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 1, name: 'Void Dreadnought', title: 'Heavy Fleet Flagship', isBig: true, archetype: 'spaceship', color: '#00f3ff', baseHp: 200, attack: 'plasma_twin' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'valkyriecharge') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 16, name: 'Valkyrie Prime', title: 'Astral Cyber-Valkyrie', isBig: true, archetype: 'humanoid', color: '#ff00aa', baseHp: 220, attack: 'curtain_fan' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        testBoss.isCastingSkill = true;
        testBoss.castSkillDuration = 10.0;
        testBoss.castSkillTimer = 5.0;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'mechacharge') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 5, name: 'Iron Colossus', title: 'Celestial Mecha Titan', isBig: true, archetype: 'mecha', color: '#ffd000', baseHp: 240, attack: 'railgun_heavy' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        testBoss.isCastingSkill = true;
        testBoss.castSkillDuration = 10.0;
        testBoss.castSkillTimer = 5.0;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bossvalkyrie') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 16, name: 'Valkyrie Prime', title: 'Astral Cyber-Valkyrie', isBig: true, archetype: 'humanoid', color: '#ff00aa', baseHp: 220, attack: 'curtain_fan' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bossalien') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 21, name: 'Oculon Apex', title: 'Cyclopean Hive Mind', isBig: false, archetype: 'alien', color: '#b844ff', baseHp: 95, attack: 'spiral_danmaku' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'megaman_dash') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 240;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 360;
        testBoss.currentX = 360;
        testBoss.y = 230;
        testBoss.tilt = -0.38;
        testBoss.actionState = 'dash_strike';
        testBoss.actionTimer = 0.5;
        testBoss.afterimages = [
          { x: 520, y: 220, tilt: -0.32, alpha: 0.35, color: '#ff1493' },
          { x: 440, y: 225, tilt: -0.35, alpha: 0.70, color: '#ffd000' }
        ];
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'megaman_slam') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 300;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 420;
        testBoss.currentX = 420;
        testBoss.y = 250;
        testBoss.tilt = 0.35;
        testBoss.actionState = 'dive_slam';
        testBoss.actionTimer = 0.4;
        testBoss.afterimages = [
          { x: 490, y: 120, tilt: 0.22, alpha: 0.35, color: '#ffd000' },
          { x: 450, y: 185, tilt: 0.30, alpha: 0.70, color: '#ff1493' }
        ];
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'megaman_railgun') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 240;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 560;
        testBoss.currentX = 560;
        testBoss.y = 240;
        testBoss.laserTargetY = 240;
        testBoss.isFiringLaser = true;
        testBoss.laserFireTimer = 0.6;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'boss') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 5, name: 'Iron Colossus', title: 'Celestial Mecha Titan', isBig: true, archetype: 'mecha', color: '#ffd000', baseHp: 240, attack: 'railgun_heavy' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'miniboss') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss('miniboss', 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bosshit') {
        startGame();
        player.x = 100;
        player.y = 240;
        state.isUltActive = true;
        const testBoss = new Boss('bigboss', 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        testBoss.flashTimer = 0.5;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'minibosshit') {
        startGame();
        player.x = 100;
        player.y = 240;
        state.isUltActive = true;
        const testBoss = new Boss('miniboss', 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        testBoss.currentX = 640;
        testBoss.flashTimer = 0.5;
        state.activeBoss = testBoss;
      } else if (viewParam === 'explosion') {
        startGame();
        player.x = 100;
        player.y = 240;
        const e1 = new ExplosionAnim(360, 240, 24, '#ff7700');
        e1.life = 0.38;
        const e2 = new ExplosionAnim(500, 190, 36, '#ff4400');
        e2.life = 0.26;
        const e3 = new ExplosionAnim(640, 280, 48, '#ffd000');
        e3.life = 0.14;
        const e4 = new ExplosionAnim(780, 200, 32, '#ffaa00');
        e4.life = 0.05;
        explosionAnims.push(e1, e2, e3, e4);
        particles.push({
          x: 640,
          y: 280,
          vx: 0,
          vy: 0,
          size: 48 * 0.4,
          growth: 48 * 2.2,
          isRing: true,
          ringWidth: 3,
          color: '#ffcc00',
          life: 0.14,
          maxLife: 0.22
        });
        setInterval(() => {
          createExplosion(420 + Math.random() * 320, 140 + Math.random() * 200, 20 + Math.random() * 25, '#ff7700');
        }, 140);
      }
    } catch (e) {}

    requestAnimationFrame(gameLoop);
  }

  // Expose for testing/CDP
  window.gameState = state;
  window.testBoss = function(id = 56) {
    const bConf = (window.BOSS_CATALOG || []).find(b => b.id === id) || window.BOSS_CATALOG[0];
    state.activeBoss = new Boss(bConf, 2);
    showBossBar(state.activeBoss);
    return state.activeBoss;
  };
  init();
})();
