



import asyncio
import time

class EchoServerProtocol(asyncio.Protocol):
    
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
      

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 60000)

    async with server:
        print(server.sockets)
        await server.serve_forever()
        print(server.sockets)
    
#asyncio.run(main())

lambda self.write_header() : if len(len(self.q_message_out) == 0 )
asyncio.create_task(lambda len(self.q_message_out) == 0 : self.write_header)