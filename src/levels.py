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
             {'x': 600, 'y': 430, 'range': 100}
        ]
    }
}

def load_level_data(level_data, platform_images):
 
    platforms = []
    platform_definitions = level_data['platforms']

    for platform_info in platform_definitions.get('standard', []):
        x_start = platform_info['x']
        y = platform_info['y']
        tile_count = platform_info['tiles']

        if tile_count == 1:
            platforms.append(Platform(x_start, y, platform_images['solid']))
        else:
            platforms.append(Platform(x_start, y, platform_images['left']))
            for i in range(1, tile_count - 1):
                x = x_start + i * TILE_SIZE
                platforms.append(Platform(x, y, platform_images['middle']))
            platforms.append(Platform(x_start + (tile_count - 1) * TILE_SIZE, y, platform_images['right']))

    for platform_info in platform_definitions.get('solid', []):
        platforms.append(Platform(platform_info['x'], platform_info['y'], platform_images['solid']))

    for platform_info in platform_definitions.get('moving', []):
        moving_platform = Platform(
            platform_info['x'],
            platform_info['y'],
            platform_images['solid'], 
            moving=True,
            move_range=platform_info.get('range', 0),
            start_direction=platform_info.get('direction', 1)
        )
        platforms.append(moving_platform)

    return platforms