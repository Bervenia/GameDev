

import enum


import net_client
import net_message
import asyncio
class custom_msg(enum.Enum):
    ServerAccept = 0 
    ServerDeny = 1
    ServerPing = 2
    MessageAll = 3
    ServerMessage = 4


class Custom_Client(net_client.Client_Interface):

    def ping_server(self):
        msg = net_message.Message("Hello")
        msg.id = custom_msg.ServerPing
        self.connection.send(msg)



if __name__ == "__main__":

    c = Custom_Client()
    
    asyncio.run(c.connect('127.0.0.1',60000))
    c.ping_server()
    c.loop.run_forever()
