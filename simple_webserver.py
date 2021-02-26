import socket
from threading import Thread
import sys
import time
# A simple webserver build on sockets
class SimpleWebserver:
    def __init__(self, adress: str, port: int):
        self.MAX_REQUESTSIZE = 2024
        self.RESPONCE_CODES = {200: 'HTTP/1.1 200 OK\r\n', 404: 'HTTP/1.1 404 Not Found\r\n'}
        self.RESPONCE_TYPES = {"html": "Content-Type: text/html; charset=utf-8\r\n"}
        # Save adress and port for loggin purposes
        self.adress = adress
        self.port = port
        # Configuring the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((adress, port))
        # Set timeout in order to be able to handle keyboardinterrupts
        self.server_socket.settimeout(0.5)
    def launch(self):
        self.server_socket.listen(1)
        self._listen()
    def _generate_response(self, r_code: int, r_type:str, content: str):
        try:
            return (self.RESPONCE_CODES[r_code] + self.RESPONCE_TYPES[r_type] + "\r\n" + content + "\r\n\r\n").encode()
        except:
            raise Exception("Http-code is not implemented yet")
    def _listen(self):
        print("Starting listening on %s and port: %i" % (self.adress, self.port))

        try:
            while True:
                try:
                    c = None;
                    # Accept connection from client
                    c, c_adress = self.server_socket.accept()
                    # Creates a thread for each individual client  
                    client_thread = Thread(target=self._handle_client, args=(c,c_adress))
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            #check if there is an active connection
            if(c):
                c.close()
            #cleanup socket
            self.server_socket.close()
            print("Server closed")
            return 1
    def _handle_client(self, c, c_adress):
        print("Handling request " + str(c_adress))
        request = c.recv(self.MAX_REQUESTSIZE).decode()
        c.send(self._generate_response(200, "html", "<h1>Hallo daar</h1>"))       
        c.close()
        


        

                
