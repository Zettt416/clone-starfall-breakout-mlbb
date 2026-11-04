import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

telegraph_code = '''    drawSkillTelegraph(ctx) {
      const bossX = this.currentX || this.x;
      const targetY = this.skillTargetY || this.y;
      const pullProgress = 1 - Math.max(0, this.castSkillTimer / this.castSkillDuration);

      ctx.save();

      // 1. Universal Telegraphed Danger Aiming Laser
      ctx.strokeStyle = this.color || '#ff0055';
      ctx.lineWidth = 1.8 + Math.sin(this.time * 20) * 0.8;
      ctx.shadowColor = this.color || '#ff0055';
      ctx.shadowBlur = 10;
      ctx.setLineDash([10, 6]);
      ctx.lineDashOffset = -this.time * 60;
      ctx.beginPath();
      ctx.moveTo(bossX - 40, targetY);
      ctx.lineTo(0, targetY);
      ctx.stroke();
      ctx.setLineDash([]);

      // 2. Archetype-specific Telegraphed Charge Graphics
      if (this.archetype === 'humanoid') {
        // Celestial Rune Circle (8-pointed sacred glyph)
        const runeX = bossX - 50;
        const runeR = 34 + pullProgress * 18;
        ctx.save();
        ctx.translate(runeX, targetY);
        ctx.rotate(this.time * 5.0);

        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.arc(0, 0, runeR, 0, Math.PI * 2);
        ctx.stroke();

        for (let p = 0; p < 8; p++) {
          const a = (p / 8) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * (runeR * 0.4), Math.sin(a) * (runeR * 0.4));
          ctx.lineTo(Math.cos(a) * runeR, Math.sin(a) * runeR);
          ctx.stroke();
        }
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // Digital Targeting Lock-On Reticle at Player Position
        const reticleX = player ? player.x : 100;
        const reticleR = 24 * (1.6 - pullProgress * 0.6);
        ctx.strokeStyle = '#ff0044';
        ctx.lineWidth = 2.0;
        ctx.strokeRect(reticleX - reticleR, targetY - reticleR, reticleR * 2, reticleR * 2);

        // Reticle crosshair
        ctx.beginPath();
        ctx.moveTo(reticleX - reticleR - 8, targetY);
        ctx.lineTo(reticleX + reticleR + 8, targetY);
        ctx.moveTo(reticleX, targetY - reticleR - 8);
        ctx.lineTo(reticleX, targetY + reticleR + 8);
        ctx.stroke();

        // Lock text
        ctx.fillStyle = '#ff0044';
        ctx.font = 'bold 10px monospace';
        ctx.fillText(`TARGET LOCK ${Math.floor(pullProgress * 100)}%`, reticleX - 35, targetY - reticleR - 4);

      } else if (this.archetype === 'alien') {
        // Psychic Sonar Ripples Expanding Outward
        for (let r = 1; r <= 3; r++) {
          const ripplePhase = (this.time * 4 + r * 0.8) % 3;
          const rippleR = ripplePhase * 45;
          ctx.strokeStyle = `${this.color || '#b844ff'}${Math.floor((1 - ripplePhase / 3) * 255).toString(16).padStart(2, '0')}`;
          ctx.lineWidth = 2.2;
          ctx.beginPath();
          ctx.arc(bossX - 30, targetY, rippleR, Math.PI * 0.5, Math.PI * 1.5);
          ctx.stroke();
        }
      }

      ctx.restore();
    }

    destroy() {'''

assert '    destroy() {' in text, 'destroy() not found!'
text = text.replace('    destroy() {', telegraph_code, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added drawSkillTelegraph successfully!')

