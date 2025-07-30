import pygame
import threading
import socket
import json
import os
from src.levels import multiplayer_data, load_level_data
from config import screen_width, screen_height
from src.utils import get_my_local_ip
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

HOST = get_my_local_ip()
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
        self.opponent_character = None
        self.opponent_frames = {"idle_frames": [pygame.Surface((50, 50))]}
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
        self.bullets=[]
        if "idle_frames" in self.frames and len(self.frames["idle_frames"]) > 0:
            self.current_picture = self.frames["idle_frames"][0]
        else:
            self.current_picture = pygame.Surface((50, 50))
            self.current_picture.fill((255, 0, 0))
        

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
            self.Roboman_bullet=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"RoboMan_pictures", "Bullet.png")
            ),
                (35,15)                                       
            )
            self.Roboman_rocket=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"RoboMan_pictures", "rocket.png")
            ),
                (43,25)                                       
            )
            self.Kunai=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"Ninja","Kunai.png")
            ),
                (60,12)                                       
            )
            self.Fired_Kunai=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"Ninja","FiredKunai.png")
            ),
                (70, 24)                                       
            )
            self.Arrow=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"Archer", "Arrow.png")
            ),
                (30,2)                                       
            )
            self.Fired_Arrow=pygame.transform.scale(pygame.image.load(
                os.path.join(base_path,"Archer", "fired arrow.png")
            ),
                (30, 8)                                      
            )
        
        except:
            print("unable to load bullet assets")
            
        
        
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
            'x_pos': 0,
            'y_pos': 0,
            'Look': 'right',
            'health': 100,
            'frame_source': 'idle_frames',
            'frame_index': 0,
            'username': '',
            'current_picture': self.frames["idle_frames"][0],
            'hitbox': pygame.Rect(0, 0, self.frames["idle_frames"][0].get_width(), self.frames["idle_frames"][0].get_height())
        })()


    
    def load_opponent_assets(self, character_name):
        frames = {}
        base_path = os.path.join("src", "assets", "images")

        if character_name == "Roboman":
            path = os.path.join(base_path, "RoboMan_pictures", "idle")
            frames["idle_frames"] = []
            for i in range(1, 11):
                try:
                    img = pygame.image.load(os.path.join(path, f"Idle ({i}).png")).convert_alpha()
                    img = pygame.transform.scale(img, (70, 118))
                    frames["idle_frames"].append(img)
                except:
                    frames["idle_frames"].append(pygame.Surface((70, 118)))

        elif character_name == "Ninja":
            path = os.path.join(base_path, "Ninja", "Idle")
            frames["idle_frames"] = []
            for i in range(10):
                try:
                    img = pygame.image.load(os.path.join(path, f"Idle__00{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (62, 118))
                    frames["idle_frames"].append(img)
                except:
                    frames["idle_frames"].append(pygame.Surface((62, 118)))

        elif character_name == "NinjaGirl":
            path = os.path.join(base_path, "NinjaGirl", "Idle")
            frames["idle_frames"] = []
            for i in range(10):
                try:
                    img = pygame.image.load(os.path.join(path, f"Idle__00{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (68, 118))
                    frames["idle_frames"].append(img)
                except:
                    frames["idle_frames"].append(pygame.Surface((68, 118)))

        elif character_name == "Archer":
            path = os.path.join(base_path, "Archer", "idle")
            frames["idle_frames"] = []
            for i in range(6):
                try:
                    img = pygame.image.load(os.path.join(path, f"{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (88, 100))
                    frames["idle_frames"].append(img)
                except:
                    frames["idle_frames"].append(pygame.Surface((88, 100)))

        else:
            print(f"Unknown character '{character_name}', using blank placeholder.")
            frames["idle_frames"] = [pygame.Surface((64, 64)) for _ in range(5)]

        return frames


 
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

    def play_sound(self, event_name, character_name="Ninja"):
        try:
            path = f"src/assets/sounds/{character_name}/{event_name}.mp3"
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception as e:
            print(f"Error playing sound for {character_name} - {event_name}: {e}")

    def receive_state(self):
        buffer = ""
        while True:
            try:
                while True:
                    chunk = self.socket.recv(1024)
                    if not chunk:
                        break
                    buffer += chunk.decode('utf-8')

                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)

                        try:
                            parsed = json.loads(line)
                            selfdata = parsed["self"]
                            self.x_pos = selfdata['x_pos']
                            self.y_pos = selfdata['y_pos']
                            self.health = selfdata['health']
                            self.Look = selfdata['look']
                            self.username = selfdata['username']
                            self.frame_source = selfdata['frame_source']
                            self.frame_index = selfdata['frame_index']
                            self.character_name = selfdata.get("character", "Ninja")
                            for event in selfdata.get("events", []):
                                 self.play_sound(event, self.character_name)

                            # Fix index out of range crash
                            frame_list = self.frames.get(self.frame_source, [])
                            if frame_list:
                                self.current_picture = frame_list[self.frame_index % len(frame_list)]

                            opp_data = parsed.get("opponent", {})
                            self.opponent.x_pos = opp_data.get('x_pos', 0)
                            self.opponent.y_pos = opp_data.get('y_pos', 0)
                            self.opponent.health = opp_data.get('health', 100)
                            self.opponent.Look = opp_data.get('look', 'right')
                            self.opponent.username = opp_data.get('username', '')
                            self.opponent.frame_source = opp_data.get('frame_source', 'idle_frames')
                            self.opponent.frame_index = opp_data.get('frame_index', 0)

                            opponent_char = opp_data.get("character", "Ninja")
                            if opponent_char != self.opponent_character:
                                self.opponent_character = opponent_char
                                self.opponent_frames = self.load_opponent_assets(opponent_char)
                            for event in opp_data.get("events", []):
                                self.play_sound(event, opp_data.get("character", "Ninja"))
                            opp_frames = self.opponent_frames.get(self.opponent.frame_source, [])
                            if opp_frames:
                                self.opponent.current_picture = opp_frames[self.opponent.frame_index % len(opp_frames)]

                            # Handle bullets
                            self.bullets = parsed.get("bullets", [])
                            

                        except Exception as e:
                            print(f"Error decoding JSON or setting frames: {e}")

            except Exception as e:
                print(f"Error receiving game state: {e}")
                break


            

    def render_game(self):
        screen.blit(background, (0, 0))
        try:
            self.opponent.current_picture = self.opponent_frames[self.opponent.frame_source][self.opponent.frame_index]
        except Exception as e:
            #print(f"Error updating opponent frame: {e}")
            self.opponent.current_picture = self.opponent_frames["idle_frames"][0]
        # Camera scrolling
        mid_x = (self.x_pos + self.current_picture.get_width() // 2 )
        mid_y = (self.y_pos + self.current_picture.get_height() // 2 )
        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15
        for platform in self.platforms:
            try:
                 platform.draw(screen, self.scroll)
            except Exception as e:
                 print(f"Error drawing platform: {e}")

        #Render heroe
        if self.Look=='right':
            screen.blit(self.current_picture, (self.x_pos - self.scroll[0], self.y_pos - self.scroll[1]))

        elif self.Look=='left':
            screen.blit(pygame.transform.flip(self.current_picture, True, False), (self.x_pos - self.scroll[0], self.y_pos - self.scroll[1]))

        if self.opponent.current_picture:
            screen.blit(
                pygame.transform.flip(self.opponent.current_picture, True, False) if self.opponent.Look == 'left' else self.opponent.current_picture,
                (self.opponent.x_pos - self.scroll[0], self.opponent.y_pos - self.scroll[1])
            )
            
        for bullet in self.bullets:
            if bullet['owner']=="Roboman":
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                     screen.blit(self.Roboman_bullet,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     screen.blit(self.Roboman_rocket,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                else:
                    if not bullet["Flag"]:
                     screen.blit(pygame.transform.flip(self.Roboman_bullet,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     screen.blit(pygame.transform.flip(self.Roboman_rocket,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
            elif bullet['owner']=="Ninja" or bullet['owner']=="NinjaGirl" :
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                     screen.blit(self.Kunai,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     screen.blit(self.Fired_Kunai,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                else:
                    if not bullet["Flag"]:
                     screen.blit(pygame.transform.flip(self.Kunai,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     screen.blit(pygame.transform.flip(self.Fired_Kunai,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                     
                     
            elif bullet['owner']=="Archer" :
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                        screen.blit(self.Arrow,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                        screen.blit(self.Fired_Arrow,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                else:
                    if not bullet["Flag"]:
                     screen.blit(pygame.transform.flip(self.Arrow,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     screen.blit(pygame.transform.flip(self.Fired_Arrow,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    
          
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