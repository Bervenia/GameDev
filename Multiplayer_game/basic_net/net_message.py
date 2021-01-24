
import net_commen
import struct
from collections import deque 

import struct

class Message_Header():
    def __init__(self):
        self.id = None
        self.format = ""
        self.size = 0

    
class Message():
    def __init__(self, *args, encoding = "utf-8"):
        self.encoding = encoding
        self.header = Message_Header()
        self.dequeue = deque()#thread safe queue
        self.body = b""

        """
        self.message_type = msg_type
        self.message_list = []
        self.add(*args)
        self.id = None
        """
    def size(self):
        pass

    def format(self, val):
        """Generate the appropriate c type formating string
        for value in *args. *args can only be comprised of 
        strings, bools, integers, and floats. 
        """
        
        val_type = type(val)
        assert val_type in [bytes,bool,int,float], f"Data type {val_type} to complex to pack!"
        if val_type == bytes:
            fmt = f"{len(val)}s"
        elif val_type == bool:
            fmt = "?"
        elif val_type == float:
            fmt = "d" #default to 'double' for general use cases
        elif val_type == int:            
            int_type = {"signed 1": "b","signed 2":"h","signed 4":"i","signed 8":"q",
                        "unsigned 1": "B","unsigned 2":"H","unsigned 4":"I","unsigned 8":"Q"}
            unsigned_max = 128
            bits = 1
            if val < 0:
                val = ~val
                fmt_char = 'signed '
                while unsigned_max <= val:
                    val >>=8
                    bits +=1
            else:
                fmt_char = 'unsigned '
                bits = (val.bit_length() + 7) // 8#get number of bytes required
            look_up = fmt_char + str((1 if bits == 0 else 2**(bits - 1).bit_length()))#closest power of 2
            fmt = int_type[look_up]
        return fmt

    def add(self,*args):
        for val in args:
            if type(val) == str:
                val = val.encode(self.encoding)
            self.header.format += self.format(val)
            self.dequeue.append(val)
            
    def remove(self,amount=1):
        values = []
        for i in range(amount):
            val = self.dequeue.pop()
            self.header.format = self.header.format[0:]
            if type(val) == bytes:
                    val = val.decode(self.encoding)
            values.append(val)
        return values

    def clear(self):
        self.message_list = []

    class Owned_Message():
        def __init__(self,*args):
            self.remote = None # connection class 
            self.msg = Message(*args)
        