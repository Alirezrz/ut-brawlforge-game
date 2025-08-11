import pygame
import socket
from Client_online import Client
import uuid 
from src.utils import get_my_local_ip


SERVER_IP = get_my_local_ip()  
SERVER_PORT = 9191

timeout = 30 # seconds
users=[
    {
        'username':'alireza',
        'password':'0000',
        'id':'1'
    }
]

class ClientConnector:
    def __init__(self):
        self.server_address = SERVER_IP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(timeout)
        self.username = None
        self.client_id = None
        self.connected = False   

        self.connect_to_server()
        if self.connected and self.exchange_user_info():
            self.send_request_option()
        else:
            print("[CLIENT] Not proceeding because user exchange or connection failed.")

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
            self.connected = True
        except Exception as e:
            print(f"[CLIENT] Failed to connect to server: {e}")
            try:
                self.client_socket.close()
            except:
                pass
            self.connected = False

    def exchange_user_info(self):
        """
        Returns True on success, False on failure.
        Does not leave the caller assuming the socket is usable if it failed.
        """
        try:
            prompt = self.client_socket.recv(1024).decode()
            print(f"[SERVER] {prompt}")

            action = input("Login/Signup(1/2):").strip()
            if action == '1':
                # LOGIN
                Flag = True
                while Flag:
                    username = input("Username:").strip()
                    password = input("Password:").strip()
                    valid = False
                    for user in users:
                        if user['username'] == username and user['password'] == password:
                            self.username = username
                            valid = True
                            Flag = False
                            break
                    if not valid:
                        print("Invalid username or password — try again.")

            elif action == '2':
                # SIGNUP
                while True:
                    username = input("Choose a username:").strip()
                    if not username:
                        print("Username cannot be empty.")
                        continue

                    # check uniqueness
                    if any(u['username'] == username for u in users):
                        print("That username is already taken. Try another.")
                        continue

                    password = input("Choose a password:").strip()
                    password_confirm = input("Confirm password:").strip()
                    if password != password_confirm:
                        print("Passwords do not match — try again.")
                        continue

                    # optional: basic password length check
                    if len(password) < 4:
                        print("Password too short (min 4 chars).")
                        continue

                    # create user and assign id
                    new_id = str(uuid.uuid4())
                    users.append({
                        'username': username,
                        'password': password,
                        'id': new_id
                    })
                    self.username = username
                    print(f"User '{username}' created with id {new_id}.")
                    break

            else:
                print("[CLIENT] Invalid action. Please enter '1' to login or '2' to signup.")
                try:
                    self.client_socket.close()
                except:
                    pass
                return False

            if not self.username:
                print("[CLIENT] Username cannot be empty.")
                try:
                    self.client_socket.close()
                except:
                    pass
                return False

            # send chosen username to server and receive assigned client_id
            self.client_socket.sendall(self.username.encode())
            self.client_id = self.client_socket.recv(1024).decode()
            print(f"[CLIENT] Your assigned ID: {self.client_id}")
            return True

        except Exception as e:
            print(f"[CLIENT] Failed to exchange user info: {e}")
            try:
                self.client_socket.close()
            except:
                pass
            return False


    def send_request_option(self):
        try:
            print("Choose an option:")
            print("1. Create a game")
            print("2. Join a game")
            option = input("Enter 1 or 2: ")
            if option not in ["1", "2"]:
                print("[CLIENT] Invalid option.")
                try:
                    self.client_socket.close()
                except:
                    pass
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
                    try:
                        self.client_socket.settimeout(timeout)
                    except:
                        pass
            else:
                try:
                    result = self.client_socket.recv(1024).decode()
                    print(f"[SERVER] {result}")
                    while True:
                        try:
                            self.client_socket.settimeout(30.0)
                            message = self.client_socket.recv(1024).decode()
                            print(f"[SERVER] {message}")
                            if "Game is starting" in message:
                                break
                            elif "Accept? (yes/no)" in message:
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
            try:
                self.client_socket.close()
            except:
                pass


if __name__ == '__main__':
    connector = ClientConnector()

    try:
        print("[CLIENT] Waiting for game start from server...")
        if not getattr(connector, "connected", False) or not getattr(connector, "username", None):
            print("[CLIENT] Not connected or not logged-in; exiting.")
        else:
            connector.client_socket.settimeout(120.0)
            while True:
                msg = connector.client_socket.recv(1024).decode()
                print(f"[SERVER] {msg}")
                
                if msg == "setup_complete":
                    print("[CLIENT] Starting local game client...")
                    type=int(input("Enter your hero type:\n1 _ Roboman\n2_Ninja\n3_ NinjaGirl\n4_Archer\n"))
                    map={1:"Roboman",2:"Ninja",3:"NinjaGirl",4:"Archer"}
                    type=map[type]
                    print("game_client created")
                    game_client = Client(
                        connector.client_socket,  
                        connector.username,
                        connector.client_id,
                        hero_type=type
                    ) 
                    break
            game_client.start()
    except KeyboardInterrupt:
        print("[CLIENT] Client terminated by user.")
        if getattr(connector, "client_socket", None):
            try:
                connector.client_socket.close()
            except:
                pass