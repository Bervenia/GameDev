import pyglet
from noise import snoise3
import random
from pyglet.gl import *
from Falloff import Falloff_Generator
class Terrain():
    def __init__(self,name,height,color):
        self.name = name
        self.height = height
        self.color = color


class noise_map():
    def __init__(self,width,length,octave,persistance,lacunarity):
        self.width = width
        self.length = length
        self.half_width = width/2
        self.half_length = length/2
        self.scale = 46
        self.octave = octave
        self.persistance = persistance
        self.lacunarity = lacunarity
        self.seed = 45
        self.falloff = True
        self.color_map = []
        self.imageData =''
        #                       name, height, rgb color
        self.regions = [Terrain("Snow",1,[222,235,238]),
                        Terrain("Rock2",.83,[72,62,52]),
                        Terrain("Rock1",.75,[90,77,65]),
                        Terrain("Grass2",.65,[48,99,42]),
                        Terrain("Grass1",.55,[70,137,68]),
                        Terrain("Sand",.45,[216,210,156]),
                        Terrain("water shallow",.42,[80,180,205]),
                        Terrain("water deep",.3,[10,140,180]),
                        ]
    def make_map(self):
        """create a collored hight map"""
        self.color_map = []
        if self.falloff:
            mask = Falloff_Generator(self.width,self.length).island()
        for x in range(self.width):
            for y in range(self.length):
                val = self.norm(snoise3((x-self.half_width)/self.scale, (y-self.half_length)/self.scale,self.seed,self.octave,self.persistance,self.lacunarity),-.85,.85)
                if self.falloff:#coment out to remove island gen
                    val = val-mask[x][y]
                #color = self.get_monochrome(val)
                color = self.get_color(val)
                self.color_map += color
                
        self.rawData = (pyglet.gl.GLubyte * len(self.color_map))(*self.color_map)
        self.imageData = pyglet.image.ImageData(self.width, self.length, 'RGB', self.rawData)                                                                                                                                                              
        return self.imageData                                                 
        
    def make_mask(self):
        """genrate the island fall of map and return it"""
        mask = Falloff_Generator(self.width,self.length).island()
        mask_color_map =[]
        for i in range(self.width):
            for j in range(self.length):
                val = self.norm(mask[i][j],0,1)
                color = int(self.lerp(0,255,val))
                mask_color_map = mask_color_map + [color,color,color]
        rawData = (pyglet.gl.GLubyte * len(mask_color_map))(*mask_color_map)
        self.mask = pyglet.image.ImageData(self.width, self.length, 'RGB', rawData)
        return self.mask
        
    def lerp(self, start, end, percent):
        """return a value between two points based off percentage"""
        return start*(1 - percent) + end*percent
    
    def norm(self, val,start,end):
        """return a percentage between two points based off value """
        return (val-start) /(end-start)
    
    def draw_map(self,x,y):
        """draw the map"""
        self.texture = self.imageData.get_texture()   
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        #^ make changes in color hard lines and not blurred ^ 
        self.texture.blit(0,0,width = x,height = y)
        
    def get_monochrome(self,val):
        color = int(self.lerp(0,255,val))
        return [color,color,color]
    
    def get_color(self,val):
        for i in range(len(self.regions)):
            if val <= self.regions[i].height:
                color = self.regions[i].color
        return color
    
if __name__ == "__main__":
    import pyglet
    from noise import snoise3
    import random
    from pyglet.gl import *
    from Falloff import Falloff_Generator
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    random.seed()
    tilesize = 20
    window = pyglet.window.Window(1080,720,visible=True, resizable=False,caption="World generation")
    x,y = window.get_size()
    octave = 4
    persistance = .5
    lacunarity = 2
    level = noise_map(100,100,octave,persistance,lacunarity)
    @window.event
    def on_draw():
        global imageData
        window.clear()
        
        level.draw_map(x,y)
    @window.event
    def on_mouse_press(x, y, button, modifiers):

        if button == pyglet.window.mouse.LEFT:
            format = 'RGB'
            pitch = level.imageData.width * len(format)
            pixels = level.imageData.get_data(format, pitch)
            temp = level.norm(x,0,1080)
            x = int(level.lerp(0,100,temp))
            temp = level.norm(y,0,720)
            y = int(level.lerp(0,100,temp))
            
        
    @window.event
    def on_key_press(symbol,modifiers):
        global seed
        if symbol == pyglet.window.key.SPACE:
            window.clear()
            level.seed = random.random()*100000
            level.make_map()
        if symbol == pyglet.window.key.W:
            level.scale +=1
            level.make_map()
        if symbol == pyglet.window.key.S:
            level.scale -=1
            level.make_map()
        
                       
    level.make_map()
    pyglet.app.run()

