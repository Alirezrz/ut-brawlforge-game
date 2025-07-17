import pygame
import random
import os
from config import screen_width, screen_height, platform_height, FPS
from src.engine.Roboman import Roboman
from src.engine.bullet import Bullet
from src.engine.enemy import Enemy
from src.engine.platform import Platform
from src.engine.explosion import Explosion
from src.engine.camera import Camera
from src.engine.input_handler import InputHandler
from src.levels import level_1_data, load_level_data
from src.engine.Ninja import Ninja
from src.engine.menu import PauseMenu
from src.engine.defuse_kit import DefuseKit
from src.engine.terrorist import Terrorist
from src.engine.teleportgate import Gates
from src.engine.bomb import Bomb
from src.engine.Drone import Drone
from src.engine.pumpkin import Pumpkin
from src.engine.gunman import Gunman
from src.engine.heatlh_box import PowerBox
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer
from src.engine.Dragon_Lord import Dragon_Lord
from src.engine.flyingdemon import FlyingDemon

class Game:
    def __init__(self, screen, hero_picture, ghost_picture, ghost2_picture, platform_image, background, explosion_picture, health_bar_green, health_bar_red, hero_profile_picture, roboman_health_bar_frame, roboman_health_bar, sounds, ninja_health_bar_frame, ninja_health_bar):
        self.screen = screen
        self.background = background
        self.explosion_picture = explosion_picture
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
        self.ninja = NinjaGirl(
            player_start_pos['x'] + 100, player_start_pos['y'],
            screen_width, screen_height,
            [self.Roboman],
            ninja_health_bar_frame, ninja_health_bar
        )


        self.bomb = Bomb(player_start_pos['x'] + 100, player_start_pos['y'] - 500, targets=[self.ninja]) 
        self.defuse_kit=DefuseKit(player_start_pos['x'] + 100, player_start_pos['y'] - 270, targets=[self.ninja])

        self.platforms = load_level_data(level_1_data, platform_image)
        self.screen_color = (60, 100, 150)

        self.scroll = [0, 0]
        self.terrorists = [
            Terrorist(player_start_pos['x'] -500, player_start_pos['y'], screen_width, screen_height, [self.ninja, self.Roboman], self.platforms, self.ninja, self.screen, self.scroll)
        ]

        self.gunmans = [
            Gunman(player_start_pos['x'] + 800, player_start_pos['y'], self.platforms, [self.ninja, self.Roboman])
        ]
        self.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images")
        self.background = pygame.image.load(os.path.join(self.base_path, "city.png"))

        self.shot_bullets = []
        self.explosions = []
        self.bullet_class = Bullet

        self.game_active = True

        self.gates = [
            Gates(player_start_pos['x'], player_start_pos['y'] - 37, player_start_pos['x'] + 1400, player_start_pos['y'] - 357, self.ninja)
        ]

        self.drones = [
            Drone(-400, 40, 'right', [self.ninja, self.Roboman])
        ]
        self.archer = Archer(player_start_pos['x'], player_start_pos['y'],[self.Roboman,self.ninja]+self.gunmans+self.terrorists+self.drones)

        self.Objects = [
            Pumpkin(player_start_pos['x'] + 100, player_start_pos['y'] - 270, [self.ninja, self.Roboman]),
            PowerBox(player_start_pos['x'] + 700, player_start_pos['y'] + 65, [self.Roboman, self.ninja])
        ]
        self.dragonlord=Dragon_Lord(player_start_pos['x'] -200, player_start_pos['y']-62,self.ninja)
        self.flyingdemon=FlyingDemon(player_start_pos['x'] - 800, player_start_pos['y']-18,self.ninja,'right')
        self.camera = Camera(self.screen, self.platforms, self.shot_bullets, self.Roboman, self.explosions, self.scroll, self.ninja, self.terrorists[0], self.gates, self.background, self.drones, self.Objects, self.gunmans,self.archer,self.dragonlord,self.flyingdemon,self.bomb,self.defuse_kit)

        self.shutter_strength = 0
        self.shutter_start_time = 0
        self.shutter_duration = 150

        self.ninja.attack_targets = [self.Roboman] + self.terrorists + self.gunmans + self.drones

        self.input_handler = InputHandler(self.Roboman, self.bullet_class, self.shot_bullets)

    def remove_bullet(self, bullet):
        if bullet in self.shot_bullets:
            self.shot_bullets.remove(bullet)
        if bullet in self.Roboman.bullets:
            self.Roboman.bullets.remove(bullet)
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
        self.Roboman.handle_input(keys, self.gates, self.shot_bullets, self.bullet_class)
        self.ninja.handle_input(keys, self.gates, self.shot_bullets, self.bullet_class, self.trigger_shutter)
        self.archer.handle_input(keys)
        if keys[pygame.K_z]:
            self.bomb.defuse_bomb()

    def update(self):
        keys = pygame.key.get_pressed()
        self.dragonlord.Update(keys,self.platforms)
        for character in [self.Roboman, self.ninja, self.archer]:
            character.is_on_ground()
            character.gravity()
            character.vertical_move()
            character.platforms_collisions(self.platforms)
            character.move_with_platform()
            character.jump_under_platform(self.platforms)

        self.Roboman.update_animation()
        self.Roboman.update_bullets(self.screen, self.shot_bullets, self.platforms, [self.ninja])

        self.ninja.update_animation(self.shot_bullets)
        self.ninja.update_bullets(self.screen, self.shot_bullets, self.platforms, [self.Roboman])

        self.archer.update_animation(self.shot_bullets)
        self.archer.update_bullets( self.screen, self.shot_bullets, self.platforms, [self.Roboman,self.ninja]+self.gunmans+self.drones+self.terrorists,self.scroll)

        for gunman in self.gunmans:
            gunman.Update(self.screen, self.scroll, self.shot_bullets, self.platforms)
        for drone in self.drones:
            drone.Update(self.shot_bullets)

        for terrorist in self.terrorists[:]:
            if terrorist and terrorist.status != 'removed':
                terrorist.Update(self.shot_bullets)
                terrorist.platforms_collisions(self.platforms)
                terrorist.jump_under_platform(self.platforms)
            else:
                self.terrorists.remove(terrorist)

        for platform in self.platforms:
            platform.update()

        self.scroll[0] += ((self.ninja.hitbox.centerx - screen_width / 2 - self.scroll[0])) / 15
        self.scroll[1] += (self.ninja.hitbox.centery - screen_height / 2 - self.scroll[1]) / 15

        for obj in self.Objects:
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

    def trigger_jetpack_shutter(self, strength=5, duration=150):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()

    def trigger_shutter(self, strength=5, duration=100):
        self.shutter_strength = strength
        self.shutter_duration = duration
        self.shutter_start_time = pygame.time.get_ticks()