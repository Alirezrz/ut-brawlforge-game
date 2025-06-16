import pygame
import os

class Terrorist:
    def __init__(self, x, y, screen_width, screen_height,Ninja,Robo,platforms):
        self.x_pos = x
        self.y_pos = y
        self.on_platform=False
        self.current_platform =None
        self.horizontal_auto_speed=0
        self.allow_move_right=True
        self.allow_move_left=True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.width=62
        self.height=118
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 63
        self.max_health=100
        self.bullets = []
        self.platforms=platforms
        
        
        
        
        self.Walk_Range=300
        self.VisionRadious=100
        self.walk_strength=3
        self.walked_len=0
        
        
        
        #loadings :
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "terrorist")
        tmp = pygame.image.load(os.path.join(base_path, "walk", f"1_terrorist_1_Walk_000.png"))
        self.pic=pygame.transform.scale(tmp,(62,118))
        
        
        # Animation attributes
        self.current_picture = self.pic
        self.current_frame_index = 0
        self.animation_speed = 100
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False 
        
        
        
        
        
        

        
    
    def display(self, screen ,offset):
        display_picture = self.current_picture
        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0] , self.y_pos - offset[1]))
        

            
            
            
    def stop_horizontal_movement(self):
        self.is_moving_horizontally = False
        
        
        
        
    def fall_from_platform(self):
        if self.current_platform != None:
            if self.x_pos + self.width  < self.current_platform.x_pos  or self.x_pos > self.current_platform.x_pos + self.current_platform.width  :
                self.on_ground=False                
                self.current_platform=None

    def  move_with_platform(self):
        if(self.current_platform != None):
            if(self.current_platform.moving):
                self.horizontal_auto_speed=2.5*self.current_platform.direction
                self.horizontal_move()

    def move_right(self):
        
        if self.allow_move_right:
            self.x_pos += self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()
        

    def move_left(self):
        #print(self.allow_move_left)
        if self.allow_move_left:
            self.x_pos -= self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'left'
            # Removed screen boundary clamping for infinite world
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            # self.clamp_to_screen() # Removed for infinite world
            self.fall_from_platform()
        


    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def is_on_ground(self):
        if self.current_platform:
            self.on_ground = True
        elif(self.current_platform==None):
            self.on_ground=False    
        

    def vertical_move(self):
           
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos,self.y_pos)     # hitbox of the hero should be updated
        
    def horizontal_move(self):
            # self.clamp_to_screen() # Removed for infinite world
            self.x_pos += self.horizontal_auto_speed 
            self.horizontal_auto_speed=0
  
    
    def platforms_collisions(self,platforms):
        for platform in platforms:
            if self.x_pos + self.width  > platform.x_pos  and self.x_pos < platform.x_pos + platform.width  :
                if ((self.y_pos + self.height) >= platform.y_pos) and ((self.y_pos + self.height) < (platform.y_pos + platform.height)+10) :
                   # if self.vertical_speed < 0:
                  
                    self.on_ground=True
                    self.vertical_speed=0
                    self.y_pos=platform.y_pos - self.height 
                    self.current_platform=platform

            if  self.x_pos + self.width  >= platform.x_pos  and self.x_pos <= platform.x_pos + platform.width  :
                    
                if ((self.y_pos + self.height) > platform.y_pos) and ((self.y_pos) < (platform.y_pos + platform.height)) :  
                    
                    if abs(self.x_pos-(platform.x_pos + platform.width )) <= 10:
                        
                        self.allow_move_left=False
                        self.x_pos=platform.x_pos + platform.width 
                    if abs(self.x_pos+self.width-(platform.x_pos )) <=10:
                        
                        self.allow_move_right=False     
                        self.x_pos=platform.x_pos -self.width
            else :
                self.allow_move_left=True
                self.allow_move_right=True

    def jump_under_platform(self,platforms):
        if(self.vertical_speed>0):
            for platform in platforms :
                if self.x_pos + self.width  > platform.x_pos  and self.x_pos < platform.x_pos + platform.width :
                    if self.y_pos<= platform.y_pos + platform.height and self.y_pos  > platform.y_pos :
                        self.vertical_speed=0
                        self.y_pos=platform.y_pos + platform.height
                        
                        
                        
    def Walk(self):
    # Edge detection
        next_x = self.x_pos + (self.walk_strength if self.Look == 'right' else -self.walk_strength)
        foot_y = self.y_pos + self.height + 5  # just below his feet

        on_edge = True
        for platform in self.platforms:
            if platform.x_pos <= next_x <= platform.x_pos + platform.width:
                if abs(platform.y_pos - foot_y) <= 10:
                    on_edge = False
                    break

        if on_edge:
        # Turn around if no ground ahead
            self.walked_len = 0
            self.Look = 'left' if self.Look == 'right' else 'right'

    # Basic range-based direction flip
        if self.walked_len > self.Walk_Range:
            self.walked_len = 0
            self.Look = 'left' if self.Look == 'right' else 'right'

    # Apply movement
        if self.Look == 'right':
            self.x_pos += self.walk_strength
        else:
            self.x_pos -= self.walk_strength

        self.walked_len += self.walk_strength
        self.hitbox.topleft = (self.x_pos, self.y_pos)

            
            
    def Update(self):
        self.on_ground = False
        self.Walk()
        self.gravity()
        self.vertical_move()
                        
                        
                        
       