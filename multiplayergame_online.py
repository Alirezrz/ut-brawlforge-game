import socket
import threading
import json
import pygame
import random
import os
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer
from config import screen_width, screen_height
from src.levels import multiplayer_data, load_level_data, online_multiplayer_data, build_objects
from src.engine.bullet import Bullet
from src.engine.heatlh_box import PowerBox
from src.engine.power_ups import Power_up
from pymongo import MongoClient
from dotenv import load_dotenv
bullet_class = Bullet

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

start_x = 58 * 64
start_y = -1000

# Load platforms
platform_image_path = "src/assets/images/"
platform_images = {}
try:
    platform_images = {
        'left': pygame.image.load(platform_image_path + "platform_left.png").convert_alpha(),
        'middle': pygame.image.load(platform_image_path + "platform_middle.png").convert_alpha(),
        'right': pygame.image.load(platform_image_path + "platform_right.png").convert_alpha(),
        'solid': pygame.image.load(platform_image_path + "platform_solid.png").convert_alpha(),
    }
    print("Platform images loaded successfully")
except Exception as e:
    print(f"Error loading platform images: {e}")
    platform_images = {key: pygame.Surface((100, 20)) for key in ['left', 'middle', 'right', 'solid']}
    for surface in platform_images.values():
        surface.fill((100, 100, 100))

try:
    platforms = load_level_data(online_multiplayer_data, platform_images)
    print("Platforms loaded successfully")
except Exception as e:
    print(f"Error loading platforms: {e}")
    platforms = []

class MultiplayerGame:
    def __init__(self, type):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in .env file")
        self.db = MongoClient(mongo_uri)["my_game_db"]
        self.users_collection = self.db["users"]
        self.clients = []
        self.player_inputs = {}
        self.heroes = [None, None] if type == '1v1' else [None, None] * 2
        self.game_active = False
        self.platforms = platforms
        self.shot_bullets = []
        self.death_logged = {}
        self.gates = []
        self.type = type
        self.game_ended = False

        self.TEAMS_SET = False
        self.objects_dict = build_objects(online_multiplayer_data, self.heroes)
        health_boxes = [obj for obj in self.objects_dict['misc'] if isinstance(obj, PowerBox)]
        selected_health_boxes = random.sample(health_boxes, min(4, len(health_boxes)))
        power_ups = [obj for obj in self.objects_dict['power ups'] if isinstance(obj, Power_up)]
        selected_power_ups = random.sample(power_ups, min(5, len(power_ups)))
        self.objects = selected_health_boxes + self.objects_dict['gates'] + selected_power_ups
        for obj in self.objects:
            if isinstance(obj, Power_up):
                obj.targets = self.heroes

    def create_hero(self, char_name, x, y, index, username):
        print(f"Creating hero: {char_name} at ({x}, {y}) for player {index} ({username})")
        try:
            if char_name == "Roboman":
                hero = Roboman(x, y, screen_width, screen_height, index, username, True, False)
                hero.SOUND_FLAG = False
            elif char_name == "Ninja":
                hero = Ninja(x, y, screen_width, screen_height, [], index, username, True, False)
                hero.SOUND_FLAG = False
            elif char_name == "NinjaGirl":
                hero = NinjaGirl(x, y, screen_width, screen_height, [], index, username, True, False)
                hero.SOUND_FLAG = False
            elif char_name == "Archer":
                hero = Archer(x, y, [], index, username, False)
                hero.SOUND_FLAG = False
            else:
                print(f"Unknown character {char_name}, defaulting to Ninja")
                hero = Ninja(x, y, screen_width, screen_height, [], index, username, True, False)
                hero.SOUND_FLAG = False

            hero.character_name = char_name
            return hero
        except Exception as e:
            print(f"Error creating hero {char_name}: {e}")
            return Ninja(x, y, screen_width, screen_height, [], index, username)

    def client_thread(self, conn, player_index):
        print(f"Player {player_index} connected")
        buffer = ""
        try:
            while '\n' not in buffer:
                chunk = conn.recv(4096)
                if not chunk:
                    raise ConnectionError("Client disconnected before sending setup")
                buffer += chunk.decode('utf-8')

            initial_line, buffer = buffer.split('\n', 1)
            try:
                initial_data = json.loads(initial_line)
            except json.JSONDecodeError as e:
                print(f"[SERVER] Failed to decode initial JSON from client {player_index}: {e}")
                conn.close()
                return

            print(f"[SERVER] Received initial data for player {player_index}: {initial_data}")
            username = initial_data.get("username", f"Player{player_index+1}")
            char_choice = initial_data.get("character", "Ninja")

            if char_choice not in ["Roboman", "Ninja", "NinjaGirl", "Archer"]:
                print(f"[SERVER] Invalid character choice '{char_choice}', defaulting to 'Ninja'")
                char_choice = "Ninja"

            if self.type == "1v1":
                if player_index == 1:
                    player_start = online_multiplayer_data['1v1player1_start']
                else:
                    player_start = online_multiplayer_data['1v1player2_start']
            else:
                if player_index == 1:
                    player_start = online_multiplayer_data['2v2player1_start']
                elif player_index == 2:
                    player_start = online_multiplayer_data['2v2player2_start']
                elif player_index == 3:
                    player_start = online_multiplayer_data['2v2player3_start']
                else:
                    player_start = online_multiplayer_data['2v2player4_start']

            hero = self.create_hero(char_choice, player_start['x'], player_start['y'], player_index + 1, username)
            self.heroes[player_index] = hero
            self.player_inputs[player_index] = {}

            conn.sendall((json.dumps({"status": "setup_complete"}) + '\n').encode('utf-8'))
            print(f"Player {player_index} setup complete: {username} as {char_choice}")

        except Exception as e:
            print(f"[SERVER] Error with client {player_index} during setup: {e}")
            conn.close()
            return

        # --- Main loop ---
        clock = pygame.time.Clock()
        while True:
            try:
                chunk = conn.recv(4096)
                if not chunk:
                    break

                buffer += chunk.decode('utf-8')

                while '\n' in buffer:
                    message_raw, buffer = buffer.split('\n', 1)
                    if not message_raw:
                        continue
                    try:
                        self.player_inputs[player_index] = json.loads(message_raw)
                    except json.JSONDecodeError as e:
                        print(f"[SERVER] JSON decode error from client {player_index}: {e} -- raw: {message_raw}")
                        continue

                clock.tick(30)
            except Exception as e:
                print(f"[SERVER] Client {player_index} error: {e}")
                break

        print(f"Player {player_index} disconnected.")
        self.clients[player_index] = None
        self.heroes[player_index] = None
        self.player_inputs[player_index] = {}
        conn.close()



    def game_loop(self):
        print("Game loop started")
        
        clock = pygame.time.Clock()
        while self.game_active:
            print("------in the loop-----")
            if not all(self.heroes):
                clock.tick(30)
                continue
            try:
                for obj in self.objects:
                    obj.Update_online()
                objs_state = []
                for obj in self.objects:
                    if hasattr(obj, 'serialize'):
                        try:
                            objs_state.append(obj.serialize())
                        except Exception as e:
                            print(f"Serialization error for object {obj}: {e}")
                if self.type == '1v1':
                    hero1, hero2 = self.heroes[0], self.heroes[1]
                    inputs1 = self.player_inputs.get(0, {})
                    inputs2 = self.player_inputs.get(1, {})

                    keys1 = {
                        pygame.K_a: inputs1.get("A", False),
                        pygame.K_d: inputs1.get("D", False),
                        pygame.K_w: inputs1.get("W", False),
                        pygame.K_LSHIFT: inputs1.get("LSHIFT", False),
                        pygame.K_g: inputs1.get("G", False),
                        pygame.K_TAB: inputs1.get("TAB", False),
                        pygame.K_RCTRL: inputs1.get("RCTRL", False),
                        pygame.K_RALT: inputs1.get("RALT", False),
                    }
                    mouse1 = (inputs1.get("left_click", False), False, inputs1.get("right_click", False))

                    keys2 = {
                        pygame.K_a: inputs2.get("A", False),
                        pygame.K_d: inputs2.get("D", False),
                        pygame.K_w: inputs2.get("W", False),
                        pygame.K_LSHIFT: inputs2.get("LSHIFT", False),
                        pygame.K_g: inputs2.get("G", False),
                        pygame.K_TAB: inputs2.get("TAB", False),
                        pygame.K_RCTRL: inputs2.get("RCTRL", False),
                        pygame.K_RALT: inputs2.get("RALT", False),
                    }
                    mouse2 = (inputs2.get("left_click", False), False, inputs2.get("right_click", False))

                    hero1.attack_targets = [hero2]
                    hero2.attack_targets = [hero1]

                    hero1.handle_input_online(keys1, self.gates, self.shot_bullets, bullet_class, None, mouse1)
                    hero2.handle_input_online(keys2, self.gates, self.shot_bullets, bullet_class, None, mouse2)

                    hero1.update_online(self.platforms, self.shot_bullets, hero1.attack_targets, keys1, self.gates, None)
                    hero2.update_online(self.platforms, self.shot_bullets, hero2.attack_targets, keys2, self.gates, None)

                    # بررسی مرگ و آپدیت kills و deaths
                  
                    state_p1 = hero1.serialize()
                    state_p2 = hero2.serialize()
                    bullets_state = [b.serialize() for b in self.shot_bullets]

                    self.clients[0].sendall(json.dumps({
                        "self": state_p1,
                        "opponents": [state_p2],
                        "bullets": bullets_state,
                        "objects": objs_state,
                    }).encode('utf-8') + b"\n")
                    
                    
                    print(f"Client one:\nself{state_p1}\nopponents:{state_p2}\nbullets:{bullets_state}\nobjects:{objs_state}\n")
                    

                    self.clients[1].sendall(json.dumps({
                        "self": state_p2,
                        "opponents": [state_p1],
                        "bullets": bullets_state,
                        "objects": objs_state,
                    }).encode('utf-8') + b"\n")
                    print(f"Client two:\nself{state_p2}\nopponents:{state_p1}\nbullets:{bullets_state}\nobjects:{objs_state}\n")

                elif self.type == '2v2':
                    hero1, hero2, hero3, hero4 = self.heroes
                    inputs = [self.player_inputs.get(i, {}) for i in range(4)]
                    keys = []
                    for i in range(4):
                        keys.append({
                            pygame.K_a: inputs[i].get("A", False),
                            pygame.K_d: inputs[i].get("D", False),
                            pygame.K_w: inputs[i].get("W", False),
                            pygame.K_LSHIFT: inputs[i].get("LSHIFT", False),
                            pygame.K_g: inputs[i].get("G", False),
                            pygame.K_TAB: inputs[i].get("TAB", False),
                            pygame.K_RCTRL: inputs[i].get("RCTRL", False),
                            pygame.K_RALT: inputs[i].get("RALT", False),
                        })
                    
                    mice = []
                    for i in range(4):
                        mice.append((inputs[i].get("left_click", False), False, inputs[i].get("right_click", False)))
                    
                    heroes = [hero1, hero2, hero3, hero4]
                    for i in range(4):
                        if heroes[i].hero_creation_index in (1, 2):
                            heroes[i].attack_targets = [h for h in heroes if h and h.hero_creation_index in (3, 4)]
                        else:
                            heroes[i].attack_targets = [h for h in heroes if h and h.hero_creation_index in (1, 2)]

                        heroes[i].handle_input_online(keys[i], self.gates, self.shot_bullets, bullet_class, None, mice[i])
                        heroes[i].update_online(self.platforms, self.shot_bullets, heroes[i].attack_targets, keys[i], self.gates, None)

                    # بررسی مرگ و آپدیت kills و deaths
       
                    states = [h.serialize() for h in heroes]
                    bullets_state = [b.serialize() for b in self.shot_bullets]

                    team_data = [
                        (0, 1, [states[2], states[3]]),
                        (1, 0, [states[2], states[3]]),
                        (2, 3, [states[0], states[1]]),
                        (3, 2, [states[0], states[1]]),
                    ]

                    for idx, mate_idx, opponents in team_data:
                        self.clients[idx].sendall(json.dumps({
                            "self": states[idx],
                            "teammate": states[mate_idx],
                            "opponents": opponents,
                            "bullets": bullets_state,
                            "objects": objs_state,
                        }).encode('utf-8') + b"\n")
                active_heroes = [h for h in self.heroes if h is not None]
                for h in active_heroes: h.events.clear()
                if not self.game_ended and self.check_win_condition():
                    self.game_active = False
                    self.game_ended = True
                    break
                clock.tick(30)

            except Exception as e:
                print(f"Game loop error: {e}")
                self.game_active = False
    def _register_death_and_kill(self, dead_username):
        killer = None
        for bullet in reversed(self.shot_bullets):  
            if bullet.owner != dead_username:
                killer = bullet.owner
                break

        self.users_collection.update_one({"username": dead_username}, {"$inc": {"deaths": 1}})
        if killer:
            self.users_collection.update_one({"username": killer}, {"$inc": {"kills": 1}})

    def _log_death_once(self, hero):
        if hero is None or hero.username in self.death_logged:
            return
        if hero.health <= 0:
            killer = self._find_killer(hero.username)
            self.users_collection.update_one({"username": hero.username}, {"$inc": {"deaths": 1}})
            if killer:
                self.users_collection.update_one({"username": killer}, {"$inc": {"kills": 1}})
            self.death_logged[hero.username] = True

    def _find_killer(self, dead_username):
        for bullet in reversed(self.shot_bullets):
            if bullet.owner != dead_username:
                return bullet.owner
        return None

    def check_win_condition(self):
        if self.type == '1v1':
            hero1, hero2 = self.heroes[0], self.heroes[1]

            self._log_death_once(hero1)
            self._log_death_once(hero2)

            if hero1.health <= 0 or hero2.health <= 0:
                if hero1.health > 0:
                    self._update_win_loss(hero1.username, hero2.username)
                elif hero2.health > 0:
                    self._update_win_loss(hero2.username, hero1.username)
                return True

        elif self.type == '2v2':
            heroes = self.heroes

            for hero in heroes:
                self._log_death_once(hero)

            team1_alive = any(h.health > 0 for h in heroes[0:2])
            team2_alive = any(h.health > 0 for h in heroes[2:4])

            if not team1_alive or not team2_alive:
                if team1_alive:
                    self._update_team_win_loss(heroes[0:2], heroes[2:4])
                elif team2_alive:
                    self._update_team_win_loss(heroes[2:4], heroes[0:2])
                return True

        return False
    def _update_win_loss(self, winner_username, loser_username):
        self._send_game_result([winner_username], [loser_username])
        self.users_collection.update_one({"username": winner_username}, {"$inc": {"wins": 1}})
        self.users_collection.update_one({"username": loser_username}, {"$inc": {"losses": 1}})
        print(f"[GAME] {winner_username} WIN, {loser_username} LOSE")

    def _update_team_win_loss(self, winning_team, losing_team):
        self._send_game_result([h.username for h in winning_team],[h.username for h in losing_team])
        for hero in winning_team:
            self.users_collection.update_one({"username": hero.username}, {"$inc": {"wins": 1}})
        for hero in losing_team:
            self.users_collection.update_one({"username": hero.username}, {"$inc": {"losses": 1}})
        print(f"[GAME] Team {[h.username for h in winning_team]} WIN, "
              f"Team {[h.username for h in losing_team]} LOSE")

    
    def set_players(self, clients):
        self.clients = clients
        self.player_inputs = {i: {} for i in range(len(clients))}
        self.game_active = True
        for idx, conn in enumerate(clients):
            threading.Thread(target=self.client_thread, args=(conn, idx), daemon=True).start()
        threading.Thread(target=self.game_loop, daemon=True).start()

    def _send_game_result(self, winners, losers):
        for idx, hero in enumerate(self.heroes):
            if hero is None:
                continue
            result = "win" if hero.username in winners else "lose"
            try:
                self.clients[idx].sendall((json.dumps({"game_result": result}) + "\n").encode("utf-8"))
            except Exception as e:
                print(f"[SERVER] Failed to send game result to {hero.username}: {e}")    