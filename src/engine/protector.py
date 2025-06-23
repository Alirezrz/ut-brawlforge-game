import pygame
import os




class Guard_Drone:
    def __init__(self,player):
        self.player=player
        self.x_pos=self.player.x_pos-40
        self.y_pos=self.player.y_pos-40
        
        
        
        
        #loading section:
        
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Guard Drone")
        
        
        self.idle_frames=[]
        
        for i in range (4):
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'idle', f"{i}.png")
                    ),
                    (50,35)
                )
                
            )
            
            
        self.display_frame=self.idle_frames[0]
        self.last_animation_update=0
        self.animation_speed=100
        self.frame_index=0
        
        
            
            
            
            
            
            
            
    def display(self,screen,offset):
        screen.blit(self.display_frame,(self.x_pos-offset[0],self.y_pos-offset[1]))







    def update_aniamtion(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time-self.last_animation_update
        if elapsed_time>self.animation_speed:
            self.frame_index=(elapsed_time)%len(self.idle_frames)
            self.display_frame=self.idle_frames[self.frame_index]
            
            
            
            
    def Update(self,screen,offset):
        self.update_pos()
        self.update_aniamtion()
        self.display(screen,offset)
        
        
        
    def update_pos(self):
        if self.player.x_pos > self.x_pos + 40:
            self.x_pos += self.player.horizontal_speed - 1
        elif self.x_pos > self.player.x_pos + 40:
            self.x_pos -= self.player.horizontal_speed - 1
    
        target_y = self.player.y_pos - 40
        if abs(self.y_pos - target_y) > 2: 
            if self.y_pos < target_y:
                self.y_pos += min(5, target_y - self.y_pos)  
            elif self.y_pos > target_y:
                self.y_pos -= min(5, self.y_pos - target_y)  
            
        