import pygame
import random
import os
from config import screen_width, screen_height, FPS
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.explosion import Explosion
from src.engine.camera import Camera
from src.engine.input_handler import InputHandler
from src.engine.Ninja import Ninja
from src.engine.Roboman import Roboman
from src.engine.menu import PauseMenu
from src.levels import get_level_data, load_platforms, load_enemies, load_objects, get_start_position, apply_targets_to_enemies

class Game_2:
    def __init__(self, screen, platform_image, background,
                explosion_picture,
                sounds,ninja_health_bar_frame,ninja_health_bar,
                roboman_health_bar_frame, roboman_health_bar,
                hero_profile_picture,selected_map='multiplayer_arena',hero1=None,hero2=None
                ):

        self.screen = screen
        self.background = background
        self.explosion_picture = explosion_picture
        self.clock = pygame.time.Clock()
        self.sounds = sounds
        self.selected_map = selected_map
        self.screen_color = (60, 100, 150)
        self.scroll = [0, 0]
        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet
        self.game_active = True

        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150
        level_data =get_level_data(self.selected_map)
        player_start_pos = level_data['player_start']
        player2_start_pos = level_data['player2_start']

        self.hero = Ninja(
            player_start_pos['x'], player_start_pos['y'],
            screen_width, screen_height,
            [],
            ninja_health_bar_frame, ninja_health_bar,
            1  # لیست targets بعداً ست می‌شود
        )
        self.hero2=Roboman(player2_start_pos['x'], player2_start_pos['y'],
            roboman_health_bar_frame, roboman_health_bar, hero_profile_picture, # اضافه کردن
            screen_width, screen_height,
            sounds, None, 2)

        self.platforms = load_platforms(self.selected_map,platform_image)

        self.enemies_dict = load_enemies(self.selected_map, self.screen, self.scroll, self.platforms)
        all_enemies = []
        for group in self.enemies_dict.values():
            if isinstance(group, list):
                all_enemies.extend(group)
            elif group:  
                all_enemies.append(group)
        all_players=[self.hero,self.hero2]
        self.objects_dict = load_objects(self.selected_map, all_players)
        self.bomb = self.objects_dict.get('bomb')
        self.defuse_kit = self.objects_dict.get('defuse_kit')
        self.gates = self.objects_dict.get('gates', [])
        self.objects = self.objects_dict.get('misc', []) + self.gates


        # هدف‌گذاری دشمنان
        apply_targets_to_enemies(self.enemies_dict, all_players)

        # اهداف حمله نینجا
        self.hero.attack_targets = all_enemies + [self.hero2]
        self.hero2.attack_targets  = all_enemies + [self.hero]

        
        self.camera = Camera(
            self.screen, self.platforms, self.shot_bullets, self.hero, 
           
            self.explosions, self.scroll,
            next(iter(self.enemies_dict.get('terrorists', [])), None),
            self.gates, self.background,
            self.enemies_dict.get('drones', []),
            self.objects,
            self.enemies_dict.get('gunmans', []),
            self.enemies_dict.get('dragonlord'),
            next(iter(self.enemies_dict.get('flyingdemons', [])), None),
            self.bomb,
            self.defuse_kit,hero2=self.hero2
        )

        self.enemies = all_enemies
        self.input_handler = InputHandler(None, self.bullet_class, self.shot_bullets)
        if self.enemies_dict.get('dragonlord'):
            self.enemies_dict['dragonlord'].camera = self.camera

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        if self.objects_dict.get('bomb'):
            self.objects_dict['bomb'].handle_input(keys)
        self.hero.handle_input(keys, self.objects_dict['gates'], self.shot_bullets, self.bullet_class, self.trigger_shutter)
        self.hero2.handle_input(keys, self.objects_dict['gates'], self.shot_bullets, self.bullet_class, self.trigger_shutter)

    def update(self):
        keys = pygame.key.get_pressed()

        if self.enemies_dict.get('dragonlord'):
            self.enemies_dict['dragonlord'].Update(self.screen, self.scroll, self.shot_bullets, self.platforms)

        for character in [self.hero,self.hero2]:
            character.is_on_ground()
            character.gravity()
            character.vertical_move()
            character.platforms_collisions(self.platforms)
            character.move_with_platform()
            character.jump_under_platform(self.platforms)

        self.hero.update_animation(self.shot_bullets)
        self.hero2.update_animation(self.shot_bullets)
        self.hero.update_bullets(self.screen,self.shot_bullets, self.platforms, self.enemies+[self.hero2])
        self.hero2.update_bullets(self.shot_bullets, self.platforms, self.enemies+[self.hero])

        for enemy in self.enemies[:]:
            if hasattr(enemy, 'Update'):
                enemy.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
            if hasattr(enemy, 'status') and enemy.status == 'removed':
                self.enemies.remove(enemy)

        for platform in self.platforms:
            platform.update()

        self.scroll[0] += ((self.hero.hitbox.centerx - screen_width / 2 - self.scroll[0])) / 15
        self.scroll[1] += (self.hero.hitbox.centery - screen_height / 2 - self.scroll[1]) / 15

        for obj in self.objects:
            obj.Update(self.screen, self.scroll)

        current_time = pygame.time.get_ticks()
        if self.shutter_strength > 0:
            shuttered_time = current_time - self.shutter_start_time
            if shuttered_time < self.shutter_duration:
                shake_x = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                shake_y = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                self.camera.scroll[0] += shake_x
                self.camera.scroll[1] += shake_y
                decay_factor = shuttered_time / self.shutter_duration
                self.shutter_strength = max(0, 10 - (10 * decay_factor))
            else:
                self.shutter_strength = 0

    def render_screen(self):
        self.screen.fill(self.screen_color)

    def run(self):
        while self.game_active:
            events = pygame.event.get()
            self.handle_inputs()
            self.handle_events(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_menu = PauseMenu(self.screen, self.background)
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

    def trigger_shutter(self, strength=5, duration=100):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()
