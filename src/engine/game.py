import pygame
import random
from config import screen_width, screen_height, platform_height, FPS
from src.engine.hero import Hero
from src.engine.bullet import Bullet
from src.engine.enemy import Enemy
from src.engine.platform import Platform

class Game:
    def __init__(self,screen, hero_picture,bullet_picture,ghost_picture, ghost2_picture, platform_image,background):
        # Initialize game objects
        self.screen = screen
        self.bullet_picture=bullet_picture
        self.background = background
        self.clock = pygame.time.Clock()
        self.hero = Hero(0, screen_height - hero_picture.get_height(), hero_picture, screen_width, screen_height,bullet_picture)
        self.platforms = [
    Platform(150, 520, 180, platform_image),                            # P1: Bottom-left
    Platform(500, 430, 180, platform_image, moving=True, move_range=100), # P2: Mid-center moving
    Platform(850, 340, 160, platform_image),                            # P3: Mid-right
    Platform(300, 250, 160, platform_image),                            # P4: Upper-left
    Platform(700, 160, 160, platform_image),                            # P5: Top-right
]


        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy(
                random.randint(0,screen_width - ghost_picture.get_width()),
                screen_height - ghost_picture.get_height() - platform_height,
                5, ghost_picture, ghost2_picture,screen_width
            ))
        self.shot_bullets = []
        self.bullet_class =Bullet  
        self.game_active =True
        self.platform_image = pygame.transform.scale(platform_image, (screen_width, platform_height))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.hero.shoot(self.shot_bullets, self.bullet_class)

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.hero.move_right()
        if keys[pygame.K_a]:
            self.hero.move_left()
        if keys[pygame.K_SPACE]:
            self.hero.jump()

    def update(self):
        # Update Hero
        self.hero.is_on_ground()
        self.hero.gravity()
        self.hero.vertical_move()
        self.hero.platforms_collisions(self.platforms)
        self.hero.move_with_platform()
        self.hero.jump_under_platform(self.platforms)
        # Update platforms
        for platform in self.platforms:
            platform.update()
        # Update enemies 
        for enemy in self.enemies[:]:
            ALIVE = True
            for bullet in self.shot_bullets[:]:
                if enemy.hitbox.colliderect(bullet.hitbox):
                    self.shot_bullets.remove(bullet)
                    if bullet in self.hero.bullets:
                        self.hero.bullets.remove(bullet)
                    ALIVE = False
                    break
            if ALIVE:
                enemy.move()
            else:
                enemy.damage(50)
                if enemy.condition == 'dead':
                    self.enemies.remove(enemy)

        # Update bullets
        self.hero.update_bullets(self.screen,self.shot_bullets)  # Pass None since drawing is handled in run_game.py

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.platform_image, (0, screen_height - platform_height))
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)

        for enemy in self.enemies:
            enemy.display(self.screen)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen)

        self.hero.display(self.screen)

    def run(self):
        while self.game_active:
            events = pygame.event.get()
            self.handle_events(events)
            self.handle_inputs()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)