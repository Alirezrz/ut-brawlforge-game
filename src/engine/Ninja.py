import pygame
import os
from src.engine.bullet import Bullet
from config import Ninja_width, Ninja_height,profileSideSize, health_bar_lenght, roboman_health_bar_frame_thickness
from src.engine.protector import Guard_Drone
## must be done -->  1- list of enemies for hit when attacking must be fixed 
class Ninja:
    def __init__(self, x, y, screen_width, screen_height, targets, hero_creation_index=2,username='Player',LOAD_FLAG=True,soundeffect_flag=True):
        self.username=username
        self.frame_address=None
        self.ALIVE=True
        self.DEAD=False
        self.events = []
        self.SOUND_FLAG=soundeffect_flag
        self.frame_address=None

        self.x_pos = x
        self.y_pos = y
        self.on_platform = False

        self.hero_creation_index = hero_creation_index  # دیفالت 2
        
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.freezed=False
        self.last_freezed=0
        self.allow_move_right = True
        self.allow_move_left = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Look = 'right'
        self.horizontal_speed = 10
        self.vertical_speed = 0
        self.jump_strenght = 25
        self.gravity_strenght = 1
        self.on_ground = False
        self.width = Ninja_width
        self.height = Ninja_height
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.health = 100
        self.max_health = 100
        self.bullets = []
        self.last_shot_time = 0
        self.shot_cooldown = 300
        self.throwing_until = 0
        self.kunai_fired = False
        self.throw_flag=False
        # Sword attack-related attributes
        self.last_attack_time = 0
        self.attack_cooldown = 500  
        self.attacking_until = 0
        self.attack_hit_registered = False
        self.attack_targets = targets  
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
        self.last_jump_time = 0
        self.jump_cooldown = 250
                            
        #drone attribute:                  # این مقدار ها برای تست هست بعدا باید تنظیم بشن
        self.guard_drone_reload_duration=10000   # بعد از 20 ثانیه شارژ میشه
        self.last_guard_call=0
        self.guard_drone=[]
        self.drone_duration=20000    # هر بار که صدا زده بشه 30 ثانیه باقی میمونه  
        
        
        
        
        self.prev_status='unknown'
        self.ATTACK=True
        self.HIT_PER_ATTACK=0
        self.MOVEWITHATTACKFLAG=True
        self.has_defuse_kit=False



        

        
        #Super power attributes:
        self.Super_cofficent=1
        self.Super_duration=10000
        self.Super_lastActivation=0
        self.SuperPower_CoolDown=100
        self.SuperPower_pic_display_duratiom=1500
        self.last_SPdisplay=0
        self.Super_PowerFlag=False
        self.frame_duration = 100
        self.shutter_overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.shutter_alpha = 0
        self.shutter_direction = 1 
        self.is_first_time=True          

        if LOAD_FLAG:
            if self.SOUND_FLAG:
                self.jump_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "ninja jump.MP3"))
                self.kunai_hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "kunai hit.mp3"))
                self.kunai_hit_platform_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "kunai hit platofrm.mp3"))
                self.melee_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "sword.mp3"))
                self.melee_hit_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "sword hit.mp3"))
                self.throw_kunai_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "throw kunai.mp3"))
                self.hurt_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja", "ninja hurt.mp3"))        
            self.ninja_health_bar_frame = pygame.image.load("src/assets/images/Ninja/Ninja_health_bar_frame.png")
            self.ninja_health_bar =pygame.image.load("src/assets/images/Ninja/Ninja_health_bar.png")
            self.ninja_profile_picture = pygame.image.load("src/assets/images/Ninja/ninja_profile.png")
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Ninja")

            # Load Idle image for default state
            tmp = pygame.image.load(os.path.join(base_path, "Idle", f"Idle__000.png"))
            self.current_picture = pygame.transform.scale(tmp, (62, 118))
            

            
            self.freezed_frame=pygame.transform.scale(
                pygame.image.load(os.path.join(base_path,"freezed.png")),
                (62,118)
            )
            
            
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
                
                
                
            self.Attack_frames=[]
            sizes = [78,75,85,132,136,149,149,149,147,137]
            self.with_sword_width= [77,75,80,73,95,108,107,105,115,105]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.Attack_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
                
                
            self.JumpAttack_frames=[]
            self.jumpattack_sizes=[(87,118),(86,118),(86,118),(136,118),(136,118),(137,138),(139,138),(140,138),(125,170),(136,118)]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.JumpAttack_frames.append(pygame.transform.scale(tmp, self.jumpattack_sizes[i]))
                
            self.death_frames=[]
            self.death_sizes=[(63,118),(74,118),(127,113),(111,108),(140,100),(157,100),(152,90),(157,90),(160,90),(156,90)]
            for i in range(0, 10):
                img_path = os.path.join(base_path, "death", f"Dead__00{i}.png")
                tmp = pygame.image.load(img_path)
                self.death_frames.append(pygame.transform.scale(tmp, self.death_sizes[i]))
            
      
        
        self.SUPER_POWER_FLAG=False
        self.GUARD_DRONE_FLAG=False
        self.DOUBLE_JUMP_FLAG=False
        
        
        self.DEAD=False

    
    def hurt(self):
        if self.SOUND_FLAG:
            self.hurt_sound.play()
        self.events.append("ninja hurt")
        if self.health <= 0:
            self.die()
    def die(self):
        if self.DEAD:
            return
        self.ALIVE = False
        self.status = 'dead'
        self.current_frame_index = 0
        self.last_animation_state = 'death'
        self.vertical_speed = 0
        self.on_ground = True
        self.AllowJump_flag = False
        self.allow_move_left = False
        self.allow_move_right = False
        self.y_pos+=30        
        self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
             
    def display_health_bar(self, screen):
        if self.health<0:
            self.health=0
        scaled_frame_height = profileSideSize
        health_bar_frame = pygame.transform.scale(
            self.ninja_health_bar_frame,
            (health_bar_lenght + (2 * roboman_health_bar_frame_thickness), scaled_frame_height)
        )
        health_bar = pygame.transform.scale(
            self.ninja_health_bar,
            (
                int(health_bar_lenght * (self.health / self.max_health)),
                scaled_frame_height - (2 * roboman_health_bar_frame_thickness)
            )
        )

        if self.hero_creation_index == 1:
            bar_x, bar_y = profileSideSize, 0
            health_x, health_y = profileSideSize + roboman_health_bar_frame_thickness, roboman_health_bar_frame_thickness
            profile_x, profile_y = 0, 0
        elif self.hero_creation_index == 2:
            if self.is_first_time:
                self.ninja_profile_picture = pygame.transform.flip(self.ninja_profile_picture, True, False)
                self.is_first_time=False
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            bar_y = 0
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = roboman_health_bar_frame_thickness
            profile_x = self.screen_width - profileSideSize
            profile_y = 0
        elif self.hero_creation_index == 3:
            bar_x = profileSideSize
            bar_y = self.screen_height - scaled_frame_height
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = bar_y + roboman_health_bar_frame_thickness
            profile_x = 0
            profile_y = self.screen_height - profileSideSize
        elif self.hero_creation_index == 4:
            if self.is_first_time:
                self.ninja_profile_picture = pygame.transform.flip(self.ninja_profile_picture, True, False)
                self.is_first_time=False
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            bar_y = self.screen_height - scaled_frame_height
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = bar_y + roboman_health_bar_frame_thickness
            profile_x = self.screen_width - profileSideSize
            profile_y = self.screen_height - profileSideSize
        else:
            bar_x = self.screen_width - health_bar_lenght - (2 * roboman_health_bar_frame_thickness) - profileSideSize
            bar_y = 0
            health_x = bar_x + roboman_health_bar_frame_thickness
            health_y = roboman_health_bar_frame_thickness
            profile_x = self.screen_width - profileSideSize
            profile_y = 0
        screen.blit(health_bar_frame, (bar_x, bar_y))
        screen.blit(health_bar, (health_x, health_y))
        if self.ninja_profile_picture:
            screen.blit(
                pygame.transform.scale(self.ninja_profile_picture, (profileSideSize, profileSideSize)),
                (profile_x, profile_y)
            )            
            
        
    def display(self, screen, offset, shot_bullets):
        self.Update_SuperPower() 
        self.Super_Power_effect()
        for drone in self.guard_drone:
            drone.Update( screen,offset,shot_bullets)

        
        
        
    
        display_picture = self.current_picture
        display_x = self.x_pos

        if self.Look == 'left':
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            width_diff = display_picture.get_width() - self.hitbox.width
            display_x -= width_diff
            screen.blit(flipped_picture, (display_x - offset[0], self.y_pos - offset[1]))
        else:
            screen.blit(display_picture, (display_x - offset[0], self.y_pos - offset[1]))

        self.display_health_bar(screen)
    def update_animation(self, shot_bullets):
        if self.DEAD:
            self.current_picture=self.death_frames[9]
            self.frame_address=["death_frames",9]
            self.y_pos=self.y_pos+118-self.current_picture.get_height()
        current_time = pygame.time.get_ticks()

        if not self.ALIVE:
            if self.current_frame_index < len(self.death_frames):
                self.current_picture = self.death_frames[self.current_frame_index]
                self.frame_address=["death_frames",self.current_frame_index]
                new_width, new_height = self.current_picture.get_size()
                if self.current_frame_index == 0:
                    self.previous_center = (self.x_pos + self.width // 2, self.y_pos + self.height)
                self.x_pos = self.previous_center[0] - new_width // 2
                self.y_pos = self.previous_center[1] - new_height
                self.hitbox = pygame.Rect(self.x_pos, self.y_pos, new_width, new_height)

                if current_time - self.last_frame_update_time > self.frame_duration:
                    self.current_frame_index += 1
                    self.last_frame_update_time = current_time
            else:
                self.current_picture = self.death_frames[-1]
                self.frame_address=["death_frames",-1]
                self.DEAD = True  
            return

        if self.freezed:
            self.current_picture = self.freezed_frame
            self.frame_address=["freezed",-2]
            return

        if self.Super_PowerFlag:
            self.current_picture = self.SuperPower_pic
            self.frame_address=["SuperPower_pic",-2]
            return
       
        
        if self.status == "attack":
            target_animation_state = 'attack'
        elif self.status == "jumpattack":
            target_animation_state = 'jumpattack'
        elif not self.on_ground and self.current_platform is None:
            if self.status == "jump_throw":
                target_animation_state = 'jump_throw'
            elif self.status == "throw":
                target_animation_state = 'jump_throw'
            else:
                target_animation_state = 'jump'
        elif self.status == "throw":
            target_animation_state = 'throw'
        else:
            target_animation_state = 'running' if self.is_moving_horizontally else 'idle'

        if target_animation_state != self.last_animation_state:
            self.current_frame_index = 0
            self.last_frame_update_time = current_time
            self.last_animation_state = target_animation_state
            self.kunai_fired = False

        speed = 50 if self.status in ['attack', 'jumpattack', 'throw', 'jump_throw'] else self.animation_speed
        elapsed_time = current_time - self.last_frame_update_time
        if elapsed_time < speed:
            return

        self.last_frame_update_time = current_time

        
        
        if target_animation_state == 'jumpattack':
            if self.current_frame_index < len(self.JumpAttack_frames):
                self.current_picture = self.JumpAttack_frames[self.current_frame_index]
                self.frame_address=["JumpAttack_frames",self.current_frame_index]
                frame_width = self.with_sword_width[self.current_frame_index]
                self.hitbox = pygame.Rect(self.x_pos, self.y_pos, frame_width, 118)
                self.current_frame_index += 1
            else:
                self.status = "Idle"
                self.last_animation_state = "idle"
                self.current_frame_index = 0
                self.ATTACK = True
                self.HIT_PER_ATTACK = 0
                self.attack_hit_registered = False

        elif target_animation_state == 'attack':
            if self.current_frame_index < len(self.Attack_frames):
                self.current_picture = self.Attack_frames[self.current_frame_index]
                self.frame_address=["Attack_frames",self.current_frame_index]
                frame_width = self.with_sword_width[self.current_frame_index]
                self.hitbox = pygame.Rect(self.x_pos, self.y_pos, frame_width, 118)
                self.current_frame_index += 1
            else:
                self.status = "Idle"
                self.last_animation_state = "idle"
                self.current_frame_index = 0
                self.ATTACK = True
                self.HIT_PER_ATTACK = 0
                self.attack_hit_registered = False

        elif target_animation_state == 'jump_throw':
            if self.current_frame_index < len(self.jumpThrow_frames):
                self.current_picture = self.jumpThrow_frames[self.current_frame_index]
                self.frame_address=["jumpThrow_frames",self.current_frame_index]
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
                self.frame_address=["jump_frames",self.current_frame_index]
                self.current_frame_index += 1

        elif target_animation_state == 'throw':
            if self.current_frame_index < len(self.throw_frames):
                self.current_picture = self.throw_frames[self.current_frame_index]
                self.frame_address=["throw_frames" , self.current_frame_index]
                
                if self.current_frame_index == 3 and not self.kunai_fired:
                    self.fire_kunai(shot_bullets)
                    self.kunai_fired = True
                self.current_frame_index += 1
                if self.current_frame_index == len(self.throw_frames) - 1:
                    self.allow_move_left = True
                    self.allow_move_right = True
            else:
                self.status = "Idle"
                self.last_animation_state = "idle"
                self.current_frame_index = 0

        elif target_animation_state == 'running':
            self.current_frame_index = (self.current_frame_index + 1) % len(self.run_frames)
            self.current_picture = self.run_frames[self.current_frame_index]
            self.frame_address=["run_frames",self.current_frame_index]

        elif target_animation_state == 'idle':
            self.current_frame_index = (self.current_frame_index + 1) % len(self.idle_frames)
            self.current_picture = self.idle_frames[self.current_frame_index]
            self.frame_address=["idle_frames",self.current_frame_index]

        self.update_attack()
        print(f"sending from ninja ")
        print(f"frame_adress={self.frame_address[0] }    {self.frame_address[1]}")
        print("-------------------------------")


    def fire_kunai(self, shot_bullets):
        bullet_x = self.x_pos + (self.width if self.Look == 'right' else -self.Kunai_pic.get_width())
        bullet_y = self.y_pos + self.height // 2 - self.Kunai_pic.get_height() // 2
        if self.Look == 'right':
            bullet_x -= 20
        else:
            bullet_x += 20

        bullet = Bullet(
            self.username,
        bullet_x,
        bullet_y,
        15*self.Super_cofficent,
        self.Look,
        self.Kunai,
        "Ninja",
        40 if self.Super_cofficent>1 else 20
        )
        if self.SOUND_FLAG:
            self.throw_kunai_sound.play()
        self.events.append("throw kunai")

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

    def move_right(self,powerup=1):
        if self.allow_move_right and self.status not in ["throw"] and self.status!='attack':
            self.x_pos += self.horizontal_speed*self.Super_cofficent*powerup
            self.is_moving_horizontally = True
            self.Look = 'right'
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            self.fall_from_platform()

    def move_left(self,powerup=1):
        if self.allow_move_left  and self.status not in ["throw"] and self.status!='attack':
            self.x_pos -= self.horizontal_speed*self.Super_cofficent*powerup
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

    def update_bullets(self, screen, shot_bullets,platforms,targets):
        self.update_drone()
        
        for bullet in self.bullets[:]:
            bullet.update()
            
        for bullet in self.bullets:
            if bullet not in shot_bullets:
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            for  platform in platforms:
                if bullet.hitbox.colliderect(platform.rect):
                    if self.SOUND_FLAG:
                        self.kunai_hit_platform_sound.play()
                    self.events.append("kunai hit platofrm")

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)
                        
        for target in targets:
            for bullet in self.bullets:
                if target.hitbox.colliderect(bullet.hitbox):
                    target.health-=bullet.damage   # should be intialized ***** 
                    target.hurt()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)
    def update_bullets_online(self,shot_bullets,platforms,targets):
        
        for bullet in self.bullets[:]:
            bullet.update()
            
        for bullet in self.bullets:
            if bullet not in shot_bullets:
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            for  platform in platforms:
                if bullet.hitbox.colliderect(platform.rect):
                    if self.SOUND_FLAG:
                        self.kunai_hit_platform_sound.play()
                    self.events.append("kunai hit platofrm")

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)
                        
        for target in targets:
            for bullet in self.bullets:
                if target.hitbox.colliderect(bullet.hitbox):
                    target.health-=bullet.damage   # should be intialized ***** 
                    target.hurt()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if bullet in shot_bullets:
                        shot_bullets.remove(bullet)

    def jump(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_jump_time < self.jump_cooldown:
            return

        if self.on_ground and self.jump_count == 0 and self.AllowJump_flag:
            if self.SOUND_FLAG:
                self.jump_sound.play()
            self.events.append("ninja jump")
            self.vertical_speed = self.jump_strenght 
            self.jump_count = 1
            self.on_ground = False
            self.current_platform = None
            self.last_jump_time = current_time  
            return

        if not self.on_ground and self.jump_count == 1 and self.Allow_double_jump and self.DOUBLE_JUMP_FLAG:
            self.double_jump()
            self.jump_count = 2
            self.last_jump_time = current_time 

    def double_jump(self):
        current_time = pygame.time.get_ticks()
        self.vertical_speed = self.jump_strenght
        if self.SOUND_FLAG:
            self.jump_sound.play()
        self.events.append("ninja jump")
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
        if current_time-self.Super_lastActivation>=self.SuperPower_CoolDown and self.current_platform!=None and self.vertical_speed==0 and self.SUPER_POWER_FLAG:
            self.Super_cofficent=1.5
            self.Super_lastActivation = current_time
            self.last_SPdisplay=current_time
            self.Super_PowerFlag=True
            self.Kunai=self.Fired_kunai_pic
            
    def Update_SuperPower(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.Super_lastActivation>self.Super_duration and self.current_platform!=None:
            self.Super_cofficent=1
            self.Kunai=self.Kunai_pic
            
            
            
            
    def Super_Power_effect(self):
        self.update_drone()
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
            
            
    def Send_teleport_request(self,Gates):
        for Gate in Gates:
            Gate.recieve_request(self)
        
        
        
    def call_drone(self):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_guard_call >= self.guard_drone_reload_duration and self.GUARD_DRONE_FLAG:
            self.guard_drone.append(Guard_Drone(self,"Ninja"))
            self.last_guard_call=current_time
            
            
    def update_drone(self):
        if len(self.guard_drone) == 1:
            current_time = pygame.time.get_ticks()
            drone = self.guard_drone[0]
            drone.update_pos()
            if current_time - self.last_guard_call >= self.drone_duration:
                if drone.status != 'departing':
                    drone.status = 'departing'
            if drone.status == 'departing' and drone.departed_len>3000:
                self.guard_drone.remove(drone)
    def handle_input(self, keys, gate, shot_bullets, bullet_class,trigger_shutter, mouse_bottons):
        if not self.ALIVE:
            return

        self.is_moving_horizontally = False
        if self.freezed:
            return
        if self.hero_creation_index==1:
            if mouse_bottons[2]:
                self.attack()  
            if keys[pygame.K_a]:
                self.move_left()
                self.is_moving_horizontally = True
            if keys[pygame.K_d]:
                self.move_right()
                self.is_moving_horizontally = True
            if keys[pygame.K_w]:
                self.jump()
            if mouse_bottons[0]:
                self.shoot(shot_bullets, bullet_class)
            if keys[pygame.K_g]:
                self.call_drone()

            if keys[pygame.K_LSHIFT]:
                if not self.Super_PowerFlag:
                    if trigger_shutter:
                        trigger_shutter(strength=10, duration=1500)
                self.Activate_Super_Power()
                
            if keys[pygame.K_TAB]:
                self.Send_teleport_request(gate)

       
                    
    def handle_input_online(self, keys, gate, shot_bullets, bullet_class, trigger_shutter, mouse_buttons):
            self.is_moving_horizontally = False
            if keys[pygame.K_d]:
                self.move_right()
                self.is_moving_horizontally = True
                print("Moving right...")
            if keys[pygame.K_a]:
                self.move_left()
                self.is_moving_horizontally = True
                print("Moving left...")
            if keys[pygame.K_w]:
                self.jump()
                print("jump...")
            if keys[pygame.K_LSHIFT]:
                if not self.Super_PowerFlag:
                    if trigger_shutter:
                        trigger_shutter(strength=10, duration=1500)
                self.Activate_Super_Power()
            if keys[pygame.K_TAB]:
                self.Send_teleport_request(gate)
            if mouse_buttons[0]:
                self.shoot(shot_bullets, bullet_class)

            
            if mouse_buttons[2]:
                self.attack()      

            
                
    def attack(self):
        if self.ATTACK and self.vertical_speed==0 and self.current_platform!=None:
            self.prev_status = self.status
            self.status = 'attack'
            if self.SOUND_FLAG:
                self.melee_sound.play() 
            self.events.append("sword")
            self.current_frame_index = 0
            self.attack_hit_registered = False
            self.ATTACK = False 
            self.MOVEWITHATTACKFLAG=True
            return
        elif self.ATTACK:
            self.prev_status = self.status
            self.status = 'jumpattack'
            if self.SOUND_FLAG:
                self.melee_sound.play() 
            self.events.append("sword")
            self.current_frame_index = 0
            self.attack_hit_registered = False
            self.ATTACK = False 
            self.MOVEWITHATTACKFLAG=True
            return
        

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
                    
                    
                    
    def update(self, platforms, shot_bullets, targets, keys, gate, trigger_shutter=None):

        if not self.ALIVE:
            self.update_animation(shot_bullets)
            return
        
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.current_picture.get_width(),self.current_picture.get_height())
        if self.y_pos>1000:
            self.health=0
        self.is_on_ground()
        self.gravity()
        self.vertical_move()
        self.platforms_collisions(platforms)
        self.move_with_platform()
        self.jump_under_platform(platforms)
        self.update_animation(shot_bullets)
        self.update_bullets(shot_bullets, targets)
        self.handle_input(keys, gate, shot_bullets, Bullet, trigger_shutter)
        self.update_drone()
        
    def update_online(self, platforms, shot_bullets, targets, keys, gate, trigger_shutter=None):
        for bullet in self.bullets:
            if bullet not in shot_bullets:
                self.bullets.remove(bullet)
        self.update_drone()  
       
        print(f"number of drones----->{len(self.guard_drone)}\n\n")
        if hasattr(self, "ALIVE") and not self.ALIVE:
            self.update_animation(shot_bullets)
            return
        if self.y_pos>1000:
            self.health=0
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.current_picture.get_width(), self.current_picture.get_height())

        self.is_on_ground()
        self.gravity()
        self.vertical_move()
        self.platforms_collisions(platforms)
        self.move_with_platform()
        self.jump_under_platform(platforms)
        self.update_animation(shot_bullets)
        self.update_drone()
        self.update_bullets_online(shot_bullets,platforms, targets)
        



    def serialize(self):
        frame_source_name = "idle_frames"
        frame_index_val = 0
        if len(self.guard_drone)==1:
            drone_data=self.guard_drone[0].serialize()
        else:
            drone_data='None'
        
        if hasattr(self, 'frame_address') and self.frame_address:
             frame_source_name = self.frame_address[0]
             frame_index_val = self.frame_address[1]
             
        data={
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
            "look": self.Look,
            "health": self.health,
            "username": self.username,
            "frame_source": frame_source_name,
            "frame_index": frame_index_val,
            "character": 'Ninja',
            "events": self.events,
            "creation_index": self.hero_creation_index,
            "is_dead": self.DEAD ,
            "drone":drone_data,
        }
        return data
        
                      

    






            
            
            
    
            
            
            
    

        
        
        
        
            
            
            
        
            
        
        
        
        
        
        
        
        
    
    
    
    
    