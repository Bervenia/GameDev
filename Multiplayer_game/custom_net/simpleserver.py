
import enum
import net_server

ADDRESS = "127.0.0.1"
PORT = 60000

class Custom_Message(enum.Enum):
    Server_Accept = 0,
    Server_Deny = 1,
    Server_Ping = 2,
    Message_All = 3,
    Server_Message =4 

class Custom_Server(net_server.Server_Interface):
    def __init__(self,port):
        super().__init__(port)

    def on_client_connect(self,client):
        print("connection")
        return True

    def on_client_disconnect(self,client):
        pass

    def on_message(self,client,message):
        if message.id == custom_msg.ServerPing:
            print("i did it")



def main():
    server = Custom_Server(PORT)
    server.start()
    
    #server.start()
    while True:
        server.update()
        #print(server.context.is_running())
        #print(server.server.is_serving())
        

if __name__ == "__main__":
    main()