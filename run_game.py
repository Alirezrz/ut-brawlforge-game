import pygame
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width
from src.engine.game import Game
from src.engine.menu import Menu, GameModeMenu, MapCharacterMenu,MultiplayerMapCharacterMenu, GameOverMenu
from src.engine.multiplayer_game import Game_2

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
    background = pygame.image.load("src/assets/images/city1.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    hero_profile_picture = pygame.image.load("src/assets/images/hero_profile.png")
    platform_image_path = "src/assets/images/"
    platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }

except (FileNotFoundError, pygame.error) as e:
    print(f"Error: Could not load asset: {e}")
    pygame.quit()
    exit()


while True:
    menu = Menu(screen, background)
    menu_action = menu.run()

    if menu_action == "exit":
        break 

    if menu_action == "settings":
        print("Settings menu not implemented yet!")
        continue 
    if menu_action == "start":
        while True:
            mode_menu = GameModeMenu(screen, background)
            mode = mode_menu.run()
            game = None

            if mode == "exit":
                break 

            if mode == "single":
                single_player_menu = MapCharacterMenu(screen, background, hero_profile_picture)
                result = single_player_menu.run()
                if result[0] == "exit":
                    break 
                selected_char, selected_map, _ = result
                game = Game(screen, platform_images, background, selected_char, selected_map)

            elif mode == "multi":
                multi_player_menu = MultiplayerMapCharacterMenu(screen, background, hero_profile_picture)
                result = multi_player_menu.run()
                if result[0] == "exit":
                    break 
                selected_char_list, selected_map, _ = result
                game = Game_2(screen, platform_images, background, selected_char_list[0], selected_char_list[1])
            if game:
                status, message = game.run()
                if status == "game_over":
                    game_over_menu = GameOverMenu(screen, background, message)
                    game_over_action = game_over_menu.run()
                    if game_over_action == "menu":
                        continue 
                    else: 
                        pygame.quit()
                        sys.exit()
                elif status == "menu":
                    break 
                
                elif status == "exit":
                    pygame.quit()
                    sys.exit()


pygame.quit()
sys.exit()