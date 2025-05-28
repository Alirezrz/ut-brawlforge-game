import pygame


class Explosion:
    
    def __init__(self,x,y,picture,display_time=150):
        self.x_pos=x
        self.y_pos=y
        self.picture=picture
        self.display_time=display_time
        self.start_time=pygame.time.get_ticks()
        
        
        
    def draw(self,screen):
        current_time=pygame.time.get_ticks()
        if current_time - self.start_time < self.display_time:
            screen.blit(self.picture,(self.x_pos,self.y_pos))
            return True
        
        return False
        