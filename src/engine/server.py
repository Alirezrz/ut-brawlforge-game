import socket
import threading
import json
import uuid

HOST = '192.168.1.6'
PORT = 65435

players = {}
def handle_client(conn,addr,player_id):
    print(f"[NEW CONNECTION] {addr} connected with ID: {player_id}")
    try:
        username_data = conn.recv(1024).decode('utf-8')
        username = json.loads(username_data).get('username','Guest')
        players[player_id] = {'username':username,'conn':conn}
        print(f"Player {player_id} set username to: {username}")
        initial_data = json.dumps({'type':'connection_success','id':player_id})
        conn.sendall(initial_data.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Could not set up{addr}:{e}")
        conn.close()
        return
    connected = True
    while connected:
        try:
            pass
        except:
            connected= False
    print(f"[DISCONNECTED] {players[player_id]['username']} ({addr}) disconnected.")
    del players[player_id]
    conn.close()
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server_socket.accept()
        player_id = str(uuid.uuid4())
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
if __name__ == "__main__":
    start_server()
