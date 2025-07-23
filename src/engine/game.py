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
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer
from src.engine.menu import PauseMenu,GameModeMenu
from src.levels import level_1_data,level_2_data,level_3_data,level_4_data, load_level_data, build_enemies, build_objects, apply_targets_to_enemies,Boss_fight_level
from src.engine.power_ups import Power_up
from src.engine.Dragon_Lord import Dragon_Lord

BOMB_LEVELS = ["level_1_data", "level_2_data","level_3_data"]
BOSS_LEVELS = ["level_4_data"]
class Game:
    def __init__(self, screen, platform_image, background,selected_char,selected_map):
        self.screen = screen
        self.background = background
        self.clock = pygame.time.Clock()
        self.screen_color = (60, 100, 150)
        self.scroll = [0, 0]
        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet
        self.game_active = True
        if selected_map=="level1":
            self.map=level_1_data
        if selected_map=="level2":
            self.map=level_2_data
        if selected_map=="level3":
            self.map=level_3_data
        if selected_map=="Boss fight":
            self.map=level_4_data        
        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150

        player_start_pos = self.map['player_start']
        if selected_char == "Ninja":
            self.hero = Ninja(
                player_start_pos['x'], player_start_pos['y'],
                screen_width, screen_height,
                [],1  # لیست targets بعداً ست می‌شود
            )
        elif selected_char == "Archer":
            self.hero=Archer(player_start_pos['x'], player_start_pos['y'],
            [],1)

        elif selected_char == "NinjaGirl": 
            self.hero=NinjaGirl(
                player_start_pos['x'], player_start_pos['y'],
                screen_width, screen_height,
                [],1
            ) 

        else:
            self.hero=Roboman(
                player_start_pos['x'], player_start_pos['y'],
                screen_width, screen_height,1
            )

        self.platforms = load_level_data(self.map, platform_image)

        self.enemies_dict = build_enemies(self.map, self.screen, self.scroll, self.platforms)
        all_enemies = []
        for group in self.enemies_dict.values():
            if isinstance(group, list):
                all_enemies.extend(group)
            elif group:  
                all_enemies.append(group)

        self.objects_dict = build_objects(self.map, [self.hero])
        self.objects = self.objects_dict['misc'] + \
                    ([self.objects_dict['bomb']] if self.objects_dict['bomb'] else []) + \
                    ([self.objects_dict['defuse_kit']] if self.objects_dict['defuse_kit'] else []) + \
                    self.objects_dict['gates'] + \
                    self.objects_dict['power ups']
                    
        for obj in self.objects:
            if type(obj)==Power_up:
                obj.targets=[self.hero]
                       
        
        

        # هدف‌گذاری دشمنان
        apply_targets_to_enemies(self.enemies_dict, [self.hero])

        # اهداف حمله نینجا
        self.hero.attack_targets = all_enemies

        
        camera_entities = [
            self.platforms,
            self.shot_bullets,
            self.hero,
            self.explosions,
            self.scroll,
            self.hero,
            self.enemies_dict.get('terrorists'),
            self.objects_dict.get('gates'),
            self.background,
            self.enemies_dict.get('drones'),
            self.objects,
            self.enemies_dict.get('gunmans'),
            None,  # archer, only if needed
            self.enemies_dict.get('dragonlord'),
            self.enemies_dict.get('flyingdemons'),  
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
        
        
        
        self.trigger_shutter = shutter_func
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        mouse_bottons=pygame.mouse.get_pressed()
        if self.objects_dict.get('bomb'):
            self.objects_dict['bomb'].handle_input(keys)
        self.hero.handle_input(keys, self.objects_dict['gates'], self.shot_bullets, self.bullet_class, self.trigger_shutter,mouse_bottons)

    
    def update(self):
        if (self.hero.health <= 0 or self.hero.y_pos > 64 * 50) and self.hero.ALIVE:
            self.hero.die()
        
        if self.enemies_dict.get('dragonlord'):
            self.enemies_dict['dragonlord'].Update(self.screen, self.scroll, self.shot_bullets, self.platforms)

        for character in [self.hero]:
            character.is_on_ground()
            character.gravity()
            character.vertical_move()
            character.platforms_collisions(self.platforms)
            character.move_with_platform()
            character.jump_under_platform(self.platforms)

        self.hero.update_animation(self.shot_bullets)
        self.hero.update_bullets(self.screen, self.shot_bullets, self.platforms, self.enemies)

        for enemy in self.enemies[:]:
            
            if hasattr(enemy, 'Update'):
                enemy.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
            if hasattr(enemy, 'status') and enemy.status == 'removed':
                self.enemies.remove(enemy)
            if hasattr(enemy, 'death_finished') :
                if enemy.death_finished:
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
        game_is_over = False
        final_message = ""
        game_over_start_time = 0
        game_over_delay = 2000
        while self.game_active:
            events = pygame.event.get()
            if not game_is_over:
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
                        return "menu", ""
                    elif action == "exit":
                        self.game_active = False
                        return "exit", "" 

            if not game_is_over:
                self.update()
            self.render_screen()
            self.camera.render()
            
            if not game_is_over:
                win_or_loss_triggered = False
                if self.hero.DEAD:
                    final_message = "You Lost!"
                    win_or_loss_triggered = True
                elif self.map in [level_1_data, level_2_data, level_3_data]:
                    bomb_obj = self.objects_dict.get('bomb')
                    if bomb_obj:
                        if bomb_obj.timer <= 0 and not bomb_obj.is_defused:
                            final_message = "You Lost! Time's Up!"
                            win_or_loss_triggered = True
                        elif bomb_obj.is_defused:
                            final_message = "You Win! Bomb Defused!"
                            win_or_loss_triggered = True
                elif self.map in [level_4_data, Boss_fight_level]:
                    boss = self.enemies_dict.get('dragonlord')
                    if boss and boss.DEAD:
                        final_message = "You Win! Boss Defeated!"
                        win_or_loss_triggered = True

                if win_or_loss_triggered:
                    game_is_over = True
                    game_over_start_time = pygame.time.get_ticks()
            
            if game_is_over:
                if pygame.time.get_ticks() - game_over_start_time > game_over_delay:
                    self.game_active = False
                    return "game_over", final_message
                
            pygame.display.update()
            self.clock.tick(FPS)
            
        return "menu", ""
