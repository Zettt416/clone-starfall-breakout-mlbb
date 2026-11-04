with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Line 4458 in drawBossHyperRailgunBeam
target1 = '''      ctx.ellipse(rx, beamY, 7, (baseH * 0.48) + ringPulse, 0, 0, Math.PI * 2);'''
replacement1 = '''      const ringRadiusY = Math.max(0.1, (baseH * 0.48) + ringPulse);
      ctx.ellipse(rx, beamY, 7, ringRadiusY, 0, 0, Math.PI * 2);'''

assert target1 in text, 'target1 not found'
text = text.replace(target1, replacement1, 1)

# 2. Line 4528 & 4533 in drawBossHyperRailgunBeam
target2 = '''    ctx.ellipse(0, beamY, 14, baseH * 0.8, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.ellipse(0, beamY, 6, baseH * 0.45, 0, 0, Math.PI * 2);'''

replacement2 = '''    ctx.ellipse(0, beamY, 14, Math.max(0.1, baseH * 0.8), 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.ellipse(0, beamY, 6, Math.max(0.1, baseH * 0.45), 0, 0, Math.PI * 2);'''

assert target2 in text, 'target2 not found'
text = text.replace(target2, replacement2, 1)

# 3. Safeguard line 4271 if exists
target3 = '''ctx.ellipse(rx, beamY, 8, beamH * 0.45, 0, 0, Math.PI * 2);'''
if target3 in text:
    text = text.replace(target3, '''ctx.ellipse(rx, beamY, 8, Math.max(0.1, beamH * 0.45), 0, 0, Math.PI * 2);''', 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched ctx.ellipse safeguards in js/game.js!')

