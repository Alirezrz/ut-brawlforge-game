import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width
from src.engine.game import Game
from src.engine.multiplayer_game import Game_2
from src.engine.menu import Menu

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")


try:
    icon = pygame.image.load("src/assets/images/icon.jpg")
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print("Warning: Icon image not found. Continuing without icon.")

try:
    background = pygame.image.load("src/assets/images/BrawlhalaBackground.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    platform_image_path = "src/assets/images/"
    platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }
    explode_picture = pygame.image.load("src/assets/images/explode.png")
    explode_picture = pygame.transform.scale(explode_picture, (explode_side_size, explode_side_size))
   

except (FileNotFoundError, pygame.error) as e:
    print(f"Error: Could not load asset: {e}")
    pygame.quit()
    exit() 

while True:
    menu = Menu(screen, background)
    menu_action = menu.run()

    if menu_action == "start":

        game = Game_2(
          screen,  
          platform_images,
          background, explode_picture, 
        )
        result = game.run()
        if result == "menu":
            continue 
        elif result == "exit":
            pygame.quit()
            break
    elif menu_action == "settings":
        print("Settings menu not implemented yet!")
    elif menu_action == "exit":
        pygame.quit()
        break
    
    
    
    
    
    