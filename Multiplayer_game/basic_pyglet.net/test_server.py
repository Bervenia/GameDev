


import net_server

class custom_server(net_server.Server_Interface):
    def __init__(self,port):
        super().__init__(port)
    def on_client_connection(client):
        return True

    def on_client_disconnect(self,client):
        pass

    def on_message(self,client,message):
        pass 

def main():
    server = custom_server(60000)
    server.start()
    while True:
        server.update()
if __name__ == "__main__":
    main()