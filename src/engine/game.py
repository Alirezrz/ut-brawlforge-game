import pygame
import random
from config import screen_width, screen_height, platform_height, FPS # type: ignore
from src.engine.hero import Hero # type: ignore
from src.engine.bullet import Bullet # type: ignore # type: ignore
from src.engine.enemy import Enemy # type: ignore
from src.engine.platform import Platform # type: ignore
from src.engine.explosion import Explosion # type: ignore
from src.engine.camera import Camera # type: ignore



class Game:
    def __init__(self,screen, hero_picture,bullet_picture,ghost_picture, ghost2_picture, platform_image,background,explosion_picture,health_bar_green,health_bar_red):
        # Initialize game objects
        self.screen = screen
        self.bullet_picture=bullet_picture
        self.background = background
        self.explosion_picture=explosion_picture
        self.clock = pygame.time.Clock()
        self.hero = Hero(0, screen_height - hero_picture.get_height(), hero_picture, screen_width, screen_height,bullet_picture,health_bar_green,health_bar_red)
        self.platforms = [
    Platform(100, 620, 250, platform_image),                            # P1: Bottom-left
    Platform(500, 430, 180, platform_image, moving=True, move_range=100), # P2: Mid-center moving
    Platform(800, 340, 300, platform_image),                            # P3: Mid-right
    Platform(200, 250, 210, platform_image, moving=True, move_range=150,start_direction=-1),                            # P4: Upper-left
]


        self.enemies = []
        self.enemies.append(Enemy(
                random.randint(0,screen_width - ghost_picture.get_width()),
                screen_height - ghost_picture.get_height() - platform_height,
                    3, ghost_picture, ghost2_picture,screen_width,health_bar_green,health_bar_red))
        self.enemies.append(Enemy(
                random.randint(0,screen_width - ghost_picture.get_width()),
                180 - ghost_picture.get_height() - platform_height,
                    3, ghost_picture, ghost2_picture,screen_width,health_bar_green,health_bar_red))
        self.enemies.append(Enemy(
                random.randint(0,screen_width - ghost_picture.get_width()),
                354 - ghost_picture.get_height() - platform_height,
                    3, ghost_picture, ghost2_picture,screen_width,health_bar_green,health_bar_red))
        
        self.shot_bullets = []
        self.explosions=[]
        self.bullet_class =Bullet  
        self.game_active =True
        self.platform_image = pygame.transform.scale(platform_image, (screen_width, platform_height))




        self.camera=Camera(self.screen,self.platforms,self.enemies,self.shot_bullets,self.hero,self.explosions)
        
        
        
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
        self.hero.update_bullets(self.screen,self.shot_bullets) 
        
        

        for bullet in self.shot_bullets:
            for platform in self.platforms:
                platform_hitbox_for_bullets = platform.rect.inflate(-10, -platform.height // 2)
                if bullet.hitbox.colliderect(platform_hitbox_for_bullets):
                    self.explosions.append(Explosion(bullet.x_pos,bullet.y_pos,self.explosion_picture))
                    
                    
                    if bullet in self.shot_bullets:
                        self.shot_bullets.remove(bullet)
                    if bullet in self.hero.bullets:
                        self.hero.bullets.remove(bullet)
                        
                        
                    
                    
                    
                    
                    
        
        
        
        

    def render_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.platform_image, (0, screen_height - platform_height))
        
        
        
    def run(self):
        while self.game_active:
            events = pygame.event.get()
            self.handle_events(events)
            self.handle_inputs()
            self.update()
            self.render_screen()
            self.camera.render()
            pygame.display.update()
            self.clock.tick(FPS)