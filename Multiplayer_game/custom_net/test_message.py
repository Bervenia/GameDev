
from enum import Enum

from net_message import Message

class Custom_Message_Types(Enum):
    Fire_bullet = 0
    Move_player = 1

def main():
    msg = Message()
    msg.header.id = Custom_Message_Types.Fire_bullet
    a = 1 
    b = True
    c = 3.14
    d = "cool"
    msg.add(a,b,c,d)
    
    a = 32
    b = "hello"
    c = None
    d,c,b,a = msg.remove(4)
    print(a,b,c,d)
if __name__ == "__main__":
    main()


