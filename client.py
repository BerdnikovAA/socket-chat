import asyncio
import socket

class Client(socket.socket):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    def connect_server(self):
        self.client_socket.connect(('localhost', 50001))
        self.client_socket.setblocking(False)

    async def _send_message(self):
        while True:
            message = await self.loop.run_in_executor(None, input)
            await self.loop.sock_sendall(self.client_socket, message.encode('utf-8'))

    async def _get_messages(self):
        while True:
            bufsiz = 2048
            data = await self.loop.sock_recv(self.client_socket, bufsiz)
            print(data.decode('utf-8'))

    async def _async_run(self):
        await asyncio.gather(
            self.loop.create_task(self._send_message()),
            self.loop.create_task(self._get_messages())
        )

    def start_chatting(self):
        self.loop.run_until_complete(self._async_run())

if __name__ == '__main__':
    client = Client()
    client.connect_server()
    client.start_chatting()
