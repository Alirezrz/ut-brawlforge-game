import pygame
import os
from openai import OpenAI
import threading
import time
from config import screen_height,screen_width,bossProfileSideSize,boss_healthBar_thickness
from src.engine.flyingdemon import FlyingDemon

client = OpenAI(
    api_key="tpsg-2pMQn399nKMGRcOpaBXAentWTdEPkbA",
    base_url="https://api.metisai.ir/openai/v1"
)
class Dragon_Lord:
    def __init__(self, x, y, target):
        self.dialog_thread = None
        self.keep_talking = True
        self.DEAD=False
        self.x_pos = x
        self.y_pos = y
        self.width = 150
        self.height = 180
        self.flyingdemons=[]
        self.target = target
        self.hurt_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "boss", "boss hurt.mp3"))        
        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.last_dialog = ""
        self.last_dialog_time = 0  
        self.dialog_display_duration = 5000 
        self.Look = 'right'
        self.horizontal_speed = 4
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health =1000
        self.max_health = 100

        self.attacking = False
        self.attack_hits = 0
        self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
        if self.target:
            self.prompt = f"Dragon Lord has {self.health} HP. Player is at ({self.target.x_pos}, {self.target.y_pos})."
        else:
            self.prompt = f"Dragon Lord has {self.health} HP. No target yet."
        self.status = 'idle'
        self.current_picture = None
        self.current_frame_index = 0
        self.animation_speed = 150
        self.profile_picture = pygame.image.load("src/assets/images/Dragon_Lord/profile.png")
        self.profile_picture=pygame.transform.scale(self.profile_picture, (bossProfileSideSize, bossProfileSideSize))
        self.health_bar_frame=pygame.image.load("src/assets/images/Dragon_Lord/health_bar_frame.png")
        self.health_bar=pygame.image.load("src/assets/images/Dragon_Lord/health_bar.png")
        self.health_bar_frame=pygame.transform.scale(self.health_bar_frame, (screen_width-bossProfileSideSize, bossProfileSideSize))
        self.max_health=self.health
        self.dialog_frame=pygame.image.load("src/assets/images/Dragon_Lord/dialog_frame.png")
        self.dialog_frame=pygame.transform.scale(self.dialog_frame, (screen_width-bossProfileSideSize, 115))
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Dragon_Lord")
        self.last_attack_time = 0
        self.last_damage_time = 0
        self.prompt_type = "idle"
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "idle", f"{i}.png")), (w, 180))
            for i, w in enumerate([137, 143, 150, 143])
        ]

        self.walk_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "walk", f"{i}.png")), (w, 180))
            for i, w in enumerate([102, 86, 132, 122, 85, 86, 132, 122])
        ]

        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "attack", f"{i}.png")), (w, 180))
            for i, w in enumerate([137,158,169,184,299,249,188,211,224,218,191,168,136,187,155,173])
        ]
        sizes=[(137,180),(165,187),(164,189),(159,190),(190,180),(178,170),(397,360),(425,530),(512,530),(515,540),(505,540),(582,530),(550,530),(518,530),(425,530),(347,530),(273,530),(279,530),(243,530),(243,530),(265,530),(220,360),(203,360),(157,360),(122,540),(118,540),(118,540),(132,540),(180,54)]
        self.death_frames=[]
        for i in range(29):
            self.death_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(
                            base_path,"death",f"{i}.png"
                        )
                    ),
                    sizes[i]
                )
            )
        self.current_picture = self.idle_frames[0]
        self.camera=None
        self.is_dying = False
        self.number_of_spotlight_activation=0
        self.start_dialog_loop()
    def get_prompt(self):
        if self.prompt_type == "attack":
            return f"Dragon Lord is unleashing a blazing punch at the player at ({self.target.x_pos}, {self.target.y_pos}).  (maximum number of words = 8)"
        elif self.prompt_type == "damage":
            return f"Dragon Lord landed a fiery hit! Player health is now {self.target.health}. (maximum number of words = 8)"
        else:
            return f"Dragon Lord has {self.health} HP. Player is at ({self.target.x_pos}, {self.target.y_pos}). (maximum number of words = 8)"
    def say_dialog_loop(self):
        while self.keep_talking:
            try:
                self.prompt = self.get_prompt()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a menacing game boss named Dragon Lord. Speak in short, taunting lines to the player."
                        },
                        {
                            "role": "user",
                            "content": self.prompt
                        }
                    ],
                    max_tokens=50,
                    temperature=0.7
                )
                self.last_dialog = response.choices[0].message.content.strip()
                print("Dragon Lord says:", response.choices[0].message.content.strip())
                self.last_dialog_time = pygame.time.get_ticks()
            except Exception as e:
                print(f"[Error getting dialog: {e}]")
                time.sleep(15)
            self.prompt_type = "idle"  

    def start_dialog_loop(self):
        if self.dialog_thread is None or not self.dialog_thread.is_alive():
            self.dialog_thread = threading.Thread(target=self.say_dialog_loop, daemon=True)
            self.dialog_thread.start()

    def stop_dialog_loop(self):
        self.keep_talking = False

    def display(self, screen, offset):
        if self.health < 0:
            self.health=0
        self.health_bar=pygame.transform.scale(self.health_bar, ((self.health/self.max_health)*(screen_width-bossProfileSideSize-2*boss_healthBar_thickness), bossProfileSideSize-2*boss_healthBar_thickness+26))
        screen.blit(self.profile_picture,(0,screen_height-bossProfileSideSize))
        screen.blit(self.health_bar_frame,(bossProfileSideSize,screen_height-bossProfileSideSize))
        screen.blit(self.health_bar,(bossProfileSideSize+boss_healthBar_thickness,screen_height-bossProfileSideSize+boss_healthBar_thickness-13))        
        image = self.current_picture
        if self.Look == 'left':
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, (self.x_pos - offset[0], self.y_pos - offset[1]))

        current_time = pygame.time.get_ticks()
        if self.last_dialog and (current_time - self.last_dialog_time < self.dialog_display_duration):
            font = pygame.font.SysFont("arial", 20, bold=True)
            text_surface = font.render(self.last_dialog, True, (0, 0, 0))  
            text_rect = text_surface.get_rect()
            text_rect.midbottom = ((boss_healthBar_thickness*2)-60+bossProfileSideSize + (screen_width - bossProfileSideSize) // 2, screen_height - bossProfileSideSize - 55)
            screen.blit(self.dialog_frame,(bossProfileSideSize-35,screen_height - bossProfileSideSize -120))
            screen.blit(text_surface, text_rect)

        for kid in self.flyingdemons:
            kid.display(screen,offset)

    def update_animation(self):
        if self.status=='dead':
            self.current_picture==self.death_frames[28]
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update_time < self.animation_speed:
            return

        self.last_frame_update_time = current_time

        if self.status=='dying':
            if self.current_frame_index < len(self.death_frames):
                current_image = self.death_frames[self.current_frame_index]
                new_width, new_height = current_image.get_size()
                self.x_pos = self.previous_center[0] - new_width // 2
                self.y_pos = self.previous_center[1] - new_height
                self.width, self.height = new_width, new_height
                self.current_picture = current_image
                self.current_frame_index += 1
                if self.current_frame_index==29:
                    self.status=='dead'
                    self.DEAD = True
            else:
                self.current_picture = self.death_frames[-1]
                self.DEAD=True
            return

        if self.status == 'attack':
            if self.current_frame_index < len(self.attack_frames):
                self.current_picture = self.attack_frames[self.current_frame_index]
                if self.current_frame_index in [3, 7, 12]:
                    if self.Look == 'right' and self.allow_move_right:
                        self.x_pos += 50
                    elif self.allow_move_left:
                        self.x_pos -= 50
                    self.hitbox.topleft = (self.x_pos, self.y_pos)
                self.check_attack_collision()
                self.current_frame_index += 1
            else:
                self.attacking = False
                self.attack_hits = 0
                self.status = 'idle'
                self.current_frame_index = 0
            return

        if self.status == 'walk':
            frames = self.walk_frames
        else:
            frames = self.idle_frames

        self.current_frame_index = (self.current_frame_index + 1) % len(frames)
        self.current_picture = frames[self.current_frame_index]

    def move_right(self):
        if self.allow_move_right and not self.attacking and not self.is_dying:
            self.x_pos += self.horizontal_speed
            self.Look = 'right'
            self.status = 'walk'
            self.is_moving_horizontally = True
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        if self.allow_move_left and not self.attacking and not self.is_dying:
            self.x_pos -= self.horizontal_speed
            self.Look = 'left'
            self.status = 'walk'
            self.is_moving_horizontally = True
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def fall_from_platform(self):
        if self.current_platform and (
            self.x_pos + self.width < self.current_platform.x_pos or
            self.x_pos > self.current_platform.x_pos + self.current_platform.width
        ):
            self.on_ground = False
            self.current_platform = None

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def horizontal_move(self):
        self.x_pos += self.horizontal_auto_speed
        self.horizontal_auto_speed = 0
    def platforms_collisions(self, platforms):
    # Reset movement flags
        self.allow_move_left = True
        self.allow_move_right = True

        for platform in platforms:
        # Landing detection
         if self.x_pos + self.width > platform.x_pos+15 and self.x_pos+15 < platform.x_pos + platform.width:
             # Landing on top of platform
             if ((self.y_pos + self.height) >= platform.y_pos) and \
                ((self.y_pos + self.height) < (platform.y_pos + platform.height) + 10) and \
                self.vertical_speed <= 0:  # Only land if moving downward

                 self.on_ground = True
                 self.vertical_speed = 0
                 self.y_pos = platform.y_pos - self.height
                 self.current_platform = platform
                 landed = True
         if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
             if ((self.y_pos + self.height) > platform.y_pos) and \
                  (self.y_pos < platform.y_pos + platform.height):
                 if abs(self.x_pos - (platform.x_pos + platform.width)) <= 15:
                     self.allow_move_left = False
                     self.x_pos = platform.x_pos + platform.width
                 elif abs(self.x_pos + self.width - platform.x_pos) <= 15:
                     self.allow_move_right = False
                     self.x_pos = platform.x_pos - self.width

    def attack(self):
        self.attacking = True
        self.status = 'attack'
        self.current_frame_index = 0
        self.attack_hits = 0
        self.prompt_type = "attack"
        self.last_attack_time = time.time()
        

    def check_attack_collision(self):
       # if self.hitbox.colliderect(self.target.hitbox):
        #    if self.Look == 'right':
         #       self.target.move_right(6)
          #  else:
           #     self.target.move_left(6)

        if self.hitbox.colliderect(self.target.hitbox) and self.attack_hits < 3 and ((self.current_frame_index >= 4 and self.current_frame_index <= 10) or (self.current_frame_index >= 13 and self.current_frame_index <= 15)):
            self.target.health -= 30
            self.attack_hits += 1
            self.prompt_type = "damage"
            self.last_damage_time = time.time()

    def Update(self, screen, scroll, shot_bullets, platforms):
        self.update_animation()
        self.gravity()
        self.vertical_move()
        self.horizontal_move()
        self.platforms_collisions(platforms)
        if self.health <= 0 and not self.is_dying:
            self.die()
            return
        self.AI_behavior()
        
        for kid in self.flyingdemons:
            if kid.death_finished:
                self.flyingdemons.remove(kid)
            

    def AI_behavior(self):
        if self.number_of_spotlight_activation==0:
            self.camera.activate_spotlight()
            self.number_of_spotlight_activation+=1
            
        if self.health<=500 and self.number_of_spotlight_activation<2:
            self.camera.activate_spotlight()
            self.number_of_spotlight_activation+=1
            self.flyingdemons.append(FlyingDemon(self.x_pos+40,self.y_pos+30,self.target,self.Look))
            self.flyingdemons.append(FlyingDemon(self.x_pos-100,self.y_pos+30,self.target,self.Look))
            self.target.attack_targets+=self.flyingdemons
            
        for enemy in self.flyingdemons:
            if hasattr(enemy, 'status') and enemy.status == 'removed':
                self.flyingdemons.remove(enemy)
            
        if self.attacking:
            return

        distance_x = abs(self.target.x_pos - self.x_pos)
        distance_y = abs(self.target.y_pos - self.y_pos)

        if distance_x <= 90 and distance_y < 200 and not self.is_dying:
            self.attack()
        elif self.target.x_pos > self.x_pos and not self.is_dying:
            self.move_right()
        elif self.target.x_pos < self.x_pos and not self.is_dying:
            self.move_left()
            
            
    def Active_spot_light_effect(self):
        if not hasattr(self, 'spotlight_alpha'):
            self.spotlight_alpha = 0
            self.spotlight_max_alpha = 180
            self.spotlight_fade_speed = 5
            self.spotlight_active = True
            self.spotlight_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

        if not self.spotlight_active:
            self.spotlight_alpha = 0
            self.spotlight_active = True

        if self.spotlight_alpha < self.spotlight_max_alpha:
            self.spotlight_alpha += self.spotlight_fade_speed

        self.spotlight_surface.fill((0, 0, 0, 0))  
        pygame.draw.circle(
            self.spotlight_surface,
            (0, 0, 0, self.spotlight_alpha),
            (int(self.target.x_pos - self.camera.scroll[0] + self.target.width // 2),
            int(self.target.y_pos - self.camera.scroll[1] + self.target.height // 2)),
            200
        )
        self.camera.screen.blit(self.spotlight_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        
        
    def die(self):
        if self.status == 'dying' or self.status=='dead':
            return  

        self.status = 'dying'
        self.current_frame_index = 0
        self.attacking = False
        self.is_dying = True
        self.keep_talking = False
        self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
        
    def hurt(self):
        self.hurt_sound.play()

    
    