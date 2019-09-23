import socket
from threading import Thread
from ast import literal_eval
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDRESS = (HOST, PORT)
HEADERSIZE = 10
IPLENGTH = 100

all_address = {}

def listen_from_clients(sender,all_address):
    reciever_ip_len = sender.recv(IPLENGTH).decode('utf-8')
    reciever_ip = sender.recv(reciever_ip_len).decode('utf-8')
    message_len = sender.recv(HEADERSIZE).decode('utf-8')
    message = sender.recv(int(message_len.strip())).decode('utf-8')

    #reciever = all_address[]

    return

def send_message(clientsocket, message):
    clientsocket.send(bytes(message, 'utf-8'))

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    return server

def accept_incoming_connections(server,all_address):
    while True:
        clientsocket, address = server.accept()
        print(f'Client with {address} has been connected')
        all_address[address] = {
            'address' : address,
            'key' : GenerateKey(),
            'socket' : clientsocket
        }
        print(all_address)
        send_message(clientsocket, 'Connection Established')
        Thread(target=listen_from_clients, args=(clientsocket, all_address,))


def GenerateKey():
    # Here Deffie Hellman is applied to generate key
    return 13


if __name__ == "__main__":
    server = Server()
    server.listen(10)
    print('Server has been started')
    print('Waiting for connections')
    Recieve_thread = Thread(target=accept_incoming_connections, args=(server,all_address,))
    Recieve_thread.start()
    Recieve_thread.join()