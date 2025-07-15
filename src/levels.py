from src.engine.platform import Platform

TILE_SIZE = 64





level_1_data = {
    'player_start': {'x': 58*64, 'y': 400},
    'enemies': [

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