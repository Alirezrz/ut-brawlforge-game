import pygame

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
                            return button["action"]

            pygame.display.update()

    def is_hovered(self,button_pos,mouse_pos):
        button_rect = pygame.Rect(0,0,200,50)
        button_rect.center = button_pos
        return button_rect.collidepoint(mouse_pos)