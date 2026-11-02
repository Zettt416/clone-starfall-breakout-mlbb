# -*- coding: utf-8 -*-

def update_game_js():
    with open('js/game.js', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update loadAsset calls
    old_load = """    loadAsset('miniboss', 'assets/images/miniboss.png');
    loadAsset('bigboss', 'assets/images/bigboss.png');"""

    new_load = """    loadAsset('miniboss', 'assets/images/boss_alien_leviathan.png');
    loadAsset('bigboss', 'assets/images/boss_mecha_titan.png');
    loadAsset('boss_monster', 'assets/images/boss_alien_leviathan.png');
    loadAsset('boss_mecha', 'assets/images/boss_mecha_titan.png');
    loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');
    loadAsset('boss_humanoid', 'assets/images/boss_humanoid_valkyrie.png');
    loadAsset('boss_alien', 'assets/images/boss_eldritch_eye.png');"""

    if old_load in src:
        src = src.replace(old_load, new_load)
        print("Updated asset loading in js/game.js")

    # 2. Update showBossBar avatar
    old_avatar = """    if (bossBarAvatar) {
      const isBig = isObj ? (boss.type === 'bigboss') : (state.activeBoss && state.activeBoss.type === 'bigboss');
      bossBarAvatar.src = isBig ? 'assets/images/bigboss.png' : 'assets/images/miniboss.png';
      if (isObj && boss.color) bossBarAvatar.style.borderColor = boss.color;
    }"""

    new_avatar = """    if (bossBarAvatar) {
      const arch = (isObj && boss.archetype) ? boss.archetype : (isObj && boss.type === 'bigboss' ? 'mecha' : 'monster');
      bossBarAvatar.src = `assets/images/boss_${arch}.png`;
      if (isObj && boss.color) bossBarAvatar.style.borderColor = boss.color;
    }"""

    if old_avatar in src:
        src = src.replace(old_avatar, new_avatar)
        print("Updated showBossBar avatar to use archetype")

    # 3. Update Boss constructor in js/game.js
    old_boss_init = """      this.data = bossData;
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
      this.height = isBig ? 182 : 91;"""

    new_boss_init = """      this.data = bossData;
      this.type = bossData.isBig ? 'bigboss' : 'miniboss';
      this.id = bossData.id || cycle;
      this.name = bossData.name || (this.type === 'bigboss' ? 'TITAN APEX' : 'VOID DESTROYER');
      this.title = bossData.title || (this.type === 'bigboss' ? 'COLOSSAL MECHA' : 'VOID DESTROYER');
      this.color = bossData.color || (this.type === 'bigboss' ? '#ffd000' : '#00f3ff');
      this.attackType = bossData.attack || (this.type === 'bigboss' ? 'railgun_heavy' : 'plasma_twin');
      this.archetype = bossData.archetype || (this.type === 'bigboss' ? 'mecha' : 'monster');
      this.cycle = cycle;
      const isBig = (this.type === 'bigboss');

      // Native proportions per archetype
      const sizeMult = isBig ? 1.25 : 1.0;
      if (this.archetype === 'spaceship') {
        this.width = Math.round(195 * sizeMult);
        this.height = Math.round(81 * sizeMult);
        this.baseHue = 183;
      } else if (this.archetype === 'mecha') {
        this.width = Math.round(180 * sizeMult);
        this.height = Math.round(172 * sizeMult);
        this.baseHue = 183;
      } else if (this.archetype === 'humanoid') {
        this.width = Math.round(160 * sizeMult);
        this.height = Math.round(130 * sizeMult);
        this.baseHue = 227;
      } else if (this.archetype === 'alien') {
        this.width = Math.round(168 * sizeMult);
        this.height = Math.round(128 * sizeMult);
        this.baseHue = 270;
      } else { // 'monster'
        this.width = Math.round(175 * sizeMult);
        this.height = Math.round(91 * sizeMult);
        this.baseHue = 318;
      }"""

    if old_boss_init in src:
        src = src.replace(old_boss_init, new_boss_init)
        print("Updated Boss constructor for 5 archetypes")

    # 4. Update drawOrganicAppendages in js/game.js
    old_appendages = """    drawOrganicAppendages(ctx) {
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
    }"""

    new_appendages = """    drawOrganicAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'monster' || this.archetype === 'alien') {
        // Undulating Bioluminescent Tendrils / Tentacles
        const tendrilCount = this.archetype === 'alien' ? 5 : 4;
        const rootX = halfW * 0.65;
        const segmentCount = 6;
        const segLen = 14;

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

          ctx.fillStyle = this.color || '#00f3ff';
          ctx.beginPath();
          ctx.arc(cx, cy, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (this.archetype === 'humanoid') {
        // Flowing Neon Energy Halo & Wings
        const wingPulse = Math.sin(this.time * 4) * 8;
        ctx.strokeStyle = this.color || '#ff00aa';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(halfW * 0.1, -halfH * 0.2, 28 + wingPulse, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(halfW * 0.1, -halfH * 0.2, 14, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        // Spaceship & Mecha: Roaring Plasma Exhaust Jets
        const thrusterCount = this.archetype === 'spaceship' ? 2 : 3;
        const rootX = halfW * 0.8;
        for (let i = 0; i < thrusterCount; i++) {
          const thrusterY = -halfH * 0.35 + i * (halfH * 0.7 / Math.max(1, thrusterCount - 1));
          const flameLen = 28 + Math.sin(this.time * 18 + i * 2) * 14 + Math.random() * 8;
          const flameGrad = ctx.createLinearGradient(rootX, thrusterY, rootX + flameLen, thrusterY);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.3, this.color || '#00f3ff');
          flameGrad.addColorStop(0.7, '#ff0055');
          flameGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(rootX, thrusterY - 6);
          ctx.lineTo(rootX + flameLen, thrusterY);
          ctx.lineTo(rootX, thrusterY + 6);
          ctx.closePath();
          ctx.fill();
        }
      }
      ctx.restore();
    }"""

    if old_appendages in src:
        src = src.replace(old_appendages, new_appendages)
        print("Updated drawOrganicAppendages for all 5 archetypes")

    # 5. Update drawMinibossShip / drawBigbossShip to load by archetype
    old_draw_mini = """    drawMinibossShip(ctx) {
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
        } else {
          const targetHue = hexToHue(this.color || '#00f3ff');
          const hueDiff = (targetHue - 185 + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.4)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();
        return;
      }"""

    new_draw_mini = """    drawMinibossShip(ctx) {
      const w = this.width;
      const h = this.height;
      const halfW = w / 2;
      const halfH = h / 2;

      const spriteKey = 'boss_' + (this.archetype || 'monster');
      const sprite = assets.images[spriteKey] || assets.images.miniboss;
      if (sprite && sprite.complete && sprite.naturalWidth > 0) {
        const auraGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, halfW * 0.95);
        auraGrad.addColorStop(0, `${this.color || '#00f3ff'}44`);
        auraGrad.addColorStop(0.65, `${this.color || '#9d4edd'}14`);
        auraGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(0, 0, halfW * 0.95, 0, Math.PI * 2);
        ctx.fill();

        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#00f3ff');
          const baseHue = this.baseHue || 318;
          const hueDiff = (targetHue - baseHue + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.35)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();
        return;
      }"""

    if old_draw_mini in src:
        src = src.replace(old_draw_mini, new_draw_mini)
        print("Updated drawMinibossShip archetype loading")

    old_draw_big = """    drawBigbossShip(ctx) {
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
        } else {
          const targetHue = hexToHue(this.color || '#ffd000');
          const hueDiff = (targetHue - 45 + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.3)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();
        return;
      }"""

    new_draw_big = """    drawBigbossShip(ctx) {
      const w = this.width;
      const h = this.height;
      const halfW = w / 2;
      const halfH = h / 2;

      const spriteKey = 'boss_' + (this.archetype || 'mecha');
      const sprite = assets.images[spriteKey] || assets.images.bigboss;
      if (sprite && sprite.complete && sprite.naturalWidth > 0) {
        const auraGrad = ctx.createRadialGradient(0, 0, 20, 0, 0, halfW * 0.95);
        auraGrad.addColorStop(0, this.isChargingLaser ? 'rgba(0, 243, 255, 0.35)' : `${this.color || '#ffd000'}44`);
        auraGrad.addColorStop(0.65, this.isChargingLaser ? 'rgba(0, 180, 255, 0.1)' : `${this.color || '#ff0055'}14`);
        auraGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.arc(0, 0, halfW * 0.95, 0, Math.PI * 2);
        ctx.fill();

        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#ffd000');
          const baseHue = this.baseHue || 183;
          const hueDiff = (targetHue - baseHue + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.35)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();
        return;
      }"""

    if old_draw_big in src:
        src = src.replace(old_draw_big, new_draw_big)
        print("Updated drawBigbossShip archetype loading")

    # 6. Update renderBossCodex with archetype badges and thumbnails
    old_codex_render = """    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
    grid.innerHTML = tierBosses.map(b => {
      const isBig = b.isBig;
      const badgeClass = isBig ? 'codex-badge-big' : 'codex-badge-mini';
      const badgeText = isBig ? '👑 BIG BOSS' : '👾 MINIBOSS';
      return `
        <div class="codex-card" style="border-left: 3px solid ${b.color};">
          <div class="codex-card-top">
            <span class="codex-id" style="color: ${b.color};">#${String(b.id).padStart(3, '0')}</span>
            <span class="codex-badge ${badgeClass}">${badgeText}</span>
          </div>
          <div class="codex-name">${b.name}</div>
          <div class="codex-title">${b.title}</div>
          <div class="codex-stats-row">
            <span>HP: <strong>${b.baseHp}</strong></span>
            <span>ATK: <strong>${b.attack.toUpperCase()}</strong></span>
          </div>
        </div>
      `;
    }).join('');"""

    new_codex_render = """    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
    const archBadges = {
      spaceship: '🛸 KAPAL',
      mecha: '🤖 MECHA',
      monster: '👾 MONSTER',
      humanoid: '👤 ORANG',
      alien: '👁️ ALIEN'
    };

    grid.innerHTML = tierBosses.map(b => {
      const isBig = b.isBig;
      const badgeClass = isBig ? 'codex-badge-big' : 'codex-badge-mini';
      const tierText = isBig ? '👑 BIG' : '👾 MINI';
      const archText = archBadges[b.archetype] || '👾 ENEMY';
      return `
        <div class="codex-card" style="border-left: 3px solid ${b.color};">
          <div class="codex-card-top">
            <span class="codex-id" style="color: ${b.color};">#${String(b.id).padStart(3, '0')}</span>
            <div style="display: flex; gap: 4px;">
              <span class="codex-badge" style="background: rgba(255,255,255,0.08); color: #fff;">${archText}</span>
              <span class="codex-badge ${badgeClass}">${tierText}</span>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;">
            <img src="assets/images/boss_${b.archetype}.png" alt="${b.name}" style="width: 44px; height: 32px; object-fit: contain; filter: drop-shadow(0 0 4px ${b.color});">
            <div>
              <div class="codex-name">${b.name}</div>
              <div class="codex-title">${b.title}</div>
            </div>
          </div>
          <div class="codex-stats-row">
            <span>HP: <strong>${b.baseHp}</strong></span>
            <span>ATK: <strong>${b.attack.toUpperCase()}</strong></span>
          </div>
        </div>
      `;
    }).join('');"""

    if old_codex_render in src:
        src = src.replace(old_codex_render, new_codex_render)
        print("Updated renderBossCodex with thumbnails and 5 archetype tags")

    with open('js/game.js', 'w', encoding='utf-8') as f:
        f.write(src)

if __name__ == '__main__':
    update_game_js()
    print("All archetype integrations complete!")

