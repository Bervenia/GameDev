import pyglet
from noise import snoise3
import random
import time


class noise_map():
    def __init__(self,width,height,seed, octave =4,persistance=.5,lacunarity=2):
        self.width = width
        self.height = height
        self.octave = octave
        self.persistance = persistance
        self.lacunarity = lacunarity
        self.scale = 300
        self.seed = seed
        self.terrain ={
            1:["0",[72,62,52]]     , .6:["2",[70,137,68]],
            .45:["1",[216,210,156]], .42:["3",[80,180,205]]
            }#rock,grass,sand,water

    def make_map(self):
        """create a collored hight map"""
        mini_map = []
        level =[["" for j in range(self.width)] for i in range(self.height)]
        mask = Falloff_Generator(self.width,self.height).island()
        half_width = self.width//2
        half_height = self.height//2
        for y in range(self.height):
            if y % (204) == 0:
                print(y // 204)
            for x in range(self.width):
                val = self.norm(snoise3((y-half_height)/self.scale,
                                        (x-half_width)/self.scale,
                                        self.seed,self.octave,self.persistance,
                                        self.lacunarity),-.85,.85)
                val = val-mask[y][x]
                terrain, color = self.get_terrain(val)
                level[y][x] = terrain
                mini_map +=color
        rawData = (pyglet.gl.GLubyte * len(mini_map))(*mini_map)
        mini_map = pyglet.image.ImageData(self.width, self.height, 'RGB', rawData)
        return level,mini_map

    def get_terrain(self,val):
        for i in self.terrain:
            if val <= float(i):
                terrain = self.terrain[i][0]
                color = self.terrain[i][1]
        return terrain, color

    def lerp(self, start, end, percent):
        """return a value between two points based off percentage"""
        return start*(1 - percent) + end*percent
    
    def norm(self, val,start,end):
        """return a percentage between two points based off value """
        return (val-start) /(end-start)

class Falloff_Generator():
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def island(self):
        new_level = [["" for i in range(self.width)]for i in range(self.height)]
        for i in range(self.width):
            for j in range(self.height):
                x = i / float(self.width) * 2 - 1
                y = j / float(self.height) * 2 - 1

                value = max(abs(x),abs(y))
                new_level[i][j] = self.island_eq(value)
        return new_level
    
    def island_eq(self,val):
         a = 3
         b = 6
         return val**a/(val**a +(b-b*val)**a)

if __name__ == "__main__":
    start_time = time.time()
# your code

    window = pyglet.window.Window(1000,1000,vsync=False)
    fps_display = pyglet.window.FPSDisplay(window)
    fps_display.label.color = (255, 255, 0, 255)
    batch = pyglet.graphics.Batch()
    
    octave = 4
    persistance = .5
    lacunarity = 2
    world = noise_map(2048,2048,45,octave,persistance,lacunarity)
    level, mini_map = world.make_map()
    sprite = pyglet.sprite.Sprite(img = mini_map, x = 0, y = 0, batch=batch)
    elapsed_time = time.time() - start_time
    print('done! took',elapsed_time, "seconds.")
    sprite.scale = .25
    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        fps_display.draw()
        
    def update(dt):
        pass
        
    pyglet.clock.schedule(update)
    pyglet.app.run()

