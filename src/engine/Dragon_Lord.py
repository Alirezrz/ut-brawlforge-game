import pygame
import os
from openai import OpenAI
import threading
import time

client = OpenAI(
    api_key="tpsg-2pMQn399nKMGRcOpaBXAentWTdEPkbA",
    base_url="https://api.metisai.ir/openai/v1"
)
class Dragon_Lord:
    def __init__(self, x, y, target):
        self.dialog_thread = None
        self.keep_talking = True

        self.x_pos = x
        self.y_pos = y
        self.width = 150
        self.height = 180

        self.target = target

        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.Look = 'right'
        self.horizontal_speed = 4
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 63
        self.max_health = 100

        self.attacking = False
        self.attack_hits = 0
        self.prompt = f"Dragon Lord has {self.health} HP. Player is at ({self.target.x_pos}, {self.target.y_pos})."
        self.status = 'idle'
        self.current_picture = None
        self.current_frame_index = 0
        self.animation_speed = 150
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Dragon_Lord")
        self.last_attack_time = 0
        self.last_damage_time = 0
        self.prompt_type = "idle"
        self.start_dialog_loop()
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

        self.current_picture = self.idle_frames[0]
        self.camera=None

        self.start_dialog_loop()
    def get_prompt(self):
        if self.prompt_type == "attack":
            return f"Dragon Lord is unleashing a blazing punch at the player at ({self.target.x_pos}, {self.target.y_pos})."
        elif self.prompt_type == "damage":
            return f"Dragon Lord landed a fiery hit! Player health is now {self.target.health}."
        else:
            return f"Dragon Lord has {self.health} HP. Player is at ({self.target.x_pos}, {self.target.y_pos})."
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
                print("Dragon Lord says:", response.choices[0].message.content.strip())
            except Exception as e:
                print(f"[Error getting dialog: {e}]")

            time.sleep(8)
            self.prompt_type = "idle"  

    def start_dialog_loop(self):
        if self.dialog_thread is None or not self.dialog_thread.is_alive():
            self.dialog_thread = threading.Thread(target=self.say_dialog_loop, daemon=True)
            self.dialog_thread.start()

    def stop_dialog_loop(self):
        self.keep_talking = False

    def display(self, screen, offset):
        image = self.current_picture
        if self.Look == 'left':
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update_time < self.animation_speed:
            return

        self.last_frame_update_time = current_time

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
        if self.allow_move_right and not self.attacking:
            self.x_pos += self.horizontal_speed
            self.Look = 'right'
            self.status = 'walk'
            self.is_moving_horizontally = True
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        if self.allow_move_left and not self.attacking:
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
        for platform in platforms:
            if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                if ((self.y_pos + self.height) >= platform.y_pos) and ((self.y_pos + self.height) < (platform.y_pos + platform.height)+10):
                    self.on_ground = True
                    self.vertical_speed = 0
                    self.y_pos = platform.y_pos - self.height
                    self.current_platform = platform

            if self.x_pos + self.width >= platform.x_pos and self.x_pos <= platform.x_pos + platform.width:
                if ((self.y_pos + self.height) > platform.y_pos) and ((self.y_pos) < (platform.y_pos + platform.height)):
                    if abs(self.x_pos - (platform.x_pos + platform.width)) <= 10:
                        self.allow_move_left = False
                        self.x_pos = platform.x_pos + platform.width
                    if abs(self.x_pos + self.width - platform.x_pos) <= 10:
                        self.allow_move_right = False
                        self.x_pos = platform.x_pos - self.width
            else:
                self.allow_move_left = True
                self.allow_move_right = True

    def attack(self):
        self.attacking = True
        self.status = 'attack'
        self.current_frame_index = 0
        self.attack_hits = 0
        self.prompt_type = "attack"
        self.last_attack_time = time.time()
        self.camera.activate_spotlight()
        

    def check_attack_collision(self):
        if self.hitbox.colliderect(self.target.hitbox):
            if self.Look == 'right':
                self.target.move_right(6)
            else:
                self.target.move_left(6)

        if self.hitbox.colliderect(self.target.hitbox) and self.attack_hits < 3 and ((self.current_frame_index >= 4 and self.current_frame_index <= 10) or (self.current_frame_index >= 13 and self.current_frame_index <= 15)):
            self.target.health -= 30
            self.attack_hits += 1
            self.prompt_type = "damage"
            self.last_damage_time = time.time()

    def Update(self, keys, platforms):
        self.update_animation()
        self.gravity()
        self.vertical_move()
        self.horizontal_move()
        self.platforms_collisions(platforms)
        self.AI_behavior()

    def AI_behavior(self):
        if self.attacking:
            return

        distance_x = abs(self.target.x_pos - self.x_pos)
        distance_y = abs(self.target.y_pos - self.y_pos)

        if distance_x <= 90 and distance_y < 200:
            self.attack()
        elif self.target.x_pos > self.x_pos:
            self.move_right()
        elif self.target.x_pos < self.x_pos:
            self.move_left()
            
            
    def Active_spot_light_effect(self):
        self.camera.activate_spotlight()