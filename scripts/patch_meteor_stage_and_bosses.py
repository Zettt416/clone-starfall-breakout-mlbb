import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Meteor.update
old_meteor_update = '''    update(dt) {
      this.x -= this.speed * dt;
      this.y += this.vy * dt;
      this.rotation += this.rotSpeed * dt;

      if (this.x < -60) {
        this.toRemove = true;
      }
    }'''

new_meteor_update = '''    update(dt) {
      this.time = (this.time || 0) + dt;
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
print("Updated Meteor.update!")

# 2. Update Meteor.draw
old_meteor_draw = '''    draw(ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);

      if (this.type === 'star') {'''

new_meteor_draw = '''    draw(ctx) {
      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation);

      if (this.isDrone) {
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
      } else if (this.type === 'star') {'''

assert old_meteor_draw in text, "old_meteor_draw not found"
text = text.replace(old_meteor_draw, new_meteor_draw, 1)
print("Updated Meteor.draw for fast drone!")

# 3. Update updateSpawners for fast_scout drones
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

# 4. Add drawStageParallaxBackdrop
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
      // --- Level 3 (HARD): Crimson Supernova Core & Solar Flares ---
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

if old_render_backdrop in text:
    text = text.replace(old_render_backdrop, new_render_backdrop, 1)
    print("Updated render() backdrop!")

# 5. Update drawBigbossShip to map unique Big Boss models
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

if old_bigboss_sprite in text:
    text = text.replace(old_bigboss_sprite, new_bigboss_sprite, 1)
    print("Updated drawBigbossShip with unique big boss models!")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("All meteor, stage backdrop, and boss patches applied successfully!")

