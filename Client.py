import socket
from threading import Thread
import tkinter, sys
from distutils.util import strtobool

HOST = "192.168.56.1"
PORT = 7000
SERVER_ADDRESS = (HOST, PORT)
HEADERSIZE = 10

def recieve(client):
     while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            print(msg)
        except OSError:  # Possibly client has left the chat.
            break

def ping(event=None):
    #Take the input from the ChatRoom GUI
    reciever = 'Client2'
    message = 'Hii'
    message_type = 3
    if(message == "#Quit"):
        message_type = 4

    data = f'{message_type}' +f'{len(reciever) :< {HEADERSIZE}}' + f'{reciever}' + f'{len(message) :< {HEADERSIZE}}' + f'{message}'
    print(data)
    client.send(bytes(data, 'utf-8'))

def Quit(event=None):
    #Take the input from the ChatRoom GUI
    message = '#Quit'
    message_type = 4

    data = f'{message_type}' + f'{len(message) :< {HEADERSIZE}}' + f'{message}'
    print(data)
    client.send(bytes(data, 'utf-8'))
    print("Disconnection from Server")
    client.close()

def create_client():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(SERVER_ADDRESS)
    return clientsocket

def Request_Chat_Access(event=None):
    # button_clicked (if register and then the outcome is false then return user already exists else if login then invalid username/password) (This will be built after the GUI is integrated)
    user = 'Client1' # To be taken from GUI
    password = '12345' # To be taken from GUI
    message_type = 1 # To be decided from either register button or login button
    message = f'{message_type}' + f'{len(user):<{HEADERSIZE}}' + f'{user}' + f'{len(password) :< {HEADERSIZE}}' + f'{password}'
    print(message)
    print('Sending Message')
    client.send(bytes(message, 'utf-8'))
    msg = bool(strtobool(client.recv(1024).decode('utf-8')))
    if msg == True:
        print('Access Granted')
        print(msg)
        return True
    else :
        # According to the button clicked the message will be printed to user
        print('Access Denied')
        print(msg)
        return False
        

if __name__ == '__main__':
    client = create_client()
    #Start Register/Login GUI
    #Request_Chat_Access is triggered from Login GUI
    if Request_Chat_Access() is True:
        #Close the Registeration/Login GUI and move forward with Chat GUI
        ping()
        recieve_thread = Thread(target=recieve, args=(client,))
        recieve_thread.start()
        x = input()
        Quit()
    else:
        client.close()
        sys.exit()