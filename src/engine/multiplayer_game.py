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
from src.engine.Archer import Archer
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Roboman import Roboman
from src.engine.menu import PauseMenu
from src.engine.power_ups import Power_up
from src.levels import multiplayer_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies

class Game_2:
    def __init__(self, screen, platform_image, background, selected_char, selected_char2):
        self.screen = screen
        self.background = background
        self.clock = pygame.time.Clock()
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

        self.hero = self.create_hero(selected_char, player_start_pos, 1)
        self.hero2 = self.create_hero(selected_char2, player2_start_pos, 2)

        self.platforms = load_level_data(multiplayer_data, platform_image)
        self.power_ups = [Power_up(player_start_pos['x']-100, player_start_pos['y'], 'guard drone', [self.hero, self.hero2])]

        self.enemies_dict = build_enemies(multiplayer_data, self.screen, self.scroll, self.platforms)
        all_enemies = [enemy for group in self.enemies_dict.values() if group for enemy in (group if isinstance(group, list) else [group])]

        self.objects_dict = build_objects(multiplayer_data, [self.hero, self.hero2])

        self.objects = self.objects_dict['misc'] + \
                    ([self.objects_dict['bomb']] if self.objects_dict['bomb'] else []) + \
                    ([self.objects_dict['defuse_kit']] if self.objects_dict['defuse_kit'] else []) + \
                    self.objects_dict['gates'] + \
                    self.objects_dict.get('power ups', [])

        for obj in self.objects:
            if isinstance(obj, Power_up):
                obj.targets = [self.hero, self.hero2]


        apply_targets_to_enemies(self.enemies_dict, [self.hero, self.hero2])

        self.hero.attack_targets = all_enemies + [self.hero2]
        self.hero2.attack_targets = all_enemies + [self.hero]

        camera_entities = [
            self.platforms,
            self.shot_bullets,
            self.hero,
            self.explosions,
            self.scroll,
            self.hero2,
            self.enemies_dict.get('terrorists'),
            self.objects_dict.get('gates'),
            self.background,
            self.enemies_dict.get('drones'),
            self.objects,
            self.enemies_dict.get('gunmans'),
            None,
            self.enemies_dict.get('dragonlord'),
            next(iter(self.enemies_dict.get('flyingdemons', [])), None),
            self.objects_dict.get('bomb'),
            self.objects_dict.get('defuse_kit')
        ]
        self.camera = Camera(self.screen, camera_entities)


        self.enemies = all_enemies
        self.input_handler = InputHandler(None, self.bullet_class, self.shot_bullets)
        if self.enemies_dict.get('dragonlord'):
            self.enemies_dict['dragonlord'].camera = self.camera
            
        def shutter_func(strength=5, duration=100):
            self.shutter_strength = strength
            self.shutter_duration = duration
            self.shutter_start_time = pygame.time.get_ticks()
        self.trigger_shutter = shutter_func


    def create_hero(self, char_name, start_pos, player_id):
        if char_name == "Ninja":
            return Ninja(start_pos['x'], start_pos['y'], screen_width, screen_height, [], player_id)
        elif char_name == "Archer":
            return Archer(start_pos['x'], start_pos['y'], [], player_id)
        elif char_name == "NinjaGirl":
            return NinjaGirl(start_pos['x'], start_pos['y'], screen_width, screen_height, [], player_id)
        else:
            return Roboman(start_pos['x'], start_pos['y'], screen_width, screen_height, player_id)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.objects_dict.get('bomb'):
            self.objects_dict['bomb'].handle_input(keys)
        self.hero.handle_input(keys, self.objects_dict['gates'], self.shot_bullets, self.bullet_class, self.trigger_shutter, mouse_buttons)
        self.hero2.handle_input(keys, self.objects_dict['gates'], self.shot_bullets, self.bullet_class, self.trigger_shutter, mouse_buttons)
    

    def update(self):
        for hero in [self.hero,self.hero2]:
            if hero.y_pos>64*50:
                hero.health=0
        
        if self.enemies_dict.get('dragonlord'):
            self.enemies_dict['dragonlord'].Update(self.screen, self.scroll, self.shot_bullets, self.platforms)

        for character in [self.hero, self.hero2]:
            character.is_on_ground()
            character.gravity()
            character.vertical_move()
            character.platforms_collisions(self.platforms)
            character.move_with_platform()
            character.jump_under_platform(self.platforms)
            character.update_animation(self.shot_bullets)
            if character == self.hero:
                other_player = self.hero2
            else:
                other_player = self.hero
            
            all_targets = self.enemies + [other_player]
            character.update_bullets(self.screen, self.shot_bullets, self.platforms, all_targets)
        for enemy in self.enemies[:]:
            if hasattr(enemy, 'Update'):
                enemy.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
            if getattr(enemy, 'status', '') == 'removed':
                self.enemies.remove(enemy)

        for platform in self.platforms:
            platform.update()

        mid_x = (self.hero.hitbox.centerx + self.hero2.hitbox.centerx) / 2
        mid_y = (self.hero.hitbox.centery + self.hero2.hitbox.centery) / 2

        self.scroll[0] += (mid_x - screen_width / 2 - self.scroll[0]) / 15
        self.scroll[1] += (mid_y - screen_height / 2 - self.scroll[1]) / 15

        for obj in self.objects:
            obj.Update(self.screen, self.scroll)

        current_time = pygame.time.get_ticks()
        if self.shutter_strength > 0:
            elapsed = current_time - self.shutter_start_time
            if elapsed < self.shutter_duration:
                shake_x = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                shake_y = random.randint(-int(self.shutter_strength), int(self.shutter_strength))
                self.camera.scroll[0] += shake_x
                self.camera.scroll[1] += shake_y
                decay = elapsed / self.shutter_duration
                self.shutter_strength = max(0, 10 - (10 * decay))
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
                        return "menu", "" # Return a tuple
                    elif action == "exit":
                        self.game_active = False
                        return "exit", "" # Return a tuple

            self.update()
            self.render_screen()
            self.camera.render()
            message = ""
            game_over = False

            if self.hero.health <= 0:
                message = "Player 2 Wins!"
                game_over = True
            elif self.hero2.health <= 0:
                message = "Player 1 Wins!"
                game_over = True

            if game_over:
                self.game_active = False
                return "game_over", message
            

            pygame.display.update()
            self.clock.tick(FPS)

        return "menu", ""