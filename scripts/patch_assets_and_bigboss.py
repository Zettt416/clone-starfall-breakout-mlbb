# -*- coding: utf-8 -*-

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update loadAsset
old_load = "loadAsset('miniboss', 'assets/images/miniboss.png');\n    loadAsset('bigboss', 'assets/images/bigboss.png');"
new_load = "loadAsset('miniboss', 'assets/images/boss_alien_leviathan.png');\n    loadAsset('bigboss', 'assets/images/boss_mecha_titan.png');\n    loadAsset('boss_monster', 'assets/images/boss_alien_leviathan.png');\n    loadAsset('boss_mecha', 'assets/images/boss_mecha_titan.png');\n    loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');\n    loadAsset('boss_humanoid', 'assets/images/boss_humanoid_valkyrie.png');\n    loadAsset('boss_alien', 'assets/images/boss_eldritch_eye.png');"

text = text.replace(old_load, new_load)

# 2. Update drawBigbossShip
old_big = "const sprite = assets.images.bigboss;"
new_big = "const spriteKey = 'boss_' + (this.archetype || 'mecha');\n      const sprite = assets.images[spriteKey] || assets.images.bigboss;"
text = text.replace(old_big, new_big)

# In drawBigbossShip hueDiff
old_hue = "const targetHue = hexToHue(this.color || '#00f3ff');\n          const hueDiff = (targetHue - 185 + 360) % 360;"
new_hue = "const targetHue = hexToHue(this.color || '#ffd000');\n          const baseHue = this.baseHue || 183;\n          const hueDiff = (targetHue - baseHue + 360) % 360;"
text = text.replace(old_hue, new_hue)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated loadAsset and drawBigbossShip!')

