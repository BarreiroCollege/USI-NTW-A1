#!/usr/bin/python3

# argparse is a native Python package used to parse command line arguments easily
import argparse
# socket is a native Python package used to open socket connections
import socket
# threading is a native Python package used to run multi-threading scripts
import threading


# We define the default port where the server will be running
DEFAULT_PORT = 8080


# For an easier workflow, we define a "server" class, where all the code will be running
class Server:
    # This server class has an attribute for the socket, so we can detect if, for any reason, the socket is
    # no longer available
    __socket = None

    def __init__(self, port=DEFAULT_PORT):
        # When we create a new server instance, we create the socket with AF_INET (IPv4) and SOCK_STREAM (TCP)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We bind the socket to the current host ('' to not specify any, or wildcard) and the specified port
        self.__socket.bind(('', port))
        # And we open the socket to start listening for connections
        self.__socket.listen(1)
        print("Server started on port", port)

    def listen(self):
        # With this method, we start listening for connections. First we make sure the socket is still up and
        # available
        if self.__socket is None:
            raise Exception("Socket is not available!")

        # And now we make the "infinite" loop so we can listen to an unlimited number of requests. If we did
        # not specify the infinite loop, we could only listen to one request, and then it would die.
        while True:
            print("Server waiting to accept connection")
            # Here we are waiting for a "client socket" to connect and send a message
            conn, addr = self.__socket.accept()
            # Once reached here, a client has requested a connection. But instead of processing it here, we just
            # open a new thread to process it, so we can accept new connections while we process the other one
            # thanks to pseudo-parallelism.
            # To process in a thread, we create a new thread, we call the function in this class to process a
            # request, and we send both the connection and address parameters.
            thread = threading.Thread(target=Server.__process_connection, args=(conn, addr))
            # And we start the thread, so the Server class can go back and accept new connections while this new
            # thread processes this request.
            thread.start()

    def close(self):
        # We define a closing method to close the socket and unset it after we finish everything.
        self.__socket.close()
        self.__socket = None

    @staticmethod
    def __process_connection(conn, addr):
        # If we reach this piece of code, it is because it was invoked by a thread which was previously created
        # because a client requested a connection, and the Server class accepted it.
        print('Serving a connection from host', addr[0], 'on port', addr[1])
        # We get the request contents
        request = conn.recv(1024)
        if not request:
            print("Empty message: discarding request!")
            return
        # And we decode these contents from bytes to string
        print(request.decode('utf-8'))
        # Now we define a valid sample HTTP response
        reply = """HTTP/1.0 200 OK
Date: Wed, 21 Mar 2022 09:30:00 GMT
Server: Group ABC Server
Content-Length: 98
Content-Type: text/plain

The administrator of guyincognito.ch is Guy Incognito.
You can contact him at guy.incognito@usi.ch.
"""
        # And we send it back encoded from string to bytes
        conn.send(reply.encode('utf-8'))
        # And we finally close the client connection (but NOT the server one, as it is in the server socket)
        conn.close()


# We make sure we only run this code and open the server if this code is run directly from a script (and not
# imported from a module)
if __name__ == "__main__":
    # We define an argument parser, so we add a description for this script to make it fancy with the help
    # argument
    parser = argparse.ArgumentParser(
        description="Sample TCP IPv4 server with multithreading support.")
    # We now define the only parameter, the port
    parser.add_argument("--port",
                        help="port to use to listen connections",
                        # We indicate we only want numbers
                        type=int,
                        # This means that we either accept 0 or 1 arguments with port
                        nargs='?',
                        # In case of 0 arguments with port are specified, we fallback to default one
                        const=DEFAULT_PORT,
                        # And if the port argument is missing, by default it is going to run on the default one
                        default=DEFAULT_PORT)
    # And we parse the arguments
    args = parser.parse_args()

    # We create the server
    server = Server()
    # Start listening for connections
    server.listen()
    # And finally close it
    server.close()
