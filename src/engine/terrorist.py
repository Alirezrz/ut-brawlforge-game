import pygame
import os
import math

class Terrorist:
    def __init__(self, x, y, screen_width, screen_height, targets, platforms, ninja, screen, scroll):
        self.x_pos = x
        self.y_pos = y
        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.width = 62
        self.height = 118
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.platforms = platforms
        self.game_screen = screen
        self.explosion_pos = 0
        self.damage_radiuos = 200
        self.targets = targets
        self.target = self.targets[0]
        self.target_status = 'free'
        self.status = 'alive'
        self.animation_status = 'walk'
        self.frame_index = 0

        self.explotion_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "terrorist", "terror exp.mp3"))

        self.Walk_Range = 300
        self.VisionRadious = 400
        self.VisionHeight = 80
        self.walk_strength = 3
        self.walked_len = 0

        self.exploding = False
        self.explosion_start_time = 0
        self.explosion_frame_duration = 40

        self.currentFrame_index = 0
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "terrorist")
        tmp = pygame.image.load(os.path.join(base_path, "walk", f"1_terrorist_1_Walk_000.png"))
        self.pic = pygame.transform.scale(tmp, (62, 118))

        self.EXP_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "ExplosionFrames", f"{i:04d}.png")), (256, 256))
            for i in range(1, 31)
        ]

        sizes = [61, 59, 56, 46, 49, 45, 43, 53]
        self.walk_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "walk", f"3_terrorist_3_Walk_00{i}.png")), (sizes[i], 118))
            for i in range(8)
        ]

        sizes = [56, 56, 68, 66, 56, 54]
        self.run_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "run", f"3_terrorist_3_Run_00{i}.png")), (sizes[i], 118))
            for i in range(6)
        ]

        sizes = [53, 52, 66, 79, 57, 52]
        self.dead_frames = []
        for i in range(9):
            path = os.path.join(base_path, "hurt", f"3_terrorist_3_Hurt_00{i}.png")
            if i == 6:
                self.dead_frames.append(pygame.transform.scale(pygame.image.load(path), (100, 67)))
            elif i == 7:
                self.dead_frames.append(pygame.transform.scale(pygame.image.load(path), (95, 90)))
            elif i == 8:
                self.dead_frames.append(pygame.transform.scale(pygame.image.load(path), (118, 46)))
            else:
                self.dead_frames.append(pygame.transform.scale(pygame.image.load(path), (sizes[i], 118)))

        self.scroll = scroll
        self.current_picture = self.pic
        self.current_frame_index = 0
        self.animation_speed = 100
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

    def display(self, screen, offset):
        if self.status == 'exploded' and self.exploding:
            frame = self.EXP_frames[self.current_frame_index]
            x = self.explosion_pos[0] - frame.get_width() // 2 - offset[0]
            y = self.explosion_pos[1] - frame.get_height() // 2 - offset[1]
            screen.blit(frame, (x, y))
        elif self.status not in ('exploded', 'removed'):
            display_picture = self.current_picture
            if self.Look == 'right':
                screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
            else:
                flipped_picture = pygame.transform.flip(display_picture, True, False)
                screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def gravity(self):
        if not self.on_ground and self.status != 'shot':
            self.vertical_speed -= self.gravity_strenght

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def platforms_collisions(self, platforms):
        self.allow_move_left = True
        self.allow_move_right = True
        self.on_ground = False
        for platform in platforms:
            horizontal_overlap = self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width
            if horizontal_overlap:
                if (self.y_pos + self.height >= platform.y_pos) and (self.y_pos + self.height < platform.y_pos + platform.height + 10) and self.vertical_speed <= 0:
                    self.on_ground = True
                    self.vertical_speed = 0
                    self.y_pos = platform.y_pos - self.height
                    self.current_platform = platform
                if (self.y_pos + self.height > platform.y_pos) and (self.y_pos < platform.y_pos + platform.height):
                    if abs(self.x_pos - (platform.x_pos + platform.width)) <= 10:
                        self.allow_move_left = False
                        self.x_pos = platform.x_pos + platform.width
                    if abs(self.x_pos + self.width - platform.x_pos) <= 10:
                        self.allow_move_right = False
                        self.x_pos = platform.x_pos - self.width

    def jump_under_platform(self, platforms):
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height

    def Walk(self):
        if self.status != 'exploded':
            direction = self.walk_strength if self.Look == 'right' else -self.walk_strength
            next_x = self.x_pos + direction
            foot_y = self.y_pos + self.height + 5
            on_edge = True
            will_hit_side = False
            for platform in self.platforms:
                if platform.x_pos <= next_x <= platform.x_pos + platform.width:
                    if abs(platform.y_pos - foot_y) <= 10:
                        on_edge = False
                if (self.y_pos + self.height > platform.y_pos) and (self.y_pos < platform.y_pos + platform.height):
                    if self.Look == 'right':
                        if abs((self.x_pos + self.width + self.walk_strength) - platform.x_pos) <= 5:
                            will_hit_side = True
                    else:
                        if abs(self.x_pos - (platform.x_pos + platform.width + self.walk_strength)) <= 5:
                            will_hit_side = True
            if on_edge or will_hit_side or self.walked_len > self.Walk_Range:
                self.walked_len = 0
                self.Look = 'left' if self.Look == 'right' else 'right'
                return
            if self.Look == 'right' and self.allow_move_right:
                self.x_pos += self.walk_strength
            elif self.Look == 'left' and self.allow_move_left:
                self.x_pos -= self.walk_strength
            self.walked_len += self.walk_strength
            self.hitbox.topleft = (self.x_pos, self.y_pos)

    def Vision(self):
        self.update_taregts()
        dx = abs(self.target.x_pos - self.x_pos)
        dy = abs(self.target.y_pos - self.y_pos)
        if dx < 20 and dy < 80:
            self.trigger_explosion()
            return
        if dx <= self.VisionRadious and dy <= self.VisionHeight:
            self.target_status = 'locked'
        else:
            self.target_status = 'free'
            self.animation_status = 'walk'

    def Attack(self):
        if self.target_status == 'locked':
            self.animation_status = 'run'
            if self.x_pos < self.target.x_pos and self.allow_move_right:
                self.x_pos += self.walk_strength + 5
                self.Look = 'right'
            elif self.allow_move_left:
                self.x_pos -= self.walk_strength + 5
                self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)

    def Update(self, bullets):
        if self.status == 'exploded':
            if not self.exploding:
                self.exploding = True
                self.explosion_start_time = pygame.time.get_ticks()
                for target in self.targets:
                    dx = abs(self.target.x_pos - self.x_pos)
                    dy = abs(self.target.y_pos - self.y_pos)
                    if dx<self.damage_radiuos and dy<self.damage_radiuos:
                        target.health -= 30
                        print(target.health)
                self.current_frame_index = 0
                self.explosion_pos = (self.x_pos, self.y_pos + 50)
            else:
                elapsed = pygame.time.get_ticks() - self.explosion_start_time
                frame_index = elapsed // self.explosion_frame_duration
                if frame_index < len(self.EXP_frames):
                    self.current_frame_index = frame_index
                else:
                    self.status = 'removed'
            return

        if self.status == 'alive':
            for bullet in bullets:
                if bullet.hitbox.colliderect(self.hitbox):
                    bullets.remove(bullet)
                    self.health -= 30
                    if self.health <= 0:
                        self.trigger_explosion()
                    break

        self.Vision()
        if self.status == 'alive':
            if self.target_status == 'locked':
                self.Attack()
            else:
                self.Walk()
            self.gravity()
            self.vertical_move()

        self.update_animation()

    def trigger_explosion(self):
        self.status = 'exploded'
        self.explosion_pos = (self.x_pos, self.y_pos + 50)

    def start_explosion(self):
        self.exploding = True
        self.explosion_start_time = pygame.time.get_ticks()
        for target in self.targets:
            dx = abs(self.x_pos - target.x_pos)
            dy = abs(self.y_pos - target.y_pos)
            if dx < self.damage_radiuos and dy < self.damage_radiuos:
                target.health -= 30
                print(target.health)
        self.current_frame_index = 0

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.status == 'shot':
            if current_time - self.last_frame_update_time >= self.animation_speed:
                self.last_frame_update_time = current_time
                self.frame_index += 1
                if self.frame_index == 6:
                    self.y_pos += 51
                elif self.frame_index == 7:
                    self.y_pos += 80
                elif self.frame_index == 8:
                    self.y_pos += 95
                if self.frame_index >= len(self.dead_frames):
                    self.status = 'removed'
                else:
                    self.current_picture = self.dead_frames[self.frame_index]
        elif current_time - self.last_frame_update_time >= self.animation_speed:
            self.last_frame_update_time = current_time
            if self.animation_status == 'walk':
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.current_picture = self.walk_frames[self.frame_index]
            elif self.animation_status == 'run':
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)
                self.current_picture = self.run_frames[self.frame_index]

    def update_taregts(self):
        print(self.health)
        if self.target_status == 'locked':
            return
        dist = [math.sqrt((self.x_pos - t.x_pos)**2 + (self.y_pos - t.y_pos)**2) for t in self.targets]
        min_index = dist.index(min(dist))
        self.target = self.targets[min_index]
