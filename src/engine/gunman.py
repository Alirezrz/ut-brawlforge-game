import pygame
import os
import math
from src.engine.bullet import Bullet
class Gunman:
    def __init__(self,x,y,platforms,targets):
        self.x_pos=x
        self.y_pos=y
                          # remember to update the sizes
        self.width=60                                               
        self.height=114
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
        self.targets=targets
        self.status='idle'
        self.prev_status='idle'
        self.Look='right'
        self.last_idle=0
        self.idle_duration=3000
        
        self.platforms=platforms
        #loading section:
        
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "gunman")
        self.bullet_pic=pygame.transform.scale(
            pygame.image.load(
                os.path.join(
                    base_path,"bullet.png"
                )
            ),
            (23,5)
            
        )
        
        
        self.idle_frames=[]
        
        for i in range(4):
            path=os.path.join(base_path , "idle" , f"{i}.png")
            
            self.idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (60,114)
                )
            )
            
        sizes=[51,50,67,74,64,53]
        self.walk_frames=[]
        for i in range(6):
            path=os.path.join(base_path , "walk" , f"{i}.png")
            
            self.walk_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (sizes[i],114)
                )
            )
        sizes=[80,83,83]    
        self.shoot_frames=[]
        for i in range(3):
            path=os.path.join(base_path , "shoot" , f"{i}.png")
            
            self.shoot_frames.append(
                pygame.transform.scale(
                    pygame.image.load(path),
                    (sizes[i],114)
                )
            ) 
            
            
        self.shot_bullets=[]
            
            
        self.display_frame=self.idle_frames[0]    
        self.animation_speed=150
        self.last_animation_update=0
        self.frame_index=0 
        self.shoot_frame_index=0
        self.Walk_Range = 200
        self.VisionRadious = 400
        self.VisionHeight = 80
        self.walk_strength = 1
        self.walked_len = 0
        self.allow_move_right=True
        self.allow_move_left=True
            
        self.idle_start_time=0
        self.idle_time=3000
        
        
        self.last_shoot=0
        self.reload_duration=2000
        
    def display(self,screen,offset):
        if self.Look=='right':
            screen.blit(self.display_frame,(self.x_pos-offset[0],self.y_pos-offset[1]))
        else:
            screen.blit(pygame.transform.flip(self.display_frame,True,False),(self.x_pos-offset[0],self.y_pos-offset[1]))
            
        
        
    def update_animation(self,shot_bullets):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_animation_update
        if self.status=='shoot':
            if elapsed_time >= self.animation_speed:
                self.frame_index = self.shoot_frame_index
                self.display_frame=self.shoot_frames[self.frame_index]
                self.shoot_frame_index+=1
                self.last_animation_update=current_time
                if self.frame_index==1:
                    self.shoot(shot_bullets)
                if self.shoot_frame_index==3:
                    #print("shot")
                    self.status=self.prev_status
                
        elif self.status == 'idle':
            if elapsed_time >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.display_frame = self.idle_frames[self.frame_index]
                self.last_animation_update = current_time

        elif self.status == 'walk':
            if elapsed_time >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.display_frame = self.walk_frames[self.frame_index]
                self.last_animation_update = current_time

            
            
    def Update(self,screen,offset,shot_bullets):
        self.update_animation(shot_bullets)
        self.Walk()
        self.vision()
        self.update_bullets(screen,offset,shot_bullets)
        
        
        
        
        
        
    def Walk(self):
        current_time = pygame.time.get_ticks()
        if self.status=='shoot':
            return
        if self.status=='idle':
            elapsed_time=current_time - self.last_idle
            if elapsed_time > self.idle_duration:
                self.status='walk'
        if self.status=='walk':
            if self.walked_len <= self.Walk_Range:
                if self.Look=='right':
                    self.x_pos+=self.walk_strength
                    self.walked_len+=self.walk_strength
                else :
                    self.x_pos-=self.walk_strength
                    self.walked_len+=self.walk_strength
            
            else :
                self.walked_len=0
                self.status='idle'
                self.last_idle=current_time
                if self.Look=='right':
                    self.Look='left'
                else:
                    self.Look='right'
                    
                    
                
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.display_frame.get_width(), self.display_frame.get_height())





    def vision(self):
        current_time = pygame.time.get_ticks()
        elapsed_time=current_time-self.last_shoot
        for target in self.targets:
            dx = target.x_pos - self.x_pos
            dy = target.y_pos - self.y_pos
            distance = math.hypot(dx, dy)
            if distance <= 500:
                if target.x_pos > self.x_pos and self.Look=='right' and elapsed_time > self.reload_duration :
                    self.prev_status=self.status
                    self.last_shoot=current_time
                    self.shoot_frame_index=0
                    self.status='shoot'
                    return
                elif target.x_pos < self.x_pos and self.Look=='left'and elapsed_time > self.reload_duration :
                    self.prev_status=self.status
                    self.last_shoot=current_time
                    self.shoot_frame_index=0
                    self.status='shoot'
                    return
                
                
    def shoot(self,shot_bullets):
        x=0
        
        if self.Look=='right':
            x=self.x_pos+self.display_frame.get_width()
        else:
            x=self.x_pos
        self.shot_bullets.append(
            Bullet(x,self.y_pos+50,8,self.Look,self.bullet_pic,'gunman')
        )
        shot_bullets.append(self.shot_bullets[len(self.shot_bullets)-1])
        
        
        
    def update_bullets(self,screen,offset,shot_bullets):
        for bullet in self.shot_bullets:
            bullet.update()
            bullet.draw(screen,offset)
            
            
            for hero in self.targets:
                if bullet.hitbox.colliderect(hero.hitbox):
                    hero.health-=20
                    if bullet in  shot_bullets:
                        self.shot_bullets.remove(bullet)
                        shot_bullets.remove(bullet)
                    
                    
            
            
            
        
                
                
            
            