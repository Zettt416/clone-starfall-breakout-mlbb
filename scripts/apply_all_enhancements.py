# -*- coding: utf-8 -*-
import re

def main():
    with open('js/game.js', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update showBossBar
    old_show_boss = """  function showBossBar(title) {
    if (bossBarContainer) bossBarContainer.classList.remove('hidden');
    if (bossName) bossName.textContent = title;
    if (bossBarAvatar) {
      const isBig = state.activeBoss && state.activeBoss.type === 'bigboss';
      bossBarAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
    }
    updateBossHpBar(1, 1);
  }"""

    new_show_boss = """  function showBossBar(boss) {
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
      const isBig = isObj ? (boss.type === 'bigboss') : (state.activeBoss && state.activeBoss.type === 'bigboss');
      bossBarAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
      if (isObj && boss.color) bossBarAvatar.style.borderColor = boss.color;
    }
    updateBossHpBar(isObj ? boss.hp : 1, isObj ? boss.maxHp : 1);
  }"""

    if old_show_boss in src:
        src = src.replace(old_show_boss, new_show_boss)
        print("Updated showBossBar")
    else:
        print("Warning: old_show_boss not found!")

    # 2. Player.draw filter application
    old_player_draw = """      // 2. Starfighter Hull (16-Bit Pixel Art PNG or Procedural Fallback)
      if (assets.images['player_ship'] && assets.images['player_ship'].complete && assets.images['player_ship'].naturalWidth > 0) {
        const shipImg = assets.images['player_ship'];
        const targetW = 62;
        const nw = shipImg.naturalWidth || shipImg.width;
        const nh = shipImg.naturalHeight || shipImg.height;
        const targetH = targetW * (nh / nw);
        ctx.drawImage(shipImg, -targetW / 2 + 2, -targetH / 2, targetW, targetH);
      } else {"""

    new_player_draw = """      // 2. Starfighter Hull (16-Bit Pixel Art PNG or Procedural Fallback)
      const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;
      if (assets.images['player_ship'] && assets.images['player_ship'].complete && assets.images['player_ship'].naturalWidth > 0) {
        const shipImg = assets.images['player_ship'];
        const targetW = 62;
        const nw = shipImg.naturalWidth || shipImg.width;
        const nh = shipImg.naturalHeight || shipImg.height;
        const targetH = targetW * (nh / nw);
        ctx.save();
        if (shipConf.filter && shipConf.filter !== 'none') {
          ctx.filter = shipConf.filter;
        }
        ctx.drawImage(shipImg, -targetW / 2 + 2, -targetH / 2, targetW, targetH);
        ctx.restore();
      } else {"""

    if old_player_draw in src:
        src = src.replace(old_player_draw, new_player_draw)
        print("Updated Player.draw filter")
    else:
        print("Warning: old_player_draw not found!")

    # 3. Boss Class Replacement
    boss_start_token = "  class Boss {"
    boss_end_token = "  // --- Ultimate Mechanism ---"
    start_pos = src.find(boss_start_token)
    end_pos = src.find(boss_end_token)

    if start_pos != -1 and end_pos != -1:
        new_boss_block = """  class Boss {
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
      this.cycle = cycle;
      const isBig = (this.type === 'bigboss');

      // Native sprite proportions
      this.width = isBig ? 190 : 175;
      this.height = isBig ? 182 : 91;
      this.x = CANVAS_WIDTH + 100;
      this.y = CANVAS_HEIGHT / 2;
      this.prevY = this.y;
      this.targetX = CANVAS_WIDTH - (isBig ? 160 : 130);
      this.currentX = this.x;
      this.tilt = 0;

      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      const baseHp = (bossData.baseHp || (isBig ? 180 : 70)) + (cycle - 1) * (isBig ? 45 : 25);
      this.maxHp = Math.floor(baseHp * conf.bossHpMult);
      this.hp = this.maxHp;

      this.time = 0;
      this.flashTimer = 0;
      this.shootTimer = 1.0 * conf.bossShootIntervalMult;
      this.specialTimer = (isBig ? 3.8 : 4.5) * conf.bossShootIntervalMult;

      // Big boss telegraphed railgun laser
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

    update(dt) {
      this.time += dt;
      this.prevY = this.y;
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

      // Smooth entry glide
      if (this.x > this.targetX) {
        this.x -= 140 * dt;
        if (this.x < this.targetX) this.x = this.targetX;
      }

      // Natural Multi-Harmonic Organic Motion
      const isBig = (this.type === 'bigboss');
      const waveSpeed = isBig ? 1.25 : 1.7;
      const yWave = Math.sin(this.time * waveSpeed) * (isBig ? 70 : 92)
                  + Math.sin(this.time * waveSpeed * 2.1) * 22
                  + Math.cos(this.time * 0.85) * 12;

      // Gentle organic horizontal breathing drift
      const xDrift = Math.sin(this.time * 1.3) * (isBig ? 12 : 18);
      this.currentX = this.x + xDrift;

      // Vertical Steering & Natural Banking
      if (!this.isChargingLaser && !this.isFiringLaser) {
        const playerTrackingOffset = player ? (player.y - CANVAS_HEIGHT / 2) * 0.28 : 0;
        const targetY = (CANVAS_HEIGHT / 2) + yWave + playerTrackingOffset;
        const clampedY = Math.max(this.height * 0.55, Math.min(CANVAS_HEIGHT - this.height * 0.55, targetY));
        this.y += (clampedY - this.y) * dt * (isBig ? 2.2 : 2.8);

        // Aerodynamic Banking / Tilt based on motion velocity
        const vy = (this.y - this.prevY) / Math.max(0.001, dt);
        const targetTilt = Math.max(-0.2, Math.min(0.2, (vy / 420) * 0.35));
        this.tilt += (targetTilt - this.tilt) * dt * 7;
      } else {
        this.tilt *= 0.92;
      }

      if (this.flashTimer > 0) {
        this.flashTimer -= dt;
      }

      // Big Boss Railgun Laser Handling
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
      }

      // Attack Timers (fire after entering arena)
      if (this.x <= this.targetX + 15 && !this.isChargingLaser && !this.isFiringLaser) {
        this.shootTimer -= dt;
        this.specialTimer -= dt;

        if (this.shootTimer <= 0) {
          if (this.type === 'miniboss') {
            this.shootMinibossPlasma();
            this.shootTimer = 1.4 * conf.bossShootIntervalMult;
          } else {
            this.shootBigbossSpread();
            this.shootTimer = 2.0 * conf.bossShootIntervalMult;
          }
        }

        if (this.specialTimer <= 0) {
          if (this.type === 'miniboss') {
            this.spawnEscortMeteors();
            this.specialTimer = 5.5 * conf.bossShootIntervalMult;
          } else {
            this.startRailgunTelegraph();
            this.specialTimer = 6.0 * conf.bossShootIntervalMult;
          }
        }
      }

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

    startRailgunTelegraph() {
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
      this.isChargingLaser = true;
      this.laserChargeTimer = conf.touhouDanmaku ? 0.85 : state.difficulty === 'hard' ? 1.0 : state.difficulty === 'easy' ? 1.4 : 1.2;
      this.laserTargetY = Math.max(40, Math.min(CANVAS_HEIGHT - 40, player.y));
      window.soundFx.playBossWarning();
      createFloatingText('⚡ RAILGUN CHARGING! ⚡', CANVAS_WIDTH / 2, 70, '#ff0055');
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

    drawOrganicAppendages(ctx) {
      const isBig = (this.type === 'bigboss');
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      if (!isBig) {
        // Alien Void Leviathan: 4 Animated Undulating Bioluminescent Tendrils / Tentacles
        const tendrilCount = 4;
        const rootX = halfW * 0.65;
        const segmentCount = 6;
        const segLen = 14;

        ctx.save();
        ctx.lineWidth = 3.5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        for (let t = 0; t < tendrilCount; t++) {
          const rootY = -halfH * 0.4 + (t / (tendrilCount - 1)) * (halfH * 0.8);
          const phaseOffset = t * 1.35;
          const tendrilGrad = ctx.createLinearGradient(rootX, rootY, rootX + 90, rootY);
          tendrilGrad.addColorStop(0, this.color || '#00f3ff');
          tendrilGrad.addColorStop(0.6, '#9d4edd');
          tendrilGrad.addColorStop(1, 'transparent');
          ctx.strokeStyle = tendrilGrad;

          ctx.beginPath();
          ctx.moveTo(rootX, rootY);
          let cx = rootX;
          let cy = rootY;
          for (let s = 1; s <= segmentCount; s++) {
            const wave = Math.sin(this.time * 5.2 + phaseOffset + s * 0.75) * (8 + s * 2.5);
            cx += segLen;
            cy += wave * 0.35;
            ctx.lineTo(cx, cy);
          }
          ctx.stroke();

          // Small bio-luminescent orb at tip
          ctx.fillStyle = '#00f3ff';
          ctx.beginPath();
          ctx.arc(cx, cy, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      } else {
        // Celestial Mecha Titan: Twin Pulsating Plasma Engine Thrusters
        const thrusterCount = 3;
        const rootX = halfW * 0.8;
        ctx.save();
        for (let i = 0; i < thrusterCount; i++) {
          const thrusterY = -halfH * 0.45 + i * (halfH * 0.45);
          const flameLength = 26 + Math.sin(this.time * 18 + i * 2) * 12 + Math.random() * 8;
          const flameGrad = ctx.createLinearGradient(rootX, thrusterY, rootX + flameLength, thrusterY);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.3, '#ffd000');
          flameGrad.addColorStop(0.7, '#ff0055');
          flameGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(rootX, thrusterY - 7);
          ctx.lineTo(rootX + flameLength, thrusterY);
          ctx.lineTo(rootX, thrusterY + 7);
          ctx.closePath();
          ctx.fill();
        }
        ctx.restore();
      }
    }

    draw(ctx) {
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
      }

      // Draw Boss with dynamic tilt and natural breathing pulse
      ctx.translate(this.currentX || this.x, this.y);
      ctx.rotate(this.tilt || 0);

      const breathFreq = this.type === 'bigboss' ? 2.2 : 3.4;
      const breathMag = this.type === 'bigboss' ? 0.025 : 0.04;
      const pulseX = 1 + Math.sin(this.time * breathFreq) * breathMag;
      const pulseY = 1 - Math.sin(this.time * breathFreq) * (breathMag * 0.8);
      ctx.scale(pulseX, pulseY);

      this.drawOrganicAppendages(ctx);

      if (this.type === 'miniboss') {
        this.drawMinibossShip(ctx);
      } else {
        this.drawBigbossShip(ctx);
      }

      ctx.restore();
    }

    drawMinibossShip(ctx) {
      const w = this.width;
      const h = this.height;
      const halfW = w / 2;
      const halfH = h / 2;

      const sprite = assets.images.miniboss;
      if (sprite && sprite.complete && sprite.naturalWidth > 0) {
        // Soft radial aura with boss color (ZERO rectangular fillRect!)
        const auraGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, halfW * 0.95);
        auraGrad.addColorStop(0, 'rgba(0, 243, 255, 0.28)');
        auraGrad.addColorStop(0.65, 'rgba(160, 30, 255, 0.08)');
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
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
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

      const sprite = assets.images.bigboss;
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
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
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
"""
        src = src[:start_pos] + new_boss_block + "\n" + src[end_pos:]
        print("Updated Boss class cleanly!")
    else:
        print("Warning: Boss start or end token not found!")

    # 4. Add Helper Functions (getNextBossConfig, activateSurviveSkill, etc.) right after updateUltBar
    old_ult_section = """  function updateUltBar() {
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
  }"""

    new_ult_section = """  function updateUltBar() {
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
  }"""

    if old_ult_section in src:
        src = src.replace(old_ult_section, new_ult_section)
        print("Added getNextBossConfig, survive skills, atmosphere background")
    else:
        print("Warning: old_ult_section not found!")

    # 5. Update triggerBossEncounter
    old_trigger_boss = """  function triggerBossEncounter() {
    const isBig = (state.bossCycle % 2 === 0);
    const t = TRANSLATIONS[state.lang] || TRANSLATIONS.id;
    const sub = isBig ? t.bossWarningBig : t.bossWarningMini;

    state.bossWarningActive = true;
    state.warningTimer = 2.4;
    if (bossWarningBanner) {
      bossWarningBanner.classList.remove('hidden');
      const titleEl = bossWarningBanner.querySelector('.warning-title');
      if (titleEl) titleEl.textContent = t.bossWarningTitle;
    }
    if (bossWarningAvatar) {
      bossWarningAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
    }
    if (warningSub) warningSub.textContent = sub;
    window.soundFx.playBossWarning();
    window.soundFx.playBGM(isBig ? 'boss' : 'miniboss');

    // Clear normal meteors to prepare the duel arena
    meteors.forEach(m => m.destroy(false));
  }"""

    new_trigger_boss = """  function triggerBossEncounter() {
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
      bossWarningAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
      bossWarningAvatar.style.borderColor = bossConfig.color || '#ff0055';
    }
    if (warningSub) {
      warningSub.textContent = `#${String(bossConfig.id).padStart(3, '0')} ${bossConfig.name.toUpperCase()} - ${bossConfig.title.toUpperCase()}`;
    }
    window.soundFx.playBossWarning();
    window.soundFx.playBGM(isBig ? 'boss' : 'miniboss');

    // Clear normal meteors to prepare the duel arena
    meteors.forEach(m => m.destroy(false));
  }"""

    if old_trigger_boss in src:
        src = src.replace(old_trigger_boss, new_trigger_boss)
        print("Updated triggerBossEncounter")
    else:
        print("Warning: old_trigger_boss not found!")

    # 6. Update startGame for ship lives & survive reset
    old_start_game = """    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

    state.maxLives = conf.lives;
    state.lives = state.maxLives;
    state.score = 0;
    state.survivalTime = 0;
    state.screen = 'playing';
    state.isPaused = false;
    state.isUltActive = false;"""

    new_start_game = """    const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
    const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;

    state.maxLives = conf.lives + shipConf.extraLives;
    state.lives = state.maxLives;
    state.score = 0;
    state.survivalTime = 0;
    state.screen = 'playing';
    state.isPaused = false;
    state.isUltActive = false;
    state.surviveSkillCooldown = 0;
    state.chronoSlowMotionTimer = 0;
    state.bgCurrent = { r: 10, g: 8, b: 20 };
    state.bgTarget = { r: 10, g: 8, b: 20 };
    updateSurviveButtonUI();"""

    if old_start_game in src:
        src = src.replace(old_start_game, new_start_game)
        print("Updated startGame for ship lives and survive reset")
    else:
        print("Warning: old_start_game not found!")

    # 7. Update render() for background atmosphere
    old_render_bg = """    // Clear background
    ctx.fillStyle = '#0a0814';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);"""

    new_render_bg = """    // Dynamic Atmosphere Background
    const bgR = Math.round(state.bgCurrent.r);
    const bgG = Math.round(state.bgCurrent.g);
    const bgB = Math.round(state.bgCurrent.b);
    ctx.fillStyle = `rgb(${bgR}, ${bgG}, ${bgB})`;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Celestial Boss Arena Backdrop (Eclipse / Ion Storm)
    if (state.activeBoss || state.bossWarningActive) {
      drawBossAtmosphereBackdrop(ctx);
    }"""

    if old_render_bg in src:
        src = src.replace(old_render_bg, new_render_bg)
        print("Updated render() background atmosphere")
    else:
        print("Warning: old_render_bg not found!")

    # 8. Update update(dt) for countdowns, slow-mo, and boss spawning
    # Find warningTimer block
    old_warning_spawn = """      if (state.warningTimer <= 0) {
        state.bossWarningActive = false;
        if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
        const isBig = (state.bossCycle % 2 === 0);
        const bossType = isBig ? 'bigboss' : 'miniboss';
        const bossTitle = isBig ? '👑 BIG BOSS: TITAN APEX STARFALL 👑' : '👾 MINI-BOSS: VOID DESTROYER 👾';
        state.activeBoss = new Boss(bossType, state.bossCycle);
        showBossBar(bossTitle);
      }"""

    new_warning_spawn = """      if (state.warningTimer <= 0) {
        state.bossWarningActive = false;
        if (bossWarningBanner) bossWarningBanner.classList.add('hidden');
        const bConf = state.pendingBossConfig || getNextBossConfig(state.difficulty, state.bossCycle);
        state.activeBoss = new Boss(bConf, state.bossCycle);
        showBossBar(state.activeBoss);
      }"""

    if old_warning_spawn in src:
        src = src.replace(old_warning_spawn, new_warning_spawn)
        print("Updated update(dt) boss spawn")
    else:
        print("Warning: old_warning_spawn not found!")

    # Add atmosphere and survive timer update in update(dt)
    old_update_start = """  function update(dt) {
    // 1. Survival time counting (seconds and minutes)
    state.survivalTime += dt;
    timerVal.textContent = formatTime(state.survivalTime);"""

    new_update_start = """  function update(dt) {
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
    }"""

    if old_update_start in src:
        src = src.replace(old_update_start, new_update_start)
        print("Updated update(dt) start")
    else:
        print("Warning: old_update_start not found!")

    # 9. Add Ship Carousel UI logic and button bindings
    ship_carousel_code = """
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
    if (shipAvatarImg) shipAvatarImg.style.filter = conf.filter;

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
"""

    old_setup_inputs = """    if (btnTouchUlt) {
      btnTouchUlt.addEventListener('pointerdown', e => {
        e.preventDefault();
        triggerUltimate();
      });
    }"""

    new_setup_inputs = """    if (btnTouchUlt) {
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
    }"""

    if old_setup_inputs in src:
        src = src.replace(old_setup_inputs, new_setup_inputs)
        print("Bound btnTouchSurvive pointerdown")
    else:
        print("Warning: old_setup_inputs not found!")

    # Key listener for [C]
    old_key_listener = """      if (e.code === 'Space') {
        e.preventDefault();
        triggerUltimate();
      }"""

    new_key_listener = """      if (e.code === 'Space') {
        e.preventDefault();
        triggerUltimate();
      }
      if (e.key === 'c' || e.key === 'C') {
        activateSurviveSkill();
      }"""

    if old_key_listener in src:
        src = src.replace(old_key_listener, new_key_listener)
        print("Bound [C] key to activateSurviveSkill")
    else:
        print("Warning: old_key_listener not found!")

    # Add initShipSelection to init()
    old_init = """    initStarfield();
    setupInputs();"""

    new_init = """    initStarfield();
    initShipSelection();
    setupInputs();"""

    if old_init in src:
        src = src.replace(old_init, new_init)
        print("Added initShipSelection() to init()")
    else:
        print("Warning: old_init not found!")

    # Insert ship_carousel_code before setupInputs
    setup_inputs_token = "  function setupInputs() {"
    if setup_inputs_token in src:
        src = src.replace(setup_inputs_token, ship_carousel_code + "\n" + setup_inputs_token)
        print("Inserted ship carousel functions")
    else:
        print("Warning: setupInputs token not found!")

    with open('js/game.js', 'w', encoding='utf-8') as f:
        f.write(src)

    print("Finished applying all enhancements to js/game.js!")

if __name__ == '__main__':
    main()

