import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 9191
        self.addr = (self.host, self.port)
        self.player_id = None
        self.username = None
        self.buffer = ""

    def connect(self, username):
        try:
            self.client.connect(self.addr)
            self.username = username
            self.send_json({"username": username})
            response = self.recv_json()
            if response and response.get("type") == "connection_success":
                self.player_id = response.get("id")
                print(f"Connected to server as {self.username} with ID {self.player_id}")
                return True
            self.disconnect()
            return False
        except Exception as e:
            print(f"Could not connect to server: {e}")
            self.disconnect()
            return False

    def send_json(self, data):
        try:
            message = json.dumps(data) + '\n'
            self.client.sendall(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def recv_json(self):
        while '\n' not in self.buffer:
            try:
                data = self.client.recv(2048).decode('utf-8')
                if not data: return None
                self.buffer += data
            except socket.error as e:
                print(f"Error receiving data: {e}")
                return None
        message_raw, self.buffer = self.buffer.split('\n', 1)
        return json.loads(message_raw)

    def disconnect(self):
        try: self.client.close()
        except: pass