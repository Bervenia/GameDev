import pyglet
from pyglet import gl
from Config import ASSET_PATH


pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
pyglet.resource.path = [".",ASSET_PATH]
pyglet.resource.reindex()
        
    
def load_image(file_name, center = False,):
    image = pyglet.resource.image(file_name)
    
    if center:
        image = center_image(image)
    return image

def load_animation(file_name,center = False,duration = None):
    image = pyglet.resource.animation(file_name)
    
    if center:
        image = center_animation(image,duration)
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    return image

def center_animation(animation,duration = None):
    """center animation frames anchor"""
    for i in range(len(animation.frames)):
        animation.frames[i].image = center_image(animation.frames[i].image)
        if duration:
            animation.frames[i].duration = duration
    return animation
    
def center_image(image):
    """Sets an image's achor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

assets = {}
assets['Grass'] = pyglet.image.TextureGrid(pyglet.image.ImageGrid(load_image("Grassx64.png",True),2,5))
assets['Grass2Sand'] = pyglet.image.TextureGrid(pyglet.image.ImageGrid(load_image("GrasstoSand.png",True),6,8))
assets['Grass2Stone'] = pyglet.image.TextureGrid(pyglet.image.ImageGrid(load_image("GrasstoStone.png",True),6,8))
assets['Sand'] = load_image("Sandx64.png",True)
assets['Sand2Stone'] = pyglet.image.TextureGrid(pyglet.image.ImageGrid(load_image("SandtoStone.png",True),6,8))
assets['Stone'] = load_image("Stonex64.png",True)
assets['Water'] = load_image("Waterx64.png",True)


       



            