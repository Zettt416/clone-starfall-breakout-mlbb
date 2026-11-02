import os
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

BRAIN_DIR = r"C:\Users\Zeke\.gemini\antigravity\brain\dda2e00e-0c43-42a4-a266-c0ea76b4a578"
ASSETS_DIR = r"assets\images"

def flood_fill_clean_bg(img_path, threshold=35):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    H, W, _ = arr.shape
    
    # Calculate brightness
    r = arr[:, :, 0].astype(np.int32)
    g = arr[:, :, 1].astype(np.int32)
    b = arr[:, :, 2].astype(np.int32)
    brightness = np.maximum(np.maximum(r, g), b)
    
    # Visited grid for flood fill from perimeter
    is_bg = np.zeros((H, W), dtype=bool)
    queue = deque()
    
    # Enqueue borders
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

    # 4-connectivity flood fill
    while queue:
        cy, cx = queue.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < H and 0 <= nx < W and not is_bg[ny, nx]:
                if brightness[ny, nx] <= threshold:
                    is_bg[ny, nx] = True
                    queue.append((ny, nx))
                    
    # Set background alpha to 0
    arr[is_bg, 3] = 0
    
    # Also for pixels directly adjacent to is_bg with low brightness (anti-aliasing clean)
    alpha = arr[:, :, 3].astype(np.float32)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not is_bg[y, x] and brightness[y, x] < threshold + 30:
                # If touching a bg pixel
                if is_bg[y-1, x] or is_bg[y+1, x] or is_bg[y, x-1] or is_bg[y, x+1]:
                    # Fade alpha
                    factor = max(0.0, (brightness[y, x] - threshold) / 30.0)
                    alpha[y, x] = factor * 255.0
                    
    arr[:, :, 3] = alpha.astype(np.uint8)
    res = Image.fromarray(arr, "RGBA")
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    return res

def clean_shield_orb(img_path):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    H, W, _ = arr.shape
    
    # Center of image
    cy, cx = H / 2.0, W / 2.0
    Y, X = np.ogrid[:H, :W]
    dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2)
    max_radius = min(cx, cy) * 0.96
    
    # Brightness
    brightness = np.maximum(np.maximum(arr[:, :, 0], arr[:, :, 1]), arr[:, :, 2])
    
    # Outer radial fade
    radial_alpha = np.clip((max_radius - dist_from_center) / 30.0, 0.0, 1.0)
    
    # Brightness based alpha for additive glow
    glow_alpha = np.clip((brightness - 25.0) / 35.0, 0.0, 1.0)
    
    final_alpha = glow_alpha * radial_alpha * 255.0
    arr[:, :, 3] = final_alpha
    
    res = Image.fromarray(arr.astype(np.uint8), "RGBA")
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    return res

# Process miniboss
mb_src = os.path.join(BRAIN_DIR, "miniboss_void_destroyer_1793614591169.jpg")
mb_clean = flood_fill_clean_bg(mb_src, threshold=32)
mb_clean.save(os.path.join(ASSETS_DIR, "miniboss.png"), "PNG")
print("Miniboss cleaned successfully!")

# Process bigboss
bb_src = os.path.join(BRAIN_DIR, "bigboss_goliath_mothership_1793614606575.jpg")
bb_clean = flood_fill_clean_bg(bb_src, threshold=32)
bb_clean.save(os.path.join(ASSETS_DIR, "bigboss.png"), "PNG")
print("Bigboss cleaned successfully!")

# Process shield
sh_src = os.path.join(BRAIN_DIR, "shield_icon_powerup_1793614623484.jpg")
sh_clean = clean_shield_orb(sh_src)
sh_clean.save(os.path.join(ASSETS_DIR, "shield_icon.png"), "PNG")
print("Shield cleaned successfully!")
