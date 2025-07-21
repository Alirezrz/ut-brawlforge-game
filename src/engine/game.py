import pygame
import random
import os
from config import screen_width, screen_height, platform_height, FPS
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.explosion import Explosion
from src.engine.camera import Camera
from src.engine.input_handler import InputHandler
from src.levels import get_level_data, load_platforms, load_enemies, load_objects, load_gates, apply_targets_to_enemies
from src.engine.menu import PauseMenu
from src.engine.defuse_kit import DefuseKit
from src.engine.terrorist import Terrorist
from src.engine.teleportgate import Gates
from src.engine.bomb import Bomb
from src.engine.Drone import Drone
from src.engine.pumpkin import Pumpkin
from src.engine.gunman import Gunman
from src.engine.heatlh_box import PowerBox
from src.engine.Dragon_Lord import Dragon_Lord
from src.engine.flyingdemon import FlyingDemon
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer

class Game:
    def __init__(self, screen, hero_picture, ghost_picture, ghost2_picture, platform_image, background, explosion_picture, health_bar_green, health_bar_red, hero_profile_picture, roboman_health_bar_frame, roboman_health_bar, sounds, ninja_health_bar_frame, ninja_health_bar, archer_health_bar_frame, archer_health_bar, main_character=None,selected_map='level_1'):
        self.screen = screen
        self.background = background
        self.explosion_picture = explosion_picture
        self.clock = pygame.time.Clock()
        self.sounds = sounds
        self.selected_map = selected_map
        self.screen_color = (60, 100, 150)
        self.scroll = [0, 0]
 
        level_data= get_level_data(self.selected_map)
        player_start_pos = level_data['player_start']
        self.main_character = main_character
        if self.main_character is None:
            self.main_character = Roboman(player_start_pos['x'], player_start_pos['y'], 
                                          roboman_health_bar_frame, roboman_health_bar, hero_profile_picture, 
                                          screen_width, screen_height, sounds=sounds)
        else:
            self.main_character.x_pos = player_start_pos['x']
            self.main_character.y_pos = player_start_pos['y']
            self.main_character.hitbox.topleft = (player_start_pos['x'], player_start_pos['y'])


        self.platforms = load_platforms(self.selected_map, platform_image)
        all_players = [self.main_character]
        enemies_data = load_enemies(self.selected_map, self.screen, self.scroll, self.platforms)
        self.terrorists = enemies_data.get('terrorists', [])
        self.gunmans = enemies_data.get('gunmans', [])
        self.drones = enemies_data.get('drones', [])
        self.flyingdemons = enemies_data.get('flyingdemons', [])
        self.dragonlord = enemies_data.get('dragonlord') 
        objects_data = load_objects(self.selected_map, all_players)
        self.bomb = Bomb(player_start_pos['x'] + 100, player_start_pos['y'] - 500, targets=[self.main_character]) 
        self.defuse_kit = DefuseKit(player_start_pos['x'] + 100, player_start_pos['y'] - 270, targets=[self.main_character])
        self.gates = objects_data.get('gates', []) 
        self.objects = objects_data.get('misc', []) + self.gates 
        apply_targets_to_enemies(enemies_data, all_players)
        all_enemies_list = []
        for group in enemies_data.values():
            if isinstance(group, list):
                all_enemies_list.extend(group)
            elif group:
                all_enemies_list.append(group)
        self.main_character.targets = all_enemies_list

        # self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images")

        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet
        self.game_active = True
        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150
        self.camera = Camera(self.screen, self.platforms, self.shot_bullets, self.main_character, self.explosions, self.scroll, 
                             next(iter(self.terrorists), None), # terrorist
                             self.gates, self.background, 
                             self.drones, self.objects, self.gunmans, self.dragonlord, 
                             next(iter(self.flyingdemons), None), # flyingdemon
                             self.bomb, self.defuse_kit)
        if self.dragonlord:
            self.dragonlord.camera = self.camera
        self.enemies = all_enemies_list
        self.input_handler = InputHandler(self.main_character, self.bullet_class, self.shot_bullets)
    def remove_bullet(self, bullet):
        if bullet in self.shot_bullets:
            self.shot_bullets.remove(bullet)
        if bullet in self.main_character.bullets:
            self.main_character.bullets.remove(bullet)
        for gunman in self.gunmans:
            if bullet in gunman.shot_bullets:
                gunman.shot_bullets.remove(bullet)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        if isinstance(self.main_character, Roboman):
            self.main_character.handle_input(keys, self.gates, self.shot_bullets, self.bullet_class,self.trigger_shutter)
        elif isinstance(self.main_character, Ninja) or isinstance(self.main_character, NinjaGirl):
            self.main_character.handle_input(keys, self.gates, self.shot_bullets, self.bullet_class,self.trigger_shutter)
        elif isinstance(self.main_character, Archer):
            self.main_character.handle_input(keys,self.gates)

    def update(self):
        keys = pygame.key.get_pressed()
        if self.dragonlord: 
            self.dragonlord.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
        self.update_enemies()
        self.main_character.is_on_ground()
        self.main_character.gravity()
        self.main_character.vertical_move()
        self.main_character.platforms_collisions(self.platforms)
        self.main_character.move_with_platform()
        self.main_character.jump_under_platform(self.platforms)

        # فراخوانی update بر اساس کاراکتر
        if isinstance(self.main_character, Roboman):
            self.main_character.update(self.platforms, self.shot_bullets, self.enemies, keys, self.gates)
        elif isinstance(self.main_character, Ninja) or isinstance(self.main_character, NinjaGirl):
            self.main_character.update(self.screen,self.platforms, self.shot_bullets, self.enemies, keys, self.gates)
        elif isinstance(self.main_character, Archer):
            self.main_character.update(self.screen,self.platforms, self.shot_bullets, self.enemies, keys,self.gates,self.scroll)


        for gunman in self.gunmans:
            gunman.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
        for drone in self.drones:
            drone.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)

        for terrorist in self.terrorists[:]:
            if terrorist and terrorist.status != 'removed':
                terrorist.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
            else:
                self.terrorists.remove(terrorist)

        for platform in self.platforms:
            platform.update()

        self.scroll[0] += ((self.main_character.hitbox.centerx - screen_width / 2 - self.scroll[0])) / 15
        self.scroll[1] += (self.main_character.hitbox.centery - screen_height / 2 - self.scroll[1]) / 15

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
        
    def update_enemies(self):
        keys = pygame.key.get_pressed()
        for enemy in self.enemies[:]:
            if hasattr(enemy, 'Update'):
                if isinstance(enemy, Dragon_Lord):
                    enemy.Update(self.screen, self.scroll, self.shot_bullets,self.platforms)
                else:
                    enemy.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
            if hasattr(enemy, 'status') and enemy.status == 'removed':
                self.enemies.remove(enemy)
                
    def cleanup_dead_entities(self):
        self.enemies = [e for e in self.enemies if not hasattr(e, 'death_finished') or not getattr(e, 'death_finished')]
        self.terrorists = [e for e in self.enemies if isinstance(e, Terrorist)]
        self.gunmans = [e for e in self.enemies if isinstance(e, Gunman)]
        self.drones = [e for e in self.enemies if isinstance(e, Drone)]
        self.flyingdemons = [e for e in self.enemies if isinstance(e, FlyingDemon)]
