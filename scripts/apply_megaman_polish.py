import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the duplicate shootTimer / specialTimer block
dup_block = '''      // Attack Timers (fire after entering arena)
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
          this.startSkillTelegraph();
          this.specialTimer = (isBig ? 6.2 : 5.4) * conf.bossShootIntervalMult;
        }
      }'''

if dup_block in text:
    text = text.replace(dup_block, '// Attack timers handled inside action states', 1)
    print('Removed duplicate attack timers block!')
else:
    print('Warning: dup_block not found')

# 2. Add drawAfterimages to Boss class right before draw(ctx)
old_draw_head = '''    draw(ctx) {
      ctx.save();

      // Telegraphed Signature Skill Charging Animation'''

new_draw_head = '''    drawAfterimages(ctx) {
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

      // Telegraphed Signature Skill Charging Animation'''

if old_draw_head in text:
    text = text.replace(old_draw_head, new_draw_head, 1)
    print('Added drawAfterimages and call to Boss.prototype.draw!')
else:
    print('Warning: old_draw_head not found')

# 3. Fix muzzle anchor in drawBossHyperRailgunBeam and drawValkyrieCelestialLanceBeam
old_hyper_beam = '''  // --- Colossal Boss Hyper-Railgun Laser Beam (Organic, Smooth, Cinematic) ---
  function drawBossHyperRailgunBeam(ctx, boss) {
    ctx.save();
    const muzzleX = boss.x - boss.width * 0.48;
    const beamY = boss.y;'''

new_hyper_beam = '''  // --- Colossal Boss Hyper-Railgun Laser Beam (Organic, Smooth, Cinematic) ---
  function drawBossHyperRailgunBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.44;
    const beamY = boss.laserTargetY || boss.y;'''

if old_hyper_beam in text:
    text = text.replace(old_hyper_beam, new_hyper_beam, 1)
    print('Fixed drawBossHyperRailgunBeam muzzle anchor!')
else:
    print('Warning: old_hyper_beam not found')

old_lance_beam = '''  // --- Radiant Valkyrie Celestial Lance of Longinus Beam ---
  function drawValkyrieCelestialLanceBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.46;
    const beamY = boss.laserTargetY || boss.y;'''

new_lance_beam = '''  // --- Radiant Valkyrie Celestial Lance of Longinus Beam ---
  function drawValkyrieCelestialLanceBeam(ctx, boss) {
    ctx.save();
    const muzzleX = (boss.currentX || boss.x) - boss.width * 0.44;
    const beamY = boss.laserTargetY || boss.y;'''

if old_lance_beam in text:
    text = text.replace(old_lance_beam, new_lance_beam, 1)
    print('Ensured drawValkyrieCelestialLanceBeam muzzle anchor!')
else:
    print('Warning: old_lance_beam not found')

# 4. Strict Safe Altitude Clamping in Boss update & startSkillTelegraph
old_safe_calc = '''      // Strict Safe Altitude Boundary (Boss never leaves screen or clips into bottom/top HUD)
      const safeMinY = Math.max(55, this.height * 0.48);
      const safeMaxY = CANVAS_HEIGHT - Math.max(55, this.height * 0.48);'''

new_safe_calc = '''      // Strict Safe Altitude Boundary (Boss never leaves screen or clips into bottom/top HUD)
      const halfH = this.height * 0.5;
      const safeMinY = Math.max(75, Math.round(halfH + 15));
      const safeMaxY = Math.min(CANVAS_HEIGHT - 35, CANVAS_HEIGHT - Math.round(halfH + 15));'''

if old_safe_calc in text:
    text = text.replace(old_safe_calc, new_safe_calc, 1)
    print('Updated strict safe altitude calculation!')
else:
    print('Warning: old_safe_calc not found')

old_telegraph_y = '''      this.skillTargetY = Math.max(45, Math.min(CANVAS_HEIGHT - 45, player ? player.y : CANVAS_HEIGHT / 2));'''
new_telegraph_y = '''      const halfH = this.height * 0.5;
      const safeMinY = Math.max(75, Math.round(halfH + 15));
      const safeMaxY = Math.min(CANVAS_HEIGHT - 35, CANVAS_HEIGHT - Math.round(halfH + 15));
      this.skillTargetY = Math.max(safeMinY, Math.min(safeMaxY, player ? player.y : CANVAS_HEIGHT / 2));'''

if old_telegraph_y in text:
    text = text.replace(old_telegraph_y, new_telegraph_y, 1)
    print('Clamped skillTargetY in startSkillTelegraph!')
else:
    print('Warning: old_telegraph_y not found')

# 5. Expose test hooks on window for automated verification
expose_hook = '''  // Expose for testing/CDP
  window.gameState = state;
  window.testBoss = function(id = 56) {
    const bConf = (window.BOSS_CATALOG || []).find(b => b.id === id) || window.BOSS_CATALOG[0];
    state.activeBoss = new Boss(bConf, 2);
    showBossBar(state.activeBoss);
    return state.activeBoss;
  };
'''

if 'window.testBoss' not in text:
    text = text.replace('  init();\n})();', expose_hook + '  init();\n})();', 1)
    print('Exposed window.testBoss hook!')

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('All patches applied to js/game.js!')

