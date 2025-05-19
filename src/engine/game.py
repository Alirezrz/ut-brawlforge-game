import pygame 
import random
pygame.init()


clock = pygame.time.Clock()


# screen :

screen = pygame.display.set_mode((1200,674))
pygame.display.set_caption("BrawlForge")
icon = pygame.image.load("../assets/images/icon.jpg")
pygame.display.set_icon(icon)

screen_width=1200
screen_height=674


platform_height = 20  
platform_color = (105, 5, 120)  



# image loadings ------
#                     |
#                     |
#                     V


background = pygame.image.load("../assets/images/BrawlhalaBackground.jpg")



hero_picture = pygame.image.load("../assets/images/hero.png")
Hero_width = hero_picture.get_width()
Hero_height = hero_picture.get_height()


bullet_picture = pygame.image.load("../assets/images/bullet.png")
bullet_picture=pygame.transform.scale(bullet_picture,(40,40))
bullet_width=bullet_picture.get_width()
bullet_height=bullet_picture.get_height()


explosion = pygame.image.load("../assets/images/explode.png")
explosion=pygame.transform.scale(explosion,(40,40))




ghost=pygame.image.load("../assets/images/ghost.png")
ghost=pygame.transform.scale(ghost,(64,64))
ghost_width=ghost.get_width()
ghost_height=ghost.get_height()


 
 
 
 
#=======================================================================================================================================================================================================
 
 
 # Hero Class:
 
class Hero:
    def __init__(self,x,y):
        self.x_pos=x
        self.y_pos=y
        self.width=Hero_width
        self.height=Hero_height
        self.picture = pygame.image.load("../assets/images/hero.png")
        self.Look='right'
        self.horizontal_speed=7
        self.vertical_speed=0
        self.jump_strenght=10
        self.gravity_strenght=1
        self.on_ground=False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health=100
        self.bullets=[]
    
        

        
        
        
        
    
    def display(self,screen):
        if self.y_pos > screen_height - self.height : # به دلیل وجود شتاب وقتی هیرو  با سرعت زیاد میومد پایین ممکن بود توی هیچ فریمی روی پلتفرم اصلی قرار نگیره و مستقیم بره پایین برای همین این خط اضافه شده
            self.y_pos=screen_height - self.height
        if self.Look == 'right':
            screen.blit(self.picture,(self.x_pos,self.y_pos))
            
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(self.picture, True, False)
            screen.blit(flipped_picture, (self.x_pos, self.y_pos))
    
    def move_right(self):
        self.x_pos += self.horizontal_speed
        self.Look = 'right'
        if self.x_pos >= screen_width - self.width:
            self.x_pos = screen_width - self.width
        self.hitbox.topleft = (self.x_pos, self.y_pos)
    
    def move_left(self):
        self.x_pos-=self.horizontal_speed  
        self.Look = 'left'
        if self.x_pos<=0:
            self.x_pos=0
        self.hitbox.topleft=(self.x_pos, self.y_pos)
        self.clamp_to_screen(screen_width,screen_height)
        
        
    
        
        
    def clamp_to_screen(self, screen_width, screen_height):
        if self.x_pos < 0:
            self.x_pos = 0
        if self.x_pos > screen_width - self.width:
            self.x_pos = screen_width - self.width
        if self.y_pos < 0:
            self.y_pos = 0
        if self.y_pos > screen_height - self.height:
            self.y_pos = screen_height - self.height
            
            
    def shoot(self):
        bullet = Bullet(self.x_pos + self.width // 2, self.y_pos + self.height // 2, 10, self.Look)
        self.bullets.append(bullet)
        
    def update_bullets(self, screen):
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.is_off_screen(screen_width):
                self.bullets.remove(bullet)
    
    def jump(self):
        if self.on_ground :
            self.vertical_speed+=self.jump_strenght


    def gravity(self):
        if self.on_ground == False :
            self.vertical_speed-=self.gravity_strenght
   
                    
    def is_on_ground(self):
        if self.y_pos == screen_height-Hero_height :
            self.on_ground=True
        else :
            self.on_ground=False


    def vertical_move(self):
        if self.vertical_speed < 0 and self.y_pos >= screen_height - self.height :       # به دلیل وجود شتاب وقتی هیرو  با سرعت زیاد میومد پایین ممکن بود توی هیچ فریمی روی پلتفرم اصلی قرار نگیره و مستقیم بره پایین برای همین این خط اضافه شده (دلیل اضافه شدن علامت بزرگتر مساوی به جای مساوی)
            self.clamp_to_screen(screen_width,screen_height)
            self.vertical_speed=0
        self.y_pos-=self.vertical_speed     
        
    
    
         


        
        
        
        
        

hero = Hero(0,screen_height-Hero_height)

#======================================================================================================================================================


# Bullet class:

class Bullet:
    def __init__(self, x, y, speed, direction):
        self.x_pos = x
        self.y_pos = y
        self.speed = speed
        self.direction = direction
        self.picture = bullet_picture
        self.width = bullet_width
        self.height = bullet_height
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    
    def update(self):
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed

        self.hitbox.topleft = (self.x_pos, self.y_pos)
        
    def draw(self, screen):
        if self.direction=='right':
            screen.blit(self.picture, (self.x_pos, self.y_pos))
        else :
            screen.blit(pygame.transform.flip(self.picture,True,False), (self.x_pos, self.y_pos))
            
        
        
    def is_off_screen(self, screen_width):
        return self.x_pos < -self.width or self.x_pos > screen_width
    

    def explode(self, screen):
        screen.blit(explosion, (self.x_pos, self.y_pos))
        
        
    
            
           

#==================================================================================================================================================================================================

# Enemy class :

class Enemy:
    def __init__(self,x,y,speed):
        self.x_pos=x
        self.y_pos=y
        self.picture=ghost
        self.health=100
        self.speed=speed
        self.width=ghost_width
        self.height=ghost_height
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
        
     
     
     
    def move(self):
        self.x_pos+=self.speed
        if self.x_pos <= 0 or self.x_pos >= screen_width - self.width:
            self.x_pos-=self.speed
            self.speed*=-1
            
               
    def display(self,screen):
        screen.blit(self.picture,(self.x_pos,self.y_pos))
        self.move()
        
    
    
            
        


enemy = Enemy(random.randint(0,screen_width-ghost_width),screen_height-ghost_height-platform_height,5)     

#==================================================================================================================================================================================================
# functions :


    





#==================================================================================================================================================================================================
#   Game Main Loop : 

GAME_ACTIVE = True

while GAME_ACTIVE:
    
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_ACTIVE=False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                hero.shoot()
     
    hero.is_on_ground() 
    hero.gravity()    
    hero.vertical_move()    

    # Chekcing for player inputs :       
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        hero.move_right()
    if keys[pygame.K_a]:
        hero.move_left()
    if keys[pygame.K_SPACE]:
        hero.jump()
    
    
    

                
        
          
          
          
          
          
    enemy.display(screen)     
    pygame.draw.rect(screen, platform_color, pygame.Rect(0, screen_height - platform_height, screen_width, platform_height))
    hero.update_bullets(screen)   
    hero.display(screen)
    pygame.display.update()
    clock.tick(60)
    

