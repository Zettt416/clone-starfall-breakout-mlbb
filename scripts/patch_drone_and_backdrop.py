import os

with open('js/game.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add enemy_scout asset
asset_needle = "loadAsset('powerup_void_needle', 'assets/images/powerup_void_needle.png');"
asset_repl = asset_needle + "\n  // Dedicated Enemy Scout Drone Sprite\n  loadAsset('enemy_scout', 'assets/images/enemy_scout_drone.png');"
assert asset_needle in code, 'Asset needle not found'
code = code.replace(asset_needle, asset_repl, 1)

# 2. Update fast_scout in Meteor constructor
drone_ctor_needle = """      } else if (type === 'fast_scout') {
        this.isDrone = true;
        this.radius = 16;
        this.hp = 2;
        this.maxHp = 2;
        this.speed = 280 + Math.random() * 60;
        this.vy = (Math.random() - 0.5) * 40;
        this.score = 75;
        this.color = '#ff0055';"""
drone_ctor_repl = """      } else if (type === 'fast_scout') {
        this.isDrone = true;
        this.radius = 16;
        this.hp = 2;
        this.maxHp = 2;
        this.speed = 280 + Math.random() * 60;
        this.vy = (Math.random() - 0.5) * 40;
        this.score = 75;
        this.color = '#ff0055';
        this.rotation = 0;
        this.rotSpeed = 0;"""
assert drone_ctor_needle in code, 'Drone ctor needle not found'
code = code.replace(drone_ctor_needle, drone_ctor_repl, 1)

# 3. Update Meteor update for drone banking
update_needle = """      if (this.isDrone) {
        this.y += Math.sin(this.time * 6.5) * 2.2;
      }
      this.rotation += this.rotSpeed * dt;"""
update_repl = """      if (this.isDrone) {
        this.y += Math.sin(this.time * 6.5) * 2.2;
        this.rotation = Math.sin(this.time * 6.5) * 0.12 + (this.vy * 0.002);
      } else {
        this.rotation += this.rotSpeed * dt;
      }"""
assert update_needle in code, 'Update needle not found'
code = code.replace(update_needle, update_repl, 1)

# 4. Update Meteor draw for drone sprite
draw_needle = """      if (this.isDrone) {
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
      }"""

draw_repl = """      if (this.isDrone) {
        // Fast Robotic Scout Interceptor Drone (Dedicated 32-bit Sprite)
        const scoutImg = assets.images['enemy_scout'];
        if (scoutImg && scoutImg.complete && scoutImg.naturalWidth > 0) {
          const dw = 52;
          const dh = 24;
          ctx.drawImage(scoutImg, -dw / 2, -dh / 2, dw, dh);

          // Animated Dual Cyan Ion Exhaust Plumes
          ctx.save();
          ctx.fillStyle = '#00f3ff';
          ctx.shadowColor = '#00f3ff';
          ctx.shadowBlur = 10;
          const flame1 = 10 + Math.random() * 9;
          ctx.beginPath();
          ctx.moveTo(dw / 2 - 5, -5);
          ctx.lineTo(dw / 2 + flame1, -3);
          ctx.lineTo(dw / 2 - 5, -1);
          ctx.fill();

          const flame2 = 8 + Math.random() * 8;
          ctx.beginPath();
          ctx.moveTo(dw / 2 - 5, 1);
          ctx.lineTo(dw / 2 + flame2, 3);
          ctx.lineTo(dw / 2 - 5, 5);
          ctx.fill();
          ctx.restore();
        } else {
          // Fallback procedural drone
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
          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.arc(0, 0, 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }"""
assert draw_needle in code, 'Draw needle not found'
code = code.replace(draw_needle, draw_repl, 1)

# 5. Overhaul backdrop functions
start_marker = '// --- Dynamic Multi-Layer Parallax Stage Environments per Level ---'
end_marker = '// --- VFX & Helpers ---'
assert start_marker in code and end_marker in code, 'Backdrop markers not found'

part_before = code[:code.index(start_marker)]
part_after = code[code.index(end_marker):]

new_backdrop = """// --- Dynamic Atmospheric Cosmic Nebulae & Parallax Space Backdrop per Level ---
  function drawStageParallaxBackdrop(ctx) {
    if (state.activeBoss || state.bossWarningActive) return; // Boss arena overrides backdrop
    const t = Date.now() * 0.0003;

    ctx.save();
    if (state.difficulty === 'easy') {
      // --- Level 1 (EASY): Azure Sector & Serene Cosmic Veil ---
      // Primary Cerulean Deep-Space Nebula
      const neb1 = ctx.createRadialGradient(CANVAS_WIDTH * 0.76, 170, 20, CANVAS_WIDTH * 0.76, 170, 360);
      neb1.addColorStop(0, 'rgba(0, 220, 255, 0.14)');
      neb1.addColorStop(0.4, 'rgba(0, 120, 220, 0.08)');
      neb1.addColorStop(0.8, 'rgba(10, 30, 80, 0.03)');
      neb1.addColorStop(1, 'transparent');
      ctx.fillStyle = neb1;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.76, 170, 360, 0, Math.PI * 2);
      ctx.fill();

      // Secondary Indigo Cosmic Dust Lane
      const neb2 = ctx.createRadialGradient(CANVAS_WIDTH * 0.38, 380, 15, CANVAS_WIDTH * 0.38, 380, 300);
      neb2.addColorStop(0, 'rgba(30, 80, 210, 0.11)');
      neb2.addColorStop(0.5, 'rgba(15, 30, 90, 0.05)');
      neb2.addColorStop(1, 'transparent');
      ctx.fillStyle = neb2;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.38, 380, 300, 0, Math.PI * 2);
      ctx.fill();

      // Soft Distant Celestial Aurora Ribbon
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.06)';
      ctx.lineWidth = 18;
      ctx.beginPath();
      ctx.moveTo(CANVAS_WIDTH * 0.1, 80);
      ctx.bezierCurveTo(CANVAS_WIDTH * 0.45, 140 + Math.sin(t * 1.5) * 15, CANVAS_WIDTH * 0.7, 70, CANVAS_WIDTH * 1.1, 150);
      ctx.stroke();

    } else if (state.difficulty === 'normal') {
      // --- Level 2 (NORMAL): Stellar Nursery / Magenta-Violet Orion Veil ---
      // Primary Violet-Magenta Stellar Rift
      const neb1 = ctx.createRadialGradient(CANVAS_WIDTH * 0.72, 230, 30, CANVAS_WIDTH * 0.72, 230, 380);
      neb1.addColorStop(0, 'rgba(180, 50, 240, 0.15)');
      neb1.addColorStop(0.35, 'rgba(230, 30, 120, 0.08)');
      neb1.addColorStop(0.75, 'rgba(60, 20, 100, 0.03)');
      neb1.addColorStop(1, 'transparent');
      ctx.fillStyle = neb1;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.72, 230, 380, 0, Math.PI * 2);
      ctx.fill();

      // Secondary Amber-Rose Stardust Bloom
      const neb2 = ctx.createRadialGradient(CANVAS_WIDTH * 0.32, 130, 10, CANVAS_WIDTH * 0.32, 130, 280);
      neb2.addColorStop(0, 'rgba(255, 140, 60, 0.09)');
      neb2.addColorStop(0.5, 'rgba(180, 50, 60, 0.04)');
      neb2.addColorStop(1, 'transparent');
      ctx.fillStyle = neb2;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.32, 130, 280, 0, Math.PI * 2);
      ctx.fill();

      // Ethereal Cosmic Filament
      ctx.strokeStyle = 'rgba(210, 80, 255, 0.05)';
      ctx.lineWidth = 22;
      ctx.beginPath();
      ctx.moveTo(CANVAS_WIDTH * 0.05, 340);
      ctx.bezierCurveTo(CANVAS_WIDTH * 0.4, 260 + Math.sin(t * 1.2) * 20, CANVAS_WIDTH * 0.65, 380, CANVAS_WIDTH * 1.05, 290);
      ctx.stroke();

    } else if (state.difficulty === 'hard') {
      // --- Level 3 (HARD): Crimson Sector & Solar Radiation Nebula ---
      // Primary Fiery Crimson Core Nebula
      const neb1 = ctx.createRadialGradient(CANVAS_WIDTH * 0.78, 250, 25, CANVAS_WIDTH * 0.78, 250, 400);
      neb1.addColorStop(0, 'rgba(255, 45, 80, 0.16)');
      neb1.addColorStop(0.4, 'rgba(200, 25, 45, 0.09)');
      neb1.addColorStop(0.8, 'rgba(80, 10, 25, 0.03)');
      neb1.addColorStop(1, 'transparent');
      ctx.fillStyle = neb1;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.78, 250, 400, 0, Math.PI * 2);
      ctx.fill();

      // Secondary Volatile Amber Flare Cloud
      const neb2 = ctx.createRadialGradient(CANVAS_WIDTH * 0.42, 390, 10, CANVAS_WIDTH * 0.42, 390, 310);
      neb2.addColorStop(0, 'rgba(255, 130, 0, 0.11)');
      neb2.addColorStop(0.5, 'rgba(150, 30, 0, 0.04)');
      neb2.addColorStop(1, 'transparent');
      ctx.fillStyle = neb2;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.42, 390, 310, 0, Math.PI * 2);
      ctx.fill();

      // Atmospheric Radiation Belt
      ctx.strokeStyle = 'rgba(255, 90, 40, 0.06)';
      ctx.lineWidth = 20;
      ctx.beginPath();
      ctx.moveTo(CANVAS_WIDTH * 0.15, 110);
      ctx.bezierCurveTo(CANVAS_WIDTH * 0.5, 190 + Math.cos(t * 1.8) * 18, CANVAS_WIDTH * 0.75, 120, CANVAS_WIDTH * 1.1, 230);
      ctx.stroke();

    } else {
      // --- Level 4 (HARDCOREZ): Abyssal Void & Dark Matter Rift ---
      // Primary Ultraviolet Deep Singularity Nebula
      const neb1 = ctx.createRadialGradient(CANVAS_WIDTH * 0.70, 240, 20, CANVAS_WIDTH * 0.70, 240, 420);
      neb1.addColorStop(0, 'rgba(140, 0, 255, 0.18)');
      neb1.addColorStop(0.35, 'rgba(0, 230, 255, 0.08)');
      neb1.addColorStop(0.75, 'rgba(30, 5, 70, 0.03)');
      neb1.addColorStop(1, 'transparent');
      ctx.fillStyle = neb1;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.70, 240, 420, 0, Math.PI * 2);
      ctx.fill();

      // Secondary Dark Matter Eddy
      const neb2 = ctx.createRadialGradient(CANVAS_WIDTH * 0.35, 160, 10, CANVAS_WIDTH * 0.35, 160, 290);
      neb2.addColorStop(0, 'rgba(0, 190, 255, 0.09)');
      neb2.addColorStop(0.5, 'rgba(80, 0, 180, 0.04)');
      neb2.addColorStop(1, 'transparent');
      ctx.fillStyle = neb2;
      ctx.beginPath();
      ctx.arc(CANVAS_WIDTH * 0.35, 160, 290, 0, Math.PI * 2);
      ctx.fill();

      // Void Gravitational Filament
      ctx.strokeStyle = 'rgba(160, 50, 255, 0.07)';
      ctx.lineWidth = 24;
      ctx.beginPath();
      ctx.moveTo(CANVAS_WIDTH * 0.08, 420);
      ctx.bezierCurveTo(CANVAS_WIDTH * 0.45, 320 + Math.sin(t * 1.4) * 22, CANVAS_WIDTH * 0.7, 440, CANVAS_WIDTH * 1.05, 330);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawBossAtmosphereBackdrop(ctx) {
    if (!state.activeBoss && !state.bossWarningActive) return;
    const isBig = state.activeBoss ? (state.activeBoss.type === 'bigboss') : (state.bossCycle % 2 === 0);
    const arenaX = CANVAS_WIDTH * 0.78;
    const arenaY = CANVAS_HEIGHT * 0.50;
    const t = Date.now() * 0.001;

    ctx.save();
    if (isBig) {
      // Atmospheric Pulsing Crimson Boss Arena Halo (No solid black ball, no spiky sticks)
      const pulse = 1.0 + Math.sin(t * 2.2) * 0.12;
      const auraGrad = ctx.createRadialGradient(arenaX, arenaY, 30, arenaX, arenaY, 360 * pulse);
      auraGrad.addColorStop(0, 'rgba(255, 0, 85, 0.22)');
      auraGrad.addColorStop(0.35, 'rgba(180, 0, 60, 0.11)');
      auraGrad.addColorStop(0.7, 'rgba(60, 0, 40, 0.04)');
      auraGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = auraGrad;
      ctx.beginPath();
      ctx.arc(arenaX, arenaY, 360 * pulse, 0, Math.PI * 2);
      ctx.fill();

      // Menacing Outer Edge Vignette to focus attention on the boss duel
      const vigGrad = ctx.createRadialGradient(CANVAS_WIDTH * 0.5, CANVAS_HEIGHT * 0.5, CANVAS_HEIGHT * 0.35, CANVAS_WIDTH * 0.5, CANVAS_HEIGHT * 0.5, CANVAS_WIDTH * 0.65);
      vigGrad.addColorStop(0, 'transparent');
      vigGrad.addColorStop(1, 'rgba(160, 0, 40, 0.13)');
      ctx.fillStyle = vigGrad;
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    } else {
      // Miniboss: Swirling Electric Ion Storm Clouds
      const pulse = 1.0 + Math.sin(t * 3.0) * 0.10;
      const stormGrad = ctx.createRadialGradient(arenaX, arenaY, 20, arenaX, arenaY, 290 * pulse);
      stormGrad.addColorStop(0, 'rgba(0, 243, 255, 0.18)');
      stormGrad.addColorStop(0.4, 'rgba(110, 0, 255, 0.09)');
      stormGrad.addColorStop(0.8, 'rgba(20, 0, 60, 0.03)');
      stormGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = stormGrad;
      ctx.beginPath();
      ctx.arc(arenaX, arenaY, 290 * pulse, 0, Math.PI * 2);
      ctx.fill();

      // Ambient Distant Lightning
      if (Math.random() < 0.03) {
        ctx.strokeStyle = 'rgba(0, 243, 255, 0.28)';
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
  }

  """

code = part_before + new_backdrop + part_after

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully patched drone and backdrop in js/game.js')

