import pygame

class Hero:
    def __init__(self, x, y, hero_picture, screen_width, screen_height,bullet_picture):
        self.x_pos = x
        self.y_pos = y
        self.on_platform=False
        self.current_platform =None
        self.bullet_picture=bullet_picture
        self.width = hero_picture.get_width()
        self.height = hero_picture.get_height()
        self.horizontal_auto_speed=0
        self.picture = hero_picture
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 20
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
    def fall_from_platform(self):
        if self.current_platform != None:
            if self.x_pos + self.width  < self.current_platform.x_pos + 20 or self.x_pos > self.current_platform.x_pos + self.current_platform.width - 20 :
                self.on_ground=False                
                self.current_platform=None

    def  move_with_platform(self):
        if(self.current_platform != None):
            if(self.current_platform.moving):
                self.horizontal_auto_speed=2.5*self.current_platform.direction
                self.horizontal_move()

    def move_right(self):
        self.x_pos += self.horizontal_speed
        self.Look = 'right'
        if self.x_pos >= self.screen_width - self.width:
            self.x_pos = self.screen_width - self.width
        self.hitbox.topleft = (self.x_pos, self.y_pos)
        self.fall_from_platform()
        

    def move_left(self):
        self.x_pos -= self.horizontal_speed
        self.Look = 'left'
        if self.x_pos <= 0:
            self.x_pos = 0
        self.hitbox.topleft = (self.x_pos, self.y_pos)
        self.clamp_to_screen()
        self.fall_from_platform()


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
        bullet = Bullet(self.x_pos + self.width // 2, self.y_pos + self.height // 2, 10, self.Look, self.bullet_picture , self.screen_width)
        self.bullets.append(bullet)
        shot_bullets.append(bullet)

    def update_bullets(self, screen,shot_bullets):
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
            self.vertical_speed = self.jump_strenght
        self.on_ground=False 
        self.current_platform=None 
         

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def is_on_ground(self):
        if self.y_pos == self.screen_height-self.height:
            self.on_ground = True
        elif(self.current_platform==None):
            self.on_ground=False    
        

    def vertical_move(self):
        if self.vertical_speed < 0 and self.y_pos >= self.screen_height - self.height:       # به دلیل وجود شتاب وقتی هیرو  با سرعت زیاد میومد پایین ممکن بود توی هیچ فریمی روی پلتفرم اصلی قرار نگیره و مستقیم بره پایین برای همین این خط اضافه شده (دلیل اضافه شدن علامت بزرگتر مساوی به جای مساوی)
            self.clamp_to_screen()
            self.vertical_speed = 0
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos,self.y_pos)     # hitbox of the hero should be updated
        
    def horizontal_move(self):
            self.clamp_to_screen()
            self.x_pos += self.horizontal_auto_speed 
            self.horizontal_auto_speed=0
  
    
    def platforms_collisions(self,platforms):
        for platform in platforms:
            if self.x_pos + self.width  > platform.x_pos + 20 and self.x_pos < platform.x_pos + platform.width - 20 :
                if ((self.y_pos + self.height) >= platform.y_pos) and ((self.y_pos + self.height) < (platform.y_pos + platform.height)+10) :
                    if self.vertical_speed < 0:
                        self.on_ground=True
                        self.vertical_speed=0
                        self.y_pos=platform.y_pos - self.height + 17
                        self.current_platform=platform

    def jump_under_platform(self,platforms):
        if(self.vertical_speed>0):
            for platform in platforms :
                if self.x_pos + self.width  > platform.x_pos + 20 and self.x_pos < platform.x_pos + platform.width - 20 :
                    if self.y_pos + 20 <= platform.y_pos + platform.height and self.y_pos + 20 > platform.y_pos :
                        self.vertical_speed=0
                        self.y_pos=platform.y_pos + platform.height