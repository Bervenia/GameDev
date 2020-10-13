import time
from collections import deque
import random

import pyglet 
from Asset_loader import assets
from Config import *
from Tiles import CustomGroup

def iter_neighbors(position):
    """iterate through position neighboring given position"""
    x, y = position
    for i in range(-1,2):
        for j in range(-1,2):
            direction = (j, i)
            neighbor = x + j, y + i
            yield neighbor, direction


class Chunk:
    def __init__(self,position):
        self.tiles = {}
        """Tiles Located within Chunk"""

        self.position = position
        """Global position of Chunk"""

        self.min_pos = [i * CHUNK_SIZE for i in position]
        """Minimum position(included) of xy tile coord"""

        self.max_pos = [(i + 1) * CHUNK_SIZE for i in position]
        """Maximum position(excluded) of xy tile coord"""
    
    def contains(self,pos):
        """Returns True if pos(x, y) tile position within Chunk""" 
        return (self.min_pos[0] <= pos[0] < self.max_pos[0]
                and self.min_pos[1] <= pos[1] < self.max_pos[1])

    def get_tile(self, position):
        "return tile at position within Chunk. Else None"
        return self.tiles[position]
        
    def add_tile(self, position, tile):
        """add a tile to this chunk so long as position is apart of chunk"""
        #print(position, self.position,self.min_pos,self.max_pos,self.contains(position))
        #print(self.min_pos[0] <= position[0] < self.max_pos[0],self.min_pos[1] <= position[1] < self.max_pos[1])
        if not self.contains(position):
            return
        #print("added tile")
        self.tiles[position] = tile
        self.check_neighbors(position)
    def empty(self,pos):
        return pos not in self.tiles
    def check_neighbors(self,position):
        """Checks all tiles surrounding `position` and ensures their visual
        state is up to date. This means autotiling and hidding tiles. 
        """
        for neighbor, direction in iter_neighbors(position):
            if self.empty(neighbor):
                continue
            else:
                tile = self.get_tile(neighbor)
                #if tile.current == False:
                 #   tile.update()


class World():
    def __init__(self, batch):
        self.batch = batch 
        """pyglet.graphics batch object"""

        self._generator = None
        """Procedural generator"""

        self.chunks = {}
        """Mapping from Chunk index a list of positions"""

        self.shown_chunks = set({})
        """Currently show chunks"""

        self._shown_chunks = {}
        """links vertex lists to chunks to keep from garbage colletion"""

        self.requested = set({})
        """list of chunks requested but not generated"""

        self.queue = deque()
        """simple queue with show and hide calls"""

    def count_tiles(self):
        """Return the number of tiles in this world"""
        return sum([len(val.blocks) for val in self.chunks.values()])

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, generator):
        assert self._generator is None, f'Generator for world already set!'
        generator.set_callback(self.on_chunk_received)
        self._generator = generator 
        
    def on_chunk_received(self,chunk):
        """called when part of the world is received"""
        self.enqueue(self.register_chunk, chunk)

    def get_corners(self,x,y,n):
        """x, y = bottom left coord of tile
        n = size of tile 
        """
        dx = x * TILE_SIZE
        dy = y * TILE_SIZE
        p1= dx-n,dy-n
        p2 = dx-n,dy+n
        p3 = dx+n,dy+n
        p4 = dx+n,dy-n
        #print(dx,dy, dx+n,dy, dx+n,dy+n, dx,dy+n)
        return(*p1,*p4,*p3,*p2)

    def update_batch_chunk(self,chunk):
        random.seed(a = 24)
        visible = chunk.position in self.shown_chunks
        

        old_vertex_list = self._shown_chunks.pop(chunk.position, None)
        if old_vertex_list:#remove old from video memory
            old_vertex_list.delete()

        if visible:
            points = CHUNK_SIZE**2 * 4
            vertex_data = []
            texture_coords = []
            #test =(0.81787109375, 0.00048828125, 0.0, 0.84912109375, 0.00048828125, 0.0, 0.84912109375, 0.03173828125, 0.0, 0.81787109375, 0.03173828125, 0.0)
            red = [255,0,0,255]
            for tile in chunk.tiles:
                #print("tile:",tile)
                temp = chunk.tiles[tile]
                #print("hi",self.get_corners(*tile,TILE_SIZE//2))
                vertex_data.extend(self.get_corners(*tile,TILE_SIZE//2))
                texture = chunk.tiles[tile].texture_coords
                #print(len(texture),texture)
                texture_coords.extend(texture) 
            #texture_coords = list(filter(lambda a: a!=0.0,texture_coords))
                 
            #print(points,len(vertex_data),len(texture_coords))
            #print(texture_coords)
            #group =
            vertex_list = self.batch.add(points, pyglet.gl.GL_QUADS, pyglet.sprite.SpriteGroup(assets["Grass"].owner,770,771),
                                         ('v2f/static', vertex_data),
                                         ('t3f/dynamic', texture_coords))
            self._shown_chunks[chunk.position] = vertex_list
            #print("did you like ma tiles")
            random.seed(a = None)

    def register_chunk(self, chunk):
        """Add a new chunk to the world. Request neighboring chunks if 
        chunk is in shown chunks
        """

        assert chunk.position not in self.chunks, f'Chunk already in world!'
        self.requested.discard(chunk.position)
        self.chunks[chunk.position] = chunk
        if chunk.position not in self.shown_chunks:
            return

        #update displayed tiles
        self.enqueue(self.update_batch_chunk, chunk)

        for neighbor, direction in iter_neighbors(chunk.position):
            pos = neighbor

            #Must not be loaded
            if pos in self.chunks:
                continue
            #Must be in shown chunks
            if pos not in self.shown_chunks:
                continue 
            #Must not already be requested
            if pos in self.requested:
                continue
            #register new chunk
            #if self.generator != None:
                #self.requested.add(pos)
                #self.generator.request_chunk(pos)

    def show_chunk(self,chunk_pos):
        """ensure tiles within a given chunk are being drawn"""
        self.shown_chunks.add(chunk_pos)
        chunk = self.chunks.get(chunk_pos, None)

        if chunk is None:
            if chunk_pos in self.requested:
                return
            #if not loaded yet
            #if not self.is_chunk_visible(chunk_pos):
             #   return
            if self.generator != None:
                self.requested.add(chunk_pos)
                self.generator.request_chunk(chunk_pos)
                return 
        self.enqueue(self.update_batch_chunk, chunk)

    def hide_chunk(self, chunk_pos):
        """Ensure tiles within a given chunk are being hidden"""
        self.shown_chunks.discard(chunk_pos)
        chunk = self.chunks.get(chunk_pos,None)
        if chunk != None:
            self.enqueue(self.update_batch_chunk, chunk)

    def show_given_chunks(self, chunk_positions):
        after_set = set(chunk_positions) 
        before_set = self.shown_chunks
        hide = before_set - after_set
        show = [chunk for chunk in chunk_positions if chunk not in before_set]
        for chunk_pos in show:
            self.show_chunk(chunk_pos)
        for chunk_pos in hide:
            self.hide_chunk(chunk_pos)

    def enqueue(self, func, *args):
        """add function to queue"""
        self.queue.append((func, args))
    
    def dequeue(self):
        """pop the top internal function and call it"""
        #print("hello sir")
        func, args = self.queue.popleft()
        func(*args)
        #print("my son died have you seen him?")

    def process_queue(self):
        """Process the entire queue with periodic breaks. Allowing
        the game to run smoothly avoiding the global interperter 
        lock.
        """
        start = time.perf_counter()
        #print(time.perf_counter() - start,1.0 / TICKS_PER_SEC ,time.perf_counter() - start < 1.0 / TICKS_PER_SEC)
        #print(time.perf_counter() - start < 1.0 / TICKS_PER_SEC)
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self.dequeue()
            if not self.queue:
                print("done")
                image = self.generator.mini_map()
                self.temp = pyglet.sprite.Sprite(img = image,x= 0,y=-400,batch = self.batch)
                self.temp.scale = 5