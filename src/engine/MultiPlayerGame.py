# === MAIN GAME FILE ===
import os
import threading
from server import multiplayer_game
from client import Client
import pygame
import time
from config import screen_width, screen_height
from src.levels import multiplayer_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies


platform_image_path = "src/assets/images/"
platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }

# Configuration
HOST_PLAYER = True  # Set to False on joining player
SERVER_IP = "0.0.0.0" if HOST_PLAYER else "192.168.1.5" #باید مقدار دهی بشه
PORT = 9191

#host
if HOST_PLAYER:
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BrawlForge Server Host")
    background = pygame.image.load("src/assets/images/city1.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    platforms=load_level_data(multiplayer_data, platform_images)

    print("Select your hero (host):")
    print("1_ ROBOMAN\n2_ Ninja\n3_ Ninjagirl\n4_ Archer")
    selected_char_host = int(input())

    selected_char_dummy = 2 if selected_char_host != 2 else 3

    server_game = multiplayer_game(screen, platforms, background, selected_char_host, selected_char_dummy)

    def server_loop():
        server_game.start()  

    threading.Thread(target=server_loop, daemon=True).start()

# Delay to allow server to boot
if HOST_PLAYER:
    time.sleep(2)


client_game = Client()

# Start threads
threading.Thread(target=client_game.send_input, daemon=True).start()
threading.Thread(target=client_game.receive_state, daemon=True).start()

# Main rendering loop
clock = pygame.time.Clock()
while True:
    client_game.render_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    clock.tick(60)
