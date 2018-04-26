# -*- coding: Utf-8 -*
# Author: Ilo et Antho

from model import *
import socket
import pickle
import threading
import errno

###########################################
#                          NETWORK SERVER CONTROLLER                           #
###########################################

class NetworkServerController:
    def __init__(self, model, port):
        self.model = model
        self.port = port
        #init socket and threads
        self.socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('', self.port))
        self.socket_server.listen(1)
        self.liste_clients = []
        self.action = False
        threading.Thread(None, self.connexion, None, ()).start()

        
    def connexion(self):
        #main thread create a thread per client
        while (True) :
            socket_accepte, adr = self.socket_server.accept()
            self.liste_clients.append(socket_accepte)
            threading.Thread(None, self.gestion_clients, None, (socket_accepte, adr)).start()

    def gestion_clients(self, socket_client, adr):
        while(True):
            if(socket_client.recv(1500).decode() == "map"):
                serv_map = pickle.dumps([self.model.map.height, self.model.map.width, self.model.map.array] )
                socket_client.sendall(serv_map)
            if(socket_client.recv(1500).decode() == "nickname"):
                socket_client.send("ack".encode())
                self.model.add_character(socket_client.recv(1500).decode)
                self.send_model()
                
    def send_model(self):                 #à faire à chaque changement
        for client in self.liste_clients:
            serv_model = pickle.dumps([self.model.characters, self.model.fruits, self.model.bombs])
            client.sendall(serv_model)
            

   
    

    # time event
    def tick(self, dt):
        return True

##########################################
#                          NETWORK CLIENT CONTROLLER                          #
##########################################

class NetworkClientController:

    def __init__(self, model, host, port, nickname):
        self.nickname = nickname
        self.host = host
        self.port = port
        self.model = model
        # init socket
        self.socket_client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_client.connect((host, port))
        # init map
        self.socket_client.send("map".encode())
        self.model.map.height, self.model.map.width, self.model.map.array = pickle.loads(self.socket_client.recv(1500))
        # init character
        self.socket_client.sendall("nickname".encode())
        self.socket_client.recv(1500)
        self.socket_client.send(self.nickname.encode())
        
        self.receive_model()


    def receive_model(self):
        self.model.characters, self.model.fruits, self.model.bombs = pickle.loads(self.socket_client.recv(1500))

        
    # keyboard events

    def keyboard_quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        # ...
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        # ...
        return True

    # time event

    def tick(self, dt):
        return True
