import random

import pyglet
from pyglet.gl import *

from Config import *
from Asset_loader import assets
def get_texture_coords(texture):

    return texture.tex_coords

class CustomGroup(pyglet.graphics.Group):
    def __init__(self):
        super().__init__()
        self.texture = pyglet.resource.get_texture_bins()[0].atlases[0].texture
        
    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

    def unset_state(self):
        glDisable(self.texture.target)

class Tile:
    def __init__(self,name,texture):
        """A class for tiles"""
        self.name = name
        self.texture = texture
        #self.texture_coords = texture
    
    @property
    def texture_coords(self):
        
        image =self.texture#assets[level[i][j]]
        n = max((image.width//TILE_SIZE),1)
        val = random.choices([i for i in range(n)],weights =[80-min(i,1)*65 for i in range(n)])[0]
        tile = image.get_region(val*TILE_SIZE,0,TILE_SIZE,TILE_SIZE)
        #print(tile.tex_coords)
        
        return tile.tex_coords
    


#GRASS = Tile("Grass",get_texture_coords(assets['Grass']))
#STONE = Tile("Stone",get_texture_coords(assets['Stone']))
#SAND = Tile("Sand",get_texture_coords(assets['Sand']))
#WATER = Tile("Water",get_texture_coords(assets['Water']))

GRASS = Tile("Grass",assets['Grass'])
STONE = Tile("Stone",assets['Stone'])
SAND = Tile("Sand",assets['Sand'])
WATER = Tile("Water",assets['Water'])



if __name__ == "__main__":
    print(GL_SRC_ALPHA)
    print(GL_ONE_MINUS_SRC_ALPHA)
    #GRASS.texture_coords
    #GRASS.texture_coords
    #GRASS.texture_coords
    #GRASS.texture_coords
    #print(get_texture_coords(assets["0"]))
    
