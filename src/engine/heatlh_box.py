import os 
import pygame


class PowerBox:
    def __init__(self,x,y,targets):
        self.x_pos=x
        self.y_pos=y
        self.targets=targets
        self.status='exist'
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Objects","health_box","Box.png")

        self.picture=pygame.transform.scale(
        pygame.image.load(path),
        (57,45)
        )
        self.hitbox=pygame.Rect(self.x_pos,self.y_pos,self.picture.get_width(),self.picture.get_height())
        
        
        
        
    def display(self,screen,offset):
        if self.status!='used':
            screen.blit(self.picture,(self.x_pos-offset[0],self.y_pos-offset[1]))
        
        
    def Update(self,screen,offset):
        self.display(screen,offset)
        for t in self.targets:
            if t.hitbox.colliderect(self.hitbox) and self.status!='used':
                if t.health<=70:
                    t.health+=30
                    self.status='used'
                elif t.health<100:
                    t.health=100
                    self.status='used'
                    
                