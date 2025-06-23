import pygame




class Bullet:
    def __init__(self, x, y, speed, direction, bullet_picture, screen_width,owner="unkown"):
        self.owner=owner
        self.x_pos = x
        self.y_pos = y
        self.speed = speed
        self.direction = direction
        self.picture = bullet_picture
        self.width = bullet_picture.get_width()
        self.height = bullet_picture.get_height()
        self.screen_width = screen_width
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        
        
        shrink = 8  
        self.hitbox = pygame.Rect(
            self.x_pos + shrink // 2,
            self.y_pos + shrink // 2,
            self.width - shrink,
            self.height - shrink
        )

    def update(self):
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)
        
        shrink = 8
        self.hitbox.topleft = (self.x_pos + shrink // 2, self.y_pos + shrink // 2)

    def draw(self, screen, offset):
        if self.direction == 'right':
            screen.blit(self.picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        else:
            screen.blit(pygame.transform.flip(self.picture, True, False), (self.x_pos - offset[0], self.y_pos - offset[1]))

    def is_off_screen(self, screen_width):
        # Bullets are now removed if they go far off screen to simulate infinite world
        # but prevent an endless list of bullets.
        return self.x_pos < -screen_width or self.x_pos > screen_width * 2

    def explode(self, screen, explosion_picture):
        screen.blit(explosion_picture, (self.x_pos, self.y_pos))
