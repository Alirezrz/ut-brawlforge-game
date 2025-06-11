import pygame
import os
from config import ROBOMAN_LANDING_INSET, ROBOMAN_SIDE_COLLISION_TOP_BUFFER, ROBOMAN_SIDE_COLLISION_BOTTOM_BUFFER,jump_strenght ,horizontal_speed,gravity_strenght,profileSideSize,health_bar_lenght,roboman_health_bar_frame_thickness

class Roboman:

    def __init__(self, x, y,  roboman_health_bar_frame,roboman_health_bar, hero_profile_picture, screen_width, screen_height):

        self.x_pos = x
        self.y_pos = y
        self.hero_profile_picture = hero_profile_picture
        self.roboman_health_bar_frame = roboman_health_bar_frame
        self.roboman_health_bar = roboman_health_bar
        self.on_platform = False
        self.current_platform = None
        self.status="idle"

        
         

        
        
        
        
        
        #==================================================================================================================================
       
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "RoboMan_pictures")

        # Load run animation frames
        self.run_frames = []
        
        for i in range(1, 9):
            try:
                img_path = os.path.join(base_path, "hero_run_frames", f"Run ({i}).png")
                tmp = pygame.image.load(img_path)
                if i == 1: self.run_frames.append(pygame.transform.scale(tmp, (63, 118)))
                elif i == 2: self.run_frames.append(pygame.transform.scale(tmp, (62, 118)))
                elif i == 3: self.run_frames.append(pygame.transform.scale(tmp, (82, 118)))
                elif i == 4: self.run_frames.append(pygame.transform.scale(tmp, (77, 118)))
                elif i == 5: self.run_frames.append(pygame.transform.scale(tmp, (73, 118)))
                elif i == 6: self.run_frames.append(pygame.transform.scale(tmp, (80, 118)))
                elif i == 7: self.run_frames.append(pygame.transform.scale(tmp, (92, 118)))
                elif i == 8: self.run_frames.append(pygame.transform.scale(tmp, (79, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman run frame 'Run ({i}).png' not found at {img_path}. Check path.")
                self.run_frames.append(pygame.Surface((70, 118)))
                
                
                
                
        # Load idle animation frames from the 'idle'
        
        
        
        
        self.idle_frames = []
        for i in range(1, 11):
            try:
                img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                idle_tmp = pygame.image.load(img_path)
                self.idle_frames.append(pygame.transform.scale(idle_tmp, (70, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")
                self.idle_frames.append(pygame.Surface((70, 118)))


        # loading jump frames:
        
        self.jump_frames = []
        for i in range(1, 11):
            try:
                img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                jump_tmp = pygame.image.load(img_path)
                self.jump_frames.append(pygame.transform.scale(jump_tmp, (70, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")



        # Load shoot frames
        self.shoot_frames = []
        self.Bullet_Class_ref = None
        self.shot_bullets_ref = None
        
        for i in range(1, 5):
            try:
                img_path = os.path.join(base_path, "Shoot", f"Shoot ({i}).png")
                shoot_tmp = pygame.image.load(img_path)
                if i == 1: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (83, 118)))
                elif i == 2: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (83, 118)))
                elif i == 3: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (82, 118)))
                elif i == 4: self.shoot_frames.append(pygame.transform.scale(shoot_tmp, (84, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman Shoot frame 'Shoot ({i}).png' not found at {img_path}. Check path.")
                self.shoot_frames.append(pygame.Surface((70, 118)))
 
        #load run shoot frames:
        self.RunShoot_frames=[]
        for i in range(1, 9):
            try:
                img_path = os.path.join(base_path, "RunShoot", f"RunShoot ({i}).png")
                tmp = pygame.image.load(img_path)
                if i == 1: self.RunShoot_frames.append(pygame.transform.scale(tmp, (83, 118)))
                elif i == 2: self.RunShoot_frames.append(pygame.transform.scale(tmp, (87, 118)))
                elif i == 3: self.RunShoot_frames.append(pygame.transform.scale(tmp, (93, 118)))
                elif i == 4: self.RunShoot_frames.append(pygame.transform.scale(tmp, (97, 118)))
                elif i == 5: self.RunShoot_frames.append(pygame.transform.scale(tmp, (88, 118)))
                elif i == 6: self.RunShoot_frames.append(pygame.transform.scale(tmp, (90, 118)))
                elif i == 7: self.RunShoot_frames.append(pygame.transform.scale(tmp, (100, 118)))
                elif i == 8: self.RunShoot_frames.append(pygame.transform.scale(tmp, (89, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman Shoot frame 'Shoot ({i}).png' not found at {img_path}. Check path.")
                self.RunShoot_frames.append(pygame.Surface((70, 118)))
        # loading jump frames :
        self.Jump_frames=[]
        self.last_jump_time=0
        scale_numebrs=[(73,118),(80,118),(90,118),(91,118),(90,118),(109,118),(95,118),(96,118),(84,118)]
        for i in range(1,10):
            try:
                img_path = os.path.join(base_path, "jump", f"Jump ({i}).png")
                tmp = pygame.image.load(img_path)
                if i == 1: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 2: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 3: self.Jump_frames.append(pygame.transform.scale(tmp,scale_numebrs[i-1]))
                elif i == 4: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 5: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 6: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 7: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 8: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 9: self.Jump_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
            except FileNotFoundError:
                print(f"Error: Roboman jump frame 'Jump ({i}).png' not found at {img_path}. Check path.")
                self.jump_frames.append(pygame.Surface((70, 118)))
                print(img_path)
        # loading jump shoot frames :
        self.jump_shoot_animation_speed = 50 
        self.jumpshoot_flag=False
        self.JumpShoot_frames=[]
        self.JumpShoot = False
        self.last_jump_shoot_index = 0
        scale_numebrs=[(97,118),(97,118),(98,118),(95,118),(97,118)]
        for i in range(1,6):
            try:
                img_path = os.path.join(base_path, "jump shoot", f"JumpShoot ({i}).png")
                tmp = pygame.image.load(img_path)
                if i == 1: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 2: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 3: self.JumpShoot_frames.append(pygame.transform.scale(tmp,scale_numebrs[i-1]))
                elif i == 4: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
                elif i == 5: self.JumpShoot_frames.append(pygame.transform.scale(tmp, scale_numebrs[i-1]))
            except FileNotFoundError:
                print(f"Error: Roboman jump shhot frame 'JumpShoot ({i}).png' not found at {img_path}. Check path.")
                self.JumpShoot_frames.append(pygame.Surface((70, 118)))
                print(img_path)
            
            
            
 
                
        # loading bullet
        
        bullet_image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "assets", "images", "RoboMan_pictures", "Bullet.png"
        )
        try:
            self.bullet_picture = pygame.image.load(bullet_image_path).convert_alpha()
            self.bullet_picture = pygame.transform.scale(self.bullet_picture ,(35,15))
        except FileNotFoundError:
            print(f"Error: Bullet.png not found at {bullet_image_path}. Using a placeholder.")
            self.bullet_picture = pygame.Surface((40, 40), pygame.SRCALPHA)

        #====================================================================================================================================


        # Set initial picture and dimensions based on loaded frames
        self.picture = self.idle_frames[0] if self.idle_frames else pygame.Surface((70, 118))
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()

        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = horizontal_speed # Roboman specific speed
        self.vertical_speed = 0
        self.jump_strenght =jump_strenght # Roboman specific jump strength
        self.gravity_strenght = gravity_strenght
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 25
        self.max_health = 100
        self.bullets = []
        #====================================================================================================================================

        # Animation attributes
        self.current_picture = self.picture
        self.current_frame_index = 0
        self.animation_speed = 100 # Milliseconds per frame
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False
        self.last_animation_state = None # To detect changes between moving and idle

        self.is_shooting=False
        self.shooting_animation_start_time = 0
        self.shooting_animation_duration = len(self.shoot_frames) * self.animation_speed if self.shoot_frames else 1
        self.last_animation_state = None
        self.RunShoot=False
        self.Last_RunShoot_frame_index=0
        self.Reload_duration= 400 #millisec
        self.Last__Shooting_time=0  # using it for reload 
        self.frame_flag=False  #usaed in jump animation
        self.in_jump_animation = False

        
        #====================================================================================================================================
        


    def display(self, screen, offset):
        """Draws the Roboman and its health bar on the screen."""
        self.roboman_health_bar = pygame.transform.scale(self.roboman_health_bar, (int(health_bar_lenght * (self.health / self.max_health)), profileSideSize-(2*roboman_health_bar_frame_thickness)))
        self.roboman_health_bar_frame = pygame.transform.scale(self.roboman_health_bar_frame, (health_bar_lenght + (2*roboman_health_bar_frame_thickness), profileSideSize))
        display_picture = self.current_picture

        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

        screen.blit(self.roboman_health_bar_frame, (profileSideSize, 0))
        screen.blit(self.roboman_health_bar, (profileSideSize+roboman_health_bar_frame_thickness, roboman_health_bar_frame_thickness))
        screen.blit(pygame.transform.scale(self.hero_profile_picture, (profileSideSize, profileSideSize)), (0, 0))
        
        
        
        
        
        

    def update_animation(self):
        """Updates Roboman's animation frame based on current state (shooting, moving, idle)."""
        current_time = pygame.time.get_ticks()
        
        if self.JumpShoot and self.JumpShoot_frames:
            elapsed_time = current_time - self.shooting_animation_start_time
            if current_time - self.last_frame_update_time > self.jump_shoot_animation_speed:
                self.last_jump_shoot_index = (self.last_jump_shoot_index + 1) % len(self.JumpShoot_frames)
                self.current_picture = self.JumpShoot_frames[self.last_jump_shoot_index]
                self.last_frame_update_time = current_time
                if self.last_jump_shoot_index == len(self.JumpShoot_frames) - 1:
                    self.JumpShoot = False
            return
        
        if not self.on_ground and self.current_platform is None:
            if self.frame_flag:
                if current_time - self.last_frame_update_time > self.animation_speed:
                    if self.current_frame_index < 8:
                        self.current_frame_index += 1
                        self.current_picture = self.Jump_frames[self.current_frame_index]
                        self.last_frame_update_time = current_time
                    else:
                        self.frame_flag = False
                        self.current_frame_index = 8  
                        self.current_picture = self.Jump_frames[8]
            else:
                self.current_picture = self.Jump_frames[8]
            return
                 
        elif self.RunShoot:
            elapsed_time = current_time - self.shooting_animation_start_time
            if elapsed_time >= self.shooting_animation_duration:
                self.is_shooting = False
                self.RunShoot=False
                self.current_frame_index = 0
                return
            if self.is_shooting:
                if current_time - self.last_frame_update_time > self.animation_speed:
                    self.current_frame_index =(self.Last_RunShoot_frame_index + int((elapsed_time / self.animation_speed)) % len(self.RunShoot_frames))%len(self.RunShoot_frames)
                    self.current_picture = self.RunShoot_frames[self.current_frame_index]
                    self.Last_RunShoot_frame_index=self.current_frame_index
                    self.last_frame_update_time = current_time
                return
            
            
        elif self.is_shooting and self.shoot_frames:
            elapsed_time = current_time - self.shooting_animation_start_time

            if elapsed_time >= self.shooting_animation_duration:
                self.is_shooting = False
                self.current_frame_index = 0
                return

            # If shooting animation is still active, update its frames
            if self.is_shooting:
                if current_time - self.last_frame_update_time > self.animation_speed:
                    self.current_frame_index = int((elapsed_time / self.animation_speed)) % len(self.shoot_frames)
                    self.current_picture = self.shoot_frames[self.current_frame_index]
                    self.last_frame_update_time = current_time
                return

        # If not shooting, proceed with running or idle animations
        if self.is_moving_horizontally and self.run_frames:
            if self.last_animation_state != 'running':
                self.current_frame_index = 0
                self.last_frame_update_time = current_time
                self.last_animation_state = 'running'

            if current_time - self.last_frame_update_time > self.animation_speed:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.run_frames)
                self.current_picture = self.run_frames[self.current_frame_index]
                self.last_frame_update_time = current_time
        elif self.idle_frames:
            if self.last_animation_state != 'idle':
                self.current_frame_index = 0
                self.last_frame_update_time = current_time
                self.last_animation_state = 'idle'

            if current_time - self.last_frame_update_time > self.animation_speed:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
                self.current_picture = self.idle_frames[self.current_frame_index]
                self.last_frame_update_time = current_time
        else:
            print("Roboman frames didnt detected")


    def stop_horizontal_movement(self):
        """Stops horizontal movement for animation purposes."""
        self.is_moving_horizontally = False

    def fall_from_platform(self):
        """Checks if Roboman has fallen off a platform."""
        if self.current_platform is not None:
            if self.x_pos + self.width < self.current_platform.x_pos or self.x_pos > self.current_platform.x_pos + self.current_platform.width:
                self.on_ground = False
                self.current_platform = None

    def move_with_platform(self):
        """Moves Roboman along with a moving platform."""
        if self.current_platform is not None and self.current_platform.moving:
            self.horizontal_auto_speed = 2.5 * self.current_platform.direction
            self.horizontal_move()

    def move_right(self):
        """Moves Roboman to the right."""
        if self.RunShoot and self.allow_move_right:
            self.x_pos += self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

        elif self.allow_move_right and not (self.is_shooting and not self.is_moving_horizontally):
            self.x_pos += self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()


    def move_left(self):
        """Moves Roboman to the left."""
        if self.RunShoot and self.allow_move_left:
            self.x_pos -= self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()
            
        elif self.allow_move_left and not (self.is_shooting and not self.is_moving_horizontally):
            self.x_pos -= self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def shoot(self, shot_bullets, Bullet_Class):
        """Roboman shoots a bullet, with a reload cooldown."""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.Last__Shooting_time > self.Reload_duration:
            self.Last__Shooting_time = current_time 
            if not self.on_ground:
                self.jumpShoot(shot_bullets, Bullet_Class)
                return
                
                

            if self.is_moving_horizontally and self.vertical_speed == 0: 
                self.RunShoot = True 
                self.shooting_animation_start_time = pygame.time.get_ticks()
                self.current_frame_index = self.Last_RunShoot_frame_index 
            
            self.is_shooting = True 
            if not self.RunShoot:
                self.shooting_animation_start_time = pygame.time.get_ticks()
                self.current_frame_index = 0 

            bullet_start_x = self.x_pos + (self.width - 25 if self.Look == 'right' else -5)
            bullet_start_y = self.y_pos + 35
            if self.Look == 'right':
                bullet_start_x -= 5
            else:
                bullet_start_x += 5
            
            # Create and add the new bullet to the game's bullet lists
            bullet = Bullet_Class(
                bullet_start_x,
                bullet_start_y + 18, 
                15, 
                self.Look, 
                self.bullet_picture, 
                self.screen_width 
            )
            self.bullets.append(bullet) 
            shot_bullets.append(bullet) 

        
    def jumpShoot(self, shot_bullets, Bullet_Class):
        bullet_start_x = self.x_pos + (self.width - 25 if self.Look == 'right' else -5)
        bullet_start_y = self.y_pos + 35
        if self.Look == 'right':
            bullet_start_x -= 5
        else:
            bullet_start_x += 5

        bullet = Bullet_Class(
            bullet_start_x,
            bullet_start_y + 18, 
            15, 
            self.Look, 
            self.bullet_picture, 
            self.screen_width 
        )
        self.bullets.append(bullet)
        shot_bullets.append(bullet)

        # Trigger jump shoot animation
        self.JumpShoot = True
        self.shooting_animation_start_time = pygame.time.get_ticks()
        self.current_frame_index = 0

        
        
        

    def respawn(self):
        """Respawns Roboman to a default position."""
        self.current_platform = None
        self.on_ground = False
        self.x_pos = 200
        self.y_pos = 250 - self.height - 20
        self.vertical_speed = 0
        self.health = self.max_health
        
        
        
        

    def update_bullets(self, screen, shot_bullets):
        """Updates and manages bullets shot by Roboman."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen(self.screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)
                    
                    
                    
                    
                    

    def jump(self):
        """Makes Roboman jump if on the ground."""
        if self.on_ground :
            self.vertical_speed = self.jump_strenght
            self.on_ground = False
            self.current_platform = None
            self.last_jump_time=pygame.time.get_ticks()
            self.current_frame_index = 0 
            self.frame_flag=True
            self.in_jump_animation = True 
            self.allow_move_left=True
            self.allow_move_right=True
            
            
            
            
            
            

    def gravity(self):
        """Applies gravity to Roboman."""
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght
            
            
            
            
            

    def is_on_ground(self):
        """Checks if Roboman is currently on a platform."""
        if self.current_platform:
            self.on_ground = True
        elif self.current_platform is None and self.vertical_speed <= 0:
            self.on_ground = False
            
            
            
            
            

    def vertical_move(self):
        """Updates Roboman's vertical position based on vertical speed."""
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)
        
        
        
        
        

    def horizontal_move(self):
        """Applies auto horizontal movement (e.g., from moving platforms)."""
        self.x_pos += self.horizontal_auto_speed
        self.horizontal_auto_speed = 0
        
        
        
        

    def platforms_collisions(self, platforms):
        """Handles collisions between Roboman and platforms."""
        for platform in platforms:
            # Check for collision with the top of the platform (landing)
            if self.x_pos + self.width > platform.x_pos + ROBOMAN_LANDING_INSET and \
   self.x_pos + ROBOMAN_LANDING_INSET < platform.x_pos + platform.width:
                if (self.y_pos + self.height) > platform.y_pos and \
                   (self.y_pos + self.height) < (platform.y_pos + platform.height) + ROBOMAN_SIDE_COLLISION_BOTTOM_BUFFER:
                    if self.vertical_speed <= 0:
                        self.on_ground = True
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos - self.height
                        self.current_platform = platform
                        
                        
            # Check for side collisions with platforms
            if self.hitbox.colliderect(platform.rect):
                # If colliding from the left side of the platform
                if self.allow_move_right and self.x_pos < platform.x_pos and \
                   self.hitbox.right > platform.rect.left and \
                   self.hitbox.bottom > platform.rect.top + ROBOMAN_SIDE_COLLISION_TOP_BUFFER and \
                 self.hitbox.top < platform.rect.bottom - ROBOMAN_SIDE_COLLISION_BOTTOM_BUFFER: # Small buffer for top/bottom
                    self.allow_move_right = False
                    self.x_pos = platform.x_pos - self.width
                # If colliding from the right side of the platform
                elif self.allow_move_left and self.x_pos + self.width > platform.x_pos + platform.width and \
                     self.hitbox.left < platform.rect.right and \
                     self.hitbox.bottom > platform.rect.top + ROBOMAN_SIDE_COLLISION_TOP_BUFFER and \
                     self.hitbox.top < platform.rect.bottom - ROBOMAN_SIDE_COLLISION_BOTTOM_BUFFER: # Small buffer for top/bottom
                    self.allow_move_left = False
                    self.x_pos = platform.x_pos + platform.width
            # Reset allow_move flags if not colliding horizontally
            else:
                self.allow_move_left = True
                self.allow_move_right = True
                
                
                
                


    def jump_under_platform(self, platforms):
        """Prevents Roboman from jumping through platforms from below."""
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and \
                   self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and \
                       self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height
