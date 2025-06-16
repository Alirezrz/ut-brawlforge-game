import pygame
import random
from config import screen_width, screen_height, platform_height, FPS
from src.engine.Roboman import Roboman
from src.engine.bullet import Bullet
from src.engine.enemy import Enemy
from src.engine.platform import Platform
from src.engine.explosion import Explosion
from src.engine.camera import Camera
from src.engine.input_handler import InputHandler  
from src.levels import level_1_data, load_level 
from src.engine.Ninja import Ninja 
from src.engine.menu import PauseMenu 
from src.engine.terrorist import Terrorist

class Game:
    def __init__(self,screen, hero_picture,ghost_picture, ghost2_picture, platform_image,background,explosion_picture,health_bar_green,health_bar_red,hero_profile_picture, roboman_health_bar_frame,roboman_health_bar, sounds):
        self.screen = screen
        self.background = background
        self.explosion_picture=explosion_picture
        self.clock = pygame.time.Clock()
        self.sounds = sounds
        
        player_start_pos = level_1_data['player_start']
        self.Roboman = Roboman(
            player_start_pos['x'], player_start_pos['y'], 
            roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
            screen_width, screen_height,
            sounds={
                'jump': self.sounds.get('jump'),
                'shoot': self.sounds.get('shoot'),
                'jetpack': self.sounds.get('jetpack')
            },
            trigger_shutter_callback=self.trigger_jetpack_shutter
        )
        self.ninja = Ninja(
    player_start_pos['x'] + 100, player_start_pos['y'], 
    screen_width, screen_height
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
        
        
        
        self.Arman=Terrorist(player_start_pos['x'],player_start_pos['y'], screen_width, screen_height,self.ninja,self.Roboman,self.platforms)
        
        self.shot_bullets = []
        self.explosions=[]
        self.bullet_class =Bullet  
        self.game_active =True
        self.platform_image = pygame.transform.scale(platform_image, (screen_width, platform_height))

        self.scroll=[0,0]

        self.camera = Camera(self.screen, self.platforms, self.enemies, self.shot_bullets, self.Roboman, self.explosions, self.scroll,self.ninja,self.Arman)
        
        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150
        self.input_handler = InputHandler(self.Roboman, self.bullet_class, self.shot_bullets)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.Roboman.shoot(self.shot_bullets, self.bullet_class)
                    
            


    
    def handle_inputs(self):
        keys = pygame.key.get_pressed()
    
    # Reset movement flags
        self.Roboman.is_moving_horizontally = False
        self.ninja_moving = False

    # Roboman controls
        if keys[pygame.K_d]:
            self.Roboman.move_right()
            self.Roboman.is_moving_horizontally = True 
        if keys[pygame.K_a]:
            self.Roboman.move_left()
            self.Roboman.is_moving_horizontally = True 
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_LSHIFT]:
                self.Roboman.activate_jetpack()
            
            else:
                self.Roboman.jump()
        if keys[pygame.K_r]:
            self.Roboman.respawn() 

    # Ninja controls
        if keys[pygame.K_LEFT]:
            self.ninja.move_left()
            self.ninja_moving = True
        if keys[pygame.K_RIGHT]:
            self.ninja.move_right()
            self.ninja_moving = True
        if keys[pygame.K_UP]:
            self.ninja.jump()
        if keys[pygame.K_RSHIFT]:
            if not self.ninja.Super_PowerFlag:  
                self.trigger_shutter(strength=10, duration=1500)
            self.ninja.Activate_Super_Power()
    
        if not self.ninja_moving:
            self.ninja.stop_horizontal_movement()
            
        if keys[pygame.K_RCTRL]:
            self.ninja.shoot(self.shot_bullets, self.bullet_class)
        
             
            
    def update(self):
        self.Roboman.is_on_ground()
        self.Roboman.gravity()
        self.Roboman.vertical_move()
        self.Roboman.platforms_collisions(self.platforms)
        self.Roboman.move_with_platform()
        self.Roboman.jump_under_platform(self.platforms)
        self.Roboman.update_animation() 
        
        self.ninja.is_on_ground()
        self.ninja.gravity()
        self.ninja.vertical_move()
        self.ninja.platforms_collisions(self.platforms)
        self.ninja.move_with_platform()
        self.ninja.jump_under_platform(self.platforms)
        self.ninja.update_animation(self.shot_bullets) 
        self.ninja.update_bullets(self.screen, self.shot_bullets)
        
        
        self.Arman.Update()
        self.Arman.platforms_collisions(self.platforms)
        self.Arman.jump_under_platform(self.platforms)
        
        
        
        
        for platform in self.platforms:
            platform.update()
        
        for enemy in self.enemies[:]:
            ALIVE = True
            for bullet in self.shot_bullets[:]:
                if enemy.hitbox.colliderect(bullet.hitbox):
                    if self.sounds and self.sounds.get('enemy_hit'):
                        self.sounds['enemy_hit'].play()
                        
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

        self.Roboman.update_bullets(self.screen, self.shot_bullets) 
        
        for bullet in self.shot_bullets:
            for platform in self.platforms:
                platform_hitbox_for_bullets = platform.rect.inflate(-10, -platform.height // 2)
                if bullet.hitbox.colliderect(platform_hitbox_for_bullets):
                    if self.sounds and self.sounds.get('explosion'):
                        self.sounds['explosion'].play()
                        
                    self.explosions.append(Explosion(bullet.x_pos, bullet.y_pos, self.explosion_picture))
                    
                    self.shutter_strength = 10  
                    self.shutter_start_time = pygame.time.get_ticks()
                    
                    if bullet in self.shot_bullets:
                        self.shot_bullets.remove(bullet)
                    if bullet in self.Roboman.bullets: 
                        self.Roboman.bullets.remove(bullet)
                        
        self.scroll[0] += (self.ninja.hitbox.centerx - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += ((self.ninja.hitbox.centery - screen_height / 2 - self.scroll[1]) / 15 ) 
                        
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
        self.screen.fill(self.screen_color)
        
    def run(self):
        while self.game_active:
            events = pygame.event.get()
            self.handle_events(events)
            self.handle_inputs() 
            #self.input_handler.handle_all_inputs() 
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_menu = PauseMenu(self.screen,self.background)
                    action = pause_menu.run()
                    if action == "resume":
                        continue
                    elif action == "menu":
                        self.game_active = False
                        return "menu"
                    elif action == "exit":
                        self.game_active = False
                        return "exit"
            self.update()
            self.render_screen()
            self.camera.render()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def trigger_jetpack_shutter(self, strength=5, duration=150):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()
        
    def trigger_shutter(self, strength=5, duration=100):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()