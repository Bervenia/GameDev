import net_commen
import struct
from collections import deque 

import struct

class Message():
    def __init__(self, *args, encoding = "utf-8", msg_type = None):
        self.encoding = encoding
        self.message_type = msg_type
        self.message_list = deque()
        self.add(*args)
        self.id = None
        
    def get_format(self, *args):
        """Generate the appropriate c type formating string
        for value in *args. *args can only be comprised of 
        strings, bools, integers, and floats. 
        """
        fmt = ""
        for val in args:
            assert type(val) in [bytes,bool,int,float], f"Data type {type(val)} to complex to pack!"
            if type(val) == bytes:
                fmt += f"{len(val)}s"
            elif type(val) == bool:
                fmt += "?"
            elif type(val) == float:
                fmt  += "d" #default to 'double' for general use cases
            elif type(val) == int:            
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
                fmt+= int_type[look_up]
        return fmt

    def add(self,*args):
        for val in args:
            if type(val) == str:
                val = val.encode(self.encoding)
            self.message_list.append(val)

    def remove(self,index = -1):
        val = self.message_list.pop(index)
        if type(val) == bytes:
                val = val.decode(self.encoding)
        return val

    def header(self):
        fmt = self.get_format(*self.message_list)
        return f"bs" + fmt #add b#s to fmt string to acount for adding fmt string to body

    def body(self):
        format_header = self.get_format(*self.message_list).encode("utf-8")
        return (len(format_header), format_header, *self.message_list)

    def clear(self):
        self.message_list = []

    def size(self):
        return len(self.message_list)


if __name__ == "__main__":
    value = ("hello world",True,12,False)
    test = Message(*value)
    print(test.message_list)
    print(test.remove())
    print(test.message_list)
    print(test.header())
    print(test.body())
    