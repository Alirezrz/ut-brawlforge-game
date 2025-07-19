import pygame 
import os

import math


class DefuseKit:
    def __init__(self,x,y,targets):
        
        
        self.x_pos=x
        self.y_pos=y
        self.targets=targets

        self.width=40
        self.height=63
        
        self.pic=pygame.image.load("src/assets/images/bomb/defuse kit.png")
        self.pic=pygame.transform.scale(self.pic, (self.width, self.height))

        self.is_finded=False    
        
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)        
        
     
        
    def display(self,screen,offset):
        if not self.is_finded:
            screen.blit(self.pic,(self.x_pos-offset[0],self.y_pos-offset[1]))
        self.Update()    
       
        

   
            
            
    def Update(self,screen,scroll):
        for target in self.targets:
            if target.hitbox.colliderect(self.hitbox):
                target.has_defuse_kit=True
                self.is_finded=True


       
    
        
            
