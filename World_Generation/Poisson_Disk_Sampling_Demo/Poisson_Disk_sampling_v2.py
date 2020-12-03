import pyglet
import math
import random

active_img = pyglet.resource.image("active_point.png")
valid_img = pyglet.resource.image("valid_point.png")
main_batch = pyglet.graphics.Batch()
class Node:
    def __init__(self,x,y):
        self.sprite = pyglet.sprite.Sprite(img = active_img, x=x, y=y, batch = main_batch)
        self.x = x
        self.y = y

class Poisson:
    def __init__(self, width, height,r):
        self.width = width
        self.height = height
        self.r = r
        self.k = 30
        self.w = self.r/math.sqrt(2)
        self.cols = int(self.width / self.w)#colum length
        self.rows = int(self.height / self.w)#row width
        self.active = []
        self.grid = [None for i in range(self.cols * self.rows)]

        #random start
        x = self.width/2
        y = self.height/2
        start_point = Node(x,y)
        index = int(start_point.x/self.w + start_point.y/self.w * self.cols)
        
        self.grid[index] = start_point
        self.active.append(start_point)

if __name__ == "__main__":
    import pyglet
    import random

    window = pyglet.window.Window(505,505,vsync=False)
    radius = 20
    poisson = Poisson(500,500,radius)
    main_batch = pyglet.graphics.Batch()
    fps_display = pyglet.window.FPSDisplay(window)
    fps_display.label.color = (255, 255, 0, 255)
    #temp = pyglet.shapes.Circle(100,100,16, color =(255,0,0), batch = main_batch)
    
    lines = []
    w = int(radius/math.sqrt(2)) 
    print(36*w)   
    for i in range(0,505,w):
        temp = pyglet.shapes.Line(0,i,504,i,batch = main_batch)
        lines.append(temp)

    for j in range(1,506,w):
        temp = pyglet.shapes.Line(j,0,j,504,batch = main_batch)
        lines.append(temp)
               
    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        fps_display.draw()
        
    def update(dt):
        #pass
        poisson.update()
        
        

    
    pyglet.clock.schedule_interval(update,1/60)

    pyglet.app.run()
