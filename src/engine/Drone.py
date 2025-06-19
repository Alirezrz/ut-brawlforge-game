import pygame
import os


class Drone:
    
    
    def __init__(self,x,y,look,target):
        
        
        
        self.x_pos=x
        self.y_pos=y
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, 100, 53)
        self.horizentalmove_range=400
        self.status='forward'
        self.prev_status='none'
        self.moved_len=0
        self.speed=2
        self.look=look
        self.target=target
        self.reload_duration=4000
        self.last_shot=0
        self.aimed=False
        
        
        self.aim_teta=0
        
        
        
                
        
        
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
            
        self.display_pic=self.Idle_frames[0] 
        self.animation_speed  = 15 
        self.Last_animationUpdate=0
        self.frame_index=0 
        self.time_falg=0
        self.idle_duration=2000
        
        
        self.bullets=[]
        
            
            
            
            
            
    def display(self,screen,offset):
        
        if self.look=='right':
            screen.blit(self.display_pic,(self.x_pos- offset[0],self.y_pos - offset[1]))
        elif self.look=='left':
            screen.blit(pygame.transform.flip(self.display_pic,True,False),(self.x_pos- offset[0],self.y_pos - offset[1]))
            
        for bullet in self.bullets:
            bullet.display(screen,offset)
            
        
        
        
    def Update_animtion(self):
        current_time=pygame.time.get_ticks()
        elapsed_time=current_time -  self.Last_animationUpdate 
        if elapsed_time>= self.animation_speed:
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
                
                
        
        
    def Move(self):
        current_time=pygame.time.get_ticks()
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
        if current_time - self.last_shot>=self.reload_duration:
            if self.aimed:
                print(self.aim_teta)
                self.bullets.append(
                    bullet(self.x_pos,self.y_pos,self.target.x_pos+60,self.target.y_pos+20,8)
                )
                self.last_shot=current_time
            
            
            
            
    def Update(self):
        self.Move()
        self.Update_animtion()
        self.Aim()
        self.shoot()
        for bullet in self.bullets:
            bullet.update()
            if bullet.hitbox.colliderect(self.target.hitbox):
                print("hit")
            
            
              
                        
                    
                    
        
        
class bullet:
    def __init__(self,x,y,target_x,target_y,speed):
        self.x_pos=x
        self.y_pos=y
        self.target_x=target_x
        self.target_y=target_y
        self.teta=(target_y-y)/(target_x - x)         #  یادت نره سایز رکت ها رو درست کنی
        self.speed=speed
        self.hitbox= self.hitbox = pygame.Rect(self.x_pos, self.y_pos, 20, 20)
        
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Drone","test.png")
        self.image=pygame.transform.scale(
            pygame.image.load(
                path
            ),
            (20,20)
        )
        
        
        
    def display(self,screen,offset):
        screen.blit(self.image,(self.x_pos-offset[0],self.y_pos-offset[1])) 
         


    def update(self):
        self.x_pos+=self.speed
        self.y_pos+=self.teta*(self.speed)
        self.hitbox.topleft=(self.x_pos,self.y_pos)
        
        
        
        
        
    
        
        
        
        
                
    
        
        
        
        
        
        
        
        