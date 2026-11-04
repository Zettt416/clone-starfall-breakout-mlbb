import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Player constructor and buffs
old_player_init = '''      this.buffs = {
        rapid: 0,
        multi: 0,
        pierce: shipConf.id === 'chrono_phantom' ? 999999 : 0,
        burst: shipConf.id === 'aether_vanguard' ? 999999 : 0,
        shield: 0
      };
      this.tilt = 0; // vertical banking angle'''

new_player_init = '''      this.buffs = {
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
      this.tilt = 0; // vertical banking angle'''

if old_player_init in text:
    text = text.replace(old_player_init, new_player_init, 1)
    print("Updated Player constructor buffs!")

# 2. Update Player.update for hyperdrive speed, tesla coil, and fire rate
old_player_update_fire = '''      // Auto-Shooting towards RIGHT
      const currentFireInterval = this.buffs.rapid > 0 ? this.baseFireInterval * 0.5 : this.baseFireInterval;
      this.shootCooldown -= dt;
      if (this.shootCooldown <= 0) {
        this.shoot();
        this.shootCooldown = currentFireInterval;
      }'''

new_player_update_fire = '''      // Automatic Tesla Coil Zap (Aether Vanguard)
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
      }'''

if old_player_update_fire in text:
    text = text.replace(old_player_update_fire, new_player_update_fire, 1)
    print("Updated Player.update fire logic!")

# 3. Update Player.shoot() to handle unique powerup mechanics
old_player_shoot = '''    shoot() {
      const isPierce = this.buffs.pierce > 0;
      const isMulti = this.buffs.multi > 0;
      const isBurst = this.buffs.burst > 0;
      const isRapid = this.buffs.rapid > 0;
      const shipConf = SHIPS_CONFIG[state.selectedShip] || SHIPS_CONFIG.stella_nova;

      window.soundFx.playShoot();

      const cannonX = this.x + 20;

      if (shipConf.id === 'aether_vanguard') {
        // Heavy Flak Cannon: 3 explosive spread shells with burst splash!
        projectiles.push(new Projectile(cannonX, this.y, 650, 0, isPierce, true, isRapid, true));
        projectiles.push(new Projectile(cannonX - 4, this.y - 14, 620, -110, isPierce, true, isRapid, true));
        projectiles.push(new Projectile(cannonX - 4, this.y + 14, 620, 110, isPierce, true, isRapid, true));
      } else if (shipConf.id === 'chrono_phantom') {
        // Needle Tachyon Laser: piercing high-speed needle beams!
        projectiles.push(new Projectile(cannonX, this.y - 6, 920, 0, true, isBurst, isRapid, false));
        projectiles.push(new Projectile(cannonX, this.y + 6, 920, 0, true, isBurst, isRapid, false));
      } else {
        // Stella Nova: Classic Twin Plasma Bolts or Triple Spread when MULTI
        if (isMulti) {
          projectiles.push(new Projectile(cannonX, this.y, 750, 0, isPierce, isBurst, isRapid, true));
          projectiles.push(new Projectile(cannonX - 4, this.y - 12, 700, -140, isPierce, isBurst, isRapid, true));
          projectiles.push(new Projectile(cannonX - 4, this.y + 12, 700, 140, isPierce, isBurst, isRapid, true));
        } else {
          projectiles.push(new Projectile(cannonX, this.y - 8, 750, 0, isPierce, isBurst, isRapid, false));
          projectiles.push(new Projectile(cannonX, this.y + 8, 750, 0, isPierce, isBurst, isRapid, false));
        }
      }

      createMuzzleSparks(cannonX + 4, this.y);
    }'''

new_player_shoot = '''    shoot() {
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
    }'''

if old_player_shoot in text:
    text = text.replace(old_player_shoot, new_player_shoot, 1)
    print("Updated Player.shoot!")

# 4. Update Player.draw() to use individual ship sprites and draw Quantum Clones
old_player_draw_hull = '''      // 2. Starfighter Hull (16-Bit Pixel Art PNG or Procedural Fallback)
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
      } else {'''

new_player_draw_hull = '''      // 2. Starfighter Hull (Unique High-Res Arcade Sprites for Each Ship)
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
      } else {'''

if old_player_draw_hull in text:
    text = text.replace(old_player_draw_hull, new_player_draw_hull, 1)
    print("Updated Player.draw hull!")

# 5. Add Tesla Chain Lightning Helper
tesla_func = '''  // --- Tesla Chain Lightning Auto-Discharge System ---
  function fireTeslaChainLightning(px, py) {
    if (!meteors || meteors.length === 0) return;
    const targets = meteors
      .filter(m => !m.toRemove && m.x > px)
      .map(m => ({ m, dist: Math.hypot(m.x - px, m.y - py) }))
      .sort((a, b) => a.dist - b.dist)
      .slice(0, 2);

    targets.forEach(({ m }) => {
      m.takeDamage(3);
      state.score += 25;
      scoreVal.textContent = state.score;

      for (let i = 0; i < 4; i++) {
        particles.push({
          x: m.x + (Math.random() - 0.5) * m.radius,
          y: m.y + (Math.random() - 0.5) * m.radius,
          vx: (Math.random() - 0.5) * 80,
          vy: (Math.random() - 0.5) * 80,
          size: 3,
          color: '#ffdd00',
          life: 0.18,
          maxLife: 0.18
        });
      }
    });

    if (targets.length > 0 && window.soundFx) {
      window.soundFx.playLaser();
    }
  }
'''

if 'fireTeslaChainLightning' not in text:
    text = text.replace('  // --- Ultimate Mechanism ---', tesla_func + '\n  // --- Ultimate Mechanism ---', 1)
    print("Added fireTeslaChainLightning!")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied Player & PowerUp mechanics updates!")
