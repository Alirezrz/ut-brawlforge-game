import pygame 
import random
import os
pygame.init()


clock = pygame.time.Clock()


# screen :

screen = pygame.display.set_mode((1200,674))
pygame.display.set_caption("BrawlForge")
icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)

screen_width=1200
screen_height=674


platform_height = 20  
platform_color = (105, 5, 120)  



# image loadings ------
#                     |
#                     |
#                     V


background = pygame.image.load("BrawlhalaBackground.jpg")



hero_picture = pygame.image.load("hero.png")
Hero_width = hero_picture.get_width()
Hero_height = hero_picture.get_height()


bullet_picture = pygame.image.load("bullet.png")
bullet_picture=pygame.transform.scale(bullet_picture,(40,40))
bullet_width=bullet_picture.get_width()
bullet_height=bullet_picture.get_height()


explosion = pygame.image.load("explode.png")
explosion=pygame.transform.scale(explosion,(40,40))




ghost=pygame.image.load("ghost.png")
ghost=pygame.transform.scale(ghost,(64,64))
ghost_width=ghost.get_width
ghost_height=ghost.get_height


 
 
 
 
#=======================================================================================================================================================================================================
 
 
 # Hero Class:
 
class Hero:
    def __init__(self,x,y):
        self.x_pos=x
        self.y_pos=y
        self.width=Hero_width
        self.height=Hero_height
        self.picture = pygame.image.load("hero.png")
        self.Look='right'
        self.horizontal_speed=7
        self.vertical_speed=5
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health=100
        self.bullets=[]
        
        

        
        
        
        
    
    def display(self,screen):
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
        x=0
        y=0
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.is_off_screen(screen_width):
                x=bullet.x_pos
                y=bullet.y_pos
                self.bullets.remove(bullet)
                
                
    
    #  def jump---
    #            |
    #            V
            
                


        
        
        
        
        

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
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    
    def update(self):
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed

        self.rect.topleft = (self.x_pos, self.y_pos)
        
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
     
     
     
    # Chekcing for player inputs :       
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        hero.move_right()
    if keys[pygame.K_a]:
        hero.move_left()
    
        
   

                
          
          
          
          
          
          
          
    pygame.draw.rect(screen, platform_color, pygame.Rect(0, screen_height - platform_height, screen_width, platform_height))
    hero.update_bullets(screen)   
    hero.display(screen)
    pygame.display.update()
    clock.tick(60)
    

