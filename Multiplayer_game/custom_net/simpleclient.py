
import net_client
from enum import Enum
from net_message import Message

class Custom_Message_Types(Enum):
    Server_Accept = 0,
    Server_Deny = 1,
    Server_Ping = 2,
    Message_All = 3,
    Server_Message = 4  

class Custom_Client(net_client.Client_Interface):
    def __init__(self):
        super().__init__()

    
def main():
    msg = Message()
    client = Custom_Client()
    client.connect("127.0.0.1",60000)
if __name__ == "__main__":
    main()


