from src.engine.platform import Platform

TILE_SIZE = 64





level_1_data = {
    'player_start': {'x': 58*64, 'y':400},
    'enemies': [
        {'type': 'terrorist', 'x': 58 * TILE_SIZE - 500, 'y': 400},
        {'type': 'gunman', 'x': 58 * TILE_SIZE + 800, 'y': 400},
        {'type': 'drone', 'x': -400, 'y': 40, 'direction': 'right'},
        {'type': 'flyingdemon', 'x': 58 * TILE_SIZE - 800, 'y': 382, 'direction': 'right'},
        {'type': 'dragonlord', 'x': 58 * TILE_SIZE - 200, 'y': 338}
    ],

    'objects': [
        {'type': 'bomb', 'x': 58 * TILE_SIZE + 100, 'y': 400 - 500},
        {'type': 'defusekit', 'x': 58 * TILE_SIZE + 100, 'y': 400 - 270},
        {'type': 'teleportgate', 'x1': 58 * TILE_SIZE, 'y1': 363, 'x2': 58 * TILE_SIZE + 1400, 'y2': 43},
        {'type': 'pumpkin', 'x': 58 * TILE_SIZE + 100, 'y': 400 - 270},
        {'type': 'powerbox', 'x': 58 * TILE_SIZE + 700, 'y': 465}
    ],
    'platforms': {
        'standard': [
            {'x': 0, 'y': 8 * TILE_SIZE, 'tiles': 60},
            {'x': -25 * TILE_SIZE, 'y': 1* TILE_SIZE, 'tiles': 20},
            {'x': 35 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'tiles': 6},
            {'x': 43 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 10},
            {'x': 62 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'tiles': 6},
            {'x': 67 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 3},
            {'x': 60 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 5},
            {'x': 48 * TILE_SIZE, 'y': -1 * TILE_SIZE, 'tiles': 10},
            {'x': 31 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 10},
            {'x': 40 * TILE_SIZE, 'y': -4 * TILE_SIZE, 'tiles': 6},
            {'x': 17 * TILE_SIZE, 'y': 2 * TILE_SIZE, 'tiles': 10},
            {'x': 14 * TILE_SIZE, 'y': -2 * TILE_SIZE, 'tiles': 6},
            {'x': 3 * TILE_SIZE, 'y': -2 * TILE_SIZE, 'tiles': 7},
            {'x': -8 * TILE_SIZE, 'y': -4 * TILE_SIZE, 'tiles': 10},
            {'x': 4 * TILE_SIZE, 'y': -9 * TILE_SIZE, 'tiles': 30},









        ],
        'solid': [
            {'x': 0, 'y': 9 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 10 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 11 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 12 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 13 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 14 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 15 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 16 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 17 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 18 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 19 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 20 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 21 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 22 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 23 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 24 * TILE_SIZE, 'repeat':60},

            
            {'x': -25 * TILE_SIZE, 'y': 2* TILE_SIZE, 'repeat': 20},
            {'x': -25 * TILE_SIZE, 'y': 3* TILE_SIZE, 'repeat': 20},
            {'x': -25 * TILE_SIZE, 'y': 4* TILE_SIZE, 'repeat': 20},
            {'x': -25 * TILE_SIZE, 'y': 5* TILE_SIZE, 'repeat': 20},
            {'x': -25 * TILE_SIZE, 'y': 6* TILE_SIZE, 'repeat': 20},



        ],
        'moving': [
            {'x': 55 * TILE_SIZE, 'y': 2 * TILE_SIZE, 'tiles': 2,'range':2*TILE_SIZE, 'direction': 1},            
            {'x': 13 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 2,'range':2*TILE_SIZE, 'direction': 1},
]
    }
}


Boss_fight_level={
    'player_start': {'x': 58*64, 'y':400},
    'enemies': [
        
    ],

    'objects': [
        
    ],
    'platforms': {
        'standard': [
            {'x': 0, 'y': 8 * TILE_SIZE, 'tiles': 60},
            {'x': -25 * TILE_SIZE, 'y': 1* TILE_SIZE, 'tiles': 20},
            {'x': 35 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'tiles': 6},
            {'x': 43 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 10},
            {'x': 62 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'tiles': 6},
            {'x': 67 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 3},
            {'x': 60 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 5},
            {'x': 48 * TILE_SIZE, 'y': -1 * TILE_SIZE, 'tiles': 10},
            {'x': 31 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 10},
            {'x': 40 * TILE_SIZE, 'y': -4 * TILE_SIZE, 'tiles': 6},
            {'x': 17 * TILE_SIZE, 'y': 2 * TILE_SIZE, 'tiles': 10},
            {'x': 14 * TILE_SIZE, 'y': -2 * TILE_SIZE, 'tiles': 6},
            {'x': 3 * TILE_SIZE, 'y': -2 * TILE_SIZE, 'tiles': 7},
            {'x': -8 * TILE_SIZE, 'y': -4 * TILE_SIZE, 'tiles': 10},
            {'x': 4 * TILE_SIZE, 'y': -9 * TILE_SIZE, 'tiles': 30},









        ],
        'solid': [
            {'x': 0, 'y': 9 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 10 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 11 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 12 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 13 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 14 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 15 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 16 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 17 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 18 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 19 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 20 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 21 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 22 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 23 * TILE_SIZE, 'repeat':60},
            {'x': 0, 'y': 24 * TILE_SIZE, 'repeat':60},

            
            



        
]
    }
}
def _add_tiled_platform(platform_list, info, images, *, moving=False):

    x_start, y = info['x'], info['y']
    tile_count = info.get('tiles', 1)

    extra_kwargs = {}
    if moving:
        extra_kwargs = {
            'moving': True,
            'move_range': info.get('range', 0),
            'start_direction': info.get('direction', 1)
        }

    if tile_count == 1:
        platform_list.append(
            Platform(x_start, y, images['solid'], **extra_kwargs)
        )
        return

    platform_list.append(
        Platform(x_start, y, images['left'], **extra_kwargs)
    )

    for i in range(1, tile_count - 1):
        xi = x_start + i * TILE_SIZE
        platform_list.append(
            Platform(xi, y, images['middle'], **extra_kwargs)
        )

    x_last = x_start + (tile_count - 1) * TILE_SIZE
    platform_list.append(
        Platform(x_last, y, images['right'], **extra_kwargs)
    )

def load_level_data(level_data, platform_images):
    platforms = []
    platform_definitions = level_data['platforms']

    for info in platform_definitions.get('standard', []):
        _add_tiled_platform(platforms, info, platform_images, moving=False)

    for info in platform_definitions.get('solid', []):
        repeat = info.get('repeat', 1)
        for i in range(repeat):
            x = info['x'] + i * TILE_SIZE
            y = info['y']
            platforms.append(
            Platform(x, y, platform_images['solid'])
            )

    for info in platform_definitions.get('moving', []):
        _add_tiled_platform(platforms, info, platform_images, moving=True)

    return platforms

def build_enemies(level_data, screen, scroll, platforms):
    from src.engine.terrorist import Terrorist
    from src.engine.gunman import Gunman
    from src.engine.Drone import Drone
    from src.engine.flyingdemon import FlyingDemon
    from src.engine.Dragon_Lord import Dragon_Lord

    terrorists, gunmans, drones, flyingdemons = [], [], [], []
    dragonlord = None

    for enemy in level_data.get('enemies', []):
        x, y = enemy['x'], enemy['y']
        t = enemy['type']
        if t == 'terrorist':
            terrorists.append(Terrorist(x, y, 1280, 720, [], platforms, None, screen, scroll))
        elif t == 'gunman':
            gunmans.append(Gunman(x, y, platforms, []))
        elif t == 'drone':
            drones.append(Drone(x, y, enemy['direction'], []))
        elif t == 'flyingdemon':
            flyingdemons.append(FlyingDemon(x, y, None, enemy['direction']))
        elif t == 'dragonlord':
            dragonlord = Dragon_Lord(x, y, None)

    return {
        'terrorists': terrorists,
        'gunmans': gunmans,
        'drones': drones,
        'flyingdemons': flyingdemons,
        'dragonlord': dragonlord
    }

def apply_targets_to_enemies(enemies, targets):
    for e in enemies['terrorists']:
        e.targets = targets
    for g in enemies['gunmans']:
        g.targets = targets
    for d in enemies['drones']:
        d.targets = targets
    for f in enemies['flyingdemons']:
        f.target = targets[0] if targets else None  # یا یه منطق بهتر
    if enemies['dragonlord']:
        enemies['dragonlord'].target = targets[0]

def build_objects(level_data, targets):
    from src.engine.bomb import Bomb
    from src.engine.defuse_kit import DefuseKit
    from src.engine.teleportgate import Gates
    from src.engine.pumpkin import Pumpkin
    from src.engine.heatlh_box import PowerBox

    objects = {
        'bomb': None,
        'defuse_kit': None,
        'gates': [],
        'misc': []
    }

    for obj in level_data.get('objects', []):
        t = obj['type']
        if t == 'bomb':
            objects['bomb'] = Bomb(obj['x'], obj['y'], targets=targets)
        elif t == 'defusekit':
            objects['defuse_kit'] = DefuseKit(obj['x'], obj['y'], targets=targets)
        elif t == 'teleportgate':
            objects['gates'].append(Gates(obj['x1'], obj['y1'], obj['x2'], obj['y2'], targets[0]))
        elif t == 'pumpkin':
            objects['misc'].append(Pumpkin(obj['x'], obj['y'], targets))
        elif t == 'powerbox':
            objects['misc'].append(PowerBox(obj['x'], obj['y'], targets))

    return objects

        
