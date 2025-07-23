import pygame
import os
import time
class Menu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 74)  
        self.small_font = pygame.font.Font(None, 50)
        self.running = True
        self.buttons = [
            {"text": "Start Game", "pos": (screen.get_width() // 2, 300), "action": "start"},
            {"text": "Settings", "pos": (screen.get_width() // 2, 400), "action": "settings"},
            {"text": "Exit", "pos": (screen.get_width() // 2, 500), "action": "exit"}
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
            self.draw_text("BrawlForge", self.font, (255, 255, 255), (self.screen.get_width() // 2, 150))
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
        self.button_width=200
        self.button_height=50
        self.single_button = pygame.Rect(screen.get_width() // 2 - self.button_width // 2, screen.get_height() // 2 - 75, self.button_width, self.button_height)
        self.multi_button = pygame.Rect(screen.get_width() // 2 - self.button_width // 2, screen.get_height() // 2 + 25, self.button_width, self.button_height)
        self.exit_button = pygame.Rect(screen.get_width() // 2 - self.button_width // 2, screen.get_height() // 2 + 125, self.button_width, self.button_height)
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
            
            single_rect = self.draw_button("Single Player", self.screen.get_height() // 2 - 50, single_rect.collidepoint(mouse_pos) if 'single_rect' in locals() else False)
            multi_rect = self.draw_button("Multi Player", self.screen.get_height() // 2 + 50, multi_rect.collidepoint(mouse_pos) if 'multi_rect' in locals() else False)    
            exit_rect = self.draw_button("Exit", self.screen.get_height() // 2 + 150, self.exit_button.collidepoint(mouse_pos))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if single_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "single"
                    if multi_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "multi"
                    if exit_rect.collidepoint(event.pos):
                        if self.click_sound:
                            self.click_sound.play()
                        return "exit"
            
            pygame.display.flip()
        
        return "exit"
    



class MapCharacterMenu:
    def __init__(self, screen, background, hero_profile_picture):
        self.screen = screen
        self.background = background
        self.hero_profile_picture = hero_profile_picture
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 60)
        self.characters = ["Roboman", "Ninja", "NinjaGirl", "Archer"]
        self.maps = ["level1", "level2", "level3", "level4"]
        self.selected_character =None
        self.selected_map = None
        self.char_button_width = 150
        self.char_button_height = 50
        self.map_button_width = 100
        self.map_button_height = 100
        self.button_spacing = 20
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
        self.maps = ["multiplayer_arena", "boss_fight"] 
        self.selected_characters  = []
        self.selected_map = None
        self.char_button_width = 150
        self.char_button_height = 50
        self.map_button_width = 100
        self.map_button_height = 100
        self.button_spacing = 20

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
            preview_img = pygame.transform.scale(self.char_previews[button["text"]], (80,120))
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
