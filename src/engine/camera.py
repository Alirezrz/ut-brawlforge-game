import pygame
from config import screen_width, screen_height ,platform_height
import os 
class Camera:
    
    def __init__(self,screen,platforms,enemies,shot_bullets,hero,explosions,scroll,ninja,Arman,Gate,background,drone,pumpkin,gunamn):
        self.screen=screen
        self.platforms=platforms
        self.enemies=enemies
        self.shot_bullets=shot_bullets
        self.hero=hero
        self.explosions=explosions
        self.scroll=scroll
        self.ninja=ninja
        self.terrorist=Arman
        self.Gate=Gate
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Back.png")
        self.background = pygame.transform.scale(background, (screen_width, screen_height))
        self.test=pygame.transform.scale(pygame.image.load(base_path),(130,130))
        
        self.drone=drone
        self.pumpkin=pumpkin
        
        
        self.gunman=gunamn
        
        
    def render(self):
        self.screen.blit(self.background,(0,0))
        
        

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen,self.scroll)
        self.Gate.display(self.screen,self.scroll)
        for enemy in self.enemies:
            enemy.display(self.screen,self.scroll)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen,self.scroll)

        self.hero.display(self.screen,self.scroll)
        
        self.ninja.display(self.screen, self.scroll,self.shot_bullets)
        if self.terrorist and self.terrorist.status != 'removed':
            self.terrorist.display(self.screen, self.scroll)
        #handeling explosions:
        self.gunman.display(self.screen,self.scroll)
        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen,self.scroll):  # If expired, remove it
                self.explosions.remove(explosion)
                
                
                
        self.drone.display(self.screen,self.scroll)
        
        self.pumpkin.Update(self.screen,self.scroll)
                
                

        
        