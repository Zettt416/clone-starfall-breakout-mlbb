import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the Boss class and replace update and draw methods cleanly
old_boss_init = '''      this.x = CANVAS_WIDTH + 100;
      this.y = CANVAS_HEIGHT / 2;
      this.prevY = this.y;
      this.targetX = CANVAS_WIDTH - (isBig ? 160 : 130);
      this.currentX = this.x;
      this.tilt = 0;'''

new_boss_init = '''      this.baseTargetX = CANVAS_WIDTH - (isBig ? 170 : 140);
      this.targetX = this.baseTargetX;
      this.dashTargetX = 220;
      this.jumpTargetX = 500;
      this.jumpTargetY = 85;
      this.diveTargetY = CANVAS_HEIGHT / 2;
      this.x = CANVAS_WIDTH + 140;
      this.y = CANVAS_HEIGHT / 2;
      this.prevY = this.y;
      this.currentX = this.x;
      this.tilt = 0;

      // Mega Man Style Action State Machine
      // States: 'enter' | 'hover' | 'dash_windup' | 'dash_strike' | 'dash_brake' | 'jump_up' | 'jump_apex' | 'dive_slam'
      this.actionState = 'enter';
      this.actionTimer = 0.9;
      this.afterimages = [];
      this.afterimageTimer = 0;'''

assert old_boss_init in text, 'old_boss_init not found!'
text = text.replace(old_boss_init, new_boss_init, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated Boss constructor with Mega Man state machine!')
