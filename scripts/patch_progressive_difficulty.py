with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add fast_scout and dynamic time HP scaling to Meteor constructor
old_meteor_types = '''      } else if (type === 'wall_block') {
        this.radius = 24;
        this.hp = 5;
        this.maxHp = 5;
        this.speed = 75;
        this.vy = 0;
        this.score = 50;
        this.color = '#452b69';
      }

      this.speed *= state.difficultyMultiplier;'''

new_meteor_types = '''      } else if (type === 'fast_scout') {
        this.isDrone = true;
        this.radius = 16;
        this.hp = 2;
        this.maxHp = 2;
        this.speed = 280 + Math.random() * 60;
        this.vy = (Math.random() - 0.5) * 40;
        this.score = 75;
        this.color = '#ff0055';
      } else if (type === 'wall_block') {
        this.radius = 24;
        this.hp = 5;
        this.maxHp = 5;
        this.speed = 75;
        this.vy = 0;
        this.score = 50;
        this.color = '#452b69';
      }

      // Dynamic HP Scaling over time & difficulty
      if (type !== 'star' && type !== 'wall_block') {
        const conf = DIFFICULTY_CONFIGS[state.difficulty] || DIFFICULTY_CONFIGS.normal;
        const timeHpScale = 1.0 + Math.min(2.0, state.survivalTime * 0.005);
        const diffHpMult = conf.meteorHpMult || 1.0;
        this.hp = Math.max(1, Math.round(this.hp * timeHpScale * diffHpMult));
        this.maxHp = this.hp;
      }

      this.speed *= state.difficultyMultiplier;'''

assert old_meteor_types in text, "old_meteor_types not found"
text = text.replace(old_meteor_types, new_meteor_types, 1)
print("1. Added fast_scout and time HP scaling to Meteor!")

# 2. Update state.difficultyMultiplier to explicitly scale with survivalTime
old_diff_mult = '''    state.difficultyMultiplier = (1.0 + Math.min(2.5, state.score / 2500)) * conf.meteorSpeedMult;'''
new_diff_mult = '''    const timeSpeedBonus = Math.min(1.8, state.survivalTime * 0.005);
    const scoreSpeedBonus = Math.min(1.2, state.score / 3500);
    state.difficultyMultiplier = (1.0 + timeSpeedBonus + scoreSpeedBonus) * conf.meteorSpeedMult;'''

assert old_diff_mult in text, "old_diff_mult not found"
text = text.replace(old_diff_mult, new_diff_mult, 1)
print("2. Updated state.difficultyMultiplier with survivalTime scaling!")

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied progressive difficulty scaling patch!")

