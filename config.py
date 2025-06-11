import pygame

pygame.init()
info = pygame.display.Info()

screen_width = info.current_w
screen_height = info.current_h

jump_strenght=22
gravity_strenght=1
horizontal_speed=8

platform_height = 64
platform_width = 64
platform_color = (105, 5, 120)
FPS = 60
