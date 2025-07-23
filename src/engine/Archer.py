import os
import pygame
from config import screen_width,screen_height,profileSideSize,health_bar_lenght,roboman_health_bar_frame_thickness

from src.engine.protector import Guard_Drone
from src.engine.bullet import Bullet

class Archer:
    def __init__(self, x, y, targets,index=3):
        self.hero_creation_index=index
        self.x_pos = x
        self.y_pos = y
        self.screen_height=screen_height
        self.screen_width=screen_width
        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 25
        self.gravity_strenght = 1
        self.on_ground = False
        self.jump_count = 0
        self.last_jump_time = 0
        self.jump_cooldown = 250
        self.double_jump_allowed = True
        self.has_defuse_kit=False
        self.jump_sound= pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "Archer", "jump.MP3"))
        self.shoot_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "Archer", "shoot.mp3"))
        self.melee_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "Archer", "melee.mp3"))
        self.DEAD=False
        self.ALIVE=True
        self.health_bar_frame =pygame.image.load("src/assets/images/Archer/health_bar_frame.png")
        self.health_bar = pygame.image.load("src/assets/images/Archer/health_bar.png")

        self.health=100
        self.targets = targets
        self.profile_picture = pygame.image.load("src/assets/images/Archer/profile.png")
        self.width = 88
        self.height = 100
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.hurt_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "archer", "archer hurt.mp3"))     
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.status = 'idle'
        self.freezed=False
        self.last_freezed=0
        self.current_frame_index = 0
        self.animation_speed = 80
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False
        self.is_first_time = True
        self.shooting = False
        self.shot_triggered = False

        self.guard_drone_reload_duration = 10000
        self.last_guard_call = 0
        self.guard_drone = []
        self.drone_duration = 20000
        self.HIT_COUNTER=0
        # Super Power Attributes
        self.super_power_active = False
        self.super_power_duration = 15000
        self.super_power_cooldown = 10000
        self.super_power_last_activation = -self.super_power_cooldown
        self.super_power_pic_display_duration = 1500
        self.super_power_display_start = 0

        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Archer")

        self.idle_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "idle", f"{i}.png")), (88, 100)) for i in range(6)]
        sizes = [89, 90, 91, 90, 89, 90, 96, 90]
        self.run_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "run", f"{i}.png")), (sizes[i], 100)) for i in range(8)]
        sizes = [91, 93, 88, 90, 94, 89, 88, 90]
        self.jump_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "jump", f"{i}.png")), (sizes[i], 100)) for i in range(8)]
        sizes = [90, 72, 72, 72, 72, 72, 97, 113, 106, 89, 77, 72, 70]
        self.shot_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "shot", f"{i}.png")), (sizes[i], 100)) for i in range(13)]
        self.arrow_pic = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "Arrow.png")), (30, 2))
        self.firedarrow_pic = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "fired arrow.png")), (30, 8))
        self.freezed_img=pygame.transform.scale(pygame.image.load(os.path.join(base_path, "freezed.png")), (88, 100))
        sizes = [78, 60, 132, 62]
        self.attack_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, "attack", f"{i}.png")), (sizes[i], 100)) for i in range(4)]

        self.super_power_effect_picture = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "super power effect.png")), (88, 127))
        sizes=[(98,100),(102,100),(150,43)]
        self.death_frames=[pygame.transform.scale(pygame.image.load(os.path.join(base_path, "death", f"{i}.png")), sizes[i]) for i in range(3)]
        
        self.current_picture = self.idle_frames[0]
        
        self.SUPER_POWER_FLAG=False
        self.GUARD_DRONE_FLAG=False
        self.DOUBLE_JUMP_FLAG=False
        
        
    def hurt(self):
        self.hurt_sound.play()
        if self.health <= 0:
            self.die()

    def display(self, screen, offset, shot_bullets):
        if self.health<0:
            self.health=0
        self.health_bar = pygame.transform.scale(
            self.health_bar, 
            (int(health_bar_lenght * (self.health / self.max_health)), profileSideSize - (2 * roboman_health_bar_frame_thickness))
        )
        self.health_bar_frame = pygame.transform.scale(
            self.health_bar_frame, 
            (health_bar_lenght + (2 * roboman_health_bar_frame_thickness), profileSideSize)
        )
        display_picture = self.current_picture

        # موقعیت health bar و profile بر اساس hero_creation_index
        if self.hero_creation_index == 1:  # بالا چپ
            bar_x, bar_y = profileSideSize, 0
            health_x, health_y = profileSideSize + roboman_health_bar_frame_thickness, roboman_health_bar_frame_thickness
            profile_x, profile_y = 0, 0
        elif self.hero_creation_index == 2:  # بالا راست
            if self.is_first_time:
                self.hero_profile_picture = pygame.transform.flip(self.profile_picture, True, False)
                self.is_first_time=False            
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            bar_y = 0
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = roboman_health_bar_frame_thickness
            profile_x = self.screen_width - profileSideSize
            profile_y = 0
        elif self.hero_creation_index == 3:  # پایین چپ
            bar_x = profileSideSize
            bar_y = self.screen_height - profileSideSize
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = bar_y + roboman_health_bar_frame_thickness
            profile_x = 0
            profile_y = self.screen_height - profileSideSize
        elif self.hero_creation_index == 4:  # پایین راست
            if self.is_first_time:
                self.hero_profile_picture = pygame.transform.flip(self.hero_profile_picture, True, False)
                self.is_first_time=False   
            self.hero_profile_picture = pygame.transform.flip(self.hero_profile_picture, True, False)
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            bar_y = self.screen_height - profileSideSize
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = bar_y + roboman_health_bar_frame_thickness
            profile_x = self.screen_width - profileSideSize
            profile_y = self.screen_height - profileSideSize
        else:  # دیفالت بالا چپ
            bar_x, bar_y = profileSideSize, 0
            health_x, health_y = profileSideSize + roboman_health_bar_frame_thickness, roboman_health_bar_frame_thickness
            profile_x, profile_y = 0, 0

        screen.blit(self.health_bar_frame, (bar_x, bar_y))
        screen.blit(self.health_bar, (health_x, health_y))
        screen.blit(pygame.transform.scale(self.profile_picture, (profileSideSize, profileSideSize)), (profile_x, profile_y))

        self.update_super_power()  
        for arrow in self.bullets:
            arrow.update()
            arrow.draw(screen, offset)
        y=self.y_pos
        
        if self.super_power_active and pygame.time.get_ticks() - self.super_power_display_start < self.super_power_pic_display_duration:
            display_picture = self.super_power_effect_picture
            y-=27
        else:
            display_picture = self.current_picture or self.idle_frames[0]

        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], y - offset[1]))
        else:
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], y - offset[1]))

        for drone in self.guard_drone:
            drone.Update(screen, offset, shot_bullets)


        self.update_drone()
            
            


    def attack(self, targets):
        if self.status == 'shot' or self.shooting:
            return  

        self.status = 'attack'
        self.current_frame_index = 0
        self.attack_triggered = False
        self.melee_sound.play()
        self.shooting = True  
        self.HIT_PER_ATTACK=0
        self.HIT_COUNTER=0
        
    def update_animation(self, shot_bullets=None):
        if hasattr(self, 'DEAD') and self.DEAD:
            self.vertical_speed -= self.gravity_strenght
            self.y_pos -= self.vertical_speed
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.current_picture = self.death_frames[-1]
            return

        current_time = pygame.time.get_ticks()

        if hasattr(self, 'ALIVE') and not self.ALIVE and self.status == 'dead':
            if self.current_frame_index < len(self.death_frames):
                self.current_picture = self.death_frames[self.current_frame_index]
                new_width, new_height = self.current_picture.get_size()
                if self.current_frame_index == 0:
                    self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
                self.x_pos = self.previous_center[0] - new_width // 2
                self.y_pos = self.previous_center[1] - new_height
                self.hitbox = pygame.Rect(self.x_pos, self.y_pos, new_width, new_height)

                if current_time - self.last_frame_update_time > self.animation_speed * 2:
                    self.current_frame_index += 1
                    self.last_frame_update_time = current_time
            else:
                self.current_picture = self.death_frames[-1]
                self.DEAD = True

            
            return

        if self.freezed:
            self.current_picture = self.freezed_img
            return

        speed = self.animation_speed if self.status != 'shot' else self.animation_speed - 50
        current_time = pygame.time.get_ticks()
        if not hasattr(self, 'last_status'):
            self.last_status = self.status

        if current_time - self.last_frame_update_time >= speed:
            self.last_frame_update_time = current_time

            if self.status != 'shot' and self.status != 'attack':
                if not self.on_ground:
                    self.status = 'jump'
                elif self.is_moving_horizontally:
                    self.status = 'run'
                else:
                    self.status = 'idle'

            if self.status != self.last_status:
                self.current_frame_index = 0
                self.last_status = self.status

            if self.status == 'idle':
                self.current_picture = self.idle_frames[self.current_frame_index % len(self.idle_frames)]
            elif self.status == 'run':
                self.current_picture = self.run_frames[self.current_frame_index % len(self.run_frames)]
            elif self.status == 'jump':
                self.current_picture = self.jump_frames[self.current_frame_index % len(self.jump_frames)]
            elif self.status == 'shot':
                self.current_picture = self.shot_frames[self.current_frame_index % len(self.shot_frames)]
                if self.current_frame_index == 11 and not self.shot_triggered:
                    self.shoot_arrow(shot_bullets)
                    self.shot_triggered = True
                if self.current_frame_index >= len(self.shot_frames) - 1:
                    self.status = 'idle'
                    self.shooting = False
                    self.shot_triggered = False
            elif self.status == 'attack':
                if self.current_frame_index == 0:
                    self.damaged_targets = set()

                self.current_picture = self.attack_frames[self.current_frame_index % len(self.attack_frames)]

                self.damage_nearby_targets()
                self.melee_sound.play()
                if self.current_frame_index >= len(self.attack_frames) - 1:
                    self.status = 'idle'
                    self.shooting = False

            self.current_frame_index += 1
            self.update_attack()
            if self.status=='attack':
                for target in self.targets:
                    if target.hitbox.colliderect(self.hitbox) and self.HIT_COUNTER==0:
                        target.health-=30
                        target.hurt()
                        self.HIT_COUNTER+=1
                        print('hit')
                        
                        
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.current_picture.get_width(),self.current_picture.get_height())
    def damage_nearby_targets(self):
        
        for target in self.targets:
            if hasattr(target, 'hitbox') and self.hitbox.colliderect(target.hitbox):
                target.health -= 50
                target.hurt()

    def shoot_arrow(self, shot_bullets):
        arrow_x = self.x_pos + (self.width if self.Look == 'right' else -30)
        arrow_y = self.y_pos + self.height // 2
        direction = self.Look
        arrow_image = self.firedarrow_pic if self.super_power_active else self.arrow_pic
        damage = 35 if self.super_power_active else 25
        new_arrow = Arrow(arrow_x, arrow_y, direction, arrow_image, damage)
        self.shoot_sound.play()
        self.bullets.append(new_arrow)
        shot_bullets.append(new_arrow)
        
    def activate_super_power(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.super_power_last_activation >= self.super_power_cooldown and self.SUPER_POWER_FLAG:
            self.super_power_active = True
            self.super_power_last_activation = current_time
            self.super_power_display_start = current_time
    def update_super_power(self):
        current_time = pygame.time.get_ticks()
        if self.super_power_active and current_time - self.super_power_last_activation > self.super_power_duration:
            self.super_power_active = False

    def handle_input(self, keys,gates,shot_bullets,bullet_class,trigger_shutter,mouse_bottons):
        if self.DEAD:
            return
        if self.freezed:
            return
        self.is_moving_horizontally = False
        if self.hero_creation_index==1:
            if keys[pygame.K_a] and self.status not in ('shot', 'attack'):
                self.move_left()
                self.is_moving_horizontally = True
            if keys[pygame.K_d] and self.status not in ('shot', 'attack'):
                self.move_right()
                self.is_moving_horizontally = True
            if keys[pygame.K_w]:
                self.jump()

            if mouse_bottons[0] and not self.shooting and self.status != 'attack':
                self.shooting = True
                self.status = 'shot'
                self.current_frame_index = 0
                self.shot_triggered = False

            if mouse_bottons[2] and self.status not in ('attack', 'shot'):
                self.status = 'attack'
                self.current_frame_index = 0
                self.attack_triggered = False
                self.attack_targets = self.targets

            if keys[pygame.K_g]:
                self.call_drone()

            if keys[pygame.K_LSHIFT]:
                self.activate_super_power()
                
            if keys[pygame.K_TAB]:
                self.Send_teleport_request(gates)
        if self.hero_creation_index==2:
            if keys[pygame.K_LEFT] and self.status not in ('shot', 'attack'):
                self.move_left()
                self.is_moving_horizontally = True
            if keys[pygame.K_RIGHT] and self.status not in ('shot', 'attack'):
                self.move_right()
                self.is_moving_horizontally = True
            if keys[pygame.K_UP]:
                self.jump()

            if keys[pygame.K_RCTRL] and not self.shooting and self.status != 'attack':
                self.shooting = True
                self.status = 'shot'
                self.current_frame_index = 0
                self.shot_triggered = False

            if keys[pygame.K_RALT] and self.status not in ('attack', 'shot'):
                self.status = 'attack'
                self.current_frame_index = 0
                self.attack_triggered = False
                self.attack_targets = self.targets

            if keys[pygame.K_SLASH]:
                self.call_drone()

            if keys[pygame.K_RSHIFT]:
                self.activate_super_power()
                
            if keys[pygame.K_RETURN]:
                self.Send_teleport_request(gates)

        if not self.is_moving_horizontally:
            self.stop_horizontal_movement()

    def update_bullets(self, screen, global_bullet_list, platforms, targets):
        
        for arrow in self.bullets[:]:
            if arrow not in global_bullet_list:
                if arrow in self.bullets:
                    self.bullets.remove(arrow)
            arrow.update()



            for target in targets:
                if hasattr(target, 'hitbox') and arrow.hitbox.colliderect(target.hitbox):
                    target.health -= arrow.damage
                    target.hurt()
                    if arrow in self.bullets:
                        self.bullets.remove(arrow)
                    if arrow in global_bullet_list:
                        global_bullet_list.remove(arrow)
                    break

            for platform in platforms:
                if arrow.hitbox.colliderect(platform.rect):
                    if arrow in self.bullets:
                        self.bullets.remove(arrow)
                    if arrow in global_bullet_list:
                        global_bullet_list.remove(arrow)
                    break





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
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.horizontal_move()

    def move_right(self):
        if self.allow_move_right:
            self.x_pos += self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self):
        if self.allow_move_left:
            self.x_pos -= self.horizontal_speed
            self.is_moving_horizontally = True
            self.Look = 'left'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def jump(self):
     current_time = pygame.time.get_ticks()
     if self.status!='shot':
        if current_time - self.last_jump_time < self.jump_cooldown :
            return

        if self.on_ground:
            self.jump_sound.play()
            self.vertical_speed = self.jump_strenght
            self.jump_count = 1
            self.on_ground = False
            self.current_platform = None
            self.last_jump_time = current_time
        elif self.jump_count == 1 and self.double_jump_allowed and self.DOUBLE_JUMP_FLAG:
            self.jump_sound.play()
            self.vertical_speed = self.jump_strenght
            self.jump_count = 2
            self.double_jump_allowed = False
            self.last_jump_time = current_time

    def gravity(self):
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def horizontal_move(self):
        self.x_pos += self.horizontal_auto_speed
        self.horizontal_auto_speed = 0

    def platforms_collisions(self, platforms):
        self.allow_move_left = True
        self.allow_move_right = True
        landed = False

        for platform in platforms:
         if self.x_pos + self.width > platform.x_pos+15 and self.x_pos+15 < platform.x_pos + platform.width:
             # Landing on top of platform
             if ((self.y_pos + self.height) >= platform.y_pos) and \
                ((self.y_pos + self.height) < (platform.y_pos + platform.height) + 10) and \
                self.vertical_speed <= 0:  # Only land if moving downward
                
                 self.on_ground = True
                 self.vertical_speed = 0
                 self.y_pos = platform.y_pos - self.height
                 self.current_platform = platform
                 landed = True
         if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:

            # Side collisions (left/right of platform)
             if ((self.y_pos + self.height) > platform.y_pos) and \
                  (self.y_pos < platform.y_pos + platform.height):
                
                # Left side collision
                 if abs(self.x_pos - (platform.x_pos + platform.width)) <= 15:
                     self.allow_move_left = False
                     self.x_pos = platform.x_pos + platform.width
                
                # Right side collision
                 elif abs(self.x_pos + self.width - platform.x_pos) <= 15:
                     self.allow_move_right = False
                     self.x_pos = platform.x_pos - self.width
    
        if landed:
            self.on_ground = True
            self.jump_count = 0
            self.double_jump_allowed = True
        else:
            self.on_ground = False

    def jump_under_platform(self, platforms):
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height

    def is_on_ground(self):
        self.on_ground = bool(self.current_platform)
        
    def call_drone(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_guard_call >= self.guard_drone_reload_duration and self.GUARD_DRONE_FLAG:
            self.guard_drone.append(Guard_Drone(self, "Archer")) 
            self.last_guard_call = current_time
            
            
    def update_drone(self):
        if len(self.guard_drone) == 1:
            current_time = pygame.time.get_ticks()
            drone = self.guard_drone[0]
            if current_time - self.last_guard_call >= self.drone_duration:
                if drone.status != 'departing':
                    drone.status = 'departing'
            if drone.status == 'departing' and drone.departed_len>3000:
                self.guard_drone.remove(drone)
                
    def update(self,platforms,shot_bullets,targets,keys,gate,trigger_shutter=None):
        if self.y_pos>1000:
            self.health=0
        self.is_on_ground()
        self.vertical_move()
        self.platforms_collisions(platforms)
        self.move_with_platform()
        self.jump_under_platform(platforms)
        self.update_animation()
        self.update_bullets(shot_bullets,targets)
        self.handle_input(keys, gate, shot_bullets, Bullet, trigger_shutter=None)
        self.update_drone()
        self.update_attack()

    def update_attack(self):
     if self.status=='attack' or self.status=='jumpattack':
        for t in self.attack_targets:
            if self.hitbox.colliderect(t.hitbox):
                if self.Look=='right' and self.x_pos < t.x_pos and self.HIT_PER_ATTACK==0:
                    t.health-=50
                    self.HIT_PER_ATTACK=1                   
                elif self.Look=='left' and self.x_pos > t.x_pos and self.HIT_PER_ATTACK==0:
                    t.health-=50                    
                    self.HIT_PER_ATTACK=1
        
    def Send_teleport_request(self,Gates):
        for Gate in Gates:
            Gate.recieve_request(self)
            
    def die(self):
        if hasattr(self, 'DEAD') and self.DEAD:
            return

        self.ALIVE = False
        self.DEAD = False  # will become True when animation finishes
        self.status = 'dead'
        self.current_frame_index = 0
        self.vertical_speed = 0
        self.on_ground = True
        self.allow_move_left = False
        self.allow_move_right = False
        self.AllowJump_flag = False if hasattr(self, 'AllowJump_flag') else None
        self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
        self.y_pos+=60
        
                
    


class Arrow:
    def __init__(self, x, y, direction, arrow_picture,damage):
        self.x_pos = x
        self.owner = 'Archer'
        self.y_pos = y
        self.speed = 14
        self.direction = direction
        self.picture = arrow_picture
        self.width = arrow_picture.get_width()
        self.height = arrow_picture.get_height()
        self.status = 'in game'
        self.damage=damage
        
       
        self.hitbox = pygame.Rect(
            self.x_pos  ,
            self.y_pos ,
            self.width,
            self.height 
        )

    def update(self):
        if self.y_pos>7000:
            self.health=0
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed

        self.hitbox.topleft = (
            self.x_pos ,
            self.y_pos
        )

    def draw(self, screen, offset):
        if self.direction == 'right':
            screen.blit(self.picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        else:
            flipped = pygame.transform.flip(self.picture, True, False)
            screen.blit(flipped, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def is_off_screen(self, screen_width):
        return self.x_pos < -screen_width or self.x_pos > screen_width * 2
    
        
