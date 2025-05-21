import pygame

class Bullet:
    def __init__(self, x, y, speed, direction, bullet_picture, screen_width):
        self.x_pos = x
        self.y_pos = y
        self.speed = speed
        self.direction = direction
        self.picture = bullet_picture
        self.width = bullet_picture.get_width()
        self.height = bullet_picture.get_height()
        self.screen_width = screen_width
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def update(self):
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def draw(self, screen):
        if self.direction == 'right':
            screen.blit(self.picture, (self.x_pos, self.y_pos))
        else:
            screen.blit(pygame.transform.flip(self.picture, True, False), (self.x_pos, self.y_pos))

    def is_off_screen(self, screen_width):
        return self.x_pos < -self.width or self.x_pos > screen_width

    def explode(self, screen, explosion_picture):
        screen.blit(explosion_picture, (self.x_pos, self.y_pos))