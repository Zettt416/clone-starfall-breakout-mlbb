import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Boss.prototype.update
old_update_start = '''    update(dt) {
      this.time += dt;
      this.prevY = this.y;
      const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;

      // Smooth entry glide
      if (this.x > this.targetX) {
        this.x -= 140 * dt;
        if (this.x < this.targetX) this.x = this.targetX;
      }'''

new_update_start = '''    spawnAfterimage(initialAlpha = 0.65) {
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
      const safeMinY = Math.max(55, this.height * 0.48);
      const safeMaxY = CANVAS_HEIGHT - Math.max(55, this.height * 0.48);

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
      this.afterimages = this.afterimages.filter(g => g.alpha > 0);'''

assert old_update_start in text, 'old_update_start not found!'

# Find the end of old update method
old_update_middle = '''      // Natural Multi-Harmonic Organic Motion
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
      }'''

assert old_update_middle in text, 'old_update_middle not found!'

# Replace the entire block from old_update_start to old_update_middle
text = text.replace(old_update_start + '\n\n' + old_update_middle, new_update_start, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Applied Mega Man update state machine successfully!')

