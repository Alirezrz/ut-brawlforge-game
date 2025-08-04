import pygame
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width
from src.engine.game import Game
from src.engine.menu import Menu, GameModeMenu, MapCharacterMenu,MultiplayerMapCharacterMenu, GameOverMenu,MatchmakingMenu,NetworkMenu,LobbyMenu,JoinGameMenu,MultiplayerCharacterSelectMenu
from src.engine.multiplayer_game import Game_2
from src.engine.network import Network
from Client import Client

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
                network_handler = Network()
                network_menu = NetworkMenu(screen, background, network_handler)
                
                if network_menu.run() == "connected":
                    multiplayer_active = True
                    while multiplayer_active:
                        match_menu = MatchmakingMenu(screen, background, network_handler)
                        action, data = match_menu.run()
                        
                        lobby_result = None
                        if action == "lobby":
                            lobby_menu = LobbyMenu(screen, background, network_handler, data, is_host=True)
                            lobby_result = lobby_menu.run()
                        elif action == "join_menu":
                            join_menu = JoinGameMenu(screen, background, network_handler)
                            join_action, _ = join_menu.run()
                            if join_action == "wait_for_acceptance":
                                lobby_menu = LobbyMenu(screen, background, network_handler, {"game_id": join_menu.game_id, "players":[]}, is_host=False)
                                lobby_result = lobby_menu.run()
                        
                        if lobby_result == "start_game":
                            char_select_menu = MultiplayerCharacterSelectMenu(screen, background)
                            selected_hero = char_select_menu.run()

                            if selected_hero:
                                game_client = Client(
                                    network_handler.client,
                                    network_handler.username,
                                    network_handler.player_id,
                                    selected_hero
                                )
                                game_client.start()
                                multiplayer_active = False
                            else:
                                multiplayer_active = False 
                        else:
                            multiplayer_active = False 
                
                network_handler.disconnect()
                
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