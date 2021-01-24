


import net_server
import asyncio


class custom_server(net_server.Server_Interface):
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
    server = custom_server(60000)
    asyncio.run(server._start_server())
    #server.start()
    while True:
        server.update()
        print(server.loop.is_running())
if __name__ == "__main__":
    main()