import pygame
import os
import math


class Power_up:
    def __init__(self, x, y, type, targets=[]):
        self.base_x = x
        self.base_y = y
        self.x_pos = x
        self.y_pos = y
        self.type = type
        self.targets = targets
        
        self.float_amplitude = 5  # pixels
        self.float_speed = 0.05   # radians per update
        self.float_angle = 0      # current angle for cosine wave

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "power ups")
        self.pic = None

        if self.type == 'double jump':
            self.pic = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "double jump.png")
                ),
                (60, 60)
            )
        elif self.type == 'guard drone':
            self.pic = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "guard drone.png")
                ),
                (60, 60)
            )
        elif self.type == 'super power':
            self.pic = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "super power.png")
                ),
                (60, 60)
            )

        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.pic.get_width(), self.pic.get_height())
        self.USED = False

    def display(self, screen, offset):
        if not self.USED:
            screen.blit(self.pic, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def Update(self, screen, offset):
        if not self.USED:
            self.float_angle += self.float_speed
            target_y = self.base_y + math.cos(self.float_angle) * self.float_amplitude
            self.y_pos += (target_y - self.y_pos) * 0.05  

            self.hitbox.topleft = (self.x_pos, self.y_pos)

            for target in self.targets:
                if target.hitbox.colliderect(self.hitbox):
                    if self.type == 'double jump' and not target.DOUBLE_JUMP_FLAG:
                        target.DOUBLE_JUMP_FLAG = True
                        self.USED = True
                    elif self.type == 'super power' and not target.SUPER_POWER_FLAG:
                        target.SUPER_POWER_FLAG = True
                        self.USED = True
                    elif self.type == 'guard drone' and not target.GUARD_DRONE_FLAG:
                        target.GUARD_DRONE_FLAG = True
                        self.USED = True

        self.display(screen, offset)