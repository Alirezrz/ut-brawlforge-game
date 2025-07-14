import os
import pygame
from src.engine.protector import Guard_Drone
class Archer:
    def __init__(self, x, y,targets):
        self.x_pos = x
        self.y_pos = y
        self.on_platform = False
        self.current_platform = None
        self.horizontal_auto_speed = 0
        self.allow_move_right = True
        self.allow_move_left = True
        self.Look = 'right'
        self.horizontal_speed = 7
        self.vertical_speed = 0
        self.jump_strenght = 20
        self.gravity_strenght = 1
        self.on_ground = False
        self.jump_count = 0
        self.last_jump_time = 0
        self.jump_cooldown = 250
        self.double_jump_allowed = True

        self.targets=targets

        self.width = 88
        self.height = 100
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        self.health = 63
        self.max_health = 100
        self.bullets = []
        self.status = 'idle'

        self.current_frame_index = 0
        self.animation_speed = 80  # slightly faster
        self.last_frame_update_time = pygame.time.get_ticks()
        self.is_moving_horizontally = False

        self.shooting = False
        self.shot_triggered = False


        self.guard_drone_reload_duration = 10000  # 10 seconds
        self.last_guard_call = 0
        self.guard_drone = []
        self.drone_duration = 20000  # drone active time in ms


        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Archer")

        self.idle_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path,"idle",f"{i}.png")),(88,100)) for i in range(6)]
        sizes = [89,90,91,90,89,90,96,90]
        self.run_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path,"run",f"{i}.png")),(sizes[i],100)) for i in range(8)]
        sizes = [91,93,88,90,94,89,88,90]
        self.jump_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path,"jump",f"{i}.png")),(sizes[i],100)) for i in range(8)]
        sizes = [90,72,72,72,72,72,97,113,106,89,77,72,70]
        self.shot_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path,"shot",f"{i}.png")),(sizes[i],100)) for i in range(13)]
        self.arrow_pic = pygame.transform.scale(pygame.image.load(os.path.join(base_path,"Arrow.png")),(30,2))
        sizes = [78,60,132,62]      
        self.attack_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path,"attack",f"{i}.png")),(sizes[i],100)) for i in range(4)]

        
        self.current_picture = None

    def display(self, screen, offset):
        for arrow in self.bullets:
            arrow.update()
            arrow.draw(screen,offset)
        display_picture = self.current_picture or self.idle_frames[0]
        if self.Look == 'right':
            screen.blit(display_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        else:
            flipped_picture = pygame.transform.flip(display_picture, True, False)
            screen.blit(flipped_picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
            
            


    def attack(self, targets):
        if self.status == 'shot' or self.shooting:
            return  # Don't allow attack while shooting

        self.status = 'attack'
        self.current_frame_index = 0
        self.attack_triggered = False
        self.shooting = True  # Reuse this flag to lock input

    def update_animation(self,shot_bullets):
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
                self.current_picture = self.attack_frames[self.current_frame_index % len(self.attack_frames)]
                if self.current_frame_index == 2 and not getattr(self, 'attack_triggered', False):
                    self.damage_nearby_targets()
                    self.attack_triggered = True
                if self.current_frame_index >= len(self.attack_frames) - 1:
                    self.status = 'idle'
                    self.shooting = False

            self.current_frame_index += 1

    def damage_nearby_targets(self):
        hitbox_range = pygame.Rect(
            self.x_pos - 40 if self.Look == 'left' else self.x_pos + self.width,
            self.y_pos,
            50, 100
        )
        for target in self.targets:
            if hasattr(target, 'hitbox') and hitbox_range.colliderect(target.hitbox):
                target.health -= 50
                print(f"Target hit! Health now: {target.health}")


    def shoot_arrow(self,shot_bullets):
        arrow_x = self.x_pos + (self.width if self.Look == 'right' else -30)
        arrow_y = self.y_pos + self.height // 2
        direction = self.Look
        new_arrow = Arrow(arrow_x, arrow_y, direction, self.arrow_pic)
        self.bullets.append(new_arrow)
        shot_bullets.append(new_arrow)

    def handle_input(self, keys):
        self.is_moving_horizontally = False

        if keys[pygame.K_h] and self.status not in ('shot', 'attack'):
            self.move_left()
            self.is_moving_horizontally = True
        if keys[pygame.K_k] and self.status not in ('shot', 'attack'):
            self.move_right()
            self.is_moving_horizontally = True
        if keys[pygame.K_u]:
            self.jump()

        if keys[pygame.K_j] and not self.shooting and self.status != 'attack':
            self.shooting = True
            self.status = 'shot'
            self.current_frame_index = 0
            self.shot_triggered = False

        if keys[pygame.K_i] and self.status not in ('attack', 'shot'):
            self.status = 'attack'
            self.current_frame_index = 0
            self.attack_triggered = False
            self.attack_targets = self.targets 
            
        if keys[pygame.K_o]:
            self.call_drone()
            print('called')

        if not self.is_moving_horizontally:
            self.stop_horizontal_movement()

    def update_bullets(self, screen, global_bullet_list, platforms, targets,offset):
        
        for arrow in self.bullets[:]:
            if arrow not in global_bullet_list:
                if arrow in self.bullets:
                    self.bullets.remove(arrow)
            arrow.update()

            if arrow.is_off_screen(screen.get_width()):
                if arrow in self.bullets:
                    self.bullets.remove(arrow)
                if arrow in global_bullet_list:
                    global_bullet_list.remove(arrow)
                continue

            for target in targets:
                if hasattr(target, 'hitbox') and arrow.hitbox.colliderect(target.hitbox):
                    target.health -= 30
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
        for drone in self.guard_drone:
            drone.Update(screen, offset, global_bullet_list)




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
            self.vertical_speed = self.jump_strenght
            self.jump_count = 1
            self.on_ground = False
            self.current_platform = None
            self.last_jump_time = current_time
        elif self.jump_count == 1 and self.double_jump_allowed:
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
            if self.x_pos + self.width > platform.x_pos and self.x_pos < platform.x_pos + platform.width:
                if (self.y_pos + self.height >= platform.y_pos) and \
                   (self.y_pos + self.height < platform.y_pos + platform.height + 10) and self.vertical_speed <= 0:
                    self.on_ground = True
                    self.vertical_speed = 0
                    self.y_pos = platform.y_pos - self.height
                    self.current_platform = platform
                    landed = True

                elif (self.y_pos + self.height > platform.y_pos) and (self.y_pos < platform.y_pos + platform.height):
                    if abs(self.x_pos - (platform.x_pos + platform.width)) <= 10:
                        self.allow_move_left = False
                        self.x_pos = platform.x_pos + platform.width
                    elif abs(self.x_pos + self.width - platform.x_pos) <= 10:
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
        if current_time - self.last_guard_call >= self.guard_drone_reload_duration:
            self.guard_drone.append(Guard_Drone(self, "Archer")) 
            self.last_guard_call = current_time
            
            
    def update_drone(self):
        if len(self.guard_drone) == 1:
            current_time = pygame.time.get_ticks()
            drone = self.guard_drone[0]
            if current_time - self.last_guard_call >= self.drone_duration:
                if drone.status != 'departing':
                    drone.status = 'departing'
            if drone.status == 'departing' and drone.is_off_screen_exit():
                self.guard_drone.remove(drone)


class Arrow:
    def __init__(self, x, y, direction, arrow_picture):
        self.x_pos = x
        self.owner = 'Archer'
        self.y_pos = y
        self.speed = 14
        self.direction = direction
        self.picture = arrow_picture
        self.width = arrow_picture.get_width()
        self.height = arrow_picture.get_height()
        self.status = 'in game'

        shrink = 8
        self.hitbox = pygame.Rect(
            self.x_pos + shrink // 2,
            self.y_pos + shrink // 2,
            self.width - shrink,
            self.height - shrink
        )

    def update(self):
        if self.direction == "right":
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed

        shrink = 8
        self.hitbox.topleft = (
            self.x_pos + shrink // 2,
            self.y_pos + shrink // 2
        )

    def draw(self, screen, offset):
        if self.direction == 'right':
            screen.blit(self.picture, (self.x_pos - offset[0], self.y_pos - offset[1]))
        else:
            flipped = pygame.transform.flip(self.picture, True, False)
            screen.blit(flipped, (self.x_pos - offset[0], self.y_pos - offset[1]))

    def is_off_screen(self, screen_width):
        return self.x_pos < -screen_width or self.x_pos > screen_width * 2
    
        
