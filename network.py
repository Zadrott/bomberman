# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:
    def __init__(self, model, port):
        self.model = model
        self.port = port

        #envoi map & model
        send_socket_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        send_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        send_socket_server.bind(('', 7777))

        print(model)
        serv_model = model.encode
        send_socket_server.send(serv_model)
        
   


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

        
        #model
        self.receive_socket_client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.receive_socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket_client.bind(('', 7777))
        self.receive_socket_client.listen(0)
        while True:
            sclient, addr = self.receive_socket_client.accept()
            print('Connected by', addr)
            while True:
                server_model = sclient.recv(1500)
                print(server_model)
        self.model = server_model.decode()
        

##        #map
##        self.receive_socket_client.send("map".encode)
##        map_to_load = (self.receive_socket_client.recv(1500).decode())
##        self.model.load_map(self.map_to_load)

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
