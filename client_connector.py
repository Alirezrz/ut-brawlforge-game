import pygame
import socket
import threading
from run_client_interface import Client
from run_multiplayer import MultiplayerGame

BROADCAST_PORT = 9192
BROADCAST_MSG = b"DISCOVER_SERVER"
SERVER_PORT = 9191

timeout = 5  # seconds


class ClientConnector:
    def __init__(self):
        self.server_address = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(timeout)

        self.find_server()

        if self.server_address:
            self.connect_to_server()
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
            # You can now start your multiplayer game or client logic
            # For example:
            # MultiplayerGame(self.client_socket)
        except Exception as e:
            print(f"[CLIENT] Failed to connect to server: {e}")


