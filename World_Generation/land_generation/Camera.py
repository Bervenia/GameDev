import pyglet
class Camera:
    """ A simple 2D camera that contains the speed and offset."""

    def __init__(self,screen_size, scroll_speed=1, max_zoom=4):
        self.scroll_speed = scroll_speed
        self.max_zoom = max_zoom
        self.offset_x = 0
        self.offset_y = 0
        self._zoom = 1
        self.attached_entity = None
        self.screen = screen_size
        self.half_screen = (self.screen[0]/2,self.screen[1]/2)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """ Here we set zoom, clamp value to minimum of 1 and max of max_zoom."""
        self._zoom = max(min(value, self.max_zoom), 1)

    @property
    def position(self):
        """Query the current offset."""
        return self.offset_x, self.offset_y

    @position.setter
    def position(self, value):
        """Set the scroll offset directly."""
        print(self.attached_entity)
        if self.attached_entity != None:
            self.offset_x = int(self.attached_entity.position.x - self.half_screen[0])
            self.offset_y = int(self.attached_entity.position.y - self.half_screen[1])
        else:
            print("value", value,value[0] - self.half_screen[0],value[1] - self.half_screen[1] )
            self.offset_x = int(value[0]+self.offset_x - self.half_screen[0])
            self.offset_y = int(value[1]+self.offset_y - self.half_screen[1])
    def attach(self,entity):
        """Attach the camera to a entity.
        
        Arguments:
            self -- [camera class instance]
            entity -- [entity object]
        """
        self.attached_entity = entity
    def update(self):
        """Update camera class to attached entity position
        """
        if self.attached_entity != None:
            self.offset_x = int(self.attached_entity.position.x - self.half_screen[0])
            self.offset_y = int(self.attached_entity.position.y - self.half_screen[1])

    def move(self, axis_x, axis_y):
        """ Move axis direction with scroll_speed.
            Example: Move left -> move(-1, 0)
         """
        self.offset_x += self.scroll_speed * axis_x
        self.offset_y += self.scroll_speed * axis_y

    def begin(self):
        # Set the current camera offset so you can draw your scene.
        # Translate using the zoom and the offset.
        pyglet.gl.glTranslatef(-self.offset_x * self._zoom, -self.offset_y * self._zoom, 0)

        # Scale by zoom level.
        pyglet.gl.glScalef(self._zoom, self._zoom, 1)

    def end(self):
        # Since this is a matrix, you will need to reverse the translate after rendering otherwise
        # it will multiply the current offset every draw update pushing it further and further away.

        # Reverse scale, since that was the last transform.
        pyglet.gl.glScalef(1 / self._zoom, 1 / self._zoom, 1)

        # Reverse translate.
        pyglet.gl.glTranslatef(self.offset_x * self._zoom, self.offset_y * self._zoom, 0)

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()