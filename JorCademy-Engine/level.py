from settings import tile_size, screen_width
from jorcademy import *
from tile import StaticTile, MysteryBox
from loot import Coin, ExtraLife, FireMario
from link import Link
from support import import_level_data, import_tileset
from tile_data import *


class Level:

    def __init__(self, level_name):
        self.level_name = level_name
        self.tiles = []
        self.cam_pos = 0
        self.link = Link((100, 100), 32, 64)


    # Initialize level
    def setup(self, screen):

        self.screen = screen
        self.level_data = import_level_data(f"maps/level_{self.level_name}.csv")
        self.level_length = len(self.level_data[0] * tile_size)
        tileset = import_tileset("maps/tileset.png")

        # Initial y-coordinate of tile
        y = tile_size / 2

        # Read tiles into tiles list
        for j, row in enumerate(self.level_data):
        
            # Initial x-coordinate of tile
            x = tile_size / 2

            for i, tile in enumerate(row):
                pos = (x, y)

                # Treat different tiles correctly
                if tile == SKY_TILE:
                    sel_tile = tileset[int(tile)]
                    self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))
                
                elif tile == PLAYER_TILE:
                    sel_tile = tileset[0]
                    self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))
                    self.link.x = pos[0]
                    self.link.y = pos[1]

                elif tile == MYSTERY_BOX:
                    # Setup loot
                    loot_code = self.level_data[j + 1][i]
                    loot = self.init_loot(loot_code, tileset, pos)

                    # Setup tile
                    self.level_data[j + 1][i] = SKY_TILE
                    sel_tile = tileset[int(tile)]
                    alt_tile = tileset[int(EMPTY_BOX)]
                    self.tiles.append(MysteryBox(tile_size, pos, sel_tile, alt_tile, tile, loot))

                else:
                    sel_tile = tileset[int(tile)]
                    self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

                # Update tile x-coordinate
                x += tile_size 

            # Update tile y-coordinate
            y += tile_size        


    # Make loot object to be added to the world
    def init_loot(self, loot_code, tileset, pos):
        loot_tile = tileset[int(loot_code)]
        loot = None

        # Determine loot type
        if loot_code == COIN:
            loot = Coin(tile_size, pos, loot_tile, loot_code, self.link)
        elif loot_code == EXTRA_LIFE:
            loot = ExtraLife(tile_size, pos, loot_tile, loot_code, self.link)
        elif loot_code == FIRE_MARIO:
            loot = FireMario(tile_size, pos, loot_tile, loot_code, self.link)
        else:
            loot = Coin(tile_size, pos, loot_tile, loot_code, self.link)

        return loot


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

            # No collision when tile is part of backdrop
            if tile.code in BACKDROP_TILES:
                continue 

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

        for i, tile in enumerate(self.tiles):

            # No collision when tile is part of backdrop
            if tile.code in BACKDROP_TILES:
                continue 

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
                    player.direction.y = 0

                    # Handle collision with mystery box
                    if tile.code == MYSTERY_BOX:
                        try:
                            loot = tile.give_loot()
                            self.tiles.insert(i, loot)
                        except:
                            pass
            
    
    # Check whether shift of the tiles should be prevented
    def prevent_tile_shift(self):
        return (self.cam_pos <= 0 and self.link.direction.x < 0) or \
               (self.cam_pos >= (self.level_length - screen_width) and \
                self.link.direction.x > 0)


    # Update the state of the level
    def update(self):

        # == Player
        self.link.update(self.cam_pos, self.level_length)
        self.horizontal_collision()
        self.vertical_collision()

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