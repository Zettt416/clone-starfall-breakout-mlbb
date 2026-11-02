import os
from PIL import Image, ImageDraw

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def create_miniboss_sprite():
    # Native pixel canvas 80 x 64, facing LEFT
    w, h = 80, 64
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    mid_y = h // 2

    # Palettes
    HULL_SHADOW = hex_to_rgba('#0d0818')
    HULL_DARK = hex_to_rgba('#1c1333')
    HULL_MID = hex_to_rgba('#2f2154')
    HULL_LIGHT = hex_to_rgba('#48367d')
    HULL_EDGE = hex_to_rgba('#6a52b3')
    HULL_SPECULAR = hex_to_rgba('#a28be0')

    ARMOR_CRIMSON = hex_to_rgba('#660026')
    ARMOR_MAGENTA = hex_to_rgba('#b30047')
    GLOW_PINK = hex_to_rgba('#ff2a85')
    GLOW_HOT_PINK = hex_to_rgba('#ff66a8')
    GLOW_WHITE = hex_to_rgba('#ffffff')

    CYAN_CORE_DARK = hex_to_rgba('#005577')
    CYAN_CORE_MID = hex_to_rgba('#00c8e6')
    CYAN_CORE_BRIGHT = hex_to_rgba('#00f3ff')
    CYAN_CORE_WHITE = hex_to_rgba('#e0ffff')

    THRUST_PURPLE = hex_to_rgba('#9d4edd')
    THRUST_PINK = hex_to_rgba('#ff2a85')
    THRUST_HOT = hex_to_rgba('#ffd000')

    # Draw symmetrical components
    for dy in range(h // 2):
        y_top = mid_y - dy - 1
        y_bot = mid_y + dy

        # 1. Main fuselage / spine (x from 12 to 70)
        # Front nose tip at x = 8..14 around mid_y
        if dy <= 3:
            # Needle prow
            x_start = 8 + dy * 2
            x_end = 42
            for x in range(x_start, x_end):
                col = HULL_SPECULAR if dy == 0 and x < 32 else (HULL_MID if dy == 1 else HULL_DARK)
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # 2. Main central hull body
        if dy <= 12:
            x_start = 16 + int(dy * 1.4)
            x_end = 66 - int(dy * 0.5)
            for x in range(x_start, x_end):
                # Gradient shading across y
                if dy <= 2:
                    col = HULL_SPECULAR if (x % 3 == 0) else HULL_LIGHT
                elif dy <= 6:
                    col = HULL_MID
                elif dy <= 10:
                    col = HULL_DARK
                else:
                    col = HULL_SHADOW
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # 3. Swept Predator Forward & Backward Wings
        # Forward wing blades extending out to dy = 28
        if 4 <= dy <= 26:
            # Swept forward angle: wing leading edge
            wing_front = int(24 + (dy - 4) * 0.8)
            wing_back = int(wing_front + 14 + (26 - dy) * 0.4)
            for x in range(wing_front, min(74, wing_back)):
                if x == wing_front:
                    col = HULL_SPECULAR # Leading edge highlight
                elif x == wing_front + 1:
                    col = GLOW_PINK if (x + dy) % 4 == 0 else HULL_EDGE # Energy conduit trace
                elif x == wing_back - 1:
                    col = HULL_SHADOW
                elif dy > 18:
                    col = ARMOR_MAGENTA if (x - wing_front) in (2, 3) else HULL_DARK
                else:
                    col = HULL_MID if (x - wing_front) < 6 else HULL_DARK
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # Wingtip plasma cannons (at dy = 24..28, x = 36..48)
        if 23 <= dy <= 27:
            for x in range(30, 44):
                col = GLOW_HOT_PINK if x < 34 else HULL_SHADOW
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

    # 4. Forward Twin Plasma Cannons (Nose flanking)
    for dy in (5, 6, 7):
        for x in range(4, 22):
            col = GLOW_PINK if x in (5, 6, 7) else (GLOW_WHITE if x == 4 else HULL_DARK)
            draw.point((x, mid_y - dy), fill=col)
            draw.point((x, mid_y + dy), fill=col)
        # Gun barrel opening
        draw.point((3, mid_y - dy), fill=CYAN_CORE_BRIGHT)
        draw.point((3, mid_y + dy), fill=CYAN_CORE_BRIGHT)

    # 5. Glowing Central Cyclops Ocular Core / Cockpit (x = 22..34, y around mid_y)
    for y in range(mid_y - 4, mid_y + 5):
        for x in range(20, 32):
            dist = ((x - 26)**2 + (y - mid_y)**2)**0.5
            if dist < 4.5:
                if dist < 1.8:
                    draw.point((x, y), fill=GLOW_WHITE)
                elif dist < 3.2:
                    draw.point((x, y), fill=CYAN_CORE_BRIGHT)
                else:
                    draw.point((x, y), fill=CYAN_CORE_MID)
            elif dist < 5.8:
                draw.point((x, y), fill=HULL_SHADOW) # Dark bezel

    # 6. Energy conduit circuits on hull
    for dy in (3, 8, 14):
        for x in range(32, 58, 2):
            draw.point((x, mid_y - dy), fill=GLOW_PINK)
            draw.point((x, mid_y + dy), fill=GLOW_PINK)

    # 7. Rear Hyperdrive Thruster Turbines (x = 64..76)
    for dy in (6, 7, 8, 9, 10, 15, 16, 17, 18):
        for x in range(64, 72):
            draw.point((x, mid_y - dy), fill=HULL_SHADOW)
            draw.point((x, mid_y + dy), fill=HULL_SHADOW)
        # Thruster exhaust flame plume
        for x in range(72, 78):
            dist_ex = x - 72
            col = GLOW_WHITE if dist_ex < 2 else (THRUST_HOT if dist_ex < 4 else THRUST_PINK)
            draw.point((x, mid_y - dy), fill=col)
            draw.point((x, mid_y + dy), fill=col)

    # Scale 2x with NEAREST for sharp 16-bit arcade rendering
    return img.resize((w * 2, h * 2), Image.NEAREST)


def create_bigboss_sprite():
    # Native pixel canvas 128 x 96, facing LEFT
    w, h = 128, 96
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    mid_y = h // 2

    # Palettes
    HULL_SHADOW = hex_to_rgba('#080610')
    HULL_DARK = hex_to_rgba('#140f24')
    HULL_MID = hex_to_rgba('#241a3d')
    HULL_LIGHT = hex_to_rgba('#3d2e61')
    HULL_EDGE = hex_to_rgba('#5a458a')
    HULL_SPECULAR = hex_to_rgba('#9580c7')

    CRIMSON_DARK = hex_to_rgba('#4a0412')
    CRIMSON_MID = hex_to_rgba('#8c0a27')
    CRIMSON_BRIGHT = hex_to_rgba('#d91142')
    CRIMSON_HOT = hex_to_rgba('#ff2a55')

    GOLD_DARK = hex_to_rgba('#8c6200')
    GOLD_MID = hex_to_rgba('#d49b00')
    GOLD_BRIGHT = hex_to_rgba('#ffd000')
    GOLD_WHITE = hex_to_rgba('#fff5cc')

    CYAN_BEAM = hex_to_rgba('#00f3ff')
    CYAN_HOT = hex_to_rgba('#c2fcff')
    WHITE = hex_to_rgba('#ffffff')

    # Draw massive hull profile symmetrically
    for dy in range(h // 2):
        y_top = mid_y - dy - 1
        y_bot = mid_y + dy

        # 1. Forward Heavy Railgun Accelerator Prongs (Nose at x = 6..28, dy = 4..12)
        if 4 <= dy <= 12:
            for x in range(6, 36):
                if dy in (4, 12):
                    col = HULL_SHADOW
                elif dy in (5, 11):
                    col = HULL_EDGE if x > 14 else HULL_SPECULAR
                elif dy in (7, 8, 9):
                    # Interior Railgun accelerator channel glowing with cyan coils
                    if x % 4 in (0, 1):
                        col = CYAN_BEAM if x > 12 else CYAN_HOT
                    else:
                        col = HULL_DARK
                else:
                    col = HULL_MID
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # Railgun muzzle tips
        if 6 <= dy <= 10:
            draw.point((5, y_top), fill=CYAN_HOT)
            draw.point((4, y_top), fill=WHITE)
            draw.point((5, y_bot), fill=CYAN_HOT)
            draw.point((4, y_bot), fill=WHITE)

        # 2. Main Armored Fortress Core (x from 28 to 112)
        if dy <= 22:
            x_start = 28 + int(dy * 0.6)
            x_end = 114 - int(dy * 0.3)
            for x in range(x_start, x_end):
                # Layered plating
                if dy <= 3:
                    col = HULL_SPECULAR if (x % 5 == 0) else HULL_LIGHT
                elif dy <= 8:
                    col = HULL_MID
                elif dy <= 15:
                    col = CRIMSON_MID if (38 <= x <= 58 or 80 <= x <= 96) else HULL_DARK
                else:
                    col = HULL_DARK if (x % 4 == 0) else HULL_SHADOW
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # 3. Heavy Armored Citadel Shoulders & Wing Sponsons (dy = 18..44)
        if 16 <= dy <= 42:
            sponson_front = int(46 + (dy - 16) * 1.1)
            sponson_back = int(sponson_front + 24 + (42 - dy) * 0.5)
            for x in range(sponson_front, min(120, sponson_back)):
                if x == sponson_front:
                    col = HULL_SPECULAR # Leading bevel
                elif x == sponson_front + 1:
                    col = GOLD_BRIGHT if (x + dy) % 6 == 0 else HULL_EDGE # Gold warning hazard strip
                elif x == sponson_back - 1:
                    col = HULL_SHADOW
                elif dy > 30 and (x - sponson_front) in (3, 4, 5):
                    col = CRIMSON_HOT # Sponson armor highlight
                else:
                    col = HULL_MID if (x - sponson_front) < 10 else HULL_DARK
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

        # Wingtip Heavy Missile Pods (dy = 36..42, x = 74..94)
        if 36 <= dy <= 41:
            for x in range(74, 94):
                if x in (76, 80, 84, 88, 92):
                    col = GOLD_BRIGHT # Missile tubes
                elif dy in (36, 41):
                    col = HULL_SHADOW
                else:
                    col = CRIMSON_MID
                draw.point((x, y_top), fill=col)
                draw.point((x, y_bot), fill=col)

    # 4. Pulsating Molten Core Chamber (Centered at x = 48, mid_y)
    for y in range(mid_y - 8, mid_y + 9):
        for x in range(40, 57):
            dist = (((x - 48)**2)*1.0 + ((y - mid_y)**2)*1.2)**0.5
            if dist < 7.5:
                if dist < 2.5:
                    draw.point((x, y), fill=WHITE)
                elif dist < 4.5:
                    draw.point((x, y), fill=CRIMSON_HOT)
                elif dist < 6.5:
                    draw.point((x, y), fill=CRIMSON_BRIGHT)
                else:
                    draw.point((x, y), fill=CRIMSON_MID)
            elif dist < 9.0:
                draw.point((x, y), fill=HULL_SHADOW) # Magnetic containment collar

    # 5. Dual Energy Shield Emitter Orbs (at x = 78, y = mid_y - 18 and mid_y + 18)
    for emitter_y in (mid_y - 18, mid_y + 18):
        for y in range(emitter_y - 4, emitter_y + 5):
            for x in range(74, 83):
                d = ((x - 78)**2 + (y - emitter_y)**2)**0.5
                if d < 3.5:
                    col = WHITE if d < 1.5 else GOLD_BRIGHT
                    draw.point((x, y), fill=col)
                elif d < 4.8:
                    draw.point((x, y), fill=HULL_SHADOW)

    # 6. Secondary Turret Batteries (at x = 66 and x = 94, y = mid_y - 10 and mid_y + 10)
    for ty in (mid_y - 10, mid_y + 10):
        for tx in (64, 92):
            draw.rectangle([tx, ty - 2, tx + 6, ty + 2], fill=HULL_LIGHT, outline=HULL_SHADOW)
            # Gun barrels pointing left
            draw.line([(tx - 4, ty - 1), (tx, ty - 1)], fill=HULL_SPECULAR)
            draw.line([(tx - 4, ty + 1), (tx, ty + 1)], fill=HULL_SPECULAR)
            draw.point((tx - 5, ty - 1), fill=CYAN_BEAM)
            draw.point((tx - 5, ty + 1), fill=CYAN_BEAM)

    # 7. Massive Quad Engine Thruster Turbines (x = 108..124)
    for dy in (8, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 27):
        for x in range(108, 116):
            draw.point((x, mid_y - dy), fill=HULL_SHADOW)
            draw.point((x, mid_y + dy), fill=HULL_SHADOW)
        # Intense fiery plasma exhaust plume
        for x in range(116, 126):
            plume_x = x - 116
            col = WHITE if plume_x < 2 else (GOLD_WHITE if plume_x < 4 else (GOLD_BRIGHT if plume_x < 7 else CRIMSON_HOT))
            draw.point((x, mid_y - dy), fill=col)
            draw.point((x, mid_y + dy), fill=col)

    # Scale 2x with NEAREST for sharp 16-bit arcade rendering
    return img.resize((w * 2, h * 2), Image.NEAREST)


if __name__ == "__main__":
    os.makedirs("assets/images", exist_ok=True)
    
    print("Generating Miniboss ('Void Destroyer')...")
    mb = create_miniboss_sprite()
    mb.save("assets/images/miniboss.png", "PNG")
    print(f"Saved assets/images/miniboss.png ({mb.size[0]}x{mb.size[1]})")

    print("Generating Big Boss ('Titan Apex Mothership')...")
    bb = create_bigboss_sprite()
    bb.save("assets/images/bigboss.png", "PNG")
    print(f"Saved assets/images/bigboss.png ({bb.size[0]}x{bb.size[1]})")

    print("All boss sprites generated successfully!")

