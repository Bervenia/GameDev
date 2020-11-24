
import socket

import net_commen
import net_message
import net_connection
from collections import deque 
import asyncio as asio
#context is thread
class client_interface():
    def __init__(self):
        
        self.q_message_in = None
        
        self.socket = socket.socket()
        self.connection = None
        self.loop = asio.get_event_loop()#context
    def __enter__(self):
        

    async def connect(self,host,port):
        self.connection = net_connection.Connection()
        address = self.loop.getaddrinfo(host,port)
        self.connection.connect_to_server(address)

        return False

    def disconnect(self):
        if self.is_connected():
            self.connection.disconnect()
        self.loop.stop
        del self.connection
    
    def is_connected(self):
        if self.connection:
            return self.connection.is_connected()
        else:
            return False

    def __exit__(self):
        self.disconnect()