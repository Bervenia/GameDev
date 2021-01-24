
import asyncio 
import threading
from collections import deque 

import net_message
from net_connection import Connection

class Server_Interface():
    def __init__(self,port):
        self.port = port
        self.q_message_in = deque()
        self.connections = deque()
        self.id_counter = 10000
        self.context = asyncio.get_event_loop()#async loop -> context for thread
        self.threadcontext = threading.Thread(target=self.context.run_forever)
        self.server = asyncio.start_server(self.wait_for_connection,"127.0.0.1",
                                           port, loop = self.context)
        
        
    def __del__(self):
        print("garbage truck")
        self.stop()
        
 
    def start(self):
        try:
            self.server = self.context.run_until_complete(self.server)
            #self.context.create_task(self.server)
            self.threadcontext.start()    
        except Exception as e:
            print('[SERVER] Exception]',e)
            return False
        
        print('[SERVER] Started')
        
        #self.context.run_forever()
        return True

    def stop(self):
        self.context.stop()
        if self.threadcontext.is_alive():
            self.threadcontext.join() 
        print('[SERVER] Stopped')

    async def wait_for_connection(self,reader,writer):
        """Server callback for handling client connections.

        Args:
            reader (asyncio.StreamReader): Associated with connecting client to read data from IO stream
            writer (asyncio.StreamWriter): Associated with connecting client to write data to IO stream
        """
        #print("hi")
        #try:
        address = writer.get_extra_info('peername')
        print("[SERVER] New Connection", address)
        new_conn = Connection(Connection.owner.server,self.context,(reader,writer),self.q_message_in)
        
        if self.on_client_connect(new_conn):#chance to deny
            new_conn.connect_to_client(self.id_counter)
            self.id_counter += 1
            self.connections.append(new_conn)#add to list of connections 
            print(f'[{new_conn.id}] Connection Accepted')
        else:
            print('[SERVER] Connection Denied' )

       # except Exception as e:
        #    print('[SERVER] Exception]',e)
            
        

        #create more work for asycnio loop
        

    def message_client(client,message):
        """Send a message to a given connected client.

        Args:
            client (net_Connection.Connection): target client to send message to 
            message (net_message.Message): desired message to sent to client
        """
        if client and client.is_connected():
            client.send(message)
        else:
            self.on_client_disconnect(client)
            self.connections.remove(client)

    def message_all_clients(message,ignore_client = None):
        """Send a message to all connected clients with the option
        to ignore a client

        Args:
            message (net_message.Message): desired message to sent to client
            ignore_client (net_Connection.Connection, optional): ignore this client. Defaults to None.
        """
        invalid_client_exists = False
        for index, client in enumerate(self.connections):
            if client and client.is_connected():
                if client != ignore_client:
                    client.send(message)
            else:
                self.on_client_disconnect(client)
                self.connections[index] = None
                invalid_client_exists = True

        if invalid_client_exists:
            self.collections = deque(set(self.connections))#remove all duplicates/dead connections
            self.connections.remove(None)
    def update(self,max_messages = 1000):
        message_count = 0 
        while message_count < max_messages and len(self.q_message_in) != 0 :
            msg = self.q_message_in.popleft()

            self.on_message(msg.remote,msg.msg)
            message_count += 1

        
    def on_client_connect(self,client):
        return False

    def on_client_disconnect(self,client):
        pass

    def on_message(self,client,message):
        pass 

if __name__ == "__main__":
    server = Server_Interface(60000)
    server.start()