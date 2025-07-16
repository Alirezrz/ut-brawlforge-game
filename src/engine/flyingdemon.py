import os
import pygame

class FlyingDemon:
    def __init__(self,x,y,target,look):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "flyingdemon")

        self.idle_frames=[
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "idle", f"{i}.png")), (w, 100))
            for i, w in enumerate([137, 97, 113, 117])
        ]

        self.fly_frames=[
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fly", f"{i}.png")), (w, 100))
            for i, w in enumerate([132, 97, 111, 112])
        ]

        self.attack_frames=[
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "attack", f"{i}.png")), (w, 100))
            for i, w in enumerate([97,96,91,124,100,110,108,126])
        ]

        self.x_pos = x
        self.y_pos = y
        self.target = target
        self.Look = look

        self.status = 'idle'
        self.current_frame = self.idle_frames[0]
        self.frame_index = 0
        self.animation_speed = 150
        self.last_animation_update = pygame.time.get_ticks()

        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.current_frame.get_width(), self.current_frame.get_height())

        self.following = False
        self.fly_speed = 2
        self.min_distance = 500
        self.detect_distance = 600
        self.avoid_distance = 300  # if target gets closer than this, demon escapes

        self.last_attack=0
        self.reload_duration=2000
        self.attacking = False
        self.attack_frame_limit = len(self.attack_frames)

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update >= self.animation_speed:
            if self.status == 'idle':
                frames = self.idle_frames
            elif self.status == 'fly':
                frames = self.fly_frames
            elif self.status == 'attack':
                frames = self.attack_frames
            
            self.frame_index += 1

            if self.status == 'attack' and self.frame_index >= len(frames):
                self.status = 'idle'  # Reset status after attack animation
                self.attacking = False
                self.frame_index = 0
            else:
                self.frame_index = self.frame_index % len(frames)

            self.current_frame = frames[self.frame_index]
            self.last_animation_update = current_time

    def display(self, screen, offset):
        self.update()
        img = self.current_frame
        if self.Look == 'right':
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def follow_target(self):
        if self.attacking:
            return  # Skip movement while attacking

        dx = self.target.x_pos - self.x_pos
        dy = self.target.y_pos - self.y_pos
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.detect_distance:
            self.following = True
        if not self.following:
            self.status = 'idle'
            return

        if distance < self.avoid_distance:
            move_x = (-dx / distance) * self.fly_speed * 2
            self.x_pos += move_x
            self.status = 'fly'
        elif distance > self.min_distance:
            move_x = (dx / distance) * self.fly_speed * 2
            self.x_pos += move_x
            self.Look = 'right' if move_x > 0 else 'left'
            self.status = 'fly'
        else:
            self.status = 'idle'

        if abs(dy) > 1:
            direction_y = 1 if dy > 0 else -1
            self.y_pos += direction_y * min(abs(dy), self.fly_speed * 2)

        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def update(self):
        self.attack()

        if not self.attacking:
            if self.following:
                self.Look = 'right' if self.x_pos < self.target.x_pos else 'left'
            self.follow_target()

        self.update_animation()

    def attack(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack

        if (
            self.following
            and elapsed_time >= self.reload_duration
            and not self.attacking
            and abs(self.y_pos - self.target.y_pos) <= 60
            and abs(self.x_pos - self.target.x_pos) <= self.min_distance
        ):
            self.status = 'attack'
            self.attacking = True
            self.frame_index = 0
            self.last_attack = current_time
