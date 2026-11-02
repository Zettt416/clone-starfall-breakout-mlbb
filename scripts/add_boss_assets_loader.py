import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:60]):
    if "loadAsset('bigboss'" in line:
        insert_lines = [
            "  loadAsset('boss_spaceship', 'assets/images/boss_spaceship_dreadnought.png');\n",
            "  loadAsset('boss_mecha', 'assets/images/boss_mecha_titan.png');\n",
            "  loadAsset('boss_monster', 'assets/images/boss_alien_leviathan.png');\n",
            "  loadAsset('boss_humanoid', 'assets/images/boss_humanoid_valkyrie.png');\n",
            "  loadAsset('boss_alien', 'assets/images/boss_eldritch_eye.png');\n"
        ]
        lines[i+1:i+1] = insert_lines
        break

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Added boss assets to loadAsset successfully!')
