import socket
from threading import Thread
import pickle
from game import Game

SERVER = "192.168.0.100"
PORT = 12344

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER, PORT))
except socket.error as e:
    print(e)
s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player_id: int, game_id: int):
    global idCount
    connection.send(str.encode(str(player_id)))

    while True:
        try:
            data = connection.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "__reset":
                        game.reset()
                    elif data != "__get":
                        game.play(player_id, data)

                    connection.sendall(pickle.dumps(game))
            else:
                break
        except socket.error as exception:
            print(f"{exception} --- User has disconnected")
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except Exception as exception:
        print(f"{exception} --- No game (game_id = {game_id}) to delete")
    idCount -= 1
    connection.close()


if __name__ == '__main__':

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        idCount += 1
        player_id = 0
        game_id = (idCount - 1) // 2
        if idCount % 2 == 1:
            games[game_id] = Game(game_id)
            print("Creating a new game...")
        else:
            games[game_id].ready = True
            player_id = 1

        Thread(target=threaded_client, daemon=True, args=(conn, player_id, game_id)).start()
