
import socket
import asyncio 
import threading
from collections import deque 

import net_message
from net_connection import Connection




class Client_Interface():
    def __init__(self):
        self._q_message_in = deque()
        self.context = asyncio.get_event_loop()#async loop -> context for thread
        self.connection = None #created on connect
        self.threadcontext = threading.Thread(target=self.context.run_forever)

        #maybe associate socket with loop

    async def connect(self,host,port):
        """Connect to server with hostname/ip address and port.
        returns true if successful.

        Args:
        host (string): A standard IPv4 address
        port (int): A standard port number (1-65535)
        """
        #try:
        print("g")
        
        reader, writer = await asyncio.open_connection(sock = self.socket, loop = self.context)
        address = await loop.getaddrinfo(host,port)
        #self.connection = Connection(Connection.owner.client,reader,writer,self.q_message_in,self.loop)
        self.connection.connect_to_server(address)
        self.threadcontext.start()
        #except:
         #   print("what")
          #  return False
        return True
    def connect(self,host,port):
        """Connect to server with hostname/ip address and port.
        returns true if successful.

        Args:
        host (string): A standard IPv4 address
        port (int): A standard port number (1-65535)
        """
        #try:
        print("g")
        
        socket = self.context.run_until_complete(asyncio.open_connection(host,port, loop = self.context))
        
        self.connection = Connection(Connection.owner.client,self.context, socket,self._q_message_in)
        self.connection.connect_to_server((host,port))
        self.threadcontext.start()
        #except:
         #   print("what")
          #  return False
        return True
    def disconnect(self):
        if self.is_connected():
            self.connection.disconnect()
        self.context.stop
        del self.connection
    def is_connected(self):
        if self.connection:
            return self.connection.is_connected()
        else:
            return False

    def __del__(self):
        """if client is deleted/garbaged collected,
        always try to disconnect from server.
        """
        self.disconnect()