import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_diff_configs = '''  // Difficulty Level Configurations
  const DIFFICULTY_CONFIGS = {
    easy: {
      label: 'EASY',
      icon: '🟢',
      lives: 4,
      scoreMultiplier: 0.8,
      meteorSpeedMult: 0.82,
      meteorSpawnRateMult: 1.25,
      bossHpMult: 0.75,
      bossShootIntervalMult: 1.35,
      revengeBullets: false,
      touhouDanmaku: false,
      hurtboxScale: 0.75
    },
    normal: {
      label: 'NORMAL',
      icon: '🔵',
      lives: 3,
      scoreMultiplier: 1.0,
      meteorSpeedMult: 1.0,
      meteorSpawnRateMult: 1.0,
      bossHpMult: 1.0,
      bossShootIntervalMult: 1.0,
      revengeBullets: false,
      touhouDanmaku: false,
      hurtboxScale: 0.7
    },
    hard: {
      label: 'HARD',
      icon: '🔴',
      lives: 3,
      scoreMultiplier: 1.5,
      meteorSpeedMult: 1.22,
      meteorSpawnRateMult: 0.82,
      bossHpMult: 1.3,
      bossShootIntervalMult: 0.8,
      revengeBullets: false,
      touhouDanmaku: false,
      hurtboxScale: 0.65
    },
    hardcorez: {
      label: 'HARDCOREZ',
      icon: '🟣',
      lives: 2,
      scoreMultiplier: 2.5,
      meteorSpeedMult: 1.38,
      meteorSpawnRateMult: 0.68,
      bossHpMult: 1.6,
      bossShootIntervalMult: 0.65,
      revengeBullets: true,
      touhouDanmaku: true,
      hurtboxScale: 0.45,
      drawHitboxCore: true
    }
  };'''

new_diff_configs = '''  // Difficulty Level Configurations (Tuning Powerups, Enemy HP, Speed & Fast Scouts)
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
  };'''

assert old_diff_configs in text, "old_diff_configs not found"
text = text.replace(old_diff_configs, new_diff_configs, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated DIFFICULTY_CONFIGS in js/game.js!")
