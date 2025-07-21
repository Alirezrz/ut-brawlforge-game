import pygame
import time
from config import screen_width, screen_height, platform_height
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
        

        self.ninja = None
        self.Arman = None
        self.Gates = gates  
        self.archer = None
        self.gunamns = gunmans 

        # New variables for spotlight timing
        self.spotlight_active = False
        self.spotlight_start_time = 0
        self.spotlight_duration = 3  # seconds

    def activate_spotlight(self):
        """Call this method to start the spotlight effect for 3 seconds."""
        self.spotlight_active = True
        self.spotlight_start_time = time.time()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        for platform in self.platforms:
            platform.draw(self.screen, self.scroll)
        
        for gate in self.gates:
            gate.display(self.screen, self.scroll)
            
        for gate in self.Gates:
            gate.display(self.screen, self.scroll)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen, self.scroll)

        self.hero.display(self.screen, self.scroll, self.shot_bullets)
        if self.ninja:
            self.ninja.display(self.screen, self.scroll, self.shot_bullets)

        if self.terrorist and self.terrorist.status != 'removed':
            self.terrorist.display(self.screen, self.scroll)
        
        self.dragonlord.display(self.screen, self.scroll)
        if self.flyingdemon.ALIVE:
            self.flyingdemon.display(self.screen, self.scroll)
        # handeling explosions:
        for gunman in self.gunmans:
            gunman.display(self.screen, self.scroll)
            
        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen, self.scroll):  # If expired, remove it
                self.explosions.remove(explosion)
                
        for drone in self.drones:        
            drone.display(self.screen, self.scroll)
        for obj in self.objects:
            obj.Update(self.screen, self.scroll)
        self.bomb.display(self.screen, self.scroll)
        self.defuse_kit.display(self.screen, self.scroll)
        
        if self.dragonlord:
            self.dragonlord.display(self.screen, self.scroll)
        if self.flyingdemon:
            if self.flyingdemon.ALIVE:
                self.flyingdemon.display(self.screen, self.scroll)

        for gunman in self.gunmans:
            gunman.display(self.screen, self.scroll)

        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen, self.scroll):
                self.explosions.remove(explosion)

        for drone in self.drones:
            drone.display(self.screen, self.scroll)

        for obj in self.objects:
            obj.Update(self.screen, self.scroll)
        if self.bomb:
            self.bomb.display(self.screen, self.scroll)
        if self.defuse_kit:   
            self.defuse_kit.display(self.screen, self.scroll)

        # Check if spotlight effect should be active
        if self.spotlight_active:
            elapsed = time.time() - self.spotlight_start_time
            if elapsed < self.spotlight_duration:
                self.draw_spotlight_on_ninja()
            else:
                self.spotlight_active = False  # Turn off spotlight after 3 sec

    def draw_spotlight_on_ninja(self):
        if not self.ninja or not hasattr(self.ninja, 'hitbox'):
            return

        spotlight_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        spotlight_surface.fill((0, 0, 0, 255))

        ninja_rect = self.ninja.hitbox.move(-self.scroll[0], -self.scroll[1])
        spotlight_center = ninja_rect.center
        spotlight_radius = max(ninja_rect.width, ninja_rect.height) * 3

        steps = 100
        for i in range(steps):
            radius = int(spotlight_radius * (i + 1) / steps)
            alpha = int(255 * ((steps - i) / steps) ** 2)
            gray_value = int(40 + (215 * (i / steps)))
            gray_value = min(gray_value, 255)
            color = (gray_value, gray_value, gray_value, alpha)
            pygame.draw.circle(spotlight_surface, color, spotlight_center, radius)

        pygame.draw.circle(spotlight_surface, (0, 0, 0, 0), spotlight_center, int(spotlight_radius * 0.2))

        self.screen.blit(spotlight_surface, (0, 0))