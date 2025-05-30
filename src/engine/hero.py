import pygame

class Hero:
    def __init__(self, x, y, hero_picture, screen_width, screen_height,bullet_picture,health_bar_green,health_bar_red,hero_profile_picture,hero_run_frames):
        self.x_pos = x
        self.y_pos = y
        self.hero_profile_picture=hero_profile_picture
        self.health_bar_green=health_bar_green
        self.health_bar_red=health_bar_red
        self.on_platform=False
        self.current_platform =None
        self.bullet_picture=bullet_picture
        self.width = hero_picture.get_width()
        self.height = hero_picture.get_height()
        self.horizontal_auto_speed=0
        self.picture = hero_picture
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
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 63
        self.max_health=100
        self.bullets = []
        
        
        # Animation attributes
        self.idle_picture = hero_picture 
        self.run_frames = hero_run_frames
        self.current_picture = self.idle_picture 
        self.current_frame_index = 0
        self.animation_speed = 200 # Milliseconds per frame
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False 
        
    
    def display(self, screen ,offset):
        self.health_bar_green= pygame.transform.scale(self.health_bar_green, (300*(self.health/self.max_health), 35))
        self.health_bar_red= pygame.transform.scale(self.health_bar_red, (300, 35))
        display_picture = self.current_picture
        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0] , self.y_pos - offset[1]))
        screen.blit(self.health_bar_red,(35,0))
        screen.blit(self.health_bar_green,(35,0))
        screen.blit(pygame.transform.scale(self.hero_profile_picture, (35, 35)),(0,0))
        
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.is_moving_horizontally and self.run_frames:
            if current_time - self.last_frame_update_time > self.animation_speed:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.run_frames)
                self.current_picture = self.run_frames[self.current_frame_index]
                self.last_frame_update_time = current_time
        else:
            self.current_picture = self.idle_picture
            self.current_frame_index = 0
            
            
            
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
        
        
        
        

    # Removed clamp_to_screen method for infinite world
    # def clamp_to_screen(self):
    #     if self.x_pos < 0:
    #         self.x_pos = 0
    #     if self.x_pos > self.screen_width - self.width:
    #         self.x_pos = self.screen_width - self.width
    #     if self.y_pos < 0:
    #         self.y_pos = 0
    #     if self.y_pos > self.screen_height - self.height:
    #         self.y_pos = self.screen_height - self.height

    def shoot(self, shot_bullets, Bullet):
        bullet = Bullet(self.x_pos + self.width // 2, self.y_pos + self.height // 2, 15, self.Look, self.bullet_picture , self.screen_width)
        self.bullets.append(bullet)
        shot_bullets.append(bullet)
    def respawn(self):
        self.current_platform=None
        self.on_ground=False
        self.x_pos=200
        self.y_pos=250 - self.picture.get_height()-20
        self.vertical_speed=0
        
    def update_bullets(self, screen,shot_bullets):
        for bullet in self.bullets[:]:
            bullet.update()
            # The bullet drawing offset is handled by the camera in game.py now
            # So, the bullet.draw(screen,[1,0]) line here is not needed.
            # However, if you want to keep it, it should also use the camera scroll.
            # For now, I'll assume bullets are drawn via the camera's render method.
            
            # Bullets are removed if they go far off screen to simulate infinite world
            # but prevent an endless list of bullets.
            if bullet.is_off_screen(self.screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)

    def jump(self):
        if self.on_ground:
            self.vertical_speed = self.jump_strenght
        self.on_ground=False 
        self.current_platform=None 
        
        
        
        
                    
         

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