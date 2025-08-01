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


start_x= 58*64
start_y=-1000

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
    def __init__(self,type):
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
        self.heroes = [None, None]  
        self.game_active = False
        self.platforms = platforms
        self.shot_bullets = []
        self.gates = []
        self.type=type
        self.TEAMS_SET=False

    def create_hero(self, char_name, x, y, index, username):
        print(f"Creating hero: {char_name} at ({x}, {y}) for player {index} ({username})")
        try:
            if char_name == "Roboman":
                hero = Roboman(x, y, screen_width, screen_height, index, username)
            elif char_name == "Ninja":
                hero = Ninja(x, y, screen_width, screen_height, [], index, username)
            elif char_name == "NinjaGirl":
                hero = NinjaGirl(x, y, screen_width, screen_height, [], index, username)
            elif char_name == "Archer":
                hero = Archer(x, y, [], index, username)
            else:
                print(f"Unknown character {char_name}, defaulting to Ninja")
                hero = Ninja(x, y, screen_width, screen_height, [], index, username)

            hero.character_name = char_name
            return hero
        except Exception as e:
            print(f"Error creating hero {char_name}: {e}")
            return Ninja(x, y, screen_width, screen_height, [], index, username)
        

    def client_thread(self, conn, player_index):
        print(f"Player {player_index} connected")
        try:
            initial_data = json.loads(conn.recv(1024).decode('utf-8'))
            username = initial_data.get("username", f"Player{player_index+1}")
            char_choice = initial_data.get("character", "Ninja")
            hero = self.create_hero(char_choice, 58*64, -2000, player_index + 1, username)
            self.heroes[player_index] = hero
            self.player_inputs[player_index] = {}
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
                self.player_inputs[player_index] = json.loads(data)
            except Exception as e:
                print(f"Client {player_index} error: {e}")
                break
        print(f"Player {player_index} disconnected.")
        self.clients[player_index] = None
        self.heroes[player_index] = None
        self.player_inputs[player_index] = {}
        conn.close()
        
    def set_teams(self):
        if self.TEAMS_SET:
            return
        if self.type=='1v1':
            self.team_A=[self.heroes[0]]
            self.team_B=[self.heroes[1]]
            
        else:
            self.team_A=[self.heros[0],self.heroes[1]]
            self.team_B=[self.heroes[2],self.heroes[3]]
            
        self.TEAMS_SET=True

    def game_loop(self):
        print("Game loop started")
        clock = pygame.time.Clock()
        while self.game_active:
            if not all(self.heroes):
                clock.tick(60)
                continue
            self.set_teams()
            try:
                if self.type == '1v1':
                    hero1, hero2 = self.heroes[0], self.heroes[1]
                    inputs1 = self.player_inputs.get(0, {})
                    inputs2 = self.player_inputs.get(1, {})

                    keys1 = {k: inputs1.get(kname, False) for k, kname in [
                        (pygame.K_a, "A"), (pygame.K_d, "D"), (pygame.K_w, "W"),
                        (pygame.K_LSHIFT, "LSHIFT"), (pygame.K_g, "G"),
                        (pygame.K_TAB, "TAB"), (pygame.K_RCTRL, "RCTRL"), (pygame.K_RALT, "RALT")]}
                    mouse1 = (inputs1.get("left_click", False), False, inputs1.get("right_click", False))

                    keys2 = {k: inputs2.get(kname, False) for k, kname in keys1.items()}
                    print("keys:")
                    print(keys2)
                    mouse2 = (inputs2.get("left_click", False), False, inputs2.get("right_click", False))

                    hero1.handle_input_online(keys1, self.gates, self.shot_bullets, bullet_class, None, mouse1)
                    hero2.handle_input_online(keys2, self.gates, self.shot_bullets, bullet_class, None, mouse2)

                    hero1.update_online(self.platforms, self.shot_bullets, [hero2], keys1, self.gates, None)
                    hero2.update_online(self.platforms, self.shot_bullets, [hero1], keys2, self.gates, None)

                    state_p1 = hero1.serialize()
                    state_p2 = hero2.serialize()
                    bullets_state = [b.serialize() for b in self.shot_bullets]

                    self.clients[0].sendall(json.dumps({
                        "self": state_p1,
                        "opponents": [state_p2],
                        "bullets": bullets_state
                    }).encode('utf-8') + b"\n")

                    self.clients[1].sendall(json.dumps({
                        "self": state_p2,
                        "opponents": [state_p1],
                        "bullets": bullets_state
                    }).encode('utf-8') + b"\n")

                    hero1.events = []
                    hero2.events = []

                elif self.type == '2v2':
                    hero1, hero2, hero3, hero4 = self.heroes
                    inputs = [self.player_inputs.get(i, {}) for i in range(4)]
                    keys = [{k: inp.get(kname, False) for k, kname in [
                        (pygame.K_a, "A"), (pygame.K_d, "D"), (pygame.K_w, "W"),
                        (pygame.K_LSHIFT, "LSHIFT"), (pygame.K_g, "G"),
                        (pygame.K_TAB, "TAB"), (pygame.K_RCTRL, "RCTRL"), (pygame.K_RALT, "RALT")]} for inp in inputs]
                    mice = [(inp.get("left_click", False), False, inp.get("right_click", False)) for inp in inputs]

                    heroes = [hero1, hero2, hero3, hero4]
                    for i in range(4):
                        heroes[i].handle_input_online(keys[i], self.gates, self.shot_bullets, bullet_class, None, mice[i])

                    for i in range(4):
                        targets = [h for j, h in enumerate(heroes) if j // 2 != i // 2]
                        heroes[i].update_online(self.platforms, self.shot_bullets, targets, keys[i], self.gates, None)

                    states = [h.serialize() for h in heroes]
                    bullets_state = [b.serialize() for b in self.shot_bullets]

                    # Players 0 and 1 are team A, 2 and 3 are team B
                    team_data = [
                        (0, 1, [states[2], states[3]]),
                        (1, 0, [states[2], states[3]]),
                        (2, 3, [states[0], states[1]]),
                        (3, 2, [states[0], states[1]]),
                    ]

                    for idx, mate_idx, opponents in team_data:
                        self.clients[idx].sendall(json.dumps({
                            "self": states[idx],
                            "teammate": states[mate_idx],
                            "opponents": opponents,
                            "bullets": bullets_state
                        }).encode('utf-8') + b"\n")

                clock.tick(60)

            except Exception as e:
                print(f"Game loop error: {e}")
                self.game_active = False

    def start(self):
        if self.type=='1v1': 
            self.server_socket.listen(2)
        else:
            self.server_socket.listen(4)
        print(f"Server started on {HOST}:{PORT}, waiting for 2 players...")
        self.clients = [None, None]  *1 if self.type=='1v1' else 2
        if self.type=='1v1':
            self.player_inputs = {0: {}, 1: {}}
        else:
            self.player_inputs = {0: {}, 1: {},2:{},3:{}}
        self.game_active = True
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True
        game_thread.start()
        while self.game_active:
            try:
                conn, addr = self.server_socket.accept()
                index = self.clients.index(None)
                self.clients[index] = conn
                thread = threading.Thread(target=self.client_thread, args=(conn, index))
                thread.daemon = True
                thread.start()
                print(f"Client connected: {addr}, assigned index: {index}")
            except Exception as e:
                print(f"Server error: {e}")
                self.game_active = False
        self.server_socket.close()

def main():
    print("1v1 or 2v2 :")
    kind=input()
    game = MultiplayerGame(kind)
    game.start()

if __name__ == "__main__":
    main()
    