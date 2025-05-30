import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from config import screen_width, screen_height # type: ignore
from src.engine.game import Game # type: ignore
from src.engine.menu import Menu # type: ignore
pygame.init()

# Screen 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")
try:
    icon = pygame.image.load("src/assets/images/icon.jpg")
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print("Warning: Icon image not found. Continuing without icon.")
try:
    background = pygame.image.load("src/assets/images/BrawlhalaBackground.jpg")
    hero_picture = pygame.image.load("src/assets/images/hero.png")
    hero_picture = pygame.transform.scale(hero_picture,(70,118))
    hero_run_frames=[]
    for i in range (1,9):
        tmp=pygame.image.load(f"src/assets/images/hero_run_frames/Run ({i}).png")
        if(i==1):
            hero_run_frames.append(pygame.transform.scale(tmp,(63,118)))
        if(i==2):
            hero_run_frames.append(pygame.transform.scale(tmp,(62,118)))
        if(i==3):
            hero_run_frames.append(pygame.transform.scale(tmp,(82,118)))
        if(i==4):
            hero_run_frames.append(pygame.transform.scale(tmp,(77,118)))
        if(i==5):
            hero_run_frames.append(pygame.transform.scale(tmp,(73,118)))
        if(i==6):
            hero_run_frames.append(pygame.transform.scale(tmp,(80,118)))            
        if(i==7):
            hero_run_frames.append(pygame.transform.scale(tmp,(92,118)))
        if(i==8):
            hero_run_frames.append(pygame.transform.scale(tmp,(79,118)))
        if(i==9):
            hero_run_frames.append(pygame.transform.scale(tmp,(82,118)))
        
    hero_profile_picture = pygame.image.load("src/assets/images/hero_profile.png")
    bullet_picture = pygame.image.load("src/assets/images/bullet.png")
    bullet_picture = pygame.transform.scale(bullet_picture, (40, 40))
    ghost = pygame.image.load("src/assets/images/ghost.png")
    ghost = pygame.transform.scale(ghost, (64, 64))
    ghost2 = pygame.image.load("src/assets/images/ghost2.png")
    ghost2 = pygame.transform.scale(ghost2, (64, 64))
    platform_tileset_picture = pygame.image.load("src/assets/images/platform.jpg")
    explode_picture = pygame.image.load("src/assets/images/explode.png")
    explode_picture = pygame.transform.scale(explode_picture, (50, 50))
    health_bar_green= pygame.image.load("src/assets/images/green_image.jpg")
    health_bar_green= pygame.transform.scale(health_bar_green, (40, 5))
    health_bar_red=pygame.image.load("src/assets/images/red_image.jpg")
    health_bar_red=pygame.transform.scale(health_bar_red, (40, 5))
except FileNotFoundError as e:
    print(f"Error: Could not load image: {e}")
    pygame.quit()
    exit()

menu = Menu(screen,background)
menu_action = menu.run()
if menu_action == "start":
    game = Game(screen, hero_picture, bullet_picture, ghost, ghost2, platform_tileset_picture, background,explode_picture,health_bar_green,health_bar_red,hero_profile_picture,hero_run_frames)
    game.run()
elif menu_action == "settings":
    print("Settings menu not implemented yet!")
elif menu_action == "exit":
    pygame.quit()
    exit()
pygame.quit()