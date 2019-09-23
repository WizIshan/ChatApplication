import socket
from threading import Thread
import tkinter

HOST = "192.168.56.1"
PORT = 7000
SERVER_ADDRESS = (HOST, PORT)
HEADERSIZE = 10
IPSIZE = 15

def recieve(client):
     while True:
        try:
            msg = client.recv(1024).decode("utf8")
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break


def create_client():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(SERVER_ADDRESS)
    return clientsocket

if __name__ == '__main__':
    client = create_client()
    recieve_thread = Thread(target=recieve, args=(client,))
    recieve_thread.start()
