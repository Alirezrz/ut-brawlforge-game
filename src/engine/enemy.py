import pygame

class Enemy:
    def __init__(self,x,y,speed, ghost_picture, ghost2_picture, screen_width,health_bar_green,health_bar_red):
        self.x_pos =x
        self.y_pos =y
        self.picture = ghost_picture
        self.ghost2_picture = ghost2_picture
        self.health =100
        self.max_health=100
        self.health_bar_green=health_bar_green
        self.health_bar_red=health_bar_red
        self.speed =speed
        self.width = ghost_picture.get_width()
        self.height = ghost_picture.get_height()
        self.screen_width =screen_width
        self.hitbox =pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
        self.condition ='alive'

    def move(self):
        self.x_pos +=self.speed
        if self.x_pos <= 0 or self.x_pos >= self.screen_width - self.width:
            self.x_pos -=self.speed
            self.speed *=-1
        self.hitbox.topleft = (self.x_pos,self.y_pos)

    def display(self, screen):
        self.health_bar_green=pygame.transform.scale(self.health_bar_green, (self.health_bar_red.get_width()*(self.health/self.max_health), 10))
        screen.blit(self.picture,(self.x_pos,self.y_pos))
        screen.blit(self.health_bar_red,(self.x_pos+(self.width/2)-(self.health_bar_red.get_width()/2),self.y_pos-20))
        screen.blit(self.health_bar_green,(self.x_pos+(self.width/2)-(self.health_bar_red.get_width()/2),self.y_pos-20))


    def damage(self, volume):
        self.health -=volume
        self.picture = self.ghost2_picture
        if self.speed <0:
            self.speed =-7
        else:
            self.speed =7
        if self.health ==0:
            self.condition ='dead'
            
            
    def collide(self):
        self.speed = -self.speed
          

