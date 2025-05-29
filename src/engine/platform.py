import pygame
from config import platform_height # type: ignore

class Platform:
    def __init__(self, x, y, width, image, height=platform_height,moving=False ,move_range=0,start_direction=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))
        self.moving = moving
        self.height=height
        self.width=width
        self.move_range = move_range
        self.start_x =x
        self.x_pos=x
        self.y_pos=y
        self.x_center=x+(width/2)
        self.offset = 0
        self.direction=start_direction
        
    def draw(self, screen,offset):
        screen.blit(self.image, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update(self):
     if self.moving:
        self.offset += 2.5 * self.direction
        if abs(self.offset) >= self.move_range:
            self.direction *= -1
            self.offset = max(min(self.offset, self.move_range), -self.move_range)
        self.rect.x = self.start_x + self.offset
        self.x_pos = self.start_x + self.offset


