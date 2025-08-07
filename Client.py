import pygame
import threading
import socket
import json
import os
from src.levels import multiplayer_data, load_level_data
from config import screen_width, screen_height,profileSideSize,health_bar_lenght,roboman_health_bar_frame_thickness


pygame.init()


class Client:
    def __init__(self, sock, username, player_id, hero_type):
        self.socket = sock
        self.username = username
        self.player_id = player_id
        self.hero_type = hero_type
        self.screen_height=screen_height
        self.screen_width=screen_width
        self.is_dead=False
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"BrawlForge - {username}")
        self.drone={}
        self.frames = {
            "Roboman": {}, "Ninja": {}, "NinjaGirl": {}, "Archer": {}
        }
        self.ui_cache = {}
        self.other_players_states = []
        self.bullets = []
        self.scroll = [0, 0]
        
        self.objects=[]
        self.x_pos, self.y_pos, self.health, self.Look = 0, 0, 100, 'right'
        self.current_picture = pygame.Surface((50, 100)) 
        self.character_name = "Ninja"
        self.creation_index = 1
        
        self.load_assets()
        try:
            self.current_picture = self.frames[self.hero_type]['idle_frames'][0]
        except (KeyError, IndexError):
           self.current_picture = pygame.Surface((70, 118), pygame.SRCALPHA)
    
    
    
    def load_assets(self):
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
            base_path = os.path.join('src', "assets", "images", "Guard Drone")
            self.drone_idle_frames = [pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, 'idle', f"{i}.png")), (50, 35)) for i in range(8)]
            self.drone_forward_frames = [pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, 'walk', f"{i}.png")), (50, 35)) for i in range(8)]
            self.drone_backward_frames = [pygame.transform.flip(pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, 'walk', f"{i}.png")), (50, 35)),True,False) for i in range(8)]

        except e:
            print(e)
            
        try:
            self.base_path = os.path.join("src", "assets", "images", "Gate")
            self.DoorOpen_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "DoorOpen.png")), (91, 150))
            self.DoorClose_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "DoorLocked.png")), (91, 150))
            self.GreenFalg_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "Switch (1).png")), (21, 75))
            self.RedFalg_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "Switch (2).png")), (21, 75))
        except  e :
            print(e)
            
        try:
            base_path = os.path.join("src", "assets", "images", "power ups")
            self.double_jump_powerup_frame=pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "double jump.png")
                ),
                (60, 60)
            )
            self.guard_drone_powerup_frame=pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "guard drone.png")
                ),
                (60, 60)
            )
            self.superpower_powerup_frame=pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "super power.png")
                ),
                (60, 60)
            )
        except e:
            print(e)
            
        try:
            path = os.path.join("src", "assets", "images", "Objects","health_box","Box.png")

            self.health_box_frame=pygame.transform.scale(
            pygame.image.load(path),
            (57,45)
            )
        except e:
            print(e)
            
        
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

    def send_input_loop(self):
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
            print(f"sending ={input_data}\n\n\n")
            self.send_json(input_data)
            clock.tick(30)

    def play_sound(self, event_name, character_name="Ninja"):
        try:
            path = f"src/assets/sounds/{character_name}/{event_name}.mp3"
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception as e:
            print(f"Error playing sound for {character_name} - {event_name}: {e}")


    def load_ui_assets(self, character_name):
        if character_name=="Roboman":
            base_path = os.path.join("src", "assets", "images", "RoboMan_pictures")
        else:
            base_path = os.path.join("src", "assets", "images", character_name)

        try:
            if character_name=="Roboman":
                self.profile_picture = pygame.image.load(os.path.join(base_path, "hero_profile.png"))
            elif character_name=="Ninja":
                self.profile_picture = pygame.image.load(os.path.join(base_path, "ninja_profile.png"))    
            else:
                self.profile_picture = pygame.image.load(os.path.join(base_path, "profile.png"))
        except:
            self.profile_picture = pygame.Surface((profileSideSize, profileSideSize))
            self.profile_picture.fill((100, 100, 100))

        try:
            if character_name=="Roboman":
                self.health_bar = pygame.image.load(os.path.join(base_path, "Roboman_health_bar.png"))
            elif character_name=="Ninja":
                self.health_bar = pygame.image.load(os.path.join(base_path, "Ninja_health_bar.png"))
            else:
                self.health_bar = pygame.image.load(os.path.join(base_path, "health_bar.png"))
        except:
            self.health_bar = pygame.Surface((health_bar_lenght, 20))
            self.health_bar.fill((255, 0, 0))

        try:
            if character_name=="Roboman":
                self.health_bar_frame = pygame.image.load(os.path.join(base_path, "Roboman_health_bar_frame.png"))
            elif character_name=="Ninja":
                self.health_bar_frame = pygame.image.load(os.path.join(base_path, "Ninja_health_bar_frame.png"))
            else:
                self.health_bar_frame = pygame.image.load(os.path.join(base_path, "health_bar_frame.png"))
        except:
            self.health_bar_frame = pygame.Surface((health_bar_lenght + 2 * roboman_health_bar_frame_thickness, 22))
            self.health_bar_frame.fill((255, 255, 255))

    def load_ui_assets_for_opponent(self, character_name):
        if character_name=="Roboman":
            base_path = os.path.join("src", "assets", "images", "RoboMan_pictures")
        else:
            base_path = os.path.join("src", "assets", "images", character_name)

        try:
            if character_name=="Roboman":
                profile_picture = pygame.image.load(os.path.join(base_path, "hero_profile.png"))
            elif character_name=="Ninja":
                profile_picture = pygame.image.load(os.path.join(base_path, "ninja_profile.png"))    
            else:
                profile_picture = pygame.image.load(os.path.join(base_path, "profile.png"))
        except:
            profile_picture = pygame.Surface((profileSideSize, profileSideSize))
            profile_picture.fill((100, 100, 100))

        try:
            if character_name=="Roboman":
                health_bar = pygame.image.load(os.path.join(base_path, "Roboman_health_bar.png"))
            elif character_name=="Ninja":
                health_bar = pygame.image.load(os.path.join(base_path, "Ninja_health_bar.png"))
            else:
                health_bar = pygame.image.load(os.path.join(base_path, "health_bar.png"))
        except:
            health_bar = pygame.Surface((health_bar_lenght, 20))
            health_bar.fill((255, 0, 0))

        try:
            if character_name=="Roboman":
                health_bar_frame = pygame.image.load(os.path.join(base_path, "Roboman_health_bar_frame.png"))
            elif character_name=="Ninja":
                health_bar_frame = pygame.image.load(os.path.join(base_path, "Ninja_health_bar_frame.png"))
            else:
                health_bar_frame = pygame.image.load(os.path.join(base_path, "health_bar_frame.png"))
        except:
            health_bar_frame = pygame.Surface((health_bar_lenght + 2 * roboman_health_bar_frame_thickness, 22))
            health_bar_frame.fill((255, 255, 255))

        return profile_picture,health_bar,health_bar_frame
                
    def get_ui_assets_cached(self, character_name):
        if character_name not in self.ui_cache:
            self.ui_cache[character_name] = self.load_ui_assets_for_opponent(character_name)
        return self.ui_cache[character_name]
    
    def receive_state_loop(self):
        buffer = ""
        while True:
            try:
                    chunk = self.socket.recv(1024)
                    if not chunk:
                        break
                    buffer += chunk.decode('utf-8')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        print(line)



                        try:
                            parsed = json.loads(line)
                            self.objects = parsed.get('objects', [])
                            selfdata = parsed["self"]
                            self.drone=selfdata.get("drone","empty")
                           
                            self.x_pos = selfdata['x_pos']
                            self.y_pos = selfdata['y_pos']
                            self.is_dead = selfdata.get("is_dead", False)
                            self.health = selfdata['health']
                            self.Look = selfdata['look']
                            self.username = selfdata['username']
                            self.frame_source = selfdata['frame_source']
                            self.frame_index = selfdata['frame_index']
                            self.character_name = selfdata.get("character", "Ninja")
                            self.creation_index = selfdata.get("creation_index", -1)
                            for event in selfdata.get("events", []):
                                self.play_sound(event, self.character_name)
                            
                            

                            type_of_hero = selfdata['character']
                            frame_source = selfdata['frame_source']
                            frame_index = selfdata['frame_index']
                            frame_list = self.frames[type_of_hero].get(frame_source, [])
                            if frame_list:
                                self.current_picture = frame_list[frame_index]
                            

                            self.bullets = parsed.get("bullets", [])

                            self.other_players_states = []
                            # نکته :اطلاعات حریف ها و هم تیمی توی یک لیست دارن ذخیره میشن و اگر هم تیمی داشته باشیم ایندکس اخر لیست برای اون هست
                            # Handle opponents (always present in both 1v1 and 2v2)
                            opponents = parsed.get("opponents", [])
                            for opponent_data in opponents:
                                

                                opponent_char = opponent_data.get("character", "Ninja")
                                creation_index = opponent_data.get("creation_index", -1)
                                opponent_frame_source = opponent_data.get("frame_source", "idle_frames")
                                opponent_frame_index = opponent_data.get("frame_index", 0)
                                opponent_frame_list = self.frames[opponent_char].get(opponent_frame_source, [])
                                opponent_frame = opponent_frame_list[opponent_frame_index]
                                for event in opponent_data.get("events", []):
                                    self.play_sound(event, opponent_char)
                                opp_profile, opp_health_bar, opp_health_bar_frame = self.get_ui_assets_cached(opponent_char)

                                
                                self.other_players_states.append({
                                    "x_pos": opponent_data.get("x_pos", 0),
                                    "y_pos": opponent_data.get("y_pos", 0),
                                    "username": opponent_data.get("username", "Player"),
                                    "frame_to_display": opponent_frame,
                                    "health": opponent_data.get("health", 100),
                                    "profile_picture": opp_profile,
                                    "health_bar": opp_health_bar,
                                    "health_bar_frame": opp_health_bar_frame,
                                    "Look":opponent_data.get('look','right'),
                                    "creation_index": opponent_data.get("creation_index", 0),
                                    "is_dead": opponent_data.get("is_dead", False)
                                })

                               

                            # Handle teammate (only present in 2v2 mode)
                            teammate_data = parsed.get("teammate")
                            if teammate_data:
                                teammate_char = teammate_data.get("character", "Ninja")
                                teammate_frame_source = teammate_data.get("frame_source", "idle_frames")
                                teammate_frame_index = teammate_data.get("frame_index", 0)
                                creation_index = teammate_data.get("creation_index", -1)

                                teammate_frame_list = self.frames[teammate_char].get(teammate_frame_source, [])
                                teammate_frame = teammate_frame_list[teammate_frame_index] 
                                for event in teammate_data.get("events", []):
                                    self.play_sound(event, teammate_char)
                                opp_profile, opp_health_bar, opp_health_bar_frame = self.get_ui_assets_cached(teammate_char)
                                self.other_players_states.append({
                                    "x_pos": teammate_data.get("x_pos", 0),
                                    "y_pos": teammate_data.get("y_pos", 0),
                                    "username": teammate_data.get("username", "Player"),
                                    "frame_to_display": teammate_frame,
                                    "health": teammate_data.get("health", 100),
                                    "Look":teammate_data.get('look','right'),
                                    "profile_picture": opp_profile,
                                    "health_bar": opp_health_bar,
                                    "health_bar_frame": opp_health_bar_frame,
                                    "creation_index": opponent_data.get("creation_index", 0)
                                })
                           
                        except Exception as e:
                            print(f"Error decoding JSON or setting frames: {e}")

            except Exception as e:
                    print(f"Error receiving game state: {e}")
                    break
    def get_bar_position_from_index(self,index,opponents_count):
        # حالت 1v1
        if opponents_count == 1:
            if index == 1:
                return False, False  # پلیر اول → چپ بالا
            elif index == 2:
                return True, False   # پلیر دوم → راست بالا
            else:
                return False, False

        # حالت 2v2
        else:
            if index == 1:
                return False, False  # چپ بالا
            elif index == 2:
                return False, True   # چپ پایین
            elif index == 3:
                return True, False   # راست بالا
            elif index == 4:
                return True, True    # راست پایین
            else:
                return False, False    
    def draw_health_bar(self, screen, health, profile_picture, health_bar, health_bar_frame, is_right_side, is_bottom):
        if health < 0:
            health = 0
        scaled_frame_height = profileSideSize
        frame_img = pygame.transform.scale(
            health_bar_frame,
            (health_bar_lenght + (2 * roboman_health_bar_frame_thickness), scaled_frame_height)
        )
        bar_img = pygame.transform.scale(
            health_bar,
            (
                int(health_bar_lenght * (health / 100)),
                scaled_frame_height - (2 * roboman_health_bar_frame_thickness)
            )
        )

        if is_right_side:
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            profile_x = self.screen_width - profileSideSize
        else:
            bar_x = profileSideSize
            profile_x = 0

        if is_bottom:
            bar_y = self.screen_height - scaled_frame_height
            profile_y = self.screen_height - profileSideSize
        else:
            bar_y = 0
            profile_y = 0

        health_x = bar_x + roboman_health_bar_frame_thickness
        health_y = bar_y + roboman_health_bar_frame_thickness

        screen.blit(frame_img, (bar_x, bar_y))
        screen.blit(bar_img, (health_x, health_y))

        if profile_picture:
            if is_right_side:
                profile_picture = pygame.transform.flip(profile_picture, True, False)
            screen.blit(pygame.transform.scale(profile_picture, (profileSideSize, profileSideSize)), (profile_x, profile_y))                               
    def render_game(self):
        if self.screen==None:
            pygame.display.set_caption("BrawlForge Client")
            
        self.screen.blit(self.background,(0, 0))
        try:
            font = pygame.font.Font("src/assets/fonts/VCR_OSD_MONO.ttf", 20)
        except:
            font = pygame.font.SysFont("arial", 20)
       
        
        mid_x = (self.x_pos + self.current_picture.get_width() // 2)
        mid_y = (self.y_pos + self.current_picture.get_height() // 2)
        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15
        
        for obj in self.objects:
         try:
            if obj.get("status") == "used":
                continue  
            x_pos = obj.get("x_pos", 0)
            y_pos = obj.get("y_pos", 0)
            obj_type = obj.get("type", "")

            if obj_type == "gates":
                a_x = obj.get("A_x", 0)
                a_y = obj.get("A_y", 0)
                b_x = obj.get("B_x", 0)
                b_y = obj.get("B_y", 0)
                a_state = obj.get("A_state", "close")
                b_state = obj.get("B_state", "close")
                flag = obj.get("flag", "GreenFlag")

                a_pic = self.DoorOpen_pic if a_state == "open" else self.DoorClose_pic
                b_pic = self.DoorOpen_pic if b_state == "open" else self.DoorClose_pic
                flag_pic = self.RedFlag_pic if flag == "RedFlag" else self.GreenFlag_pic

                self.screen.blit(a_pic, (a_x - self.scroll[0], a_y - self.scroll[1]))
                self.screen.blit(b_pic, (b_x - self.scroll[0], b_y - self.scroll[1]))
                self.screen.blit(flag_pic, (a_x - 30 - self.scroll[0], a_y + 75 - self.scroll[1]))
                self.screen.blit(flag_pic, (b_x - 30 - self.scroll[0], b_y + 75 - self.scroll[1]))

            elif obj_type == "double jump":
                self.screen.blit(self.double_jump_powerup_frame, (x_pos - self.scroll[0], y_pos - self.scroll[1]))
            elif obj_type == "guard drone":
                self.screen.blit(self.guard_drone_powerup_frame, (x_pos - self.scroll[0], y_pos - self.scroll[1]))
            elif obj_type == "super power":
                self.screen.blit(self.superpower_powerup_frame, (x_pos - self.scroll[0], y_pos - self.scroll[1]))
            elif obj_type == "health_box":
                self.screen.blit(self.health_box_frame, (x_pos - self.scroll[0], y_pos - self.scroll[1]))

         except Exception as e:
            print(f"Error rendering object {obj}: {e}")

        for platform in self.platforms:
            try:
                 platform.draw(self.screen, self.scroll)
            except Exception as e:
                 print(f"Error drawing platform: {e}")
        if self.current_picture and  not self.is_dead:
            self_image = pygame.transform.flip(self.current_picture, True, False) if self.Look == 'left' else self.current_picture
            self.screen.blit(self_image, (self.x_pos - self.scroll[0], self.y_pos - self.scroll[1]))
            if isinstance(self.drone, dict) and 'frame_source' in self.drone:
                if self.drone['frame_source']=="idle_frames":
                    self.screen.blit(self.drone_idle_frames[self.drone['frame_index']],(self.drone['x_pos']-self.scroll[0],self.drone['y_pos']-self.scroll[1]))
                elif self.drone['frame_source']=="forward":
                    self.screen.blit(self.drone_forward_frames[self.drone['frame_index']],(self.drone['x_pos']-self.scroll[0],self.drone['y_pos']-self.scroll[1]))
                elif self.drone['frame_source']=="backward":
                    self.screen.blit(self.drone_backward_frames[self.drone['frame_index']],(self.drone['x_pos']-self.scroll[0],self.drone['y_pos']-self.scroll[1]))                    
            username_surface = font.render(self.username, True, (255, 255, 255))
            username_rect = username_surface.get_rect(center=(self.x_pos - self.scroll[0] + self_image.get_width() / 2, self.y_pos - self.scroll[1] - 15))
            self.screen.blit(username_surface, username_rect)
                
        for player_state in self.other_players_states:
          if not player_state.get("is_dead",False):
            opponent_image = player_state["frame_to_display"]
            px = player_state.get("x_pos", 0)
            py = player_state.get("y_pos", 0)
            p_look = player_state.get('Look', 'right')
            p_username = player_state.get('username', 'Player') 
        
            if p_look == 'left':
               opponent_image = pygame.transform.flip(opponent_image, True, False)
    
            self.screen.blit(opponent_image, (px - self.scroll[0], py - self.scroll[1]))
            other_username_surface = font.render(p_username, True, (220, 220, 220))
            other_username_rect = other_username_surface.get_rect(center=(px - self.scroll[0] + opponent_image.get_width() / 2, py - self.scroll[1] - 15))
            self.screen.blit(other_username_surface, other_username_rect)
            drone = player_state.get('drone', 'None')
            if drone != 'None':
                if drone['frame_source'] == "idle_frames":
                    self.screen.blit(self.drone_idle_frames[drone['frame_index']], (drone['x_pos'] - self.scroll[0], drone['y_pos'] - self.scroll[1]))
                elif drone['frame_source'] == "forward":
                    self.screen.blit(self.drone_forward_frames[drone['frame_index']], (drone['x_pos'] - self.scroll[0], drone['y_pos'] - self.scroll[1]))
                elif drone['frame_source'] == "backward":
                    self.screen.blit(self.drone_backward_frames[drone['frame_index']], (drone['x_pos'] - self.scroll[0], drone['y_pos'] - self.scroll[1]))
            
        for bullet in self.bullets:
            if bullet['owner']=="Roboman":
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                     self.screen.blit(self.Roboman_bullet,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     self.screen.blit(self.Roboman_rocket,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                else:
                    if not bullet["Flag"]:
                     self.screen.blit(pygame.transform.flip(self.Roboman_bullet,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     self.screen.blit(pygame.transform.flip(self.Roboman_rocket,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
            elif bullet['owner']=="Ninja" or bullet['owner']=="NinjaGirl" :
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                     self.screen.blit(self.Kunai,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     self.screen.blit(self.Fired_Kunai,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                else:
                    if not bullet["Flag"]:
                     self.screen.blit(pygame.transform.flip(self.Kunai,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     self.screen.blit(pygame.transform.flip(self.Fired_Kunai,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                     
                     
            elif bullet['owner']=="Archer" :
                if bullet['Look']=='right':
                    if not bullet["Flag"]:
                        self.screen.blit(self.Arrow,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                        self.screen.blit(self.Fired_Arrow,(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                        
                else:
                    if not bullet["Flag"]:
                     self.screen.blit(pygame.transform.flip(self.Arrow,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
                    else:
                     self.screen.blit(pygame.transform.flip(self.Fired_Arrow,True,False),(bullet['x_pos']-self.scroll[0],bullet['y_pos']-self.scroll[1]))
        #باید عکس پروفایل های همه لود بشه و بعد دیسپلی بشن
        is_right_side, is_bottom = self.get_bar_position_from_index(self.creation_index,len(self.other_players_states))
        self.draw_health_bar(self.screen, self.health, self.profile_picture, self.health_bar, self.health_bar_frame, is_right_side, is_bottom)
        for other_state in self.other_players_states:
            idx = other_state.get("creation_index", 0)  
            is_right_side, is_bottom = self.get_bar_position_from_index(
                idx,
                len(self.other_players_states)
            )

            self.draw_health_bar(
                self.screen,
                other_state["health"],
                other_state["profile_picture"],  
                other_state["health_bar"],                
                other_state["health_bar_frame"],
                is_right_side,
                is_bottom
            )

        pygame.display.flip()
    def send_json(self, data):
        try:
            message = json.dumps(data) + '\n'
            self.socket.sendall(message.encode('utf-8'))
        except (socket.error, BrokenPipeError):
            print("Connection to server lost.")    
    def start(self):
        initial_data = {"username": self.username, "character": self.hero_type}
        print(f"DEBUG [Client.py]: Sending initial character data to server: {initial_data}")
        self.send_json(initial_data)

      
        threading.Thread(target=self.send_input_loop, daemon=True).start()
        threading.Thread(target=self.receive_state_loop, daemon=True).start()

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.render_game()
            clock.tick(60)
        try:
           self.socket.close()
        except:
            pass
        pygame.quit()

