import pygame
import os


class Drone:
    
    
    def __init__(self,x,y):
        
        
        
        self.x_pos=x
        self.y_pos=y
        self.horizentalmove_range=400
        self.status='forward'
        self.prev_status='none'
        self.moved_len=0
        self.speed=2
        
        
        
        
        
        #loading section:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Drone")
        
        self.Idle_frames=[]
        for i in range (4):
            self.Idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Idle', f"{i}.png")
                    ),
                    (100,50)
                )
                
            )
            
            
            
        self.Forward_frames=[]
        for i in range (4):
            self.Forward_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Forward', f"{i}.png")
                    ),
                    (100,53)
                )
                
            )
            
            
        self.Back_frames=[]
        for i in range (4):
            self.Back_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Back', f"{i}.png")
                    ),
                    (100,50)
                )
                
            )
            
        self.display_pic=self.Idle_frames[0] 
        self.animation_speed  = 15 
        self.Last_animationUpdate=0
        self.frame_index=0 
        self.time_falg=0
        self.idle_duration=2000
        
            
            
            
            
            
    def display(self,screen,offset):
        self.Move()
        self.Update_animtion()
        screen.blit(self.display_pic,(self.x_pos- offset[0],self.y_pos - offset[1]))
        
        
        
    def Update_animtion(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time -  self.Last_animationUpdate 
        if elapsed_time>= self.animation_speed:
            if self.status=='idle':
                self.frame_index= (elapsed_time)%len(self.Idle_frames)
                self.display_pic=self.Idle_frames[self.frame_index]
                self.Last_animationUpdate=current_time
            elif self.status=='forward':
                self.frame_index= (elapsed_time)%len(self.Forward_frames)
                self.display_pic=self.Forward_frames[self.frame_index]
                self.Last_animationUpdate=current_time
                
            elif self.status=='backward':
                self.frame_index= (elapsed_time)%len(self.Back_frames)
                self.display_pic=self.Back_frames[self.frame_index]
                self.Last_animationUpdate=current_time
                
                
        
        
    def Move(self):
        current_time=pygame.time.get_ticks()
        if self.status=='forward':
            if self.moved_len < self.horizentalmove_range:
                self.x_pos+=self.speed
                self.moved_len+=self.speed
            else:
                self.status='idle'
                self.prev_status='forward'
                self.moved_len=0
                self.time_falg=current_time
        elif self.status=='idle':
            self.moved_len=0
            if current_time-self.time_falg>self.idle_duration:
                if self.prev_status=='forward':
                    self.status='backward'
                    self.time_falg=0
                    self.prev_status='idle'
                else:
                    self.status='forward'
                    self.time_falg=0
                    
                
        elif self.status=='backward':
            if self.moved_len<= self.horizentalmove_range:
                self.x_pos-=self.speed
                self.moved_len+=self.speed
            else:
                self.prev_status='backward'
                self.status='idle'
                self.time_falg=current_time
        
            
                    
                    
                    
            
                
    
        
        
        
        
        
        
        
        