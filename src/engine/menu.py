import pygame
import os
import math
import time
import json
import socket
import sys
import subprocess
class Menu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 74)  
        self.small_font = pygame.font.Font(None, 50)
        self.running = True
        try:
            logo_path = os.path.join("src", "assets", "images", "ut-brawlforge-icon.png") 
            self.logo = pygame.image.load(logo_path).convert_alpha()
            self.logo = pygame.transform.scale(self.logo, (400, 400))
        except pygame.error as e:
            print(f"Error loading logo: {e}")
            self.logo = None
        self.logo_base_y = screen.get_height() // 2 - 100
        if self.logo:
            self.logo_rect = self.logo.get_rect(center=(screen.get_width() // 2, self.logo_base_y))
        self.float_angle = 0
        self.float_speed = 0.03
        self.float_amplitude = 15
        logo_bottom = self.logo_base_y+200
        self.buttons = [
           {"text": "Start Game", "pos": (screen.get_width() // 2, logo_bottom + 80), "action": "start"},
           {"text": "Exit", "pos": (screen.get_width() // 2, logo_bottom + 150), "action": "exit"}
        ]
        self.button_color = (255,255,255)  
        self.button_hover_color = (255,165,0) 
        self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
    def draw_text(self, text, font, color, pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def run(self):
        while self.running:
            self.screen.blit(self.background,(0,0))
            if self.logo:
                self.float_angle +=self.float_speed
                offset_y = math.sin(self.float_angle) * self.float_amplitude
                self.logo_rect.centery = self.logo_base_y + int(offset_y)
                self.screen.blit(self.logo, self.logo_rect)
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                color = self.button_hover_color if self.is_hovered(button["pos"], mouse_pos) else self.button_color
                button_rect = self.draw_text(button["text"], self.small_font, color, button["pos"])
                button["rect"] = button_rect
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.get("rect") and self.is_hovered(button["pos"], mouse_pos):
                            if self.click_sound:
                                self.click_sound.play()
                                if button["action"] == "exit":
                                    print("Playing sound for Exit in Main Menu")
                                    time.sleep(0.1)  
                            return button["action"]

            pygame.display.update()

    def is_hovered(self,button_pos,mouse_pos):
        button_rect = pygame.Rect(0,0,200,50)
        button_rect.center = button_pos
        return button_rect.collidepoint(mouse_pos)
class PauseMenu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background  
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 45)
        self.buttons = [
            {"text": "Resume", "pos": (screen.get_width() // 2, 250), "action": "resume"},
            {"text": "Return to Menu", "pos": (screen.get_width() // 2, 350), "action": "menu"},
            {"text": "Exit", "pos": (screen.get_width() // 2, 450), "action": "exit"}
        ]
        self.button_color = (255, 255, 255)
        self.button_hover_color = (100, 200, 255)
        self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
    def draw_text(self, text, font, color, pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def run(self):
        paused = True
        while paused:
            self.screen.blit(self.background, (0, 0))
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128)) 
            self.screen.blit(overlay, (0, 0))
            
            self.draw_text("Paused", self.font, (255, 255, 255), (self.screen.get_width() // 2, 150))
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                color = self.button_hover_color if self.is_hovered(button["pos"], mouse_pos) else self.button_color
                button_rect = self.draw_text(button["text"], self.small_font, color, button["pos"])
                button["rect"] = button_rect

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
                    return "resume"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.get("rect") and self.is_hovered(button["pos"], mouse_pos):
                            if self.click_sound:
                                self.click_sound.play()
                                if button["action"] == "exit":
                                    print("Playing sound for Exit in Pause Menu")
                                    time.sleep(0.1)  
                            return button["action"]

            pygame.display.update()

    def is_hovered(self, button_pos, mouse_pos):
        button_rect = pygame.Rect(0, 0, 250, 50)
        button_rect.center = button_pos
        return button_rect.collidepoint(mouse_pos)
class GameModeMenu:
    def __init__(self,screen,background):
        self.screen = screen 
        self.background = background
        self.font = pygame.font.SysFont(None,50)
        self.status_message = ""
        button_y_start = screen.get_height() // 2 - 100
        self.single_button_rect = pygame.Rect(0, 0, 300, 50)
        self.single_button_rect.center = (screen.get_width() // 2, button_y_start)
        self.multi_button_rect = pygame.Rect(0, 0, 300, 50)
        self.multi_button_rect.center = (screen.get_width() // 2, button_y_start + 70)
        self.host_button_rect = pygame.Rect(0, 0, 300, 50)
        self.online_button_rect = pygame.Rect(0, 0, 300, 50)
        self.online_button_rect.center = (screen.get_width() // 2, button_y_start + 140)
        self.host_button_rect.center = (screen.get_width() // 2, button_y_start + 210)
        self.exit_button_rect = pygame.Rect(0, 0, 300, 50)
        self.exit_button_rect.center = (screen.get_width() // 2, button_y_start + 280)
        try:
           self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except FileNotFoundError:
           self.click_sound = None

    def draw_button(self, text, center_y, hover):
        color = (255, 255, 255) if not hover else (255, 165, 0)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, center_y))
        self.screen.blit(text_surface, text_rect)
        return text_rect
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            
            self.draw_button("Single Player", self.single_button_rect, self.single_button_rect.collidepoint(mouse_pos))
            self.draw_button("Multi Player", self.multi_button_rect, self.multi_button_rect.collidepoint(mouse_pos))
            self.draw_button("Host Server", self.host_button_rect, self.host_button_rect.collidepoint(mouse_pos))
            self.draw_button("Connect to Online Server", self.online_button_rect, self.online_button_rect.collidepoint(mouse_pos))
            self.draw_button("Back to Main Menu", self.exit_button_rect, self.exit_button_rect.collidepoint(mouse_pos))
            if self.status_message:
                self.draw_text(self.status_message, pygame.font.SysFont(None, 35), (200, 255, 200), (self.screen.get_width() // 2, self.host_button_rect.bottom + 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.single_button_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "single"
                    if self.multi_button_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "multi"
                    if self.online_button_rect.collidepoint(event.pos):
                          if self.click_sound:
                            self.click_sound.play()
                            return "online"
                    if self.exit_button_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "exit"
                    if self.host_button_rect.collidepoint(event.pos):
                        if self.click_sound: 
                            self.click_sound.play()
                        try:
                            python_executable = sys.executable
                            subprocess.Popen([python_executable, "server.py"])
                            # self.status_message = "Server started successfully in background!"
                        except Exception as e:
                            self.status_message = f"Error: Could not start server. {e}"            
            pygame.display.flip()
        
        return "exit"
    def draw_button(self, text, rect, hover):
      color = (255, 165, 0) if hover else (255, 255, 255)
      text_surface = self.font.render(text, True, color)
      text_rect = text_surface.get_rect(center=rect.center)
      self.screen.blit(text_surface, text_rect)

    def draw_text(self, text, font, color, pos):
      text_surface = font.render(text, True, color)
      text_rect = text_surface.get_rect(center=pos)
      self.screen.blit(text_surface, text_rect)



class MapCharacterMenu:
    def __init__(self, screen, background, hero_profile_picture):
        self.screen = screen
        self.background = background
        self.hero_profile_picture = hero_profile_picture
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 60)
        self.characters = ["Roboman", "Ninja", "NinjaGirl", "Archer"]
        self.maps = ["level1", "level2", "level3", "Boss fight"]
        self.selected_character =None
        self.selected_map = None
        self.char_button_width = 150
        self.char_button_height = 50
        self.map_button_width = 100
        self.map_button_height = 100
        self.button_spacing = 60
        total_char_width = len(self.characters) * self.char_button_width + (len(self.characters) - 1) * self.button_spacing
        start_x = (screen.get_width() - total_char_width) // 2
        self.char_buttons = [
            {
                "text": char, 
                "pos": (start_x + i * (self.char_button_width + self.button_spacing), 330), 
                "size": (self.char_button_width, self.char_button_height),
                "preview_pos": (start_x + i * (self.char_button_width + self.button_spacing) + self.char_button_width // 2 - 60, 200)
            } for i, char in enumerate(self.characters)
        ]
        total_map_width = len(self.maps) * self.map_button_width + (len(self.maps) - 1) * self.button_spacing
        start_x = (screen.get_width() - total_map_width) // 2
        self.map_buttons = [
            {
                "text": map_name, 
                "pos": (start_x + i * (self.map_button_width + self.button_spacing), screen.get_height() - 400), 
                "size": (self.map_button_width, self.map_button_height),
                "preview_image": self.load_map_preview(map_name)
            } for i, map_name in enumerate(self.maps)
        ]
        self.confirm_button = {"text": "Confirm", "pos": (screen.get_width() - 200, screen.get_height() - 100), "size": (150, 50)}
        self.exit_button = {"text": "Exit", "pos": (50, screen.get_height() - 100), "size": (150, 50)}
        self.hovered_button = None
        self.char_previews = {
            "Roboman": pygame.image.load("src/assets/images/RoboMan_pictures/intro.png").convert_alpha(),
            "Ninja": pygame.image.load("src/assets/images/Ninja/intro.png").convert_alpha(),
            "NinjaGirl": pygame.image.load("src/assets/images/NinjaGirl/intro.png").convert_alpha(),
            "Archer": pygame.image.load("src/assets/images/Archer/intro.png").convert_alpha()
        }
        self.sounds ={
            "click": pygame.mixer.Sound("src/assets/sounds/menu/click.wav"),
            "confirm": pygame.mixer.Sound("src/assets/sounds/menu/confirm.mp3"),
            "exit": pygame.mixer.Sound("src/assets/sounds/menu/confirm.mp3")
        }
        for sound in self.sounds.values():
            sound.set_volume(0.5)
    def load_map_preview(self, map_name):
        try:
            img_path = os.path.join("src", "assets", "images", "levels", f"{map_name}_preview.png")
            img = pygame.image.load(img_path)
            return pygame.transform.scale(img, (self.map_button_width, self.map_button_height))
        except FileNotFoundError:
            print(f"Warning: Preview image for {map_name} not found at {img_path}")
            surface = pygame.Surface((self.map_button_width, self.map_button_height))
            surface.fill((50, 50, 50))
            return surface

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_text = self.title_font.render("Choose Your Character and Map", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.char_buttons:
            is_hovered = pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos)
            color = (0, 255, 0) if button["text"] == self.selected_character else (150, 150, 150) if is_hovered else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (*button["pos"], *button["size"]), border_radius=10)
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(button["pos"][0] + button["size"][0] // 2, button["pos"][1] + button["size"][1] // 2))
            self.screen.blit(text, text_rect)
            preview_img = pygame.transform.scale(self.char_previews[button["text"]], (120, 120))
            self.screen.blit(preview_img, button["preview_pos"])

        
        for button in self.map_buttons:
            is_hovered = pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos)
            color = (0, 255, 0) if button["text"] == self.selected_map else (150, 150, 150) if is_hovered else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (*button["pos"], *button["size"]), border_radius=10)
            self.screen.blit(button["preview_image"], button["pos"])
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(button["pos"][0] + button["size"][0] // 2, button["pos"][1] + button["size"][1] + 20))
            self.screen.blit(text, text_rect)

        confirm_enabled = self.selected_character is not None and self.selected_map is not None
        confirm_color = (0, 200, 0) if confirm_enabled else (50, 50, 50)
        confirm_hovered = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"]).collidepoint(mouse_pos)
        if confirm_enabled and confirm_hovered:
            confirm_color = (0,255 ,0)

        pygame.draw.rect(self.screen, confirm_color, (*self.confirm_button["pos"], *self.confirm_button["size"]), border_radius=10)
        confirm_text = self.font.render(self.confirm_button["text"], True, (255, 255, 255))
        confirm_text_rect = confirm_text.get_rect(center=(self.confirm_button["pos"][0] + self.confirm_button["size"][0] // 2, self.confirm_button["pos"][1] + self.confirm_button["size"][1] // 2))
        self.screen.blit(confirm_text, confirm_text_rect)

        exit_hovered = pygame.Rect(self.exit_button["pos"], self.exit_button["size"]).collidepoint(mouse_pos)
        exit_color = (150,150, 150) if exit_hovered else (100,100,100)
        pygame.draw.rect(self.screen, exit_color, (*self.exit_button["pos"], *self.exit_button["size"]), border_radius=10)
        exit_text = self.font.render(self.exit_button["text"], True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=(self.exit_button["pos"][0] + self.exit_button["size"][0] // 2, self.exit_button["pos"][1] + self.exit_button["size"][1] // 2))
        self.screen.blit(exit_text, exit_text_rect)

        selected_info_text = "Selected: "
        if self.selected_character:
            selected_info_text += f"Character: {self.selected_character}"
        if self.selected_map:
            selected_info_text += f", Map: {self.selected_map}"
        selected_text_surface = self.font.render(selected_info_text, True, (255, 255, 255))
        selected_rect = selected_text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 150))
        self.screen.blit(selected_text_surface, selected_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit",None,None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos 
                    for button in self.char_buttons:
                        button_rect = pygame.Rect(button["pos"], button["size"])
                        if button_rect.collidepoint(mouse_pos):
                            self.sounds["click"].play()
                            self.selected_character = button["text"] 
                            print(f"Selected character: {self.selected_character}")
                    for button in self.map_buttons:
                        button_rect = pygame.Rect(button["pos"], button["size"])
                        if button_rect.collidepoint(mouse_pos):
                            self.selected_map = button["text"]
                            print(f"Selected map: {self.selected_map}")
                            self.sounds["click"].play()
                    confirm_rect = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"])
                    if confirm_rect.collidepoint(mouse_pos) and self.selected_character and self.selected_map:
                        print(f"Confirmed: {self.selected_character}, {self.selected_map}")
                        self.sounds["confirm"].play()
                        return self.selected_character, self.selected_map, "single"
                    exit_rect = pygame.Rect(self.exit_button["pos"], self.exit_button["size"])
                    if exit_rect.collidepoint(mouse_pos):
                        self.sounds["exit"].play()
                        return "exit",None,None
            self.draw()
            pygame.display.flip()

class MultiplayerMapCharacterMenu:
    def __init__(self, screen, background, hero_profile_picture):
        self.screen = screen
        self.background = background
        self.hero_profile_picture = hero_profile_picture 
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 60)
        self.characters = ["Roboman", "Ninja", "NinjaGirl", "Archer"]
        self.maps = ["multiplayer_arena 1", "multiplayer_arena 2"] 
        self.selected_characters  = []
        self.selected_map = None
        self.char_button_width = 150
        self.char_button_height = 50
        self.map_button_width = 100
        self.map_button_height = 100
        self.button_spacing = 115

        total_char_width = len(self.characters) * self.char_button_width + (len(self.characters) - 1) * self.button_spacing
        start_x_char = (screen.get_width() - total_char_width) // 2
        self.char_buttons = [
            {
                "text": char,
                "pos": (start_x_char + i * (self.char_button_width + self.button_spacing), 330),
                "size": (self.char_button_width, self.char_button_height),
                "preview_pos": (start_x_char + i * (self.char_button_width + self.button_spacing) + self.char_button_width // 2 - 60, 200)
            } for i, char in enumerate(self.characters)
        ]
        total_map_width = len(self.maps) * self.map_button_width + (len(self.maps) - 1) * self.button_spacing
        start_x_map = (screen.get_width() - total_map_width) // 2
        self.map_buttons = [
            {
                "text": map_name,
                "pos": (start_x_map + i * (self.map_button_width + self.button_spacing), screen.get_height() - 400),
                "size": (self.map_button_width, self.map_button_height),
                "preview_image": self.load_map_preview(map_name)
            } for i, map_name in enumerate(self.maps)
        ]
        
        self.confirm_button = {"text": "Confirm", "pos": (screen.get_width() - 200, screen.get_height() - 100), "size": (150, 50)}
        self.exit_button = {"text": "Exit", "pos": (50, screen.get_height() - 100), "size": (150, 50)}
        self.char_previews = {
            "Roboman": pygame.image.load("src/assets/images/RoboMan_pictures/intro.png").convert_alpha(),
            "Ninja": pygame.image.load("src/assets/images/Ninja/intro.png").convert_alpha(),
            "NinjaGirl": pygame.image.load("src/assets/images/NinjaGirl/intro.png").convert_alpha(),
            "Archer": pygame.image.load("src/assets/images/Archer/intro.png").convert_alpha()
        }
        self.sounds ={
            "click": pygame.mixer.Sound("src/assets/sounds/menu/click.wav"),
            "confirm": pygame.mixer.Sound("src/assets/sounds/menu/confirm.mp3"),
            "exit": pygame.mixer.Sound("src/assets/sounds/menu/confirm.mp3")
        }
        for sound in self.sounds.values():
            sound.set_volume(0.5)

    def load_map_preview(self, map_name):
        try:
            img_path = os.path.join("src", "assets", "images", "levels", f"{map_name}_preview.png")
            img = pygame.image.load(img_path)
            return pygame.transform.scale(img, (self.map_button_width, self.map_button_height))
        except FileNotFoundError:
            print(f"Warning: Preview image for {map_name} not found at {img_path}")
            surface = pygame.Surface((self.map_button_width, self.map_button_height))
            surface.fill((50, 50, 50))
            return surface


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_text = self.title_font.render("Choose Two Characters and a Map", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.char_buttons:
            is_hovered = pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos)
            color = (0, 255, 0) if button["text"] in self.selected_characters else (255,165,0) if is_hovered else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (*button["pos"], *button["size"]), border_radius=10)
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(button["pos"][0] + button["size"][0] // 2, button["pos"][1] + button["size"][1] // 2))
            self.screen.blit(text, text_rect)
            preview_img = pygame.transform.scale(self.char_previews[button["text"]], (120,120))
            self.screen.blit(preview_img, button["preview_pos"])


        for button in self.map_buttons:
            is_hovered = pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos)
            color = (0, 255, 0) if button["text"] == self.selected_map else (255,165,0) if is_hovered else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (*button["pos"], *button["size"]), border_radius=10)
            self.screen.blit(button["preview_image"], button["pos"])
            text = self.font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(button["pos"][0] + button["size"][0] // 2, button["pos"][1] + button["size"][1] + 20))
            self.screen.blit(text, text_rect)
        confirm_enabled = len(self.selected_characters) == 2 and self.selected_map is not None
        confirm_color = (0, 200, 0) if confirm_enabled else (50, 50, 50)
        confirm_hovered = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"]).collidepoint(mouse_pos)
        
        if confirm_enabled and confirm_hovered:
            confirm_color = (0, 255, 0)

        pygame.draw.rect(self.screen, confirm_color, (*self.confirm_button["pos"], *self.confirm_button["size"]), border_radius=10)
        confirm_text = self.font.render(self.confirm_button["text"], True, (255, 255, 255))
        confirm_text_rect = confirm_text.get_rect(center=(self.confirm_button["pos"][0] + self.confirm_button["size"][0] // 2, self.confirm_button["pos"][1] + self.confirm_button["size"][1] // 2))
        self.screen.blit(confirm_text, confirm_text_rect)

        exit_hovered = pygame.Rect(self.exit_button["pos"], self.exit_button["size"]).collidepoint(mouse_pos)
        exit_color = (150, 150, 150) if exit_hovered else (100, 100, 100)
        pygame.draw.rect(self.screen, exit_color, (*self.exit_button["pos"], *self.exit_button["size"]), border_radius=10)
        exit_text = self.font.render(self.exit_button["text"], True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=(self.exit_button["pos"][0] + self.exit_button["size"][0] // 2, self.exit_button["pos"][1] + self.exit_button["size"][1] // 2))
        self.screen.blit(exit_text, exit_text_rect)
        selected_info_text = "Selected: "
        if self.selected_characters:
            selected_info_text += f"Players: {', '.join(self.selected_characters)}"
        if self.selected_map:
            selected_info_text += f", Map: {self.selected_map}"

        selected_text_surface = self.font.render(selected_info_text, True, (255, 255, 255))
        selected_rect = selected_text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 150))
        self.screen.blit(selected_text_surface, selected_rect)
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit", None, None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    for button in self.char_buttons:
                        button_rect = pygame.Rect(button["pos"], button["size"])
                        if button_rect.collidepoint(mouse_pos):
                            self.sounds["click"].play()
                            if button["text"] in self.selected_characters:
                                self.selected_characters.remove(button["text"]) 
                            elif len(self.selected_characters) < 2:
                                self.selected_characters.append(button["text"]) 
                            print(f"Selected characters: {self.selected_characters}")
                    
                    for button in self.map_buttons:
                        button_rect = pygame.Rect(button["pos"], button["size"])
                        if button_rect.collidepoint(mouse_pos):
                            self.selected_map = button["text"]
                            print(f"Selected map: {self.selected_map}")
                            self.sounds["click"].play()
                    
                    
                    confirm_rect = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"])
                    if confirm_rect.collidepoint(mouse_pos) and len(self.selected_characters) == 2 and self.selected_map is not None:
                        print(f"Confirmed: {self.selected_characters[0]}, {self.selected_characters[1]}, {self.selected_map}")
                        self.sounds["confirm"].play()
                        return self.selected_characters, self.selected_map, "multi" 
                    
                    
                    exit_rect = pygame.Rect(self.exit_button["pos"], self.exit_button["size"])
                    if exit_rect.collidepoint(mouse_pos):
                        self.sounds["exit"].play()
                        return "exit", None, None 
            self.draw()
            pygame.display.flip()


class GameOverMenu:
    def __init__(self, screen, background, message):
        self.screen = screen
        self.background = background
        self.message = message
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)

        self.menu_options = ["Return to Mode Selection", "Exit Game"]
        self.selected_option_index = 0

        self.return_to_menu_rect = None
        self.exit_game_rect = None

    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Draw the game over message
        message_surface = self.font.render(self.message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
        self.screen.blit(message_surface, message_rect)

        # Draw menu options
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.selected_option_index else (255, 255, 255)
            option_surface = self.small_font.render(option, True, color)
            
            if i == 0:
                self.return_to_menu_rect = option_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
                self.screen.blit(option_surface, self.return_to_menu_rect)
            elif i == 1:
                self.exit_game_rect = option_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 70))
                self.screen.blit(option_surface, self.exit_game_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option_index = (self.selected_option_index - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option_index = (self.selected_option_index + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option_index == 0:
                            return "menu" 
                        elif self.selected_option_index == 1:
                            return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_to_menu_rect and self.return_to_menu_rect.collidepoint(event.pos):
                        return "menu"
                    if self.exit_game_rect and self.exit_game_rect.collidepoint(event.pos):
                        return "exit"
                if event.type == pygame.MOUSEMOTION:
                    if self.return_to_menu_rect and self.return_to_menu_rect.collidepoint(event.pos):
                        self.selected_option_index = 0
                    elif self.exit_game_rect and self.exit_game_rect.collidepoint(event.pos):
                        self.selected_option_index = 1
                    else:
                        pass 

            self.draw()
            pygame.time.Clock().tick(30)            

class NetworkMenu:
    def __init__(self, screen, background, network_handler):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.username = ""
        self.input_box = pygame.Rect(screen.get_width() // 2 - 150, 300, 300, 50)
        self.connect_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        self.exit_button = pygame.Rect(50, screen.get_height() - 100, 150, 50)
        self.message = "Enter Your Username"
        self.message_color = (255, 255, 255)
        self.active_input = False
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active_input = not self.active_input
                    else:
                        self.active_input = False
                    
                    if self.connect_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        if self.try_connect():
                           return "connected"
                    
                    if self.exit_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "exit"

                if event.type == pygame.KEYDOWN and self.active_input:
                    if event.key == pygame.K_RETURN:
                        if self.try_connect():
                           return "connected"
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode
            
            self.draw()
            pygame.display.flip()
    def try_connect(self):
        if len(self.username) > 2:
            self.message = "Connecting..."
            self.draw() 
            pygame.display.flip()
            if self.network.connect(self.username):
                return True
            else:
                self.message = "Connection Failed. Try again."
                self.message_color = (255, 100, 100)
                return False
        else:
            self.message = "Username must be at least 3 characters."
            self.message_color = (255, 100, 100)
            return False
    def draw(self):
        self.screen.blit(self.background, (0,0))
        title_surf = self.title_font.render("Multiplayer", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width()//2, 150)))
        
        msg_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.screen.get_width()//2, 250)))
        color = (255, 165, 0) if self.active_input else (255, 255, 255)
        pygame.draw.rect(self.screen, color, self.input_box, 2)
        text_surface = self.font.render(self.username, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, (0, 150, 0), self.connect_button)
        connect_text = self.font.render("Connect", True, (255, 255, 255))
        self.screen.blit(connect_text, connect_text.get_rect(center=self.connect_button.center))
        pygame.draw.rect(self.screen, (150, 0, 0), self.exit_button)
        exit_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(exit_text, exit_text.get_rect(center=self.exit_button.center))

class MatchmakingMenu:
    def __init__(self, screen, background, network_handler):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.buttons = [
            {"text": "Create 1v1 Game", "rect": pygame.Rect(0, 0, 400, 50), "action": "create_1v1"},
            {"text": "Create 2v2 Game", "rect": pygame.Rect(0, 0, 400, 50), "action": "create_2v2"},
            {"text": "Join Game by ID", "rect": pygame.Rect(0, 0, 400, 50), "action": "join"},
            {"text": "Search Player by ID", "rect": pygame.Rect(0, 0, 400, 50), "action": "search_player"}
        ]
        for i, button in enumerate(self.buttons):
            button["rect"].center = (screen.get_width() // 2, 300 + i * 80)
        self.status_message = f"Connected as {self.network.username} (ID: {self.network.player_id})"
        self.game_request_popup = None 
        self.error_message_popup = None
        self.popup_display_start_time = 0
        self.accept_button_rect = None
        self.deny_button_rect = None
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None   
    def run(self):
        while True:
            action,data=self.check_server_messages()
            if action:
                self.network.client.setblocking(True)
                return action,data
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit", None
                if event.type == pygame.MOUSEBUTTONDOWN:
                 if self.game_request_popup:
                        self.handle_popup_click(event.pos)
                 else:
                    mouse_pos = event.pos
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if self.click_sound:
                                self.click_sound.play()
                            action = button["action"]
                            if action == "host_server":
                                try:
                                    python_executable = sys.executable
                                    subprocess.Popen([python_executable, "server.py"])
                                    self.status_message = "Server started in background!"
                                except Exception as e:
                                    self.status_message = f"Error starting server: {e}"          
                    
                            elif "create" in action:
                                game_type = "1v1" if "1v1" in action else "2v2"
                                request = {"action": "create_game", "game_type": game_type}
                                self.network.send_json(request)
                                response = self.network.recv_json()
                                if response and response.get("type") == "lobby_created":
                                    return "lobby", response
                            elif action == "join":
                                return "join_menu", None

                            elif action == "search_player":
                                return "search_player", None
            self.draw()
            self.draw_popups()
            pygame.display.flip()
    


    
    def draw(self):
        self.screen.blit(self.background, (0,0))
        title_surf = self.title_font.render("Find a Game", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width()//2, 150)))
        status_surf = self.font.render(self.status_message, True, (200, 200, 200))
        self.screen.blit(status_surf, status_surf.get_rect(center=(self.screen.get_width()//2, 220)))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
           
            color = (255, 165, 0) if button["rect"].collidepoint(mouse_pos) else (255, 255, 255)
            text_surf = self.font.render(button["text"], True, color)
            self.screen.blit(text_surf, text_surf.get_rect(center=button["rect"].center))
    def check_server_messages(self):
        try:
            self.network.client.setblocking(False)
            data = self.network.client.recv(4096).decode('utf-8')
            if not data: return "exit", None
            for message_raw in data.strip().split('\n'):
                if not message_raw: continue
                response = json.loads(message_raw)
                msg_type = response.get("type")

                if msg_type == "direct_game_request":
                    self.game_request_popup = response 
                elif msg_type == "lobby_created":
                    return "lobby", response
                elif msg_type == "error":
                    self.error_message_popup = response.get("message", "An error occurred.")
                    self.popup_display_start_time = pygame.time.get_ticks()

        except BlockingIOError:
            pass 
        except (json.JSONDecodeError, socket.error, ConnectionResetError) as e:
            print(f"Error in MatchmakingMenu: {e}")
            return "exit", None
        
        return None, None
    def draw_popups(self):
        if self.game_request_popup:
            s = pygame.Surface((600, 250), pygame.SRCALPHA)
            s.fill((0, 0, 0, 200))
            popup_rect = s.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            self.screen.blit(s, popup_rect.topleft)
            
            requester_name = self.game_request_popup['from_username']
            req_text = f"'{requester_name}' challenges you to a duel!"
            text_surf = self.font.render(req_text, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50)))
            
            self.accept_button_rect = pygame.Rect(0, 0, 150, 60)
            self.accept_button_rect.center = (popup_rect.centerx - 120, popup_rect.centery + 50)
            
            self.deny_button_rect = pygame.Rect(0, 0, 150, 60)
            self.deny_button_rect.center = (popup_rect.centerx + 120, popup_rect.centery + 50)

            pygame.draw.rect(self.screen, (0, 150, 0), self.accept_button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (150, 0, 0), self.deny_button_rect, border_radius=10)
            
            accept_text = self.font.render("Accept", True, (255,255,255))
            deny_text = self.font.render("Deny", True, (255,255,255))
            self.screen.blit(accept_text, accept_text.get_rect(center=self.accept_button_rect.center))
            self.screen.blit(deny_text, deny_text.get_rect(center=self.deny_button_rect.center))
        if self.error_message_popup:
            if pygame.time.get_ticks() - self.popup_display_start_time < 3000:
                error_font = pygame.font.Font(None, 40)
                text_surf = error_font.render(self.error_message_popup, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(self.screen.get_width() / 2, self.screen.height - 50))
                pygame.draw.rect(self.screen, (180, 0, 0, 220), text_rect.inflate(20, 10))
                self.screen.blit(text_surf, text_rect)
            else:
                self.error_message_popup = None

    def handle_popup_click(self, pos):
        if self.game_request_popup:
            decision = None
            if self.accept_button_rect and self.accept_button_rect.collidepoint(pos):
                decision = "accept"
            elif self.deny_button_rect and self.deny_button_rect.collidepoint(pos):
                decision = "deny"
            
            if decision:
                if self.click_sound: self.click_sound.play()
                
                request = {
                    "action": "respond_to_request",
                    "from_id": self.game_request_popup["from_id"],
                    "decision": decision
                }
                self.network.send_json(request)
                self.game_request_popup = None
class JoinGameMenu:
    def __init__(self, screen, background, network_handler):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.game_id = ""
        self.input_box = pygame.Rect(screen.get_width() // 2 - 150, 300, 300, 50)
        self.join_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        self.back_button = pygame.Rect(50, screen.get_height() - 100, 150, 50)
        self.message = "Enter Game ID"
        self.message_color = (255, 255, 255)
        self.active_input = True
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None      

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "back", None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.join_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        action, data = self.try_join()
                        if action: return action, data
                    if self.back_button.collidepoint(event.pos): return "back", None
                    self.active_input = self.input_box.collidepoint(event.pos)
                if event.type == pygame.KEYDOWN and self.active_input:
                    if event.key == pygame.K_RETURN:
                        action, data = self.try_join()
                        if action: return action, data
                    elif event.key == pygame.K_BACKSPACE: self.game_id = self.game_id[:-1]
                    elif event.unicode.isdigit() and len(self.game_id) < 4:
                        self.game_id += event.unicode
            self.draw()
            pygame.display.flip()

    def try_join(self):
        if self.game_id:
            request = {"action": "join_game", "game_id": self.game_id}
            self.network.send_json(request)
            return "wait_for_acceptance", None
        else:
            self.message = "Please enter a Game ID."
            self.message_color = (255, 100, 100)
            return None, None
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_surf = self.title_font.render("Join Game by ID", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 150)))
        msg_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.screen.get_width() // 2, 250)))
        color = (255, 165, 0) if self.active_input else (255, 255, 255)
        pygame.draw.rect(self.screen, color, self.input_box, 2, border_radius=5)
        text_surface = self.font.render(self.game_id, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 5))
        pygame.draw.rect(self.screen, (0, 150, 0), self.join_button, border_radius=10)
        join_text = self.font.render("Join", True, (255, 255, 255))
        self.screen.blit(join_text, join_text.get_rect(center=self.join_button.center))
        pygame.draw.rect(self.screen, (150, 0, 0), self.back_button, border_radius=10)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

class LobbyMenu:
    def __init__(self, screen, background, network_handler, lobby_data, is_host):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.game_id = lobby_data.get("game_id")
        self.players = lobby_data.get("players", [])
        self.game_type = lobby_data.get("game_type", "1v1") 
        self.is_host = is_host
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.network.client.setblocking(False)
        self.join_request_popup = None
        self.buffer = ""
        self.yes_button_rect = None
        self.no_button_rect = None
        if self.is_host:
            self.start_button = pygame.Rect(screen.get_width() - 380, screen.get_height() - 110, 350, 70)
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None   

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.disconnect()
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.join_request_popup:
                        self.handle_popup_click(event.pos)
                    if self.is_host and self.start_button.collidepoint(event.pos):
                        max_players = 2 if self.game_type == '1v1' else 4
                        if len(self.players) == max_players:
                            if self.click_sound:
                                self.click_sound.play()
                            print("[CLIENT DEBUG] 'Start Game' button clicked. Sending action to server...")
                            self.network.client.setblocking(True)
                            

                            self.network.send_json({"action": "start_game"})
                           
                            self.network.client.setblocking(False)
                            print("[CLIENT DEBUG] 'start_game' action sent.")

            result = self.check_server_messages()
            if result: 
                return result
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(15) 

    def check_server_messages(self):
        try:
            data = self.network.client.recv(4096).decode('utf-8')
            if not data:
                return "exit"
            self.buffer += data

            while '\n' in self.buffer:
                message_raw, self.buffer = self.buffer.split('\n', 1)
                if not message_raw:
                    continue
                print(f"[CLIENT DEBUG] Received raw message from server: {message_raw}")
                response = json.loads(message_raw)
                msg_type = response.get("type")

                if msg_type in ["lobby_update", "join_accepted", "lobby_created"]:
                    self.players = response.get("players", [])
                elif msg_type == "join_request" and self.is_host:
                    self.join_request_popup = {"username": response["username"], "visible": True}
                elif msg_type == "match_starting":
                    print("[CLIENT DEBUG] 'match_starting' message received! Exiting lobby...") 
                    self.network.client.setblocking(True)
                    return "start_game"
                elif msg_type == "join_denied":
                    print(f"Join denied: {response.get('message')}")
                    return "matchmaking_menu" 
                elif msg_type == "error":
                    print(f"Server Error: {response.get('message')}")
                    return "exit"
                
        except BlockingIOError: pass
        except (json.JSONDecodeError, socket.error, ConnectionResetError) as e:
            print(f"Error in lobby: {e}")
            return "exit"
        return None

    def handle_popup_click(self, pos):
        if self.yes_button_rect and self.yes_button_rect.collidepoint(pos):
            decision = "yes"
        elif self.no_button_rect and self.no_button_rect.collidepoint(pos):
            decision = "no"
        
        if decision:
            if self.click_sound:
                self.click_sound.play()
            self.network.client.setblocking(True)
            self.network.send_json({"action": "host_decision", "decision": decision})
            self.network.client.setblocking(False)
            self.join_request_popup = None

    def draw(self):
        self.screen.blit(self.background, (0,0))
        title_surf = self.title_font.render(f"Lobby - Game ID: {self.game_id}", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width()//2, 100)))

        for i, player_name in enumerate(self.players):
            player_surf = self.font.render(f"Player {i+1}: {player_name}", True, (255, 255, 255))
            player_rect = player_surf.get_rect(center=(self.screen.get_width()//2, 250 + i * 60))
            self.screen.blit(player_surf, player_rect)

        if self.is_host:
            max_players = 2 if self.game_type == '1v1' else 4
            if len(self.players) == max_players:
                color = (0, 200, 0) 
                text = "Start Game"
            else:
                color = (100, 100, 100) 
                text = f"Waiting... ({len(self.players)}/{max_players})"
            
            pygame.draw.rect(self.screen, color, self.start_button, border_radius=10)
            text_surf = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=self.start_button.center))

        if self.join_request_popup:
            self.draw_popup()

    def draw_popup(self):
        s = pygame.Surface((600, 250), pygame.SRCALPHA)
        s.fill((0,0,0, 200))
        popup_rect = s.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(s, popup_rect.topleft)
        
        req_text = f"Player '{self.join_request_popup['username']}' wants to join."
        text_surf = self.font.render(req_text, True, (255, 255, 255))
        self.screen.blit(text_surf, text_surf.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50)))
        
        self.yes_button_rect = pygame.Rect(0, 0, 120, 50)
        self.yes_button_rect.center = (popup_rect.centerx - 90, popup_rect.centery + 50)
        
        self.no_button_rect = pygame.Rect(0, 0, 120, 50)
        self.no_button_rect.center = (popup_rect.centerx + 90, popup_rect.centery + 50)
        pygame.draw.rect(self.screen, (0, 150, 0), self.yes_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (150, 0, 0), self.no_button_rect, border_radius=10)
        
        yes_text = self.font.render("Accept", True, (255,255,255))
        no_text = self.font.render("Deny", True, (255,255,255))
        self.screen.blit(yes_text, yes_text.get_rect(center=self.yes_button_rect.center))
        self.screen.blit(no_text, no_text.get_rect(center=self.no_button_rect.center))
class MultiplayerCharacterSelectMenu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)
        self.characters = ["Roboman", "Ninja", "NinjaGirl", "Archer"]
        self.selected_character = None
        self.button_width = 150
        self.button_height = 50
        self.button_spacing = 60

        total_char_width = len(self.characters) * self.button_width + (len(self.characters) - 1) * self.button_spacing
        start_x = (screen.get_width() - total_char_width) // 2
        
        self.char_buttons = [
            {
                "text": char, 
                "pos": (start_x + i * (self.button_width + self.button_spacing), 400), 
                "size": (self.button_width, self.button_height),
                "preview_pos": (start_x + i * (self.button_width + self.button_spacing) + self.button_width // 2 - 60, 250)
            } for i, char in enumerate(self.characters)
        ]
        
        self.confirm_button = {"text": "Ready!", "pos": (screen.get_width() // 2 - 75, screen.get_height() - 150), "size": (150, 50)}
        
        self.char_previews = {
            "Roboman": pygame.image.load("src/assets/images/RoboMan_pictures/intro.png").convert_alpha(),
            "Ninja": pygame.image.load("src/assets/images/Ninja/intro.png").convert_alpha(),
            "NinjaGirl": pygame.image.load("src/assets/images/NinjaGirl/intro.png").convert_alpha(),
            "Archer": pygame.image.load("src/assets/images/Archer/intro.png").convert_alpha()
        }
        self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_text = self.title_font.render("Choose Your Hero", True, (255, 255, 255))
        self.screen.blit(title_text, title_text.get_rect(center=(self.screen.get_width() // 2, 100)))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.char_buttons:
            is_hovered = pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos)
            color = (0, 255, 0) if button["text"] == self.selected_character else (150, 150, 150) if is_hovered else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (*button["pos"], *button["size"]), border_radius=10)
            text = self.font.render(button["text"], True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(button["pos"][0] + button["size"][0] // 2, button["pos"][1] + button["size"][1] // 2)))
            
            preview_img = pygame.transform.scale(self.char_previews[button["text"]], (120, 120))
            self.screen.blit(preview_img, button["preview_pos"])

        confirm_enabled = self.selected_character is not None
        confirm_color = (0, 200, 0) if confirm_enabled else (50, 50, 50)
        confirm_hovered = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"]).collidepoint(mouse_pos)
        if confirm_enabled and confirm_hovered:
            confirm_color = (0, 255, 0)

        pygame.draw.rect(self.screen, confirm_color, (*self.confirm_button["pos"], *self.confirm_button["size"]), border_radius=10)
        confirm_text = self.font.render(self.confirm_button["text"], True, (255, 255, 255))
        self.screen.blit(confirm_text, confirm_text.get_rect(center=(self.confirm_button["pos"][0] + self.confirm_button["size"][0] // 2, self.confirm_button["pos"][1] + self.confirm_button["size"][1] // 2)))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in self.char_buttons:
                        if pygame.Rect(button["pos"], button["size"]).collidepoint(mouse_pos):
                            self.click_sound.play()
                            self.selected_character = button["text"]
                    
                    confirm_rect = pygame.Rect(self.confirm_button["pos"], self.confirm_button["size"])
                    if confirm_rect.collidepoint(mouse_pos) and self.selected_character:
                        self.click_sound.play()
                        return self.selected_character

            self.draw()
            pygame.display.flip()

class SearchPlayerMenu:
    def __init__(self, screen, background, network_handler):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.player_id = ""
        self.input_box = pygame.Rect(screen.get_width() // 2 - 150, 300, 300, 50)
        self.search_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        self.back_button = pygame.Rect(50, screen.get_height() - 100, 150, 50)
        self.message = "Enter Player ID to challenge"
        self.message_color = (255, 255, 255)
        self.active_input = True
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error:
            self.click_sound = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "back", None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.search_button.collidepoint(event.pos):
                        if self.click_sound: self.click_sound.play()
                        if self.player_id:
                            request = {"action": "request_play_by_id", "target_id": self.player_id}
                            self.network.send_json(request)
                            return "waiting_for_response", None
                    if self.back_button.collidepoint(event.pos):
                        if self.click_sound: self.click_sound.play()
                        return "back", None
                    self.active_input = self.input_box.collidepoint(event.pos)

                if event.type == pygame.KEYDOWN and self.active_input:
                    if event.key == pygame.K_RETURN:
                        if self.player_id:
                            request = {"action": "request_play_by_id", "target_id": self.player_id}
                            self.network.send_json(request)
                            return "waiting_for_response", None
                    elif event.key == pygame.K_BACKSPACE: self.player_id = self.player_id[:-1]
                    elif event.unicode.isdigit() and len(self.player_id) < 4:
                        self.player_id += event.unicode
            self.draw()
            pygame.display.flip()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_surf = self.title_font.render("Search Player by ID", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 150)))
        msg_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.screen.get_width() // 2, 250)))
        color = (255, 165, 0) if self.active_input else (255, 255, 255)
        pygame.draw.rect(self.screen, color, self.input_box, 2, border_radius=5)
        text_surface = self.font.render(self.player_id, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 5))
        pygame.draw.rect(self.screen, (0, 150, 0), self.search_button, border_radius=10)
        search_text = self.font.render("Search", True, (255, 255, 255))
        self.screen.blit(search_text, search_text.get_rect(center=self.search_button.center))
        pygame.draw.rect(self.screen, (150, 0, 0), self.back_button, border_radius=10)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

class LoginSignupMenu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        self.username = ""
        self.password = ""
        self.active_field = "username" 
        self.message = "Enter your info"
        self.message_color = (255, 255, 255)
        self.username_box = pygame.Rect(screen.get_width() // 2 - 200, 250, 400, 50)
        self.password_box = pygame.Rect(screen.get_width() // 2 - 200, 320, 400, 50)
        self.login_button = pygame.Rect(screen.get_width() // 2 - 200, 400, 180, 60)
        self.signup_button = pygame.Rect(screen.get_width() // 2 + 20, 400, 180, 60)
        self.back_button = pygame.Rect(50, screen.get_height() - 100, 150, 50)
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None  
    def draw(self):
        self.screen.blit(self.background, (0, 0))
       
        title_surf = self.title_font.render("Login / Signup", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 150)))
        msg_surf = self.font.render(self.message, True, self.message_color)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.screen.get_width() // 2, 210)))
        pygame.draw.rect(self.screen, (255, 165, 0) if self.active_field == "username" else (255, 255, 255), self.username_box, 2, border_radius=5)
        username_surf = self.font.render("Username: " + self.username, True, (255, 255, 255))
        self.screen.blit(username_surf, (self.username_box.x + 10, self.username_box.y + 10))

        pygame.draw.rect(self.screen, (255, 165, 0) if self.active_field == "password" else (255, 255, 255), self.password_box, 2, border_radius=5)
        password_surf = self.font.render("Password: " + "*" * len(self.password), True, (255, 255, 255))
        self.screen.blit(password_surf, (self.password_box.x + 10, self.password_box.y + 10))

        pygame.draw.rect(self.screen, (0, 150, 0), self.login_button, border_radius=10)
        login_text = self.font.render("Login", True, (255, 255, 255))
        self.screen.blit(login_text, login_text.get_rect(center=self.login_button.center))

        pygame.draw.rect(self.screen, (0, 100, 150), self.signup_button, border_radius=10)
        signup_text = self.font.render("Signup", True, (255, 255, 255))
        self.screen.blit(signup_text, signup_text.get_rect(center=self.signup_button.center))
        pygame.draw.rect(self.screen, (150, 0, 0), self.back_button)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit", None, None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_box.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        self.active_field = "username"
                    elif self.password_box.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        self.active_field = "password"
                    else:
                        self.active_field = None

                    if self.login_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "login", self.username, self.password
                    if self.signup_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "signup", self.username, self.password
                    if self.back_button.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "back", None, None

                if event.type == pygame.KEYDOWN and self.active_field:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_field == "username":
                            self.username = self.username[:-1]
                        elif self.active_field == "password":
                            self.password = self.password[:-1]
                    elif event.key == pygame.K_TAB:
                        self.active_field = "password" if self.active_field == "username" else "username"
                    else:
                        if self.active_field == "username":
                            self.username += event.unicode
                        elif self.active_field == "password":
                            self.password += event.unicode
            
            self.draw()
            pygame.display.flip()


class OnlineActionMenu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        
        y_start = 250
        self.buttons = [
            {"text": "Create 1v1 Game", "rect": pygame.Rect(0, 0, 400, 60), "action": "create_1v1"},
            {"text": "Create 2v2 Game", "rect": pygame.Rect(0, 0, 400, 60), "action": "create_2v2"},
            {"text": "Join Game", "rect": pygame.Rect(0, 0, 400, 60), "action": "join_game"},
            {"text": "Back to Main Menu", "rect": pygame.Rect(0, 0, 400, 60), "action": "back"}
        ]
        
        for i, button in enumerate(self.buttons):
            button["rect"].center = (screen.get_width() // 2, y_start + i * 80)
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None  
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_surf = self.title_font.render("Online Lobby", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 150)))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            color = (255, 165, 0) if button["rect"].collidepoint(mouse_pos) else (255, 255, 255)
            text_surf = self.font.render(button["text"], True, color)
            self.screen.blit(text_surf, text_surf.get_rect(center=button["rect"].center))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            if self.click_sound:
                                self.click_sound.play()
                            return button["action"]
            
            self.draw()
            pygame.display.flip()


class JoinMethodMenu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 74)
        
        y_start = 300
        self.buttons = [
            {"text": "Search by ID / username ", "rect": pygame.Rect(0, 0, 500, 60), "action": "search_id"},
            {"text": "Let Server Decide", "rect": pygame.Rect(0, 0, 500, 60), "action": "server_decide"},
            {"text": "Back", "rect": pygame.Rect(0, 0, 200, 60), "action": "back"}
        ]
        
        for i, button in enumerate(self.buttons):
            button["rect"].center = (screen.get_width() // 2, y_start + i * 90)
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None  
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_surf = self.title_font.render("How to Join?", True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 180)))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            color = (255, 165, 0) if button["rect"].collidepoint(mouse_pos) else (255, 255, 255)
            text_surf = self.font.render(button["text"], True, color)
            self.screen.blit(text_surf, text_surf.get_rect(center=button["rect"].center))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            if self.click_sound:
                                self.click_sound.play()
                            return button["action"]
            
            self.draw()
            pygame.display.flip()


class TextInputMenu:
    def __init__(self, screen, background, prompt):
        self.screen = screen
        self.background = background
        self.prompt = prompt
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 60)
        self.input_text = ""
        self.input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 50)
        self.confirm_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        self.back_button = pygame.Rect(50, screen.get_height() - 100, 150, 50)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        prompt_surf = self.title_font.render(self.prompt, True, (255, 255, 255))
        self.screen.blit(prompt_surf, prompt_surf.get_rect(center=(self.screen.get_width() // 2, 220)))
        
        pygame.draw.rect(self.screen, (255, 165, 0), self.input_box, 2, border_radius=5)
        text_surface = self.font.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 5))
        
        pygame.draw.rect(self.screen, (0, 150, 0), self.confirm_button, border_radius=10)
        confirm_text = self.font.render("Confirm", True, (255, 255, 255))
        self.screen.blit(confirm_text, confirm_text.get_rect(center=self.confirm_button.center))

        pygame.draw.rect(self.screen, (150, 0, 0), self.back_button, border_radius=10)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirm_button.collidepoint(event.pos):
                        return self.input_text
                    if self.back_button.collidepoint(event.pos):
                        return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.input_text
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
            
            self.draw()
            pygame.display.flip()


class OnlineLobbyMenu:
    def __init__(self, screen, background, network_handler, lobby_data, is_host):
        self.screen = screen
        self.background = background
        self.network = network_handler
        self.game_id = lobby_data.get("game_id", "N/A")
        self.players = lobby_data.get("players", [])
        self.game_type = lobby_data.get("game_type", "1v1")
        self.is_host = is_host
        self.title_font = pygame.font.Font(None, 70)
        self.player_font = pygame.font.Font(None, 50)
        self.popup_font = pygame.font.Font(None, 40) 
        self.button_font = pygame.font.Font(None, 45) 

        self.network.client.setblocking(False)
        self.join_request_popup_text = None 
        self.yes_button_rect = None
        self.no_button_rect = None

        if self.is_host:
            self.start_button = pygame.Rect(screen.get_width() - 380, screen.get_height() - 110, 350, 70)
        try:
            self.click_sound = pygame.mixer.Sound("src/assets/sounds/menu/click.wav")
        except pygame.error as e:
            print(f"Cannot load click sound in NetworkMenu: {e}")
            self.click_sound = None   

    def run(self):
        while True:
            server_message = self.check_server_messages()
            if server_message:
                if "wants to join" in server_message and self.is_host:
                    self.join_request_popup_text = server_message
                elif "Game is starting" in server_message or "setup_complete" in server_message:
                    return "start_game"
                elif "You have been accepted" in server_message:
                    pass 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.client.close()
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.join_request_popup_text:
                        self.handle_popup_click(event.pos)
            
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(15)

    def check_server_messages(self):
        try:
            data = self.network.client.recv(4096).decode('utf-8').strip()
            if data:
                print(f"[SERVER MESSAGE RECEIVED] {data}")
                return data
        except BlockingIOError:
            pass 
        except (socket.error, ConnectionResetError):
            return "exit"
        return None

    def handle_popup_click(self, pos):
        decision = None
        if self.yes_button_rect and self.yes_button_rect.collidepoint(pos):
            decision = "yes"
        elif self.no_button_rect and self.no_button_rect.collidepoint(pos):
            decision = "no"
        
        if decision:
            if self.click_sound:
                self.click_sound.play()
            self.network.client.setblocking(True)
            self.network.client.sendall(decision.encode())
            self.network.client.setblocking(False)
            self.join_request_popup_text = None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        id_text = f"Game ID: {self.game_id}" if self.is_host else f"Lobby: {self.game_id}"
        title_surf = self.title_font.render(id_text, True, (255, 255, 255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.screen.get_width() // 2, 100)))
        for i, player_name in enumerate(self.players):
            player_surf = self.player_font.render(f"Player {i+1}: {player_name}", True, (255, 255, 255))
            self.screen.blit(player_surf, player_surf.get_rect(center=(self.screen.get_width() // 2, 250 + i * 60)))
        if self.is_host:
            pygame.draw.rect(self.screen, (100, 100, 100), self.start_button, border_radius=10)
            text_surf = self.player_font.render("Waiting for Players...", True, (255, 255, 255))
            self.screen.blit(text_surf, text_surf.get_rect(center=self.start_button.center))

        if self.join_request_popup_text:
            self.draw_popup()
            
    def draw_popup(self):
        s = pygame.Surface((750, 250), pygame.SRCALPHA); s.fill((0, 0, 0, 220))
        popup_rect = s.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(s, popup_rect.topleft)
        text_surf = self.popup_font.render(self.join_request_popup_text, True, (255, 255, 255))
        self.screen.blit(text_surf, text_surf.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50)))
  
        self.yes_button_rect = pygame.Rect(0, 0, 140, 55); self.yes_button_rect.center = (popup_rect.centerx - 110, popup_rect.centery + 50)
        self.no_button_rect = pygame.Rect(0, 0, 140, 55); self.no_button_rect.center = (popup_rect.centerx + 110, popup_rect.centery + 50)
        pygame.draw.rect(self.screen, (0, 150, 0), self.yes_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (150, 0, 0), self.no_button_rect, border_radius=10)
        yes_text = self.button_font.render("Accept", True, (255, 255, 255))
        no_text = self.button_font.render("Deny", True, (255, 255, 255))
        self.screen.blit(yes_text, yes_text.get_rect(center=self.yes_button_rect.center))
        self.screen.blit(no_text, no_text.get_rect(center=self.no_button_rect.center))