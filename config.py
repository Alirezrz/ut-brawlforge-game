import pygame

pygame.init()
info = pygame.display.Info()

screen_width = info.current_w
screen_height = info.current_h

profileSideSize=100
jump_strenght=22
gravity_strenght=1
horizontal_speed=8
health_bar_lenght=276
roboman_health_bar_frame_thickness=24
roboman_reload_time=400
roboman_jetpack_reload=3000 

platform_height = 64
platform_width = 64
platform_color = (105, 5, 120)
FPS = 60

explode_side_size=50

enenmy_health_bar_width=40
enenmy_health_bar_height=5

ROBOMAN_LANDING_INSET = 20
ROBOMAN_SIDE_COLLISION_TOP_BUFFER = 40
ROBOMAN_SIDE_COLLISION_BOTTOM_BUFFER = 10



Ninja_width=62
Ninja_height=118