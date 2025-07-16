import pygame
import os
import math 

class Drone:
    
    
    def __init__(self,x,y,look,targets):
        
        self.health=100
        self.Alive=True
        self.death_frame_flag=False
        self.x_pos=x
        self.y_pos=y
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, 100, 53)
        self.horizentalmove_range=400
        self.status='forward'
        self.prev_status='none'
        self.moved_len=0
        self.speed=2
        self.look=look
        self.targets=targets
        self.target=targets[0]
        self.reload_duration=7000
        self.last_shot=0
        self.aimed=False

        self.shoot_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "freeze drone", "freeze drone shoot.mp3"))     
        self.shot_hit_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "freeze drone", "freezed.mp3"))     
        self.hurt=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "freeze drone", "freeze drone hurt.mp3"))     
    
        
        self.aim_teta=0
        
        
        self.freez_durtation=5000
        self.last_freezed=0   # برای چند تا پلیر باید هندل شن
        
        self.ALIVE=True
        
        
        self.fall_velocity = 0
        self.gravity = 0.5      
                
        
        
        #loading section:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Drone")
        
        self.Idle_frames=[]
        for i in range (4):
            self.Idle_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Idle', f"{i}.png")
                    ),
                    (100,50)
                )
                
            )
            
            
            
        self.Forward_frames=[]
        for i in range (4):
            self.Forward_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Forward', f"{i}.png")
                    ),
                    (100,53)
                )
                
            )
            
            
        self.Back_frames=[]
        for i in range (4):
            self.Back_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Back', f"{i}.png")
                    ),
                    (100,50)
                )
                
            )
        heights=[50,49,47,47,50,38,38,39]  
        self.death_frames=[]
        for i in range(8):
            self.death_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path ,'Death', f"{i}.png")
                    ),
                    (100,heights[i])
                )
                
            )
            
            
        self.display_pic=self.Idle_frames[0] 
        self.animation_speed  = 15 
        self.Last_animationUpdate=0
        self.frame_index=0 
        self.time_falg=0
        self.idle_duration=2000
        
        
        self.bullets=[]
        
            
            
            
    def hurt(self):
        self.hurt.play()            
            
    def display(self, screen, offset):
        screen_width, screen_height = screen.get_size()
        screen_x = self.x_pos - offset[0]
        screen_y = self.y_pos - offset[1]

        if self.look == 'right':
            screen.blit(self.display_pic, (screen_x, screen_y))
        elif self.look == 'left':
            screen.blit(pygame.transform.flip(self.display_pic, True, False), (screen_x, screen_y))

        for bullet in self.bullets:
            bullet.display(screen, offset)
            
        
        
        
    def Update_animtion(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time -  self.Last_animationUpdate 
        if elapsed_time>= self.animation_speed and not self.death_frame_flag:
            if self.status=='idle':
                self.frame_index= (elapsed_time)%len(self.Idle_frames)
                self.display_pic=self.Idle_frames[self.frame_index]
                self.Last_animationUpdate=current_time
            elif self.status=='forward' and self.look=='right':
                self.frame_index= (elapsed_time)%len(self.Forward_frames)
                self.display_pic=self.Forward_frames[self.frame_index]
                self.Last_animationUpdate=current_time
                
            elif self.status=='forward' and self.look=='left':
                self.frame_index= (elapsed_time)%len(self.Back_frames)
                self.display_pic=self.Back_frames[self.frame_index]
                self.Last_animationUpdate=current_time
                
            elif self.status=='backward' and self.look=='right':
                self.frame_index= (elapsed_time)%len(self.Back_frames)
                self.display_pic=self.Back_frames[self.frame_index]
                self.Last_animationUpdate=current_time
            elif self.status=='backward' and self.look=='left':
                self.frame_index= (elapsed_time)%len(self.Forward_frames)
                self.display_pic=self.Forward_frames[self.frame_index]
                self.Last_animationUpdate=current_time
                
            elif self.status == 'dead':
                if current_time - self.Last_animationUpdate >= self.animation_speed and not self.death_frame_flag:
                    if self.frame_index < len(self.death_frames) - 1:
                        self.frame_index += 1
                        self.display_pic = self.death_frames[self.frame_index]
                        self.Last_animationUpdate = current_time
                    else:
                        self.death_frame_flag = True
                        self.display_pic = self.death_frames[-1]
        
        else:
            self.display_pic=self.death_frames[7]
                
                
                
                
        
        
    def Move(self):
        current_time=pygame.time.get_ticks()
        if not self.ALIVE:
            self.fall_velocity += self.gravity
            self.y_pos += self.fall_velocity
            if self.prev_status == 'forward':
                self.x_pos += 1
            elif self.prev_status == 'backward':
                self.x_pos -= 1
            self.hitbox.topleft = (self.x_pos, self.y_pos)
            return
        if self.status=='forward':
            if self.moved_len < self.horizentalmove_range:
                self.x_pos+=self.speed
                self.moved_len+=self.speed
            else:
                self.status='idle'
                self.prev_status='forward'
                self.moved_len=0
                self.time_falg=current_time
        elif self.status=='idle':
            self.moved_len=0
            if current_time-self.time_falg>self.idle_duration:
                if self.prev_status=='forward':
                    self.status='backward'
                    self.time_falg=0
                    self.prev_status='idle'
                else:
                    self.status='forward'
                    self.time_falg=0
                    
                
        elif self.status=='backward':
            if self.moved_len<= self.horizentalmove_range:
                self.x_pos-=self.speed
                self.moved_len+=self.speed
            else:
                self.prev_status='backward'
                self.status='idle'
                self.time_falg=current_time
                
                
        self.hitbox.topleft=(self.x_pos,self.y_pos)
        
    
    
    def Aim(self):
        x=self.target.x_pos
        y=self.target.y_pos
        
        if self.look=='right':
            if y-self.y_pos> 50:
                if  x - self.x_pos > 200:
                    self.aimed=True
                    self.aim_teta=(y-self.y_pos)/(x-self.x_pos)
                    
                    
                    
        elif self.look=='left' :
            if y-self.y_pos> 50:
                if  self.x_pos - x> 200:
                    self.aimed=True
    
    
    
    
    
    def shoot(self):
        current_time=pygame.time.get_ticks()  
        if current_time - self.last_shot>=self.reload_duration and self.target.y_pos > self.y_pos   :
            if self.aimed:
                self.bullets.append(
                    laser(self.x_pos,self.y_pos,self.target.x_pos+30,self.target.y_pos+60,8)
                )
                self.shoot_sound.play()
                self.last_shot=current_time
            
            
            
            
    def Update(self,bullets_in_air):
        self.update_targets()
        self.update_alive()
        self.update_freezing()
        self.Move()
        self.Update_animtion()
        self.Aim()
        self.shoot()
        for bullet in self.bullets:
            bullet.update()
            if bullet.len_of_horizental_move > 20000:    # برای اینکه از اورهد اضافی جلوگیری بشه 
                self.bullets.remove(bullet)
            if bullet.hitbox.colliderect(self.target.hitbox):
                self.target.freezed=True
                self.shot_hit_sound.play()
                self.bullets.remove(bullet)
                self.last_freezed=pygame.time.get_ticks()
                
        for bullet in bullets_in_air:
            
            if self.hitbox.colliderect(bullet.hitbox):
                self.health-=50
                bullets_in_air.remove(bullet)
                
                
    def update_freezing(self):
        current_time = pygame.time.get_ticks()
        if self.target.freezed:
            if current_time - self.last_freezed >= self.freez_durtation or not self.ALIVE:
                self.target.freezed = False

            
            
    def update_alive(self):
        if self.health <= 0 :
            self.prev_status=self.status
            self.status='dead'
            self.ALIVE=False
            
            
    def update_targets(self):
        min_index=0
        distances=[]
        for target in self.targets:
            distances.append(((self.x_pos - target.x_pos)**2) + ((self.y_pos - target.y_pos)**2))
            
            
        for i in range(len(distances)):
            if distances[i] < distances[min_index]:
                min_index=i
                
        self.target=self.targets[min_index]
            
            
            
            
            
   
        
        
            
            
              
                        
                    
                    
        
        
class laser:
    def __init__(self,x,y,target_x,target_y,speed):
        self.x_pos=x
        self.y_pos=y
        self.target_x=target_x
        self.target_y=target_y
        self.teta=(target_y-y)/(target_x - x)         #  یادت نره سایز رکت ها رو درست کنی
        self.speed=speed
        self.len_of_horizental_move=0
        self.hitbox= self.hitbox = pygame.Rect(self.x_pos, self.y_pos, 20, 20)
        self.display_angle=math.degrees(self.teta)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Drone","lazer.png")
        self.image=pygame.transform.scale(
            pygame.image.load(
                path
            ),
            (9,40)
        )
        self.image=pygame.transform.rotate(self.image,self.display_angle)
        
        
        
    def display(self,screen,offset):
        screen.blit(self.image,(self.x_pos-offset[0],self.y_pos-offset[1])) 
         


    def update(self):
        self.x_pos+=self.speed
        self.y_pos+=self.teta*(self.speed)
        self.len_of_horizental_move+=self.speed
        self.hitbox.topleft=(self.x_pos,self.y_pos)
        
        
        
        
        
        

        
        
        
        
        
    
        
        
        
        
                
    
        
        
        
        
        
        
        
        