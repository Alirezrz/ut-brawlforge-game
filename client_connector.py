import pygame
import socket
import threading
import json
from Client import Client

BROADCAST_PORT = 9192
BROADCAST_MSG = b"DISCOVER_SERVER"
SERVER_PORT = 9191

timeout = 30  # seconds
users = [
    {
        "username": 'alireza',
        'password': '0000',  # better to keep as string
        'id': 1,
    }
]

action = input("1_Signup\n2_Login\nChoose (1/2): ")

if action == '1':  # Signup
    while True:
        name = input("Username: ")
        password = input("Password: ")

        # Check if username already exists
        exists = False
        for user in users:
            if user['username'] == name:
                exists = True
                break
        
        if exists:
            print("Username already taken! Try again.")
        else:
            new_id = users[-1]['id'] + 1 if users else 1
            users.append({
                'username': name,
                'password': password,
                'id': new_id
            })
            print(f"Signup successful! Welcome, {name}.")
            break

elif action == '2':  # Login
    name = input("Username: ")
    password = input("Password: ")

    found = False
    for user in users:
        if user['username'] == name and user['password'] == password:
            found = True
            print(f"Login successful! Welcome back, {name}.")
            break
    
    if not found:
        print("Invalid username or password.")

else:
    print("Invalid choice. Please restart.")
    
NAME=name

class ClientConnector:
    def __init__(self):
        self.server_address = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(timeout)
        self.username = NAME
        self.client_id = None
        self.is_connected = False
        self.find_server()

        if self.server_address:
            if self.connect_to_server():
                if self.exchange_user_info():
                    self.send_request_option()
        else:
            print("[CLIENT] No server found on local network.")

    def find_server(self):
        print("[CLIENT] Searching for server...")
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind(('', BROADCAST_PORT))
        udp_socket.settimeout(timeout)

        try:
            data, addr = udp_socket.recvfrom(1024)
            if data == BROADCAST_MSG:
                print(f"[CLIENT] Server discovered at {addr[0]}")
                self.server_address = addr[0]
        except socket.timeout:
            print("[CLIENT] Server discovery timed out.")
        finally:
            udp_socket.close()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_address, SERVER_PORT))
            print(f"[CLIENT] Connected to server at {self.server_address}:{SERVER_PORT}")
            self.is_connected = True
            return True
        except Exception as e:
            print(f"[CLIENT] Failed to connect to server: {e}")
            self.client_socket.close()
            self.is_connected = False
            return False

    def exchange_user_info(self):
        try:
            self.username = NAME
            if not self.username:
                print("[CLIENT] Username cannot be empty.")
                self.client_socket.close()
                self.is_connected = False
                return False
            initial_data = {"username": self.username}
            self.client_socket.sendall(json.dumps(initial_data).encode('utf-8'))
            response_raw = self.client_socket.recv(1024).decode('utf-8')
            response = json.loads(response_raw)

            if response.get("type") == "connection_success":
                self.client_id = response.get("id")
                print(f"[CLIENT] Your assigned ID: {self.client_id}")
                return True
            else:
                print(f"[CLIENT] Failed to get confirmation from server.")
                self.client_socket.close()
                self.is_connected = False
                return False

        except (socket.timeout, json.JSONDecodeError, ConnectionResetError) as e:
            print(f"[CLIENT] Failed to exchange user info: {e}")
            self.client_socket.close()
            self.is_connected = False
            return False

    def send_request_option(self):
        try:
            print("Choose an option:")
            print("1. Create a game")
            print("2. Join a game")
            option = input("Enter 1 or 2: ")

            if option == "1":
                game_type_choice = input("Choose game type:\n1. 1v1\n2. 2v2\n")
                game_type = "1v1" if game_type_choice == "1" else "2v2"
                request = {"action": "create_game", "game_type": game_type}
                self.client_socket.sendall(json.dumps(request).encode('utf-8'))
                print(f"[CLIENT] Sent request to create a {game_type} game.")
            
            elif option == "2":
                game_id = input("Enter the Game ID of the host to join: ")
                request = {"action": "join_game", "game_id": game_id}
                self.client_socket.sendall(json.dumps(request).encode('utf-8'))
                print(f"[CLIENT] Sent request to join game {game_id}.")

            else:
                print("[CLIENT] Invalid option.")
                self.client_socket.close()
                self.is_connected = False

        except (socket.error, json.JSONDecodeError) as e:
            print(f"[CLIENT] Error during option selection: {e}")
            self.client_socket.close()
            self.is_connected = False


if __name__ == '__main__':
    connector = ClientConnector()

    if connector.is_connected:
        try:
            print("[CLIENT] Waiting for server messages...")
            connector.client_socket.settimeout(None) 

            while True:
                response_raw = connector.client_socket.recv(4096).decode('utf-8')
                if not response_raw:
                    print("[CLIENT] Disconnected from server.")
                    break
                
                response = json.loads(response_raw)
                msg_type = response.get("type")
                print(f"[SERVER RESPONSE] {response}")

                if msg_type == "join_request":
                    answer = input(f"Player '{response['username']}' wants to join. Accept? (yes/no): ")
                    decision = {"decision": answer.lower()}
                    connector.client_socket.sendall(json.dumps(decision).encode('utf-8'))

                elif msg_type == "match_starting":
                    print("[CLIENT] Match is starting! Initializing game client...")
                    
                    type_num = int(input("Enter your hero type:\n1 _ Roboman\n2_Ninja\n3_ NinjaGirl\n4_Archer\n"))
                    type_map = {1:"Roboman", 2:"Ninja", 3:"NinjaGirl", 4:"Archer"}
                    hero_type = type_map[type_num]
                    
                    game_client = Client(
                        connector.client_socket,
                        connector.username,
                        connector.client_id,
                        hero_type=hero_type
                    )
                    game_client.start()
                    exit()

        except (OSError, socket.error, json.JSONDecodeError) as e:
            print(f"[CLIENT] Connection error: {e}")
        except KeyboardInterrupt:
            print("[CLIENT] Client terminated by user.")
        finally:
            if connector.client_socket:
                connector.client_socket.close()