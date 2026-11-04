with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''      } else if (viewParam === 'boss') {'''
replacement = '''      } else if (viewParam === 'megaman_dash') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 240;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 360;
        testBoss.currentX = 360;
        testBoss.y = 230;
        testBoss.tilt = -0.38;
        testBoss.actionState = 'dash_strike';
        testBoss.actionTimer = 0.5;
        testBoss.afterimages = [
          { x: 520, y: 220, tilt: -0.32, alpha: 0.35, color: '#ff1493' },
          { x: 440, y: 225, tilt: -0.35, alpha: 0.70, color: '#ffd000' }
        ];
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'megaman_slam') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 300;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 420;
        testBoss.currentX = 420;
        testBoss.y = 250;
        testBoss.tilt = 0.35;
        testBoss.actionState = 'dive_slam';
        testBoss.actionTimer = 0.4;
        testBoss.afterimages = [
          { x: 490, y: 120, tilt: 0.22, alpha: 0.35, color: '#ffd000' },
          { x: 450, y: 185, tilt: 0.30, alpha: 0.70, color: '#ff1493' }
        ];
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'megaman_railgun') {
        startGame();
        state.difficulty = 'hard';
        player.x = 100;
        player.y = 240;
        const b56 = (window.BOSS_CATALOG || []).find(b => b.id === 56) || { id: 56, name: 'Hellion Warlord', title: 'Siege Fleet Battleship', isBig: true, archetype: 'mecha', color: '#ff1493', baseHp: 290, attack: 'railgun_laser' };
        const testBoss = new Boss(b56, 2);
        testBoss.x = 560;
        testBoss.currentX = 560;
        testBoss.y = 240;
        testBoss.laserTargetY = 240;
        testBoss.isFiringLaser = true;
        testBoss.laserFireTimer = 0.6;
        state.activeBoss = testBoss;
        showBossBar(testBoss);
      } else if (viewParam === 'boss') {'''

assert target in text, 'target not found'
text = text.replace(target, replacement, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added megaman views to js/game.js!')
