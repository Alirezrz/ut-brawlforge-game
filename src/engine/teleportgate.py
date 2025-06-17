import pygame
import os

class Gates:
    def __init__(self, x1, y1, x2, y2, ninja):
        self.A_x = x1
        self.A_y = y1
        self.B_x = x2
        self.B_y = y2

        self.ninja = ninja

        self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Gate")
        self.DoorOpen_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "DoorOpen.png")), (91, 150))
        self.DoorClose_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "DoorLocked.png")), (91, 150))
        self.GreenFalg_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "Switch (1).png")), (21, 75))
        self.RedFalg_pic = pygame.transform.scale(pygame.image.load(os.path.join(self.base_path, "Switch (2).png")), (21, 75))

        self.open_a = False
        self.open_b = False
        self.last_teleport_time = 0
        self.cooldown = 10000  
        self.teleport_display_time = 400  # how long doors stay open after teleport

    def display(self, screen, offset):
        current_time = pygame.time.get_ticks()
        in_cooldown = current_time - self.last_teleport_time < self.cooldown
        flag_pic = self.RedFalg_pic if in_cooldown else self.GreenFalg_pic

        a_pic = self.DoorOpen_pic if self.open_a else self.DoorClose_pic
        b_pic = self.DoorOpen_pic if self.open_b else self.DoorClose_pic

        screen.blit(a_pic, (self.A_x - offset[0], self.A_y - offset[1]))
        screen.blit(b_pic, (self.B_x - offset[0], self.B_y - offset[1]))

        screen.blit(flag_pic, (self.A_x - 30 - offset[0], self.A_y + 75 - offset[1]))
        screen.blit(flag_pic, (self.B_x - 30  - offset[0], self.B_y + 75 - offset[1]))

        
        if in_cooldown and current_time - self.last_teleport_time > self.teleport_display_time:
            self.open_a = False
            self.open_b = False

    def recieve_request(self, target):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_teleport_time < self.cooldown:
            return

        near_a = abs(self.A_x - target.x_pos) < 50 and abs(self.A_y - target.y_pos) < 50
        near_b = abs(self.B_x - target.x_pos) < 50 and abs(self.B_y - target.y_pos) < 50

        if near_a:
            target.x_pos = self.B_x
            target.y_pos = self.B_y + 57
            self.open_a = True
            self.open_b = True
            self.last_teleport_time = current_time

        elif near_b:
            target.x_pos = self.A_x
            target.y_pos = self.A_y + 57
            self.open_a = True
            self.open_b = True
            self.last_teleport_time = current_time
