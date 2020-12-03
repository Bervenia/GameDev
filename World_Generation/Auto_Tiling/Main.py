import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet import gl
from Camera import Camera
from Asset_loader import Asset_Loader
from Renderv2 import Render
import ui_module as ui

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1280,740, resizable=False,config =  pyglet.gl.Config(double_buffer = True,depth_size =24),vsync = False,
                                   fullscreen=False, caption="arena",)
        self.asset_loader = Asset_Loader("./Assets")
        self.assets = self.asset_loader.load()
    
        self.auto = True
        self.main_batch = pyglet.graphics.Batch()
        self.bg_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.projection = Projection2D()
        self.render = Render(self)
        
        self.ui_banners = ui.Banner
        self.ui_menus = ui.Menu 
        ui.Banner(self,"Auto Tiling",True,True, timeout = 5)
        self.world_camera = Camera((self.width,self.height))
        self.ui_camera = Camera((self.width,self.height))
        self.fps = pyglet.window.FPSDisplay(self)
        self.draw = False
        
        pyglet.clock.schedule(self.update)   

    def update(self,dt):
        for menu in self.ui_menus.instances:
            menu.update(dt)
        for banner in self.ui_banners.instances:
            banner.update(dt) 
        self.world_camera.update()
        self.ui_camera.update()

    def on_draw(self):
        self.clear()
        with self.world_camera:
            self.main_batch.draw()
            self.bg_batch.draw()
            self.fps.draw()
        with self.ui_camera:
            for menu in self.ui_menus.instances:
                menu.draw()
            for banner in self.ui_banners.instances:
                banner.draw()
    
    def on_mouse_press(self,x, y, button, modifiers):
        pass
    def on_key_press(self,symbol,modifiers):
        if symbol == pyglet.window.key.W:
            self.auto = not self.auto
            self.render = Render(self)
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
