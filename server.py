import pygame 
import socket 
import threading 
from run_client_interface import Client
from run_multiplayer import MultiplayerGame


HOST='0.0.0.0'
PORT=9191
BROADCAST_PORT=9192
BROADCAST_MSG = b"DISCOVER_SERVER"




class Server:
    def __init__(self):
        # TCP socket for client connections
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print(f"[SERVER] Listening for clients on {HOST}:{PORT}")

        # UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.connected_clients = []

        # Start the thread that listens for clients
        threading.Thread(target=self.accept_clients, daemon=True).start()
        
        # Start the thread that broadcasts the server presence
        threading.Thread(target=self.broadcast_presence, daemon=True).start()
        
    def accept_clients(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f"[SERVER] Client connected from {addr}")
            self.connected_clients.append((client_socket, addr))

    def broadcast_presence(self):
        while True:
            self.broadcast_socket.sendto(BROADCAST_MSG, ('<broadcast>', BROADCAST_PORT))
            pygame.time.wait(1000) 
            