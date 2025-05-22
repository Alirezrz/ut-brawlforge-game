import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from config import screen_width, screen_height
from src.engine.game import Game

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
    bullet_picture = pygame.image.load("src/assets/images/bullet.png")
    bullet_picture = pygame.transform.scale(bullet_picture, (40, 40))
    ghost = pygame.image.load("src/assets/images/ghost.png")
    ghost = pygame.transform.scale(ghost, (64, 64))
    ghost2 = pygame.image.load("src/assets/images/ghost2.png")
    ghost2 = pygame.transform.scale(ghost2, (64, 64))
    platform_tileset_picture = pygame.image.load("src/assets/images/platform.jpg")
except FileNotFoundError as e:
    print(f"Error: Could not load image: {e}")
    pygame.quit()
    exit()


game = Game(screen, hero_picture, bullet_picture, ghost, ghost2, platform_tileset_picture, background)
game.run()

pygame.quit()