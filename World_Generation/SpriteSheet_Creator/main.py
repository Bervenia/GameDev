import pyglet

from pyglet import clock
from pyglet.window import key
from pyglet import gl
from Camera import Camera
from Asset_loader import Asset_Loader
from Render import Render
import ui_module as ui


class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1280,740, resizable=False,config =  pyglet.gl.Config(double_buffer = True,depth_size =24),vsync = False,
                                   fullscreen=False, caption="arena",)
        self.asset_loader = Asset_Loader("./Assets")
        self.assets = self.asset_loader.load()
    

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
        
        self.render.draw()
        
        #self.world_camera.attach(self.entity_manager.get(0))
        self.on_draw = self.event(self.on_draw)
 
  #      self.game_object = []
        
        pyglet.clock.schedule_interval(self.update,1/60)
        #pyglet.clock.set_fps_limit(60)
    def remove_ui(self,ui_element, element_list):
        print(self.overlays)
        print(element_list)
        element_list.remove(ui_element)
        print(self.overlays)
        print(element_list)

    def update(self,dt):  
        #self.system.update_all(dt, self.entity_manager)
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

        
       
    def on_mouse_motion(self,x, y, dx, dy):
        #print("mouse x: ",x,"mouse y: ",y )
        self.system.inject({'type': 'player_movement', 'data': ["mouse_pos",x]})
    def on_mouse_press(self,x, y, button, modifiers):
        #print(button)
        if button == 4:
            print(self.world_camera.position)
            
            self.world_camera.position = (x,y)
            
            
            
        if button == 1:
            print("hello")
        
            entity = self.entity_manager.add(None,'Health','View',"Position","Velocity",'Collision')
            #entity = self.entity_manager.get(entity_id[0])

            entity.position.x, entity.position.y = x+self.world_camera.offset_x *self.world_camera.zoom,y+self.world_camera.offset_y *self.world_camera.zoom
            entity.view.sprite = sprite.CardSprite(img = self.assets['enemy'],x= entity.position.x, y = entity.position.y, tilt = 1,batch = self.main_batch)
            
            
            entity.view.sprite.scale = 3
            entity.view.idle = self.assets['enemy']
            print(entity.view.sprite.x)
            print(entity.view.sprite.tilt)
                
            print("by")
            
            #print("hi")
            #print(self.entity_manager.get_all())

    def on_key_press(self,symbol,modifiers):
        if symbol == key.ESCAPE:
            self.close()
        if symbol == key.F3:
            print('calvin is gey')
            self.ui_module.debug_mode = not self.ui_module.debug_mode
        if symbol == key.W:
            print("swap")
            self.bg_batch = pyglet.graphics.Batch()
            self.draw = not self.draw
            self.render.draw(self.draw)
        
    def on_key_release(self,symbol, modifiers):
        pass
        # self.world_camera.position = (int(self.player.pos_vector[0]-self.world_size[0]/2),int(self.player.pos_vector[1]-self.world_size[1]/2))

    
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
