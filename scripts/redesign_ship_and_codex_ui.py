import sys

# ==============================================================================
# 1. PATCH INDEX.HTML
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_ship_carousel = '''        <!-- Character / Ship Selection Carousel -->
        <div class="ship-select-container">
          <div class="ship-carousel">
            <button type="button" id="btnShipPrev" class="ship-nav-btn" aria-label="Pesawat Sebelumnya">◀</button>
            <div id="shipCardActive" class="ship-card">
              <div class="ship-card-avatar-wrap">
                <img id="shipAvatarImg" src="assets/images/ship_stella_nova.png" alt="Ship" class="ship-avatar-main">
                <span id="shipClassBadge" class="ship-class-badge badge-interceptor">INTERCEPTOR</span>
              </div>
              <div class="ship-card-details">
                <div class="ship-name-row">
                  <span id="shipNameText" class="ship-name">STELLA NOVA</span>
                </div>
                <div class="ship-stats-row">
                  <span class="stat-badge">⚡ SPD <b id="statSpeed">320</b></span>
                  <span class="stat-badge">💥 WEAPON <b id="statPower">TWIN CANNON</b></span>
                  <span class="stat-badge">❤️ HP <b id="statHp">STANDARD</b></span>
                </div>
                <div class="ship-skills-row">
                  <div class="ship-skill-chip survive-chip">
                    <span class="skill-type-tag">🛡️ SURVIVE [C]:</span>
                    <span id="shipSurviveDesc" class="skill-name-val">COSMIC AEGIS SHIELD</span>
                  </div>
                  <div class="ship-skill-chip ult-chip">
                    <span class="skill-type-tag">⭐ ULT [SPACE]:</span>
                    <span id="shipUltDesc" class="skill-name-val">STELLAR BLASTER BEAM</span>
                  </div>
                </div>
              </div>
            </div>
            <button type="button" id="btnShipNext" class="ship-nav-btn" aria-label="Pesawat Berikutnya">▶</button>
          </div>
        </div>'''

new_ship_carousel = '''        <!-- Character / Ship Selection Carousel - Streamlined & Elegant -->
        <div class="ship-select-container">
          <div class="ship-carousel">
            <button type="button" id="btnShipPrev" class="ship-nav-btn" aria-label="Pesawat Sebelumnya">◀</button>
            <div id="shipCardActive" class="ship-card">
              <div class="ship-card-avatar-wrap">
                <img id="shipAvatarImg" src="assets/images/ship_stella_nova.png" alt="Ship" class="ship-avatar-main">
                <span id="shipClassBadge" class="ship-class-badge badge-interceptor">INTERCEPTOR</span>
              </div>
              <div class="ship-card-details">
                <div class="ship-name-row">
                  <span id="shipNameText" class="ship-name">STELLA NOVA</span>
                </div>
                <div id="shipPlaystyleDesc" class="ship-playstyle">Lincah & Seimbang • Tembakan Plasma Cepat</div>
                <div class="ship-skills-row">
                  <span class="ship-skill-chip survive-chip">
                    <span class="skill-icon">🛡️</span>
                    <span id="shipSurviveShort">Cosmic Aegis</span>
                  </span>
                  <span class="ship-skill-chip ult-chip">
                    <span class="skill-icon">⭐</span>
                    <span id="shipUltShort">Stellar Blaster</span>
                  </span>
                </div>
              </div>
            </div>
            <button type="button" id="btnShipNext" class="ship-nav-btn" aria-label="Pesawat Berikutnya">▶</button>
          </div>
        </div>'''

assert old_ship_carousel in html, "old_ship_carousel not found in index.html"
html = html.replace(old_ship_carousel, new_ship_carousel, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("1. Successfully updated index.html!")

# ==============================================================================
# 2. PATCH JS/GAME.JS
# ==============================================================================
with open('js/game.js', 'r', encoding='utf-8') as f:
    game_js = f.read()

# 2.1 Update SHIPS_CONFIG
old_ships_cfg = '''  // Starship / Character Roster (Unique Real Arcade Sprites, Dedicated Power-Ups & Skills)
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

new_ships_cfg = '''  // Starship / Character Roster (Streamlined, Clear Identity, Real Arcade Sprites)
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
      descId: 'Lincah & Seimbang • Tembakan Plasma Cepat',
      descEn: 'Agile & Balanced • Rapid Twin Plasma',
      surviveShort: 'Cosmic Aegis',
      ultShort: 'Stellar Blaster',
      surviveName: 'COSMIC SHIELD',
      surviveDesc: 'COSMIC AEGIS SHIELD (3D FORCEFIELD)',
      ultName: 'STELLAR BLASTER',
      ultDesc: 'STELLAR BLASTER HORIZONTAL BEAM',
      extraLives: 0,
      uniquePowerups: ['HYPERDRIVE', 'PLASMA_SPREAD']
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
      descId: 'Armor Berat (+1 Nyawa) • Meriam Flak Area',
      descEn: 'Heavy Armor (+1 Life) • Area Flak Cannon',
      surviveShort: 'Nanite Barrier',
      ultShort: 'Cluster Barrage',
      surviveName: 'NANITE MATRIX',
      surviveDesc: 'NANITE PHASE BARRIER (EMP PULSE CLEAR)',
      ultName: 'CLUSTER BARRAGE',
      ultDesc: 'HEAVY CLUSTER BARRAGE BOMBS',
      extraLives: 1,
      uniquePowerups: ['HEAVY_FLAK', 'TESLA_COIL']
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
      descId: 'Kecepatan Ekstrem • Jarum Laser Tembus',
      descEn: 'Extreme Speed • Piercing Void Needles',
      surviveShort: 'Chrono Warp (Slow-Mo)',
      ultShort: 'Singularity Rift',
      surviveName: 'CHRONO WARP',
      surviveDesc: 'TEMPORAL WARP (70% TIME DILATION)',
      ultName: 'SINGULARITY RIFT',
      ultDesc: 'SINGULARITY VORTEX FIELD',
      extraLives: 0,
      uniquePowerups: ['QUANTUM_CLONES', 'VOID_NEEDLE']
    }
  };'''

assert old_ships_cfg in game_js, "old_ships_cfg not found in game.js"
game_js = game_js.replace(old_ships_cfg, new_ships_cfg, 1)

# 2.2 Update updateShipCardUI
old_update_ship_card = '''  function updateShipCardUI() {
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
    if (shipAvatarImg) {
      if (conf.avatarSrc) {
        shipAvatarImg.src = conf.avatarSrc;
        shipAvatarImg.style.filter = 'none';
      } else {
        shipAvatarImg.style.filter = conf.filter;
      }
    }

    const btnTouchSurvive = document.getElementById('btnTouchSurvive');
    if (btnTouchSurvive) {
      btnTouchSurvive.title = `Survive Skill: ${conf.surviveName} [C]`;
    }
  }'''

new_update_ship_card = '''  function updateShipCardUI() {
    const shipId = state.selectedShip || 'stella_nova';
    const conf = SHIPS_CONFIG[shipId] || SHIPS_CONFIG.stella_nova;

    const shipAvatarImg = document.getElementById('shipAvatarImg');
    const shipClassBadge = document.getElementById('shipClassBadge');
    const shipNameText = document.getElementById('shipNameText');
    const shipPlaystyleDesc = document.getElementById('shipPlaystyleDesc');
    const shipSurviveShort = document.getElementById('shipSurviveShort');
    const shipUltShort = document.getElementById('shipUltShort');

    if (shipNameText) shipNameText.textContent = conf.name;
    if (shipClassBadge) {
      shipClassBadge.className = 'ship-class-badge ' + conf.badgeClass;
      shipClassBadge.textContent = conf.class;
    }
    if (shipPlaystyleDesc) {
      shipPlaystyleDesc.textContent = (state.lang === 'id' ? conf.descId : conf.descEn) || conf.descId;
    }
    if (shipSurviveShort) shipSurviveShort.textContent = conf.surviveShort || conf.surviveName;
    if (shipUltShort) shipUltShort.textContent = conf.ultShort || conf.ultName;

    if (shipAvatarImg) {
      if (conf.avatarSrc) {
        shipAvatarImg.src = conf.avatarSrc;
        shipAvatarImg.style.filter = 'none';
      }
    }

    const btnTouchSurvive = document.getElementById('btnTouchSurvive');
    if (btnTouchSurvive) {
      btnTouchSurvive.title = `Survive Skill: ${conf.surviveShort || conf.surviveName} [C]`;
    }
  }'''

assert old_update_ship_card in game_js, "old_update_ship_card not found in game.js"
game_js = game_js.replace(old_update_ship_card, new_update_ship_card, 1)

# 2.3 Call updateShipCardUI in applyTranslations
old_apply_trans_end = '''    updateHudDifficultyBadge();
  }'''

new_apply_trans_end = '''    updateHudDifficultyBadge();
    updateShipCardUI();
  }'''

assert old_apply_trans_end in game_js, "old_apply_trans_end not found"
game_js = game_js.replace(old_apply_trans_end, new_apply_trans_end, 1)

# 2.4 Update renderBossCodex with real images and clean 2-column card markup
old_render_codex = '''  function renderBossCodex(tier) {
    activeCodexTier = tier;
    const grid = document.getElementById('bossCodexGrid');
    if (!grid || !window.BOSS_CATALOG) return;

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tier === tier);
    });

    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
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
    }).join('');
  }'''

new_render_codex = '''  // Map Boss Catalog entries to real 32-bit transparent arcade PNGs
  function getBossCodexImage(b) {
    const bName = b.name || '';
    if (b.isBig) {
      if (bName.includes('Annihilator') || bName.includes('Dreadnought') || bName.includes('Apex') || bName.includes('Flagship') || bName.includes('Warlord') || bName.includes('Carrier') || bName.includes('Bastion')) {
        return 'assets/images/boss_crimson_annihilator.png';
      }
      if (b.archetype === 'monster' || bName.includes('Singularity') || bName.includes('Leviathan') || bName.includes('Maw') || bName.includes('Goliath')) {
        return 'assets/images/boss_void_singularity.png';
      }
      if (b.archetype === 'humanoid' || bName.includes('Astraea') || bName.includes('Archon') || bName.includes('Ex-Machina') || bName.includes('Zephyr') || bName.includes('Valkyrie')) {
        return 'assets/images/boss_astraea_archon.png';
      }
    }
    const archMap = {
      spaceship: 'assets/images/boss_spaceship_dreadnought.png',
      mecha: 'assets/images/boss_mecha_titan.png',
      monster: 'assets/images/boss_alien_leviathan.png',
      humanoid: 'assets/images/boss_humanoid_valkyrie.png',
      alien: 'assets/images/boss_eldritch_eye.png'
    };
    return archMap[b.archetype] || 'assets/images/boss_alien_leviathan.png';
  }

  const codexAtkNames = {
    plasma_twin: 'Twin Plasma',
    plasma_burst: 'Plasma Burst',
    curtain_fan: 'Curtain Fan',
    railgun_laser: 'Railgun Laser',
    railgun_heavy: 'Heavy Railgun',
    spiral_danmaku: 'Spiral Danmaku',
    escort_shield: 'Escort Barrier',
    homing_missiles: 'Homing Missiles',
    void_vortex: 'Void Vortex',
    quantum_lasers: 'Quantum Laser'
  };

  function renderBossCodex(tier) {
    activeCodexTier = tier;
    const grid = document.getElementById('bossCodexGrid');
    if (!grid || !window.BOSS_CATALOG) return;

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tier === tier);
    });

    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
    const archBadges = {
      spaceship: '🛸 KAPAL',
      mecha: '🤖 MECHA',
      monster: '👾 MONSTER',
      humanoid: '👤 VALKYRIE',
      alien: '👁️ ALIEN'
    };

    grid.innerHTML = tierBosses.map(b => {
      const isBig = b.isBig;
      const tierText = isBig ? '👑 BIG BOSS' : '👾 MINIBOSS';
      const rankClass = isBig ? 'big' : 'mini';
      const archText = archBadges[b.archetype] || '👾 ENEMY';
      const imgSrc = getBossCodexImage(b);
      const atkText = codexAtkNames[b.attack] || b.attack.replace(/_/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase());

      return `
        <div class="codex-card" style="border-left: 4px solid ${b.color};">
          <div class="codex-card-top">
            <div class="codex-id-wrap">
              <span class="codex-id" style="color: ${b.color};">#${String(b.id).padStart(3, '0')}</span>
              <span class="codex-rank-pill ${rankClass}">${tierText}</span>
            </div>
            <span class="codex-arch-tag">${archText}</span>
          </div>
          <div class="codex-card-body">
            <div class="codex-sprite-box" style="background: radial-gradient(circle, ${b.color}24 0%, rgba(10,14,28,0.85) 75%); border-color: ${b.color}55;">
              <img src="${imgSrc}" alt="${b.name}" class="codex-sprite-img">
            </div>
            <div class="codex-info-col">
              <div class="codex-name">${b.name}</div>
              <div class="codex-title">${b.title}</div>
              <div class="codex-stats-row">
                <span class="codex-stat-pill"><span class="stat-icon">❤️</span> <strong>${b.baseHp} HP</strong></span>
                <span class="codex-stat-pill"><span class="stat-icon">⚔️</span> <strong>${atkText}</strong></span>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }'''

assert old_render_codex in game_js, "old_render_codex not found in game.js"
game_js = game_js.replace(old_render_codex, new_render_codex, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(game_js)
print("2. Successfully updated js/game.js!")

# ==============================================================================
# 3. PATCH CSS/STYLE.CSS
# ==============================================================================
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 3.1 Replace Ship Card Styles
old_ship_card_css = '''.ship-select-container {
  margin: 4px 0 8px 0;
  width: 100%;
  max-width: 620px;
}

.ship-carousel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.ship-nav-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--neon-cyan);
  font-size: 16px;
  width: 36px;
  height: 64px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  user-select: none;
}

.ship-nav-btn:hover {
  background: rgba(0, 243, 255, 0.25);
  border-color: var(--neon-cyan);
  transform: scale(1.06);
}

.ship-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(14, 18, 36, 0.9);
  border: 1px solid rgba(0, 243, 255, 0.35);
  border-radius: 14px;
  padding: 8px 14px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(0, 243, 255, 0.08);
  transition: all 0.25s ease;
}

.ship-card-avatar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 64px;
}

.ship-avatar-main {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: 2px solid var(--neon-cyan);
  background: radial-gradient(circle, rgba(0, 243, 255, 0.25) 0%, #000 80%);
  object-fit: contain;
  padding: 3px;
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.4);
}

.ship-class-badge {
  font-family: var(--font-retro);
  font-size: 7px;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  background: rgba(0, 243, 255, 0.2);
  color: var(--neon-cyan);
  border: 1px solid rgba(0, 243, 255, 0.4);
}

.ship-card-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  text-align: left;
}

.ship-name-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ship-name {
  font-family: var(--font-retro);
  font-size: 11px;
  color: #fff;
  letter-spacing: 1px;
  text-shadow: 0 0 8px rgba(0, 243, 255, 0.6);
}

.ship-stats-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.stat-badge {
  font-family: var(--font-main);
  font-size: 10px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.75);
  background: rgba(255, 255, 255, 0.06);
  padding: 2px 7px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-badge b {
  color: var(--neon-yellow);
}

.ship-skills-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.ship-skill-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-main);
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
}

.survive-chip {
  background: rgba(0, 243, 255, 0.12);
  color: var(--neon-cyan);
  border: 1px solid rgba(0, 243, 255, 0.3);
}

.ult-chip {
  background: rgba(255, 42, 133, 0.12);
  color: var(--neon-pink);
  border: 1px solid rgba(255, 42, 133, 0.3);
}'''

new_ship_card_css = '''.ship-select-container {
  margin: 6px 0 10px 0;
  width: 100%;
  max-width: 580px;
}

.ship-carousel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.ship-nav-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--neon-cyan);
  font-size: 15px;
  width: 38px;
  height: 68px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  user-select: none;
}

.ship-nav-btn:hover {
  background: rgba(0, 243, 255, 0.2);
  border-color: var(--neon-cyan);
  transform: scale(1.05);
}

.ship-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16px;
  background: linear-gradient(135deg, rgba(16, 22, 44, 0.95), rgba(9, 13, 28, 0.95));
  border: 1px solid rgba(0, 243, 255, 0.28);
  border-radius: 14px;
  padding: 10px 18px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.25s ease;
}

.ship-card-avatar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 60px;
}

.ship-avatar-main {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid var(--neon-cyan);
  background: radial-gradient(circle, rgba(0, 243, 255, 0.22) 0%, rgba(5, 8, 18, 0.9) 75%);
  object-fit: contain;
  padding: 4px;
  box-shadow: 0 0 14px rgba(0, 243, 255, 0.35);
  transition: transform 0.2s ease;
}

.ship-class-badge {
  font-family: var(--font-retro);
  font-size: 7.5px;
  padding: 3px 7px;
  border-radius: 4px;
  letter-spacing: 0.6px;
  background: rgba(0, 243, 255, 0.15);
  color: var(--neon-cyan);
  border: 1px solid rgba(0, 243, 255, 0.35);
}

.ship-card-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
  text-align: left;
}

.ship-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ship-name {
  font-family: var(--font-retro);
  font-size: 13px;
  color: #fff;
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
}

.ship-playstyle {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 500;
  letter-spacing: 0.3px;
  line-height: 1.3;
}

.ship-skills-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 2px;
}

.ship-skill-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10.5px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 6px;
  letter-spacing: 0.3px;
}

.survive-chip {
  background: rgba(0, 243, 255, 0.1);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.28);
}

.ult-chip {
  background: rgba(255, 42, 133, 0.1);
  color: #f472b6;
  border: 1px solid rgba(244, 114, 182, 0.28);
}'''

assert old_ship_card_css in css, "old_ship_card_css not found"
css = css.replace(old_ship_card_css, new_ship_card_css, 1)

# 3.2 Replace Kodex Grid & Card Styles
old_kodex_css = '''.modal-codex-card {
  max-width: 820px;
  width: 95%;
}

.codex-tabs-row {
  display: flex;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(0, 0, 0, 0.4);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
}

.codex-tab-btn {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 8px;
  padding: 8px 12px;
  background: #140c24;
  color: #8b80a5;
  border: 1px solid #3d2c60;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.codex-tab-btn.active, .codex-tab-btn:hover {
  background: #2b144d;
  color: #00f3ff;
  border-color: #00f3ff;
  box-shadow: 0 0 8px rgba(0, 243, 255, 0.35);
}

.codex-scroll {
  max-height: 420px;
}

.codex-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 12px;
  padding: 12px;
}

.codex-card {
  background: rgba(18, 12, 34, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.15s, border-color 0.15s;
}

.codex-card:hover {
  transform: translateY(-2px);
  border-color: #00f3ff;
  background: rgba(28, 18, 54, 0.95);
}

.codex-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.codex-id {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 9px;
  font-weight: bold;
}

.codex-badge {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 7px;
  padding: 2px 6px;
  border-radius: 3px;
  letter-spacing: 0.5px;
}

.codex-badge-big {
  background: rgba(255, 0, 85, 0.2);
  color: #ff0055;
  border: 1px solid #ff0055;
}

.codex-badge-mini {
  background: rgba(0, 243, 255, 0.18);
  color: #00f3ff;
  border: 1px solid #00f3ff;
}

.codex-name {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 10px;
  color: #ffffff;
  margin-top: 2px;
}

.codex-title {
  font-size: 11px;
  color: #a89cb9;
  line-height: 1.3;
}

.codex-stats-row {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px dashed rgba(255, 255, 255, 0.08);
  color: #ffd000;
}'''

new_kodex_css = '''.modal-codex-card {
  max-width: 840px;
  width: 95%;
  max-height: 88vh;
}

.codex-tabs-row {
  display: flex;
  gap: 8px;
  padding: 12px 18px;
  background: rgba(0, 0, 0, 0.45);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-wrap: wrap;
}

.codex-tab-btn {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 8px;
  padding: 8px 14px;
  background: #140c24;
  color: #8b80a5;
  border: 1px solid #3d2c60;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.codex-tab-btn.active, .codex-tab-btn:hover {
  background: #2b144d;
  color: #00f3ff;
  border-color: #00f3ff;
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.35);
}

.codex-scroll {
  max-height: 440px;
  padding: 6px 14px 14px 14px;
}

.codex-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 12px;
  padding: 8px 4px;
}

.codex-card {
  background: linear-gradient(135deg, rgba(17, 24, 46, 0.88), rgba(11, 15, 30, 0.92));
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
}

.codex-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
  border-color: rgba(0, 243, 255, 0.5);
}

.codex-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.codex-id-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.codex-id {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 9px;
  letter-spacing: 0.5px;
}

.codex-rank-pill {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 7px;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.4px;
}

.codex-rank-pill.big {
  background: rgba(255, 0, 85, 0.18);
  color: #ff0055;
  border: 1px solid rgba(255, 0, 85, 0.45);
}

.codex-rank-pill.mini {
  background: rgba(0, 243, 255, 0.14);
  color: #00f3ff;
  border: 1px solid rgba(0, 243, 255, 0.4);
}

.codex-arch-tag {
  font-size: 10px;
  color: #94a3b8;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 7px;
  border-radius: 4px;
}

.codex-card-body {
  display: flex;
  align-items: center;
  gap: 12px;
}

.codex-sprite-box {
  width: 52px;
  height: 52px;
  flex-shrink: 0;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  background: rgba(0, 0, 0, 0.35);
}

.codex-sprite-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 6px rgba(0, 243, 255, 0.4));
}

.codex-info-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.codex-name {
  font-family: 'Press Start 2P', sans-serif;
  font-size: 10px;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.codex-title {
  font-size: 11px;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
}

.codex-stats-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 2px;
}

.codex-stat-pill {
  font-size: 10px;
  color: #ffd000;
  background: rgba(255, 208, 0, 0.08);
  border: 1px solid rgba(255, 208, 0, 0.22);
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.codex-stat-pill strong {
  font-weight: 700;
}'''

assert old_kodex_css in css, "old_kodex_css not found"
css = css.replace(old_kodex_css, new_kodex_css, 1)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("3. Successfully updated css/style.css!")

