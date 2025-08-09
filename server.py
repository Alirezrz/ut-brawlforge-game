import socket
import threading
import json
import random
import time
from multiplayergame import MultiplayerGame

HOST = '0.0.0.0'
PORT = 9191
SERVER_ADDRESS = (HOST, PORT)

clients = {}
lobbies = {}
active_games = {}

def send_json(conn, data):
    try:
        message = json.dumps(data) + '\n'
        conn.sendall(message.encode('utf-8'))
    except (socket.error, BrokenPipeError) as e:
        print(f"Could not send data: {e}")

def broadcast_lobby_update(lobby_id):
    if lobby_id in lobbies:
        lobby = lobbies[lobby_id]
        player_list = [clients[conn]["username"] for conn in lobby["players"]]
        update_message = {"type": "lobby_update", "players": player_list}
        for conn in lobby["players"]:
            send_json(conn, update_message)

def client_handler(conn):
    player_id = "0"
    username = "Guest"
    client_info = None

    try:
        initial_data_str = conn.recv(1024).decode('utf-8').strip()
        initial_data = json.loads(initial_data_str)
        username = initial_data.get("username", f"Guest_{random.randint(100,999)}")
        
        player_id = str(random.randint(1000, 9999))
        while player_id in [c['id'] for c in clients.values()]:
            player_id = str(random.randint(1000, 9999))

        client_info = {"id": player_id, "username": username, "lobby": None, "in_game": False}
        clients[conn] = client_info

        send_json(conn, {"type": "connection_success", "id": player_id})
        print(f"[+] {username} (ID: {player_id}) connected.")
        conn.settimeout(0.5)
        buffer = ""
        while True:
            if clients.get(conn) and clients[conn]["in_game"]:
                print(f"Handing off connection for in-game player {username} (ID: {player_id}).")
                break
            try:
               data = conn.recv(4096).decode('utf-8')
               if not data: break
               buffer += data
            except socket.timeout:
                continue
            while '\n' in buffer:
                message_raw, buffer = buffer.split('\n', 1)
                if not message_raw: continue
                
                request = json.loads(message_raw)
                action = request.get("action")

                if action == "create_game":
                    game_type = request.get("game_type", "1v1")
                    lobby_id = str(random.randint(1000, 9999))
                    lobbies[lobby_id] = {
                        "host": conn,
                        "players": {conn: player_id},
                        "game_type": game_type,
                        "pending_joiner": None
                    }
                    clients[conn]["lobby"] = lobby_id
                    send_json(conn, {"type": "lobby_created", "game_id": lobby_id, "players": [username], "game_type": game_type})
                    print(f"Lobby {lobby_id} ({game_type}) created by {username}.")

                elif action == "join_game":
                    game_id = request.get("game_id")
                    if game_id in lobbies:
                        lobby = lobbies[game_id]
                        max_players = 2 if lobby['game_type'] == '1v1' else 4
                        if len(lobby['players']) >= max_players:
                            send_json(conn, {"type": "join_denied", "message": "Lobby is full."}); continue
                        lobby["pending_joiner"] = conn
                        send_json(lobby["host"], {"type": "join_request", "username": username})
                    else:
                        send_json(conn, {"type": "join_denied", "message": "Lobby not found."})

                elif action == "host_decision":
                    lobby_id = clients[conn]["lobby"]
                    if lobby_id in lobbies and lobbies[lobby_id]["host"] == conn:
                        lobby = lobbies[lobby_id]
                        joiner_conn = lobby.get("pending_joiner")
                        if joiner_conn:
                            if request.get("decision") == "yes":
                                joiner_id = clients[joiner_conn]["id"]
                                lobby["players"][joiner_conn] = joiner_id
                                clients[joiner_conn]["lobby"] = lobby_id
                                send_json(joiner_conn, {"type": "join_accepted", "game_id": lobby_id, "players": [clients[c]["username"] for c in lobby["players"]], "game_type": lobby["game_type"]})
                                broadcast_lobby_update(lobby_id)
                            else:
                                send_json(joiner_conn, {"type": "join_denied", "message": "Host denied your request."})
                            lobby["pending_joiner"] = None
                elif action == "response_to_request":
                    target_id = request.get("target_id")
                    requester_info = clients[conn]
                    target_conn = None
                    for c, info in clients.items():
                        if info["id"] == target_id:
                            target_conn = c
                            break
                    if target_conn is None:
                        send_json(conn, {"type": "error", "message": "Player ID not found."})
                    elif clients[target_conn]["lobby"] or clients[target_conn]["in_game"]:
                        send_json(conn, {"type": "error", "message": "Player is currently busy."})
                    else:
                         send_json(target_conn, {
                            "type": "direct_game_request", 
                            "from_username": requester_info["username"],
                            "from_id": requester_info["id"]
                        })  
                elif action == "respond_to_request":
                    requester_id = request.get("from_id")
                    decision = request.get("decision")
                    responder_info = clients[conn]
                    requester_conn = None
                    for c, info in clients.items():
                        if info["id"] == requester_id:
                            requester_conn = c
                            break
                    
                    if requester_conn:
                        if decision == "accept":
                            lobby_id = str(random.randint(1000, 9999))
                            lobbies[lobby_id] = {
                                "host": requester_conn,
                                "players": {requester_conn: requester_id, conn: responder_info["id"]},
                                "game_type": "1v1",
                            }
                            clients[requester_conn]["lobby"] = lobby_id
                            clients[conn]["lobby"] = lobby_id
                            player_list = [clients[c]["username"] for c in lobbies[lobby_id]["players"]]
                            lobby_info = {"type": "lobby_created", "game_id": lobby_id, "players": player_list, "game_type": "1v1"}
                            send_json(requester_conn, lobby_info)
                            send_json(conn, lobby_info)
                        else:
                            
                            send_json(requester_conn, {"type": "error", "message": f"{responder_info['username']} denied your request."})                     
                elif action == "start_game":
                    lobby_id = clients[conn]["lobby"]
                    if lobby_id in lobbies and lobbies[lobby_id]["host"] == conn:
                        lobby = lobbies[lobby_id]
                        max_players = 2 if lobby['game_type'] == '1v1' else 4
                        if len(lobby["players"]) != max_players:
                            send_json(conn, {"type": "error", "message": f"Need {max_players} players to start."})
                            continue
            
                        
                        print(f"Host {username} is starting game for lobby {lobby_id}...")
                        
                        for player_conn in lobby["players"]:
                            clients[player_conn]["in_game"] = True
                        
                        player_connections = list(lobby["players"].keys())
                        teams = {1: [], 2: []}
                        if lobby["game_type"] == "2v2":
                            teams[1] = [player_connections[0], player_connections[1]]
                            teams[2] = [player_connections[2], player_connections[3]]

                        game = MultiplayerGame(lobby["game_type"])
                        active_games[lobby_id] = game
                        game.set_players(player_connections, teams)

                        for player_conn in lobby["players"]:
                            send_json(player_conn, {"type": "match_starting"})
                        
                        return

    except Exception as e:
        print(f"Error with client {player_id} ({username}): {e}")

    finally:
        conn.settimeout(None)
        if client_info and not client_info.get("in_game"):

            print(f"[-] Client {player_id} ({username}) disconnected before game start.")
            lobby_id = client_info.get("lobby")
            if lobby_id and lobby_id in lobbies:
                lobby = lobbies[lobby_id]
                lobby["players"].pop(conn, None)
                if not lobby["players"] or lobby["host"] == conn:
                    print(f"Host left or lobby empty, closing lobby {lobby_id}.")
                    for player_conn in lobby["players"]:
                        if player_conn != conn:
                            send_json(player_conn, {"type": "error", "message": "Host disconnected."})
                    lobbies.pop(lobby_id, None)
                else:
                    broadcast_lobby_update(lobby_id)
            clients.pop(conn, None)
            try: conn.close()
            except: pass
        elif client_info and client_info.get("in_game"):
             print(f"[+] Client {username} (ID: {player_id}) has entered a game. Handing off connection.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM); server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(SERVER_ADDRESS); server.listen(5); print(f"[*] Lobby server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler, args=(conn,)); thread.daemon = True; thread.start()

if __name__ == "__main__":
    main()