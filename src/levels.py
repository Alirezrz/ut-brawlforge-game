from src.engine.platform import Platform 


level_1_data = {
    'platforms': [
        
        {'x': 600, 'y': 430, 'moving': True, 'range': 100},
        {'x': 664, 'y': 430, 'moving': True, 'range': 100},
        {'x': 728, 'y': 430, 'moving': True, 'range': 100},
        {'x': 792, 'y': 430, 'moving': True, 'range': 100},
        {'x': 856, 'y': 430, 'moving': True, 'range': 100},
        
        
        {'x': 864, 'y': 340},
        {'x': 928, 'y': 340},
        {'x': 992, 'y': 340},
       
        
      
        *[{'x': i * 64, 'y': 600} for i in range(20)]
    ],
    'enemies': [
      
        {'x': 400, 'y': 550, 'type': 'ghost'},
        {'x': 900, 'y': 300, 'type': 'ghost2'}
    ],
    'player_start': {
        'x': 200,
        'y': 250 - 118 - 20
    }
}





def load_level(level_data, platform_image):
    """
    این تابع داده‌های خام مرحله را می‌گیرد و لیست آبجکت‌های پلتفرم را برمی‌گرداند.
    """
    platforms = []
    for platform_info in level_data['platforms']:
        x = platform_info.get('x')
        y = platform_info.get('y')
        moving = platform_info.get('moving', False) 
        move_range = platform_info.get('range', 0)
        start_direction = platform_info.get('direction', 1)

        platforms.append(
            Platform(x, y, platform_image, moving=moving, move_range=move_range, start_direction=start_direction)
        )
    return platforms