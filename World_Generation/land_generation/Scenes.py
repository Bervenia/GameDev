import os
import json
import random

import pyglet

import land_generator
import World
import Renderv3
from Config import *
class Scene_Manager():
    _current_scene = None
    def __init__(self, window, ):
        #self._current_scene = scene
        self.window = window

    def update(self):
        if self._current_scene:
            self._current_scene.update()

    def draw(self):
        if self._current_scene:
            self._current_scene.bg_batch.draw()
            self._current_scene.main_batch.draw()


    @classmethod
    def change_scene(cls,new_scene):
        if cls._current_scene != None:
            cls._current_scene.unload()
        new_scene.load()
        cls._current_scene = new_scene

class Scene():
    def __init__(self, window, name):
        self.name = name
        self.window = window
        self.main_batch = pyglet.graphics.Batch()
        self.bg_batch = pyglet.graphics.Batch()

    def update(self):
        pass#overwrite in subclass

    def load(self):
        pass#overwrite in subclass
    
    def unload(self):
        pass#overwrite in subclass

class Overworld(Scene):
    def __init__(self,window, data = None):
        super().__init__(window,"Overworld")
        self.data = data
        self.position = (0,0)
        self.current_chunk = None
        self.seed = 300
        self.size = (128,128)
        self.world = World.World(self.main_batch)
        self.on_resize(*self.window.get_size())
        self.initialized = False
        self.moved_camera = False

    def update(self,dt):
        if not self.initialized:
            self.load()
        self.world.process_queue()
        if self.moved_camera:
            pass

    def update_shown_chunks(self,position):
        chunk = (self.position[0] // CHUNK_SIZE, self.position[1] // CHUNK_SIZE)
        if chunk == self.current_chunk:
            return
        chunks_to_show = []
        for dy in range(-1,2):
            for dx in range(-1,2):
                x, y = chunk 
                chunks_to_show.append((x + dx, y + dy))
        self.world.show_given_chunks(chunks_to_show)
    
    def on_resize(self):
        pass
    def load(self,directory = "/test_folder"):
        generator = World_Generator()
        self.world.generator = generator