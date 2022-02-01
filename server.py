import socket
import asyncio

class Server(socket.socket):

    def __init__(self):
        super().__init__()
        self.users = []
        self.loop = asyncio.new_event_loop()
        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    def set_up_server(self):
        self.server_socket.bind(('localhost', 50001))
        self.server_socket.setblocking(False)
        self.server_socket.listen()

    async def _accept_clients(self):
        while True:
            user_conn, user_address = await self.loop.sock_accept(self.server_socket)
            print('New user connected!')
            self.users.append(user_conn)

            self.loop.create_task(self._get_message(user_conn, user_address))

    async def _get_message(self, user_conn, user_address):
        while True:
            bufsiz = 2048
            data = await self.loop.sock_recv(user_conn, bufsiz)
            message = 'User-[{}]: {}'.format(user_address, data.decode('utf-8'))
            await self._send_message(message)
            #self.loop.create_task(self._send_message(message))

    async def _send_message(self, message):
        for user in self.users:
            await self.loop.sock_sendall(user, message.encode('utf-8'))

    async def _async_run(self):
        print('Server is running!')
        await self.loop.create_task(self._accept_clients())

    def start_server(self):
        self.loop.run_until_complete(self._async_run())

if __name__ == '__main__':
    server = Server()
    server.set_up_server()
    server.start_server()
