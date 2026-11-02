# -*- coding: utf-8 -*-

with open('js/game.js', 'r', encoding='utf-8') as f:
    src = f.read()

# Replace ctx.drawImage(sprite, -halfW, -halfH, w, h); in drawMinibossShip
old_draw_mini_call = """        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();
        return;"""

new_draw_mini_call = """        if (this.archetype === 'monster' || this.archetype === 'alien') {
          // Organic Spine Undulation / Tentacle Slither Mesh Slicer
          const slices = 22;
          const sliceW = w / slices;
          const srcSliceW = sprite.naturalWidth / slices;
          for (let i = 0; i < slices; i++) {
            const progress = i / (slices - 1);
            const amp = Math.pow(progress, 1.4) * (this.archetype === 'alien' ? 14 : 18);
            const waveY = Math.sin(this.time * 6.5 + i * 0.42) * amp;
            const waveScaleY = 1 + Math.cos(this.time * 6.5 + i * 0.42) * (progress * 0.08);

            const dx = -halfW + i * sliceW;
            const dy = -halfH * waveScaleY + waveY;
            const dw = sliceW + 0.6;
            const dh = h * waveScaleY;

            const sx = i * srcSliceW;
            const sy = 0;
            const sw = srcSliceW;
            const sh = sprite.naturalHeight;

            ctx.drawImage(sprite, sx, sy, sw, sh, dx, dy, dw, dh);
          }
        } else {
          ctx.drawImage(sprite, -halfW, -halfH, w, h);
        }
        ctx.restore();
        return;"""

# Do the same for drawBigbossShip
old_draw_big_call = """        ctx.drawImage(sprite, -halfW, -halfH, w, h);
        ctx.restore();

        // Forward Railgun Charging Flare at the cannon nose (-halfW * 0.48, 0)"""

new_draw_big_call = """        if (this.archetype === 'monster' || this.archetype === 'alien') {
          const slices = 22;
          const sliceW = w / slices;
          const srcSliceW = sprite.naturalWidth / slices;
          for (let i = 0; i < slices; i++) {
            const progress = i / (slices - 1);
            const amp = Math.pow(progress, 1.4) * (this.archetype === 'alien' ? 14 : 18);
            const waveY = Math.sin(this.time * 6.5 + i * 0.42) * amp;
            const waveScaleY = 1 + Math.cos(this.time * 6.5 + i * 0.42) * (progress * 0.08);

            const dx = -halfW + i * sliceW;
            const dy = -halfH * waveScaleY + waveY;
            const dw = sliceW + 0.6;
            const dh = h * waveScaleY;

            const sx = i * srcSliceW;
            const sy = 0;
            const sw = srcSliceW;
            const sh = sprite.naturalHeight;

            ctx.drawImage(sprite, sx, sy, sw, sh, dx, dy, dw, dh);
          }
        } else {
          ctx.drawImage(sprite, -halfW, -halfH, w, h);
        }
        ctx.restore();

        // Forward Railgun Charging Flare at the cannon nose (-halfW * 0.48, 0)"""

if old_draw_mini_call in src:
    src = src.replace(old_draw_mini_call, new_draw_mini_call)
    print("Added tentacle slither slicer to drawMinibossShip")

if old_draw_big_call in src:
    src = src.replace(old_draw_big_call, new_draw_big_call)
    print("Added tentacle slither slicer to drawBigbossShip")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(src)

print("Tentacle animation patch complete!")

