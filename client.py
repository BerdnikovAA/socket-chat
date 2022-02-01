from Socket import Socket
from threading import Thread

class Client(Socket):
    def __init__(self):
        super().__init__()

    def _connect_server(self):
        self.connect(('localhost', 12345))

    def _send_message(self):
        while True:
            self.send(input().encode('utf-8'))

    def _get_messages(self):
        while True:
            check_data = True
            bufsiz = 10
            byte_string = b''
            while check_data:
                data = self.recv(bufsiz)
                byte_string += data
                if len(data) < bufsiz:
                    check_data = False
            print(byte_string.decode('utf-8'))

    def start_chating(self):
        self._connect_server()
        send_mes_thread = Thread(target=self._send_message)
        send_mes_thread.start()

        get_mes_thread = Thread(target=self._get_messages)
        get_mes_thread.start()

if __name__ == '__main__':
    client = Client()
    client.start_chating()

