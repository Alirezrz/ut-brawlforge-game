import pygame 
import os




class Pumpkin:
    def __init__(self,x,y):
        
        
        self.x_pos=x
        self.y_pos=y
        
        self.aniamtion_speed=100
        self.last_animation_update=0
        self.frame_index=0
        
        
        
        
        
        
        
        
        # loading section:
        
        
        base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Objects","Pumpkin")
        
        self.idle_frames=[]
        
        for i in range (4):
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path , f"{i}.png")
                    ),
                    (1000,1000)
                )
                
            )
            
            
        self.display_pic=self.idle_frames[0]
        
    def display(self,screen,offset):
        screen.blit(self.display_pic,(self.x_pos-offset[0],self.y_pos-offset[1]))
        print('displaying')
        print(len(self.idle_frames))
        

    def update_animation(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time-self.last_animation_update
        if self.last_animation_update - current_time >= self.aniamtion_speed:
            self.frame_index= (elapsed_time)%len(self.idle_frames)
            self.display_pic=self.idle_frames[self.frame_index]
            self.last_animation_update=current_time
            
            
            
            
    def Update(self,screen,offset):
        print("update")
        self.update_animation()
        self.display(screen,offset)
            
                
        
        
            
