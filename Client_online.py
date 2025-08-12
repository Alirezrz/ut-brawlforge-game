import socket
import json
import pygame
import os

# Constants (make sure these values match your game configuration)
screen_width = 800
screen_height = 600
profileSideSize = 50
health_bar_lenght = 200
roboman_health_bar_frame_thickness = 2

class Client:
    def __init__(self, sock, username, player_id, hero_type):
        self.socket = sock
        self.username = username
        self.player_id = player_id
        self.hero_type = hero_type

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Game - {self.username}")

        # Game state
        self.bullets = []
        self.other_players_states = []
        self.frame_source = 'idle_frames'
        self.current_picture = pygame.Surface((50, 50))  # Default size
        self.is_dead = False

        # Load assets (to be implemented, can be handled later)
        self.load_assets()

        # Send initial connection data to the server
        initial_data = {"username": self.username, "character": self.hero_type}
        self.send_data(initial_data)

    def load_assets(self):
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
            self.platforms = load_level_data(multiplayer_data, platform_images)
            print("Platform images loaded successfully")
            
        except Exception as e:
            print(f"Error loading platform images: {e}")
            self.platform_images = {
                'left': pygame.Surface((64, 64)),
                'middle': pygame.Surface((64, 64)),
                'right': pygame.Surface((64, 64)),
                'solid': pygame.Surface((64, 64))
            }
            self.platforms = load_level_data(multiplayer_data, self.platform_images)
        try:
            self.background = pygame.image.load("src/assets/images/city1.png")
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
            print("Background image loaded successfully")
        except Exception as e:
            print(f"Error loading background: {e}")
              
            
        
        try:
            self.type = self.hero_type
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
                base_path = os.path.join(base_path, "RoboMan_pictures")
                self.frames["Roboman"]['freezed_img']=pygame.transform.scale(pygame.image.load(os.path.join(base_path,"freezed.png")),(69,118))
                self.frames["Roboman"]["run_frames"] = []
                sizes = [(63, 118), (62, 118), (82, 118), (77, 118), (73, 118), (80, 118), (92, 118), (79, 118)]
                for i in range(1, 9):
                    img_path = os.path.join(base_path, "hero_run_frames", f"Run ({i}).png")
                    try:
                        self.frames["Roboman"]["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman run frame 'Run ({i}).png': {e}")
                        self.frames["Roboman"]["run_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["idle_frames"] = []
                for i in range(1, 11):
                    img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                    try:
                        self.frames["Roboman"]["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (70, 118)))
                    except Exception as e:
                        print(f"Error loading Roboman idle frame 'Idle ({i}).png': {e}")
                        self.frames["Roboman"]["idle_frames"].append(pygame.Surface((70, 118)))
                self.frames["Roboman"]["Jump_frames"] = []
                sizes = [(73, 118), (80, 118), (90, 118), (91, 118), (90, 118), (109, 118), (95, 118), (96, 118), (84, 118)]
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "jump", f"Jump ({i}).png")
                    try:
                        self.frames["Roboman"]["Jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman jump frame 'Jump ({i}).png': {e}")
                        self.frames["Roboman"]["Jump_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["shoot_frames"] = []
                sizes = [(83, 118), (83, 118), (82, 118), (84, 118)]
                for i in range(1, 5):
                    img_path = os.path.join(base_path, "Shoot", f"Shoot ({i}).png")
                    try:
                        self.frames["Roboman"]["shoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman shoot frame 'Shoot ({i}).png': {e}")
                        self.frames["Roboman"]["shoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["RunShoot_frames"] = []
                sizes = [(83, 118), (87, 118), (93, 118), (97, 118), (88, 118), (90, 118), (100, 118), (89, 118)]
                for i in range(1, 9):
                    img_path = os.path.join(base_path, "RunShoot", f"RunShoot ({i}).png")
                    try:
                        self.frames["Roboman"]["RunShoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman RunShoot frame 'RunShoot ({i}).png': {e}")
                        self.frames["Roboman"]["RunShoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["JumpShoot_frames"] = []
                sizes = [(97, 118), (97, 118), (98, 118), (95, 118), (97, 118)]
                for i in range(1, 6):
                    img_path = os.path.join(base_path, "jump shoot", f"JumpShoot ({i}).png")
                    try:
                        self.frames["Roboman"]["JumpShoot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman JumpShoot frame 'JumpShoot ({i}).png': {e}")
                        self.frames["Roboman"]["JumpShoot_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["death_frames"] = []
                sizes = [(73, 118), (84, 118), (90, 100), (145, 90), (133, 90), (110, 61), (118, 56), (118, 52), (118, 53), (118, 53)]
                for i in range(1, 11):
                    img_path = os.path.join(base_path, "death", f"Dead ({i}).png")
                    try:
                        self.frames["Roboman"]["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i-1]))
                    except Exception as e:
                        print(f"Error loading Roboman death frame 'Dead ({i}).png': {e}")
                        self.frames["Roboman"]["death_frames"].append(pygame.Surface(sizes[i-1]))
                self.frames["Roboman"]["jetpack_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "jetpack.png")), (80, 118))
                
                base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src","assets", "images")
                base_path = os.path.join(base_path, "Ninja")
                self.frames["Ninja"]["freezed_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (62, 118))
                self.frames["Ninja"]["SuperPower_pic"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "SuperPower effect.png")), (100, 118))
                self.frames["Ninja"]["idle_frames"] = []
                for i in range(10):
                    img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                    try:
                        self.frames["Ninja"]["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (62, 118)))
                    except Exception as e:
                        print(f"Error loading Ninja idle frame 'Idle__00{i}.png': {e}")
                        self.frames["Ninja"]["idle_frames"].append(pygame.Surface((62, 118)))
                self.frames["Ninja"]["run_frames"] = []
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                    try:
                        self.frames["Ninja"]["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (94, 118)))
                    except Exception as e:
                        print(f"Error loading Ninja run frame 'Run__00{i}.png': {e}")
                        self.frames["Ninja"]["run_frames"].append(pygame.Surface((94, 118)))
                self.frames["Ninja"]["jump_frames"] = []
                sizes = [77, 69, 69, 71, 70, 70, 77, 84, 95, 93]
                for i in range(10):
                    img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                    try:
                        self.frames["Ninja"]["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja jump frame 'Jump__00{i}.png': {e}")
                        self.frames["Ninja"]["jump_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Ninja"]["throw_frames"] = []
                sizes = [72, 66, 83, 81, 79, 79, 78, 86, 78, 66]
                for i in range(10):
                    img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                    try:
                        self.frames["Ninja"]["throw_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja throw frame 'Throw__00{i}.png': {e}")
                        self.frames["Ninja"]["throw_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Ninja"]["jumpThrow_frames"] = []
                sizes = [85, 88, 92, 99, 101, 104, 103, 96, 89, 89]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                    try:
                        self.frames["Ninja"]["jumpThrow_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja jumpThrow frame 'Jump_Throw__00{i}.png': {e}")
                        self.frames["Ninja"]["jumpThrow_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Ninja"]["Attack_frames"] = []
                sizes = [78, 75, 85, 132, 136, 149, 149, 149, 147, 137]
                for i in range(10):
                    img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                    try:
                        self.frames["Ninja"]["Attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading Ninja attack frame 'Attack__00{i}.png': {e}")
                        self.frames["Ninja"]["Attack_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["Ninja"]["JumpAttack_frames"] = []
                sizes = [(87, 118), (86, 118), (86, 118), (136, 118), (136, 118), (137, 138), (139, 138), (140, 138), (125, 170), (136, 118)]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                    try:
                        self.frames["Ninja"]["JumpAttack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Ninja jumpAttack frame 'Jump_Attack__00{i}.png': {e}")
                        self.frames["Ninja"]["JumpAttack_frames"].append(pygame.Surface(sizes[i]))
                self.frames["Ninja"]["death_frames"] = []
                sizes = [(63, 118), (74, 118), (127, 113), (111, 108), (140, 100), (157, 100), (152, 90), (157, 90), (160, 90), (156, 90)]
                for i in range(10):
                    img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                    try:
                        self.frames["Ninja"]["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Ninja death frame 'Dead__00{i}.png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames["Ninja"]["Kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Kunai.png")), (60, 12))
                self.frames["Ninja"]["Fired_kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "FiredKunai.png")), (70, 24))
                base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src","assets", "images")
                base_path = os.path.join(base_path, "NinjaGirl")
                self.frames["NinjaGirl"]["freezed_frame"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (68, 118))
                self.frames["NinjaGirl"]["SuperPower_pic"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "super power.png")), (118, 118))
                self.frames["NinjaGirl"]["idle_frames"] = []
                for i in range(10):
                    img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (68, 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl idle frame 'Idle__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["idle_frames"].append(pygame.Surface((68, 118)))
                self.frames["NinjaGirl"]["run_frames"] = []
                sizes = [82, 77, 77, 90, 88, 82, 78, 78, 83]
                for i in range(1, 10):
                    img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i-1], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl run frame 'Run__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["run_frames"].append(pygame.Surface((sizes[i-1], 118)))
                self.frames["NinjaGirl"]["jump_frames"] = []
                sizes = [75, 70, 71, 71, 72, 71, 78, 77, 79, 79]
                for i in range(10):
                    img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jump frame 'Jump__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["jump_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["NinjaGirl"]["throw_frames"] = []
                sizes = [70, 68, 73, 85, 69, 68, 68, 77, 73, 67]
                for i in range(10):
                    img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["throw_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl throw frame 'Throw__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["throw_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["NinjaGirl"]["jumpThrow_frames"] = []
                sizes = [79, 77, 82, 92, 94, 97, 95, 89, 80, 79]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["jumpThrow_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jumpThrow frame 'Jump_Throw__00{i}.png': {e}")
                        self.frames["jumpThrow_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["NinjaGirl"]["Attack_frames"] = []
                sizes = [70, 70, 76, 118, 121, 130, 129, 127, 124, 118]
                for i in range(10):
                    img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["Attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 118)))
                    except Exception as e:
                        print(f"Error loading NinjaGirl attack frame 'Attack__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["Attack_frames"].append(pygame.Surface((sizes[i], 118)))
                self.frames["NinjaGirl"]["JumpAttack_frames"] = []
                sizes = [(71, 118), (67, 118), (68, 118), (108, 118), (108, 118), (115, 128), (118, 133), (119, 134), (118, 129), (92, 118)]
                for i in range(10):
                    img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["JumpAttack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading NinjaGirl jumpAttack frame 'Jump_Attack__00{i}.png': {e}")
                        self.frames["NinjaGirl"]["JumpAttack_frames"].append(pygame.Surface(sizes[i]))
                self.frames["NinjaGirl"]["death_frames"] = []
                sizes = [(70, 118), (83, 118), (93, 108), (102, 90), (104, 70), (118, 78), (118, 73), (118, 78), (118, 78), (118, 79)]
                for i in range(10):
                    img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                    try:
                        self.frames["NinjaGirl"]["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading NinjaGirl death frame 'Dead__00{i}.png': {e}")
                        self.frames["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames["NinjaGirl"]["Kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Kunai.png")), (60, 12))
                self.frames["NinjaGirl"]["Fired_kunai"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "FiredKunai.png")), (70, 24))
                base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src","assets", "images")
                base_path = os.path.join(base_path, "Archer")
                self.frames['Archer']["freezed_img"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "freezed.png")), (88, 100))
                self.frames['Archer']["super_power_effect_picture"] = pygame.transform.scale(
                    pygame.image.load(os.path.join(base_path, "super power effect.png")), (88, 127))
                self.frames['Archer']["idle_frames"] = []
                for i in range(6):
                    img_path = os.path.join(base_path, "idle", f"{i}.png")
                    try:
                        self.frames['Archer']["idle_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (88, 100)))
                    except Exception as e:
                        print(f"Error loading Archer idle frame '{i}.png': {e}")
                        self.frames['Archer']["idle_frames"].append(pygame.Surface((88, 100)))
                self.frames['Archer']["run_frames"] = []
                sizes = [89, 90, 91, 90, 89, 90, 96, 90]
                for i in range(8):
                    img_path = os.path.join(base_path, "run", f"{i}.png")
                    try:
                        self.frames['Archer']["run_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer run frame '{i}.png': {e}")
                        self.frames['Archer']["run_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames['Archer']["jump_frames"] = []
                sizes = [91, 93, 88, 90, 94, 89, 88, 90]
                for i in range(8):
                    img_path = os.path.join(base_path, "jump", f"{i}.png")
                    try:
                        self.frames['Archer']["jump_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer jump frame '{i}.png': {e}")
                        self.frames['Archer']["jump_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames['Archer']["shot_frames"] = []
                sizes = [90, 72, 72, 72, 72, 72, 97, 113, 106, 89, 77, 72, 70]
                for i in range(13):
                    img_path = os.path.join(base_path, "shot", f"{i}.png")
                    try:
                        self.frames['Archer']["shot_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer shot frame '{i}.png': {e}")
                        self.frames['Archer']["shot_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames['Archer']["attack_frames"] = []
                sizes = [78, 60, 132, 62]
                for i in range(4):
                    img_path = os.path.join(base_path, "attack", f"{i}.png")
                    try:
                        self.frames['Archer']["attack_frames"].append(pygame.transform.scale(pygame.image.load(img_path), (sizes[i], 100)))
                    except Exception as e:
                        print(f"Error loading Archer attack frame '{i}.png': {e}")
                        self.frames["attack_frames"].append(pygame.Surface((sizes[i], 100)))
                self.frames['Archer']["death_frames"] = []
                sizes = [(98, 100), (102, 100), (150, 43)]
                for i in range(3):
                    img_path = os.path.join(base_path, "death", f"{i}.png")
                    try:
                        self.frames['Archer']["death_frames"].append(pygame.transform.scale(pygame.image.load(img_path), sizes[i]))
                    except Exception as e:
                        print(f"Error loading Archer death frame '{i}.png': {e}")
                        self.frames['Archer']["death_frames"].append(pygame.Surface(sizes[i]))
                self.frames['Archer']["arrow_pic"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Arrow.png")), (30, 2))
                self.frames['Archer']["firedarrow_pic"] = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fired arrow.png")), (30, 8))
                print("Hero assets loaded successfully")
        except Exception as e:
            print(f"Error loading hero assets: {e}")
            self.frames = {key: [pygame.Surface((50, 50)) for _ in range(10)] for key in ["idle_frames", "run_frames", "jump_frames"]}

        self.load_ui_assets(self.hero_type)

        # hero and opponent
        self.hero = type('Hero', (), {
            'x_pos': 0, 'y_pos': 0, 'Look': 'right', 'health': 100,
            'current_picture': self.frames['Roboman']["idle_frames"][0],
            'hitbox': pygame.Rect(0, 0, self.frames['Roboman']["idle_frames"][0].get_width(), self.frames['Roboman']["idle_frames"][0].get_height())
        })()
        self.opponent = type('Hero', (), {
            'x_pos': 0,
            'y_pos': 0,
            'Look': 'right',
            'health': 100,
            'frame_source': 'idle_frames',
            'frame_index': 0,
            'username': '',
            'current_picture': self.frames['Roboman']["idle_frames"][0],
            'hitbox': pygame.Rect(0, 0, self.frames['Roboman']["idle_frames"][0].get_width(), self.frames['Roboman']["idle_frames"][0].get_height())
        })()

 


    def send_data(self, data):
        """Send JSON data to the server."""
        try:
            print(f"[CLIENT] Sending data: {json.dumps(data)}")
            self.socket.sendall(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"[CLIENT] Error sending data: {e}")
            self.socket.close()
            return

    def receive_data(self):
        """Receive and process data from the server."""
        buffer = ""
        try:
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    print("[CLIENT] Server disconnected.")
                    break
                buffer += chunk.decode('utf-8')

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        self.process_data(data)
                    except json.JSONDecodeError as e:
                        print(f"[CLIENT] Error decoding JSON: {e}")
        except Exception as e:
            print(f"[CLIENT] Error receiving data: {e}")

    def process_data(self, data):
        """Process the received game data from the server."""
        if data.get("type") == "game_over":
            print(f"Game Over! Winner: {data.get('winner')}")
            self.is_dead = True
        else:
            # Update game state (e.g., player positions, health, etc.)
            self.update_game_state(data)

    def update_game_state(self, data):
        """Update the client game state based on the received data."""
        self.other_players_states = data.get("opponents", [])
        self.bullets = data.get("bullets", [])
        self.current_picture = pygame.image.load(data.get("character", "default.png"))

    def game_loop(self):
        """Main game loop."""
        clock = pygame.time.Clock()

        while not self.is_dead:
            self.handle_events()
            self.receive_data()

            # Update game display
            self.render_game()

            # Control frame rate
            clock.tick(60)

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_dead = True

        # Get keyboard inputs
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # Prepare input data
        input_data = {
            "A": keys[pygame.K_a],
            "D": keys[pygame.K_d],
            "W": keys[pygame.K_w],
            "LSHIFT": keys[pygame.K_LSHIFT],
            "G": keys[pygame.K_g],
            "TAB": keys[pygame.K_TAB],
            "left_click": mouse[0],
            "right_click": mouse[2]
        }

        # Send player inputs to server
        self.send_data(input_data)

    def render_game(self):
        """Render the game state to the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black

        # Draw the current player (this is where you would draw the character sprite, health bar, etc.)
        if not self.is_dead:
            self.screen.blit(self.current_picture, (100, 100))  # Example position

        # Draw other players (if any)
        for player in self.other_players_states:
            self.screen.blit(player.get("frame_to_display", self.current_picture), (player["x_pos"], player["y_pos"]))

        # Update the screen
        pygame.display.flip()

    def disconnect(self):
        """Close the connection with the server."""
        try:
            self.socket.close()
        except Exception as e:
            print(f"[CLIENT] Error closing socket: {e}")

