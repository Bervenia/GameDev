
import pyglet 
from pyglet.gl import *
class Overlay:
    
    def __init__(self):
        self.font_name = 'Arial'
    def update(self, dt):
        pass

    def draw(self):
        pass
    



class Banner(Overlay):
    instances = [] 
    def __init__(self,game, label, fade_in = False, fade_out = False, timeout=None):
        super(Banner, self).__init__()
        #glEnable(GL_BLEND)                                  # transparency
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.text = pyglet.text.Label(label,
                                      font_name = self.font_name,
                                      font_size = 36,
                                      x = game.width // 2,
                                      y = game.height *.7,
                                      anchor_x="center",
                                      anchor_y="baseline")
        self.color = list(self.text.color)
        self.timeout  = timeout
        self.fade_in  = fade_in
        self.fade_out = fade_out

        self.time_elapsed = 0
        '''
        #self.dismiss_func = lambda n: Banner.delete_instance(self)
        
        if timeout and self.dismiss_func:
            pyglet.clock.schedule_once(self.dismiss_func, timeout)
        '''
        self.instances.append(self)


    def update(self,dt):
        if self.fade_in and self.time_elapsed < self.timeout//2:
            percentage = self.time_elapsed / (self.timeout //2)
            self.color[-1] = max(min(int(percentage * 255),255),0)
            self.text.color = tuple(self.color)
        if self.fade_out and self.time_elapsed > self.timeout//2:
            percentage = (self.timeout - self.time_elapsed) / (self.timeout //2)
            self.color[-1] = max(min(int(percentage * 255),255),0)
            self.text.color = tuple(self.color)
        if self.time_elapsed >= self.timeout:
            Banner.delete_instance(self)
        self.time_elapsed += dt
    def draw(self):
        self.text.draw()

    @classmethod    
    def delete_instance(cls,instance,):
        cls.instances.remove(instance)
    

class Menu(Overlay):
    instances = []
    def __init__(self, title, x, y):
        self.items = []
        self.title_text = pyglet.text.Label(title,
                                            font_name=self.font_name,
                                            font_size=36,
                                            x= x,
                                            y= y,
                                            anchor_x='center',
                                            anchor_y='center')
    """
    def reset(self):
        self.selected_index = 0
        self.items[self.selected_index].selected = True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.DOWN:
            self.selected_index += 1
        elif symbol == key.UP:
            self.selected_index -= 1
        self.selected_index = min(max(self.selected_index, 0),
                                  len(self.items) - 1)

        if symbol in (key.DOWN, key.UP) and enable_sound:
            bullet_sound.play()

    def on_key_release(self, symbol, modifiers):
        self.items[self.selected_index].on_key_release(symbol, modifiers)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            item.draw(i == self.selected_index)
    """