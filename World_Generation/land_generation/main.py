import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet import gl
from Camera import Camera
from Asset_loader import assets
from land_generator import noise_map
from Renderv3 import Render
import ui_module as ui
import Scenes

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1280,740, resizable=False,config =  pyglet.gl.Config(double_buffer = True,depth_size =24),vsync = False,
                                   fullscreen=False, caption="arena",)
        #engine parameters                                   
        self.on_draw = self.event(self.on_draw)
        self.projection = Projection2D()     
        self.fps = pyglet.window.FPSDisplay(self)   

        #graphics and view ports
        self.assets = assets
        self.ui_batch = pyglet.graphics.Batch()
        self.render = Render(self)
        self.scene_manager = Scenes.Scene_Manager(self)
        self.world_camera = Camera((self.width,self.height))
        self.world_camera.position = (0,0)
        self.ui_camera = Camera((self.width,self.height))
        self.ui_banners = ui.Banner
        self.ui_menus = ui.Menu

        #start up
        ui.Banner(self,"Overworld",True,True, timeout = 5)
        self.scene_manager.change_scene(Scenes.Overworld(self))
        pyglet.clock.schedule(self.update)   

    def update(self,dt):
        for menu in self.ui_menus.instances:
            menu.update(dt)
        for banner in self.ui_banners.instances:
            banner.update(dt) 
        self.world_camera.update()
        self.ui_camera.update()
        self.scene_manager.update(dt)

    def on_draw(self):
        self.clear()
        with self.world_camera:
            self.scene_manager.draw()
            self.fps.draw()
        with self.ui_camera:
            self.ui_batch.draw()
    
    def on_mouse_press(self,x, y, button, modifiers):
        if button == 4:#right click
            self.world_camera.position = (x, y)

    def on_key_press(self,symbol,modifiers):
        pass

    def on_key_release(self,symbol, modifiers):
        pass
    

class Projection2D(pyglet.window.Projection):
    """A 2D orthographic projection"""
    def set(self, window_width, window_height, viewport_width, viewport_height):
        gl.glViewport(0, 0, max(1, viewport_width), max(1, viewport_height))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, max(1, window_width), 0, max(1, window_height), -255, 255)
        gl.glMatrixMode(gl.GL_MODELVIEW)
            
if __name__ == '__main__': 
    window = Game()
    pyglet.app.run()
