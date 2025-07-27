import os
import threading
import socket
import json
import time
import pygame
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from config import screen_width, screen_height
from src.levels import multiplayer_data, load_level_data

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")

# Load platform images
platform_image_path = "src/assets/images/"
platform_images = {
    'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
    'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
    'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
    'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
}

# Load background
background = pygame.image.load("src/assets/images/city1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Configuration
HOST = "0.0.0.0"  # Server listens on all interfaces
PORT = 9191
SERVER_IP = "127.0.0.1"  # Clients connect to localhost by default; change for remote server

class Server:
    def __init__(self, screen, platforms, background, hero_choice):
        self.screen = screen
        self.platforms = platforms
        self.background = background
        self.hero_choice = hero_choice
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.clients = []
        self.heroes = {}
        self.player_inputs = {}
        self.game_active = False
        self.shot_bullets = []
        self.gates = []  # Assuming gates are empty for simplicity; extend if needed

    def create_hero(self, char_name, x, y, index, username):
        # Create hero based on character name
        if char_name == "Roboman":
            return Roboman(x, y, screen_width, screen_height, index, username)
        if char_name == "Ninja":
            return Ninja(x, y, screen_width, screen_height, [], index, username)
        return Ninja(x, y, screen_width, screen_height, [], index, username)  # Default to Ninja

    def client_thread(self, conn, player_index):
        print(f"Player {player_index} connected")
        try:
            # Receive initial data (username and character choice)
            initial_data = json.loads(conn.recv(1024).decode('utf-8'))
            username = initial_data.get("username", f"Player{player_index+1}")
            char_choice = initial_data.get("character", "Ninja")
            # Create hero with specified position and index
            hero = self.create_hero(char_choice, 400 + player_index * 400, 400, player_index + 1, username)
            self.heroes[conn] = hero
            self.player_inputs[conn] = {}
            conn.sendall(json.dumps({"status": "setup_complete"}).encode('utf-8'))
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
            except:
                break
        print(f"Player {player_index} disconnected.")
        self.clients.remove(conn)
        del self.heroes[conn]
        del self.player_inputs[conn]
        conn.close()

    def game_loop(self):
        clock = pygame.time.Clock()
        while self.game_active and len(self.heroes) == 2:
            # Get heroes and their inputs
            hero_list = list(self.heroes.values())
            hero1, hero2 = hero_list
            inputs1 = self.player_inputs.get(self.clients[0], {})
            inputs2 = self.player_inputs.get(self.clients[1], {})

            # Process inputs for hero1
            keys1 = {pygame.K_a: inputs1.get("A", False),
                     pygame.K_d: inputs1.get("D", False),
                     pygame.K_w: inputs1.get("W", False),
                     pygame.K_LSHIFT: inputs1.get("LSHIFT", False),
                     pygame.K_g: inputs1.get("G", False),
                     pygame.K_TAB: inputs1.get("TAB", False),
                     pygame.K_RCTRL: inputs1.get("RCTRL", False),
                     pygame.K_RALT: inputs1.get("RALT", False)}
            mouse1 = (inputs1.get("left_click", False), False, inputs1.get("right_click", False))

            # Process inputs for hero2
            keys2 = {pygame.K_a: inputs2.get("A", False),
                     pygame.K_d: inputs2.get("D", False),
                     pygame.K_w: inputs2.get("W", False),
                     pygame.K_LSHIFT: inputs2.get("LSHIFT", False),
                     pygame.K_g: inputs2.get("G", False),
                     pygame.K_TAB: inputs2.get("TAB", False),
                     pygame.K_RCTRL: inputs2.get("RCTRL", False),
                     pygame.K_RALT: inputs2.get("RALT", False)}
            mouse2 = (inputs2.get("left_click", False), False, inputs2.get("right_click", False))

            # Update heroes with their respective inputs
            hero1.update(self.platforms, self.shot_bullets, [hero2], keys1, self.gates, None)
            hero2.update(self.platforms, self.shot_bullets, [hero1], keys2, self.gates, None)

            # Check for bullet collisions between heroes
            for bullet in self.shot_bullets[:]:
                if bullet.owner == "Roboman" and bullet.hitbox.colliderect(hero2.hitbox):
                    hero2.health -= bullet.damage
                    hero2.hurt()
                    self.shot_bullets.remove(bullet)
                elif bullet.owner == "Ninja" and bullet.hitbox.colliderect(hero1.hitbox):
                    hero1.health -= bullet.damage
                    hero1.hurt()
                    self.shot_bullets.remove(bullet)

            # Serialize game state
            state_p1 = hero1.serialize()
            state_p2 = hero2.serialize()
            response_for_p1 = {"self": state_p1, "opponent": state_p2}
            response_for_p2 = {"self": state_p2, "opponent": state_p1}

            # Send game state to clients
            try:
                self.clients[0].sendall(json.dumps(response_for_p1).encode('utf-8'))
                self.clients[1].sendall(json.dumps(response_for_p2).encode('utf-8'))
            except Exception as e:
                print(f"Error sending state, ending game: {e}")
                self.game_active = False

            # Render server view
            self.screen.blit(self.background, (0, 0))
            for platform in self.platforms:
                platform.draw(self.screen, [0, 0])
            hero1.display(self.screen, [0, 0], self.shot_bullets)
            hero2.display(self.screen, [0, 0], self.shot_bullets)
            pygame.display.update()

            clock.tick(30)

    def start(self):
        self.server_socket.listen(2)
        print(f"Server started on {HOST}:{PORT}, waiting for 2 players...")
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            thread = threading.Thread(target=self.client_thread, args=(conn, len(self.clients) - 1))
            thread.daemon = True
            thread.start()
        print("Both players connected. Starting the game in 3 seconds...")
        time.sleep(3)
        self.game_active = True
        self.game_loop()

class Client:
    def __init__(self, server_ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_ip, port))
        self.platforms = load_level_data(multiplayer_data, platform_images)
        self.scroll = [0, 0]
        self.type = None
        self.frames = {}
        self.hero = None
        self.opponent = None
        self.load_assets()
        self.send_initial_data()

    def load_assets(self):
        print("Select your hero:")
        print("1_ Roboman")
        print("2_ Ninja")
        self.type = int(input("Enter choice (1 or 2): "))
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "RoboMan_pictures" if self.type == 1 else "Ninja")
        
        # Load frames based on hero type
        if self.type == 1:  # Roboman
            self.frames["freezed_img"] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, "freezed.png")), (69, 118))
            self.frames["run_frames"] = []
            for i in range(1, 9):
                img_path = os.path.join(base_path, "hero_run_frames", f"Run ({i}).png")
                tmp = pygame.image.load(img_path)
                sizes = [(63, 118), (62, 118), (82, 118), (77, 118), (73, 118), (80, 118), (92, 118), (79, 118)]
                self.frames["run_frames"].append(pygame.transform.scale(tmp, sizes[i-1]))
            self.frames["idle_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "idle", f"Idle ({i}).png")), (70, 118))
                for i in range(1, 11)
            ]
            self.frames["Jump_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "jump", f"Jump ({i}).png")), sizes[i-1])
                for i, sizes in enumerate([(73, 118), (80, 118), (90, 118), (91, 118), (90, 118), (109, 118), (95, 118), (96, 118), (84, 118)], 1)
            ]
            self.frames["shoot_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Shoot", f"Shoot ({i}).png")), sizes[i-1])
                for i, sizes in enumerate([(83, 118), (83, 118), (82, 118), (84, 118)], 1)
            ]
            self.frames["RunShoot_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "RunShoot", f"RunShoot ({i}).png")), sizes[i-1])
                for i, sizes in enumerate([(83, 118), (87, 118), (93, 118), (97, 118), (88, 118), (90, 118), (100, 118), (89, 118)], 1)
            ]
            self.frames["JumpShoot_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "jump shoot", f"JumpShoot ({i}).png")), sizes[i-1])
                for i, sizes in enumerate([(97, 118), (97, 118), (98, 118), (95, 118), (97, 118)], 1)
            ]
            self.frames["death_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "death", f"Dead ({i}).png")), sizes[i-1])
                for i, sizes in enumerate([(73, 118), (84, 118), (90, 100), (145, 90), (133, 90), (110, 61), (118, 56), (118, 52), (118, 53), (118, 53)], 1)
            ]
            self.frames["jetpack_frame"] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, "jetpack.png")), (80, 118))
        else:  # Ninja
            self.frames["freezed_frame"] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, "freezed.png")), (62, 118))
            self.frames["SuperPower_pic"] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, "SuperPower effect.png")), (100, 118))
            self.frames["idle_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Idle", f"Idle__00{i}.png")), (62, 118))
                for i in range(10)
            ]
            self.frames["run_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Run", f"Run__00{i}.png")), (94, 118))
                for i in range(1, 10)
            ]
            self.frames["jump_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Jump", f"Jump__00{i}.png")), (sizes[i], 118))
                for i in range(10)
            ]
            self.frames["throw_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Throw", f"Throw__00{i}.png")), (sizes[i], 118))
                for i in range(10)
            ]
            self.frames["jumpThrow_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")), (sizes[i], 118))
                for i in range(10)
            ]
            self.frames["Attack_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Attack", f"Attack__00{i}.png")), (sizes[i], 118))
                for i in range(10)
            ]
            self.frames["JumpAttack_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")), sizes[i])
                for i in range(10)
            ]
            self.frames["death_frames"] = [
                pygame.transform.scale(pygame.image.load(os.path.join(base_path, "death", f"Dead__00{i}.png")), sizes[i])
                for i in range(10)
            ]

    def send_initial_data(self):
        username = input("Enter your username: ")
        char_map = {1: "Roboman", 2: "Ninja"}
        initial_data = {"username": username, "character": char_map.get(self.type, "Ninja")}
        self.socket.sendall(json.dumps(initial_data).encode('utf-8'))
        # Wait for setup confirmation
        data = self.socket.recv(1024).decode('utf-8')
        if json.loads(data).get("status") == "setup_complete":
            print("Connected to server successfully!")

    def send_input(self):
        clock = pygame.time.Clock()
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            input_data = {
                "A": keys[pygame.K_a],
                "D": keys[pygame.K_d],
                "W": keys[pygame.K_w],
                "left_click": mouse[0],
                "right_click": mouse[2],
                "LSHIFT": keys[pygame.K_LSHIFT],
                "G": keys[pygame.K_g],
                "TAB": keys[pygame.K_TAB],
                "RCTRL": keys[pygame.K_RCTRL],
                "RALT": keys[pygame.K_RALT]
            }
            try:
                self.socket.sendall(json.dumps(input_data).encode('utf-8'))
            except Exception as e:
                print("Connection lost:", e)
                break
            clock.tick(60)

    def update_from_state(self, state, is_opponent=False):
        obj = self.opponent if is_opponent else self.hero
        if not obj:
            obj = type('Hero', (), {})()
            if is_opponent:
                self.opponent = obj
            else:
                self.hero = obj
        obj.x_pos = state["x"] if "x" in state else state.get("x_pos", 0)
        obj.y_pos = state["y"] if "y" in state else state.get("y_pos", 0)
        obj.Look = state["look"] if "look" in state else state.get("Look", "right")
        obj.health = state["health"]
        frame_source = state["frame_source"] if "frame_source" in state else state.get("frame list address", "idle_frames")
        frame_index = state["frame_index"] if "frame_index" in state else state.get("frame_index", 0)
        
        # Map frame source to frames
        obj.current_picture = self.frames.get(frame_source, self.frames["idle_frames"])[frame_index if frame_index >= 0 else -1]
        obj.hitbox = pygame.Rect(obj.x_pos, obj.y_pos, obj.current_picture.get_width(), obj.current_picture.get_height())

    def render_game(self):
        screen.blit(background, (0, 0))
        for platform in self.platforms:
            platform.draw(screen, self.scroll)
        
        if self.hero and self.opponent:
            mid_x = (self.hero.x_pos + self.hero.current_picture.get_width() // 2 + 
                     self.opponent.x_pos + self.opponent.current_picture.get_width() // 2) / 2
            mid_y = (self.hero.y_pos + self.hero.current_picture.get_height() // 2 + 
                     self.opponent.y_pos + self.opponent.current_picture.get_height() // 2) / 2
            self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
            self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15
            
            for obj in [self.hero, self.opponent]:
                flipped = pygame.transform.flip(obj.current_picture, obj.Look == 'left', False)
                screen.blit(flipped, (obj.x_pos - self.scroll[0], obj.y_pos - self.scroll[1]))
                
                # Display health bar
                health_bar_width = int(100 * (obj.health / 100))
                health_bar = pygame.Surface((health_bar_width, 10))
                health_bar.fill((255, 0, 0))
                screen.blit(health_bar, (obj.x_pos - self.scroll[0], obj.y_pos - self.scroll[1] - 20))
        
        pygame.display.update()

    def receive_state(self):
        while True:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                state_bundle = json.loads(data.decode('utf-8'))
                self.update_from_state(state_bundle["self"])
                self.update_from_state(state_bundle["opponent"], is_opponent=True)
            except Exception as e:
                print("Error receiving game state:", e)
                break

def main():
    print("Do you want to start a server or join as a client?")
    print("1_ Start Server")
    print("2_ Join as Client")
    choice = int(input("Enter choice (1 or 2): "))
    
    if choice == 1:
        print("Select your hero (host):")
        print("1_ Roboman")
        print("2_ Ninja")
        hero_choice = int(input("Enter choice (1 or 2): "))
        platforms = load_level_data(multiplayer_data, platform_images)
        server = Server(screen, platforms, background, hero_choice)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        
        # Host also acts as a client
        time.sleep(2)  # Wait for server to start
        client = Client(SERVER_IP, PORT)
        threading.Thread(target=client.send_input, daemon=True).start()
        threading.Thread(target=client.receive_state, daemon=True).start()
        
        # Main rendering loop
        clock = pygame.time.Clock()
        while True:
            client.render_game()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(60)
    
    elif choice == 2:
        client = Client(SERVER_IP, PORT)
        threading.Thread(target=client.send_input, daemon=True).start()
        threading.Thread(target=client.receive_state, daemon=True).start()
        
        # Main rendering loop
        clock = pygame.time.Clock()
        while True:
            client.render_game()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(60)

if __name__ == "__main__":
    main()