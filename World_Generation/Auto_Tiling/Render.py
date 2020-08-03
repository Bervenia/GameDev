import pyglet
from random import randint
#import cardspritev2 as sprite
class Render():
    def __init__(self,game):
        self.game = game
        self.level = 'test.txt'
        self.chunk_size = 8
        self.tile_size = 64
        self.map = self.get_chunks()
        self.map_draw = self.get_chunk_image()
        
       

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

    def get_chunks(self):
        """splits the 2d tilemap list into smaller sub-chuncks

        Returns:
            [type] -- 3d list x,y for chunk z for tile
        """
        level = self.get_level()
        #print(len(level),len(level[0]))
        chunk_list = [[[] for j in range(len(level[0])//self.chunk_size)] for i in range(len(level)//self.chunk_size)]
        #print(chunk_list)
        for i in range(len(level)):
            for j in range(len(level[0])):
                chunk_list[i//self.chunk_size][j//self.chunk_size].append(level[i][j])
        #print(chunk_list)
        return chunk_list

    def get_chunk_image(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        level = self.get_level()
        chunk_img_list = [[[] for j in range(len(level[0])//self.chunk_size)] for i in range(len(level)//self.chunk_size)]
        level = self.get_chunks()
        #print(level)
        for i in range(len(level)):
            for j in range(len(level[0])):
                chunk_img_list[i][j] = pyglet.image.Texture.create(width = self.tile_size*self.chunk_size, height =self.tile_size*self.chunk_size)
                for k in range(len(level[0][0])):
                    
                    image =  self.game.assets[level[i][j][k]]
                    if level[i][j][k] == '2':
                        image  = image.get_region(self.tile_size*(randint(0,3)),0,self.tile_size,self.tile_size)
                    chunk_img_list[i][j].blit_into(image,(k %self.chunk_size)* self.tile_size,abs((k //self.chunk_size))* self.tile_size,0)
        print(chunk_img_list)
        #chunk_img_list = self.auto_tile_all(chunk_img_list)
        for i in range(len(chunk_img_list)):
            for j in range(len(chunk_img_list[0])):
                chunk_img_list[i][j] = pyglet.resource.get_texture_bins()[-1].add(chunk_img_list[i][j].get_image_data())
        return chunk_img_list

    def neighbors(self,d,x,y,i,v,l):
        w = l
        h = l
        size = w * h
        neighbors = []
        temp = -1
        if d == 0:
            if i % w != 0 and self.map[y][x][i-1] > v:
                neighbors.append(self.map[y][x][i-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if i + w < size and self.map[y][x][i+w] > v:
                neighbors.append(self.map[y][x][i+w])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and ((i + w - 1) < size) and (i % w != 0) and self.map[y][x][i+w-1] > v:
                neighbors.append(self.map[y][x][i+w-1])  # southwest
                temp += 4
            else:
                neighbors.append(None)
        if d == 1:
            if (i + 1) % w != 0 and self.map[y][x][i+1] > v:
                neighbors.append(self.map[y][x][i+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if i + w < size and self.map[y][x][i+w] > v:
                neighbors.append(self.map[y][x][i+w])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and ((i + w + 1) < size) and ((i + 1) % w != 0) and self.map[y][x][i+w+1] > v:
                neighbors.append(self.map[y][x][i+w+1])  # southeast
                temp += 4
            else:
                #print((i + w + 1) < size, ((i + 1) % w != 0))
                neighbors.append(None)
        if d == 2:
            if i % w != 0 and self.map[y][x][i-1] > v:
                neighbors.append(self.map[y][x][i-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if i - w >= 0 and self.map[y][x][i-w] > v:
                neighbors.append(self.map[y][x][i-w])  # north
                temp += 2
            else:
                neighbors.append(None)

            
            if temp == -1 and ((i - w - 1) >= 0) and (i % w != 0) and self.map[y][x][i-w-1] > v:
                neighbors.append(self.map[y][x][i-w-1])  # northwest
                temp += 4
            else:
                neighbors.append(None)
        if d == 3:
            if (i + 1) % w != 0 and self.map[y][x][i+1] > v :
                neighbors.append(self.map[y][x][i+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if i - w >= 0 and self.map[y][x][i-w] > v:
                neighbors.append(self.map[y][x][i-w])  # north
                temp += 2
            else:
                neighbors.append(None)  
            if temp == -1 and ((i - w + 1) >= 0) and ((i + 1) % w != 0) and self.map[y][x][i-w+1] > v:
                neighbors.append(self.map[y][x][i-w+1])  # northeast
                temp += 4
            else:
                neighbors.append(None)

                
        
        
        temp = min(temp,3)
        neighbors.append(temp)
        return neighbors

    def sub_tile(self, image_data, x,y,z):
        sel = int()
        print(image_data)
        for i in range(4):
            temp = i
            sub_tile_value = self.neighbors(i,y,x,z,self.map[x][y][z],self.chunk_size)

            if sub_tile_value[-1] != -1:
                if sub_tile_value[0] == None or sub_tile_value[1] == None:
                    
                    sub_tile = self.game.assets[max([i for i in sub_tile_value[:-1] if i is not None])].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),64+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                elif sub_tile_value[0] != None and sub_tile_value[1] != None:#vert and horizontal
                    if sub_tile_value[0] >= sub_tile_value[1]:
                        sub_tile = self.game.assets[sub_tile_value[0]].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),64+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                    else:
                        sub_tile = self.game.assets[sub_tile_value[1]].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),64+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                image = image_data[x][y].get_region(self.tile_size*(z%self.chunk_size),self.tile_size*(z//self.chunk_size),self.tile_size,self.tile_size)
                original = image.get_image_data()
                image.blit_into(sub_tile,(self.tile_size//2*((i)%2)),(self.tile_size//2*((3-i)//2)),0)
                
                sub_tile = self.blend_transparent(image,original)

                #image_data[x][y].blit_into(sub_tile,self.tile_size*(z%self.chunk_size)+(self.tile_size//2*((i)%2)),self.tile_size*(z//self.chunk_size)+(self.tile_size//2*((3-i)//2)),0)
                image_data[x][y].blit_into(sub_tile,self.tile_size*(z%self.chunk_size),self.tile_size*(z//self.chunk_size),0)
                #image_data[x][y].blit_into(sub_tile,0,0,0)
        return image_data[x][y]

    def auto_tile_all(self,image_data):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                for k in range(len(self.map[0][0])):
                    #print(image_data[i][j])
                    image_data[i][j] = self.sub_tile(image_data,i,j,k)
        return image_data
    def blend_transparent(self,image,original):
        img_data = image.get_image_data()
        fmt_1 = img_data.format
        original_data = original.get_image_data()
        fmt_2 = original_data.format
        assert fmt_1 == fmt_2,\
            f"Both images must have the same format. Current {fmt_1}, {fmt_2}"
        
        def chunker(data_1,data_2, length):
            colors_1 = [iter(data_1)] * length
            colors_2 = [iter(data_2)] * length
            return zip(*colors_1,*colors_2)

        orig_raw_bytes = original_data.get_data()
        img_raw_bytes = img_data.get_data()
        new_array = []
        for pixels in chunker(img_raw_bytes,orig_raw_bytes,len(fmt_1)):
            if pixels[3] == 0 and pixels[-1] == 255:
                new_array.extend(pixels[4:8])
            else:
                new_array.extend(pixels[:4])
            
        img_data.set_data(img_data.format, 0, bytes(new_array))
        image.blit_into(img_data, 0, 0, 0)
        return image.get_image_data()

    def draw(self,mode = False):
        self.temp = []
        #print(self.map_draw[0][0])
        for i in range(len(self.map_draw)):
            for j in range(len(self.map_draw[0])):
                x = (j*self.chunk_size*self.tile_size+self.game.width/2)
                y = (i*self.chunk_size*self.tile_size+self.game.height/2)
                width = self.chunk_size*self.tile_size
                height = self.chunk_size*self.tile_size
                if mode == False:
                    self.temp.append(pyglet.sprite.Sprite(img = self.map_draw[i][j],x= x, y = y, batch = self.game.bg_batch))
                else:
                    self.auto_draw = self.auto_tile_all(self.map_draw.copy())
                    self.temp.append(pyglet.sprite.Sprite(img = self.auto_draw[i][j],x= x, y = y, batch = self.game.bg_batch))
                



if __name__ == "__main__":
    test = Render("test")
    level = test.get_chunks()
    print(test.neighbors(5,1,0,0,4,4))
    #print(test.get_chunks())
