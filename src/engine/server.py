import os
import pygame
import socket
import threading 
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
import json
import time
import uuid




HOST="0.0.0.0"
PORT=9191


class multiplayer_game:
    def __init__(self, screen, platform_image, background, selected_char, selected_char2):
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(2)  # Expecting 2 clients for now
        print(f"Server started on {HOST}:{PORT}")
        
        
        self.clients = []  # list of (conn, addr)
        self.inputs = [None, None]
        self.states = [None, None]
        
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


        self.hero.attack_targets =  [self.hero2]
        self.hero2.attack_targets =  [self.hero]
        
    def client_thread(self, conn, client_id):
        print(f"Client {client_id} connected")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                input_data = json.loads(data.decode('utf-8'))
                self.inputs[client_id] = input_data
                print(f"Client {client_id} input: {input_data}")

                # Build the state response
                client_state = self.states[client_id]
                opponent_id = 1 - client_id
                opponent_state = self.states[opponent_id]

                state_response = {
                    "self": client_state,
                    "opponent": opponent_state
                }

                conn.sendall(json.dumps(state_response).encode('utf-8'))

            except Exception as e:
                print(f"Error with client {client_id}: {e}")
                break
        conn.close()
        print(f"Client {client_id} disconnected")
        
        
    def start(self):
        for i in range(2):
            conn, addr = self.server_socket.accept()
            self.clients.append((conn, addr))
            threading.Thread(target=self.client_thread, args=(conn, i), daemon=True).start()

        print("All clients connected. Game ready to begin.")




players = {}         
waiting_room = {
    "1v1": [],
    "2v2": []
}
active_games = {} 

def check_for_matches():
    """Checks the waiting room and creates matches if possible."""
    while True:
        if len(waiting_room["1v1"]) >= 2:
            p1_id = waiting_room["1v1"].pop(0)
            p2_id = waiting_room["1v1"].pop(0)
            game_id = str(uuid.uuid4())
            active_games[game_id] = [p1_id, p2_id]
            
            print(f"[MATCH FOUND] 1v1 match created: {p1_id} vs {p2_id}")
            match_data = json.dumps({
                "type": "match_found",
                "payload": {
                    "game_id": game_id,
                    "opponents": {p1_id: players[p1_id]['username'], p2_id: players[p2_id]['username']}
                }
            })
            if p1_id in players: players[p1_id]['conn'].sendall(match_data.encode('utf-8'))
            if p2_id in players: players[p2_id]['conn'].sendall(match_data.encode('utf-8'))
        if len(waiting_room["2v2"]) >= 4:
            print("2v2 match found!")

        time.sleep(1)

def handle_client(conn, addr, player_id):
    """Handles a single client connection."""
    print(f"[NEW CONNECTION] {addr} connected with ID: {player_id}")
    
    try:
        username_data = conn.recv(1024).decode('utf-8')
        username = json.loads(username_data).get('username', 'Guest')
        
        players[player_id] = {'username': username, 'conn': conn, 'state': {}}
        print(f"Player {player_id} set username to: {username}")

        initial_data = json.dumps({'type': 'connection_success', 'id': player_id})
        conn.sendall(initial_data.encode('utf-8'))
        
    except Exception as e:
        print(f"[ERROR] Could not set up client {addr}: {e}")
        conn.close()
        return

    connected = True
    while connected:
        try:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                break

            message = json.loads(data)
            msg_type = message.get("type")
            payload = message.get("payload")

            if msg_type == "join_waiting_room":
                game_mode = payload.get("game_mode")
                if game_mode in waiting_room and player_id not in waiting_room[game_mode]:
                    waiting_room[game_mode].append(player_id)
                    print(f"Player {players[player_id]['username']} joined {game_mode} waiting room.")
                    conn.sendall(json.dumps({"type": "waiting", "payload": {"status": "You are in the waiting room..."}}).encode('utf-8'))

            elif msg_type == "search_by_id":
                target_id = payload.get("target_id")
                if target_id in players:
                    print(f"Player {player_id} wants to play with {target_id}")
                else:
                    conn.sendall(json.dumps({"type": "error", "payload": {"message": "ID not found"}}).encode('utf-8'))
        except (ConnectionResetError, json.JSONDecodeError):
            break
        except Exception as e:
            print(f"An error occurred with {player_id}: {e}")
            break

    print(f"[DISCONNECTED] {players[player_id]['username']} ({addr}) disconnected.")
    for mode in waiting_room:
        if player_id in waiting_room[mode]:
            waiting_room[mode].remove(player_id)
    del players[player_id]
    conn.close()

def start_server():
    """Main function to start the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    threading.Thread(target=check_for_matches, daemon=True).start()

    while True:
        conn, addr = server_socket.accept()
        player_id = str(uuid.uuid4())
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

if __name__ == "__main__":
    start_server()

