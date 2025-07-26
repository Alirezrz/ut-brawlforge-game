import socket
import threading
import json
import uuid
import time


HOST = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
PORT = 65432


players = {}         
waiting_room = {
    "1v1": [],
    "2v2": []
}
active_games = {} 

def check_for_matches():
    """Checks the waiting room and creates matches if possible."""
    while True:
        if len(waiting_room["1v1"]) >= 2:
            p1_id = waiting_room["1v1"].pop(0)
            p2_id = waiting_room["1v1"].pop(0)
            game_id = str(uuid.uuid4())
            active_games[game_id] = [p1_id, p2_id]
            
            print(f"[MATCH FOUND] 1v1 match created: {p1_id} vs {p2_id}")
            match_data = json.dumps({
                "type": "match_found",
                "payload": {
                    "game_id": game_id,
                    "opponents": {p1_id: players[p1_id]['username'], p2_id: players[p2_id]['username']}
                }
            })
            if p1_id in players: players[p1_id]['conn'].sendall(match_data.encode('utf-8'))
            if p2_id in players: players[p2_id]['conn'].sendall(match_data.encode('utf-8'))
        if len(waiting_room["2v2"]) >= 4:
            print("2v2 match found!")

        time.sleep(1)

def handle_client(conn, addr, player_id):
    """Handles a single client connection."""
    print(f"[NEW CONNECTION] {addr} connected with ID: {player_id}")
    
    try:
        username_data = conn.recv(1024).decode('utf-8')
        username = json.loads(username_data).get('username', 'Guest')
        
        players[player_id] = {'username': username, 'conn': conn, 'state': {}}
        print(f"Player {player_id} set username to: {username}")

        initial_data = json.dumps({'type': 'connection_success', 'id': player_id})
        conn.sendall(initial_data.encode('utf-8'))
        
    except Exception as e:
        print(f"[ERROR] Could not set up client {addr}: {e}")
        conn.close()
        return

    connected = True
    while connected:
        try:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                break

            message = json.loads(data)
            msg_type = message.get("type")
            payload = message.get("payload")

            if msg_type == "join_waiting_room":
                game_mode = payload.get("game_mode")
                if game_mode in waiting_room and player_id not in waiting_room[game_mode]:
                    waiting_room[game_mode].append(player_id)
                    print(f"Player {players[player_id]['username']} joined {game_mode} waiting room.")
                    conn.sendall(json.dumps({"type": "waiting", "payload": {"status": "You are in the waiting room..."}}).encode('utf-8'))

            elif msg_type == "search_by_id":
                target_id = payload.get("target_id")
                if target_id in players:
                    print(f"Player {player_id} wants to play with {target_id}")
                else:
                    conn.sendall(json.dumps({"type": "error", "payload": {"message": "ID not found"}}).encode('utf-8'))
        except (ConnectionResetError, json.JSONDecodeError):
            break
        except Exception as e:
            print(f"An error occurred with {player_id}: {e}")
            break

    print(f"[DISCONNECTED] {players[player_id]['username']} ({addr}) disconnected.")
    for mode in waiting_room:
        if player_id in waiting_room[mode]:
            waiting_room[mode].remove(player_id)
    del players[player_id]
    conn.close()

def start_server():
    """Main function to start the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    threading.Thread(target=check_for_matches, daemon=True).start()

    while True:
        conn, addr = server_socket.accept()
        player_id = str(uuid.uuid4())
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

if __name__ == "__main__":
    start_server()