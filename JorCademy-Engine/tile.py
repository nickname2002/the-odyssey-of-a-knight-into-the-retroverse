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


    # Update the state of the tile
    def update(self, shift_x):
        self.x = self.orig_position[0] - shift_x 


    # Draw the tile
    def draw(self):
        rect(self.color, self.x, self.y, tile_size, tile_size)


class StaticTile(Tile):

    def __init__(self, size, pos, surface, code):
        super().__init__(size, pos)
        self.image = surface 
        self.code = code


    def draw(self, screen):
        screen.blit(self.image, (self.x - tile_size / 2, self.y - tile_size / 2))


class MysteryBox(StaticTile):

    def __init__(self, size, pos, surface, alt_surface, code, loot):
        super().__init__(size, pos, surface, code)
        self.loot = loot 
        self.alt_surface = alt_surface


    def give_loot(self, level):
        if self.image != self.alt_surface:
            self.image = self.alt_surface
            
            try:
                self.loot.show(level)
            except:
                pass 

        return self.loot
    

        

    