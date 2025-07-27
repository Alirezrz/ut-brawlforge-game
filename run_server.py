import socket
import threading
import json
import pygame
import os
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer
from config import screen_width, screen_height
from src.levels import multiplayer_data, load_level_data
from src.engine.bullet import Bullet
bullet_class=Bullet

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.display.init()
pygame.display.set_mode((1, 1))

pygame.init()

# Load platforms
platform_image_path = "src/assets/images/"
platform_images = {}
try:
    platform_images = {
        'left': pygame.image.load(platform_image_path + "platform_left.png").convert_alpha(),
        'middle': pygame.image.load(platform_image_path + "platform_middle.png").convert_alpha(),
        'right': pygame.image.load(platform_image_path + "platform_right.png").convert_alpha(),
        'solid': pygame.image.load(platform_image_path + "platform_solid.png").convert_alpha(),
    }
    print("Platform images loaded successfully")
except Exception as e:
    print(f"Error loading platform images: {e}")
    platform_images = {key: pygame.Surface((100, 20)) for key in ['left', 'middle', 'right', 'solid']}
    for surface in platform_images.values():
        surface.fill((100, 100, 100))

try:
    platforms = load_level_data(multiplayer_data, platform_images)
    print("Platforms loaded successfully")
except Exception as e:
    print(f"Error loading platforms: {e}")
    platforms = []

HOST = "0.0.0.0"
PORT = 9191

class MultiplayerGame:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((HOST, PORT))
            print(f"Server socket bound to {HOST}:{PORT}")
        except Exception as e:
            print(f"Error binding server socket: {e}")
            exit()
        self.clients = []
        self.player_inputs = {}
        self.heroes = {}
        self.game_active = False
        self.platforms = platforms
        self.shot_bullets = []
        self.gates = []

    def create_hero(self, char_name, x, y, index, username):
        print(f"Creating hero: {char_name} at ({x}, {y}) for player {index} ({username})")
        try:
            if char_name == "Roboman":
                return Roboman(x, y, screen_width, screen_height, index, username)
            if char_name == "Ninja":
                return Ninja(x, y, screen_width, screen_height, [], index, username)
            if char_name == "NinjaGirl":
                return NinjaGirl(x, y, screen_width, screen_height, [], index, username)
            if char_name == "Archer":
                return Archer(x, y, [], index, username)
            print(f"Unknown character {char_name}, defaulting to Ninja")
            return Ninja(x, y, screen_width, screen_height, [], index, username)
        except Exception as e:
            print(f"Error creating hero {char_name}: {e}")
            return Ninja(x, y, screen_width, screen_height, [], index, username)

    def client_thread(self, conn, player_index):
        print(f"Player {player_index} connected")
        try:
            initial_data = json.loads(conn.recv(1024).decode('utf-8'))
            username = initial_data.get("username", f"Player{player_index+1}")
            char_choice = initial_data.get("character", "Ninja")
            hero = self.create_hero(char_choice, 400 + player_index * 400, 400, player_index + 1, username)
            self.heroes[conn] = hero
            self.player_inputs[conn] = {}
            conn.sendall(json.dumps({"status": "setup_complete"}).encode('utf-8'))
            print(f"Player {player_index} setup complete: {username} as {char_choice}")
        except Exception as e:
            print(f"Error with client {player_index} during setup: {e}")
            conn.close()
            return
        while True:
            try:
                data = conn.recv(2048).decode('utf-8')
                if not data:
                    break
                self.player_inputs[conn] = json.loads(data)
            except Exception as e:
                print(f"Client {player_index} error: {e}")
                break
        print(f"Player {player_index} disconnected.")
        if conn in self.clients:
            self.clients.remove(conn)
        if conn in self.heroes:
            del self.heroes[conn]
        if conn in self.player_inputs:
            del self.player_inputs[conn]
        conn.close()

    def game_loop(self):
        print("here1")
        clock = pygame.time.Clock()
        while self.game_active:
            if len(self.heroes) < 2:
                print(f"Waiting for second player... Current heroes: {len(self.heroes)}")
                clock.tick(60)
                continue

            try:
                hero1, hero2 = list(self.heroes.values())
                print(f"Hero1: {hero1.__class__.__name__}, x_pos={hasattr(hero1, 'x_pos')}")
                print(f"Hero2: {hero2.__class__.__name__}, x_pos={hasattr(hero2, 'x_pos')}")
                inputs1 = self.player_inputs.get(self.clients[0], {})
                inputs2 = self.player_inputs.get(self.clients[1], {})

                keys1 = {
                    pygame.K_a: inputs1.get("A", False),
                    pygame.K_d: inputs1.get("D", False),
                    pygame.K_w: inputs1.get("W", False),
                    pygame.K_LSHIFT: inputs1.get("LSHIFT", False),
                    pygame.K_g: inputs1.get("G", False),
                    pygame.K_TAB: inputs1.get("TAB", False),
                    pygame.K_RCTRL: inputs1.get("RCTRL", False),
                    pygame.K_RALT: inputs1.get("RALT", False)
                }
                mouse1 = (inputs1.get("left_click", False), False, inputs1.get("right_click", False))

                keys2 = {
                    pygame.K_a: inputs2.get("A", False),
                    pygame.K_d: inputs2.get("D", False),
                    pygame.K_w: inputs2.get("W", False),
                    pygame.K_LSHIFT: inputs2.get("LSHIFT", False),
                    pygame.K_g: inputs2.get("G", False),
                    pygame.K_TAB: inputs2.get("TAB", False),
                    pygame.K_RCTRL: inputs2.get("RCTRL", False),
                    pygame.K_RALT: inputs2.get("RALT", False)
                }
                mouse2 = (inputs2.get("left_click", False), False, inputs2.get("right_click", False))
                # hero1.handle_input( keys1, self.gates, self.shot_bullets, bullet_class,None, mouse1)
                # hero2.handle_input( keys2, self.gates, self.shot_bullets, bullet_class,None, mouse2)

                hero1.update_online(self.platforms, self.shot_bullets, [hero2], keys1, self.gates, None)
                hero2.update_online(self.platforms, self.shot_bullets, [hero1], keys2, self.gates, None)


                state_p1 = hero1.serialize()
                state_p2 = hero2.serialize()
                
                response_for_p1 = {"self": state_p1, "opponent": state_p2}
                response_for_p2 = {"self": state_p2, "opponent": state_p1}
                
                self.clients[0].sendall(json.dumps(response_for_p1).encode('utf-8'))
                self.clients[1].sendall(json.dumps(response_for_p2).encode('utf-8'))
                
                print(f"Sent states: P1({hero1.x_pos},{hero1.y_pos}), P2({hero2.x_pos},{hero2.y_pos})")
                print(f"Hero1 x_pos: {hero1.x_pos}")
                clock.tick(60)
                
            except Exception as e:
                print(f"Game loop error: {e}")
                if len(self.heroes) < 2:
                    print("Not enough heroes, reverting to waiting state")
                else:
                    self.game_active = False

    def start(self):
        self.server_socket.listen(2)
        print(f"Server started on {HOST}:{PORT}, waiting for 2 players...")
        self.game_active = True
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True
        game_thread.start()
        while self.game_active:
            try:
                conn, addr = self.server_socket.accept()
                self.clients.append(conn)
                thread = threading.Thread(target=self.client_thread, args=(conn, len(self.clients) - 1))
                thread.daemon = True
                thread.start()
                print(f"Client connected: {addr}, total clients: {len(self.clients)}")
            except Exception as e:
                print(f"Server error: {e}")
                self.game_active = False
        self.server_socket.close()

def main():
    game = MultiplayerGame()
    game.start()

if __name__ == "__main__":
    main()