
import socket

import net_commen
import net_message
from net_connection import Connection
from collections import deque 
import asyncio 
import socket
#context is thread
class Client_Interface():
    def __init__(self):
        
        self.q_message_in = deque()
        self.connection = None
        self.loop = asyncio.get_event_loop()#context
        
        

        

    async def connect(self,host,port):
        #try:
        print("g")
        address = socket.getaddrinfo(host,port)
        reader, writer = await asyncio.open_connection(host, port)
        
        self.connection = Connection(Connection.owner.client,reader,writer,self.q_message_in,self.loop)
        self.connection.connect_to_server(address)
        #except:
         #   print("what")
          #  return False
        return True

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