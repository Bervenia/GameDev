import pyglet
from random import randint
import os
#import cardspritev2 as sprite
class Render():
    def __init__(self,game):
        self.game = game
        self.level = './directions/30.txt'
        self.chunk_size = 16
        self.tile_size = 32
        self.sprite_name = 'GrasstoStonex32.png'
        self.sheet = self.sprite_sheet()


        #self.map = self.flatten(self.get_level())
        #self.single_tile = self.get_sub()

    def order_files(self,files):
        temp  = [] 
        print(len(temp))
        while len(temp) != len(files):
            for file in files:
                print(file.split('.'))
                if int(file.split('.')[0]) == len(temp):
                    temp.append(os.path.join("./directions",file))

        return temp
    def sprite_sheet(self):
        files = [f for f in os.listdir('./directions') if os.path.isfile(os.path.join("./directions",f))]
        files = self.order_files(files)
        temp = []
        sheet = pyglet.image.Texture.create(width = self.tile_size*8, height =self.tile_size*6)
        print("sheet",sheet.width,sheet.height)
        for file in files:
            self.level = file
            self.map = self.flatten(self.get_level())
                
            #print(self.level)           
            level = self.get_level()
            #print(file)
            for i in range(len(level)):
                for j in range(len(level[0])):
                    if j+i*3 == 4:
                        self.game.assets = self.game.asset_loader.load()
                        image = self.game.assets[level[i][j]]
                        print("image",image.width,image.height)
                        if level[i][j] == '1':
                                image = image.get_region(self.tile_size*(randint(0,3)),0,self.tile_size,self.tile_size)

                        new_image =self.sub(image.get_texture(),j+i*3)
                        if new_image[1] == 4:

                            #print((len(temp) %8),abs((len(temp)//8)),len(temp),file)
                            #if abs((len(temp)//5)) != 8:
                            print(new_image[0].width,new_image[0].height)
                            sheet.blit_into(new_image[0],((len(temp) %8) * self.tile_size),abs((len(temp)//8))* self.tile_size,0)
                            temp.append('1')
                            #sheet = pyglet.resource.get_texture_bins()[-1].add(sheet.get_image_data())
        sheet.save(self.sprite_name)
        return sheet
    def flatten(self,level):
        new = []
        for i in range(len(level)):
            for j in range(len(level[0])):
                new.append(level[i][j])
        return new
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
    def new_neighbors(self,d,i,v,l):
        w = l
        h = l
        size = w * h
        neighbors = []
        temp = -1
        if d == 0:
            if i % w != 0 and self.map[i-1] > v:
                neighbors.append(self.map[i-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if i + w < size and self.map[i+w] > v:
                neighbors.append(self.map[i+w])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and ((i + w - 1) < size) and (i % w != 0) and self.map [i+w-1] > v:
                neighbors.append(self.map[i+w-1])  # southwest
                temp += 4
            else:
                neighbors.append(None)
        if d == 1:
            if (i + 1) % w != 0 and self.map[i+1] > v:
                neighbors.append(self.map[i+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if i + w < size and self.map[i+w] > v:
                neighbors.append(self.map[i+w])  # south
                temp += 2
            else:
                neighbors.append(None)
            if temp == -1 and ((i + w + 1) < size) and ((i + 1) % w != 0) and self.map[i+w+1] > v:
                neighbors.append(self.map[i+w+1])  # southeast
                temp += 4
            else:
                #print((i + w + 1) < size, ((i + 1) % w != 0))
                neighbors.append(None)
        if d == 2:
            if i % w != 0 and self.map[i-1] > v:
                neighbors.append(self.map[i-1])  # west
                temp += 1
            else:
                neighbors.append(None)
            if i - w >= 0 and self.map[i-w] > v:
                neighbors.append(self.map[i-w])  # north
                temp += 2
            else:
                neighbors.append(None)

            
            if temp == -1 and ((i - w - 1) >= 0) and (i % w != 0) and self.map[i-w-1] > v:
                neighbors.append(self.map[i-w-1])  # northwest
                temp += 4
            else:
                neighbors.append(None)
        if d == 3:
            if (i + 1) % w != 0 and self.map[i+1] > v :
                neighbors.append(self.map[i+1])  # east
                temp += 1
            else:
                neighbors.append(None)
            if i - w >= 0 and self.map[i-w] > v:
                neighbors.append(self.map[i-w])  # north
                temp += 2
            else:
                neighbors.append(None)  
            if temp == -1 and ((i - w + 1) >= 0) and ((i + 1) % w != 0) and self.map[i-w+1] > v:
                neighbors.append(self.map[i-w+1])  # northeast
                temp += 4
            else:
                neighbors.append(None)

                
        
        
        temp = min(temp,3)
        neighbors.append(temp)
        return neighbors
    def sub(self, image_data,y):
        image_data = image_data.get_texture()
        print(image_data.width,image_data.height,"here")
        sel = int()
        #print(y,self.map[y],self.chunk_size)
        for i in range(4):
            temp = i
            #f,d,i,v,l
            sub_tile_value = self.new_neighbors(i,y,self.map[y],3)
          #  if y==4:
         #       print(sub_tile_value)
            if sub_tile_value[-1] != -1 :
                if sub_tile_value[0] == None or sub_tile_value[1] == None:
                    
                    sub_tile = self.game.assets[max([i for i in sub_tile_value[:-1] if i is not None])].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),32+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                elif sub_tile_value[0] != None and sub_tile_value[1] != None:#vert and horizontal
                    if sub_tile_value[0] >= sub_tile_value[1]:
                        sub_tile = self.game.assets[sub_tile_value[0]].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),32+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                    else:
                        sub_tile = self.game.assets[sub_tile_value[1]].get_region(self.tile_size*sub_tile_value[-1]+(self.tile_size//2*(i%2)),32+(self.tile_size//2*((i)//2)),self.tile_size//2,self.tile_size//2)
                image = image_data
                #print("here",image.width,image.height,sub_tile.width,sub_tile.height)
                original = image.get_image_data()
                image.blit_into(sub_tile,(self.tile_size//2*((i)%2)),(self.tile_size//2*((3-i)//2)),0)
                image = image.get_texture()
                sub_tile = self.blend_transparent(image,original)

                #image_data[x][y].blit_into(sub_tile,self.tile_size*(z%self.chunk_size)+(self.tile_size//2*((i)%2)),self.tile_size*(z//self.chunk_size)+(self.tile_size//2*((3-i)//2)),0)
                image_data.blit_into(sub_tile,0,0,0)
                #image_data[x][y].blit_into(sub_tile,0,0,0)
        return [image_data.get_image_data(),y]
  

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
        
        if mode == False:
            self.temp.append(pyglet.sprite.Sprite(img = self.sheet,x= 0, y = 0, batch = self.game.bg_batch))
                


if __name__ == "__main__":
    test = Render("test")
    level = test.sprite_sheet()
    #print(test.neighbors(5,1,0,0,4,4))
    #print(test.get_chunks())
