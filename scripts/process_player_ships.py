import os
from collections import deque
import numpy as np
from PIL import Image

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

ships = [
    ("ship1_stella_nova_black_1793785457418.jpg", "ship_stella_nova.png"),
    ("ship2_aether_vanguard_1793785478682.jpg", "ship_aether_vanguard.png"),
    ("ship3_chrono_phantom_1793785499743.jpg", "ship_chrono_phantom.png")
]

for src_name, dst_name in ships:
    src_path = os.path.join(BRAIN_DIR, src_name)
    dst_path = os.path.join(ASSETS_DIR, dst_name)
    if os.path.exists(src_path):
        res = flood_fill_clean_bg(src_path)
        res.save(dst_path, format="PNG")
        print(f"Processed {src_name} -> {dst_path} (size: {res.size})")
    else:
        print(f"Warning: {src_path} not found!")

print("All player ships processed!")
