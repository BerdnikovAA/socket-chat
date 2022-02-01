import socket

class Socket(socket.socket):
    def __init__(self):
        super(socket.socket, self).__init__(family=socket.AF_INET, type=socket.SOCK_STREAM)
        super(Socket, self).__init__()