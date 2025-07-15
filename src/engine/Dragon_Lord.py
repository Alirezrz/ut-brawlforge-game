import pygame
import os

class Dragon_Lord:
    def __init__(self, x, y,target):
        self.x_pos = x
        self.y_pos = y
        self.width = 150
        self.height = 180

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

        self.target = target

        # Attack state
        self.attacking = False
        self.attack_hits = 0

        # Animation attributes
        self.status = 'idle'
        self.current_picture = None
        self.current_frame_index = 0
        self.animation_speed = 150
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

        # Load sprites
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Dragon_Lord")

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
                    if self.Look == 'right':
                        self.x_pos += 10
                    else:
                        self.x_pos -= 10
                    self.hitbox.topleft = (self.x_pos, self.y_pos)
                self.check_attack_collision()
                self.current_frame_index += 1
            else:
                self.attacking = False
                self.attack_hits = 0
                self.status = 'idle'
                self.current_frame_index = 0
                
            if self.current_frame_index==4 or self.current_frame_index==8  or self.current_frame_index==13 :
                if self.Look=='right':
                    self.x_pos+=6
                else:
                    self.x_pos-=6
            return

        if self.status == 'walk':
            frames = self.walk_frames
        else:
            frames = self.idle_frames

        self.current_frame_index = (self.current_frame_index + 1) % len(frames)
        self.current_picture = frames[self.current_frame_index]

    def handle_input(self, keys):
            self.is_moving_horizontally = False
            if keys[pygame.K_n] and not self.attacking:
                self.attack()
            elif keys[pygame.K_m]:
                self.move_right()
            elif keys[pygame.K_b]:
                self.move_left()
            else:
                if not self.attacking:
                    self.status = 'idle'

    def move_right(self):
        if self.allow_move_right and not self.attacking:
            self.x_pos += self.horizontal_speed
            self.Look = 'right'
            self.status = 'walk'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        if self.allow_move_left and not self.attacking:
            self.x_pos -= self.horizontal_speed
            self.Look = 'left'
            self.status = 'walk'
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

    def check_attack_collision(self):
        if self.hitbox.colliderect(self.target.hitbox) and self.attack_hits < 3:
            self.target.health -= 30
            self.attack_hits += 1

    def Update(self,keys,platforms):
        self.handle_input(keys)
        self.update_animation()
        self.gravity()
        self.vertical_move()
        self.horizontal_move()
        self.platforms_collisions(platforms)
