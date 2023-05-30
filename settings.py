WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 32

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 70
UI_FONT = './fonts/Monoton-Regular.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
EXP_COLOR = 'green'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

TEXT_COLOR_SELECTED = 'black'
TEXT_COLOR = 'pink'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'


weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': './player/weapons/sword/full.png'},
    'longsword': {'cooldown': 700, 'damage': 45, 'graphic': './player/weapons/longsword/full.png'},
    'katana': {'cooldown': 50, 'damage': 10, 'graphic': './player/weapons/katana/full.png'},
    'wand': {'cooldown': 300, 'damage': 20, 'graphic': './player/weapons/wand/full.png'},
    'vampire_sword': {'cooldown': 100, 'damage': 15, 'lifesteal': 10,
                      'graphic': './player/weapons/vampire_sword/full.png'},
}

magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': './player/magic/flame/Fireball1.png'},
    'haduken': {'strength': 100, 'cost': 60, 'graphic': './player/magic/haduken/haduken1.png'},
    'shuriken': {'strength': 3, 'cost': 10, 'graphic': './player/magic/shuriken/ShurikenMagic1.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': './player/magic/heal/heal1.png'}
}

monster_data = {
    'axolotl': {'health': 75, 'exp': 50, 'damage': 10, 'attack_type': 'claw',
                'attack_sound': './monsters/audio/claw.wav',
                'speed': 1.5, 'resistance': 3, 'attack_radius': 20, 'notice_radius': 240},
    'octopus': {'health': 150, 'exp': 100, 'damage': 25, 'attack_type': 'slash',
                'attack_sound': './monsters/audio/slash.wav',
                'speed': 3, 'resistance': 6, 'attack_radius': 30, 'notice_radius': 300},
    'skull': {'health': 150, 'exp': 120, 'damage': 30, 'attack_type': 'spirit',
              'attack_sound': './monsters/audio/spirit.wav',
              'speed': 3, 'resistance': 6, 'attack_radius': 30, 'notice_radius': 300}


}
