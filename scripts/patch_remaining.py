# -*- coding: utf-8 -*-
import sys

def main():
    with open('js/game.js', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Patch startGame
    old_start = """    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

    state.screen = 'playing';
    state.score = 0;
    state.survivalTime = 0;
    state.lives = conf.lives;
    state.maxLives = conf.lives;"""

    new_start = """    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
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
    updateSurviveButtonUI();"""

    if old_start in src:
        src = src.replace(old_start, new_start)
        print("Patched startGame successfully!")
    else:
        print("Warning: old_start not matched!")

    # 2. Patch warning spawn in update(dt)
    old_warn_spawn = """    // Boss Warning Timer Countdown
    if (state.bossWarningActive) {
      state.warningTimer -= dt;
      if (state.warningTimer <= 0) {
        state.bossWarningActive = false;
        if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
        const isBig = (state.bossCycle % 2 === 0);
        const bossType = isBig ? 'bigboss' : 'miniboss';
        const bossTitle = isBig ? '🔥 BIG BOSS: TITAN APEX STARFALL 🔥' : '⚠️ MINI-BOSS: VOID DESTROYER ⚠️';
        state.activeBoss = new Boss(bossType, state.bossCycle);
        showBossBar(bossTitle);
      }
    }"""

    new_warn_spawn = """    // Boss Warning Timer Countdown
    if (state.bossWarningActive) {
      state.warningTimer -= dt;
      if (state.warningTimer <= 0) {
        state.bossWarningActive = false;
        if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
        const bConf = state.pendingBossConfig || getNextBossConfig(state.difficulty, state.bossCycle);
        state.activeBoss = new Boss(bConf, state.bossCycle);
        showBossBar(state.activeBoss);
      }
    }"""

    if old_warn_spawn in src:
        src = src.replace(old_warn_spawn, new_warn_spawn)
        print("Patched warningTimer boss spawn successfully!")
    else:
        print("Warning: old_warn_spawn not matched!")

    # 3. Patch key listener for KeyC (Survive skill)
    old_key_ult = """      if (e.code === 'Space' || e.code === 'ShiftLeft' || e.code === 'ShiftRight' || e.code === 'KeyE' || e.code === 'KeyF') {
        if (state.screen === 'playing') {
          triggerUltimate();
        }
      }"""

    new_key_ult = """      if (e.code === 'Space' || e.code === 'ShiftLeft' || e.code === 'ShiftRight' || e.code === 'KeyE' || e.code === 'KeyF') {
        if (state.screen === 'playing') {
          triggerUltimate();
        }
      }
      if (e.code === 'KeyC' || e.key === 'c' || e.key === 'C') {
        if (state.screen === 'playing') {
          activateSurviveSkill();
        }
      }"""

    if old_key_ult in src:
        src = src.replace(old_key_ult, new_key_ult)
        print("Patched KeyC survive listener successfully!")
    else:
        print("Warning: old_key_ult not matched!")

    with open('js/game.js', 'w', encoding='utf-8') as f:
        f.write(src)

if __name__ == '__main__':
    main()

