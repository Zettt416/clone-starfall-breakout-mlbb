# -*- coding: utf-8 -*-

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_branch = """      } else if (viewParam === 'boss') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss('bigboss', 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);"""

new_branch = """      } else if (viewParam === 'bossship') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 1, name: 'Void Dreadnought', title: 'Heavy Fleet Flagship', isBig: true, archetype: 'spaceship', color: '#00f3ff', baseHp: 200, attack: 'plasma_twin' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bossvalkyrie') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 16, name: 'Valkyrie Prime', title: 'Astral Cyber-Valkyrie', isBig: true, archetype: 'humanoid', color: '#ff00aa', baseHp: 220, attack: 'curtain_fan' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'bossalien') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 21, name: 'Oculon Apex', title: 'Cyclopean Hive Mind', isBig: false, archetype: 'alien', color: '#b844ff', baseHp: 95, attack: 'spiral_danmaku' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'boss') {
        startGame();
        player.x = 100;
        player.y = 240;
        const testBoss = new Boss({ id: 5, name: 'Iron Colossus', title: 'Celestial Mecha Titan', isBig: true, archetype: 'mecha', color: '#ffd000', baseHp: 240, attack: 'railgun_heavy' }, 1);
        testBoss.x = 640;
        testBoss.y = 240;
        testBoss.targetX = 640;
        state.activeBoss = testBoss;
        showBossBar(testBoss);"""

text = text.replace(old_branch, new_branch)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added archetype test views!')

