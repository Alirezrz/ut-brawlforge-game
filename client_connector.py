
import socket
import json


SERVER_IP = 'b24ebf58-d845-4345-bf3e-f31854065465.hsvc.ir'  
SERVER_PORT = 28640
TIMEOUT = 30

class ClientConnector:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(TIMEOUT)
        self.username = None
        self.client_id = None
        self.connected = False
        self.client = self.client_socket 

    def connect_to_server(self):
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"[CLIENT] Connected to server at {SERVER_IP}:{SERVER_PORT}")
            self.connected = True
            return True, "Connected successfully"
        except Exception as e:
            print(f"[CLIENT] Failed to connect to server: {e}")
            self.connected = False
            return False, f"Failed to connect: {e}"

    def authenticate(self, action, username, password):
        try:
            self.client_socket.recv(1024) 
            self.client_socket.sendall(action.encode())
            self.client_socket.recv(1024) 
            self.client_socket.sendall(username.encode())
            self.client_socket.recv(1024)
            self.client_socket.sendall(password.encode())
            response = self.client_socket.recv(1024).decode()
            if response.startswith("OK:"):
                self.client_id = response.split(":", 1)[1].strip()
                self.username = username
                return True, "Authentication successful!"
            elif response.startswith("ERR:"):
                reason = response.split(":", 1)[1].strip()
                return False, reason
            else:
                return False, "Unknown server response."

        except Exception as e:
            print(f"[CLIENT] Authentication error: {e}")
            return False, f"Error: {e}"