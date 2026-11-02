import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('testBoss.targetX = 640;', 'testBoss.targetX = 640;\n        testBoss.currentX = 640;')

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated preview views currentX!')
