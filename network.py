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
            msg = socket_client.recv(1500).decode()
            if(msg == "map"):
                serv_map = pickle.dumps([self.model.map.height, self.model.map.width, self.model.map.array] )
                socket_client.sendall(serv_map)
            if(msg == "nickname"):
                self.model.add_character(pickle.loads(socket_client.recv(1500))[0])
                self.action = True
            if(msg == "move"):
                nickname, direction = pickle.loads(socket_client.recv(1500))
                self.model.move_character(nickname, int(direction))
                self.action = True
            if(msg == "bomb"):
                nick = pickle.loads(socket_client.recv(1500))[0]
                self.model.drop_bomb(nick)
                self.action = True
                
    def send_model(self):
        for client in self.liste_clients:
            serv_model = pickle.dumps([self.model.characters, self.model.fruits, self.model.bombs])
            client.sendall(serv_model)
            

    # time event
    def tick(self, dt):
        #Envoi le modèle aux clients dès qu'une action se produit
        if self.action == True :
            self.send_model()
            self.action = False
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
        self.socket_client.send(pickle.dumps([self.nickname]))
        self.socket_client.setblocking(False)

    def receive_model(self):
        try: 
            self.model.characters, self.model.fruits, self.model.bombs = pickle.loads(self.socket_client.recv(10000))
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                pass
            else:
                print("error:", e)

        
    # keyboard events

    def keyboard_quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        self.socket_client.sendall("move".encode())
        self.socket_client.send(pickle.dumps([self.nickname, direction]))
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        self.socket_client.sendall("bomb".encode())
        self.socket_client.send(pickle.dumps([self.nickname]))
        return True

    # time event

    def tick(self, dt):
        self.receive_model()
        return True
