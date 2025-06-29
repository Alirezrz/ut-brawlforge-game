import pygame
import os


class Gunman:
    def __init__(self,x,y,platforms):
        self.x_pos=x
        self.y_pos=y
                          # remember to update the sizes
        self.width=60                                               
        self.height=114
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
        
        self.status='idle'
        self.Look='right'
        self.last_idle=0
        self.idle_duration=3000
        
        self.platforms=platforms
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
            
        sizes=[51,50,67,74,64,53]
        self.walk_frames=[]
        for i in range(6):
            path=os.path.join(base_path , "walk" , f"{i}.png")
            
            self.walk_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (sizes[i],114)
                )
            )
            
            
            
            
            
        self.display_frame=self.idle_frames[0]    
        self.animation_speed=150
        self.last_animation_update=0
        self.frame_index=0 
        
        self.Walk_Range = 200
        self.VisionRadious = 400
        self.VisionHeight = 80
        self.walk_strength = 1
        self.walked_len = 0
        self.allow_move_right=True
        self.allow_move_left=True
            
        self.idle_start_time=0
        self.idle_time=3000
        
    def display(self,screen,offset):
        if self.Look=='right':
            screen.blit(self.display_frame,(self.x_pos-offset[0],self.y_pos-offset[1]))
        else:
            screen.blit(pygame.transform.flip(self.display_frame,True,False),(self.x_pos-offset[0],self.y_pos-offset[1]))
            
        
        
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_animation_update

        if self.status == 'idle':
            if elapsed_time >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.display_frame = self.idle_frames[self.frame_index]
                self.last_animation_update = current_time

        elif self.status == 'walk':
            if elapsed_time >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.display_frame = self.walk_frames[self.frame_index]
                self.last_animation_update = current_time

            
            
    def Update(self):
        self.update_animation()
        self.Walk()
        
        
        
        
        
    def Walk(self):
        current_time = pygame.time.get_ticks()
        if self.status=='idle':
            elapsed_time=current_time - self.last_idle
            if elapsed_time > self.idle_duration:
                self.status='walk'
        if self.status=='walk':
            if self.walked_len <= self.Walk_Range:
                if self.Look=='right':
                    self.x_pos+=self.walk_strength
                    self.walked_len+=self.walk_strength
                else :
                    self.x_pos-=self.walk_strength
                    self.walked_len+=self.walk_strength
            
            else :
                self.walked_len=0
                self.status='idle'
                self.last_idle=current_time
                if self.Look=='right':
                    self.Look='left'
                else:
                    self.Look='right'
                    
                    
                
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.display_frame.get_width(), self.display_frame.get_height())


