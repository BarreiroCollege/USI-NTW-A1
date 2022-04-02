#!/usr/bin/python3

import argparse
import socket
import threading


# Server Constants
from http.enums import HttpVersion
from http.request import HttpRequest
from http.response import HttpResponse, HttpResponseError
from settings import DEFAULT_PORT, HTTP_ENCODING


class Server:
    __socket = None

    def __init__(self, port=DEFAULT_PORT):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(('', port))
        self.__socket.listen(1)
        print("Server started on port", port)

    def listen(self):
        if self.__socket is None:
            raise Exception("Socket is not available!")

        while True:
            conn, addr = self.__socket.accept()
            thread = threading.Thread(target=Server.__process_connection, args=(conn, addr))
            thread.start()

    def close(self):
        self.__socket.close()
        self.__socket = None

    @staticmethod
    def __get_response(request: HttpRequest) -> HttpResponse:
        return HttpResponse()

    @staticmethod
    def __process_connection(conn, addr):
        print('Serving a connection from host {} on port {}'.format(addr[0], addr[1]))

        request, response = None, None
        try:
            request = HttpRequest(conn.recv(1024))
            response = Server.__get_response(request)
        except HttpResponseError as e:
            response = e

        out = "{} {}\r\n{}\r\n".format(
            HttpVersion.HTTP_10 if not request else request.get_http_version(), response.get_status_code(),
            response.serialize())
        conn.send(out.encode(HTTP_ENCODING))
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HTTP server based on TCP IPv4 with multithreading support.")
    parser.add_argument("--port",
                        help="port to use to listen connections",
                        type=int,
                        nargs='?',
                        const=DEFAULT_PORT,
                        default=DEFAULT_PORT)
    args = parser.parse_args()

    server = Server()
    server.listen()
    server.close()
