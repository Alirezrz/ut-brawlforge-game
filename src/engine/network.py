import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 9191
        self.addr = (self.host, self.port)
        self.player_id = None
    def connect(self,username):
        try:
            self.client.connect(self.addr)
            self.username = username
            self.client.sendall(json.dumps({"username": username}).encode('utf-8'))
            response_raw = self.client.recv(1024).decode('utf-8')
            response = json.loads(response_raw)
            if response.get("type") == "connection_success":
                self.player_id = response.get("id")
                print(f"Connected to server as {self.username} with ID {self.player_id}")
                return True
            else:
                print(f"Connection failed: {response.get('message')}")
                return False
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Could not connect to server: {e}")
            return False
    def send_request(self, request_data):
        try:
            self.client.sendall(json.dumps(request_data).encode('utf-8'))
            response_raw = self.client.recv(2048).decode('utf-8')
            return json.loads(response_raw)
        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error sending/receiving data: {e}")
            return None
    def disconnect(self):
        self.client.close()