import pygame
import os
from config import screen_width, screen_height
import math


class Guard_Drone:
    def __init__(self, player, owner="unknown"):
        self.player = player
        self.x_pos = -(screen_width)
        self.y_pos = -(screen_height)
        self.status = 'idle'
        self.owner = owner
        self.bullets = []
        self.reload_duration = 1000
        self.last_shot = 0

        self.shoot_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "protect drone", "protect drone shot.mp3"))
        self.shot_hit_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "protect drone", "protect drone shot hit.mp3"))

        self.tracked_targets = []
        self.smokes = []

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Guard Drone")

        self.idle_frames = [pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, 'idle', f"{i}.png")), (50, 35)) for i in range(8)]

        self.walk_frames = [pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, 'walk', f"{i}.png")), (50, 35)) for i in range(8)]

        self.display_frame = self.idle_frames[0]
        self.last_animation_update = 0
        self.animation_speed = 25
        self.frame_index = 0

    def display(self, screen, offset):
        screen.blit(self.display_frame, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update > self.animation_speed:
            if self.status == 'idle':
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.display_frame = self.idle_frames[self.frame_index]
            elif self.status == 'forward':
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.display_frame = self.walk_frames[self.frame_index]
            elif self.status == 'backward':
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.display_frame = pygame.transform.flip(self.walk_frames[self.frame_index], True, False)

            self.last_animation_update = current_time

    def Update(self, screen, offset, shot_bullets):
        self.Vision(shot_bullets)
        self.update_pos()
        self.update_animation()
        self.display(screen, offset)

        for b in self.bullets[:]:
            b.update()
            b.display(screen, offset)
            if b.is_off_screen():
                self.bullets.remove(b)

        for smoke in self.smokes[:]:
            smoke.update()
            smoke.display(screen, offset)
            if smoke.status == 'dead':
                self.smokes.remove(smoke)

    def update_pos(self):
        if self.status == 'departing':
            self.x_pos += 10  
            self.y_pos -= 5  
            return  
        if self.player.x_pos > self.x_pos + 40:
            self.x_pos += self.player.horizontal_speed - 1
            self.status = 'forward'
        elif self.x_pos > self.player.x_pos + 40:
            self.x_pos -= self.player.horizontal_speed - 1
            self.status = 'backward'
        else:
            self.status = 'idle'

        target_y = self.player.y_pos - 40
        if abs(self.y_pos - target_y) > 2:
            if self.y_pos < target_y:
                self.y_pos += min(5, target_y - self.y_pos)
            elif self.y_pos > target_y:
                self.y_pos -= min(5, self.y_pos - target_y)

    def Vision(self, shot_bullets):
        for bullet in shot_bullets:
            d = math.sqrt((self.player.x_pos - bullet.x_pos) ** 2 + (self.player.y_pos - bullet.y_pos) ** 2)
            if d < 400 and bullet.owner != self.owner and bullet not in self.tracked_targets:
                self.shoot(bullet)
                self.tracked_targets.append(bullet)

        for laser in self.bullets[:]:
            for bullet in shot_bullets[:]:
                if laser.hitbox.colliderect(bullet.hitbox) and bullet.owner != self.owner:
                    self.shot_hit_sound.play()
                    collision_x = (laser.x_pos + bullet.x_pos) // 2
                    collision_y = (laser.y_pos + bullet.y_pos) // 2
                    self.smokes.append(Smoke(collision_x, collision_y))
                    bullet.status='removed'
                    shot_bullets.remove(bullet)
                    self.bullets.remove(laser)
                    if bullet in self.tracked_targets:
                        self.tracked_targets.remove(bullet)

    def shoot(self, target):
        self.bullets.append(laser(self.x_pos, self.y_pos + 30, target))
        self.shoot_sound.play()
        
        
    def is_off_screen_exit(self):
        return self.x_pos > screen_width or self.y_pos + 40 < 0


class laser:
    def __init__(self, x, y, target):
        self.x_pos = x
        self.y_pos = y
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, 10, 10)
        self.target = target
        self.speed = 17
        self.travel_distance = 0
        self.max_distance = 800  # Distance after which the laser is removed

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Guard Drone", "fire.png")
        self.image = pygame.transform.scale(pygame.image.load(path), (10, 10))

    def display(self, screen, offset):
        screen.blit(self.image, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update(self):
        dx = self.target.x_pos - self.x_pos
        dy = self.target.y_pos - self.y_pos
        distance = math.hypot(dx, dy)
        if distance != 0:
            move_x = self.speed * dx / distance
            move_y = self.speed * dy / distance
            self.x_pos += move_x
            self.y_pos += move_y
            self.travel_distance += math.hypot(move_x, move_y)
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def is_off_screen(self):
        return self.travel_distance > self.max_distance


class Smoke:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y

        self.frames = []
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Guard Drone", "smoke")

        for i in range(5):
            self.frames.append(pygame.transform.scale((pygame.image.load(os.path.join(path, f"{i}.png"))),(50,50)))

        self.frame_inx = 0
        self.last_updt = 0
        self.speed = 100
        self.status = 'alive'
        self.frame = self.frames[0]

    def display(self, screen, offset):
        screen.blit(self.frame, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_updt
        if elapsed_time >= self.speed:
            self.frame_inx += 1
            if self.frame_inx < len(self.frames):
                self.frame = self.frames[self.frame_inx]
            else:
                self.status = 'dead'
            self.last_updt = current_time
            
            

