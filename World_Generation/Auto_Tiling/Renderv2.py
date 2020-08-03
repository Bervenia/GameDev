import pyglet
from random import randint
import json
#import cardspritev2 as sprite
class Render():
    def __init__(self,game):
        self.game = game
        self.level = 'test.txt'
        self.chunk_size = 3
        self.tile_size = 64
        self.map = self.get_level()
        self.auto_tile_region(self.map,0,0,3,3)
        self.sum_to_sheet = {
            2:1, 8:2, 10:3, 11:4, 16:5, 18:6, 22:7, 24:8, 26:9, 27:10, 30:11, 31:12,
	        64:13, 66:14, 72:15, 74:16, 75:17, 80:18, 82:19, 86:20, 88:21, 90:22, 91:23,
            94:24, 95:25, 104:26, 106:27, 107:28, 120:29, 122:30, 123:31, 126:32, 
	        127:33, 208:34, 210:35, 214:36, 216:37, 218:38, 219:39, 222:40, 223:41, 
	        246:36, 248:42, 250:43, 251:44, 254:45, 255:46, 0:47
            }

    def get_level(self):
        """Loads the tilemap from a given textfile and returns a 2d list tilemap
        
        Returns:
            data -- 2d tilemap list
        """
        with open(self.level)as file:
            data = file.read().splitlines()
            for i in range(len(data)):
                data[i] = data[i].split(",")
            data.reverse() #reverse order due to pyglet's coordinate system   
        return data
    
    def boundary_check(self,length,x,y):
        return 0 <= y < length and 0 <= x < length

    def check_neighbor_types(self, level, x, y):
        tiles = []
        for i in range(-1,2):
            for j in range(-1,2):
                if self.boundary_check(len(level),x+j,y+i) and level[y+i][x+j] > level[y][x]:
                    if level[y+i][x+j] not in tiles:
                        tiles.append(level[y+i][x+j])
        print(tiles)
        if len(tiles) == 1 and level[y][x]+tiles[0] in self.game.assets.keys():
            return level[y][x]+tiles[0]
        else:
            return False
    def check_neighbor(self, level, x, y, x_off, y_off):
        if self.boundary_check(len(level),x+x_off,y+y_off):
            if x_off == 0 or y_off == 0:#N,E,S,W
                if level[y+y_off][x+x_off] == level[y][x]:
                    return True
                else:
                    return False
            else:#NW,NE,SW,SE
                if (level[y+y_off][x+x_off] == level[y][x] and
                    level[y+y_off][x] == level[y][x] and
                    level[y][x+x_off] == level[y][x]):
                    return True
                else: 
                    return False

    def auto_tile_region(self, level, x, y, width, height):
        region = pyglet.image.Texture.create(width = self.tile_size*self.chunk_size, height =self.tile_size*self.chunk_size)    
        # loop through level looking at neighbors of
        for i in range(y,height):
            for j in range(x,width):
                tile_value = 0
                single_transition = self.check_neighbor_types(level,j,i)
                
                
                if single_transition:
                    if self.check_neighbor(level,j,i,-1,-1): tile_value += 1 #NW
                    if self.check_neighbor(level,j,i, 0,-1): tile_value += 2#N
                    if self.check_neighbor(level,j,i, 1,-1): tile_value += 4#NE
                    if self.check_neighbor(level,j,i,-1, 0): tile_value += 8#W
                    if self.check_neighbor(level,j,i, 1, 0): tile_value += 16#E
                    if self.check_neighbor(level,j,i,-1, 1): tile_value += 32#SW
                    if self.check_neighbor(level,j,i, 0, 1): tile_value += 64#S
                    if self.check_neighbor(level,j,i, 1, 1): tile_value += 128#SE
                
                
if __name__ == "__main__":
    pass