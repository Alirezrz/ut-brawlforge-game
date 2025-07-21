import pygame
from config import screen_width, screen_height ,platform_height
import os 

class Camera:
    def __init__(self, screen, platforms, shot_bullets, hero, explosions, scroll, terrorist, gates, background, drones, objects, gunmans, dragonlord, flyingdemon, bomb, defuse_kit):
        self.screen = screen
        self.platforms = platforms
        self.shot_bullets = shot_bullets
        self.hero = hero
        self.bomb = bomb
        self.defuse_kit = defuse_kit
        self.explosions = explosions
        self.scroll = scroll
        self.terrorist = terrorist
        self.gates = gates
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Back.png")
        self.background = pygame.transform.scale(background, (screen_width, screen_height))
        self.test = pygame.transform.scale(pygame.image.load(base_path), (130, 130))
        
        self.drones = drones
        self.objects = objects
        self.gunmans = gunmans
        self.dragonlord = dragonlord
        self.flyingdemon = flyingdemon
        
    def render(self):
        self.screen.blit(self.background,(0,0))
        
        

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen,self.scroll)
        
        
        for gate in self.gates:
            gate.display(self.screen,self.scroll)
            


        for bullet in self.shot_bullets:
            bullet.draw(self.screen,self.scroll)

        self.hero.display(self.screen, self.scroll, self.shot_bullets)

        if self.terrorist and self.terrorist.status != 'removed':
            self.terrorist.display(self.screen, self.scroll)
            
        
        self.dragonlord.display(self.screen,self.scroll)
        if self.flyingdemon.ALIVE:
            self.flyingdemon.display(self.screen,self.scroll)
        #handeling explosions:
        for gunman in self.gunmans:
            gunman.display(self.screen,self.scroll)
            
        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen,self.scroll):  # If expired, remove it
                self.explosions.remove(explosion)
                
                
        for drone in self.drones:        
            drone.display(self.screen,self.scroll)
        for obj in self.objects:
            obj.Update(self.screen,self.scroll)
        self.bomb.display(self.screen,self.scroll)
        self.defuse_kit.display(self.screen,self.scroll)
                
                

        
        