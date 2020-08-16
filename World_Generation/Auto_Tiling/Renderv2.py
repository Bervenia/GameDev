import pyglet
from random import randint
import json

class Render():
    def __init__(self,game):
        self.game = game
        self.level = 'test.txt'
        self.chunk_size = 3
        self.tile_size = 64
        self.value_to_tile = {
            2:1, 8:2, 10:3, 11:4, 16:5, 18:6, 22:7, 24:8, 26:9, 27:10, 30:11, 31:12,
	        64:13, 66:14, 72:15, 74:16, 75:17, 80:18, 82:19, 86:20, 88:21, 90:22, 91:23,
            94:24, 95:25, 104:26, 106:27, 107:28, 120:29, 122:30, 123:31, 126:32, 
	        127:33, 208:34, 210:35, 214:36, 216:37, 218:38, 219:39, 222:40, 223:41, 
	        246:36, 248:42, 250:43, 251:44, 254:45, 255:46, 0:47
            }
        self.map = self.get_level()
        self.bg_sprites = self.auto_tile_region(self.map,0,0,len(self.map),len(self.map),True)

    def get_level(self):
        """Loads the tilemap from a given textfile and returns a 2d list tilemap
        
        Returns:
            data -- 2d tilemap list
        """
        with open(self.level)as file:
            data = file.read().splitlines()
            for i in range(len(data)):
                data[i] = data[i].split(",") 
        return data
    
    def boundary_check(self,length,x,y):
        return 0 <= y < length and 0 <= x < length

    def check_neighbor_types(self, level, x, y):
        tiles = []
        key = ""
        for i in range(-1,2):
            for j in range(-1,2):
                if self.boundary_check(len(level),x+j,y+i) and level[y+i][x+j] > level[y][x]:
                    key += level[y+i][x+j]
                    if level[y+i][x+j] not in tiles:
                        tiles.append(level[y+i][x+j])
                else:
                    key += level[y][x]
        if len(tiles) == 1 and level[y][x]+tiles[0] in self.game.assets.keys():
            return [len(tiles),level[y][x]+tiles[0]]
        else:
            return [len(tiles),tiles,key]
            
    def check_neighbor(self, level, x, y, x_off, y_off,mask = None):
        if self.boundary_check(len(level),x+x_off,y+y_off):
            if x_off == 0 or y_off == 0:#N,E,S,W
                if level[y+y_off][x+x_off] == level[y][x] or level[y+y_off][x+x_off] != mask:
                    return True
                else:
                    return False
            else:#NW,NE,SW,SE
                check_1 = level[y+y_off][x+x_off] == level[y][x] or level[y+y_off][x+x_off] != mask
                check_2 = level[y+y_off][x] == level[y][x] or level[y+y_off][x] != mask
                check_3 = level[y][x+x_off] == level[y][x] or level[y][x+x_off] != mask
                if (check_1 and check_2 and check_3):
                    return True
                else: 
                    return False
        else:#border
            boundary_x = self.boundary_check(len(level),x+x_off,y)
            boundary_y = self.boundary_check(len(level),x,y+y_off)
            tile_check_x = (level[y][x+x_off] == level[y][x] or level[y][x+x_off] != mask)
            tile_check_y = (level[y+y_off][x] == level[y][x] or level[y+y_off][x] != mask)
            check_1 = (x_off == 0 or y_off == 0)#vertical or horizontal
            check_2 = (not boundary_y and not boundary_x)#corner with vert and horz out of bounds 
            check_3 = not boundary_y and (boundary_x and tile_check_x)#corner with vert out of bounds
            check_4 = not boundary_x and (boundary_y and tile_check_y)#corner with horz out of bounds 
            if check_1 or check_2 or check_3 or check_4:
                return True

    def get_tile_value(self,level,j,i,mask = None):
        tile_value = 0
        if self.check_neighbor(level,j,i,-1,-1,mask): tile_value += 1#NW
        if self.check_neighbor(level,j,i, 0,-1,mask): tile_value += 2#N
        if self.check_neighbor(level,j,i, 1,-1,mask): tile_value += 4#NE
        if self.check_neighbor(level,j,i,-1, 0,mask): tile_value += 8#W
        if self.check_neighbor(level,j,i, 1, 0,mask): tile_value += 16#E
        if self.check_neighbor(level,j,i,-1, 1,mask): tile_value += 32#SW
        if self.check_neighbor(level,j,i, 0, 1,mask): tile_value += 64#S
        if self.check_neighbor(level,j,i, 1, 1,mask): tile_value += 128#SE
        return tile_value

    def auto_tile_region(self, level, x, y, width, height,auto_tile = False):
        sprites = []
        # loop through level looking at neighbors of
        for i in range(y,height):
            for j in range(x,width):
                x_pos = ((j)*self.tile_size)
                y_pos = ((height-i)*self.tile_size)
                
                transition = self.check_neighbor_types(level,j,i)
                if auto_tile == False:
                    transition = [0,level[i][j]]
                if transition[0] == 0:
                    image = self.game.assets[level[i][j]]
                    val = randint(0,image.width//self.tile_size-1)
                    tile = image.get_region(val*self.tile_size,0,self.tile_size,self.tile_size)
                    sprite = pyglet.sprite.Sprite(img = tile,x= x_pos, y = y_pos, batch = self.game.bg_batch)
                    sprites.append(sprite)
                elif transition[0] == 1:
                    image = self.game.assets[transition[1]]
                    tile_value = self.get_tile_value(level,j,i)
                    tile = image[self.value_to_tile[tile_value]]
                    sprites.append(pyglet.sprite.Sprite(img = tile,x= x_pos, y = y_pos, batch = self.game.bg_batch))
                elif transition[0] > 1:
                    if transition[2] in self.game.assets:
                        self.game.assets[transition[2]]
                    else:
                        base_image = self.game.assets[level[i][j]+transition[1][0]]
                        base_value = self.get_tile_value(level,j,i,transition[1][0])
                        tile = base_image[self.value_to_tile[base_value]]



        return sprites

    def neighbors(self,direction,level, x,y,mask):
        neighbors = []
        temp = -1
        if direction == 0:
            if self.boundary_check(len(level),x-1,y) and level[y][x-1] == mask:
                neighbors.append(level[y][x-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if self.boundary_check(len(level),x,y+1) and level[y+1][x] == mask:
                neighbors.append(level[y+1][x])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and self.boundary_check(len(level),x-1,y+1) and level[y+1][x-1] == mask:
                neighbors.append(level[y+1][x-1])  # southwest
                temp += 4
            else:
                neighbors.append(None)
        if direction == 1:
            if self.boundary_check(len(level),x+1,y) and level[y][x+1] == mask:
                neighbors.append(level[y][x+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if self.boundary_check(len(level),x,y+1) and level[y+1][x] == mask:
                neighbors.append(level[y+1][x])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and self.boundary_check(len(level),x+1,y+1) and level[y+1][x+1] == mask:
                neighbors.append(level[y+1][x+1])  # southeast
                temp += 4
            else:
                neighbors.append(None)
        if direction == 2:
            if self.boundary_check(len(level),x-1,y) and level[y][x-1] == mask:
                neighbors.append(level[y][x-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if self.boundary_check(len(level),x,y-1) and level[y-1][x] == mask:
                neighbors.append(level[y-1][x])  # north
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and self.boundary_check(len(level),x-1,y-1) and level[y-1][x-1] == mask:
                neighbors.append(level[y-1][x-1])  # northwest
                temp += 4
            else:
                neighbors.append(None)
        if direction == 3:
            if self.boundary_check(len(level),x+1,y) and level[y][x+1] == mask:
                neighbors.append(level[y][x+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if self.boundary_check(len(level),x,y-1) and level[y-1][x] == mask:
                neighbors.append(level[y-1][x])  # north
                temp += 2
            else:
                neighbors.append(None)  
            if temp == -1 and self.boundary_check(len(level),x+1,y-1) and level[y-1][x+1] == mask:
                neighbors.append(level[y-1][x+1])  # northeast
                temp += 4
            else:
                neighbors.append(None)
        temp = min(temp,3)
        neighbors.append(temp)
        return neighbors
                
                
if __name__ == "__main__":
    pass