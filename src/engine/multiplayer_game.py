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
from src.levels import multiplayer_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies

class Game_2:
    def __init__(self, screen, platform_image, background,
                explosion_picture,
                sounds,ninja_health_bar_frame,ninja_health_bar,
                roboman_health_bar_frame, roboman_health_bar,
                hero_profile_picture
                ):

        self.screen = screen
        self.background = background
        self.explosion_picture = explosion_picture
        self.clock = pygame.time.Clock()
        self.sounds = sounds

        self.screen_color = (60, 100, 150)
        self.scroll = [0, 0]
        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet
        self.game_active = True

        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150

        player_start_pos = multiplayer_data['player_start']
        player2_start_pos = multiplayer_data['player2_start']

        self.hero = Ninja(
            player_start_pos['x'], player_start_pos['y'],
            screen_width, screen_height,
            [],
            ninja_health_bar_frame, ninja_health_bar, #موقتا برای دیباگ
            1  # لیست targets بعداً ست می‌شود
        )
        self.hero2=Roboman(player2_start_pos['x'], player2_start_pos['y'],
            roboman_health_bar_frame, roboman_health_bar, hero_profile_picture, # اضافه کردن
            screen_width, screen_height,
            sounds, None, 2)

        self.platforms = load_level_data(multiplayer_data, platform_image)

        self.enemies_dict = build_enemies(multiplayer_data, self.screen, self.scroll, self.platforms)
        all_enemies = []
        for group in self.enemies_dict.values():
            if isinstance(group, list):
                all_enemies.extend(group)
            elif group:  
                all_enemies.append(group)

        self.objects_dict = build_objects(multiplayer_data, [self.hero,self.hero2])
        self.objects = self.objects_dict['misc'] + \
                       ([self.objects_dict['bomb']] if self.objects_dict['bomb'] else []) + \
                       ([self.objects_dict['defuse_kit']] if self.objects_dict['defuse_kit'] else []) + \
                       self.objects_dict['gates']

        # هدف‌گذاری دشمنان
        apply_targets_to_enemies(self.enemies_dict, [self.hero,self.hero2])

        # اهداف حمله نینجا
        self.hero.attack_targets = all_enemies + [self.hero2]
        self.hero2.attack_targets = all_enemies + [self.hero]

        
        self.camera = Camera(
            self.screen, self.platforms, self.shot_bullets, self.hero2,
            self.explosions, self.scroll, self.hero,
            next(iter(self.enemies_dict['terrorists']), None),
            self.objects_dict['gates'], self.background,
            self.enemies_dict['drones'],
            self.objects,
            self.enemies_dict['gunmans'],  
            self.enemies_dict.get('dragonlord'),
            next(iter(self.enemies_dict['flyingdemons']), None),
            self.objects_dict['bomb'],
            self.objects_dict['defuse_kit']
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
        self.hero.update_bullets(self.screen, self.shot_bullets, self.platforms, self.enemies+[self.hero2])
        self.hero2.update_bullets(self.screen, self.shot_bullets, self.platforms, self.enemies+[self.hero])

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
