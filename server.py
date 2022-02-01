from threading import Thread
from Socket import Socket

class Server(Socket):
    users = []

    def __init__(self):
        super().__init__()
        self._server_address = ('localhost', 12345)

    def _set_up(self):
        self.bind(self._server_address)
        self.listen()

    def _accept_clients(self):
        while True:
            user_conn, user_address = self.accept()
            print('New user connected!')
            self.users.append(user_conn)
            get_mes_thread = Thread(target=self._get_message, args=(user_conn, user_address,))
            get_mes_thread.start()


    def _get_message(self, user_conn, user_address):
        while True:
            check_data = True
            bufsiz = 10
            byte_string = b''
            while check_data:
                data = user_conn.recv(bufsiz)
                byte_string += data
                if len(data) < bufsiz:
                    check_data = False
            message = 'User: {}: {}'.format(user_address, byte_string.decode('utf-8'))
            self._send_message(message)

    def _send_message(self, message):
        for user in self.users:
            user.send(message.encode('utf-8'))

    def start_server(self):
        print('Server is running!')
        self._set_up()
        self._accept_clients()

if __name__ == '__main__':
    server = Server()
    server.start_server()