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


    def give_loot(self):
        if self.image != self.alt_surface:
            self.image = self.alt_surface
            self.loot.show()
        return self.loot
        

class Loot(StaticTile):
    
    def __init__(self, size, pos, surface, code):
        super().__init__(size, pos, surface, code)
        self.direction_y = 0
        self.activated = False
        self.speed = 1.5


    def show(self):
        self.activated = True
        self.direction_y = -self.speed

    
    def rise_animation(self):
        if self.activated and self.y > self.orig_position[1] - tile_size:
            self.y += self.direction_y
        else:
            self.direction_y = 0


    def update(self, shift_x):
        super().update(shift_x)
        self.rise_animation()




        

    