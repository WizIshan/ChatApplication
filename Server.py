import socket
from threading import Thread
import os, sys, csv
from pprint import pprint
from pymongo import MongoClient

HOST = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDRESS = (HOST, PORT)
HEADERSIZE = 10

GRANT = True
REVOKE = False

online_users = {}
database_client = MongoClient('mongodb+srv://Server:Server009@chatcluster-n5m5n.mongodb.net/Users?retryWrites=true&w=majority')
database = database_client.get_database('Users').user_data

if database_client.server_info() :
    print('Connected with database')
else:
    print('Database error')


# def disconnect_user(clientsocket, ):
#     database.update_one({})

def listen_from_clients(sender, online_users):
    print(f"Listening to {sender}")
    sender_username = ""
    for user, value in online_users.items():
        if value["Socket"] == sender:
            sender_username = user

    #Check here for if online or not
    #if online 
    #pprint(online_users)

    while True:
        print("Here")
        message_type = int(sender.recv(1).decode('utf-8'))
        print("Sender  - ",sender_username)
        print("Message Type - ", message_type)
        if message_type == 3:
            reciever_len = int(sender.recv(HEADERSIZE).decode('utf-8'))
            reciever = sender.recv(reciever_len).decode('utf-8')
            message_len = int(sender.recv(HEADERSIZE).decode('utf-8'))
            message = sender.recv(message_len).decode('utf-8')
            print(reciever)
            print(message)

            if reciever in online_users.keys():
                print("Reciever is Online")
                send_message(online_users[reciever]['Socket'], message)
            else :
                print("Reciever is Offline")
                send_message(sender, "Reciever is Offline")
                print("Message Sent")
        elif message_type == 4:
            print("Disconnecting Client")
            database.update_one({"Username" : sender_username}, {"$set" : {"Access" : False}})
            del online_users[sender_username]
            sender.close()
            pprint(online_users)
            break
        else:
            print("Invalid Request Type")
            break

        

def enter_data(data):
    database.insert_one(data)

def validate_user(user, password):
    print("Validating")
    print(database.count_documents({"$and" : [{"Username" : user}, {"Password" : password}, {"Access" : False}]}))

    if database.count_documents({"$and" : [{"Username" : user}, {"Password" : password}, {"Access" : False}]}) == 1:
        database.update_one({"$and" : [{"Username" : user}, {"Password" : password}, {"Access" : False}]}, {"$set" : {"Access" : True}})
        return True
    return False


def send_message(clientsocket, message):
    clientsocket.send(bytes(str(message), 'utf-8'))

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    return server

def Grant_Chat_Access(clientsocket, address):
    message_type = clientsocket.recv(1).decode('utf-8')
    userlen = int(clientsocket.recv(HEADERSIZE).decode('utf-8').strip())
    user = clientsocket.recv(userlen).decode('utf-8')
    passlen = int(clientsocket.recv(HEADERSIZE).decode('utf-8').strip())
    password = clientsocket.recv(passlen).decode('utf-8')
    print(message_type)
    print(user)
    print(password)

    if message_type == '0' :
        enter_data({"Username" : user, "Password" : password, "Access" : GRANT})
        return (True,user)

    elif message_type == '1':
        status = validate_user(user, password)

        send_message(clientsocket, status)

        return (status,user)
        
    else:
        send_message(clientsocket, 'Invalid Access, Closing Connection')
        return (False, None)

def accept_incoming_connections(server, online_users):
    while True:
        clientsocket, address = server.accept()
        print(f'Client with {address} has been connected')
        #send_message(clientsocket, 'Connection Established') 
        Access_response = Grant_Chat_Access(clientsocket, address)
        if Access_response[0] is True:
            online_users[Access_response[1]] = {
                'Address' : address,
                'Socket' : clientsocket
            }
            send_message(clientsocket, True)
            print("Calling this Thread")
            Thread(target=listen_from_clients, args=(clientsocket,online_users,)).start()
        else:
            send_message(clientsocket, False)
            clientsocket.close()
        


def GenerateKey():
    # Here Deffie Hellman is applied to generate key
    return 13


if __name__ == "__main__":
    server = Server()
    server.listen(10)
    print('Server has been started')
    print('Waiting for connections')
    Recieve_thread = Thread(target=accept_incoming_connections, args=(server,online_users,))
    Recieve_thread.start()
    Recieve_thread.join()