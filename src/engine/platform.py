import pygame
from config import platform_height

class Platform:
    def __init__(self, x, y, width, image, height=platform_height,moving=False ,move_range=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.moving = moving
        self.move_range = move_range
        self.start_x =x
        self.offset = 0
        self.direction=1
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
     if self.moving:
        self.offset += 2.5 * self.direction
        if abs(self.offset) >= self.move_range:
            self.direction *= -1
            self.offset = max(min(self.offset, self.move_range), -self.move_range)
        self.rect.x = self.start_x + self.offset


