import pygame
import os

class Terrorist:
    def __init__(self, x, y, screen_width, screen_height, Ninja, Robo, platforms, ninja):
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
        self.health = 63
        self.max_health = 100
        self.bullets = []
        self.platforms = platforms

        self.target = ninja
        self.target_status = 'free'

        self.Walk_Range = 300
        self.VisionRadious =400
        self.VisionHeight = 80
        self.walk_strength = 3
        self.walked_len = 0

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "terrorist")
        tmp = pygame.image.load(os.path.join(base_path, "walk", f"1_terrorist_1_Walk_000.png"))
        self.pic = pygame.transform.scale(tmp, (62, 118))

        self.current_picture = self.pic
        self.current_frame_index = 0
        self.animation_speed = 100
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

    def display(self, screen, offset):
        display_picture = self.current_picture
        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        else:
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def platforms_collisions(self, platforms):
        for platform in platforms:
            if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                if (self.y_pos + self.height >= platform.y_pos) and (self.y_pos + self.height < platform.y_pos + platform.height + 10):
                    self.on_ground = True
                    self.vertical_speed = 0
                    self.y_pos = platform.y_pos - self.height
                    self.current_platform = platform

    def jump_under_platform(self, platforms):
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height

    def Walk(self):
        next_x = self.x_pos + (self.walk_strength if self.Look == 'right' else -self.walk_strength)
        foot_y = self.y_pos + self.height + 5

        on_edge = True
        for platform in self.platforms:
            if platform.x_pos <= next_x <= platform.x_pos + platform.width:
                if abs(platform.y_pos - foot_y) <= 10:
                    on_edge = False
                    break

        if on_edge:
            self.walked_len = 0
            self.Look = 'left' if self.Look == 'right' else 'right'

        if self.walked_len > self.Walk_Range:
            self.walked_len = 0
            self.Look = 'left' if self.Look == 'right' else 'right'

        if self.Look == 'right':
            self.x_pos += self.walk_strength
        else:
            self.x_pos -= self.walk_strength

        self.walked_len += self.walk_strength
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def Vision(self):
        dx = abs(self.target.x_pos - self.x_pos)
        dy = abs(self.target.y_pos - self.y_pos)

        if dx <= self.VisionRadious and dy <= self.VisionHeight:
            self.target_status = 'locked'
        else:
            self.target_status = 'free'

    def Attack(self):
        if self.target_status == 'locked':
            if self.x_pos < self.target.x_pos:
                self.x_pos += self.walk_strength + 10
                self.Look = 'right'
            else:
                self.x_pos -= self.walk_strength + 10
                self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)

    def Update(self):
        self.on_ground = False
        self.Vision()

        if self.target_status == 'locked':
            self.Attack()
        else:
            self.Walk()

        self.gravity()
        self.vertical_move()