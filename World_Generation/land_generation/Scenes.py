import pyglet
import os
import json
import random
import land_generator
import Renderv3
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
        self.world_settings = {} 
        #window.main_batch = self.batch
        self.world_settings['seed'] = 300#int(random.random() * 10**8)
        self.world_settings['size'] = [128,128]
    def create_level_data(self,direct):
        data = self.world_settings
        level = land_generator.noise_map(data['size'][0],data['size'][1],data['seed']).make_map()
        
        #with open(os.path.join(direct,"level.dat"),"w") as output:
         #   json.dump(data,output)
        return level
    def create_world(self,level):
        self.tiles = self.window.render.auto_tile_region(level, 0, 0,self.bg_batch,True)

        
        print('hi there')
        #print(self.tiles)
    def load(self,directory = "/test_folder"):
        if os.path.exists(directory):
            pass#os.makedirs('my_folder')        
        else:
            #os.makedirs(directory)  
            data = self.create_level_data(directory)
            self.create_world(data[0])
            self.mini_map = pyglet.sprite.Sprite(img = data[1], x = 0, y = -200, batch=self.bg_batch)

