import pygame
import threading
import socket
import json
import os
from src.levels import multiplayer_data, load_level_data
from config import screen_width, screen_height

# Initialize Pygame
pygame.init()
try:
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BrawlForge Client")
except Exception as e:
    print(f"Error initializing Pygame screen: {e}")
    exit()

# Load platform images
platform_image_path = "src/assets/images/"
platform_images = {}
try:
    platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }
    print("Platform images loaded successfully")
except Exception as e:
    print(f"Error loading platform images: {e}")
    platform_images = {key: pygame.Surface((100, 20)) for key in ['left', 'middle', 'right', 'solid']}
    for surface in platform_images.values():
        surface.fill((100, 100, 100)) 

# Load background
try:
    background = pygame.image.load("src/assets/images/city1.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    print("Background image loaded successfully")
except Exception as e:
    print(f"Error loading background: {e}")
    background = pygame.Surface((screen_width, screen_height))
    background.fill((0, 100, 200))  

HOST = "10.138.26.11"
PORT = 9191

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            exit()
        
        self.platforms = load_level_data(multiplayer_data, platform_images)
        self.scroll = [0, 0]
        self.type = None
        self.hero = None
        self.opponent = None
        self.frames = {}
        self.load_assets()
        self.send_initial_data()
        self.x_pos=0
        self.y_pos=0
        self.health=100
        self.Look='right'
        self.username=None
        self.frame_source='idle'
        self.frame_index=0
        self.current_picture=None
        self.scroll=[0,0]
        

    def load_assets(self):
        print("Select your hero type:")
        print("1_ Roboman")
        print("2_ Ninja")
        print("3_ NinjaGirl")
        print("4_ Archer")
        
        try:
            self.type = int(input("Enter choice (1-4): "))
            if self.type not in [1, 2, 3, 4]:
                raise ValueError("Invalid hero type")
        except ValueError:
            print("Invalid input, defaulting to Ninja")
            self.type = 2



        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src","assets", "images")
        
        
        
        
        try:
            if self.type == 1:  # Roboman
                base_path = os.path.join(base_path, "RoboMan_pictures")
                self.frames['freezed_img']=pygame.transform.scale(pygame.image.load(os.path.join(base_path,"freezed.png")),(69,118))
                self.frames["run_frames"] = []
                sizes = [(63, 118), (62, 118), (82, 118), (77, 118), (73, 118), (80, 118), (92, 118), (79, 118)]
                for i in range(1, 9):
                    img_path = os.path.join(base_path, "hero_run_frames", f"Run ({i}).png")
                    try:
                        self.frames["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman run frame 'Run ({i}).png': {e}")
                        self.frames["run_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["idle_frames"] = []
                for i in range(1, 11):
                    img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                    try:
                        self.frames["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (70, 118)))
                    except Exception as e:
                        print(f"Error loading Roboman idle frame 'Idle ({i}).png': {e}")
                        self.frames["idle_frames"].append(pygame.Surface((70, 118)))
                self.frames["jump_frames"] = []
                sizes = [(73, 118), (80, 118), (90, 118), (91, 118), (90, 118), (109, 118), (95, 118), (96, 118), (84, 118)]
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "jump", f"Jump ({i}).png")
                    try:
                        self.frames["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman jump frame 'Jump ({i}).png': {e}")
                        self.frames["jump_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["shoot_frames"] = []
                sizes = [(83, 118), (83, 118), (82, 118), (84, 118)]
                for i in range(1, 5):
                    img_path = os.path.join(base_path, "Shoot", f"Shoot ({i}).png")
                    try:
                        self.frames["shoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman shoot frame 'Shoot ({i}).png': {e}")
                        self.frames["shoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["RunShoot_frames"] = []
                sizes = [(83, 118), (87, 118), (93, 118), (97, 118), (88, 118), (90, 118), (100, 118), (89, 118)]
                for i in range(1, 9):
                    img_path = os.path.join(base_path, "RunShoot", f"RunShoot ({i}).png")
                    try:
                        self.frames["RunShoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman RunShoot frame 'RunShoot ({i}).png': {e}")
                        self.frames["RunShoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["JumpShoot_frames"] = []
                sizes = [(97, 118), (97, 118), (98, 118), (95, 118), (97, 118)]
                for i in range(1, 6):
                    img_path = os.path.join(base_path, "jump shoot", f"JumpShoot ({i}).png")
                    try:
                        self.frames["JumpShoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman JumpShoot frame 'JumpShoot ({i}).png': {e}")
                        self.frames["JumpShoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["death_frames"] = []
                sizes = [(73, 118), (84, 118), (90, 100), (145, 90), (133, 90), (110, 61), (118, 56), (118, 52), (118, 53), (118, 53)]
                for i in range(1, 11):
                    img_path = os.path.join(base_path, "death", f"Dead ({i}).png")
                    try:
                        self.frames["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman death frame 'Dead ({i}).png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["jetpack_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "jetpack.png")), (80, 118))

            elif self.type == 2:  # Ninja
                base_path = os.path.join(base_path, "Ninja")
                self.frames["freezed_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (62, 118))
                self.frames["SuperPower_pic"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "SuperPower effect.png")), (100, 118))
                self.frames["idle_frames"] = []
                for i in range(10):
                    img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                    try:
                        self.frames["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (62, 118)))
                    except Exception as e:
                        print(f"Error loading Ninja idle frame 'Idle__00{i}.png': {e}")
                        self.frames["idle_frames"].append(pygame.Surface((62, 118)))
                self.frames["run_frames"] = []
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                    try:
                        self.frames["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (94, 118)))
                    except Exception as e:
                        print(f"Error loading Ninja run frame 'Run__00{i}.png': {e}")
                        self.frames["run_frames"].append(pygame.Surface((94, 118)))
                self.frames["jump_frames"] = []
                sizes = [77, 69, 69, 71, 70, 70, 77, 84, 95, 93]
                for i in range(10):
                    img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                    try:
                        self.frames["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja jump frame 'Jump__00{i}.png': {e}")
                        self.frames["jump_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["throw_frames"] = []
                sizes = [72, 66, 83, 81, 79, 79, 78, 86, 78, 66]
                for i in range(10):
                    img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                    try:
                        self.frames["throw_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja throw frame 'Throw__00{i}.png': {e}")
                        self.frames["throw_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["jumpThrow_frames"] = []
                sizes = [85, 88, 92, 99, 101, 104, 103, 96, 89, 89]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                    try:
                        self.frames["jumpThrow_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja jumpThrow frame 'Jump_Throw__00{i}.png': {e}")
                        self.frames["jumpThrow_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Attack_frames"] = []
                sizes = [78, 75, 85, 132, 136, 149, 149, 149, 147, 137]
                for i in range(10):
                    img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                    try:
                        self.frames["Attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja attack frame 'Attack__00{i}.png': {e}")
                        self.frames["Attack_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["JumpAttack_frames"] = []
                sizes = [(87, 118), (86, 118), (86, 118), (136, 118), (136, 118), (137, 138), (139, 138), (140, 138), (125, 170), (136, 118)]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                    try:
                        self.frames["JumpAttack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Ninja jumpAttack frame 'Jump_Attack__00{i}.png': {e}")
                        self.frames["JumpAttack_frames"].append(pygame.Surface(sizes[i]))
                self.frames["death_frames"] = []
                sizes = [(63, 118), (74, 118), (127, 113), (111, 108), (140, 100), (157, 100), (152, 90), (157, 90), (160, 90), (156, 90)]
                for i in range(10):
                    img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                    try:
                        self.frames["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Ninja death frame 'Dead__00{i}.png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames["Kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Kunai.png")), (60, 12))
                self.frames["Fired_kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "FiredKunai.png")), (70, 24))

            elif self.type == 3:  # NinjaGirl
                base_path = os.path.join(base_path, "NinjaGirl")
                self.frames["freezed_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (68, 118))
                self.frames["SuperPower_pic"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "super power.png")), (118, 118))
                self.frames["idle_frames"] = []
                for i in range(10):
                    img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                    try:
                        self.frames["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (68, 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl idle frame 'Idle__00{i}.png': {e}")
                        self.frames["idle_frames"].append(pygame.Surface((68, 118)))
                self.frames["run_frames"] = []
                sizes = [82, 77, 77, 90, 88, 82, 78, 78, 83]
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                    try:
                        self.frames["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i-1], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl run frame 'Run__00{i}.png': {e}")
                        self.frames["run_frames"].append(pygame.Surface((sizes[i-1], 118)))
                self.frames["jump_frames"] = []
                sizes = [75, 70, 71, 71, 72, 71, 78, 77, 79, 79]
                for i in range(10):
                    img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                    try:
                        self.frames["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jump frame 'Jump__00{i}.png': {e}")
                        self.frames["jump_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["throw_frames"] = []
                sizes = [70, 68, 73, 85, 69, 68, 68, 77, 73, 67]
                for i in range(10):
                    img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                    try:
                        self.frames["throw_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl throw frame 'Throw__00{i}.png': {e}")
                        self.frames["throw_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["jumpThrow_frames"] = []
                sizes = [79, 77, 82, 92, 94, 97, 95, 89, 80, 79]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                    try:
                        self.frames["jumpThrow_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jumpThrow frame 'Jump_Throw__00{i}.png': {e}")
                        self.frames["jumpThrow_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Attack_frames"] = []
                sizes = [70, 70, 76, 118, 121, 130, 129, 127, 124, 118]
                for i in range(10):
                    img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                    try:
                        self.frames["Attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl attack frame 'Attack__00{i}.png': {e}")
                        self.frames["Attack_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["JumpAttack_frames"] = []
                sizes = [(71, 118), (67, 118), (68, 118), (108, 118), (108, 118), (115, 128), (118, 133), (119, 134), (118, 129), (92, 118)]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                    try:
                        self.frames["JumpAttack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jumpAttack frame 'Jump_Attack__00{i}.png': {e}")
                        self.frames["JumpAttack_frames"].append(pygame.Surface(sizes[i]))
                self.frames["death_frames"] = []
                sizes = [(70, 118), (83, 118), (93, 108), (102, 90), (104, 70), (118, 78), (118, 73), (118, 78), (118, 78), (118, 79)]
                for i in range(10):
                    img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                    try:
                        self.frames["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading NinjaGirl death frame 'Dead__00{i}.png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames["Kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Kunai.png")), (60, 12))
                self.frames["Fired_kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "FiredKunai.png")), (70, 24))

            elif self.type == 4:  # Archer
                base_path = os.path.join(base_path, "Archer")
                self.frames["freezed_img"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (88, 100))
                self.frames["super_power_effect_picture"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "super power effect.png")), (88, 127))
                self.frames["idle_frames"] = []
                for i in range(6):
                    img_path = os.path.join(base_path, "idle", f"{i}.png")
                    try:
                        self.frames["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (88, 100)))
                    except Exception as e:
                        print(f"Error loading Archer idle frame '{i}.png': {e}")
                        self.frames["idle_frames"].append(pygame.Surface((88, 100)))
                self.frames["run_frames"] = []
                sizes = [89, 90, 91, 90, 89, 90, 96, 90]
                for i in range(8):
                    img_path = os.path.join(base_path, "run", f"{i}.png")
                    try:
                        self.frames["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer run frame '{i}.png': {e}")
                        self.frames["run_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames["jump_frames"] = []
                sizes = [91, 93, 88, 90, 94, 89, 88, 90]
                for i in range(8):
                    img_path = os.path.join(base_path, "jump", f"{i}.png")
                    try:
                        self.frames["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer jump frame '{i}.png': {e}")
                        self.frames["jump_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames["shot_frames"] = []
                sizes = [90, 72, 72, 72, 72, 72, 97, 113, 106, 89, 77, 72, 70]
                for i in range(13):
                    img_path = os.path.join(base_path, "shot", f"{i}.png")
                    try:
                        self.frames["shot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer shot frame '{i}.png': {e}")
                        self.frames["shot_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames["attack_frames"] = []
                sizes = [78, 60, 132, 62]
                for i in range(4):
                    img_path = os.path.join(base_path, "attack", f"{i}.png")
                    try:
                        self.frames["attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer attack frame '{i}.png': {e}")
                        self.frames["attack_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames["death_frames"] = []
                sizes = [(98, 100), (102, 100), (150, 43)]
                for i in range(3):
                    img_path = os.path.join(base_path, "death", f"{i}.png")
                    try:
                        self.frames["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Archer death frame '{i}.png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames["arrow_pic"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Arrow.png")), (30, 2))
                self.frames["firedarrow_pic"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fired arrow.png")), (30, 8))
            print("Hero assets loaded successfully")
        except Exception as e:
            print(f"Error loading hero assets: {e}")
            self.frames = {key: [pygame.Surface((50, 50)) for _ in range(10)] for key in ["idle_frames", "run_frames", "jump_frames"]}

        # hero and opponent
        self.hero = type('Hero', (), {
            'x_pos': 0, 'y_pos': 0, 'Look': 'right', 'health': 100,
            'current_picture': self.frames["idle_frames"][0],
            'hitbox': pygame.Rect(0, 0, self.frames["idle_frames"][0].get_width(), self.frames["idle_frames"][0].get_height())
        })()
        self.opponent = type('Hero', (), {
            'x_pos': 0, 'y_pos': 0, 'Look': 'right', 'health': 100,
            'current_picture': self.frames["idle_frames"][0],
            'hitbox': pygame.Rect(0, 0, self.frames["idle_frames"][0].get_width(), self.frames["idle_frames"][0].get_height())
        })()

    def send_initial_data(self):
        username = input("Enter your username: ")
        char_map = {1: "Roboman", 2: "Ninja", 3: "NinjaGirl", 4: "Archer"}
        initial_data = {"username": username, "character": char_map.get(self.type, "Ninja")}
        try:
            self.socket.sendall(json.dumps(initial_data).encode('utf-8'))
            data = self.socket.recv(1024).decode('utf-8')
            if json.loads(data).get("status") == "setup_complete":
                print("Connected to server successfully!")
            else:
                print("Server setup failed")
                exit()
        except Exception as e:
            print(f"Error sending initial data: {e}")
            exit()

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
                "LSHIFT": keys[pygame.K_LSHIFT],
                "G": keys[pygame.K_g],
                "TAB": keys[pygame.K_TAB],
                "RCTRL": keys[pygame.K_RCTRL],
                "RALT": keys[pygame.K_RALT],
                "left_click": mouse[0],
                "right_click": mouse[2]
            }
            try:
                self.socket.sendall(json.dumps(input_data).encode('utf-8'))
            except Exception as e:
                print(f"Connection lost: {e}")
                break
            clock.tick(60)


    def receive_state(self):
        while True:
            try:
                data = self.socket.recv(1024)
                data = data.decode('utf-8')
                if not data:
                    print("Server disconnected")
                    break

                parsed = json.loads(data)
                selfdata = parsed["self"]
                self.x_pos = selfdata['x_pos']
                self.y_pos = selfdata['y_pos']
                self.health = selfdata['health']
                self.Look = selfdata['look']
                self.username=selfdata['username']
                self.frame_source=selfdata['frame_source']
                self.frame_index=selfdata['frame_index']
                print(f"x_pos={self.x_pos}   y_pos={self.y_pos}")
                try:
                    self.current_picture=self.frames[self.frame_source][self.frame_index if self.frame_index>=-1 else 0]
                except:
                    print("not able to update the frame")
                    self.current_picture = self.frames["idle_frames"][0]
                    
                print(f"x_pos={self.x_pos}   y_pos={self.y_pos}")
                print(f"frame_source={self.frame_source}   frame_index={self.frame_index}")
                print("-----------")
            except Exception as e:
                print(f"Error receiving game state: {e}")
                break

    def render_game(self):
        screen.blit(background, (0, 0))
        for platform in self.platforms:
            try:
                 platform.draw(screen, self.scroll)
            except Exception as e:
                 print(f"Error drawing platform: {e}")

        # Camera scrolling
        mid_x = (self.x_pos + self.current_picture.get_width() // 2 )
        mid_y = (self.y_pos + self.current_picture.get_height() // 2 )
        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15

        #Render heroe
        if self.Look=='right':
            screen.blit(self.current_picture, (screen_width//2, screen_height//2))
        elif self.Look=='left':
            screen.blit(self.current_picture, (screen_width//2, screen_height//2))
        pygame.display.update()

def main():
    client = Client()
    threading.Thread(target=client.send_input, daemon=True).start()
    threading.Thread(target=client.receive_state, daemon=True).start()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.socket.close()
                exit()
        if client.current_picture!=None:
            client.render_game()
        
        clock.tick(60)

if __name__ == "__main__":
    main()