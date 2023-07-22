from settings import tile_size
from jorcademy import rect

class Tile:

    def __init__(self, color, pos):
        self.color = color
        self.orig_position = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = tile_size
        self.height = tile_size

    def draw(self):
        # TODO: change into picture
        rect(self.color, self.x, self.y, tile_size, tile_size)

    def update(self, shift_x):
        self.x = self.orig_position[0] - shift_x 
        self.y = self.orig_position[1]
