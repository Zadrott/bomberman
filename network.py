# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket
import pickle

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:
    def __init__(self, model, port):
        self.model = model
        self.port = port
        #init socket
        self.socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('', 7777))
        self.socket_server.listen(1)

    def gestion_clients():
        while(true):
            serv_model = pickle.dumps([self.model.map.height, self.model.map.width, self.model.map.array] )
            #faire threads pour les clients
            socket_server.sendall(serv_model)
        
   


    # time event
    def tick(self, dt):
        # ...
        return True

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, host, port, nickname):
        self.nickname = nickname
        self.host = host
        self.port = port 
        # init socket
        self.socket_client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_client.bind(('', 7777))
        self.socket_client.listen(1)
        # load map
        self.socket_client(send.
        pickle.loads()
        
        



        #fruits-> boucle for car plusieurs


        
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
        while True:
            # make sure game doesn't run at more than FPS frames per second
            dt = clock.tick(FPS)
            server.tick(dt)
            model.tick(dt)
            # view.tick(dt)
            return True
