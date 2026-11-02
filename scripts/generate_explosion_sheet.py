import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math, os

def create_explosion_spritesheet():
    # 4x4 grid, 128x128 per frame -> 512x512 spritesheet
    frame_size = 128
    grid = 4
    sheet_size = frame_size * grid
    sheet = Image.new('RGBA', (sheet_size, sheet_size), (0, 0, 0, 0))

    np.random.seed(2026)

    Y, X = np.ogrid[:frame_size, :frame_size]
    center = (frame_size - 1) / 2.0
    dist_from_center = np.sqrt((X - center)**2 + (Y - center)**2)
    angles = np.arctan2(Y - center, X - center)

    for idx in range(16):
        t = idx / 15.0  # 0.0 -> 1.0 progress
        col = idx % grid
        row = idx // grid

        # Core radius expansion curve (clamped safely within frame_size/2 - 6 = 58px)
        max_safe_r = (frame_size / 2.0) - 8.0
        if t < 0.25:
            # Stage 1: Explosive flash expansion
            r = 6.0 + (t / 0.25) * (max_safe_r * 0.70)
            alpha_global = 1.0
        elif t < 0.55:
            # Stage 2: Max fiery fireball
            r = max_safe_r * 0.70 + (t - 0.25) * (max_safe_r * 0.28)
            alpha_global = 1.0 - (t - 0.25) * 0.25
        else:
            # Stage 3: Dissipating smoky embers
            r = max_safe_r * 0.85 + (t - 0.55) * 4.0
            alpha_global = max(0.0, 0.82 - (t - 0.55) / 0.45 * 0.82)

        # Multi-harmonic organic distortion lobes
        lobes = (
            0.20 * np.sin(angles * 3.0 + idx * 0.9) +
            0.15 * np.cos(angles * 5.0 - idx * 1.3) +
            0.10 * np.sin(angles * 7.0 + idx * 0.7)
        )
        distorted_r = np.clip(r * (1.0 + lobes), 2.0, max_safe_r)

        # Normalized distance (0 at center, 1 at boundary)
        norm_dist = np.clip(dist_from_center / (distorted_r + 1e-4), 0.0, 1.0)

        # Alpha channel: Soft non-linear plasma falloff
        alpha = np.clip((1.0 - norm_dist**1.85) * 255.0 * alpha_global, 0.0, 255.0)
        alpha[dist_from_center > distorted_r * 1.15] = 0.0

        # High-energy Fireball color gradient
        red = np.zeros_like(dist_from_center, dtype=np.float32)
        green = np.zeros_like(dist_from_center, dtype=np.float32)
        blue = np.zeros_like(dist_from_center, dtype=np.float32)

        if t < 0.30:
            # Blinding white ignition core -> Solar gold -> Fierce crimson edge
            red[:] = 255.0
            green[:] = np.clip(255.0 - norm_dist**1.05 * 215.0, 0.0, 255.0)
            blue[:] = np.clip(255.0 - norm_dist**0.45 * 255.0, 0.0, 255.0)
        elif t < 0.65:
            # Molten fireball: Bright gold/orange -> Fiery red/crimson -> Smoke
            p = (t - 0.30) / 0.35
            red[:] = 255.0
            green[:] = np.clip((230.0 - p * 130.0) - norm_dist**1.15 * 200.0, 0.0, 255.0)
            blue[:] = np.clip((65.0 - p * 65.0) - norm_dist * 65.0, 0.0, 255.0)
        else:
            # Billowing dark volcanic smoke cloud with glowing embers
            p = (t - 0.65) / 0.35
            red[:] = np.clip((170.0 * (1.0 - p * 0.65)) * (1.0 - norm_dist * 0.65), 0.0, 255.0)
            green[:] = np.clip((55.0 * (1.0 - p * 0.88)) * (1.0 - norm_dist), 0.0, 255.0)
            blue[:] = np.clip((20.0 * (1.0 - p)), 0.0, 255.0)

        rgba = np.stack([red, green, blue, alpha], axis=-1).astype(np.uint8)
        frame_img = Image.fromarray(rgba, 'RGBA')
        draw = ImageDraw.Draw(frame_img)

        # Starburst flash spikes during initial ignition (strictly clamped inside frame)
        if t < 0.25:
            spike_len = min(max_safe_r * 0.95, r * 1.35)
            spike_alpha = int(255 * (1.0 - t / 0.25))
            for ang in [0, math.pi/2, math.pi, math.pi*3/2]:
                sx = center + math.cos(ang) * spike_len
                sy = center + math.sin(ang) * spike_len
                draw.line([(center, center), (sx, sy)], fill=(255, 255, 255, spike_alpha), width=2)
            for ang in [math.pi/4, math.pi*3/4, math.pi*5/4, math.pi*7/4]:
                sx = center + math.cos(ang) * (spike_len * 0.68)
                sy = center + math.sin(ang) * (spike_len * 0.68)
                draw.line([(center, center), (sx, sy)], fill=(0, 243, 255, int(spike_alpha * 0.8)), width=1)

        # Flying incendiary spark shards
        num_sparks = int(18 * (1.0 - t * 0.7))
        for s in range(num_sparks):
            sp_angle = np.random.uniform(0.0, math.pi * 2.0)
            sp_dist = min(max_safe_r - 2, r * (0.35 + t * 0.75 + np.random.uniform(0.0, 0.25)))
            sx = center + math.cos(sp_angle) * sp_dist
            sy = center + math.sin(sp_angle) * sp_dist
            sp_radius = np.random.uniform(1.2, 2.8) * (1.0 - t * 0.5)

            if 2 <= sx < frame_size - 2 and 2 <= sy < frame_size - 2:
                sp_alpha = int(255 * alpha_global * np.random.uniform(0.75, 1.0))
                spark_col = (255, 255, 210, sp_alpha) if s % 2 == 0 else (255, 160, 40, sp_alpha)
                draw.ellipse([sx - sp_radius, sy - sp_radius, sx + sp_radius, sy + sp_radius], fill=spark_col)

        # Expanding supersonic shockwave ring during mid-phase
        if 0.12 < t < 0.65:
            ring_t = (t - 0.12) / 0.53
            ring_r = min(max_safe_r - 2, r * (0.65 + ring_t * 0.5))
            ring_alpha = int(220 * (1.0 - ring_t**1.4))
            if ring_alpha > 5:
                ring_box = [center - ring_r, center - ring_r, center + ring_r, center + ring_r]
                draw.ellipse(ring_box, outline=(255, 220, 100, ring_alpha), width=max(1, int(3 * (1 - ring_t))))

        # Smooth blending
        frame_smoothed = frame_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        box = (int(col * frame_size), int(row * frame_size), int((col + 1) * frame_size), int((row + 1) * frame_size))
        sheet.paste(frame_smoothed, box, frame_smoothed)

    os.makedirs('assets/images', exist_ok=True)
    out_path = 'assets/images/explosion_sheet.png'
    sheet.save(out_path)
    print(f"Successfully generated enhanced explosion spritesheet: {out_path} ({sheet.size[0]}x{sheet.size[1]})")

if __name__ == '__main__':
    create_explosion_spritesheet()
