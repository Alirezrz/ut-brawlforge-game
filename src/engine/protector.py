import pygame
import os
from config import screen_width, screen_height
import math


class Guard_Drone:
    def __init__(self,player,owner="unknown"):
        self.player=player
        self.x_pos=-(screen_width)
        self.y_pos=-(screen_height)
        self.status='idle'
        self.owner=owner
        self.bullets=[]
        
        
        #loading section:
        
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Guard Drone")
        
        
        self.idle_frames=[]
        
        for i in range (8):
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'idle', f"{i}.png")
                    ),
                    (50,35)
                )
                
            )
            
            
        self.walk_frames=[]
        
        for i in range (8):
            self.walk_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'walk', f"{i}.png")
                    ),
                    (50,35)
                )
                
            )
            
            
        self.display_frame=self.idle_frames[0]
        self.last_animation_update=0
        self.animation_speed=25
        self.frame_index=0
        
        
            
            
            
            
            
            
            
    def display(self,screen,offset):
        screen.blit(self.display_frame,(self.x_pos-offset[0],self.y_pos-offset[1]))







    def update_aniamtion(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time-self.last_animation_update
        if elapsed_time>self.animation_speed:
            if self.status=='idle':
                self.frame_index=(elapsed_time)%len(self.idle_frames)
                self.display_frame=self.idle_frames[self.frame_index]
            elif self.status=='forward':
                self.frame_index=(elapsed_time)%len(self.walk_frames)
                self.display_frame=self.walk_frames[self.frame_index]
            elif self.status=='backward':
                self.frame_index=(elapsed_time)%len(self.walk_frames)
                self.display_frame=pygame.transform.flip(self.walk_frames[self.frame_index],True,False)
                
                
            
            
            
    def Update(self,screen,offset,shot_bullets):
        self.Vision(shot_bullets)
        self.update_pos()
        self.update_aniamtion()
        self.display(screen,offset)
        for b in self.bullets:
            b.update()
            b.display(screen,offset)
        
        
        
    def update_pos(self):
        if self.player.x_pos > self.x_pos + 40:
            self.x_pos += self.player.horizontal_speed - 1
            self.status='forward'
        elif self.x_pos > self.player.x_pos + 40:
            self.x_pos -= self.player.horizontal_speed - 1
            self.status='backward'
        else:
            self.status='idle'
    
        target_y = self.player.y_pos - 40
        if abs(self.y_pos - target_y) > 2: 
            if self.y_pos < target_y:
                self.y_pos += min(5, target_y - self.y_pos)  
            elif self.y_pos > target_y:
                self.y_pos -= min(5, self.y_pos - target_y)  
                
                
                
    
    def Vision(self,shot_bullets):
        for bullet in shot_bullets:
            d = math.sqrt(((self.player.x_pos - bullet.x_pos)**2) +((self.player.y_pos - bullet.y_pos)**2))
            if d < 400 and bullet.owner!=self.owner:
                print(f"detect bullet   {bullet.owner}")
                self.shoot(bullet)
                
                
                
    def shoot(self,target):
        self.bullets.append(
            laser(
                self.x_pos,self.y_pos,target
            )
        )
            
            
            
            




class laser:
    def __init__(self,x,y,target):
       self.x_pos=x
       self.y_pos=y
       self.target=target
       self.speed=20
       path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Drone","lazer.png")
       self.image=pygame.transform.scale(
            pygame.image.load(
                path
            ),
            (10,10)
        )
        
        
        
    def display(self,screen,offset):
        screen.blit(self.image,(self.x_pos-offset[0],self.y_pos-offset[1])) 
         


    def update(self):
        if self.x_pos < self.target.x_pos:
            self.x_pos+=self.speed
        elif self.x_pos>self.target.x_pos:
            self.x_pos-=self.speed
        
        
        if self.y_pos < self.target.y_pos:
            self.y_pos+=self.speed
        elif self.y_pos>self.target.y_pos:
            self.y_pos-=self.speed
            
            
            
        
            
            
        
        