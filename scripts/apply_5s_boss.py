import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update initial state nextBossCheckpoint
old_state = 'nextBossCheckpoint: 60,'
new_state = 'nextBossCheckpoint: 5,'
assert old_state in content, 'old_state not found'
content = content.replace(old_state, new_state, 1)

# 2. Update Boss constructor specialTimer
old_timer = 'this.specialTimer = (isBig ? 3.8 : 4.5) * conf.bossShootIntervalMult;'
new_timer = 'this.specialTimer = (isBig ? 1.5 : 1.8) * conf.bossShootIntervalMult;'
assert old_timer in content, 'old_timer not found'
content = content.replace(old_timer, new_timer, 1)

# 3. Update Boss.destroy nextBossCheckpoint
old_destroy = 'state.nextBossCheckpoint = Math.floor(state.survivalTime / 60) * 60 + 60;'
new_destroy = 'state.nextBossCheckpoint = state.survivalTime + 5;'
assert old_destroy in content, 'old_destroy not found'
content = content.replace(old_destroy, new_destroy, 1)

# 4. Update getNextBossConfig for archetype interleaving
old_get_boss = """    if (tierBosses.length === 0) return window.BOSS_CATALOG[0];

    const index = (cycle - 1) % tierBosses.length;
    return tierBosses[index];"""

new_get_boss = """    if (tierBosses.length === 0) return window.BOSS_CATALOG[0];

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
    return tierBosses[index];"""

assert old_get_boss in content, 'old_get_boss not found'
content = content.replace(old_get_boss, new_get_boss, 1)

# 5. Update triggerBossEncounter warningTimer and avatar
old_warn = """    state.bossWarningActive = true;
    state.warningTimer = 2.4;
    state.pendingBossConfig = bossConfig;

    if (bossWarningBanner) {
      bossWarningBanner.classList.remove('hidden');
      const titleEl = bossWarningBanner.querySelector('.warning-title');
      if (titleEl) titleEl.textContent = t.bossWarningTitle;
    }
    if (bossWarningAvatar) {
      bossWarningAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
      bossWarningAvatar.style.borderColor = bossConfig.color || '#ff0055';
    }"""

new_warn = """    state.bossWarningActive = true;
    state.warningTimer = 1.0;
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
    }"""

assert old_warn in content, 'old_warn not found'
content = content.replace(old_warn, new_warn, 1)

# 6. Update startGame nextBossCheckpoint
old_start = 'state.nextBossCheckpoint = 60;'
new_start = 'state.nextBossCheckpoint = 5;'
assert old_start in content, 'old_start not found'
content = content.replace(old_start, new_start, 1)

# 7. Add KeyB (spawn next boss) and KeyK (kill boss) test hotkeys
old_keys = """      if (e.code === 'KeyC' || e.key === 'c' || e.key === 'C') {
        if (state.screen === 'playing') {
          activateSurviveSkill();
        }
      }"""

new_keys = """      if (e.code === 'KeyC' || e.key === 'c' || e.key === 'C') {
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
      }"""

assert old_keys in content, 'old_keys not found'
content = content.replace(old_keys, new_keys, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully applied 5s boss updates to js/game.js!')

