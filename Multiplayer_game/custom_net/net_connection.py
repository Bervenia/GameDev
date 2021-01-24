
import enum
from collections import deque 
import net_message



class Connection():
    class owner(enum.Enum):
        server = 0,
        client = 1
    def __init__(self, owner, context, socket, q_message_in):
        self.owner_type = owner
        self.context = context
        self.q_message_in = q_message_in
        self.q_message_out = deque()
        self.reader, self.writer = socket
        self.id = 0

    def get_id(self):
        return self.id

    def connect_to_server(self,address):
        if self.owner_type == self.owner.client:
            self.context.create_task(self.read_header())

    def connect_to_client(self,user_id):
        if self.owner_type == self.owner.server:
            if not self.writer.is_closing():
                self.id = user_id
                #print("here")
                self.context.create_task(self.read_header())
                #asyncio.create_task(self.read_header())

    def disconnect(self):
        if not self.writer.is_closing():
            self.writer.close()
    def is_connected(self):
        return not self.writer.is_closing()

    def send(self, msg):
        async def check_progress():
            busy_writing = not len(self.q_message_out) == 0
            self.q_message_out.append(message)
            if not busy_writing:
                asyncio.create_task(self.write_header())

        self.context.create_task(check_progress())
        

    #Async methods
    async def read_header(self):
        print('reading')
        try:
            print(self.reader)
            header = await self.reader.readexactly(4)
            size = struct.unpack('b', header)[0]
            print(size)
            if size > 0:
                self.read_body(size)
        except:
            print(f"[{self.id}] Read Header Fail.")
    async def read_body(self):
        try:
            body = await self.reader.readexactly(size)
            
            print(body)
            self.add_to_incoming_message_queue(body)
            #message = await self._reader.readexactly(size)
            #self._loop.call_soon(self.dispatch_event, 'on_receive', self, message)
        except asyncio.IncompleteReadError:
            print(f'[{self.id}] Read header failed')
            self.close()

    async def write_header(self):
        try:
            message = self.q_message_out[0]
            self.writer.write(message.header())
            await self._writer.drain()
            if message.body.size > 0:
                self.write_body()
            else:
                self.q_message_out.popleft()
                if len(self.q_message_out) != 0:
                    self.write_header() 

        except ConnectionResetError:
            print(f'[{self.id}] Write header failed')
            self.disconnect()
    async def write_body(self):
        try:
            message = self.q_message_out[0]
            self.writer.write(message.body())
            await self._writer.drain()
           
            self.q_message_out.popleft()
            if len(self.q_message_out) != 0:
                self.write_header() 

        except ConnectionResetError:
            print(f'[{self.id}] Write body failed')
            self.disconnect()

    def add_to_incoming_message_queue(self,msg):
        if self.owner_type == self.owner.server:
            self.q_message_in.append(self,msg)#add ownership
        else:
            self.q_message_in.append(None,msg)
        self.read_header()