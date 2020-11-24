import socket
import asyncio 

import net_commen
import net_message
import net_connection
from collections import deque 


class Server_Interface():
    def __init__(self,port):
        self.port = port
        self.loop = asyncio.get_event_loop()#context/thread
        #self.server = sloop.create_server()
        #self.loop.sock_accept(self.socket)
        self.q_message_in = deque()
        self.id_counter = 10000
        self.connections = []

    def start(self):
        #self.server = asyncio.start_server(self.on_client_connect,"127.0.0.1",self.port,loop = self.loop)
        self.server = socket.create_server(("127.0.0.1",self.port))
        print("[SERVER] Started")
        self.loop.run_until_complete(self.wait_for_connection())

    async def wait_for_connection(self):
        #print(self.server)
        try:
            conn ,address = await self.loop.sock_accept(self.server)
            print("[SERVER] New Connection", address)
            #new_conn = net_connection.Connection("server",conn,self.q_message_in)
            #chance to deny connection
            if on_client_connect(new_conn):
                #add to list of connections
                self.connections.append(new_conn)
                self.connections[-1].connect_to_client(self.id_counter)
                self.id_counter += 1
                print(conn,address,"connection has been approved")
            else:
                print(conn,address,"connection denied")
            
        except:
            print("[SERVER] New Connection Failed")
        
        self.loop.create_task(self.wait_for_connection())
    
    def update(self, max_messages = -1):
        message_count = 0
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
        print("hi")
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
