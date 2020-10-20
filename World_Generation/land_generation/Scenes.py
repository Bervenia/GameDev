import os
import json
import random

import pyglet

#import land_generator

import World
from Generators import World_Generator
import Renderv3
from Config import *
class Scene_Manager():
    _current_scene = None
    def __init__(self, window, ):
        #self._current_scene = scene
        self.window = window

    def update(self,dt):
        if self._current_scene:
            self._current_scene.update(dt)

    def draw(self):
        if self._current_scene:
            self._current_scene.bg_batch.draw()
            self._current_scene.main_batch.draw()


    @classmethod
    def change_scene(cls,win,new_scene):
        if cls._current_scene != None:
            cls._current_scene.unload()
        new_scene.load()
        
        cls._current_scene = new_scene
        win.push_handlers(cls._current_scene)

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
        self.world = World.World(self.main_batch,self.window.ui_batch)
        self.initialized = False
        self.moved_camera = False

    def update(self,dt):
        if not self.initialized:
            self.load()
        
        self.world.process_queue()
      
        if self.moved_camera:
            cam_pos = self.window.world_camera.position
            tile_pos = (cam_pos[0]//TILE_SIZE,cam_pos[1]//TILE_SIZE)
            chunk = (int(tile_pos[0]/CHUNK_SIZE),int(tile_pos[1]/CHUNK_SIZE))
            print(chunk,self.current_chunk)
            self.update_shown_chunks(tile_pos)

            self.current_chunk = chunk
            self.position = tile_pos
            self.world.mini_map(self.window.width,self.window.height,self.position,self.window.ui_batch)
            print("movement")
            self.moved_camera = False

    def update_shown_chunks(self,position):
        chunk = (int(position[0] // CHUNK_SIZE), int(position[1] // CHUNK_SIZE))
        #print(chunk)
        if chunk == self.current_chunk:
            print("the same")
            return
        chunks_to_show = []
        for dy in range(-1,2):
            for dx in range(-1,2):
                x, y = chunk 
                chunks_to_show.append((x + dx, y + dy))
        print(chunks_to_show)
        self.world.show_given_chunks(chunks_to_show)
    
    def load(self,directory = "/test_folder"):
        generator = World_Generator()
        self.world.generator = generator
        self.update_shown_chunks(self.position)
        self.world.mini_map(self.window.width,self.window.height,self.position,self.window.ui_batch)
        self.initialized = True

    
    def on_mouse_press(self,x, y, button, modifiers):
        if button == 4:#right click
            self.window.world_camera.position = (x, y)
            pos = self.window.world_camera.position
            print(pos,(pos[0]//64,pos[1]//64))
            self.moved_camera = True