# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket
import pickle
import threading
import errno

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:
    def __init__(self, model, port):
        self.model = model
        self.port = port
        #init socket and threads
        self.socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('', self.port))
        self.socket_server.listen(1)
        threading.Thread(None, self.connexion, None, ()).start()

        
    def connexion(self):
        #main thread create a thread per client
        while (True) :
            socket_accepte, adr = self.socket_server.accept()
            threading.Thread(None, self.gestion_clients, None, (socket_accepte, adr)).start()

    def gestion_clients(self, socket_client, adr):
        while(True):
            if(socket_client.recv(1500).decode() == "map"):
                serv_map = pickle.dumps([self.model.map.height, self.model.map.width, self.model.map.array] )
                socket_client.sendall(serv_map)
            #reception nickname
            #socket_client.recv(1500)
                
            #def send_model():                        #à faire à chaque changement
            serv_model = pickle.dumps([self.model.characters, self.model.fruits, self.model.bombs])
            socket_client.sendall(serv_model)

   
    

    # time event
    def tick(self, dt):
            return True

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

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
        self.map = pickle.loads(self.socket_client.recv(1500))
        self.model.map.height = self.map[0]
        self.model.map.width = self.map[1]
        self.model.map.array = self.map[2]
        
#### #################  en cours  ################################################
        # envoi nickmame
        #self.socket_client.send(nickname.encode())

        
    #def receive_model(self):
        self.model.characters, self.model.fruits, self.model.bombs = pickle.loads(self.socket_client.recv(1500))
##        received_model = pickle.loads(self.socket_client.recv(1500))
##        self.model.characters = self.received_model[0]
##        self.model.fruits = self.received_model[1]
##        self.model.bombs = self.received_model[2]

        
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
