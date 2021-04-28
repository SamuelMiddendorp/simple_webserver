#!/usr/bin/python
import socket
from threading import Thread
import sys
import time
import os
import webbrowser
def main():
    # Check if a system argument is provided
    if(len(sys.argv) > 1):
        # When "." is entered we serve the current directory in powershell
        if(sys.argv[1] == "."):
            server = SimpleWebserver("0.0.0.0", 8000, os.getcwd())
        else:
            server = SimpleWebserver("0.0.0.0", 8000, sys.argv[1])
    else:
        server = SimpleWebserver("0.0.0.0", 8000)
    server.launch()
# A simple webserver build on sockets
class SimpleWebserver:
    def __init__(self, adress: str, port: int, folder_to_serve = ""):
        self.MAX_REQUESTSIZE = 2024
        self.RESPONCE_CODES = {200: 'HTTP/1.1 200 OK\r\n', 404: 'HTTP/1.1 404 Not Found\r\n'}
        self.RESPONCE_TYPES = {"html": "Content-Type: text/html; charset=utf-8\r\n", "jpg": "Content-Type: image/jpeg\r\n", "css": "Content-Type: text/css\r\n"}
        # Save adress and port for loggin purposes
        self.adress = adress
        self.port = port
        self.folder_to_serve = folder_to_serve
        # Configuring the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((adress, port))
        print("Server initialised on %s" % socket.gethostbyname(socket.gethostname()))
        # Set timeout in order to be able to handle keyboardinterrupts
        self.server_socket.settimeout(0.5)
    def launch(self):
        webbrowser.open("http://localhost:8000", new=2)
        self.server_socket.listen(1)
        self._listen()
    def _read_file(self, src: str) -> str:
        print(src)
        try:
            default_path = "index.html"
            new_src = src
            if(self.folder_to_serve != ""):
                new_src = self.folder_to_serve + "\\" + src
                default_path = self.folder_to_serve + "\\" + default_path
            if(src == "" or src == "/"):
                with open (default_path, "rb") as f:
                    return f.read()
            if("." not in src):
                new_src +=  ".html"
            with open (new_src, "rb") as f:
                return f.read()
        except FileNotFoundError:
            print("Not able to read file %s" % src)
            return "<h1>404 file not found</h1>".encode()
    def _format_get_request(self, request: str) -> dict:
        request_dict = dict()
        # Split up request into usable parts.
        for entry in request.split("\r\n"):
            if(entry == ""):
                continue
            if("HTTP" in entry):
                request_dict["Http-Protocol"] = entry.split(" ")[0]
                request_dict["Path"] = entry.split(" ")[1][1:]
                request_dict["Http-Version"] = entry.split(" ")[2]
                continue
            key_value = entry.split(": ")
            request_dict[key_value[0]] = key_value[1]
        return request_dict
    def _generate_response(self, r_code: int, r_type:str, content: bytes) -> bytes:
        try:
            return (self.RESPONCE_CODES[r_code] + self.RESPONCE_TYPES[r_type]).encode() + "\r\n".encode() + content + "\r\n\r\n".encode()
        except:
            raise Exception("Http-code is not implemented yet")
    def _listen(self):
        print("Starting listening on %s and port: %i" % (self.adress, self.port))
        # encapsulating try catch block for windows.
        try:
            while True:
                try:
                    c = None
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
        
        initial_request = c.recv(self.MAX_REQUESTSIZE).decode()
        if(initial_request is ""):
            print("Client disconnected")
            c.close()
            return
        request = self._format_get_request(initial_request)
        print("Handling request %s for resource %s" % (str(c_adress), request["Path"]))
        try:
            file_content_bytes = self._read_file(request["Path"])
        except:
            print(initial_request)
        response_type = "html"
        if(".jpg" in request["Path"]):
            response_type = "jpg"
        if(".css" in request["Path"]):
            response_type = "css"
        c.send(self._generate_response(200, response_type, file_content_bytes))
        c.close()
        return
if __name__ == '__main__':
    main()