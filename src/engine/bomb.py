import pygame 
import os

import math


class Bomb:
    def __init__(self, x, y, targets, timer_seconds=30):
        self.x_pos = x
        self.y_pos = y
        self.targets = targets
        self.width = 100
        self.height = 126
        self.bomb_on = pygame.image.load("src/assets/images/bomb/bomb on.png")
        self.bomb_on = pygame.transform.scale(self.bomb_on, (self.width, self.height))
        self.bomb_off = pygame.image.load("src/assets/images/bomb/bomb off.png")
        self.bomb_off = pygame.transform.scale(self.bomb_off, (self.width, self.height))
        self.display_pic = self.bomb_on
        self.time=timer_seconds
        self.timer = timer_seconds
        self.is_defused = False
        self.font = pygame.font.SysFont("Arial", 36)
        self.timer_finished = False
        self.start_time=pygame.time.get_ticks()
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)        


    def display(self, screen,offset):
        screen.blit(self.display_pic, (self.x_pos-offset[0], self.y_pos-offset[1]))
        timer_text = self.font.render(f"Timer: {int(self.timer)}", True, (255, 0, 0))
        screen.blit(timer_text, (screen.get_width() // 2 - 80, 20))
        self.Update(screen,offset)

    def Update(self,screen,scroll):
        current_time=pygame.time.get_ticks()

        if self.timer > 0 and not self.is_defused:
            self.timer=self.time-((current_time-self.start_time)/1000)
            if self.timer <= 0:
                self.timer = 0
                self.timer_finished = True
                print("lose")
        elif self.is_defused and not self.timer_finished:
            self.timer_finished = True
            print("win")

    def bomb_defused(self):
        self.display_pic = self.bomb_off
        self.is_defused = True

    def defuse_bomb(self):
        for target in self.targets:
            if target.hitbox.colliderect(self.hitbox):
                if target.has_defuse_kit:
                    self.bomb_defused() 

    def handle_input(self,keys):
        if keys[pygame.K_z]:
            self.defuse_bomb()                
