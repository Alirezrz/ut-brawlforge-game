import pygame
import os
from src.engine.bullet import Bullet
from config import Ninja_width, Ninja_height

class Ninja:
    def __init__(self, x, y, screen_width, screen_height):
        self.x_pos = x
        self.y_pos = y
        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.width = Ninja_width
        self.height = Ninja_height

        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 63
        self.max_health = 100
        self.bullets = []
        self.last_shot_time = 0
        self.shot_cooldown = 300
        self.throwing_until = 0
        self.kunai_fired = False
        self.throw_flag=False

        # Animation attributes
        self.status = "Idle"
        self.last_animation_state = 'idle'
        self.current_frame_index = 0
        self.animation_speed = 100
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False
        self.last_doubleJump=0
        self.double_jump_rest_time=400
        self.jump_count = 0
        self.Allow_double_jump=True
        self.AllowJump_flag=True
        
        
        
        

        
        #Super power attributes:
        self.Super_cofficent=1
        self.Super_duration=5000
        self.Super_lastActivation=0
        self.SuperPower_CoolDown=100
        self.SuperPower_pic_display_duratiom=1500
        self.last_SPdisplay=0
        self.Super_PowerFlag=False
        
        self.shutter_overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.shutter_alpha = 0
        self.shutter_direction = 1 
        
        
        
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Ninja")

        # Load Idle image for default state
        tmp = pygame.image.load(os.path.join(base_path, "Idle", f"Idle__000.png"))
        self.current_picture = pygame.transform.scale(tmp, (62, 118))
        
        
        
        img_path = os.path.join(base_path, "SuperPower effect.png")
        self.SuperPower_pic=pygame.image.load(img_path )
        self.SuperPower_pic=pygame.transform.scale(self.SuperPower_pic,(100,118))

        # Load Idle frames
        self.idle_frames = []
        for i in range(0, 10): 
            img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.idle_frames.append(pygame.transform.scale(tmp, (62, 118)))

        # Load Run frames
        self.run_frames = []
        for i in range(1, 10):
            img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.run_frames.append(pygame.transform.scale(tmp, (94, 118)))
            
        # Load Jump frames
        self.jump_frames = []
        sizes = [77, 69, 69, 71, 70, 70, 77, 84, 95, 93]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.jump_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
        

        # Load Kunai
        img_path = os.path.join(base_path, "Kunai.png")
        self.Kunai_pic = pygame.image.load(img_path)
        self.Kunai_pic = pygame.transform.scale(self.Kunai_pic, (60, 12))
        
        img_path = os.path.join(base_path, "FiredKunai.png") 
        self.Fired_kunai_pic=pygame.image.load(img_path)
        self.Fired_kunai_pic= pygame.transform.scale(self.Fired_kunai_pic, (70, 24))
        
        self.Kunai=self.Kunai_pic

        # Load Throw frames
        self.throw_frames = []
        throw_widths = [72, 66, 83, 81, 79, 79, 78, 86, 78, 66]
        for i in range(10):
            img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
            tmp = pygame.image.load(img_path)
            scaled = pygame.transform.scale(tmp, (throw_widths[i], 118))
            self.throw_frames.append(scaled)
        # Load Jump throw frames
        self.jumpThrow_frames = []
        sizes = [85,88,92,99,101,104,103,96,89,89]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.jumpThrow_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
            
            
        

    def display(self, screen, offset):
        self.Update_SuperPower() 
        self.Super_Power_effect()
           
        
        
    
        display_picture = self.current_picture
        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def update_animation(self, shot_bullets):
        
        current_time = pygame.time.get_ticks()
        if self.Super_PowerFlag:
            self.current_picture=self.SuperPower_pic
            print("here")
            return
        # Determine animation state
        if not self.on_ground and self.current_platform is None:
            if self.status == "jump_throw":
                target_animation_state = 'jump_throw'
            elif self.status == "throw":
                target_animation_state = 'jump_throw'  # fallback for air
            else:
                target_animation_state = 'jump'
        elif self.status == "throw":
            target_animation_state = 'throw'
        else:
            target_animation_state = 'running' if self.is_moving_horizontally else 'idle'
            

        # Handle animation transition
        if target_animation_state != self.last_animation_state:
            self.current_frame_index = 0
            self.last_frame_update_time = current_time
            self.last_animation_state = target_animation_state
            self.kunai_fired = False

        # Frame update
        elapsed_time = current_time - self.last_frame_update_time
        if elapsed_time < self.animation_speed:
            return

        if target_animation_state == 'jump_throw':
            target_animation_state='jump'
            
            if self.current_frame_index < len(self.jumpThrow_frames):
                self.current_picture = self.jumpThrow_frames[self.current_frame_index]
                if self.current_frame_index == 2 and not self.kunai_fired:
                    self.fire_kunai(shot_bullets)
                    self.kunai_fired = True
                self.current_frame_index += 1
            
                
            else:
                self.status = "Idle"
                self.last_animation_state = "jump"
                self.current_frame_index = 0

        elif target_animation_state == 'jump':
            if self.current_frame_index < len(self.jump_frames):
                self.current_picture = self.jump_frames[self.current_frame_index]
                self.current_frame_index += 1

        elif target_animation_state == 'throw':
            if self.current_frame_index < len(self.throw_frames):
                self.current_picture = self.throw_frames[self.current_frame_index]
                if self.current_frame_index == 3 and not self.kunai_fired:
                    self.fire_kunai(shot_bullets)
                    self.kunai_fired = True
                self.current_frame_index += 1
                if self.current_frame_index==len(self.throw_frames)-1:
                    self.allow_move_left=True
                    self.allow_move_right=True
            else:
                self.status = "Idle"
                self.last_animation_state = "idle"
                self.current_frame_index = 0

        elif target_animation_state == 'running':
            self.current_frame_index = (self.current_frame_index + 1) % len(self.run_frames)
            self.current_picture = self.run_frames[self.current_frame_index]

        elif target_animation_state == 'idle':
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
            self.current_picture = self.idle_frames[self.current_frame_index]

        self.last_frame_update_time = current_time

    def fire_kunai(self, shot_bullets):
        bullet_x = self.x_pos + (self.width if self.Look == 'right' else -self.Kunai_pic.get_width())
        bullet_y = self.y_pos + self.height // 2 - self.Kunai_pic.get_height() // 2
        if self.Look == 'right':
            bullet_x -= 20
        else:
            bullet_x += 20

        bullet = Bullet(
        bullet_x,
        bullet_y,
        15,
        self.Look,
        self.Kunai,
        self.screen_width
        )

        self.bullets.append(bullet)
        shot_bullets.append(bullet)
        self.status='jump'
        

    def shoot(self, shot_bullets, Bullet):
        current_time = pygame.time.get_ticks()
        if self.on_ground and self.current_platform!=None:
            if self.status == "throw" and current_time < self.throwing_until:
                return

            if current_time - self.last_shot_time < self.shot_cooldown:
                return
        
            self.throw_flag=True
            self.last_shot_time = current_time
            self.allow_move_left=False
            self.allow_move_right=False
            self.status = "throw"
            self.throwing_until = current_time + (len(self.throw_frames) * self.animation_speed)
            self.kunai_fired = False 
        else:
            self.jump_throw()
            
    def jump_throw(self):
        """Triggers a throwing animation in mid-air (jump_throw) if allowed."""
        current_time = pygame.time.get_ticks()

        # Prevent interrupting an ongoing air-throw or a repeat bug
        if self.status == "jump_throw" and current_time < self.throwing_until:
            return

        # Use doubled cooldown for jump_throw
        if current_time - self.last_shot_time < self.shot_cooldown * 2:
            return

        # Mark as air-throwing
        self.throw_flag = True
        self.last_shot_time = current_time
        self.status = "jump_throw"
        self.throwing_until = current_time + (len(self.jumpThrow_frames) * self.animation_speed)
        self.kunai_fired = False

    def stop_horizontal_movement(self):
        self.is_moving_horizontally = False
        
    def fall_from_platform(self):
        if self.current_platform:
            if self.x_pos + self.width < self.current_platform.x_pos or self.x_pos > self.current_platform.x_pos + self.current_platform.width:
                self.on_ground = False
                self.current_platform = None

    def move_with_platform(self):
        if self.current_platform and self.current_platform.moving:
            self.horizontal_auto_speed = 2.5 * self.current_platform.direction
            self.horizontal_move()

    def move_right(self):
        if self.allow_move_right and self.status not in ["throw"]:
            self.x_pos += self.horizontal_speed*self.Super_cofficent
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        if self.allow_move_left  and self.status not in ["throw"]:
            self.x_pos -= self.horizontal_speed*self.Super_cofficent
            self.is_moving_horizontally = True
            self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def respawn(self):
        self.current_platform = None
        self.on_ground = False
        self.x_pos = 200
        self.y_pos = 250 - self.current_picture.get_height() - 20
        self.vertical_speed = 0

    def update_bullets(self, screen, shot_bullets):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen(self.screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)

    def jump(self):
        if self.on_ground and self.current_platform!=None and self.AllowJump_flag:
                self.vertical_speed = self.jump_strenght*self.Super_cofficent
                self.jump_count = 1
                return
        elif self.Allow_double_jump:
            self.double_jump()
            
       
        self.on_ground = False
        self.current_platform = None
        
    def double_jump(self):
        current_time = pygame.time.get_ticks()
        self.vertical_speed = self.jump_strenght*self.Super_cofficent
        self.on_ground = False
        self.current_platform = None
        self.current_frame_index=1
        self.last_doubleJump=current_time
        self.Allow_double_jump=False
    

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def is_on_ground(self):
        self.on_ground = bool(self.current_platform)

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def horizontal_move(self):
        self.x_pos += self.horizontal_auto_speed
        self.horizontal_auto_speed = 0

    def platforms_collisions(self, platforms):
     # Reset movement permissions and landing status
     self.allow_move_left = True
     self.allow_move_right = True
     landed = False
    
     for platform in platforms:
         if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
             # Landing on top of platform
             if ((self.y_pos + self.height) >= platform.y_pos) and \
                ((self.y_pos + self.height) < (platform.y_pos + platform.height) + 10) and \
                self.vertical_speed <= 0:  # Only land if moving downward
                
                 self.on_ground = True
                 self.vertical_speed = 0
                 self.y_pos = platform.y_pos - self.height
                 self.current_platform = platform
                 landed = True
                
            # Side collisions (left/right of platform)
             elif ((self.y_pos + self.height) > platform.y_pos) and \
                  (self.y_pos < platform.y_pos + platform.height):
                
                # Left side collision
                 if abs(self.x_pos - (platform.x_pos + platform.width)) <= 10:
                     self.allow_move_left = False
                     self.x_pos = platform.x_pos + platform.width
                
                # Right side collision
                 elif abs(self.x_pos + self.width - platform.x_pos) <= 10:
                     self.allow_move_right = False
                     self.x_pos = platform.x_pos - self.width
    
    # Reset jump count if landed on any platform
     if landed:
         self.jump_count = 0
         self.on_ground = True
         self.Allow_double_jump = True
     else:
        # Only set on_ground to False if not on any platform
         if not any(platform.x_pos <= self.x_pos + self.width and 
                   platform.x_pos + platform.width >= self.x_pos and
                   abs((self.y_pos + self.height) - platform.y_pos) < 5 
                   for platform in platforms):
             self.on_ground = False

    def jump_under_platform(self, platforms):
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height
                        
                        
                        
    def Activate_Super_Power(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.Super_lastActivation>=self.SuperPower_CoolDown:
            self.Super_cofficent=2
            self.Super_lastActivation = current_time
            self.last_SPdisplay=current_time
            self.Super_PowerFlag=True
            self.Kunai=self.Fired_kunai_pic
            print("active")
            
    def Update_SuperPower(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.Super_lastActivation>self.Super_duration and self.current_platform!=None:
            self.Super_cofficent=1
            self.Kunai=self.Kunai_pic
            
            
            
            
    def Super_Power_effect(self):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_SPdisplay < self.SuperPower_pic_display_duratiom:
            self.allow_move_left=False
            self.allow_move_right=False
            self.vertical_speed=0
            self.AllowJump_flag=False
            
            self.shutter_alpha += self.shutter_direction * 10
            if self.shutter_alpha >= 100:
                self.shutter_alpha = 100
                self.shutter_direction = -1
            elif self.shutter_alpha <= 0:
                self.shutter_alpha = 0
                self.shutter_direction = 1
        else:
            self.allow_move_left=True
            self.allow_move_right=True
            self.Super_PowerFlag=False
            self.AllowJump_flag=True
            
            
        