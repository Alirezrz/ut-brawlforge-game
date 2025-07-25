import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '192.168.1.6'
        self.port = 65435
        self.addr = (self.host, self.port)
        self.player_id = None
    def connect(self,username):
        try:
            self.client.connect(self.addr)
            self.client.sendall(json.dumps({'username': username}).encode('utf-8'))
            response_data = self.client.recv(1024).decode('utf-8')
            response = json.loads(response_data)
            if response.get('type') == 'connection_success':
                self.player_id = response.get('id')
                print(f"Connected to server as player {self.player_id}")
                return True
            else:
                print("Failed to connect to server.")
                return False
        except socket.error as e:
            print(f"Could not connect to server: {e}")

    def send(self,data):
        try:
            self.client.sendall(json.dumps(data).encode('utf-8'))
            return json.loads(self.client.recv(2048).decode('utf-8'))
        except socket.error as e:
            print(e)
    def disconnect(self):
        self.client.close()