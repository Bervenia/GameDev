import math
import random
import pyglet
class Node:
    def __init__(self,x,y):
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
        print(self.cols,self.rows)
        self.active = []
        self.grid = [None for i in range(self.cols * self.rows)]

        #random start
        x = self.width/2
        y = self.height/2
        start_point = Node(x,y)
        index = int(start_point.x/self.w + start_point.y/self.w * self.cols)
        print(index,len(self.grid))
        self.grid[index] = start_point
        self.active.append(start_point)

    def update(self):
        if len(self.active) > 0:
            randindex = random.randint(0,len(self.active)-1)
            current_node = self.active[randindex]
            found = False
            for i in range(self.k):
                new = Node(random.uniform(-2,2),random.uniform(-2,2))
                mag = math.sqrt(new.x*new.x + new.y*new.y)
                
                new_mag = random.randint(self.r,self.r*2)
                new.x = (new.x/mag * new_mag)+current_node.x
                new.y = (new.y/mag * new_mag)+current_node.y

                col = int(new.x/self.w)
                row = int(new.y/self.w)

                if (col > 1 and row > 1 and col < self.cols-1 and row < self.rows-1
                 and not self.grid[col +row *self.cols] ):
                    
                    valid = True
                    for i in range(-1,2):
                        for j in range(-1,2):
                            index = (col+i + (row+j) * self.cols)
                            neighbor = self.grid[index]
                            if neighbor:
                                dist = math.sqrt((new.x - neighbor.x)**2 + (new.y - neighbor.y)**2)
                                if dist < self.r:
                                    valid = False
                    if valid:
                        found = True
                        
                        self.grid[(col + row*self.cols)] = new
                        self.active.append(new)
            if not found:
                del self.active[randindex]





if __name__ == "__main__":
    import pyglet
    import random

    window = pyglet.window.Window(500,500,vsync=False)
    radius = 20
    poisson = Poisson(500,500,radius)
    main_batch = pyglet.graphics.Batch()
    fps_display = pyglet.window.FPSDisplay(window)
    fps_display.label.color = (255, 255, 0, 255)
    #temp = pyglet.shapes.Circle(100,100,16, color =(255,0,0), batch = main_batch)
    
    circles = []
    w = int(radius/math.sqrt(2))
    print(500/w)
    """
    for i in range(0,500,w):
        temp = pyglet.shapes.Line(0,i,500,i,batch = main_batch)
        circles.append(temp)
    print(len(circles))
    for j in range(0,500,w):
        temp = pyglet.shapes.Line(j,0,j,500,batch = main_batch)
        circles.append(temp)
    """        
    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        fps_display.draw()
        
    def update(dt):
        
        poisson.update()
        
        

        for cell in poisson.grid:
            if cell:
                #print(cell.x,cell.y)
                temp = pyglet.shapes.Circle(cell.x,cell.y,5, color =(255,255,255), batch = main_batch)
                circles.append(temp)
                #drawn.append(cell)
        for cell in poisson.active:
            
            temp = pyglet.shapes.Circle(cell.x,cell.y,5, color = (255,0,0),batch = main_batch)
            circles.append(temp)

    pyglet.clock.schedule_interval(update,1/60)

    pyglet.app.run()
