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
ghost_width=ghost.get_width()
ghost_height=ghost.get_height()

ghost2=pygame.image.load("ghost2.png")
ghost2=pygame.transform.scale(ghost2,(64,64))
ghost2_width=ghost.get_width()
ghost2_height=ghost.get_height()


 
 
 
 
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
        shot_bullets.append(bullet)
        
    def update_bullets(self, screen):
        for bullet in self.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.is_off_screen(screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)

                
                
    
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
        self.condition='alive'
        
     
     
     
    def move(self):
        self.x_pos+=self.speed
        if self.x_pos <= 0 or self.x_pos >= screen_width - self.width:
            self.x_pos-=self.speed
            self.speed*=-1
        self.hitbox.topleft = (self.x_pos, self.y_pos)  
            
               
    def display(self,screen):
        screen.blit(self.picture,(self.x_pos,self.y_pos))
        self.move()
        
        
    def damage(self,volume):
        self.health-=volume
        self.picture=ghost2
        if self.speed<0 :
            self.speed =-7
        else:
            self.speed=7
        if self.health==0:
            self.condition='dead'
        
        
    
    
            
        



#==================================================================================================================================================================================================
# functions :


    





#==================================================================================================================================================================================================

enemys =list ()
for i in range(5): 
    enemys.append(Enemy(random.randint(0,screen_width-ghost_width),screen_height-ghost_height-platform_height,5))
    
    
shot_bullets= list()





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
    
        
   

                
          
          
          
          
          
          
    for enemy in enemys[:]:  
        ALIVE = True
        for bullet in shot_bullets[:]:  
            if enemy.hitbox.colliderect(bullet.hitbox):
                shot_bullets.remove(bullet)
                if bullet in hero.bullets:
                    hero.bullets.remove(bullet)
                ALIVE = False
                break  
        if ALIVE:
            enemy.display(screen)
        else:
            enemy.damage(50)
            if enemy.condition=='dead':
                enemys.remove(enemy)
                
            

    
     
        
           
    pygame.draw.rect(screen, platform_color, pygame.Rect(0, screen_height - platform_height, screen_width, platform_height))
    hero.update_bullets(screen)   
    hero.display(screen)
    pygame.display.update()
    clock.tick(60)
    

