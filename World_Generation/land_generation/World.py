import time
from collections import deque

from Config import *

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
        """ Returns True if xy tile position within Chunk""" 
        return (self.min_pos[0] <= pos[0] < self.max_pos[0]
                and self.max_pos[1] <= pos[1] < self.max_pos[1])

    def get_tile(self, position):
        "return tile at position within Chunk. Else None"
        return self.tiles[position]
    
    def check_neighbors(self,position):
        """Checks all tiles surrounding `position` and ensures their visual
        state is up to date. This means autotiling and hidding tiles. 
        """
        for neighbor, direction in iter_neighbors(position):
            tile = self.get_tile(neighbor)
            if tile.current == False:
                tile.update()


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

        self.requested = set({})
        """list of chunks requested but not generated"""

        self.queue = deque()

    def count_tiles(self):
        """Return the number of tiles in this world"""
        return sum([len(val.blocks) for val in self.sectors.values()])

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, generator):
        assert self._generator is None, f'Generator for world already set!'
        self._generator = generator 
        
    def on_chunk_received(self,chunk):
        """called when part of the world is received"""
        self.enqueue(self.register_chunk, chunk)
    def update_batch_chunk(self,chunk):
        visible = chunk.position in self.shown_chunks

        
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
            if self.generator != None:
                self.requested.add(pos)
                self.generator.request_sector(pos)

    def show_chunk(self,chunk_pos):
        """ensure tiles within a given sector are being drawn"""
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
                self.generator.request_sector(chunk_pos)

        self.enqueue(self.update_batch_chunk, chunk)

    def hide_chunk(self, chunk_pos):
        """Ensure tiles within a given sector are being hidden"""
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
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """Process the entire queue with periodic breaks. Allowing
        the game to run smoothly avoiding the global interperter 
        lock.
        """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self.dequeue()