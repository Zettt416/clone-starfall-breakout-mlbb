import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_pixel_arcade_explosion():
    grid = 4
    frame_size = 128
    sheet_size = grid * frame_size  # 512 x 512
    scale = 2
    hires = frame_size * scale      # 256 x 256
    cx, cy = hires // 2, hires // 2
    
    sheet = Image.new('RGBA', (sheet_size, sheet_size), (0, 0, 0, 0))
    rng = random.Random(777)

    # 8 organic boiling lobes with varied angular distribution
    lobe_angles = [i * (2 * math.pi / 8) + rng.uniform(-0.16, 0.16) for i in range(8)]
    lobe_speeds = [rng.uniform(0.7, 1.3) for _ in range(8)]
    lobe_phases = [rng.uniform(0, math.pi * 2) for _ in range(8)]
    lobe_sizes  = [rng.uniform(0.85, 1.25) for _ in range(8)]

    # Flying hot sparks that launch outward irregularly
    sparks = []
    for _ in range(22):
        sparks.append({
            'angle': rng.uniform(0, math.pi * 2),
            'speed': rng.uniform(1.3, 2.5),
            'size': rng.uniform(2.2, 4.0),
            'dist_offset': rng.uniform(-14.0, 18.0) * scale,
            'color': rng.choice([
                (255, 255, 240),
                (255, 230, 80),
                (255, 140, 20),
                (255, 70, 10)
            ])
        })

    for f in range(16):
        t = f / 15.0  # progress 0.0 -> 1.0
        
        y, x = np.ogrid[:hires, :hires]
        dx = x - cx
        dy = y - cy
        
        # Overall explosion expansion envelope
        if t < 0.20:
            # Instantaneous blast ignition
            blast_scale = (t / 0.20) ** 0.5
            core_r = 10 * scale + blast_scale * 54 * scale
            cool_ratio = 0.0
            overall_alpha = 1.0
        elif t < 0.48:
            # Peak fireball explosion
            mid_t = (t - 0.20) / 0.28
            core_r = 64 * scale + mid_t * 22 * scale
            cool_ratio = mid_t * 0.38
            overall_alpha = 1.0
        else:
            # Billowing volcanic smoke & embers dissipation
            end_t = (t - 0.48) / 0.52
            core_r = 86 * scale + end_t * 12 * scale
            cool_ratio = 0.38 + end_t * 0.62
            overall_alpha = max(0.0, 1.0 - (end_t ** 1.35))

        inv_dist_field = np.zeros((hires, hires), dtype=np.float32)

        # 1. Central core lobe
        c_rad = max(4.0, core_r * 0.62)
        dist_c = np.sqrt(dx*dx + dy*dy)
        inv_c = np.clip(1.0 - (dist_c / c_rad), 0.0, 1.0)
        inv_dist_field = np.maximum(inv_dist_field, inv_c)

        # 2. Outer boiling lobes
        for i in range(8):
            ang = lobe_angles[i]
            spd = lobe_speeds[i]
            lsz = lobe_sizes[i]
            
            drift = spd * (t ** 0.75) * (core_r * 0.52)
            lx = cx + math.cos(ang) * drift
            ly = cy + math.sin(ang) * drift
            lr = max(4.0, lsz * core_r * (0.38 + 0.14 * math.sin(t * 7.0 + lobe_phases[i])))
            
            dist_l = np.sqrt((x - lx)**2 + (y - ly)**2)
            inv_l = np.clip(1.0 - (dist_l / lr), 0.0, 1.0)
            inv_dist_field = np.maximum(inv_dist_field, inv_l)

        # Harmonic turbulence
        theta = np.arctan2(dy, dx)
        wobble = 1.0 + 0.07 * np.sin(5 * theta + t * 5.0) + 0.05 * np.cos(7 * theta - t * 3.0)
        effective_val = inv_dist_field * wobble

        rgba = np.zeros((hires, hires, 4), dtype=np.uint8)
        inside = effective_val > 0.04
        val = effective_val[inside]
        
        heat = np.clip(val - cool_ratio * 0.88, 0.0, 1.0)
        
        r_arr = np.zeros_like(val, dtype=np.float32)
        g_arr = np.zeros_like(val, dtype=np.float32)
        b_arr = np.zeros_like(val, dtype=np.float32)
        a_arr = np.zeros_like(val, dtype=np.float32)

        # 1. Blinding White-Hot Plasma Core
        m_white = heat > 0.70
        r_arr[m_white] = 255
        g_arr[m_white] = 255
        b_arr[m_white] = 235 + (heat[m_white] - 0.70) * 60
        a_arr[m_white] = 255

        # 2. Brilliant Golden Lemon Yellow
        m_yellow = (heat > 0.42) & (~m_white)
        w_y = (heat[m_yellow] - 0.42) / (0.70 - 0.42)
        r_arr[m_yellow] = 255
        g_arr[m_yellow] = 205 + w_y * 50
        b_arr[m_yellow] = 35 + w_y * 190
        a_arr[m_yellow] = 255

        # 3. Vivid Fiery Orange
        m_orange = (heat > 0.16) & (~m_white) & (~m_yellow)
        w_o = (heat[m_orange] - 0.16) / (0.42 - 0.16)
        r_arr[m_orange] = 255
        g_arr[m_orange] = 95 + w_o * 110
        b_arr[m_orange] = 15 + w_o * 20
        a_arr[m_orange] = 250

        # 4. Deep Vermilion / Crimson Rim
        m_crimson = (heat > 0.05) & (~m_white) & (~m_yellow) & (~m_orange)
        w_c = (heat[m_crimson] - 0.05) / (0.16 - 0.05)
        r_arr[m_crimson] = 200 + w_c * 55
        g_arr[m_crimson] = 25 + w_c * 70
        b_arr[m_crimson] = 12
        a_arr[m_crimson] = 240

        # 5. Volcanic Charcoal Smoke & Ash
        m_edge = (~m_white) & (~m_yellow) & (~m_orange) & (~m_crimson)
        w_e = heat[m_edge] / 0.05
        if cool_ratio > 0.25:
            # Ash smoke: charcoal grey with slight obsidian purple undertone
            smoke_blend = min(1.0, (cool_ratio - 0.25) / 0.75)
            r_arr[m_edge] = (1.0 - smoke_blend) * 140 + smoke_blend * 56
            g_arr[m_edge] = (1.0 - smoke_blend) * 25 + smoke_blend * 46
            b_arr[m_edge] = (1.0 - smoke_blend) * 15 + smoke_blend * 58
            a_arr[m_edge] = 220 * w_e
        else:
            r_arr[m_edge] = 135 * w_e
            g_arr[m_edge] = 22 * w_e
            b_arr[m_edge] = 10
            a_arr[m_edge] = 220 * w_e

        a_arr = a_arr * overall_alpha
        
        rgba[inside, 0] = np.clip(r_arr, 0, 255).astype(np.uint8)
        rgba[inside, 1] = np.clip(g_arr, 0, 255).astype(np.uint8)
        rgba[inside, 2] = np.clip(b_arr, 0, 255).astype(np.uint8)
        rgba[inside, 3] = np.clip(a_arr, 0, 255).astype(np.uint8)

        frame = Image.fromarray(rgba, 'RGBA')

        # Starburst diamond flare for frame 0 and 1
        if f <= 1:
            fl_img = Image.new('RGBA', (hires, hires), (0, 0, 0, 0))
            f_draw = ImageDraw.Draw(fl_img)
            flare_len = (24 * scale) if f == 0 else (46 * scale)
            flare_w = max(2, int((5 if f == 0 else 7) * scale))
            pts_h = [(cx - flare_len, cy), (cx, cy - flare_w), (cx + flare_len, cy), (cx, cy + flare_w)]
            pts_v = [(cx - flare_w, cy), (cx, cy - flare_len), (cx + flare_w, cy), (cx, cy + flare_len)]
            f_draw.polygon(pts_h, fill=(255, 255, 255, 255))
            f_draw.polygon(pts_v, fill=(255, 255, 255, 255))
            frame = Image.alpha_composite(frame, fl_img)

        # Fast flying incendiary sparks/embers (launching ahead of the fireball)
        if 0.10 <= t <= 0.85:
            s_draw = ImageDraw.Draw(frame)
            sp_t = (t - 0.10) / 0.75
            sp_alpha = int(255 * max(0.0, 1.0 - (sp_t ** 1.3)))
            for sp in sparks:
                s_dist = (core_r * 0.7) + sp['dist_offset'] + sp['speed'] * sp_t * 54 * scale
                sx = cx + math.cos(sp['angle']) * s_dist
                sy = cy + math.sin(sp['angle']) * s_dist
                ssz = max(1.0, sp['size'] * scale * (1.0 - sp_t * 0.45))
                if 2 <= sx < hires - 2 and 2 <= sy < hires - 2:
                    col = sp['color'] + (sp_alpha,)
                    s_draw.ellipse([sx - ssz, sy - ssz, sx + ssz, sy + ssz], fill=col)

        # Downsample to 128x128
        frame_down = frame.resize((frame_size, frame_size), Image.Resampling.LANCZOS)
        
        col_idx = f % grid
        row_idx = f // grid
        sheet.paste(frame_down, (col_idx * frame_size, row_idx * frame_size), frame_down)

    sheet.save('assets/images/explosion_sheet.png', 'PNG')
    print("Arcade pixel explosion saved to assets/images/explosion_sheet.png")

    preview = Image.new('RGBA', (sheet_size, sheet_size), (10, 8, 20, 255))
    preview.alpha_composite(sheet)
    preview.save('test_explosion_preview.png', 'PNG')
    print("Preview saved to test_explosion_preview.png")

if __name__ == '__main__':
    generate_pixel_arcade_explosion()
