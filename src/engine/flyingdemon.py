import os
import pygame

class FlyingDemon:
    def __init__(self, x, y, target, look):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "flyinglord")

        self.fly_frames = [
            pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fly", f"{i}.png")), (w, 100))
            for i, w in enumerate([132, 97, 111, 112])
        ]

        self.x_pos = x
        self.y_pos = y
        self.target = target
        self.Look = look
        self.status = 'idle'

        self.current_frame = self.fly_frames[0]
        self.frame_index = 0
        self.animation_speed = 100
        self.last_animation_update = pygame.time.get_ticks()

        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.current_frame.get_width(), self.current_frame.get_height())

        self.following = False
        self.fly_speed = 2
        self.min_distance = 300
        self.detect_distance = 600

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.fly_frames)
            self.current_frame = self.fly_frames[self.frame_index]
            self.last_animation_update = current_time

    def display(self, screen, offset):
        self.update()
        img = self.current_frame
        if self.Look == 'left':
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def follow_target(self):
        dx = self.target.x_pos - self.x_pos
        dy = self.target.y_pos - self.y_pos
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.detect_distance:
            self.following = True
        if not self.following:
            return

        if distance > self.min_distance:
            move_x = (dx / distance) * self.fly_speed
            move_y = (dy / distance) * self.fly_speed

            self.x_pos += move_x
            self.y_pos += move_y
            self.Look = 'right' if move_x > 0 else 'left'

        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def update(self):
        self.update_animation()
        self.follow_target()
