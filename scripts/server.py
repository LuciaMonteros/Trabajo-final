import socket
import threading
import configparser
import pathlib

config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

HOST = config['SERVER']['host']
PORT = int(config['SERVER']['port'])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"conectado con {str(address)}")

        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        client.send("conectado al servidor\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"server corriendo en {socket.gethostbyname(socket.gethostname())}, puerto {PORT}")
receive()