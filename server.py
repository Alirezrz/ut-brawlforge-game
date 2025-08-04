import pygame
import socket
import threading
import random
import json
import time

from multiplayergame import MultiplayerGame
HOST = '0.0.0.0'
PORT = 9191
BROADCAST_PORT = 9192
BROADCAST_MSG = b"DISCOVER_SERVER"

game_sessions = {}  # creator_id -> {'creator_socket': socket, 'players': [client_info], 'type': game_type}

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print(f"[SERVER] Listening for clients on {HOST}:{PORT}")
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.connected_clients = []
        self.lock = threading.Lock()
        threading.Thread(target=self.accept_clients, daemon=True).start()
        threading.Thread(target=self.broadcast_presence, daemon=True).start()

    def generate_unique_id(self, existing_ids):
        while True:
            new_id = str(random.randint(1000, 9999))
            if new_id not in existing_ids:
                return new_id

    def cleanup_client(self, client_info):
        with self.lock:
            if client_info in self.connected_clients:
                self.connected_clients.remove(client_info)
                print(f"[SERVER] Removed client {client_info['username']} (ID: {client_info['id']})")
            
            sessions_to_remove = []
            for game_id, session in game_sessions.items():
                if client_info in session['players']:
                    session['players'].remove(client_info)
                    if client_info['id'] == game_id:
                        sessions_to_remove.append(game_id)
                        for player in session['players']:
                             try:
                                 player['socket'].sendall(json.dumps({"type": "error", "message": "Host disconnected."}).encode('utf-8'))
                             except: pass
                    else:
                        self.broadcast_lobby_update(session)

            for game_id in sessions_to_remove:
                del game_sessions[game_id]
                print(f"[SERVER] Removed game session {game_id}")
            
            try:
                client_info['socket'].close()
            except: pass

    def accept_clients(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f"[SERVER] Client connected from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        client_info = None
        try:
            initial_data_raw = client_socket.recv(1024).decode('utf-8')
            initial_data = json.loads(initial_data_raw)
            username = initial_data.get("username")
            if not username:
                client_socket.close()
                return

            with self.lock:
                client_id = self.generate_unique_id([c['id'] for c in self.connected_clients])
            client_info = {"socket": client_socket, "address": addr, "username": username, "id": client_id}
            with self.lock:
                self.connected_clients.append(client_info)
            client_socket.sendall(json.dumps({"type": "connection_success", "id": client_id}).encode('utf-8'))

            while True:
                request_raw = client_socket.recv(1024).decode('utf-8')
                if not request_raw: break
                request = json.loads(request_raw)
                
                action = request.get("action")
                if action == "create_game":
                    self.handle_create_game(client_info, request.get("game_type"))
                elif action == "join_game":
                    self.handle_join_game(client_info, request.get("game_id"))
                elif action == "host_decision":
                    self.handle_host_decision(client_info, request)

        except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
            print(f"[SERVER] Error with client {addr}: {e}")
        finally:
            if client_info: self.cleanup_client(client_info)

    def handle_create_game(self, client_info, game_type):
        creator_id = client_info['id']
        with self.lock:
            game_sessions[creator_id] = {
                'creator_info': client_info,
                'players': [client_info],
                'type': game_type,
                'pending_join_request': None
            }
        print(f"[SERVER] Game created by {client_info['username']} (ID: {creator_id}), type: {game_type}")
        response = {"type": "lobby_created", "game_id": creator_id, "players": [p['username'] for p in game_sessions[creator_id]['players']]}
        client_info['socket'].sendall(json.dumps(response).encode('utf-8'))

    def handle_join_game(self, joiner_info, game_id):
        with self.lock:
            session = game_sessions.get(game_id)
            if not session:
                joiner_info['socket'].sendall(json.dumps({"type": "error", "message": "Game ID not found."}).encode('utf-8'))
                return
            if session['pending_join_request']:
                joiner_info['socket'].sendall(json.dumps({"type": "error", "message": "Host is busy."}).encode('utf-8'))
                return
            
            required_players = 2 if session['type'] == "1v1" else 4
            if len(session['players']) >= required_players:
                joiner_info['socket'].sendall(json.dumps({"type": "error", "message": "Game is full."}).encode('utf-8'))
                return
            
            session['pending_join_request'] = joiner_info
            host_socket = session['creator_info']['socket']

        try:
            request_to_host = {"type": "join_request", "username": joiner_info['username']}
            host_socket.sendall(json.dumps(request_to_host).encode('utf-8'))
        except socket.error as e:
            print(f"Error sending join request to host: {e}")
            with self.lock:
                session['pending_join_request'] = None

    def handle_host_decision(self, host_info, response):
        game_id = host_info['id']
        with self.lock:
            session = game_sessions.get(game_id)
            if not session or not session['pending_join_request']:
                return
            joiner_info = session.pop('pending_join_request')

        if response.get("decision") == "yes":
            with self.lock:
                session['players'].append(joiner_info)
            joiner_info['socket'].sendall(json.dumps({"type": "join_accepted", "game_id": game_id, "players": [p['username'] for p in session['players']]}).encode('utf-8'))
            self.broadcast_lobby_update(session)
            self.check_game_start(session)
        else:
            joiner_info['socket'].sendall(json.dumps({"type": "join_denied"}).encode('utf-8'))

    def broadcast_lobby_update(self, session):
        with self.lock:
            player_list = [p['username'] for p in session['players']]
            update_message = json.dumps({"type": "lobby_update", "players": player_list})
        for player in session['players']:
            try:
                player['socket'].sendall(update_message.encode('utf-8'))
            except socket.error:
                print(f"Could not send lobby update to {player['username']}")

    def check_game_start(self, session):
        with self.lock:
            player_count = len(session['players'])
            required_players = 2 if session['type'] == "1v1" else 4
            if player_count == required_players:
                game_id = session['creator_info']['id']
                print(f"[SERVER] Game {game_id} is ready to start.")
                start_message = json.dumps({"type": "match_starting"}).encode('utf-8')
                for p in session['players']:
                    p['socket'].sendall(start_message)
                threading.Thread(target=self.start_game_thread, args=(session,)).start()
                
                if game_id in game_sessions:
                    del game_sessions[game_id]
    
    def start_game_thread(self, session):
        game_type = session['type']
        player_sockets = [p['socket'] for p in session['players']]
        for sock in player_sockets:
            sock.sendall(json.dumps({"type": "select_character"}).encode('utf-8'))

        game = MultiplayerGame(game_type)
        game.set_players(player_sockets)
        game.game_loop()

    def broadcast_presence(self):
        while True:
            try:
                self.broadcast_socket.sendto(BROADCAST_MSG, ('<broadcast>', BROADCAST_PORT))
                time.sleep(2)
            except: pass

if __name__ == '__main__':
    server = Server()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("[SERVER] Shutting down.")
        server.socket.close()