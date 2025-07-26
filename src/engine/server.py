import socket
import threading
import json
import time
import pygame 

from Ninja import Ninja
from Roboman import Roboman
from NinjaGirl import NinjaGirl
from Archer import Archer

HOST = "0.0.0.0"
PORT = 9191

class multiplayer_game:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.clients = [] 
        self.player_inputs = {} 
        self.heroes = {} 
        self.game_active = False

    def create_hero(self, char_name, x, y, index, username):
        if char_name == "Roboman": return Roboman(x, y, 1280, 720, index, username)
        if char_name == "Ninja": return Ninja(x, y, 1280, 720, [], index, username)
        if char_name == "NinjaGirl": return NinjaGirl(x, y, 1280, 720, [], index, username)
        if char_name == "Archer": return Archer(x, y, [], index, username)
        return Ninja(x, y, 1280, 720, [], index, username) 

    def client_thread(self, conn, player_index):
        print(f"Player {player_index} connected")
        try:
            
            initial_data = json.loads(conn.recv(1024).decode('utf-8'))
            username = initial_data.get("username", f"Player{player_index+1}")
            char_choice = initial_data.get("character", "Ninja")
            hero = self.create_hero(char_choice, 400 + player_index * 400, 400, player_index + 1, username)
            self.heroes[conn] = hero
            self.player_inputs[conn] = {}
            conn.sendall(json.dumps({"status": "setup_complete"}).encode('utf-8'))

        except Exception as e:
            print(f"Error with client {player_index} during setup: {e}")
            conn.close()
            return
        while True:
            try:
                data = conn.recv(2048).decode('utf-8')
                if not data:
                    break
                self.player_inputs[conn] = json.loads(data)
            except:
                break
        
        print(f"Player {player_index} disconnected.")
        self.clients.remove(conn)
        del self.heroes[conn]
        del self.player_inputs[conn]
        conn.close()

    def game_loop(self):
        """This is the main, authoritative game loop running on the server."""
        clock = pygame.time.Clock()
        while self.game_active:
            hero1, hero2 = self.heroes.values()
            inputs1 = self.player_inputs.get(self.clients[0], {})
            inputs2 = self.player_inputs.get(self.clients[1], {})
            if inputs1.get("D"): hero1.move_right()
            if inputs1.get("A"): hero1.move_left()
            hero1.gravity()
            hero1.vertical_move()
            hero1.update_animation(None) 
        
            if inputs2.get("D"): hero2.move_right()
            if inputs2.get("A"): hero2.move_left()
            hero2.gravity()
            hero2.vertical_move()
            hero2.update_animation(None)
            state_p1 = hero1.serialize()
            state_p2 = hero2.serialize()
            response_for_p1 = {"self": state_p1, "opponent": state_p2}
            response_for_p2 = {"self": state_p2, "opponent": state_p1}
            try:
                self.clients[0].sendall(json.dumps(response_for_p1).encode('utf-8'))
                self.clients[1].sendall(json.dumps(response_for_p2).encode('utf-8'))
            except Exception as e:
                print(f"Error sending state, ending game: {e}")
                self.game_active = False

            clock.tick(30) 

    def start(self):
        self.server_socket.listen(2)
        print(f"Server started on {HOST}:{PORT}, waiting for 2 players...")
        
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            thread = threading.Thread(target=self.client_thread, args=(conn, len(self.clients) - 1))
            thread.daemon = True
            thread.start()
        
        print("Both players connected. Starting the game in 3 seconds...")
        time.sleep(3)
        self.game_active = True
        self.game_loop()

