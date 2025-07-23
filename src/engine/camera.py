import pygame
from config import screen_width, screen_height
import time

class Camera:
    def __init__(self, screen, entities: list):
        (
            self.platforms,
            self.shot_bullets,
            self.hero,
            self.explosions,
            self.scroll,
            self.ninja,
            self.terrorists,
            self.Gates,
            background,
            self.drones,
            self.objects,
            self.gunmans,
            self.archer,
            self.dragonlord,
            self.flyingdemon,
            self.bomb,
            self.defuse_kit
        ) = entities

        self.screen = screen
        
        import os
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "Back.png")
        self.background = pygame.transform.scale(background, (screen_width, screen_height))
        self.test = pygame.transform.scale(pygame.image.load(base_path), (130, 130))

        self.spotlight_active = False
        self.spotlight_start_time = 0
        self.spotlight_duration = 3  

    def activate_spotlight(self):
        self.spotlight_active = True
        self.spotlight_start_time = time.time()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        for platform in self.platforms:
            platform.draw(self.screen, self.scroll)

        for gate in self.Gates:
            gate.display(self.screen, self.scroll)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen, self.scroll)

        self.hero.display(self.screen, self.scroll, self.shot_bullets)
        self.ninja.display(self.screen, self.scroll, self.shot_bullets)

        for terrorist in self.terrorists:
            if terrorist.status != 'removed':
                terrorist.display(self.screen, self.scroll)

        if self.dragonlord:
            self.dragonlord.display(self.screen, self.scroll)
        if self.flyingdemon and self.flyingdemon.ALIVE:
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

        if self.spotlight_active:
            elapsed = time.time() - self.spotlight_start_time
            if elapsed < self.spotlight_duration:
                self.draw_spotlight_on_ninja()
            else:
                self.spotlight_active = False

    def draw_spotlight_on_ninja(self):
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
