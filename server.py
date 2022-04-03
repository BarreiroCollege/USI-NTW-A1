#!/usr/bin/python3

import argparse
import socket
import threading

from http.enums import HttpMethod
from http.request import HttpRequest
from http.response import HttpResponse, HttpResponseError
from settings import DEFAULT_PORT, HTTP_ENCODING
from utils.entity import generate_output


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
        response = HttpResponse()
        if request.get_method() == HttpMethod.GET:
            # TODO
            pass
        elif request.get_method() == HttpMethod.PUT:
            # TODO
            pass
        elif request.get_method() == HttpMethod.DELETE:
            # TODO
            pass
        elif request.get_method() == HttpMethod.NTW22INFO:
            # TODO
            pass
        return response

    @staticmethod
    def __process_connection(conn, addr):
        print('Serving a connection from host {} on port {}'.format(addr[0], addr[1]))

        request, response = None, None
        try:
            request = HttpRequest(conn.recv(1024))
            response = Server.__get_response(request)
        except HttpResponseError as e:
            response = e

        out = generate_output(request, response)
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
