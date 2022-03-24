#!/usr/bin/python3

import argparse
import socket
import threading


DEFAULT_PORT = 8080


class Server:
    __socket = None

    def __init__(self, port=DEFAULT_PORT):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(('', port))
        self.__socket.listen(1)

    def listen(self):
        if self.__socket is None:
            raise Exception("Socket is not defined!")

        while True:
            conn, addr = self.__socket.accept()
            threading.Thread(target=self.process_connection, args=(conn, addr)).start()

    def close(self):
        self.__socket.close()
        self.__socket = None

    def process_connection(self, conn, addr):
        print('Serving a connection from host', addr[0], 'on port', addr[1])
        request = conn.recv(1024)   # reading data (a request) from the connection
        if not request:
            print("empty message: bailing out!")
            return
        if request.decode('utf-8') == 'shutdown':
            print("shutdown request: bailing out!")
            return
        print(request.decode('utf-8'))
        reply = """HTTP/1.0 200 OK
Date: Wed, 21 Mar 2022 09:30:00 GMT
Server: Group ABC Server
Content-Length: 98
Content-Type: text/plain

The administrator of guyincognito.ch is Guy Incognito.
You can contact him at guy.incognito@usi.ch.
"""
        conn.send(reply.encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port",
                        help="port to use to listen connections",
                        type=int,
                        nargs='?',
                        const=1,
                        default=DEFAULT_PORT)
    args = parser.parse_args()

    server = Server()
    server.listen()
    server.close()
