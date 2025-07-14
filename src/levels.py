from src.engine.platform import Platform

TILE_SIZE = 64

level_1_data = {
    'player_start': {'x': 150, 'y': 400},
    'enemies': [
        {'x': 400, 'y': 500, 'type': 'ghost'},
        {'x': 900, 'y': 250, 'type': 'ghost2'}
    ],
    'platforms': {
        'standard': [
            {'x': 3 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 10},
            {'x': 19 * TILE_SIZE, 'y': 3 * TILE_SIZE, 'tiles': 8},
            {'x': 4 * TILE_SIZE, 'y': 6 * TILE_SIZE, 'tiles': 5},
            {'x': 21 * TILE_SIZE, 'y': 6 * TILE_SIZE, 'tiles': 4},
            {'x': 0, 'y': 8 * TILE_SIZE, 'tiles': 30},
        ],
        'solid': [
            {'x': 17 * TILE_SIZE, 'y': 5 * TILE_SIZE},
            {'x': 11 * TILE_SIZE, 'y': 7 * TILE_SIZE},
        ],
        'moving': [
            {'x': 600, 'y': 430, 'range': 100, 'tiles': 4, 'direction': 1}          ]
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
        platforms.append(
            Platform(info['x'], info['y'], platform_images['solid'])
        )

    for info in platform_definitions.get('moving', []):
        _add_tiled_platform(platforms, info, platform_images, moving=True)

    return platforms