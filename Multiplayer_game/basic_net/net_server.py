import socket
import asyncio 

import net_commen
import net_message
from net_connection import Connection
from collections import deque 
import threading


class Server_Interface():
    def __init__(self,port):
        self.port = port
        self.loop = asyncio.new_event_loop()#context/thread
        
        self.q_message_in = deque()
        self.id_counter = 10000
        self.connections = []
        

    async def _start_server(self):
        self.server = await asyncio.start_server(self.wait_for_connection,"127.0.0.1",self.port)
        print("[SERVER] Started")
        async with self.server:
            await self.server.serve_forever()
        

    async def wait_for_connection(self,reader,writer):
        #try:
        print("Waiting")
        #conn ,address = await self.loop.sock_accept(self.server)
        conn = writer
            
        print(conn.get_extra_info("socket"))
        address = conn.get_extra_info('peername')
        print("[SERVER] New Connection", address)
        new_conn = Connection(Connection.owner.server,reader,writer,self.q_message_in,self.loop)
        #chance to deny connection
        if self.on_client_connect(new_conn):
            #add to list of connections
            self.connections.append(new_conn)
            self.connections[-1].connect_to_client(self.id_counter)
            self.id_counter += 1
            print(self.connections[-1].id,address,"connection has been approved")
        else:
            print(address,"connection denied")
       # except:
        #    print("[SERVER] New Connection Failed")
        
        print("my sockets",self.server.sockets)
        print('my connections',self.connections)
        
    
    def update(self, max_messages = -1):
        message_count = 0
       # print(self.connections)
        while message_count < max_messages and len(self.q_message_in) != 0:
            message = self.q_message_in.popleft()
            self.on_message(msg.remote, msg.msg)
            message_count +=1


    def message_client(client,message):
        if client and client.is_connected():
            client.send(message)
        else:
            self.on_client_disconnect(client)
            self.connections.remove(client)

    def message_all_clients(message,ignore_client = None):
        invalid_client_exists = False
        for i in range(len(self.connections)):
            if self.connections[i] != ignore_client:
                self.connections[i].send(message)
            else:
                self.on_client_disconnect(self.connections[i])
                invalid_client_exists = True
                self.connections[i] = None
        if invalid_client_exists:
            self.connections.remove(None)#remove disconnects at the end


    def on_client_connect(self,client):
        return False
    def on_client_disconnect(self,client):
        pass

    def on_message(self,client,message):
        pass 

    def stop(self):
        self.loop.stop()
        print("server stoped")

    

    def __exit__(self):
        self.stop()
