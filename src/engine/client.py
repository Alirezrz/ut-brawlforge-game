import pygame
import threading
import socket
import json
import os
from src.levels import multiplayer_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies
from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width

platform_image_path = "src/assets/images/"
platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }

background = pygame.image.load("src/assets/images/city1.png")
background = pygame.transform.scale(background, (screen_width, screen_height))


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")


HOST = "127.0.0.1"
PORT = 9191

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        pygame.init()
        print("what is your hero type?")
        print("1_ ROBOMAN")
        print("2_ Ninja")
        print("3_ Ninjagirl")
        print("4_ Archer")
        self.type=int(input())
        self.opponent = self
        
        if self.type==1:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "RoboMan_pictures")
            self.freezed_img=pygame.transform.scale(pygame.image.load(os.path.join(base_path,"freezed.png")),(69,118))
            self.run_frames = []
            for i in range(1, 9):
                try:
                    img_path = os.path.join(base_path, "hero_run_frames", f"Run ({i}).png")
                    tmp = pygame.image.load(img_path)
                    if i == 1: self.run_frames.append(pygame.transform.scale(tmp, (63, 118)))
                    elif i == 2: self.run_frames.append(pygame.transform.scale(tmp, (62, 118)))
                    elif i == 3: self.run_frames.append(pygame.transform.scale(tmp, (82, 118)))
                    elif i == 4: self.run_frames.append(pygame.transform.scale(tmp, (77, 118)))
                    elif i == 5: self.run_frames.append(pygame.transform.scale(tmp, (73, 118)))
                    elif i == 6: self.run_frames.append(pygame.transform.scale(tmp, (80, 118)))
                    elif i == 7: self.run_frames.append(pygame.transform.scale(tmp, (92, 118)))
                    elif i == 8: self.run_frames.append(pygame.transform.scale(tmp, (79, 118)))
                except FileNotFoundError:
                    print(f"Error: Roboman run frame 'Run ({i}).png' not found at {img_path}. Check path.")
                    self.run_frames.append(pygame.Surface((70, 118)))

            self.idle_frames = []
            for i in range(1, 11):
                try:
                    img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                    idle_tmp = pygame.image.load(img_path)
                    self.idle_frames.append(pygame.transform.scale(idle_tmp, (70, 118)))
                except FileNotFoundError:
                    print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")
                    self.idle_frames.append(pygame.Surface((70, 118)))

            self.jump_frames = []
            for i in range(1, 11):
                try:
                    img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                    jump_tmp = pygame.image.load(img_path)
                    self.jump_frames.append(pygame.transform.scale(jump_tmp, (70, 118)))
                except FileNotFoundError:
                    print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")

            self.shoot_frames = []
            for i in range(1, 5):
                        try:
                            img_path = os.path.join(base_path, "Shoot", f"Shoot ({i}).png")
                            shoot_tmp = pygame.image.load(img_path)
                            if i == 1: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (83, 118)))
                            elif i == 2: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (83, 118)))
                            elif i == 3: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (82, 118)))
                            elif i == 4: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (84, 118)))
                        except FileNotFoundError:
                            print(f"Error: Roboman Shoot frame 'Shoot ({i}).png' not found at {img_path}. Check path.")
                            self.shoot_frames.append(pygame.Surface((70, 118)))

            self.RunShoot_frames=[]
            for i in range(1, 9):
                try:
                    img_path = os.path.join(base_path, "RunShoot", f"RunShoot ({i}).png")
                    tmp = pygame.image.load(img_path)
                    if i == 1: self.RunShoot_frames.append(pygame.transform.scale(tmp, (83, 118)))
                    elif i == 2: self.RunShoot_frames.append(pygame.transform.scale(tmp, (87, 118)))
                    elif i == 3: self.RunShoot_frames.append(pygame.transform.scale(tmp, (93, 118)))
                    elif i == 4: self.RunShoot_frames.append(pygame.transform.scale(tmp, (97, 118)))
                    elif i == 5: self.RunShoot_frames.append(pygame.transform.scale(tmp, (88, 118)))
                    elif i == 6: self.RunShoot_frames.append(pygame.transform.scale(tmp, (90, 118)))
                    elif i == 7: self.RunShoot_frames.append(pygame.transform.scale(tmp, (100, 118)))
                    elif i == 8: self.RunShoot_frames.append(pygame.transform.scale(tmp, (89, 118)))
                except FileNotFoundError:
                    print(f"Error: Roboman Shoot frame 'Shoot ({i}).png' not found at {img_path}. Check path.")
                    self.RunShoot_frames.append(pygame.Surface((70, 118)))

            self.Jump_frames=[]
            scale_numebrs=[(73,118),(80,118),(90,118),(91,118),(90,118),(109,118),(95,118),(96,118),(84,118)]
            for i in range(1,10):
                try:
                    img_path = os.path.join(base_path, "jump", f"Jump ({i}).png")
                    tmp = pygame.image.load(img_path)
                    if i == 1: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 2: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 3: self.Jump_frames.append(pygame.transform.scale(tmp,scale_numebrs[i-1]))
                    elif i == 4: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 5: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 6: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 7: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 8: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 9: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                except FileNotFoundError:
                    print(f"Error: Roboman jump frame 'Jump ({i}).png' not found at {img_path}. Check path.")
                    self.jump_frames.append(pygame.Surface((70, 118)))
                    print(img_path)

            scale_numebrs=[(97,118),(97,118),(98,118),(95,118),(97,118)]
            for i in range(1,6):
                try:
                    img_path = os.path.join(base_path, "jump shoot", f"JumpShoot ({i}).png")
                    tmp = pygame.image.load(img_path)
                    if i == 1: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 2: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 3: self.JumpShoot_frames.append(pygame.transform.scale(tmp,scale_numebrs[i-1]))
                    elif i == 4: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                    elif i == 5: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                except FileNotFoundError:
                    print(f"Error: Roboman jump shhot frame 'JumpShoot ({i}).png' not found at {img_path}. Check path.")
                    self.JumpShoot_frames.append(pygame.Surface((70, 118)))
                    print(img_path)
            sizes=[(73,118),(84,118),(90,100),(145,90),(133,90),(110,61),(118,56),(118,52),(118,53),(118,53)]
            self.death_frames=[]
            for i in range(1,11):
                self.death_frames.append(pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(
                            base_path,
                            "death",
                            f"Dead ({i}).png"
                        )
                    ),
                    sizes[i-1]
                ))

            img_path = os.path.join(base_path, f"jetpack.png")
            self.jetpack_frame=pygame.image.load(img_path)
            self.jetpack_frame=pygame.transform.scale(self.jetpack_frame, (80,118))
          
          
          
        elif self.type==2:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Ninja")
            # Load Idle image for default state
            tmp = pygame.image.load(os.path.join(base_path, "Idle", f"Idle__000.png"))
            self.current_picture = pygame.transform.scale(tmp, (62, 118))
            

            
            self.freezed_frame=pygame.transform.scale(
                pygame.image.load(os.path.join(base_path,"freezed.png")),
                (62,118)
            )
            
            
            img_path = os.path.join(base_path, "SuperPower effect.png")
            self.SuperPower_pic=pygame.image.load(img_path )
            self.SuperPower_pic=pygame.transform.scale(self.SuperPower_pic,(100,118))

            # Load Idle frames
            self.idle_frames = []
            for i in range(0, 10): 
                img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.idle_frames.append(pygame.transform.scale(tmp, (62, 118)))

            # Load Run frames
            self.run_frames = []
            for i in range(1, 10):
                img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.run_frames.append(pygame.transform.scale(tmp, (94, 118)))
                
            # Load Jump frames
            self.jump_frames = []
            sizes = [77, 69, 69, 71, 70, 70, 77, 84, 95, 93]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.jump_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
            

            # Load Kunai
            img_path = os.path.join(base_path, "Kunai.png")
            self.Kunai_pic = pygame.image.load(img_path)
            self.Kunai_pic = pygame.transform.scale(self.Kunai_pic, (60, 12))
            
            img_path = os.path.join(base_path, "FiredKunai.png") 
            self.Fired_kunai_pic=pygame.image.load(img_path)
            self.Fired_kunai_pic= pygame.transform.scale(self.Fired_kunai_pic, (70, 24))
            
            self.Kunai=self.Kunai_pic

            # Load Throw frames
            self.throw_frames = []
            throw_widths = [72, 66, 83, 81, 79, 79, 78, 86, 78, 66]
            for i in range(10):
                img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                tmp = pygame.image.load(img_path)
                scaled = pygame.transform.scale(tmp, (throw_widths[i], 118))
                self.throw_frames.append(scaled)
            # Load Jump throw frames
            self.jumpThrow_frames = []
            sizes = [85,88,92,99,101,104,103,96,89,89]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.jumpThrow_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
                
                
                
            self.Attack_frames=[]
            sizes = [78,75,85,132,136,149,149,149,147,137]
            self.with_sword_width= [77,75,80,73,95,108,107,105,115,105]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.Attack_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
                
                
            self.JumpAttack_frames=[]
            self.jumpattack_sizes=[(87,118),(86,118),(86,118),(136,118),(136,118),(137,138),(139,138),(140,138),(125,170),(136,118)]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.JumpAttack_frames.append(pygame.transform.scale(tmp, self.jumpattack_sizes[i]))
                
            self.death_frames=[]
            self.death_sizes=[(63,118),(74,118),(127,113),(111,108),(140,100),(157,100),(152,90),(157,90),(160,90),(156,90)]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.death_frames.append(pygame.transform.scale(tmp, self.death_sizes[i]))
                
        
        elif self.type==3:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "NinjaGirl")
            # Load Idle frames
            self.idle_frames = []
            for i in range(0, 10): 
                img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.idle_frames.append(pygame.transform.scale(tmp, (68, 118)))

            # Load Run frames
            size=[82,77,77,90,88,82,78,78,83,84]
            self.run_frames = []
            for i in range(1, 10):
                img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.run_frames.append(pygame.transform.scale(tmp, (size[i], 118)))
                
            # Load Jump frames
            self.jump_frames = []
            sizes = [75, 70,71,71,72,71,78,77,79,79]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.jump_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))  
                
            # Load Kunai
            img_path = os.path.join(base_path, "Kunai.png")
            self.Kunai_pic = pygame.image.load(img_path)
            self.Kunai_pic = pygame.transform.scale(self.Kunai_pic, (60, 12))
            
            img_path = os.path.join(base_path, "FiredKunai.png") 
            self.Fired_kunai_pic=pygame.image.load(img_path)
            self.Fired_kunai_pic= pygame.transform.scale(self.Fired_kunai_pic, (70, 24))
            
            self.Kunai=self.Kunai_pic
            
            # Load Throw frames
            self.throw_frames = []
            throw_widths = [70,68,73,85,69,68,68,77,73,67]
            for i in range(10):
                img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
                tmp = pygame.image.load(img_path)
                scaled = pygame.transform.scale(tmp, (throw_widths[i], 118))
                self.throw_frames.append(scaled)
            
            # Load Jump throw frames
            self.jumpThrow_frames = []
            sizes = [79,77,82,92,94,97,95,89,80,79]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.jumpThrow_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
                
            
            self.Attack_frames=[]
            sizes = [70,70,76,118,121,130,129,127,124,118]
            self.with_sword_width= [70,70,76,69,84,94,92,91,99,91]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.Attack_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
                
            self.JumpAttack_frames=[]
            self.jumpattack_sizes=[(71,118),(67,118),(68,118),(108,118),(108,118),(115,128),(118,133),(119,134),(118,129),(92,118)]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.JumpAttack_frames.append(pygame.transform.scale(tmp, self.jumpattack_sizes[i]))
                
            self.freezed_frame=pygame.transform.scale(
                pygame.image.load(os.path.join(base_path,"freezed.png")),
                (68,118)
            )
            
            
            self.SuperPower_pic=pygame.transform.scale(
                pygame.image.load(os.path.join(base_path,"super power.png")),
                (118,118)
            )
            
            sizes=[(70,118),(83,118),(93,108),(102,90),(104,70),(118,78),(118,73),(118,78),(118,78),(118,79)]
            self.death_frames=[]
            for i in range(10):
                self.death_frames.append(
                    pygame.transform.scale(
                        pygame.image.load(
                            os.path.join(base_path,'death',f"Dead__00{i}.png")
                        ),
                        sizes[i]
                    )
                )
                
                
        elif self.type==4:

            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Archer")

            self.idle_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "idle", f"{i}.png")), (88, 100)) for i in range(6)]
            sizes = [89, 90, 91, 90, 89, 90, 96, 90]
            self.run_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "run", f"{i}.png")), (sizes[i], 100)) for i in range(8)]
            sizes = [91, 93, 88, 90, 94, 89, 88, 90]
            self.jump_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "jump", f"{i}.png")), (sizes[i], 100)) for i in range(8)]
            sizes = [90, 72, 72, 72, 72, 72, 97, 113, 106, 89, 77, 72, 70]
            self.shot_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "shot", f"{i}.png")), (sizes[i], 100)) for i in range(13)]
            self.arrow_pic = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Arrow.png")), (30, 2))
            self.firedarrow_pic = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fired arrow.png")), (30, 8))
            self.freezed_img=pygame.transform.scale(pygame.image.load(os.path.join(base_path, "freezed.png")), (88, 100))
            sizes = [78, 60, 132, 62]
            self.attack_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "attack", f"{i}.png")), (sizes[i], 100)) for i in range(4)]

            self.super_power_effect_picture = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "super power effect.png")), (88, 127))
            sizes=[(98,100),(102,100),(150,43)]
            self.death_frames=[pygame.transform.scale(pygame.image.load(os.path.join(base_path, "death", f"{i}.png")), sizes[i]) for i in range(3)]
            
        self.scroll=[0,0]     
                
                
        self.platforms=load_level_data(multiplayer_data, platform_images)
        
        
        mid_x = (self.hero.hitbox.centerx + self.hero2.hitbox.centerx) / 2
        mid_y = (self.hero.hitbox.centery + self.hero2.hitbox.centery) / 2
        
        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15
 
        


    def send_input(self):
        clock = pygame.time.Clock()
        while True:
            pygame.event.pump()  
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()

            # Create a dictionary of relevant inputs
            input_data = {
                "A": keys[pygame.K_a],
                "D": keys[pygame.K_d],
                "W": keys[pygame.K_w],
                "left click": mouse[0], 
                "right click": mouse[2], 
                "LSHIFT": keys[pygame.K_LSHIFT]
            } 

            # Send the input as JSON
            try:
                self.socket.sendall(json.dumps(input_data).encode('utf-8'))
            except Exception as e:
                print("Connection lost:", e)
                break

            clock.tick(60) 
            
    def receive_state(self):
        while True:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                state_bundle = json.loads(data.decode('utf-8'))

                self_state = state_bundle["self"]
                opponent_state = state_bundle["opponent"]

                self.update_from_state(self_state)
                self.opponent.update_from_state(opponent_state)

            except Exception as e:
                print("Error receiving game state:", e)
                break

            
    def update_from_state(self, state):
        self.x_pos = state["x_pos"]
        self.y_pos = state["y_pos"]
        self.Look = state["Look"]
        self.health = state["health"]

        frame_source = state["frame list address"]
        frame_index = state["frame_index"]

        # Mapping string to actual frame list/image
        if frame_source == "idle_frames":
            self.current_picture = self.idle_frames[frame_index]
        elif frame_source == "run_frames":
            self.current_picture = self.run_frames[frame_index ]
        elif frame_source == "jump_frames":
            self.current_picture = self.jump_frames[frame_index ]
        elif frame_source == "Jump_frames":
            self.current_picture = self.Jump_frames[frame_index]
        elif frame_source == "RunShoot_frames":
            self.current_picture = self.RunShoot_frames[frame_index]
        elif frame_source == "shoot_frames":
            self.current_picture = self.shoot_frames[frame_index ]
        elif frame_source == "JumpShoot_frames":
            self.current_picture = self.JumpShoot_frames[frame_index ]
        elif frame_source == "attack_frames":
            self.current_picture = self.attack_frames[frame_index]
        elif frame_source == "JumpAttack_frames":
            self.current_picture = self.JumpAttack_frames[frame_index]
        elif frame_source == "throw_frames":
            self.current_picture = self.throw_frames[frame_index ]
        elif frame_source == "jumpThrow_frames":
            self.current_picture = self.jumpThrow_frames[frame_index]
        elif frame_source == "death_frames":
            self.current_picture = self.death_frames[frame_index if frame_index >= 0 else -1]
        elif frame_source == "freezed_img" or frame_source == "freezed":
            self.current_picture = self.freezed_img if hasattr(self, "freezed_img") else self.freezed_frame
        elif frame_source == "jetpack_frame":
            self.current_picture = self.jetpack_frame
        elif frame_source == "SuperPower_pic":
            self.current_picture = self.SuperPower_pic
        else:
            self.current_picture = pygame.Surface((50, 50))  # fallback

        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.current_picture.get_width(), self.current_picture.get_height())
                
    def render_game(self):
        screen.blit(background, (0, 0))

        for platform in self.platforms:
            platform.draw(screen, self.scroll)

        mid_x = self.x_pos + self.current_picture.get_width() // 2
        mid_y = self.y_pos + self.current_picture.get_height() // 2
        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15

        if self.Look=='left':
            flag=True
        else:
            flag=False

        flipped_self = pygame.transform.flip(self.current_picture, flag, False)
        screen.blit(flipped_self, (self.x_pos - self.scroll[0], self.y_pos - self.scroll[1]))



        pygame.display.update()
            
            
        
        
        
            
            
            

