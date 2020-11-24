
import enum

import net_message
import net_commen
from collections import deque 

class Connection():
    class owner(enum):
        server = 0
        client = 1
    def __init__(self,owner,socket,q_message_in):
        self.ownertype = owner
        self.socket = None
        self.q_message_in = q_message_in#pass a queue

        self.id = 0
        
        self.q_message_out = deque()
    def connect_to_client(user_id):
        if self.ownertype == owner.server:
            if self.socket:#may need to check connection?

    def connect_to_server(self,address):
        pass
    def disconnect(self):
        pass
    def is_connected(self):
        pass
    def send(self,message):
        pass