import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update updateShipDisplay to set real avatar image
old_ship_display = '''    if (shipNameText) shipNameText.textContent = conf.name;
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
    if (shipAvatarImg) shipAvatarImg.style.filter = conf.filter;'''

new_ship_display = '''    if (shipNameText) shipNameText.textContent = conf.name;
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
    }'''

assert old_ship_display in text, "old_ship_display not found"
text = text.replace(old_ship_display, new_ship_display, 1)
print("Updated shipDisplay avatar logic!")

# 2. Update PowerUp.prototype.draw & collect
old_powerup_draw_icons = '''      // Check if custom AI icon image is loaded
      let iconImg = null;
      if (this.kind === 'HEART') iconImg = assets.images['cyber_heart'];
      else if (this.kind === 'STAR') iconImg = assets.images['stellar_star'];
      else if (this.kind === 'SHIELD') iconImg = assets.images['shield_icon'];
      else if (this.kind === 'RAPID') iconImg = assets.images['powerup_rapid'];
      else if (this.kind === 'MULTI') iconImg = assets.images['powerup_multi'];
      else if (this.kind === 'PIERCE') iconImg = assets.images['powerup_pierce'];
      else if (this.kind === 'BURST') iconImg = assets.images['powerup_burst'];'''

new_powerup_draw_icons = '''      // Check if custom AI icon image is loaded (supports generic and character-specific)
      let iconImg = null;
      if (this.kind === 'HEART') iconImg = assets.images['cyber_heart'];
      else if (this.kind === 'STAR') iconImg = assets.images['stellar_star'];
      else if (this.kind === 'SHIELD') iconImg = assets.images['shield_icon'];
      else if (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].iconAsset) {
        iconImg = assets.images[BUFF_TYPES[this.kind].iconAsset];
      }'''

assert old_powerup_draw_icons in text, "old_powerup_draw_icons not found"
text = text.replace(old_powerup_draw_icons, new_powerup_draw_icons, 1)
print("Updated PowerUp.prototype.draw icons!")

old_powerup_collect = '''      } else if (this.kind === 'SHIELD') {
        player.buffs.shield = BUFF_TYPES.SHIELD.duration;
        createFloatingText('COSMIC SHIELD! 🛡️', this.x, this.y - 12, '#00f3ff');
        window.soundFx.playShieldPickup();
      } else {
        const buffKey = this.kind.toLowerCase();
        player.buffs[buffKey] = (BUFF_TYPES[this.kind] && BUFF_TYPES[this.kind].duration) || 10.0;
        createFloatingText(`${this.kind}!`, this.x, this.y - 10, BUFF_TYPES[this.kind].color);
      }'''

new_powerup_collect = '''      } else if (this.kind === 'SHIELD') {
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

assert old_powerup_collect in text, "old_powerup_collect not found"
text = text.replace(old_powerup_collect, new_powerup_collect, 1)
print("Updated PowerUp.prototype.collect!")

# 3. Update rollPowerUpDrop to use character-specific pools and difficulty rates
old_roll_powerup = '''  function rollPowerUpDrop(x, y, meteorType) {
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

new_roll_powerup = '''  function rollPowerUpDrop(x, y, meteorType) {
    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    let baseDropRate = conf.powerupDropRate || 0.24;

    if (meteorType === 'star') baseDropRate = 1.0;
    else if (meteorType === 'fast_scout') baseDropRate = 0.45;
    else if (meteorType === 'armored') baseDropRate = 0.65;
    else if (meteorType === 'wall_block') baseDropRate = 0.12;

    if (Math.random() < baseDropRate) {
      let kind;
      if (meteorType === 'star') {
        kind = 'STAR';
      } else {
        const roll = Math.random();
        const shipId = state.selectedShip || 'stella_nova';

        // Difficulty weighted survivability vs offensive powerups
        const heartWeight = conf.heartDropWeight || 0.12;
        const shieldWeight = conf.survivalDropWeight || 0.16;

        if (roll < heartWeight) {
          kind = 'HEART';
        } else if (roll < heartWeight + shieldWeight) {
          kind = 'SHIELD';
        } else if (roll < heartWeight + shieldWeight + 0.08) {
          kind = 'STAR';
        } else {
          // Character-Specific Unique Powerups
          const weaponRoll = Math.random();
          if (shipId === 'aether_vanguard') {
            kind = weaponRoll < 0.52 ? 'HEAVY_FLAK' : 'TESLA_COIL';
          } else if (shipId === 'chrono_phantom') {
            kind = weaponRoll < 0.52 ? 'QUANTUM_CLONES' : 'VOID_NEEDLE';
          } else {
            // Stella Nova
            kind = weaponRoll < 0.52 ? 'HYPERDRIVE' : 'PLASMA_SPREAD';
          }
        }
      }
      powerUps.push(new PowerUp(x, y, kind));
    }
  }'''

assert old_roll_powerup in text, "old_roll_powerup not found"
text = text.replace(old_roll_powerup, new_roll_powerup, 1)
print("Updated rollPowerUpDrop with character pools and difficulty scaling!")

# 4. Update Meteor class with fast scout drone and dynamic HP scaling
old_meteor_init = '''      if (type === 'normal') {
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

      this.speed *= state.difficultyMultiplier;'''

new_meteor_init = '''      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const timeScale = 1.0 + Math.min(2.0, state.survivalTime * 0.005);
      const hpMult = (conf.meteorHpMult || 1.0) * timeScale;

      this.time = 0;
      this.isDrone = (type === 'fast_scout');

      if (type === 'fast_scout') {
        // High-Speed Robotic Kamikaze Scout Drone (2.5x speed, weaves in sine wave)
        this.radius = 16;
        this.hp = Math.max(1, Math.round(2 * hpMult));
        this.maxHp = this.hp;
        this.speed = (270 + Math.random() * 60) * (conf.meteorSpeedMult || 1.0);
        this.vy = 0;
        this.score = 80;
        this.color = '#ff0055';
      } else if (type === 'normal') {
        this.radius = 18;
        this.hp = Math.max(1, Math.round(1 * hpMult));
        this.maxHp = this.hp;
        this.speed = (150 + Math.random() * 70) * (conf.meteorSpeedMult || 1.0);
        this.vy = (Math.random() - 0.5) * 30;
        this.score = 15;
        this.color = '#7c6f9e';
      } else if (type === 'medium') {
        this.radius = 28;
        this.hp = Math.max(2, Math.round(3 * hpMult));
        this.maxHp = this.hp;
        this.speed = (110 + Math.random() * 45) * (conf.meteorSpeedMult || 1.0);
        this.vy = (Math.random() - 0.5) * 25;
        this.score = 40;
        this.color = '#5d4e80';
      } else if (type === 'armored') {
        this.radius = 36;
        this.hp = Math.max(4, Math.round(7 * hpMult));
        this.maxHp = this.hp;
        this.speed = (80 + Math.random() * 30) * (conf.meteorSpeedMult || 1.0);
        this.vy = 0;
        this.score = 100;
        this.color = '#a83258';
      } else if (type === 'star') {
        this.radius = 20;
        this.hp = Math.max(1, Math.round(2 * hpMult));
        this.maxHp = this.hp;
        this.speed = 170 * (conf.meteorSpeedMult || 1.0);
        this.vy = (Math.random() - 0.5) * 40;
        this.score = 60;
        this.color = '#ffd000';
      } else if (type === 'wall_block') {
        this.radius = 24;
        this.hp = Math.max(3, Math.round(5 * hpMult));
        this.maxHp = this.hp;
        this.speed = 75 * (conf.meteorSpeedMult || 1.0);
        this.vy = 0;
        this.score = 50;
        this.color = '#452b69';
      }

      this.speed *= state.difficultyMultiplier;'''

assert old_meteor_init in text, "old_meteor_init not found"
text = text.replace(old_meteor_init, new_meteor_init, 1)
print("Updated Meteor.constructor with fast_scout and dynamic HP scaling!")

# 5. Update Meteor.update for sinusoidal wave weaving
old_meteor_update = '''    update(dt) {
      this.x -= this.speed * dt;
      this.y += this.vy * dt;
      this.rotation += this.rotSpeed * dt;

      if (this.x < -60) {
        this.toRemove = true;
      }
    }'''

new_meteor_update = '''    update(dt) {
      this.time += dt;
      this.x -= this.speed * dt;
      this.y += this.vy * dt;
      if (this.isDrone) {
        this.y += Math.sin(this.time * 6.5) * 2.2;
      }
      this.rotation += this.rotSpeed * dt;

      if (this.x < -60) {
        this.toRemove = true;
      }
    }'''

assert old_meteor_update in text, "old_meteor_update not found"
text = text.replace(old_meteor_update, new_meteor_update, 1)

# 6. Update Meteor.draw to draw fast scout drone
old_meteor_draw = '''      if (this.type === 'star') {
        drawPolygon(ctx, 0, 0, this.radius, 5, 0.45);
      } else if (this.type === 'wall_block') {'''

new_meteor_draw = '''      if (this.isDrone) {
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
        drawPolygon(ctx, 0, 0, this.radius, 5, 0.45);
      } else if (this.type === 'wall_block') {'''

assert old_meteor_draw in text, "old_meteor_draw not found"
text = text.replace(old_meteor_draw, new_meteor_draw, 1)

# 7. Update updateSpawners for fast_scout drones
old_spawner_roll = '''      if (roll < 0.08) {
        meteors.push(new Meteor(spawnX, spawnY, 'star'));
      } else if (roll < 0.28) {
        meteors.push(new Meteor(spawnX, spawnY, 'armored'));
      } else if (roll < 0.60) {
        meteors.push(new Meteor(spawnX, spawnY, 'medium'));
      } else {
        meteors.push(new Meteor(spawnX, spawnY, 'normal'));
      }'''

new_spawner_roll = '''      const fastRate = (conf.fastEnemySpawnRate || 0.12) * Math.min(2.0, 1.0 + state.survivalTime * 0.007);
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
      }'''

assert old_spawner_roll in text, "old_spawner_roll not found"
text = text.replace(old_spawner_roll, new_spawner_roll, 1)
print("Updated Spawner roll for fast_scouts!")

# 8. Dynamic Parallax Background per Stage / Level in updateAtmosphereColors & render()
old_atm_target = '''    } else {
      state.bgTarget = { r: 10, g: 8, b: 20 };
    }'''

new_atm_target = '''    } else {
      // Dynamic Stage Atmosphere per Level / Difficulty
      if (state.difficulty === 'easy') {
        state.bgTarget = { r: 6, g: 16, b: 34 };   // Level 1: Deep Azure Void
      } else if (state.difficulty === 'normal') {
        state.bgTarget = { r: 18, g: 8, b: 30 };   // Level 2: Royal Nebula Purple
      } else if (state.difficulty === 'hard') {
        state.bgTarget = { r: 34, g: 8, b: 14 };   // Level 3: Crimson Supernova Abyss
      } else {
        state.bgTarget = { r: 6, g: 2, b: 14 };    // Level 4: Obsidian Event Horizon
      }
    }'''

assert old_atm_target in text, "old_atm_target not found"
text = text.replace(old_atm_target, new_atm_target, 1)

# Add drawStageParallaxBackdrop function
stage_backdrop_func = '''  // --- Dynamic Multi-Layer Parallax Stage Environments per Level ---
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
      // Glowing Nebular Cloud Clusters
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
      // --- Level 3 (HARD): Crimson Supernova Core & Retro Warp Grid ---
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
'''

if 'drawStageParallaxBackdrop' not in text:
    text = text.replace('  function drawBossAtmosphereBackdrop(ctx) {', stage_backdrop_func + '\n  function drawBossAtmosphereBackdrop(ctx) {', 1)
    print("Added drawStageParallaxBackdrop!")

# Update render() to call drawStageParallaxBackdrop(ctx)
old_render_backdrop = '''    // Celestial Boss Arena Backdrop (Eclipse / Ion Storm)
    if (state.activeBoss || state.bossWarningActive) {
      drawBossAtmosphereBackdrop(ctx);
    }'''

new_render_backdrop = '''    // Dynamic Multi-Layer Parallax Stage Backdrop per Level
    drawStageParallaxBackdrop(ctx);

    // Celestial Boss Arena Backdrop (Eclipse / Ion Storm)
    if (state.activeBoss || state.bossWarningActive) {
      drawBossAtmosphereBackdrop(ctx);
    }'''

assert old_render_backdrop in text, "old_render_backdrop not found"
text = text.replace(old_render_backdrop, new_render_backdrop, 1)

# 9. Update drawBigbossShip to map unique Big Boss models
old_bigboss_sprite = '''      const spriteKey = 'boss_' + (this.archetype || 'mecha');
      const sprite = assets.images[spriteKey] || assets.images.bigboss;'''

new_bigboss_sprite = '''      // Select Dedicated Unique Big Boss Sprite Assets
      let spriteKey = 'boss_' + (this.archetype || 'mecha');
      const bName = this.name || '';

      if (bName.includes('Annihilator') || bName.includes('Dreadnought') || bName.includes('Apex') || bName.includes('Flagship') || bName.includes('Warlord') || bName.includes('Carrier')) {
        spriteKey = 'boss_crimson_annihilator';
      } else if (this.archetype === 'monster' || bName.includes('Singularity') || bName.includes('Leviathan') || bName.includes('Maw') || bName.includes('Goliath')) {
        spriteKey = 'boss_void_singularity';
      } else if (this.archetype === 'humanoid' || bName.includes('Astraea') || bName.includes('Archon') || bName.includes('Ex-Machina') || bName.includes('Zephyr')) {
        spriteKey = 'boss_astraea_archon';
      }

      const sprite = assets.images[spriteKey] || assets.images['boss_' + (this.archetype || 'mecha')] || assets.images.bigboss;'''

assert old_bigboss_sprite in text, "old_bigboss_sprite not found"
text = text.replace(old_bigboss_sprite, new_bigboss_sprite, 1)
print("Updated drawBigbossShip with unique big boss model mapping!")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully applied game complete revision to js/game.js!")

