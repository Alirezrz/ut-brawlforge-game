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
            
            
        self.walk_frames=[]
        for i in range(6):
            path=os.path.join(base_path , "walk" , f"{i}.png")
            
            self.walk_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (53,114)
                )
            )
            
            
            
            
            
        self.display_frame=self.idle_frames[0]    
        self.animation_speed=150
        self.last_animation_update=0
        self.frame_index=0 
        
        self.Walk_Range = 500
        self.VisionRadious = 400
        self.VisionHeight = 80
        self.walk_strength = 1
        self.walked_len = 0
        self.allow_move_right=True
        self.allow_move_left=True
            
        
        
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
        #print(self.Look)
        if self.status == 'exploded':
            return

        direction = self.walk_strength if self.Look == 'right' else -self.walk_strength
        next_x = self.x_pos + direction
        foot_x = next_x + self.width // 2
        foot_y = self.y_pos + self.height + 1

        on_platform = False
        blocked_by_wall = False

        for platform in self.platforms:
            platform_top = platform.y_pos
            platform_left = platform.x_pos
            platform_right = platform.x_pos + platform.width

            # Check for ground support
            if platform_left <= foot_x <= platform_right:
                if abs(foot_y - platform_top) <= 10:
                    on_platform = True

            # Check wall collision
            if self.y_pos + self.height > platform.y_pos and self.y_pos < platform.y_pos + platform.height:
                if self.Look == 'right':
                    if self.x_pos + self.width <= platform.x_pos and abs((self.x_pos + self.width + self.walk_strength) - platform.x_pos) <= 5:
                        blocked_by_wall = True
                else:
                    if self.x_pos >= platform.x_pos + platform.width and abs(self.x_pos - (platform.x_pos + platform.width + self.walk_strength)) <= 5:
                        blocked_by_wall = True

        if not on_platform or blocked_by_wall or self.walked_len > self.Walk_Range:
            self.walked_len = 0
            self.Look = 'left' if self.Look == 'right' else 'right'
            self.status = 'idle'
            return

        if self.Look == 'right' and self.allow_move_right:
            self.x_pos += self.walk_strength
        elif self.Look == 'left' and self.allow_move_left:
            self.x_pos -= self.walk_strength

        self.walked_len += self.walk_strength
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.display_frame.get_width(), self.display_frame.get_height())
        self.status = 'walk'

