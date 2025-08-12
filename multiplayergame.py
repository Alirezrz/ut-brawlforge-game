import socket
import threading
import json
import pygame
import random
import os
import time
from src.engine.Roboman import Roboman
from src.engine.Ninja import Ninja
from src.engine.NinjaGirl import NinjaGirl
from src.engine.Archer import Archer
from config import screen_width, screen_height
from src.levels import online_multiplayer_data , load_level_data,build_objects
from src.engine.bullet import Bullet
from src.engine.heatlh_box import PowerBox
from src.engine.power_ups import Power_up
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800,600))
platform_image_path = "src/assets/images/"
platform_images = {key: pygame.Surface((64, 64)) for key in ['left', 'middle', 'right', 'solid']}
platforms = load_level_data(online_multiplayer_data , platform_images)

def send_json(conn, data):
    """Safely sends a JSON object with a newline terminator."""
    try:
        message = json.dumps(data) + '\n'
        conn.sendall(message.encode('utf-8'))
    except (socket.error, BrokenPipeError):
        pass 

class MultiplayerGame:
    def __init__(self, game_type):
        self.clients = []
        self.player_inputs = {}
        self.heroes = [None] * (2 if game_type == '1v1' else 4)
        self.game_active = False
        self.platforms = platforms
        self.shot_bullets = []
        self.gates = []
        self.type = game_type
        self.game_over_timer_start = None
        self.game_over_delay = 3000 
        self.objects_dict= build_objects(online_multiplayer_data , self.heroes)
        health_boxes = [obj for obj in self.objects_dict['misc'] if isinstance(obj, PowerBox)]
        selected_health_boxes = random.sample(health_boxes, min(4, len(health_boxes)))
        power_ups = [obj for obj in self.objects_dict['power ups'] if isinstance(obj, Power_up)]
        selected_power_ups = random.sample(power_ups, min(5, len(power_ups)))
        other_misc = [obj for obj in self.objects_dict['misc'] 
                    if not isinstance(obj, PowerBox) and not isinstance(obj, Power_up)]        
        self.objects = selected_health_boxes + self.objects_dict['gates'] + selected_power_ups + other_misc

        for obj in self.objects:
            if type(obj)==Power_up:
                obj.targets=self.heroes
            
    def create_hero(self, char_name, x, y, index, username):
        print(f"Creating hero on server: {char_name} for player index {index} ({username})")
        if char_name == "Roboman":
            return Roboman(x, y, screen_width, screen_height, index, username, LOAD_FLAG=True)
            
        elif char_name == "Ninja":
            return Ninja(x, y, screen_width, screen_height, [], index, username, LOAD_FLAG=True)
        elif char_name == "NinjaGirl":
            return NinjaGirl(x, y, screen_width, screen_height, [], index, username)
        elif char_name == "Archer":
            return Archer(x, y, [], index, username)
        
        return Ninja(x, y, screen_width, screen_height, [], index, username, LOAD_FLAG=True)

    def client_thread(self, conn, player_session_index):
        print(f"Game thread started for player index {player_session_index}.")
        conn.settimeout(None)
        buffer = ""
        try:
    
            data = conn.recv(1024).decode('utf-8')
            buffer += data
            message_raw, buffer = buffer.split('\n', 1)
            initial_data = json.loads(message_raw)
            
            username = initial_data.get("username", f"Player{player_session_index}")
            char_choice = initial_data.get("character", "Ninja")
            if self.type == "1v1":
                if player_session_index==1:
                    player_start=online_multiplayer_data['1v1player1_start']
                else :
                    player_start=online_multiplayer_data['1v1player2_start']    
            else:
                if player_session_index==1:
                    player_start=online_multiplayer_data['2v2player1_start']  
                elif player_session_index==2:
                    player_start=online_multiplayer_data['2v2player2_start']               
                elif player_session_index==3:
                    player_start=online_multiplayer_data['2v2player3_start']
                else:
                    player_start=online_multiplayer_data['2v2player4_start']

            hero = self.create_hero(char_choice, player_start['x'],  player_start['y'], player_session_index, username)
            self.heroes[player_session_index - 1] = hero
            self.player_inputs[player_session_index] = {}
            print(f"Player {player_session_index} setup complete: {username} as {char_choice}")

        except Exception as e:
            print(f"CRITICAL ERROR during setup for client {player_session_index}: {e}")
            self.cleanup_client(conn, player_session_index)
            return

        while self.game_active:
            try:
                data = conn.recv(4096).decode('utf-8')
                if not data: break
                buffer += data
                while '\n' in buffer:
                    message_raw, buffer = buffer.split('\n', 1)
                    if not message_raw: continue
                    self.player_inputs[player_session_index] = json.loads(message_raw)
            except (socket.error, json.JSONDecodeError, IndexError):
                break
        
        self.cleanup_client(conn, player_session_index)

    def cleanup_client(self, conn, player_index):
        print(f"Player {player_index} disconnected from game.")
        if player_index - 1 < len(self.clients) and self.clients[player_index - 1] is not None:
            self.clients[player_index - 1] = None
            self.heroes[player_index - 1] = None
        try:
            conn.close()
        except:
            pass

    def game_loop(self):
        print("Game loop preparing...")
        clock = pygame.time.Clock()
    
        while any(h is None for h in self.heroes):
            print("Waiting for all players to send character info...")
            time.sleep(0.5)
            if not any(self.clients):
                self.game_active = False
                break
        
        if not self.game_active:
            print("Game cancelled before start because all clients disconnected.")
            return
        max_players = 2 if self.type == '1v1' else 4
        while True:
            ready_players = sum(1 for h in self.heroes if h is not None)
            if ready_players == max_players:
                print("All players ready. Starting main game simulation.")
                break
            print(f"Waiting for players... ({ready_players}/{max_players})")
            time.sleep(0.5)
        winner_found =False
        print("All players ready. Starting main game simulation.")
        while self.game_active:
            try:
                current_time = pygame.time.get_ticks()
                if self.game_over_timer_start:
                    if current_time - self.game_over_timer_start > self.game_over_delay:
                        game_over_message = {"type": "game_over", "winner": self.winner}
                        for client_conn in self.clients:
                            if client_conn:
                                send_json(client_conn, game_over_message)
                        self.game_active = False
                        break
                for obj in self.objects:
                    obj.Update_online()
                    
                    
                active_heroes = [h for h in self.heroes if h is not None]
                for hero in active_heroes:
                    player_id = hero.hero_creation_index
                    inputs = self.player_inputs.get(player_id, {})
                    if hero.health <= 0 and hero.ALIVE:
                        hero.die()
                    keys = {
                        pygame.K_d: inputs.get("D", False), pygame.K_a: inputs.get("A", False), 
                        pygame.K_w: inputs.get("W", False), pygame.K_LSHIFT: inputs.get("LSHIFT", False),
                        pygame.K_g: inputs.get("G", False), pygame.K_TAB: inputs.get("TAB", False),
                    }
                    mouse = (inputs.get("left_click", False), False, inputs.get("right_click", False))
                    # --- TEAM-BASED TARGETING ---
                    if self.type == '2v2':
                        if hero.hero_creation_index in (1, 2):  # Team 1
                            targets = [h for h in active_heroes if h.hero_creation_index in (3, 4)]
                        else:  # Team 2
                            targets = [h for h in active_heroes if h.hero_creation_index in (1, 2)]
                    else:
                        targets = [h for h in active_heroes if h is not hero]
                    hero.attack_targets = targets
                    hero.handle_input_online(keys, self.gates, self.shot_bullets, Bullet, None, mouse)
                    hero.update_online(self.platforms, self.shot_bullets, targets, keys, self.gates, None)
                    
                    
                if not winner_found:
                    winner = self.check_win_condition()
                    if winner:
                        winner_found = True
                        self.winner = winner
                        self.game_over_timer_start = current_time
                all_states = [h.serialize() if h else None for h in self.heroes]
                bullets_state = [b.serialize() for b in self.shot_bullets]
                print(f"bullets=\n{bullets_state}\n")
                objs_state = []
                for obj in self.objects:
                    if hasattr(obj, 'serialize'):
                        try:
                            objs_state.append(obj.serialize())
                        except Exception as e:
                            print(f"Serialization error for object {obj}: {e}")
                
                for i, client_conn in enumerate(self.clients):
                    if client_conn and all_states[i] is not None:
                        my_team_num = 1 if client_conn in self.teams.get(1, []) else 2
                        opponent_team_num = 2 if my_team_num == 1 else 1
                        teammate_conn = None
                        if self.type == '2v2':
                            for conn in self.teams[my_team_num]:
                                if conn != client_conn:
                                    teammate_conn = conn
                        opponents_conns = self.teams.get(opponent_team_num, [])            
                        opponents_states = [all_states[self.clients.index(c)] for c in opponents_conns if c in self.clients and all_states[self.clients.index(c)] is not None]
                        teammate_state = all_states[self.clients.index(teammate_conn)] if teammate_conn and teammate_conn in self.clients else None
                        game_state = {
                           "self": all_states[i], 
                           "opponents": opponents_states, 
                           "teammate": teammate_state, 
                           "bullets": bullets_state,
                           "objects":objs_state,
                        } 
                        send_json(client_conn, game_state)

                for h in active_heroes: h.events.clear()
                
                
                if not any(self.clients):
                    print("All clients have disconnected. Stopping game.")
                    self.game_active = False

                clock.tick(60) 

            except Exception as e:
                print(f"FATAL GAME LOOP ERROR: {e}")
                self.game_active = False

    # def set_players(self, clients_with_indices,teams):
    #     num_players = len(clients_with_indices)
    #     self.clients = [None] * num_players
    #     self.teams = teams
        
    #     for conn, player_session_index in clients_with_indices.items():
    #         self.clients[player_session_index - 1] = conn
        
    #     self.game_active = True
        
    #     for conn, player_session_index in clients_with_indices.items():
    #         thread = threading.Thread(target=self.client_thread, args=(conn, player_session_index), daemon=True)
    #         thread.start()
        
    #     threading.Thread(target=self.game_loop, daemon=True).start()

    def check_win_condition(self):
        winner_name = None

        if self.type == '1v1':
          player1 = next((h for h in self.heroes if h and h.hero_creation_index == 1), None)
          player2 = next((h for h in self.heroes if h and h.hero_creation_index == 2), None)
          if player1 and player2:
            if player1.DEAD and not player2.DEAD:
                winner_name = player2.username  
            elif player2.DEAD and not player1.DEAD:
                winner_name = player1.username 
            elif player1.DEAD and player2.DEAD:
                winner_name = "Draw"
        elif self.type == '2v2':
          team1_players = [h for h in self.heroes if h and h.hero_creation_index in (1, 2)]
          team2_players = [h for h in self.heroes if h and h.hero_creation_index in (3, 4)]
          if team1_players and team2_players:
            team1_eliminated = all(p.DEAD for p in team1_players)
            team2_eliminated = all(p.DEAD for p in team2_players)

            if team1_eliminated and not team2_eliminated:
                winner_name = "Team 2"
            elif team2_eliminated and not team1_eliminated:
                winner_name = "Team 1"
            elif team1_eliminated and team2_eliminated:
                winner_name = "Draw"
    
        return winner_name
    def set_players(self, connections, teams):
        self.clients = connections
        self.teams = teams 
        self.game_active = True

        for i, conn in enumerate(self.clients):
           thread = threading.Thread(target=self.client_thread, args=(conn, i + 1), daemon=True)
           thread.start()

        threading.Thread(target=self.game_loop, daemon=True).start()
