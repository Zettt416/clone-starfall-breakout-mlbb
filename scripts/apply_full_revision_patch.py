import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Preload Assets for Ships, Bosses, and Unique Powerups
old_preloads = '''  loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');
  loadAsset('boss_mecha', 'assets/images/boss_mecha_titan.png');
  loadAsset('boss_monster', 'assets/images/boss_alien_leviathan.png');
  loadAsset('boss_humanoid', 'assets/images/boss_humanoid_valkyrie.png');
  loadAsset('boss_alien', 'assets/images/boss_eldritch_eye.png');
  loadAsset('explosion_sheet', 'assets/images/explosion_sheet.png');'''

new_preloads = '''  loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');
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
  loadAsset('powerup_void_needle', 'assets/images/powerup_void_needle.png');'''

assert old_preloads in text, "old_preloads not found"
text = text.replace(old_preloads, new_preloads, 1)
print("1. Added loadAsset preloads!")

# 2. Update BUFF_TYPES
old_buff_types = '''  // Power-up types
  const BUFF_TYPES = {
    RAPID: { id: 'rapid', name: 'RAPID', color: '#ff2a85', symbol: '⚡', duration: 8.0 },
    MULTI: { id: 'multi', name: 'MULTI', color: '#00f3ff', symbol: '✦', duration: 9.0 },
    PIERCE: { id: 'pierce', name: 'PIERCE', color: '#ffd000', symbol: '➤', duration: 7.0 },
    BURST: { id: 'burst', name: 'BURST', color: '#ff7700', symbol: '💥', duration: 8.0 },
    SHIELD: { id: 'shield', name: 'SHIELD', color: '#00f3ff', symbol: '🛡️', duration: 12.0 }
  };'''

new_buff_types = '''  // Power-up types
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
  };'''

assert old_buff_types in text, "old_buff_types not found"
text = text.replace(old_buff_types, new_buff_types, 1)
print("2. Updated BUFF_TYPES!")

# 3. Update SHIPS_CONFIG
old_ships_config = '''  // Starship / Character Roster (Each with a unique survival skill & ultimate)
  const SHIPS_CONFIG = {
    stella_nova: {
      id: 'stella_nova',
      name: 'STELLA NOVA',
      class: 'INTERCEPTOR',
      badgeClass: 'badge-interceptor',
      color: '#00f3ff',
      filter: 'none',
      speed: 320,
      firepowerLabel: 'TWIN CANNON',
      hpLabel: 'STANDARD',
      extraLives: 0,
      surviveName: 'COSMIC SHIELD',
      surviveDesc: 'COSMIC AEGIS SHIELD (3D FORCEFIELD)',
      ultName: 'STELLAR BLASTER',
      ultDesc: 'STELLAR BLASTER BEAM'
    },
    aether_vanguard: {
      id: 'aether_vanguard',
      name: 'AETHER VANGUARD',
      class: 'DREADNOUGHT',
      badgeClass: 'badge-dreadnought',
      color: '#ffd000',
      filter: 'hue-rotate(180deg) saturate(1.4) brightness(1.1)',
      speed: 270,
      firepowerLabel: 'TRIPLE FLAK',
      hpLabel: '+1 EXTRA LIFE',
      extraLives: 1,
      surviveName: 'NANITE MATRIX',
      surviveDesc: 'NANITE PHASE BARRIER (PULSE CLEAR)',
      ultName: 'CLUSTER BARRAGE',
      ultDesc: 'HEAVY CLUSTER BARRAGE'
    },
    chrono_phantom: {
      id: 'chrono_phantom',
      name: 'CHRONO PHANTOM',
      class: 'RECON GHOST',
      badgeClass: 'badge-ghost',
      color: '#b844ff',
      filter: 'hue-rotate(270deg) brightness(1.2) contrast(1.1)',
      speed: 390,
      firepowerLabel: 'NEEDLE PIERCE',
      hpLabel: 'FAST ULT CHARGE',
      extraLives: 0,
      surviveName: 'CHRONO WARP',
      surviveDesc: 'TEMPORAL WARP (70% SLOW-MO)',
      ultName: 'SINGULARITY RIFT',
      ultDesc: 'SINGULARITY VORTEX'
    }
  };'''

new_ships_config = '''  // Starship / Character Roster (Unique Real Arcade Sprites, Dedicated Power-Ups & Skills)
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
  };'''

assert old_ships_config in text, "old_ships_config not found"
text = text.replace(old_ships_config, new_ships_config, 1)
print("3. Updated SHIPS_CONFIG!")

# 4. Update PowerUp.prototype.draw to render custom iconAsset inside orbs
old_pu_draw = '''      // Check if custom AI icon image is loaded
      let iconImg = null;
      if (this.kind === 'HEART') iconImg = assets.images['cyber_heart'];
      else if (this.kind === 'STAR') iconImg = assets.images['stellar_star'];
      else if (this.kind === 'SHIELD') iconImg = assets.images['shield_icon'];
      else if (this.kind === 'RAPID') iconImg = assets.images['powerup_rapid'];
      else if (this.kind === 'MULTI') iconImg = assets.images['powerup_multi'];
      else if (this.kind === 'PIERCE') iconImg = assets.images['powerup_pierce'];
      else if (this.kind === 'BURST') iconImg = assets.images['powerup_burst'];'''

new_pu_draw = '''      // Check if custom AI icon image is loaded
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
      }'''

assert old_pu_draw in text, "old_pu_draw not found"
text = text.replace(old_pu_draw, new_pu_draw, 1)
print("4. Updated PowerUp.prototype.draw!")

# 5. Update PowerUp.prototype.collect
old_pu_collect = '''      } else if (this.kind === 'SHIELD') {
        player.buffs.shield = BUFF_TYPES.SHIELD.duration;
        createFloatingText('COSMIC SHIELD! 🛡️', this.x, this.y - 12, '#00f3ff');
        window.soundFx.playShieldPickup();
      } else {
        const buffKey = this.kind.toLowerCase();
        player.buffs[buffKey] = (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].duration) || 10.0;
        createFloatingText(`${this.kind}!`, this.x, this.y - 10, BUFF_TYPES[this.kind].color);
      }'''

new_pu_collect = '''      } else if (this.kind === 'SHIELD') {
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
      }'''

assert old_pu_collect in text, "old_pu_collect not found"
text = text.replace(old_pu_collect, new_pu_collect, 1)
print("5. Updated PowerUp.prototype.collect!")

# 6. Update rollPowerUpDrop to respect level drop rates and character-specific weapons
old_roll = '''  function rollPowerUpDrop(x, y, meteorType) {
    let dropChance = 0.14;
    if (meteorType === 'star') dropChance = 1.0;
    if (meteorType === 'armored') dropChance = 0.5;
    if (meteorType === 'wall_block') dropChance = 0.1;

    if (Math.random() < dropChance) {
      let kind;
      if (meteorType === 'star') {
        kind = 'STAR';
      } else {
        const roll = Math.random();
        if (roll < 0.22) kind = 'RAPID';
        else if (roll < 0.42) kind = 'MULTI';
        else if (roll < 0.62) kind = 'PIERCE';
        else if (roll < 0.80) kind = 'BURST';
        else if (roll < 0.93) kind = 'SHIELD';
        else kind = 'HEART';
      }
      powerUps.push(new PowerUp(x, y, kind));
    }
  }'''

new_roll = '''  function rollPowerUpDrop(x, y, meteorType) {
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
  }'''

assert old_roll in text, "old_roll not found"
text = text.replace(old_roll, new_roll, 1)
print("6. Updated rollPowerUpDrop!")

# 7. Update updateShipCardUI to switch avatar src
old_avatar_filter = '''    if (shipAvatarImg) shipAvatarImg.style.filter = conf.filter;'''
new_avatar_filter = '''    if (shipAvatarImg) {
      if (conf.avatarSrc) {
        shipAvatarImg.src = conf.avatarSrc;
        shipAvatarImg.style.filter = 'none';
      } else {
        shipAvatarImg.style.filter = conf.filter;
      }
    }'''

assert old_avatar_filter in text, "old_avatar_filter not found"
text = text.replace(old_avatar_filter, new_avatar_filter, 1)
print("7. Updated updateShipCardUI avatar src!")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("ALL PATCHES APPLIED TO js/game.js!")

