# -*- coding: utf-8 -*-
import json, re

def update_bosses_js():
    with open('js/bosses.js', 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'window\.BOSS_CATALOG\s*=\s*(\[.*?\]);', text, re.DOTALL)
    if not m:
        print("Error: Could not find window.BOSS_CATALOG in js/bosses.js")
        return

    catalog = json.loads(m.group(1))
    archetypes = ['spaceship', 'mecha', 'monster', 'humanoid', 'alien']

    # Assign archetypes in a balanced way across each tier of 25
    for i, b in enumerate(catalog):
        tier_index = i % 25
        # 5 archetypes distributed evenly across 25 bosses:
        # 0..4: spaceship, 5..9: mecha, 10..14: monster, 15..19: humanoid, 20..24: alien
        archetype_idx = (tier_index // 5) % 5
        b['archetype'] = archetypes[archetype_idx]

        # Ensure name and title sound authentic to the archetype
        if b['archetype'] == 'humanoid':
            humanoid_titles = [
                'Astral Cyber-Valkyrie', 'Celestial Void Warlord', 'Archon of Eclipse',
                'Stellar Blade Inquisitor', 'Cosmic Sovereign Knight'
            ]
            humanoid_names = [
                'Valkyrie Prime', 'Lord Malakor', 'Archon Zephyr', 'Vanquisher Sol', 'Astraea Dawn'
            ]
            sub_idx = tier_index % len(humanoid_titles)
            b['title'] = humanoid_titles[sub_idx]
            b['name'] = f"{humanoid_names[sub_idx]} #{b['id']}"
        elif b['archetype'] == 'alien':
            alien_titles = [
                'Cyclopean Hive Mind', 'Psionic Star-Horror', 'Eldritch Nether-Eye',
                'Abyssal Synapse Beast', 'Cthulhic Mind-Weaver'
            ]
            alien_names = [
                'Oculon Apex', 'Synapse Queen', 'Void Beholder', 'Xanthos Core', 'Mind Eater'
            ]
            sub_idx = tier_index % len(alien_titles)
            b['title'] = alien_titles[sub_idx]
            b['name'] = f"{alien_names[sub_idx]} #{b['id']}"

    # Write back formatted JSON
    new_json = json.dumps(catalog, indent=2)
    new_content = """// 100 Unique Bosses Catalog - Starfall Breakout
// Tiered by difficulty:
// #001 - #025: Easy Tier (Orbital Drones, Corvettes, Astral Entities)
// #026 - #050: Normal Tier (Void Destroyers, Mecha Titans, Star Monsters)
// #051 - #075: Hard Tier (Planetary Battleships, Cyber-Valkyries, Eldritch Horrors)
// #076 - #100: Hardcorez Tier (Celestial Danmaku Horrors, Abyssal Gods, Reality Shredders)
// Archetypes: spaceship, mecha, monster, humanoid, alien

window.BOSS_CATALOG = """ + new_json + ";\n"

    with open('js/bosses.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated js/bosses.js with 5 balanced archetypes!")

if __name__ == '__main__':
    update_bosses_js()

