import pygame
import socket
import threading
import random
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from multiplayergame_online import MultiplayerGame

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

        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in .env file")
        
        self.client = MongoClient(mongo_uri)
        self.db = self.client["my_game_db"]
        self.users_collection = self.db["users"]
        self.users_collection.create_index("username", unique=True)
        
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.connected_clients = []
        self.lock = threading.Lock()

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def generate_unique_id(self, existing_ids):
        while True:
            new_id = str(random.randint(1000, 9999))
            if new_id not in existing_ids:
                return new_id

    def is_socket_open(self, sock):
        """Check if a socket is still open and valid."""
        try:
            sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            return True
        except socket.error:
            return False

    def cleanup_client(self, client_info):
        """Remove a client from connected_clients and game_sessions if disconnected."""
        with self.lock:
            if client_info in self.connected_clients:
                self.connected_clients.remove(client_info)
                print(f"[SERVER] Removed client {client_info['username']} (ID: {client_info['id']}) from connected clients")

            creator_id = client_info['id']
            if creator_id in game_sessions:
                del game_sessions[creator_id]
                print(f"[SERVER] Removed game session {creator_id} due to creator disconnection")

            try:
                if self.is_socket_open(client_info['socket']):
                    client_info['socket'].close()
            except:
                pass

    def accept_clients(self):
        while True:
            try:
                client_socket, addr = self.socket.accept()
                print(f"[SERVER] Client connected from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except Exception as e:
                print(f"[SERVER] Error accepting client: {e}")
    def find_user_by_credentials(self, username, password):
        return self.users_collection.find_one({"username": username, "password": password})

    def username_exists(self, username):
        return self.users_collection.find_one({"username": username}) is not None


    def create_user(self, username, password):
        last_user = self.users_collection.find_one(sort=[("id", -1)])
        new_id = str(int(last_user["id"]) + 1) if last_user else "1"

        new_user = {
            "username": username,
            "password": password,
            "id": new_id,
            "kill": 0,
            "death": 0,
            "win": 0,
            "lose": 0

        }
        self.users_collection.insert_one(new_user)
        return new_user

    def handle_client(self, client_socket, addr):
        client_info = None
        option = None
        try:
            client_socket.settimeout(30.0)
            client_socket.sendall(b"Login(1) or Signup(2):")
            action = client_socket.recv(1024).decode().strip()
            if not action:
                client_socket.close()
                return

            if action == "1":
                client_socket.sendall(b"Username:")
                username = client_socket.recv(1024).decode().strip()
                client_socket.sendall(b"Password:")
                password = client_socket.recv(1024).decode().strip()

                user = self.find_user_by_credentials(username, password)
                if not user:
                    client_socket.sendall(b"ERR:Invalid username/password")
                    client_socket.close()
                    print(f"[SERVER] Failed login attempt from {addr} username={username}")
                    return
                db_id = user['id']
                client_socket.sendall(f"OK:{db_id}".encode())

            elif action == "2":
                while True:
                    client_socket.sendall(b"Choose username:")
                    username = client_socket.recv(1024).decode().strip()
                    if not username:
                        client_socket.sendall(b"ERR:Username cannot be empty")
                        continue
                    if self.username_exists(username):
                        client_socket.sendall(b"ERR:Username taken")
                        continue
                    client_socket.sendall(b"Choose password:")
                    password = client_socket.recv(1024).decode().strip()
                    if len(password) < 4:
                        client_socket.sendall(b"ERR:Password too short")
                        continue
                    new_user = self.create_user(username, password)
                    db_id = new_user['id']
                    client_socket.sendall(f"OK:{db_id}".encode())
                    break
            else:
                client_socket.sendall(b"ERR:Invalid action")
                client_socket.close()
                return

            username = username 
            client_id = db_id

            client_info = {
                "socket": client_socket,
                "address": addr,
                "username": username,
                "id": client_id
            }
            with self.lock:
                self.connected_clients.append(client_info)
            print(f"[SERVER] Authenticated client {username} (ID: {client_id}) from {addr}")

            client_socket.settimeout(None)
            option = client_socket.recv(1024).decode().strip()
            if option == "1":
                self.handle_create_game(client_info)
                self.handle_creator_session(client_info)
            elif option == "2":
                self.handle_join_game(client_info)
            else:
                client_socket.sendall(b"Invalid option selected.")
        except socket.timeout:
            print(f"[SERVER] Timeout for client {addr}")
        except Exception as e:
            print(f"[SERVER] Error handling client {addr}: {e}")
        finally:
            if client_info and (not self.is_socket_open(client_socket) or option not in ["1", "2"]):
                self.cleanup_client(client_info)

    def handle_create_game(self, client_info):
        sock = client_info['socket']
        sock.sendall(b"Choose game type:\n1. 1v1\n2. 2v2")
        game_type = sock.recv(1024).decode().strip()
        creator_id = client_info['id']
        with self.lock:
            game_sessions[creator_id] = {
                'creator_socket': sock,
                'creator_id': creator_id,
                'creator_username': client_info['username'],
                'players': [client_info],
                'type': game_type
            }
        print(f"[SERVER] Game created by {client_info['username']} (ID: {creator_id}), type: {game_type}")
    # def handle_creator_session(self, client_info):
    #     creator_id = client_info['id']
    #     sock = client_info['socket']
        
    #     try:
    #         while True:
    #             with self.lock:
    #                 session = game_sessions.get(creator_id)
    #                 if not session: break
    #                 if session['pending_requests']:
    #                     joiner_info = session['pending_requests'].pop(0) 
    #                     joiner_socket = joiner_info['socket']
                        
    #                     msg = f"Player {joiner_info['username']} (ID: {joiner_info['id']}) wants to join. Accept? (yes/no):"
                        
    #                     try:
    #                         sock.settimeout(30.0)
    #                         sock.sendall(msg.encode())
    #                         answer = sock.recv(1024).decode().strip().lower()
    #                         sock.settimeout(None)
                            
    #                         if answer == "yes":
    #                             session['players'].append(joiner_info)
    #                             joiner_socket.sendall(b"You have been accepted to game")
    #                         else:
    #                             joiner_socket.sendall(b"You have been denied from game")
    #                     except socket.timeout:
    #                         joiner_socket.sendall(b"Host did not respond in time.")
    #                     finally:
    #                         joiner_info['event'].set()

    #             pygame.time.wait(100) 

    #     except Exception as e:
    #         print(f"[SERVER] Error in creator session for {client_info['username']}: {e}")
    #     finally:
    #         self.cleanup_client(client_info)
    def handle_creator_session(self, client_info):
        sock = client_info['socket']
        creator_id = client_info['id']
        try:
            sock.sendall(b"Game created. Waiting for players to join...\n")
            while True:
                with self.lock:
                    session = game_sessions.get(creator_id)
                    if session:
                        player_count = len(session['players'])
                        game_type = session['type']
                        required_players = 2 if game_type == "1" else 4
                        if player_count == required_players:
                            print(f"[SERVER] Game {creator_id} is ready to start with {player_count} players.")
                            game_type_str = "1v1" if game_type == "1" else "2v2"
                            for p in session['players']:
                                try:
                                    p['socket'].sendall(b"Game is starting\n")
                                except:
                                    pass
                            pygame.time.wait(3000)
                            for p in session['players']:
                                try:
                                    p['socket'].sendall(b"setup_complete\n")
                                except:
                                    pass
                            game = MultiplayerGame(game_type_str)
                            game.set_players([p['socket'] for p in session['players']])
                            game.game_active = True
                            threading.Thread(target=game.game_loop, daemon=True).start()
                            break
                    if not self.is_socket_open(sock):
                        print(f"[SERVER] Creator {client_info['username']} (ID: {creator_id}) socket closed")
                        break
                    pygame.time.wait(100)
        except Exception as e:
            print(f"[SERVER] Error in creator session for {client_info['username']}: {e}")


    def handle_join_game(self, client_info):
        sock = client_info['socket']
        sock.sendall(b"Choose the way to join the game:\n1. Search username or id(creator of game id/username)\n2. Leave it on server\n(1 or 2):")
        choice = sock.recv(1024).decode().strip()

        creator_id = None
        if choice == "1":
            sock.sendall(b"Enter username or id of game creator:")
            creator_address = sock.recv(1024).decode().strip()
            with self.lock:
                for cid, session in game_sessions.items():
                    if creator_address == session['creator_id'] or creator_address == session['creator_username']:
                        creator_id = cid
                        break
            if not creator_id:
                sock.sendall(b"Invalid id/username")
                print(f"[SERVER] Invalid creator id/username {creator_address} for {client_info['username']}")
                return
        else:
            with self.lock:
                creator_id = random.choice(list(game_sessions.keys())) if game_sessions else None
            if not creator_id:
                sock.sendall(b"No games available.")
                print(f"[SERVER] No games available for {client_info['username']}")
                return

        with self.lock:
            if creator_id not in game_sessions:
                sock.sendall(b"No such game found.")
                print(f"[SERVER] Game {creator_id} not found for {client_info['username']}")
                return
            creator_socket = game_sessions[creator_id]['creator_socket']

        if not self.is_socket_open(creator_socket):
            sock.sendall(b"Game creator is no longer connected.")
            print(f"[SERVER] Creator {creator_id} socket closed for joiner {client_info['username']}")
            with self.lock:
                if creator_id in game_sessions:
                    del game_sessions[creator_id]
                    print(f"[SERVER] Removed game session {creator_id} due to invalid creator socket")
            return

        msg = f"Player {client_info['username']} (ID: {client_info['id']}) wants to join the game. Accept? (yes/no):"
        try:
            creator_socket.settimeout(30.0)
            creator_socket.sendall(msg.encode())
            answer = creator_socket.recv(1024).decode().strip().lower()
            creator_socket.settimeout(None)
            if answer == "yes":
                with self.lock:
                    game_sessions[creator_id]['players'].append(client_info)
                sock.sendall(b"You have been accepted to game")
                print(f"[SERVER] {client_info['username']} accepted into game {creator_id}")
            else:
                sock.sendall(b"You have been denied from game")
                print(f"[SERVER] {client_info['username']}'s join request denied by creator {creator_id}")
        except socket.timeout:
            sock.sendall(b"Game creator did not respond in time.")
            print(f"[SERVER] Timeout waiting for response from creator {creator_id}")
        except Exception as e:
            sock.sendall(b"Error communicating with game creator.")
            print(f"[SERVER] Error handling join request for {client_info['username']}: {e}")
            if not self.is_socket_open(creator_socket):
                with self.lock:
                    if creator_id in game_sessions:
                        del game_sessions[creator_id]
                        print(f"[SERVER] Removed game session {creator_id} due to invalid creator socket")

    def broadcast_presence(self):
        while True:
            try:
                self.broadcast_socket.sendto(BROADCAST_MSG, ('<broadcast>', BROADCAST_PORT))
                pygame.time.wait(1000)
            except Exception as e:
                print(f"[SERVER] Error broadcasting presence: {e}")


if __name__ == '__main__':
    pygame.init()
    server = Server()
    try:
        while True:
            pygame.time.wait(1000)
    except KeyboardInterrupt:
        print("[SERVER] Server terminated by user.")
        for client in server.connected_clients:
            try:
                client['socket'].close()
            except:
                pass
        server.socket.close()
        server.broadcast_socket.close()
