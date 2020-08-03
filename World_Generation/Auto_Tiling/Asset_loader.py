import pyglet
from pyglet import gl

class Asset_Loader():
    def __init__(self,Asset_location):
        pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
        pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
        pyglet.resource.path = [".",Asset_location]
        pyglet.resource.reindex()
    
    def load_image(self,file_name,center_image=False,):
        image = pyglet.resource.image(file_name)
        
        if center_image:
           image = self.center_image(image)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        return image

    def load_animation(self,file_name,center_animation = False,duration = None):
        image = pyglet.resource.animation(file_name)
        
        if center_animation:
            image = self.center_animation(image,duration)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        return image

    def center_animation(self,animation,duration = None):
        """center animation frames anchor"""
        for i in range(len(animation.frames)):
           animation.frames[i].image = self.center_image(animation.frames[i].image)
           if duration:
            animation.frames[i].duration = duration
        return animation
        
    def center_image(self,image):
        """Sets an image's achor point to its center"""
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        return image

    def load(self):
        pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
        pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
        assets = {}
        
        assets['1'] = self.load_image("Grassx64.png",True).get_image_data() 
        #assets['0'] = self.load_image("Stonex64.png",True).get_image_data() 
        assets['01'] = self.load_image("GrasstoSand.png",True).get_image_data() 
        assets['0'] = self.load_image("Sandx64.png",True).get_image_data()


       


        return assets
            