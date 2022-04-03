#!/usr/bin/python3

import argparse
import socket
import threading

from http.enums import HttpMethod
from http.request import HttpRequest
from http.response import HttpResponse, HttpResponseError
from settings import DEFAULT_PORT, HTTP_ENCODING, VHOSTS_FILE
from utils.entity import generate_output
from utils.vhosts import Vhost


class Server:
    __socket = None
    __hosts = None

    def __init__(self, port=DEFAULT_PORT):
        # Parse vhosts.conf file
        Server.__hosts = Vhost.parse_file(VHOSTS_FILE)
        # Initialize the socket to work with IPv4 TCP
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Using the specified port
        self.__socket.bind(('', port))
        self.__socket.listen(1)
        print("Server started on port", port)

    def listen(self):
        if self.__socket is None:
            # Cannot listen if socket is None (probably because it was closed)
            raise Exception("Socket is not available!")

        while True:
            # We listen to connections forever and, for each connection, launch a thread
            conn, addr = self.__socket.accept()
            thread = threading.Thread(target=Server.__process_connection, args=(conn, addr))
            thread.start()

    def close(self):
        # Close and remove the socket
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
            # Try to parse the request (if not possible, HttpResponseError will catch it)
            request = HttpRequest(conn.recv(1024), Server.__hosts)
            # And generate the response based on the request
            response = Server.__get_response(request)
        except HttpResponseError as e:
            response = e

        # Generate the output based on the request and the repsonse
        out = generate_output(request, response)
        # Encode it as bytes and send it
        conn.send(out.encode(HTTP_ENCODING))
        # TODO: For HTTP/1.1, if no Connection header is present or not equal to "Connection: close" (case
        #  insensitive), this connection can NOT be closed and be open until header "Connection: close" is
        #  received.
        conn.close()


if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="HTTP server based on TCP IPv4 with multithreading support.")
    # Accept a custom port number as argument
    parser.add_argument("--port",
                        help="port to use to listen connections",
                        type=int,
                        nargs='?',
                        const=DEFAULT_PORT,
                        default=DEFAULT_PORT)
    args = parser.parse_args()

    # Create the server in the specified port (8080 by default) and start listening for connections
    server = Server(port=args.port)
    server.listen()
    # Close the server after finishing
    server.close()
