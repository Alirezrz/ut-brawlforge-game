import pygame
import sys
import os
import json
import socket
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width
from src.engine.game import Game
from src.engine.menu import Menu, GameModeMenu, MapCharacterMenu,MultiplayerMapCharacterMenu, GameOverMenu,MatchmakingMenu,NetworkMenu,LobbyMenu,JoinGameMenu,MultiplayerCharacterSelectMenu,SearchPlayerMenu,LoginSignupMenu,OnlineActionMenu,JoinMethodMenu,TextInputMenu,OnlineLobbyMenu 
from src.engine.multiplayer_game import Game_2
from src.engine.network import Network
from Client import Client
from Client_online import Client as ClientOnline 
from client_connector import ClientConnector
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
    background1 = pygame.image.load("src/assets/images/city1.png")
    background1 = pygame.transform.scale(background1, (screen_width, screen_height))
    background2 = pygame.image.load("src/assets/images/city2.png")
    background2 = pygame.transform.scale(background2, (screen_width, screen_height))
    background3 = pygame.image.load("src/assets/images/city3.png")
    background3 = pygame.transform.scale(background3, (screen_width, screen_height))
    background4 = pygame.image.load("src/assets/images/city4.png")
    background4 = pygame.transform.scale(background4, (screen_width, screen_height))
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


def display_temporary_message(screen, background, message, duration=2000):
    font = pygame.font.Font(None, 60)
    text_surf = font.render(message, True, (255, 200, 200))
    text_rect = text_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(background, (0, 0))
        screen.blit(text_surf, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def wait_for_server_response(screen, background, sock):
    """Displays a waiting screen and listens for a simple TEXT response."""
    font = pygame.font.Font(None, 60)
    wait_text = font.render("Waiting for Host Approval...", True, (255, 255, 255))
    wait_rect = wait_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    
    sock.settimeout(45.0) 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sock.settimeout(None)
                return "exit"
        
        try:
           
            data = sock.recv(1024).decode('utf-8').strip()
            if data:
                sock.settimeout(None) 
                return data
        except socket.timeout:
            print("[CLIENT] Timed out waiting for host response.")
            sock.settimeout(None)
            return "timeout"
        except (socket.error, ConnectionResetError) as e:
            print(f"Error while waiting for response: {e}")
            return "error"

        screen.blit(background, (0, 0))
        screen.blit(wait_text, wait_rect)
        pygame.display.flip()

while True:
    menu = Menu(screen, background1)
    menu_action = menu.run()

    if menu_action == "exit":
        break 
    if menu_action == "start":
        start_menu_running = True
        while start_menu_running:
            mode_menu = GameModeMenu(screen, background1)
            mode = mode_menu.run()

            if mode == "exit":
                break

            game = None

            if mode == "single":
                single_player_menu = MapCharacterMenu(screen, background1, hero_profile_picture)
                result = single_player_menu.run()
                if result[0] == "exit":
                    continue
                selected_char, selected_map, _ = result
                if selected_map=='level1':
                    game = Game(screen, platform_images, background1, selected_char, selected_map)
                elif selected_map=='level2':
                     game = Game(screen, platform_images, background2, selected_char, selected_map)
                elif selected_map=='level3':
                     game = Game(screen, platform_images, background4, selected_char, selected_map)
                elif selected_map=='Boss fight':
                     game = Game(screen, platform_images, background3, selected_char, selected_map)

        
            elif mode == "multi":
                network_handler = Network()
                network_menu = NetworkMenu(screen, background1, network_handler)
                
                if network_menu.run() == "connected":
                    multiplayer_active = True
                    while multiplayer_active:
                        match_menu = MatchmakingMenu(screen, background1, network_handler)
                        action, data = match_menu.run()
                        
                        lobby_result = None
                        if action == "lobby":
                            lobby_menu = LobbyMenu(screen, background1, network_handler, data, is_host=True)
                            lobby_result = lobby_menu.run()
                        elif action == "join_menu":
                            join_menu = JoinGameMenu(screen, background1, network_handler)
                            join_action, _ = join_menu.run()
                            if join_action == "wait_for_acceptance":
                                waiting_for_response = True
                                while waiting_for_response:
                                    screen.blit(background1, (0, 0))
                                    font = pygame.font.Font(None, 60)
                                    wait_text = font.render("Waiting for host to accept...", True, (255, 255, 255))
                                    screen.blit(wait_text, wait_text.get_rect(center=(screen_width/2, screen_height/2)))
                                    pygame.display.flip()

                                    response = network_handler.recv_json() 
                                    if response:
                                        waiting_for_response = False
                                        if response.get("type") == "join_accepted":
                                            lobby_menu = LobbyMenu(screen, background1, network_handler, response, is_host=False)
                                            lobby_result = lobby_menu.run()
                                        else:
                                            print(f"Could not join lobby: {response.get('message')}")
                                            lobby_result = "exit"
                        elif action == "search_player":
                            search_menu = SearchPlayerMenu(screen, background1, network_handler)
                            search_action, _ = search_menu.run()
                            if search_action == "wait_for_response":
                                print("Request sent. Waiting for player to respond...")
                                continue

                        print(f"[CLIENT DEBUG] LobbyMenu finished and returned: {lobby_result}") # DEBUG PRINT
                        if lobby_result == "start_game":
                            char_select_menu = MultiplayerCharacterSelectMenu(screen, background1)
                            selected_hero = char_select_menu.run()
                            print(f"DEBUG [run_game.py]: Character selected from menu is '{selected_hero}'")
                            if selected_hero:
                                print("[CLIENT DEBUG] Character selected. Starting game client...") # DEBUG PRINT
                        
                                game_client = Client(network_handler.client, network_handler.username, network_handler.player_id, selected_hero, background1)
                                action_after_game = game_client.start() 
                                if action_after_game == "exit":
                                    multiplayer_active = False
                                    start_menu_running = False 
                                else:
                                    multiplayer_active = False
                            else:
                               
                                multiplayer_active = False
                        else:
                           
                            multiplayer_active = False
                
                network_handler.disconnect()
            elif mode == "online":
                login_menu = LoginSignupMenu(screen, background1)
                
                while True:
                    action, username, password = login_menu.run()

                    if action in ["back", "exit"]:
                        break

                    if not username or not password:
                        login_menu.message = "Username and password are required."
                        login_menu.message_color = (255, 100, 100)
                        continue

                    connector = ClientConnector()
                    connected, msg = connector.connect_to_server()

                    if not connected:
                        login_menu.message = "Connection to server failed."
                        login_menu.message_color = (255, 100, 100)
                        continue

                    action_code = "1" if action == "login" else "2"
                    success, message = connector.authenticate(action_code, username, password)

                    if success:
                        online_action_menu = OnlineActionMenu(screen, background1)
                        
                        while True: 
                            online_action = online_action_menu.run()

                            if online_action in ["back", "exit"]:
                                connector.client_socket.close()
                                break 

                            lobby_result = None
                            
                            if "create" in online_action:
                                game_type = "1v1" if "1v1" in online_action else "2v2"
                                connector.client.sendall(b'1') 
                                connector.client.recv(1024)
                                connector.client.sendall(b'1' if game_type == '1v1' else b'2')
                                
                                print("[CLIENT] Waiting for server confirmation of lobby creation...")
                                try:
                                    confirmation_msg = connector.client.recv(1024).decode()
                                    print(f"[SERVER] {confirmation_msg}")
                                except socket.timeout:
                                    print("[CLIENT] Timed out waiting for lobby confirmation.")
                                    continue
                                
                                print("[CLIENT] Entering lobby screen...")
                                initial_data = {"game_id": "Syncing...", "players": [username], "game_type": game_type}
                                lobby_menu = OnlineLobbyMenu(screen, background1, connector, initial_data, is_host=True)
                                lobby_result = lobby_menu.run()

                            elif online_action == "join_game":
                                connector.client.sendall(b'2')
                                connector.client.recv(1024)
                                
                                join_method_menu = JoinMethodMenu(screen, background1)
                                join_action = join_method_menu.run()

                                join_request_sent = False
                                if join_action == "search_id":
                                    connector.client.sendall(b'1')
                                    text_input_menu = TextInputMenu(screen, background1, "Enter Host ID or Username")
                                    game_id = text_input_menu.run()
                                    if game_id:
                                        connector.client.recv(1024)
                                        connector.client.sendall(game_id.encode())
                                        join_request_sent = True
                                
                                elif join_action == "server_decide":
                                    connector.client.sendall(b'2')
                                    join_request_sent = True

                                if join_request_sent:

                                    response_text = wait_for_server_response(screen, background1, connector.client)
                                    
                                    if response_text and "accepted" in response_text.lower():
                                        print("[CLIENT] Join request accepted! Entering lobby...")
                                        accepted_data = {"game_id": "Joined", "players": ["You", "Host"], "game_type": "N/A"}
                                        lobby_menu = OnlineLobbyMenu(screen, background1, connector, accepted_data, is_host=False)
                                        lobby_result = lobby_menu.run()
                                    else:
                                        display_temporary_message(screen, background1, response_text or "Join Failed!")
                            if lobby_result == "start_game":
                                char_menu = MultiplayerCharacterSelectMenu(screen, background1)
                                selected_hero = char_menu.run()
                                if selected_hero:
                                    game_client = ClientOnline(connector.client_socket, connector.username, connector.client_id, selected_hero, background1)
                                    action_after_game = game_client.start()
                                    if action_after_game == "exit":
                                        start_menu_running = False
                                        break
                                    else: 
                                        break 
                                
                        if not start_menu_running: break
                    else:
                        login_menu.message = message
                        login_menu.message_color = (255, 100, 100)
                continue
            if game: 
                status, message = game.run()
                if status == "game_over":
                    game_over_menu = GameOverMenu(screen, background1, message)
                    game_over_action = game_over_menu.run()
                    if game_over_action == "menu":
                        continue
                    else: 
                        start_menu_running = False
                        menu_action = "exit"
                elif status == "menu":
                    continue
                elif status == "exit":
                    start_menu_running = False
                    menu_action = "exit"
            
            if menu_action == "exit":
                break
pygame.quit()
sys.exit()

