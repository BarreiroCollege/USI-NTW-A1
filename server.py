#!/usr/bin/python3

import argparse
import logging
import mimetypes
import os
import socket
import threading

from http.enums import HttpMethod, HttpResponseCode, HttpVersion
from http.header import HttpHeader, HEADER_CONTENT_TYPE, HEADER_CONTENT_TYPE_TEXT_PLAIN, HEADER_CONNECTION, \
    HEADER_CONNECTION_CLOSE, HEADER_CONTENT_LOCATION
from http.request import HttpRequest
from http.response import HttpResponse, HttpResponseError, HttpResponseMethodNotAllowed, HttpResponseNotFound, \
    HttpResponseUnsupportedMediaType, HttpResponseForbidden
from settings import DEFAULT_PORT, VHOSTS_FILE
from utils.entity import generate_output
from utils.mime import CUSTOM_MIMETYPES
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
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__socket.listen(1)
        logging.info("Server started on port {}".format(port))

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
        # Create an initial response, so at least there is one always
        response = HttpResponse()

        if request.get_method() == HttpMethod.GET:
            file_path = request.get_vhost().get_host_root_path().joinpath(request.get_path())
            # If user is requesting an existing path, try to access the index file
            if file_path.exists() and not file_path.is_file():
                file_path = file_path.joinpath(request.get_vhost().get_index_file())

            # If file does not exist, then 404
            if not file_path.exists():
                raise HttpResponseNotFound()
            # And if it is a folder, then 405
            elif not file_path.is_file():
                raise HttpResponseMethodNotAllowed()

            # Try to get file contents
            content = Vhost.get_file_contents(file_path)
            response = HttpResponse(content=content)

            # Try to guess the content type from the MIME type
            content_type = mimetypes.guess_type(file_path)[0]
            if content_type is None:
                # If no content type, check if it is one of the manually defined ones
                extension = file_path.suffix[1:]
                if extension not in CUSTOM_MIMETYPES:
                    # If still cannot find the content type, raise error 415
                    raise HttpResponseUnsupportedMediaType()
                content_type = CUSTOM_MIMETYPES[extension]

            # Add the Content-Type header
            content_type_header = HttpHeader(HEADER_CONTENT_TYPE, content_type)
            response.add_header(HEADER_CONTENT_TYPE, content_type_header)

        elif request.get_method() == HttpMethod.PUT:
            # It is not possible to PUT to a folder so, if it is one, just raise 405
            if request.get_path().endswith("/"):
                raise HttpResponseMethodNotAllowed()

            # Get the file to remove, and the parent one (create these folders recursively)
            file_path = request.get_vhost().get_host_root_path().joinpath(request.get_path())
            folder_path = file_path.parent

            try:
                # Create all folders up to the file
                os.makedirs(folder_path, exist_ok=True)
                # Open file and write contents to it
                Vhost.put_file_contents(file_path, request.get_body())
            except PermissionError:
                raise HttpResponseForbidden()

            # Use 201 as response code
            response = HttpResponse(status=HttpResponseCode.CREATED)

            # And specify where such file has been created
            content_location_header = HttpHeader(HEADER_CONTENT_LOCATION, request.get_path())
            response.add_header(HEADER_CONTENT_LOCATION, content_location_header)

        elif request.get_method() == HttpMethod.DELETE:
            # This method is strict, which means that it will only strictly delete the file if it exists
            file_path = request.get_vhost().get_host_root_path().joinpath(request.get_path())
            if not file_path.exists():
                raise HttpResponseNotFound(content="File not found")

            # If file is not a file, raise error 405 because it means it is a non-empty folder (as per the current
            # implementation, it is impossible that at this point empty folders exist)
            if not file_path.is_file():
                raise HttpResponseMethodNotAllowed()

            # Deletes the file and also the parent folders if they are empty
            Vhost.delete_file(file_path, request.get_vhost().get_host_root_path())

        elif request.get_method() == HttpMethod.NTW22INFO:
            # Specify the format of the output string
            ntw = "The administrator of {} is {}.\nYou can contact him at {}.".format(
                request.get_vhost().get_hostname(),
                request.get_vhost().get_server_admin_name(),
                request.get_vhost().get_server_admin_email()
            )

            # Create the response
            response = HttpResponse(content=ntw)

            # And use plain text as response content
            content_type_header = HttpHeader(HEADER_CONTENT_TYPE, HEADER_CONTENT_TYPE_TEXT_PLAIN)
            response.add_header(HEADER_CONTENT_TYPE, content_type_header)

        return response

    @staticmethod
    def __process_connection(conn, addr):
        logging.debug('Serving a connection from host {} on port {}'.format(addr[0], addr[1]))

        request, response = None, None
        try:
            # Try to parse the request basic request (if not possible, HttpResponseError will catch it)
            request = HttpRequest(conn.recv(1024))
            # Now try with headers and body (but if fails, at least request object will exist)
            request.parse_request(Server.__hosts)
            # And generate the response based on the request
            response = Server.__get_response(request)
        except HttpResponseError as e:
            response = e

        # Generate the output based on the request and the repsonse
        out = generate_output(request, response)
        # Encode it as bytes and send it
        conn.send(bytes(out))

        if request:
            # For HTTP/1.0, we always close the connection
            if request.get_http_version() == HttpVersion.HTTP_10:
                conn.close()
                return
            # For HTTP/1.1, if "Connection: close" header is present, we also close the connection
            if request.has_header(HEADER_CONNECTION) and request[HEADER_CONNECTION] == HEADER_CONNECTION_CLOSE:
                conn.close()
                return
        # Otherwise, we keep listening for connections
        Server.__process_connection(conn, addr)


if __name__ == "__main__":
    # Define logging format
    logging.basicConfig(format='%(asctime)s | %(message)s')
    # And output all logging messages
    logging.getLogger().setLevel(logging.DEBUG)

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="HTTP server based on TCP IPv4 with multithreading support.")
    # Accept a custom port number as argument
    parser.add_argument("-p", "--port",
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
