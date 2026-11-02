# -*- coding: utf-8 -*-

def update_game_js():
    with open('js/game.js', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update Boss constructor properties
    old_boss_props = """      // Big boss telegraphed railgun laser
      this.isChargingLaser = false;
      this.laserChargeTimer = 0;
      this.isFiringLaser = false;
      this.laserFireTimer = 0;
      this.laserTargetY = CANVAS_HEIGHT / 2;

      this.toRemove = false;"""

    new_boss_props = """      // Universal Telegraphed Signature Skill System
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

      this.toRemove = false;"""

    if old_boss_props in src:
        src = src.replace(old_boss_props, new_boss_props)
        print("Updated Boss constructor skill properties")

    # 2. Update Boss.update(dt) skill wind-up and firing handling
    old_laser_update = """      // Big Boss Railgun Laser Handling
      if (this.type === 'bigboss') {
        if (this.isChargingLaser) {
          this.y += (this.laserTargetY - this.y) * dt * 4;
          this.laserChargeTimer -= dt;
          if (this.laserChargeTimer <= 0) {
            this.isChargingLaser = false;
            this.isFiringLaser = true;
            this.laserFireTimer = 0.75;
            this.laserTargetY = this.y;
            state.screenShake = 14;
            window.soundFx.playBossShoot();
          }
        } else if (this.isFiringLaser) {
          this.laserFireTimer -= dt;
          this.laserTargetY = this.y;
          if (player.invulnerableTimer <= 0 && !state.isUltActive) {
            if (player.x < this.x && Math.abs(player.y - this.y) < 26 + player.height / 2) {
              playerTakeDamage();
            }
          }
          if (this.laserFireTimer <= 0) {
            this.isFiringLaser = false;
          }
        }
      }"""

    new_laser_update = """      // Signature Skill Wind-up / Casting Telegraph Handling
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
      }"""

    if old_laser_update in src:
        src = src.replace(old_laser_update, new_laser_update)
        print("Updated Boss.update skill wind-up and firing logic")

    # 3. Update specialTimer trigger in Boss.update(dt)
    old_special_timer = """        if (this.specialTimer <= 0) {
          if (this.type === 'miniboss') {
            this.spawnEscortMeteors();
            this.specialTimer = 5.5 * conf.bossShootIntervalMult;
          } else {
            this.startRailgunTelegraph();
            this.specialTimer = 6.0 * conf.bossShootIntervalMult;
          }
        }"""

    new_special_timer = """        if (this.specialTimer <= 0) {
          this.startSkillTelegraph();
          this.specialTimer = (isBig ? 6.2 : 5.4) * conf.bossShootIntervalMult;
        }"""

    if old_special_timer in src:
        src = src.replace(old_special_timer, new_special_timer)
        print("Updated Boss.update specialTimer trigger to call startSkillTelegraph")

    # 4. Add startSkillTelegraph and executeSkillRelease methods
    old_start_railgun = """    startRailgunTelegraph() {
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      this.isChargingLaser = true;
      this.laserChargeTimer = conf.touhouDanmaku ? 0.85 : state.difficulty === 'hard' ? 1.0 : state.difficulty === 'easy' ? 1.4 : 1.2;
      this.laserTargetY = Math.max(40, Math.min(CANVAS_HEIGHT - 40, player.y));
      window.soundFx.playBossWarning();
      createFloatingText('⚡ RAILGUN CHARGING! ⚡', CANVAS_WIDTH / 2, 70, '#ff0055');
    }"""

    new_skill_methods = """    startSkillTelegraph() {
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      this.isCastingSkill = true;
      this.castSkillDuration = conf.touhouDanmaku ? 0.95 : state.difficulty === 'hard' ? 1.1 : state.difficulty === 'easy' ? 1.4 : 1.25;
      this.castSkillTimer = this.castSkillDuration;
      this.skillTargetY = Math.max(45, Math.min(CANVAS_HEIGHT - 45, player ? player.y : CANVAS_HEIGHT / 2));
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
    }"""

    if old_start_railgun in src:
        src = src.replace(old_start_railgun, new_skill_methods)
        print("Replaced startRailgunTelegraph with startSkillTelegraph and executeSkillRelease")

    # 5. Update Boss.draw(ctx) to call drawSkillTelegraph and lance beam
    old_draw_boss_top = """    draw(ctx) {
      ctx.save();

      // Railgun charging / laser
      if (this.type === 'bigboss') {
        if (this.isChargingLaser) {
          const chargePct = 1 - (this.laserChargeTimer / 1.6);
          const muzzleX = (this.currentX || this.x) - this.width * 0.48;
          const beamY = this.y;

          ctx.save();
          const sightGrad = ctx.createLinearGradient(muzzleX, beamY, 0, beamY);
          sightGrad.addColorStop(0, `rgba(255, 0, 85, ${0.7 + chargePct * 0.3})`);
          sightGrad.addColorStop(1, 'rgba(255, 0, 85, 0.15)');
          ctx.strokeStyle = sightGrad;
          ctx.lineWidth = 1.5 + chargePct * 2.5;
          ctx.setLineDash([12, 6]);
          ctx.lineDashOffset = -(Date.now() * 0.05);
          ctx.beginPath();
          ctx.moveTo(muzzleX, beamY);
          ctx.lineTo(0, beamY);
          ctx.stroke();
          ctx.setLineDash([]);

          const coreR = 8 + chargePct * 18;
          const chargeGrad = ctx.createRadialGradient(muzzleX, beamY, 2, muzzleX, beamY, coreR);
          chargeGrad.addColorStop(0, '#ffffff');
          chargeGrad.addColorStop(0.35, '#00f3ff');
          chargeGrad.addColorStop(0.7, '#ff0055');
          chargeGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = chargeGrad;
          ctx.beginPath();
          ctx.arc(muzzleX, beamY, coreR, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        } else if (this.isFiringLaser) {
          drawBossHyperRailgunBeam(ctx, this);
        }
      }"""

    new_draw_boss_top = """    draw(ctx) {
      ctx.save();

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
      }"""

    if old_draw_boss_top in src:
        src = src.replace(old_draw_boss_top, new_draw_boss_top)
        print("Updated Boss.draw to call drawSkillTelegraph and drawValkyrieCelestialLanceBeam")

    # 6. Add drawSkillTelegraph method to Boss class
    telegraph_draw_code = """
    drawSkillTelegraph(ctx) {
      const chargePct = Math.max(0, Math.min(1, 1 - (this.castSkillTimer / this.castSkillDuration)));
      const halfW = this.width / 2;
      const halfH = this.height / 2;
      const muzzleX = (this.currentX || this.x) - halfW * 0.48;
      const beamY = this.y;

      ctx.save();

      if (this.archetype === 'humanoid') {
        // --- 1. Valkyrie Sacred Celestial Summoning Glyph / Magic Rune Circle ---
        const glyphR = 48 + chargePct * 30;
        const glyphAngle = Date.now() * 0.0025;
        const col = this.color || '#ff00aa';

        ctx.save();
        ctx.translate(this.currentX || this.x, this.y);

        // Outer Runic Circle
        ctx.strokeStyle = col;
        ctx.lineWidth = 2 + chargePct * 1.5;
        ctx.shadowColor = col;
        ctx.shadowBlur = 14;
        ctx.beginPath();
        ctx.arc(0, 0, glyphR, 0, Math.PI * 2);
        ctx.stroke();

        // 8-Pointed Star / Octagram Spokes
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        for (let i = 0; i < 8; i++) {
          const a = glyphAngle + (i * Math.PI * 2 / 8);
          ctx.moveTo(Math.cos(a) * (glyphR * 0.35), Math.sin(a) * (glyphR * 0.35));
          ctx.lineTo(Math.cos(a) * glyphR, Math.sin(a) * glyphR);
        }
        ctx.stroke();

        // Inner Rotating Diamond Glyph
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        for (let i = 0; i < 4; i++) {
          const a = -glyphAngle * 1.5 + (i * Math.PI / 2);
          const px = Math.cos(a) * (glyphR * 0.65);
          const py = Math.sin(a) * (glyphR * 0.65);
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.stroke();
        ctx.restore();

        // --- 2. Star-Lance Tip Blinding Supernova Flare ---
        const lanceTipX = (this.currentX || this.x) - halfW * 0.46;
        const lanceTipY = this.y - halfH * 0.06;
        const flareR = 8 + chargePct * 22;

        const lanceGrad = ctx.createRadialGradient(lanceTipX, lanceTipY, 2, lanceTipX, lanceTipY, flareR);
        lanceGrad.addColorStop(0, '#ffffff');
        lanceGrad.addColorStop(0.35, '#ffd000');
        lanceGrad.addColorStop(0.7, col);
        lanceGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = lanceGrad;
        ctx.beginPath();
        ctx.arc(lanceTipX, lanceTipY, flareR, 0, Math.PI * 2);
        ctx.fill();

        // Star Lens Flare Cross
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(lanceTipX - flareR * 1.8, lanceTipY);
        ctx.lineTo(lanceTipX + flareR * 1.8, lanceTipY);
        ctx.moveTo(lanceTipX, lanceTipY - flareR * 1.8);
        ctx.lineTo(lanceTipX, lanceTipY + flareR * 1.8);
        ctx.stroke();

        // Aiming Starlight Beam Sights to player Y
        ctx.strokeStyle = `rgba(255, 215, 0, ${0.4 + chargePct * 0.5})`;
        ctx.lineWidth = 2;
        ctx.setLineDash([14, 6]);
        ctx.lineDashOffset = -(Date.now() * 0.06);
        ctx.beginPath();
        ctx.moveTo(lanceTipX, lanceTipY);
        ctx.lineTo(0, this.skillTargetY);
        ctx.stroke();
        ctx.setLineDash([]);

      } else if (this.archetype === 'mecha') {
        // --- 2. Mecha Titan: Twin Shoulder Railgun Lasers & Overdrive Reactor ---
        const col = this.color || '#ffd000';
        const topCannonY = this.y - halfH * 0.35;
        const botCannonY = this.y + halfH * 0.35;
        const cannonX = (this.currentX || this.x) - halfW * 0.44;

        // Twin Aiming Lasers
        ctx.strokeStyle = `rgba(255, 0, 85, ${0.6 + chargePct * 0.4})`;
        ctx.lineWidth = 1.8 + chargePct * 2;
        ctx.setLineDash([12, 6]);
        ctx.lineDashOffset = -(Date.now() * 0.05);
        ctx.beginPath();
        ctx.moveTo(cannonX, topCannonY);
        ctx.lineTo(0, this.skillTargetY);
        ctx.moveTo(cannonX, botCannonY);
        ctx.lineTo(0, this.skillTargetY);
        ctx.stroke();
        ctx.setLineDash([]);

        // Twin Cannon Muzzle Plasma Charge Orbs
        const muzzleR = 7 + chargePct * 16;
        [topCannonY, botCannonY].forEach(cy => {
          const mGrad = ctx.createRadialGradient(cannonX, cy, 2, cannonX, cy, muzzleR);
          mGrad.addColorStop(0, '#ffffff');
          mGrad.addColorStop(0.4, '#00f3ff');
          mGrad.addColorStop(0.8, col);
          mGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = mGrad;
          ctx.beginPath();
          ctx.arc(cannonX, cy, muzzleR, 0, Math.PI * 2);
          ctx.fill();
        });

        // Chest Overdrive Reactor Core Flare
        const chestX = (this.currentX || this.x) - halfW * 0.08;
        const chestY = this.y;
        const coreR = 12 + chargePct * 24;
        const coreGrad = ctx.createRadialGradient(chestX, chestY, 2, chestX, chestY, coreR);
        coreGrad.addColorStop(0, '#ffffff');
        coreGrad.addColorStop(0.3, '#00f3ff');
        coreGrad.addColorStop(0.7, '#ff0055');
        coreGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = coreGrad;
        ctx.beginPath();
        ctx.arc(chestX, chestY, coreR, 0, Math.PI * 2);
        ctx.fill();

      } else if (this.archetype === 'alien') {
        // --- 3. Alien Horror: Cyclopean Eye Dilation & Sonar Waves ---
        const eyeX = (this.currentX || this.x) - halfW * 0.25;
        const eyeY = this.y - halfH * 0.08;
        const col = this.color || '#b844ff';

        for (let w = 1; w <= 3; w++) {
          const ringR = ((Date.now() * 0.08 + w * 28) % 90) + chargePct * 20;
          ctx.strokeStyle = col;
          ctx.lineWidth = 2.5 * (1 - ringR / 110);
          ctx.globalAlpha = Math.max(0, 1 - ringR / 110);
          ctx.beginPath();
          ctx.arc(eyeX, eyeY, ringR, 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.globalAlpha = 1.0;

      } else {
        // --- 4. Spaceship & Monster: Aiming Lasers & Core Glow ---
        const col = this.color || '#00f3ff';
        ctx.strokeStyle = col;
        ctx.lineWidth = 1.8 + chargePct * 2;
        ctx.setLineDash([12, 6]);
        ctx.lineDashOffset = -(Date.now() * 0.05);
        ctx.beginPath();
        ctx.moveTo(muzzleX, beamY);
        ctx.lineTo(0, this.skillTargetY);
        ctx.stroke();
        ctx.setLineDash([]);

        const coreR = 8 + chargePct * 18;
        const cGrad = ctx.createRadialGradient(muzzleX, beamY, 2, muzzleX, beamY, coreR);
        cGrad.addColorStop(0, '#ffffff');
        cGrad.addColorStop(0.4, col);
        cGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = cGrad;
        ctx.beginPath();
        ctx.arc(muzzleX, beamY, coreR, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }
"""

    if 'drawSkillTelegraph(ctx)' not in src:
        src = src.replace('    drawOrganicAppendages(ctx) {', telegraph_draw_code + '\n    drawOrganicAppendages(ctx) {')
        print("Added drawSkillTelegraph to Boss class")

    # 7. Add drawValkyrieCelestialLanceBeam function
    lance_func = """
  // --- Radiant Valkyrie Celestial Lance of Longinus Beam ---
  function drawValkyrieCelestialLanceBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.46;
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
"""

    if 'function drawValkyrieCelestialLanceBeam' not in src:
        src = src.replace('  // --- Colossal Boss Hyper-Railgun Laser Beam', lance_func + '\n  // --- Colossal Boss Hyper-Railgun Laser Beam')
        print("Added drawValkyrieCelestialLanceBeam function")

    # 8. Add preview views ?view=valkyriecharge and ?view=mechacharge
    old_preview = "      } else if (viewParam === 'bossvalkyrie') {"
    new_preview = """      } else if (viewParam === 'valkyriecharge') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 16, name: 'Valkyrie Prime', title: 'Astral Cyber-Valkyrie', isBig: true, archetype: 'humanoid', color: '#ff00aa', baseHp: 220, attack: 'curtain_fan' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
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
        testBoss.isCastingSkill = true;
        testBoss.castSkillDuration = 10.0;
        testBoss.castSkillTimer = 5.0;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bossvalkyrie') {"""

    if old_preview in src and 'valkyriecharge' not in src:
        src = src.replace(old_preview, new_preview)
        print("Added valkyriecharge and mechacharge test view parameters")

    with open('js/game.js', 'w', encoding='utf-8') as f:
        f.write(src)

if __name__ == '__main__':
    update_game_js()
    print("All skill telegraph updates finished!")

