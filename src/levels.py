from src.engine.platform import Platform
from src.engine.power_ups import Power_up

TILE_SIZE = 64





level_1_data = {
    'player_start': {'x': 2*TILE_SIZE, 'y':400},
    'enemies': [
        {'type': 'terrorist', 'x': 41 * TILE_SIZE , 'y': 400},
        {'type': 'drone', 'x': -400, 'y': 40, 'direction': 'right'},
        {'type': 'terrorist', 'x': 46 * TILE_SIZE , 'y': 400},
        {'type': 'gunman', 'x': 40 * TILE_SIZE , 'y': 400},
        {'type': 'gunman', 'x': 25 * TILE_SIZE , 'y': 400},
        {'type': 'terrorist', 'x': 15 * TILE_SIZE , 'y': 400},
        {'type': 'gunman', 'x': 49 * TILE_SIZE , 'y': -1*TILE_SIZE-110},
        {'type': 'terrorist', 'x': 53 * TILE_SIZE , 'y': -1*TILE_SIZE-110},        
        {'type': 'gunman', 'x': 44 * TILE_SIZE , 'y': 3*TILE_SIZE-110},
        {'type': 'gunman', 'x': 47 * TILE_SIZE , 'y': 3*TILE_SIZE-110},
    ],

    'objects': [
        {'type': 'bomb', 'x': 31 * TILE_SIZE , 'y': -9*TILE_SIZE-127},
        {'type': 'defusekit', 'x': 60 * TILE_SIZE + 100, 'y':200},
        {'type': 'teleportgate', 'x1': 58 * TILE_SIZE, 'y1': 363, 'x2': 62 * TILE_SIZE , 'y2':1*TILE_SIZE-150},
        {'type': 'pumpkin', 'x': 58 * TILE_SIZE + 150, 'y': 400 - 270-130},
        #{'type': 'powerbox', 'x': 58 * TILE_SIZE + 700, 'y': 465},
        {'type': 'power ups', 'x': -20 * TILE_SIZE + 200, 'y': 400 - 200, 'subtype': 'double jump'},
        {'type': 'power ups', 'x': 60 * TILE_SIZE + 200, 'y': 400 - 200, 'subtype': 'super power'},
        {'type': 'power ups', 'x':  7* TILE_SIZE + 200, 'y': -9*TILE_SIZE - 200, 'subtype': 'guard drone'}
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
level_2_data = {
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
level_3_data = {
    'player_start': {'x': 2013, 'y':400},
    'enemies': [
     {'type': 'flyingdemon', 'x': 58 * TILE_SIZE - 800, 'y': 382, 'direction': 'right'},
     {'type': 'gunman', 'x': 58 * TILE_SIZE - 1300, 'y': 382+17},
     {'type': 'terrorist', 'x': 58 * TILE_SIZE - 700, 'y': -1*TILE_SIZE},
     {'type': 'flyingdemon', 'x': 20 * TILE_SIZE, 'y': 2 * TILE_SIZE-100, 'direction': 'right'},
     {'type': 'gunman', 'x': 15 * TILE_SIZE, 'y': -2 * TILE_SIZE-113},
     {'type': 'terrorist', 'x': 3291, 'y': -182+70},
     {'type': 'gunman', 'x': 4664, 'y': 266},
     {'type': 'flyingdemon', 'x': 6071, 'y': 458-30, 'direction': 'left'},
     {'type': 'terrorist', 'x': 5538, 'y': 458},
     {'type': 'gunman', 'x': 6860, 'y': 486-30+6},
     {'type': 'flyingdemon', 'x': 7022+300, 'y': 38, 'direction': 'left'},
     {'type': 'terrorist', 'x': 6603, 'y': -154},
      {'type': 'gunman', 'x': 7183-10, 'y': -410-30+6},
      {'type': 'flyingdemon', 'x': 5851, 'y': -694, 'direction': 'right'},
      {'type': 'terrorist', 'x': 5352, 'y': -666},
      {'type': 'terrorist', 'x': 5352-300, 'y': -666},
      {'type': 'gunman', 'x': 5352-500, 'y': -666-30+5},
      {'type': 'drone', 'x': 5920-800, 'y': 458-500, 'direction': 'right'},
     
    ],

    'objects': [
        {'type': 'bomb', 'x': 4704, 'y':-655-50+4},
        {'type': 'defusekit', 'x': 58 * TILE_SIZE + 100, 'y': 400 - 270},
        {'type': 'teleportgate', 'x1': 2013, 'y1': 422-60, 'x2':6250, 'y2': 458-60+20+10},
        {'type': 'pumpkin', 'x': 2554, 'y': 202+60},
        {'type': 'pumpkin', 'x': 3693, 'y': 394+60},
        {'type': 'pumpkin', 'x': 4380, 'y': 74+60},
        {'type': 'pumpkin', 'x': 7180, 'y': 458+60},
        {'type': 'pumpkin', 'x': 7186, 'y': -438+60},
                {'type': 'power ups', 'x': 58*64 -400, 'y':400, 'subtype': 'double jump'},
                {'type': 'power ups', 'x': 58 * TILE_SIZE - 700, 'y': 2*TILE_SIZE, 'subtype': 'super power'},
                {'type': 'power ups', 'x': 58 * TILE_SIZE + 200, 'y': 0, 'subtype': 'guard drone'},
                {'type': 'defusekit', 'x': 19 * TILE_SIZE, 'y': 2 * TILE_SIZE-66},
                {'type': 'powerbox',  'x': 15 * TILE_SIZE, 'y': -2 * TILE_SIZE-48},
                {'type': 'powerbox',  'x': 3291, 'y': -182+70},
    ],
    'platforms': {
        'standard': [
            {'x': 1920, 'y': 8 * TILE_SIZE, 'tiles': 30},
            {'x': 70 * TILE_SIZE, 'y': 6* TILE_SIZE, 'tiles': 7},
            {'x': 80 * TILE_SIZE, 'y': 9* TILE_SIZE, 'tiles': 20},
            {'x': 103 * TILE_SIZE, 'y': 9 * TILE_SIZE, 'tiles': 14},
            {'x': 113 * TILE_SIZE, 'y': 6 * TILE_SIZE, 'tiles': 4},
            {'x': 110 * TILE_SIZE, 'y':2 * TILE_SIZE, 'tiles': 2},
            {'x': 100 * TILE_SIZE, 'y':-1 * TILE_SIZE, 'tiles': 9},
            {'x': 110 * TILE_SIZE, 'y':-5 * TILE_SIZE, 'tiles': 6},
            {'x': 103 * TILE_SIZE, 'y':-7 * TILE_SIZE, 'tiles': 3},
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
            {'x': 70 * TILE_SIZE, 'y': -9 * TILE_SIZE, 'tiles': 30},









        ],
        'solid': [
            {'x': 1920, 'y': 9 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 10 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 11 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 12 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 13 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 14 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 15 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 16 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 17 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 18 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 19 * TILE_SIZE, 'repeat':30},
            {'x':1920, 'y': 20 * TILE_SIZE, 'repeat':30},
            {'x':1920, 'y': 21 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 22 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 23 * TILE_SIZE, 'repeat':30},
            {'x': 1920, 'y': 24 * TILE_SIZE, 'repeat':30},

            
            {'x': 80 * TILE_SIZE, 'y': 10* TILE_SIZE, 'repeat': 20},
            {'x': 80 * TILE_SIZE, 'y': 11* TILE_SIZE, 'repeat': 20},
            {'x': 80 * TILE_SIZE, 'y': 12* TILE_SIZE, 'repeat': 20},
            {'x': 80 * TILE_SIZE, 'y': 13* TILE_SIZE, 'repeat': 20},
            {'x': 80 * TILE_SIZE, 'y':14* TILE_SIZE, 'repeat': 20},



        ],
        'moving': [
            {'x': 55 * TILE_SIZE, 'y': 2 * TILE_SIZE, 'tiles': 2,'range':2*TILE_SIZE, 'direction': 1},            
            {'x': 13 * TILE_SIZE, 'y': 1 * TILE_SIZE, 'tiles': 2,'range':2*TILE_SIZE, 'direction': 1},
]
    }
}
level_4_data = {
    'player_start': {'x': 10*64, 'y':400},
    'enemies': [
        {'type': 'terrorist', 'x': 6* TILE_SIZE, 'y': 1* TILE_SIZE},
        {'type': 'dragonlord', 'x': 10*64+1500, 'y':400},
        {'type': 'gunman', 'x': 28 * TILE_SIZE, 'y': 2* TILE_SIZE-115}
    ],

    'objects': [
      {'type': 'powerbox', 'x': 9 * TILE_SIZE, 'y': 2* TILE_SIZE +15},
      {'type': 'powerbox', 'x': 28 * TILE_SIZE+50, 'y': 1* TILE_SIZE +15}
    ],
    'platforms': {
        'standard': [
            
{'x': -19 * TILE_SIZE, 'y': 1* TILE_SIZE, 'tiles': 20},
{'x': 5 * TILE_SIZE, 'y': 3* TILE_SIZE, 'tiles': 10},
{'x': 1 * TILE_SIZE, 'y': 6* TILE_SIZE, 'tiles': 1},
{'x': 40 * TILE_SIZE, 'y': 6* TILE_SIZE, 'tiles': 7},

{'x': 28 * TILE_SIZE, 'y': 2* TILE_SIZE, 'tiles': 14},







        ],
        'solid': [
            {'x': 41*TILE_SIZE, 'y': 7 * TILE_SIZE, 'repeat':6},
            {'x': 41*TILE_SIZE, 'y': 8 * TILE_SIZE, 'repeat':6},
            {'x': 40*TILE_SIZE, 'y':7 * TILE_SIZE, 'repeat':1},
            {'x': 40*TILE_SIZE, 'y': 8 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 2 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 3 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 4 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 5 * TILE_SIZE, 'repeat':1},
             {'x': 0, 'y': 6 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 7 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 8 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 9 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 10 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 11 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 12 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 13 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 14 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 15 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 16 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 17 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 18 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 19 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 20 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 21 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 22 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 23 * TILE_SIZE, 'repeat':40},
            {'x': 0, 'y': 24 * TILE_SIZE, 'repeat':40},
            {'x': -19 * TILE_SIZE, 'y': 2* TILE_SIZE, 'repeat': 20},
            {'x': -19 * TILE_SIZE, 'y': 3* TILE_SIZE, 'repeat': 20},
            {'x': -19 * TILE_SIZE, 'y': 4* TILE_SIZE, 'repeat': 20},
            {'x': -19 * TILE_SIZE, 'y': 5* TILE_SIZE, 'repeat': 20},
            {'x': -19 * TILE_SIZE, 'y': 6* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 7* TILE_SIZE, 'repeat': 20},

{'x': -19 * TILE_SIZE, 'y': 8* TILE_SIZE, 'repeat': 20},

{'x': -19 * TILE_SIZE, 'y': 9* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 10* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 11* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 12* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 13* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 14* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 15* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 16* TILE_SIZE, 'repeat': 20},
{'x': -19 * TILE_SIZE, 'y': 17* TILE_SIZE, 'repeat': 20},


            
          



        ],
        'moving': [
            
]
    }
}


multiplayer_data = {
    'player_start': {'x': 58*64, 'y':400},
    'player2_start': {'x': 54*64, 'y':400},

    'enemies': [
       
    ],

    'objects': [

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
        {'type': 'dragonlord', 'x': 58 * TILE_SIZE - 200, 'y': 338}
        
    ],

    'objects': [
        
    ],
    'platforms': {
        'standard': [
          









        ],
        'solid': [
            {'x': 0, 'y': 6 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 7 * TILE_SIZE, 'repeat':1},
            {'x': 0, 'y': 8 * TILE_SIZE, 'repeat':1},
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
        'misc': [],
        'power ups':[]
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
                elif t == 'power ups':
                    objects['power ups'].append(Power_up(obj['x'], obj['y'], obj['subtype'], targets))

        return objects

        
