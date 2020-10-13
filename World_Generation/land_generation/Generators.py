

import concurrent.futures
import random

from noise import snoise3

from Config import *
from Tiles import *
from World import Chunk

class Noise:
    def __init__(self,enclosure,seed, octave =4,persistance=.5,lacunarity=2):
        self.enclosure = enclosure
        self.octave = octave
        self.persistance = persistance
        self.lacunarity = lacunarity
        self.scale = 300
        self.seed = seed

    def lerp(self, start, end, percent):
        """return a value between two points based off percentage"""
        return start*(1 - percent) + end*percent
    
    def norm(self, val,start,end):
        """return a percentage between two points based off value """
        return (val-start) /(end-start)

    def snoise3(self,x,y):
        """return a simplex noise value between (-1,1) with z axis acting as
        the seed. may need to revisit later.
        """
        x_pos = (x-self.enclosure//2)/self.scale
        y_pos = (y-self.enclosure//2)/self.scale
        val = max(min(snoise3(x,y,self.seed,self.octave,self.persistance,self.lacunarity),1),-1)
        val = self.norm(val,-.85,.85)
        return val

class World_Generator:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        self.callback = None

        self.seed = 24
        """noise seed for world"""

        self.enclosure = 128
        """map boundary size in x and w"""

        self.island_enable = True
        """If true applies fall off to world making an island"""
        self.terrain_gen = Noise(self.enclosure,self.seed)

        self.terrain_lookup = {}
        def add_terrain(height,terrain):
            self.terrain_lookup[height] = terrain

        add_terrain(1,STONE)
        add_terrain(.6,GRASS)
        add_terrain(.45,SAND)
        add_terrain(.42,WATER)

    def set_callback(self,callback):
        """set a new callback when a new chunk is loaded"""
        self.callback = callback

    def request_chunk(self,chunk):

        def send_result(future):
            chunk = future.result()
            
            self.callback(chunk)
        future = self.executor.submit(self.generate, chunk)
        future.add_done_callback(send_result)
    
    def inter_all(self, chunk):
        """iterate over all the tiles in chunk"""
        x_min, y_min = chunk.min_pos
        x_max, y_max = chunk.max_pos
        
        for x in range(x_min,x_max):
            for y in range(y_min,y_max):
                yield x, y

    def generate(self,chunk):
        """Generate a specifice chunk and tiles of the world"""
        chunk = Chunk(chunk)

        if self.island_enable:
            self._generate_island_map(chunk)
        return chunk

    def _generate_island_map(self,chunk):
        n = self.enclosure

        for x, y in self.inter_all(chunk):
            
            if x <= -n or x >= n or y <= -n or y >= n :
                continue
            
            tile = self._get_tile(x,y)
            
            chunk.add_tile((x,y),tile)

    def _get_tile(self,x,y):
        val = self.terrain_gen.snoise3(x,y)
        #print(val,int((val+1)*.5*len(self.terrain_lookup)))
        for i in self.terrain_lookup:
            
            if val <= i:
                terrain = self.terrain_lookup[i]
        return terrain
        
if __name__ == "__main__":
    temp = World_Generator()
    #temp._get_biome(500,5)