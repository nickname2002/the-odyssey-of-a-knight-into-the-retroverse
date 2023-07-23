from settings import tile_size, screen_width
from jorcademy import *
from tile import Tile, StaticTile
from link import Link
from support import import_level_data, import_tileset


class Level:

    # TODO: Make sure levels can be imported
    def __init__(self, level_name):
        self.level_name = level_name
        self.tiles = []
        self.cam_pos = 0
        self.link = Link((100, 100), 20, 40)


    # Initialize level
    def setup(self, screen):

        self.screen = screen
        self.level_data = import_level_data(f"maps/level_{self.level_name}.csv")
        self.level_length = len(self.level_data[0] * tile_size)
        tileset = import_tileset("maps/tileset.png")

        # Initial y-coordinate of tile
        y = tile_size / 2

        # Read tiles into tiles list
        for row in self.level_data:
        
            # Initial x-coordinate of tile
            x = tile_size / 2

            for tile in row:
                pos = (x, y)

                # Treat different tiles correctly
                if tile != "-1":
                    sel_tile = tileset[int(tile)]
                    self.tiles.append(StaticTile((100, 100, 100), pos, sel_tile))
                else:
                    self.link.x = pos[0]
                    self.link.y = pos[1]

                # Update tile x-coordinate
                x += tile_size 

            # Update tile y-coordinate
            y += tile_size


    # Update the camera position
    def world_shift(self):
        if is_key_down("d") and self.link.x >= screen_width / 2:
            self.cam_pos += self.link.speed
        if is_key_down("a") and self.link.x <= screen_width / 4 and self.cam_pos > 0:         
            self.cam_pos -= self.link.speed


    # Change horizontal collision of player with the map
    def horizontal_collision(self):
        player = self.link

        for tile in self.tiles:

            # Handle collision on left side of Link
            if player.collision_left(tile):
                if player.direction.x < 0:
                    player.x = tile.x + tile.width / 2 + player.width / 2
            
            # Handle collision on right side of Link
            elif player.collision_right(tile):
                if player.direction.x > 0:
                    player.x = tile.x - tile.width / 2 - player.width / 2


    # Change vertical collision of player with the map
    def vertical_collision(self):
        player = self.link
        player.apply_gravity()

        for tile in self.tiles:

            # Handle collision on bottom side of Link
            if player.collision_bottom(tile):
                if player.direction.y > 0:
                    player.y = tile.y - tile.height / 2 - player.height / 2
                    player.direction.y = 0
                    
                player.is_grounded = True

            # Handle collision on top side of Link
            elif player.collision_top(tile):
                if player.direction.y < 0:
                    player.y = tile.y + tile.height / 2 + player.height / 2
            
    
    # Check whether shift of the tiles should be prevented
    def prevent_tile_shift(self):
        return (self.cam_pos <= 0 and self.link.direction.x < 0) or \
               (self.cam_pos >= (self.level_length - screen_width) and \
                self.link.direction.x > 0)


    # Update the state of the level
    def update(self):
        # == Player
        self.link.update(self.cam_pos, self.level_length)
        #self.horizontal_collision()
        #self.vertical_collision()

        # == Tiles
        if not self.prevent_tile_shift():
            self.world_shift()

        for tile in self.tiles:
            tile.update(self.cam_pos)


    # Draw the state of the level
    def draw(self):
        self.link.draw()
        for tile in self.tiles:
            tile.draw(self.screen)