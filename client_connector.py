import pygame
import socket
import threading
from Client import Client

BROADCAST_PORT = 9192
BROADCAST_MSG = b"DISCOVER_SERVER"
SERVER_PORT = 9191

timeout = 5  # seconds

class ClientConnector:
    def __init__(self):
        self.server_address = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(timeout)
        self.username = None
        self.client_id = None

        self.find_server()

        if self.server_address:
            self.connect_to_server()
            self.exchange_user_info()
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
            while True:
                data, addr = udp_socket.recvfrom(1024)
                if data == BROADCAST_MSG:
                    print(f"[CLIENT] Server discovered at {addr[0]}")
                    self.server_address = addr[0]
                    break
        except socket.timeout:
            print("[CLIENT] Server discovery timed out.")
        finally:
            udp_socket.close()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_address, SERVER_PORT))
            print(f"[CLIENT] Connected to server at {self.server_address}:{SERVER_PORT}")
        except Exception as e:
            print(f"[CLIENT] Failed to connect to server: {e}")
            self.client_socket.close()

    def exchange_user_info(self):
        try:
            prompt = self.client_socket.recv(1024).decode()
            print(f"[SERVER] {prompt}")
            self.username = input("Enter your username: ")
            if not self.username:
                print("[CLIENT] Username cannot be empty.")
                self.client_socket.close()
                return
            self.client_socket.sendall(self.username.encode())

            self.client_id = self.client_socket.recv(1024).decode()
            print(f"[CLIENT] Your assigned ID: {self.client_id}")
        except Exception as e:
            print(f"[CLIENT] Failed to exchange user info: {e}")
            self.client_socket.close()

    def send_request_option(self):
        try:
            print("Choose an option:")
            print("1. Create a game")
            print("2. Join a game")
            option = input("Enter 1 or 2: ")
            if option not in ["1", "2"]:
                print("[CLIENT] Invalid option.")
                self.client_socket.close()
                return

            self.client_socket.sendall(option.encode())
            print(f"[CLIENT] Sent option {option} to server.")

            server_prompt = self.client_socket.recv(1024).decode()
            print(f"[SERVER] {server_prompt}")
            sub_option = input("Enter your choice: ")
            self.client_socket.sendall(sub_option.encode())

            if option == "2":
                if sub_option == "1":
                    id_prompt = self.client_socket.recv(1024).decode()
                    print(f"[SERVER] {id_prompt}")
                    game_id = input("Enter Game ID or username: ")
                    self.client_socket.sendall(game_id.encode())

                print("[CLIENT] Waiting for approval from the game creator...")
                try:
                    self.client_socket.settimeout(30.0)
                    result = self.client_socket.recv(1024).decode()
                    print(f"[SERVER] {result}")
                except socket.timeout:
                    print("[CLIENT] Timed out waiting for approval from game creator.")
                except Exception as e:
                    print(f"[CLIENT] Error while waiting for approval: {e}")
                finally:
                    self.client_socket.settimeout(timeout)
            else:
                try:
                    result = self.client_socket.recv(1024).decode()
                    print(f"[SERVER] {result}")
                    while True:
                        try:
                            self.client_socket.settimeout(30.0)
                            message = self.client_socket.recv(1024).decode()
                            print(f"[SERVER] {message}")
                            if "Accept? (yes/no)" in message:
                                response = input("Enter yes/no: ")
                                self.client_socket.sendall(response.encode())
                        except socket.timeout:
                            continue  
                        except Exception as e:
                            print(f"[CLIENT] Error in creator session: {e}")
                            break
                except Exception as e:
                    print(f"[CLIENT] Error after game creation: {e}")
        except Exception as e:
            print(f"[CLIENT] Error during option selection: {e}")
            self.client_socket.close()

if __name__ == '__main__':
    connector = ClientConnector()

    try:
        print("[CLIENT] Waiting for game start from server...")
        while True:
            msg = connector.client_socket.recv(1024).decode()
            print(f"[SERVER] {msg}")
            
            if msg == "setup_complete":
                print("[CLIENT] Starting local game client...")
                print("game_client created")
                game_client = Client(
                connector.client_socket,  
                connector.username,
                connector.client_id,
                hero_type=2
            ) 
                threading.Thread(target=game_client.send_input, daemon=True).start()
                threading.Thread(target=game_client.receive_state, daemon=True).start()

                while True:
                    game_client.render_game()
    except KeyboardInterrupt:
        print("[CLIENT] Client terminated by user.")
        if connector.client_socket:
            connector.client_socket.close()