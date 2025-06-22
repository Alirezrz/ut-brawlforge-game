import pygame 
import os

import math


class Pumpkin:
    def __init__(self,x,y,targets):
        
        
        self.x_pos=x
        self.y_pos=y
        self.targets=targets
        self.aniamtion_speed=100
        self.last_animation_update=0
        self.frame_index=0
        self.status='idle'
        
        
        
        
        
        
        
        
        # loading section:
        
        
        base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Objects","Pumpkin")
        
        self.idle_frames=[]
        
        for i in range (4):
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path,"idle" , f"{i}.png")
                    ),
                    (60,60)
                )
                
            )
            
            
            
        self.scared_frames=[]
        
        for i in range (4):
            self.scared_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'scared', f"{i}.png")
                    ),
                    (60,60)
                )
                
            )
            
            
            
        self.display_pic=self.idle_frames[0]
        
    def display(self,screen,offset):
        screen.blit(self.display_pic,(self.x_pos-offset[0],self.y_pos-offset[1]))
       
        

    def update_animation(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time-self.last_animation_update
        if current_time-self.last_animation_update  >= self.aniamtion_speed:
            if self.status=='idle':
             self.frame_index= (elapsed_time)%len(self.idle_frames)
             self.display_pic=self.idle_frames[self.frame_index]
             self.last_animation_update=current_time
            else:
             self.frame_index= (elapsed_time)%len(self.scared_frames)
             self.display_pic=self.scared_frames[self.frame_index]
             self.last_animation_update=current_time
                
            
            
    def update_status(self):
        distances=[]
        self.status='idle'
        for i in range(len(self.targets)):
            distances.append(math.sqrt(((self.x_pos-self.targets[i].x_pos)**2)+((self.y_pos - self.targets[i].y_pos)**2)))
            
            
             
        FLAG=False  
        for i in range (len(self.targets)):
            if distances[i]<250:
                self.status='scared'
                return
        self.status='idle'
                
    def Update(self,screen,offset):
        self.update_status()
        self.update_animation()
        self.display(screen,offset)
            
                
        
        
            
