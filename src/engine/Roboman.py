import pygame
import os

class Roboman:

    def __init__(self, x, y, health_bar_green, health_bar_red, hero_profile_picture, screen_width, screen_height):

        self.x_pos = x
        self.y_pos = y
        self.hero_profile_picture = hero_profile_picture
        self.health_bar_green = health_bar_green
        self.health_bar_red = health_bar_red
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
                
        # loading bullet
        
        bullet_image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "assets", "images", "RoboMan_pictures", "Bullet.png"
        )
        try:
            self.bullet_picture = pygame.image.load(bullet_image_path).convert_alpha()
            self.bullet_picture = pygame.transform.scale(self.bullet_picture ,(23,23))
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
        self.horizontal_speed = 8 # Roboman specific speed
        self.vertical_speed = 0
        self.jump_strenght = 22 # Roboman specific jump strength
        self.gravity_strenght = 1
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 63
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
        #====================================================================================================================================
        


    def display(self, screen, offset):
        """Draws the Roboman and its health bar on the screen."""
        self.health_bar_green = pygame.transform.scale(self.health_bar_green, (int(300 * (self.health / self.max_health)), 35))
        self.health_bar_red = pygame.transform.scale(self.health_bar_red, (300, 35))
        display_picture = self.current_picture

        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

        screen.blit(self.health_bar_red, (35, 0))
        screen.blit(self.health_bar_green, (35, 0))
        screen.blit(pygame.transform.scale(self.hero_profile_picture, (35, 35)), (0, 0))
        
        
        
        
        
        

    def update_animation(self):
        """Updates Roboman's animation frame based on current state (shooting, moving, idle)."""
        current_time = pygame.time.get_ticks()

        # Prioritize shooting animation if active
        if self.is_shooting and self.shoot_frames:
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
        if self.allow_move_right:
            self.x_pos += self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        """Moves Roboman to the left."""
        if self.allow_move_left:
            self.x_pos -= self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def shoot(self, shot_bullets, Bullet_Class):
        """Roboman shoots a bullet."""
        bullet_start_x = self.x_pos + (self.width - 25 if self.Look == 'right' else -5)
        bullet_start_y = self.y_pos + 35
        if self.Look=='right' :
            bullet_start_x-=5
        else:
            bullet_start_x+=5
        bullet = Bullet_Class(
            bullet_start_x,
            bullet_start_y+10,
            15, # Bullet speed
            self.Look,
            self.bullet_picture, 
            self.screen_width
        )
        self.bullets.append(bullet)
        shot_bullets.append(bullet)

        # Trigger shooting animation
        self.is_shooting = True
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
        if self.on_ground:
            self.vertical_speed = self.jump_strenght
            self.on_ground = False
            self.current_platform = None
            
            
            
            
            
            

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
            if self.x_pos + self.width > platform.x_pos+20 and \
               self.x_pos+20 < platform.x_pos + platform.width:
                if (self.y_pos + self.height) > platform.y_pos and \
                   (self.y_pos + self.height) < (platform.y_pos + platform.height) + 10:
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
                   self.hitbox.bottom > platform.rect.top + 30 and \
                   self.hitbox.top < platform.rect.bottom - 30: # Small buffer for top/bottom
                    self.allow_move_right = False
                    self.x_pos = platform.x_pos - self.width
                # If colliding from the right side of the platform
                elif self.allow_move_left and self.x_pos + self.width > platform.x_pos + platform.width and \
                     self.hitbox.left < platform.rect.right and \
                     self.hitbox.bottom > platform.rect.top + 30 and \
                     self.hitbox.top < platform.rect.bottom - 30: # Small buffer for top/bottom
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
