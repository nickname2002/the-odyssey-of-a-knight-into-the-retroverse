from settings import tile_size
from jorcademy import rect, image

class Tile:

    def __init__(self, color, pos):
        self.color = color
        self.orig_position = pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = tile_size
        self.height = tile_size


    # Update the state of the tile
    def update(self, shift_x):
        self.x = self.orig_position[0] - shift_x 
        self.y = self.orig_position[1]


    # Draw the tile
    def draw(self):
        rect(self.color, self.x, self.y, tile_size, tile_size)


class StaticTile(Tile):

    def __init__(self, size, pos, surface):
        super().__init__(size, pos)
        self.image = surface 

    def draw(self, screen):
        screen.blit(self.image, (self.x - tile_size / 2, self.y - tile_size / 2))