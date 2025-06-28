import pygame
import os


class Gunman:
    def __init__(self,x,y):
        self.x_pos=x
        self.y_pos=y
                          # remember to update the sizes
        self.width=60                                               
        self.height=114
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
        
        self.status='idle'
        
        
        
        #loading section:
        
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "gunman")

        
        
        self.idle_frames=[]
        
        for i in range(4):
            path=os.path.join(base_path , "idle" , f"{i}.png")
            
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (60,114)
                )
            )
            
            
            
        self.display_frame=self.idle_frames[0]    
        self.animation_speed=150
        self.last_animation_update=0
        self.frame_index=0 
            
        
        
    def display(self,screen,offset):
        screen.blit(self.display_frame,(self.x_pos-offset[0],self.y_pos-offset[1]))
        print(self.frame_index)
        
        
    def update_animation(self):
        current_time=pygame.time.get_ticks()
        elapsed_time= current_time - self.last_animation_update
        if self.status=='idle':
            if elapsed_time >= self.animation_speed:
                self.frame_index=elapsed_time%(len(self.idle_frames))
                self.display_frame=self.idle_frames[self.frame_index]
                self.last_animation_update=current_time
                return
            
            
    def Update(self):
        self.update_animation()
        
            