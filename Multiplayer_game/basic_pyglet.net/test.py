
import struct
class message():
    def __init__(self):
        self.message_list = []

    def pack(self,fmt,*args):
        var_sizes = ["s","p"]
        self.var_matchs = [index for index, char in enumerate(fmt) if char in var_sizes]

        print(header.size)
        if not header.size:
            return super().pack(*args)
        body_fmt = body.format   
        index_len = {index: len(args[index]) for index in self.var_matchs}
        new_format = [str(index_len.get(index,"")) + char for index, char in enumerate(self.format)]
        new_format = "".join(new_format)

        print(new_format,"here")
        print(*[index_len[index] for index in self.var_matchs])
        return header.pack(*[index_len[index] for index in self.var_matchs]) + struct.pack(new_format,*args)
    def __lshift__(self,data):
        self.message_list.append(data)
        return self
    def __rshift__(self,data):
        val = self.message_list.pop()
        #not sure how to store val in passed var outside of namespace
        return self
    

class Custom_Struct(struct.Struct):
    def __init__(self, fmt):
        self.original_format = fmt
        self._build(fmt)

    def _build(self, fmt):
        var_sizes = ["s","p"]
        self.var_matchs = [index for index, char in enumerate(fmt) if char in var_sizes]
        header_fmt = "B"*len(self.var_matchs)
        print(header_fmt,self.var_matchs)
        self.header = struct.Struct(header_fmt)
        self.body = struct.Struct(fmt)
        
        new_format = "".join((header_fmt,fmt))
        
        super().__init__(fmt)
    
    def pack(self,*args,fmt = None):
        header = self.header
        body = self.body

        print(header.size)
        if not header.size:
            return super().pack(*args)
        body_fmt = body.format   
        index_len = {index: len(args[index]) for index in self.var_matchs}
        new_format = [str(index_len.get(index,"")) + char for index, char in enumerate(self.format)]
        new_format = "".join(new_format)

        print(new_format,"here")
        print(*[index_len[index] for index in self.var_matchs])
        #print()
        return header.pack(*[index_len[index] for index in self.var_matchs]) + struct.pack(new_format,*args)
    def unpack(self, bytes):
        header = self.header
        body = self.body
        
        if not header.size:
            return super().unpack(*args)
        
        header_size = bytes[0]
        
        header_formant = bytes[1:header_size + 1]
        header_formant.decode('utf-8')

        
        message = None

        header_bytes = bytes[:header.size]
        body_bytes = bytes[header.size:]

        body_format = body.format

        size_var = header.unpack(header_bytes)    
        print("size_var",size_var)
        index_len = dict(zip(self.var_matchs, size_var))

        new_format = [str(index_len.get(index,"")) + char for index, char in enumerate(body_format)]
        new_format = "".join(new_format)

        return struct.unpack(new_format, body_bytes)

    def size(self, bytes):
        base_size = super().size
        if not bytes:
            return base_size
        header_bytes = self.header.unpack(bytes[:self.header.size])

        return base_size +sum(header_bytes)

"""
a = Custom_Struct("s?B?")
packet = ("hello".encode("utf-8"),True,12,False)
test = a.pack(*packet)
print("bytes",a.pack(*packet))
print(a.unpack(test))
"""
fmt = "5s?B?"
args = ("hello",True,12,False)
new_args = [i.encode("utf-8") if type(i) == str else i for i in args]
print(new_args)

def temp():
    temp = ()
    temp = temp + (1,)
    return temp

print(temp())