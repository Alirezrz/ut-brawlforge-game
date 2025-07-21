import pygame
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height, explode_side_size, enenmy_health_bar_height, enenmy_health_bar_width
from src.engine.game import Game
from src.engine.menu import Menu, GameModeMenu, MapCharacterMenu,MultiplayerMapCharacterMenu
import src.levels as levels_module
from src.engine.multiplayer_game import Game_2
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")

try:
    icon = pygame.image.load("src/assets/images/icon.jpg")
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print("Warning: Icon image not found. Continuing without icon.")

try:
    sound_path = os.path.join("src", "assets", "sounds", "RoboMan")
    background = pygame.image.load("src/assets/images/BrawlhalaBackground.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    hero_profile_picture = pygame.image.load("src/assets/images/hero_profile.png") 
    ghost = pygame.image.load("src/assets/images/ghost.png")
    ghost = pygame.transform.scale(ghost, (64, 64))
    ghost2 = pygame.image.load("src/assets/images/ghost2.png")
    ghost2 = pygame.transform.scale(ghost2, (64, 64))
    platform_image_path = "src/assets/images/"
    platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }
    platform_tileset_picture = pygame.image.load("src/assets/images/platform.jpg")
    explode_picture = pygame.image.load("src/assets/images/explode.png")
    ninja_health_bar_frame = pygame.image.load("src/assets/images/Ninja/Ninja_health_bar_frame.png")
    ninja_health_bar = pygame.image.load("src/assets/images/Ninja/ninja_health_bar.png")
    archer_health_bar_frame = pygame.image.load("src/assets/images/Archer/health_bar_frame.png")
    archer_health_bar = pygame.image.load("src/assets/images/Archer/health_bar.png")
    explode_picture = pygame.transform.scale(explode_picture, (explode_side_size, explode_side_size))
    health_bar_green = pygame.image.load("src/assets/images/green_image.jpg")
    health_bar_green = pygame.transform.scale(health_bar_green, (enenmy_health_bar_width, enenmy_health_bar_height))
    health_bar_red = pygame.image.load("src/assets/images/red_image.jpg")
    health_bar_red = pygame.transform.scale(health_bar_red, (enenmy_health_bar_width, enenmy_health_bar_height))
    roboman_health_bar_frame = pygame.image.load("src/assets/images/RoboMan_pictures/Roboman_health_bar_frame.png")
    roboman_health_bar = pygame.image.load("src/assets/images/RoboMan_pictures/Roboman_health_bar.png")
    shoot_sound = pygame.mixer.Sound(os.path.join(sound_path, "shoot.wav"))
    jump_sound = pygame.mixer.Sound(os.path.join(sound_path, "robot jump.MP3"))
    jetpack_sound = pygame.mixer.Sound(os.path.join(sound_path, "jetpack.wav"))
    explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, "shot_hit_platoform.mp3"))
    enemy_hit_sound = pygame.mixer.Sound(os.path.join(sound_path, "shot_hit_enemy.wav"))
    game_sounds = {
        "shoot": shoot_sound,
        "jump": jump_sound,
        "jetpack": jetpack_sound,
        "explosion": explosion_sound,
        "enemy_hit": enemy_hit_sound
    }
    shoot_sound.set_volume(0.5)
    jump_sound.set_volume(0.7)

except (FileNotFoundError, pygame.error) as e:
    print(f"Error: Could not load asset: {e}")
    pygame.quit()
    exit() 

while True:
    menu = Menu(screen, background)
    menu_action = menu.run()
    if menu_action == "start":
        mode_menu = GameModeMenu(screen, background)
        mode = mode_menu.run()
        if mode == "single":
            single_player_menu = MapCharacterMenu(screen, background, hero_profile_picture) # تغییر اینجا
            result = single_player_menu.run() 
            
            if result[0] == "exit": 
                continue

            selected_char, selected_map, _ = result
            player_start_pos = levels_module.get_start_position(selected_map,player_index = 1)

            main_character = None
            if selected_char == "Roboman":
                main_character = Roboman(
                    player_start_pos['x'], player_start_pos['y'],
                    roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
                    screen_width, screen_height,
                    sounds=game_sounds,
                    trigger_shutter_callback=None 
                )
            elif selected_char == "NinjaGirl":
                main_character = NinjaGirl(
                    player_start_pos['x'], player_start_pos['y'],
                    screen_width, screen_height,
                    [], # targets
                    ninja_health_bar_frame, ninja_health_bar
                )
            elif selected_char == "Ninja":
                main_character = Ninja(
                    player_start_pos['x'], player_start_pos['y'],
                    screen_width, screen_height,
                    [], # targets
                    ninja_health_bar_frame, ninja_health_bar
                )
            elif selected_char == "Archer":
                main_character = Archer(
                    player_start_pos['x'], player_start_pos['y'],
                    screen_width, screen_height, 
                    [], # targets
                    archer_health_bar_frame, archer_health_bar
                )

            game = Game(
                screen, hero_profile_picture, ghost, ghost2,
                platform_images, background, explode_picture,
                health_bar_green, health_bar_red, hero_profile_picture,
                roboman_health_bar_frame, roboman_health_bar,
                game_sounds, ninja_health_bar_frame, ninja_health_bar,
                archer_health_bar_frame, archer_health_bar,
                main_character=main_character,
                selected_map=selected_map
            )

        elif mode == "multi": 
            multi_player_menu = MultiplayerMapCharacterMenu(screen, background, hero_profile_picture) # تغییر اینجا
            result = multi_player_menu.run()

            if result[0] == "exit": 
                continue

            selected_char_list, selected_map, _ = result 
            player1_char_name = selected_char_list[0]
            player2_char_name = selected_char_list[1]

            player1_start_pos = levels_module.get_start_position(selected_map, player_index=1)
            player2_start_pos = levels_module.get_start_position(selected_map, player_index=2) 

            hero1 = None
            hero2 = None
            if player1_char_name == "Roboman":
                hero1 = Roboman(player1_start_pos['x'], player1_start_pos['y'],
                                roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
                                screen_width, screen_height, sounds=game_sounds)
            elif player1_char_name == "NinjaGirl":
                hero1 = NinjaGirl(player1_start_pos['x'], player1_start_pos['y'],
                                  screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player1_char_name == "Ninja":
                hero1 = Ninja(player1_start_pos['x'], player1_start_pos['y'],
                              screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player1_char_name == "Archer":
                hero1 = Archer(player1_start_pos['x'], player1_start_pos['y'],
                               screen_width, screen_height, [], archer_health_bar_frame, archer_health_bar)

            if player2_char_name == "Roboman":
                hero2 = Roboman(player2_start_pos['x'], player2_start_pos['y'],
                                roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
                                screen_width, screen_height, sounds=game_sounds)
            elif player2_char_name == "NinjaGirl":
                hero2 = NinjaGirl(player2_start_pos['x'], player2_start_pos['y'],
                                  screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player2_char_name == "Ninja":
                hero2 = Ninja(player2_start_pos['x'], player2_start_pos['y'],
                              screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player2_char_name == "Archer":
                hero2 = Archer(player2_start_pos['x'], player2_start_pos['y'],
                               screen_width, screen_height, [], archer_health_bar_frame, archer_health_bar)
            game = Game_2(
                screen,
                platform_images,
                background, explode_picture,
                game_sounds,
                ninja_health_bar_frame, ninja_health_bar,
                roboman_health_bar_frame, roboman_health_bar,
                hero_profile_picture, 
                selected_map , hero1=hero1,hero2=hero2
            )

        elif mode == "exit":
            pygame.quit()
            sys.exit() 
        else:
            continue 

    elif menu_action == "settings":
        print("Settings menu not implemented yet!")
    elif menu_action == "exit":
        pygame.quit()
        sys.exit() 

    if 'game' in locals() and game: 
        game_result = game.run() 
        if game_result == "menu":
            continue
        elif game_result == "exit":
            pygame.quit()
            sys.exit() 