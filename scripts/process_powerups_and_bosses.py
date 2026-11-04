import os
from collections import deque
import numpy as np
from PIL import Image, ImageDraw

BRAIN_DIR = r"C:\Users\Zeke\.gemini\antigravity\brain\dda2e00e-0c43-42a4-a266-c0ea76b4a578"
ASSETS_DIR = r"assets\images"

def flood_fill_clean_bg(img_path, threshold=38):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    H, W, _ = arr.shape
    
    r = arr[:, :, 0].astype(np.int32)
    g = arr[:, :, 1].astype(np.int32)
    b = arr[:, :, 2].astype(np.int32)
    brightness = np.maximum(np.maximum(r, g), b)
    
    is_bg = np.zeros((H, W), dtype=bool)
    queue = deque()
    
    for x in range(W):
        if brightness[0, x] <= threshold:
            queue.append((0, x))
            is_bg[0, x] = True
        if brightness[H - 1, x] <= threshold:
            queue.append((H - 1, x))
            is_bg[H - 1, x] = True
            
    for y in range(H):
        if brightness[y, 0] <= threshold:
            queue.append((y, 0))
            is_bg[y, 0] = True
        if brightness[y, W - 1] <= threshold:
            queue.append((y, W - 1))
            is_bg[y, W - 1] = True

    while queue:
        cy, cx = queue.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < H and 0 <= nx < W and not is_bg[ny, nx]:
                if brightness[ny, nx] <= threshold:
                    is_bg[ny, nx] = True
                    queue.append((ny, nx))
                    
    arr[is_bg, 3] = 0
    
    # Smooth edges with brightness ramp
    soft_mask = (brightness <= threshold + 25) & (~is_bg)
    ramp = (brightness[soft_mask] - threshold) / 25.0
    arr[soft_mask, 3] = np.clip(ramp * 255, 0, 255).astype(np.uint8)
    
    result = Image.fromarray(arr)
    bbox = result.getbbox()
    if bbox:
        result = result.crop(bbox)
        
    return result

# 1. Process Powerup Icons
powerups = [
    ("powerup_hyperdrive_1793785442884.jpg", "powerup_hyperdrive.png"),
    ("powerup_plasma_spread_1793785454004.jpg", "powerup_plasma_spread.png"),
    ("powerup_heavy_flak_1793785477532.jpg", "powerup_heavy_flak.png"),
    ("powerup_tesla_coil_1793785487934.jpg", "powerup_tesla_coil.png"),
    ("powerup_quantum_clones_1793785513484.jpg", "powerup_quantum_clones.png")
]

for src_name, dst_name in powerups:
    src_path = os.path.join(BRAIN_DIR, src_name)
    dst_path = os.path.join(ASSETS_DIR, dst_name)
    if os.path.exists(src_path):
        res = flood_fill_clean_bg(src_path)
        res.save(dst_path, format="PNG")
        print(f"Processed powerup {src_name} -> {dst_path} (size: {res.size})")

# 2. Generate powerup_void_needle.png procedurally with PIL
size = 256
needle_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(needle_img)

# Outer glowing circle badge
cx, cy = size // 2, size // 2
r = 105
for i in range(12):
    alpha = int(35 * (1 - i / 12))
    draw.ellipse([cx - r - i*2, cy - r - i*2, cx + r + i*2, cy + r + i*2], outline=(184, 68, 255, alpha), width=2)

draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 5, 30, 230), outline=(224, 170, 255, 255), width=4)

# Piercing needle spearhead
spear = [
    (cx + 70, cy),       # tip right
    (cx - 30, cy - 28),  # top fin
    (cx - 55, cy - 12),  # inner top
    (cx - 80, cy),       # back shaft
    (cx - 55, cy + 12),  # inner bot
    (cx - 30, cy + 28),  # bot fin
]
draw.polygon(spear, fill=(230, 180, 255, 255), outline=(255, 255, 255, 255))
draw.polygon([(cx + 60, cy), (cx - 20, cy - 14), (cx - 40, cy), (cx - 20, cy + 14)], fill=(255, 255, 255, 255))

# Prismatic laser flare
draw.line([(cx - 75, cy), (cx + 85, cy)], fill=(255, 255, 255, 255), width=3)
draw.line([(cx + 60, cy - 35), (cx + 60, cy + 35)], fill=(200, 100, 255, 200), width=2)
draw.ellipse([cx + 55, cy - 5, cx + 65, cy + 5], fill=(255, 255, 255, 255))

dst_path = os.path.join(ASSETS_DIR, "powerup_void_needle.png")
needle_img.save(dst_path, format="PNG")
print(f"Generated procedural powerup_void_needle.png -> {dst_path}")

# 3. Process the 3 new Big Boss sprites
bosses = [
    ("boss1_crimson_annihilator_1793785462406.jpg", "boss_crimson_annihilator.png"),
    ("boss2_void_singularity_goliath_1793785483270.jpg", "boss_void_singularity.png"),
    ("boss3_astraea_ex_machina_black_bg_1793785533606.jpg", "boss_astraea_archon.png")
]

for src_name, dst_name in bosses:
    src_path = os.path.join(BRAIN_DIR, src_name)
    dst_path = os.path.join(ASSETS_DIR, dst_name)
    if os.path.exists(src_path):
        res = flood_fill_clean_bg(src_path)
        res.save(dst_path, format="PNG")
        print(f"Processed boss {src_name} -> {dst_path} (size: {res.size})")

print("All powerup and boss assets successfully processed!")
