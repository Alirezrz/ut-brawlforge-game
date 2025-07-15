import pygame
import os
from config import roboman_jetpack_reload,roboman_reload_time, jump_strenght ,horizontal_speed,gravity_strenght,profileSideSize,health_bar_lenght,roboman_health_bar_frame_thickness
from src.engine.protector import Guard_Drone

# bug : وقتی تیر انداز تیرش به تروریست بخوره روبات میمیره
class Roboman:

    def __init__(self, x, y,  roboman_health_bar_frame,roboman_health_bar, hero_profile_picture, screen_width, screen_height, sounds=None, trigger_shutter_callback=None, hero_creation_index=1):
        self.x_pos = x
        self.y_pos = y
        self.hero_profile_picture = hero_profile_picture
        self.roboman_health_bar_frame = roboman_health_bar_frame
        self.roboman_health_bar = roboman_health_bar
        self.on_platform = False
        self.current_platform = None
        self.status="idle"
        self.trigger_shutter_callback = trigger_shutter_callback
        self.horizontal_speed = 7  
        self.jump_strenght = 20 
        self.freezed=False
        self.is_first_time=True

        self.hero_creation_index = hero_creation_index  # اضافه شد
        self.shot_hit_enemy_sound = pygame.mixer.Sound(
            os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "RoboMan", "shot_hit_enemy.wav")
)
        self.shot_hit_platform_sound = pygame.mixer.Sound(
            os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "RoboMan", "shot_hit_platoform.wav")
)
        self.jump_sound = sounds.get('jump') if sounds else None
        self.shoot_sound = sounds.get('shoot') if sounds else None
        self.jetpack_sound = sounds.get('jetpack') if sounds else None
          
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "RoboMan_pictures")

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

        self.idle_frames = []
        for i in range(1, 11):
            try:
                img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                idle_tmp = pygame.image.load(img_path)
                self.idle_frames.append(pygame.transform.scale(idle_tmp, (70, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")
                self.idle_frames.append(pygame.Surface((70, 118)))

        self.jump_frames = []
        for i in range(1, 11):
            try:
                img_path = os.path.join(base_path, "idle", f"Idle ({i}).png")
                jump_tmp = pygame.image.load(img_path)
                self.jump_frames.append(pygame.transform.scale(jump_tmp, (70, 118)))
            except FileNotFoundError:
                print(f"Error: Roboman idle frame 'Idle ({i}).png' not found at {img_path}. Check path.")

        self.shoot_frames = []
        self.Bullet_Class_ref = None
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
            
        img_path = os.path.join(base_path, f"jetpack.png")
        self.jetpack_frame=pygame.image.load(img_path)
        self.jetpack_frame=pygame.transform.scale(self.jetpack_frame, (80,118))
 
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

        self.picture = self.idle_frames[0] if self.idle_frames else pygame.Surface((70, 118))
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()

        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = horizontal_speed
        self.vertical_speed = 0
        self.jump_strenght =jump_strenght
        self.gravity_strenght = gravity_strenght
        self.on_ground = False
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.explosions=[]
        
        self.jetpack_reload_duration = roboman_jetpack_reload
        self.last_jetpack_fire=0
        self.jetpack_thrust = 12
        self.jetpack_burn_time = 600
        self.jetpack_reload_duration = 2000
        self.last_jetpack_use_time = 0
        self.jetpack_start_time = 0
        self.jetpack_active = False

        self.current_picture = self.picture
        self.current_frame_index = 0
        self.animation_speed = 100
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False
        self.last_animation_state = None

        self.is_shooting=False
        self.shooting_animation_start_time = 0
        self.shooting_animation_duration = len(self.shoot_frames) * self.animation_speed if self.shoot_frames else 1
        self.last_animation_state = None
        self.RunShoot=False
        self.Last_RunShoot_frame_index=0
        self.Reload_duration= roboman_reload_time
        self.Last__Shooting_time=0
        self.frame_flag=False
        self.in_jump_animation = False
        
        # drone attributes:
        self.guard_drone_reload_duration = 10000  # cooldown time (ms)
        self.last_guard_call = 0
        self.guard_drone = []
        self.drone_duration = 20000

    def display(self, screen, offset, shot_bullets):
        self.roboman_health_bar = pygame.transform.scale(
            self.roboman_health_bar, 
            (int(health_bar_lenght * (self.health / self.max_health)), profileSideSize - (2 * roboman_health_bar_frame_thickness))
        )
        self.roboman_health_bar_frame = pygame.transform.scale(
            self.roboman_health_bar_frame, 
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
                self.hero_profile_picture = pygame.transform.flip(self.hero_profile_picture, True, False)
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

        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        elif self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))

        for drone in self.guard_drone:
            drone.Update(screen, offset, shot_bullets)
            
        for exp in self.explosions:
            if not exp.Expired:
                exp.display(screen,offset)
            else:
                self.explosions.remove(exp)

        # رسم health bar و profile در موقعیت مناسب
        screen.blit(self.roboman_health_bar_frame, (bar_x, bar_y))
        screen.blit(self.roboman_health_bar, (health_x, health_y))
        screen.blit(pygame.transform.scale(self.hero_profile_picture, (profileSideSize, profileSideSize)), (profile_x, profile_y))

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.jetpack_active and self.jetpack_frame:
            self.current_picture = self.jetpack_frame
            return
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

            if self.is_shooting:
                if current_time - self.last_frame_update_time > self.animation_speed:
                    self.current_frame_index = int((elapsed_time / self.animation_speed)) % len(self.shoot_frames)
                    self.current_picture = self.shoot_frames[self.current_frame_index]
                    self.last_frame_update_time = current_time
                return

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
        self.is_moving_horizontally = False

    def fall_from_platform(self):
        if self.current_platform is not None:
            if self.x_pos + self.width < self.current_platform.x_pos or self.x_pos > self.current_platform.x_pos + self.current_platform.width:
                self.on_ground = False
                self.current_platform = None

    def move_with_platform(self):
        if self.current_platform is not None and self.current_platform.moving:
            self.horizontal_auto_speed = 2.5 * self.current_platform.direction
            self.horizontal_move()
            self.hitbox.topleft = (self.x_pos, self.y_pos)

    def move_right(self):
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
        current_time = pygame.time.get_ticks()
        
        if current_time - self.Last__Shooting_time > self.Reload_duration and not self.jetpack_active:
            if self.shoot_sound:
                self.shoot_sound.play()
            
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
            
            bullet = Bullet_Class(
                bullet_start_x,
                bullet_start_y + 18, 
                15, 
                self.Look, 
                self.bullet_picture, 
                "Roboman"
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

        self.JumpShoot = True
        self.shooting_animation_start_time = pygame.time.get_ticks()
        self.current_frame_index = 0

    def respawn(self):
        self.current_platform = None
        self.on_ground = False
        self.x_pos = 200
        self.y_pos = 250 - self.height - 20
        self.vertical_speed = 0
        self.health = self.max_health

    def update_bullets(self, screen, shot_bullets,platforms,targets):
        self.update_drone()
        print(len(self.bullets))
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen(self.screen_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                if bullet in shot_bullets:
                    shot_bullets.remove(bullet)
        for bullet in self.bullets:
            for  platform in platforms:
                if bullet.hitbox.colliderect(platform.rect):
                    self.explosions.append(Explosion(bullet.x_pos,bullet.y_pos-65))
                    if self.shot_hit_platform_sound:
                        self.shot_hit_platform_sound.play()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)
                        
        for target in targets:
            for bullet in self.bullets:
                if target.hitbox.colliderect(bullet.hitbox):
                    target.health-=20   # should be intialized ***** 
                    if self.shot_hit_enemy_sound:
                        self.shot_hit_enemy_sound.play()

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)
                    
                    
        
                
                                  
                    


    def jump(self):
        if self.on_ground :
            if self.jump_sound:
                self.jump_sound.play()
            self.vertical_speed = self.jump_strenght
            self.on_ground = False
            self.current_platform = None
            self.last_jump_time=pygame.time.get_ticks()
            self.current_frame_index = 0 
            self.frame_flag=True
            self.in_jump_animation = True 
            self.allow_move_left=True
            self.allow_move_right=True
            
    def activate_jetpack(self):
        current_time = pygame.time.get_ticks()
        if not self.on_ground and not self.jetpack_active and (current_time - self.last_jetpack_use_time >= self.jetpack_reload_duration):
            if self.jetpack_sound:
                self.jetpack_sound.play()
            self.jetpack_active = True
            self.jetpack_start_time = current_time
            self.last_jetpack_use_time = current_time
            if self.trigger_shutter_callback:
                self.trigger_shutter_callback(strength=5, duration=150)

    def update_jetpack(self):
        if self.jetpack_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.jetpack_start_time <= self.jetpack_burn_time:
                self.vertical_speed = self.jetpack_thrust
            else:
                self.jetpack_active = False
                if self.Jump_frames:
                    self.current_frame_index = 8
                    self.current_picture = self.Jump_frames[8]

    def gravity(self):
        self.update_jetpack() 
        if not self.on_ground:
            self.vertical_speed -= self.gravity_strenght

    def is_on_ground(self):
    # Simplify like Ninja's version
        self.on_ground = bool(self.current_platform)

    def vertical_move(self):
        self.y_pos -= self.vertical_speed
        self.hitbox.topleft = (self.x_pos, self.y_pos)

    def horizontal_move(self):
        self.x_pos += self.horizontal_auto_speed
        self.horizontal_auto_speed = 0

    def platforms_collisions(self, platforms):
    # Reset movement flags
        self.allow_move_left = True
        self.allow_move_right = True
    
        for platform in platforms:
        # Landing detection
            if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                if ((self.y_pos + self.height) >= platform.y_pos) and ((self.y_pos + self.height) < (platform.y_pos + platform.height) + 10):
                    if self.vertical_speed <= 0:  # Only land if falling
                        self.on_ground = True
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos - self.height
                        self.current_platform = platform
        
        # Side collision detection
            if self.x_pos + self.width >= platform.x_pos and self.x_pos <= platform.x_pos + platform.width:
                if ((self.y_pos + self.height) > platform.y_pos) and (self.y_pos < platform.y_pos + platform.height):
                # Left collision
                    if abs(self.x_pos - (platform.x_pos + platform.width)) <= 10:
                        self.allow_move_left = False
                        self.x_pos = platform.x_pos + platform.width
                # Right collision
                    if abs(self.x_pos + self.width - platform.x_pos) <= 10:
                        self.allow_move_right = False
                        self.x_pos = platform.x_pos - self.width

    def jump_under_platform(self, platforms):
        if self.vertical_speed > 0:
            for platform in platforms:
                if self.x_pos + self.width > platform.x_pos and \
                   self.x_pos < platform.x_pos + platform.width:
                    if self.y_pos <= platform.y_pos + platform.height and \
                       self.y_pos > platform.y_pos:
                        self.vertical_speed = 0
                        self.y_pos = platform.y_pos + platform.height
                        
                        
    def Send_teleport_request(self,Gates):
        for gate in Gates:
            gate.recieve_request(self)
        
        
        
    def handle_input(self, keys, gate, shot_bullets, bullet_class):
        self.is_moving_horizontally = False
        if self.freezed:
            return

        if keys[pygame.K_d]:
            self.move_right()
            self.is_moving_horizontally = True
        if keys[pygame.K_a]:
            self.move_left()
            self.is_moving_horizontally = True
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_LSHIFT]:
                self.activate_jetpack()
            else:
                self.jump()
        if keys[pygame.K_r]:
            self.respawn()
        if keys[pygame.K_t]:
            self.Send_teleport_request(gate)
        if keys[pygame.K_f]: # this one must change 
            self.shoot(shot_bullets, bullet_class)
            
        if keys[pygame.K_g]:
            self.call_drone()
            
            
    def call_drone(self):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_guard_call >= self.guard_drone_reload_duration:
            self.guard_drone.append(Guard_Drone(self,"Roboman"))
            self.last_guard_call=current_time
    def update_drone(self):
        if len(self.guard_drone) == 1:
            current_time = pygame.time.get_ticks()
            drone = self.guard_drone[0]
            if current_time - self.last_guard_call >= self.drone_duration:
                if drone.status != 'departing':
                    drone.status = 'departing'
            if drone.status == 'departing' and drone.is_off_screen_exit():
                self.guard_drone.remove(drone)






#================================================

class Explosion:
    def __init__(self,x,y):
        self.x_pos=x
        self.y_pos=y
        self.Expired=False
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "RoboMan_pictures")
        
        self.images=[]
        
        for i in range (5):
            self.images.append(
                pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path,"explosion",f"{i}.png")
                ),
                (12,150)
            )
            )
        self.frame_index=-1
        self.frame=self.images[0]
        self.last_update=0
        
            
            
            
    def display(self,screen,offset):
        self.update()
        screen.blit(self.frame,(self.x_pos-offset[0],self.y_pos-offset[1]))
        
    def update(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time-self.last_update
        if elapsed_time>=60 and self.frame_index<4:
            self.frame_index+=1
            self.frame=self.images[self.frame_index]
            self.last_update=current_time
        elif elapsed_time>=60 and not self.frame_index<4:
            self.Expired=True
            
        
        
        
        