# -*- coding: utf-8 -*-

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Add btnBossCodex button
    old_btn_row = """        <div class="screen-btn-row">
          <button id="btnStart" class="pixel-btn play-btn" data-i18n="btnStart">MULAI MAIN</button>
          <button id="btnLeaderboardStart" class="pixel-btn leaderboard-btn" data-i18n="btnLeaderboard">🏆 TOP PILOT</button>
          <button id="btnHowToPlayStart" class="pixel-btn help-btn" data-i18n="btnHowToPlay">❓ CARA MAIN</button>
        </div>"""

    new_btn_row = """        <div class="screen-btn-row">
          <button id="btnStart" class="pixel-btn play-btn" data-i18n="btnStart">MULAI MAIN</button>
          <button id="btnLeaderboardStart" class="pixel-btn leaderboard-btn" data-i18n="btnLeaderboard">🏆 TOP PILOT</button>
          <button id="btnBossCodex" class="pixel-btn codex-btn" title="Katalog 100 Bos">👾 KODEX BOS (100)</button>
          <button id="btnHowToPlayStart" class="pixel-btn help-btn" data-i18n="btnHowToPlay">❓ CARA MAIN</button>
        </div>"""

    if old_btn_row in src:
        src = src.replace(old_btn_row, new_btn_row)
        print("Added btnBossCodex to index.html")
    else:
        # Check if emojis are different in file
        idx = src.find('<button id="btnStart"')
        end_idx = src.find('</div>', idx)
        if idx != -1 and end_idx != -1:
            chunk = src[idx:end_idx]
            if 'btnBossCodex' not in chunk:
                replaced_chunk = chunk.replace('</button>', '</button>\n          <button id="btnBossCodex" class="pixel-btn codex-btn" title="Katalog 100 Bos">👾 KODEX BOS (100)</button>', 2)
                # Just replace once after leaderboard
                src = src[:idx] + chunk.replace('id="btnHowToPlayStart"', 'id="btnBossCodex" class="pixel-btn codex-btn" title="Katalog 100 Bos">👾 KODEX BOS (100)</button>\n          <button id="btnHowToPlayStart"') + src[end_idx:]
                print("Added btnBossCodex via fallback match")

    # 2. Add bossCodexModal
    codex_modal_html = """
    <!-- Boss Codex Modal (100 Bosses Catalog Viewer) -->
    <div id="bossCodexModal" class="modal-overlay hidden">
      <div class="modal-card modal-codex-card">
        <div class="modal-header">
          <div class="modal-title-group">
            <span class="modal-tag">👾 ARCHIVE // STARFALL BREAKOUT</span>
            <h2 class="modal-title">KODEX 100 BOS & MINIBOS</h2>
          </div>
          <button id="btnCloseBossCodex" class="modal-close-btn" aria-label="Tutup">✕</button>
        </div>
        <div class="codex-tabs-row">
          <button type="button" class="codex-tab-btn active" data-tier="easy">EASY (#001–#025)</button>
          <button type="button" class="codex-tab-btn" data-tier="normal">NORMAL (#026–#050)</button>
          <button type="button" class="codex-tab-btn" data-tier="hard">HARD (#051–#075)</button>
          <button type="button" class="codex-tab-btn" data-tier="hardcorez">HARDCOREZ (#076–#100)</button>
        </div>
        <div id="bossCodexScroll" class="modal-body-scroll codex-scroll">
          <div id="bossCodexGrid" class="codex-grid">
            <!-- Dynamically populated 25 cards per tier -->
          </div>
        </div>
        <div class="modal-footer">
          <button id="btnCloseBossCodexBottom" class="pixel-btn small-btn">TUTUP KODEX ✕</button>
        </div>
      </div>
    </div>
"""

    how_to_play_end = 'id="btnCloseHowToPlayBottom"'
    idx_close = src.find(how_to_play_end)
    if idx_close != -1:
        modal_end = src.find('</div>\n    </div>', idx_close)
        if modal_end != -1:
            insert_pos = modal_end + len('</div>\n    </div>')
            if 'bossCodexModal' not in src:
                src = src[:insert_pos] + codex_modal_html + src[insert_pos:]
                print("Inserted bossCodexModal in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(src)

def update_css():
    with open('css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    if '.codex-btn' not in css:
        codex_css = """
/* Codex 100 Bosses Modal & Cards */
.codex-btn {
  background: linear-gradient(180deg, #1f0836, #0e041c);
  border-color: #b844ff;
  color: #ff88ff;
  box-shadow: 0 4px 0 #4a0f73, 0 0 10px rgba(184, 68, 255, 0.35);
}
.codex-btn:hover {
  background: linear-gradient(180deg, #300c54, #180630);
  border-color: #e088ff;
  box-shadow: 0 4px 0 #6815a3, 0 0 16px rgba(224, 136, 255, 0.55);
}

.modal-codex-card {
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
}
"""
        css += codex_css
        with open('css/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Added codex css")

def update_game_js():
    with open('js/game.js', 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Add hexToHue and hue filtering in Boss.drawMinibossShip and drawBigbossShip
    old_miniboss_draw = """        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();"""

    new_miniboss_draw = """        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#00f3ff');
          const hueDiff = (targetHue - 185 + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.4)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();"""

    if old_miniboss_draw in src:
        src = src.replace(old_miniboss_draw, new_miniboss_draw)
        print("Updated drawMinibossShip hue filter")

    old_bigboss_draw = """        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();"""

    new_bigboss_draw = """        ctx.save();
        ctx.shadowBlur = 0;
        if (this.flashTimer > 0) {
          ctx.filter = 'brightness(3.2) contrast(1.15)';
        } else {
          const targetHue = hexToHue(this.color || '#ffd000');
          const hueDiff = (targetHue - 45 + 360) % 360;
          ctx.filter = `hue-rotate(${hueDiff}deg) saturate(1.3)`;
        }
        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();"""

    if old_bigboss_draw in src:
        src = src.replace(old_bigboss_draw, new_bigboss_draw)
        print("Updated drawBigbossShip hue filter")

    # 2. Add hexToHue definition before Boss
    if 'function hexToHue' not in src:
        hex_func = """  // Helper to convert hex color to HSL hue degrees for Canvas ctx.filter
  function hexToHue(hex) {
    if (!hex || hex[0] !== '#') return 0;
    const r = parseInt(hex.slice(1,3), 16) / 255;
    const g = parseInt(hex.slice(3,5), 16) / 255;
    const b = parseInt(hex.slice(5,7), 16) / 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0;
    if (max === min) h = 0;
    else if (max === r) h = (60 * ((g - b) / (max - min)) + 360) % 360;
    else if (max === g) h = (60 * ((b - r) / (max - min)) + 120) % 360;
    else h = (60 * ((r - g) / (max - min)) + 240) % 360;
    return Math.round(h);
  }
"""
        src = src.replace('  class Boss {', hex_func + '\n  class Boss {')
        print("Added hexToHue function")

    # 3. Add Boss Codex Modal functions
    codex_code = """
  // --- Boss Codex (100 Bosses Catalog Modal) ---
  let activeCodexTier = 'easy';

  function openBossCodex() {
    const modal = document.getElementById('bossCodexModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    renderBossCodex(activeCodexTier);
    if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
  }

  function closeBossCodex() {
    const modal = document.getElementById('bossCodexModal');
    if (modal) modal.classList.add('hidden');
  }

  function renderBossCodex(tier) {
    activeCodexTier = tier;
    const grid = document.getElementById('bossCodexGrid');
    if (!grid || !window.BOSS_CATALOG) return;

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tier === tier);
    });

    const tierBosses = window.BOSS_CATALOG.filter(b => b.tier === tier);
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
    }).join('');
  }
"""

    if 'function openBossCodex' not in src:
        src = src.replace('  function openLeaderboard() {', codex_code + '\n  function openLeaderboard() {')
        print("Added Boss Codex functions")

    # 4. Bind Boss Codex buttons in setupInputs
    old_help_bind = "if (btnHowToPlayStart) btnHowToPlayStart.addEventListener('click', openHowToPlay);"
    new_help_bind = """if (btnHowToPlayStart) btnHowToPlayStart.addEventListener('click', openHowToPlay);
    const btnBossCodex = document.getElementById('btnBossCodex');
    if (btnBossCodex) btnBossCodex.addEventListener('click', openBossCodex);
    const btnCloseBossCodex = document.getElementById('btnCloseBossCodex');
    if (btnCloseBossCodex) btnCloseBossCodex.addEventListener('click', closeBossCodex);
    const btnCloseBossCodexBottom = document.getElementById('btnCloseBossCodexBottom');
    if (btnCloseBossCodexBottom) btnCloseBossCodexBottom.addEventListener('click', closeBossCodex);

    document.querySelectorAll('.codex-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tier = btn.dataset.tier;
        if (tier) {
          renderBossCodex(tier);
          if (window.soundFx && window.soundFx.playPowerup) window.soundFx.playPowerup();
        }
      });
    });"""

    if old_help_bind in src and 'btnBossCodex' not in src:
        src = src.replace(old_help_bind, new_help_bind)
        print("Bound Boss Codex event listeners")

    # 5. Add ?view=codex preview param
    if "viewParam === 'codex'" not in src:
        src = src.replace("viewParam === 'leaderboard'", "viewParam === 'codex') {\n        if (startScreen) startScreen.classList.remove('active');\n        openBossCodex();\n      } else if (viewParam === 'leaderboard'")
        print("Added ?view=codex test parameter")

    with open('js/game.js', 'w', encoding='utf-8') as f:
        f.write(src)

if __name__ == '__main__':
    update_index_html()
    update_css()
    update_game_js()
    print("All codex updates finished!")

