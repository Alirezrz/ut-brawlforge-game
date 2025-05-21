import pygame

class Hero:
    def __init__(self, x, y, hero_picture, screen_width, screen_height):
        self.x_pos = x
        self.y_pos = y
        self.width = hero_picture.get_width()
        self.height = hero_picture.get_height()
        self.picture = hero_picture
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 10
        self.gravity_strenght = 1
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 100
        self.bullets = []

    def display(self, screen):
        if self.y_pos > self.screen_height - self.height:   # به دلیل وجود شتاب وقتی هیرو  با سرعت زیاد میومد پایین ممکن بود توی هیچ فریمی روی پلتفرم اصلی قرار نگیره و مستقیم بره پایین برای همین این خط اضافه شده
            self.y_pos = self.screen_height - self.height
        if self.Look == 'right':
            screen.blit(self.picture, (self.x_pos, self.y_pos))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(self.picture, True, False)
            screen.blit(flipped_picture, (self.x_pos, self.y_pos))

    def move_right(self):
        self.x_pos += self.horizontal_speed
        self.Look = 'right'
        if self.x_pos >= self.screen_width - self.width:
            self.x_pos = self.screen_width - self.width
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def move_left(self):
        self.x_pos -= self.horizontal_speed
        self.Look = 'left'
        if self.x_pos <= 0:
            self.x_pos = 0
        self.hitbox.topleft = (self.x_pos, self.y_pos)
        self.clamp_to_screen()

    def clamp_to_screen(self):
        if self.x_pos < 0:
            self.x_pos = 0
        if self.x_pos > self.screen_width - self.width:
            self.x_pos = self.screen_width - self.width
        if self.y_pos < 0:
            self.y_pos = 0
        if self.y_pos > self.screen_height - self.height:
            self.y_pos = self.screen_height - self.height

    def shoot(self, shot_bullets, Bullet):
        bullet = Bullet(self.x_pos + self.width // 2, self.y_pos + self.height // 2, 10, self.Look)
        self.bullets.append(bullet)
        shot_bullets.append(bullet)

    def update_bullets(self, screen):
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.is_off_screen(self.screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)

    def jump(self):
        if self.on_ground:
            self.vertical_speed += self.jump_strenght

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def is_on_ground(self):
        if self.y_pos == self.screen_height-self.height:
            self.on_ground = True
        else:
            self.on_ground = False

    def vertical_move(self):
        if self.vertical_speed < 0 and self.y_pos >= self.screen_height - self.height:       # به دلیل وجود شتاب وقتی هیرو  با سرعت زیاد میومد پایین ممکن بود توی هیچ فریمی روی پلتفرم اصلی قرار نگیره و مستقیم بره پایین برای همین این خط اضافه شده (دلیل اضافه شدن علامت بزرگتر مساوی به جای مساوی)
            self.clamp_to_screen()
            self.vertical_speed = 0
        self.y_pos -= self.vertical_speed