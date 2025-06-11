import pygame
import random
from config import screen_width, screen_height, platform_height, FPS # type: ignore
from src.engine.Roboman import Roboman # type: ignore
from src.engine.bullet import Bullet # type: ignore
from src.engine.enemy import Enemy # type: ignore
from src.engine.platform import Platform # type: ignore
from src.engine.explosion import Explosion # type: ignore
from src.engine.camera import Camera # type: ignore
from src.engine.input_handler import InputHandler  
from src.levels import level_1_data, load_level 

class Game:
    def __init__(self,screen, hero_picture,ghost_picture, ghost2_picture, platform_image,background,explosion_picture,health_bar_green,health_bar_red,hero_profile_picture, roboman_health_bar_frame,roboman_health_bar):
        self.screen = screen
        self.background = background
        self.explosion_picture=explosion_picture
        self.clock = pygame.time.Clock()
        
    
        player_start_pos = level_1_data['player_start']
        self.Roboman = Roboman(
            player_start_pos['x'], player_start_pos['y'], 
            roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
            screen_width, screen_height,
            trigger_shutter_callback=self.trigger_jetpack_shutter
        )

        self.platforms = load_level(level_1_data, platform_image)

        self.screen_color=(60,100,150) 
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

        self.scroll=[0,0] # Camera scroll offset

        self.camera = Camera(self.screen, self.platforms, self.enemies, self.shot_bullets, self.Roboman, self.explosions, self.scroll)
        
        # Screen shutter effect variables for explosions 
        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150 #  <---- milliseconds
        self.input_handler = InputHandler(self.Roboman, self.bullet_class, self.shot_bullets)

    def handle_events(self, events):
        """Handles Pygame events like quitting and mouse clicks."""
        for event in events:
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.Roboman.shoot(self.shot_bullets, self.bullet_class)

    def handle_inputs(self):
        """Handles keyboard inputs (legacy, now mostly in InputHandler)."""
        keys = pygame.key.get_pressed()
        self.Roboman.is_moving_horizontally = False

        if keys[pygame.K_d]:
            self.Roboman.move_right()
            self.Roboman.is_moving_horizontally = True 
        if keys[pygame.K_a]:
            self.Roboman.move_left()
            self.Roboman.is_moving_horizontally = True 
        if keys[pygame.K_SPACE]:
            self.Roboman.jump()
        if keys[pygame.K_r]:
            self.Roboman.respawn()  
            
    def update(self):
        """Updates game state including character, enemies, and bullets."""
        # Update Roboman
        self.Roboman.is_on_ground()
        self.Roboman.gravity()
        self.Roboman.vertical_move()
        self.Roboman.platforms_collisions(self.platforms)
        self.Roboman.move_with_platform()
        self.Roboman.jump_under_platform(self.platforms)
        self.Roboman.update_animation() 
        
        # Update platforms
        for platform in self.platforms:
            platform.update()
        
        # Update enemies 
        for enemy in self.enemies[:]:
            ALIVE = True
            for bullet in self.shot_bullets[:]:
                if enemy.hitbox.colliderect(bullet.hitbox):
                    self.shot_bullets.remove(bullet)
                    if bullet in self.Roboman.bullets: 
                        self.Roboman.bullets.remove(bullet)
                    ALIVE = False
                    break
            if ALIVE:
                enemy.move()
            else:
                enemy.damage(20)
                if enemy.condition == 'dead':
                    self.enemies.remove(enemy)

        # Update bullets shot by Roboman
        self.Roboman.update_bullets(self.screen, self.shot_bullets) 
        
        for bullet in self.shot_bullets:
            for platform in self.platforms:
                platform_hitbox_for_bullets = platform.rect.inflate(-10, -platform.height // 2)
                if bullet.hitbox.colliderect(platform_hitbox_for_bullets):
                    self.explosions.append(Explosion(bullet.x_pos, bullet.y_pos, self.explosion_picture))
                    
                    self.shutter_strength = 10  
                    self.shutter_start_time = pygame.time.get_ticks()
                    
                    if bullet in self.shot_bullets:
                        self.shot_bullets.remove(bullet)
                    if bullet in self.Roboman.bullets: 
                        self.Roboman.bullets.remove(bullet)
                        
        # Updating camera scroll:
        # Use Roboman's hitbox for camera centering
        self.scroll[0] += (self.Roboman.hitbox.centerx - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += ((self.Roboman.hitbox.centery - screen_height / 2 - self.scroll[1]) / 15 ) 
                        
        # Shutter effect if it is active
        current_time = pygame.time.get_ticks()
        if self.shutter_strength > 0:
            shttered_time = current_time - self.shutter_start_time
            if shttered_time < self.shutter_duration:
                shake_x = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                shake_y = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                self.camera.scroll[0] += shake_x
                self.camera.scroll[1] += shake_y
                decay_factor = shttered_time / self.shutter_duration
                self.shutter_strength = max(0, 10 - (10 * decay_factor)) 
            else:
                self.shutter_strength = 0           
        
    def render_screen(self):
        """Fills the screen background."""
        self.screen.fill(self.screen_color)
        
    def run(self):
        """Main game loop."""
        while self.game_active:
            events = pygame.event.get()
            self.handle_events(events)
            self.input_handler.handle_all_inputs() # Use the input handler

            self.update()
            self.render_screen()
            self.camera.render()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def trigger_jetpack_shutter(self, strength=5, duration=150):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()

