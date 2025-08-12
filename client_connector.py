import pygame
import socket
from Client_online import Client
import uuid 
from src.utils import get_my_local_ip


SERVER_IP = 'b24ebf58-d845-4345-bf3e-f31854065465.hsvc.ir'  
SERVER_PORT = 28640

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
        Talk to the server to perform signup/login.
        Server returns either "OK:<id>" or "ERR:<reason>".
        Returns True on success, False on failure.
        """
        try:
            # first message from server (Login/Signup prompt)
            prompt = self.client_socket.recv(1024).decode()
            print(f"[SERVER] {prompt}")

            action = input("Login/Signup(1/2):").strip()
            if action not in ("1", "2"):
                print("[CLIENT] Invalid action. Please enter '1' to login or '2' to signup.")
                try:
                    self.client_socket.close()
                except:
                    pass
                return False

            self.client_socket.sendall(action.encode())

            while True:
                server_msg = self.client_socket.recv(1024).decode()
                if not server_msg:
                    print("[CLIENT] Server closed the connection.")
                    try:
                        self.client_socket.close()
                    except:
                        pass
                    return False

                print(f"[SERVER] {server_msg}")

                if server_msg.startswith("USERNAME:") or server_msg.startswith("Choose username:") or server_msg.startswith("Username:"):
                    username = input("Username:").strip()
                    self.client_socket.sendall(username.encode())

                elif server_msg.startswith("Password:") or server_msg.startswith("Choose password:") or server_msg.startswith("Password"):
                    password = input("Password:").strip()
                    self.client_socket.sendall(password.encode())

                elif server_msg.startswith("OK:"):
                    self.client_id = server_msg.split(":", 1)[1].strip()
                    try:
                        self.username = username
                    except UnboundLocalError:
                        pass
                    print(f"[CLIENT] Your assigned ID: {self.client_id}")
                    return True

                elif server_msg.startswith("ERR:"):
                    reason = server_msg.split(":", 1)[1]
                    print(f"[CLIENT] Server error: {reason}")
                    if "Invalid username/password" in reason:
                        try:
                            self.client_socket.close()
                        except:
                            pass
                        return False

                else:
                    print(f"[CLIENT] Received: {server_msg}")
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