from settings import tile_size, screen_width, screen_height
from jorcademy import *
from tile import StaticTile, MysteryBox, MovingTile
from loot import Coin, ExtraLife, FireMario
from link import Link
from monster import Bokoblin
from support import import_level_data, import_tile_set
from tile_data import *


class Level:

    def __init__(self, level_name):
        # Properties
        self.level_length = None
        self.level_data = None
        self.screen = None
        self.level_name = level_name
        self.cam_pos = 0
        self.link = Link((100, screen_height / 2), 32, 64)
        self.backdrop_color = (147, 187, 236)

        # Collections
        self.tiles = []
        self.text_anomalies = []
        self.monsters = []

    # Initialize level
    def setup(self, screen):

        self.screen = screen
        self.level_data = import_level_data(f"maps/level_{self.level_name}.csv")
        self.level_length = len(self.level_data[0] * tile_size)
        tile_set = import_tile_set("maps/tileset.png")

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
                    pass

                elif tile == PLAYER_TILE:
                    sel_tile = tile_set[0]
                    self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))
                    self.link.x = pos[0]
                    self.link.y = pos[1]

                elif tile == MYSTERY_BOX:
                    # Setup loot
                    loot_code = self.level_data[j + 1][i]
                    loot = self.init_loot(loot_code, tile_set, pos)

                    # Setup tile
                    self.level_data[j + 1][i] = SKY_TILE
                    sel_tile = tile_set[int(tile)]
                    alt_tile = tile_set[int(EMPTY_BOX)]
                    self.tiles.append(MysteryBox(tile_size, pos, sel_tile, alt_tile, tile, loot))

                elif tile in MONSTERS:
                    self.init_monster(tile, pos)

                else:
                    sel_tile = tile_set[int(tile)]
                    self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

                # Update tile x-coordinate
                x += tile_size

                # Update tile y-coordinate
            y += tile_size

            # Make new monster object and add it to the list of monsters 

    def init_monster(self, tile_code, pos):
        if tile_code == BOKOBLIN:
            self.monsters.append(Bokoblin(pos, tile_size * 1.5, tile_size * 1.5, self.link, self))

    # Make loot object to be added to the world
    def init_loot(self, loot_code, tile_set, pos):
        loot_tile = tile_set[int(loot_code)]

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

    # Handle collision
    def handle_collision(self):
        for i, tile in enumerate(self.tiles):

            # No collision when tile is part of backdrop
            if tile.code in BACKDROP_TILES:
                continue

                # Moving tiles collision
            if issubclass(type(tile), MovingTile):
                tile.collision(self.tiles)

            # Monsters collision
            for monster in self.monsters:
                monster.handle_collision(tile, i, self)

            # Link collision
            self.link.handle_collision(tile, i, self)

    # Update text anomaly buffer
    def update_text_anomalies(self, new_anomaly=None):

        # Remove inactive text anomalies from buffer
        for msg in self.text_anomalies:
            if not msg.visible:
                self.text_anomalies.remove(msg)

                # Add new anomaly to buffer
        if new_anomaly is not None:
            self.text_anomalies.append(new_anomaly)

    # Check whether shift of the tiles should be prevented
    def prevent_tile_shift(self):
        return (self.cam_pos <= 0 and self.link.direction.x < 0) or \
               (self.cam_pos >= (self.level_length - screen_width) and
                self.link.direction.x > 0)

    def reset(self):
        # Properties
        self.cam_pos = 0

        # Reset link pos
        self.link.x = 100
        self.link.y = screen_height / 2

        # Collections
        self.tiles = []
        self.text_anomalies = []
        self.monsters = []

        # Execute setup again to reset map
        self.setup(self.screen)

    # Update the state of the level
    def update(self):
        # UI
        for msg in self.text_anomalies:
            msg.update()

        # == Player
        self.link.update(self.cam_pos, self.level_length)

        # == Monsters
        for monster in self.monsters:
            if monster.is_out_of_frame() or monster.killed:
                self.monsters.remove(monster)

            monster.update(self.cam_pos, self.level_length)

        # == Tiles
        if not self.prevent_tile_shift():
            self.world_shift()

        for tile in self.tiles:
            if tile.is_out_of_frame():
                self.tiles.remove(tile)
                continue

            tile.update(self.cam_pos)

        # Collision
        self.handle_collision()

    # Draw the state of the level
    def draw(self):

        # == Player 
        self.link.draw()

        # == Monsters
        for monster in self.monsters:
            if monster.in_frame():
                monster.draw()

        # == Tiles
        for tile in self.tiles:
            if tile.in_frame():
                tile.draw(self.screen)

        # == UI
        for message in self.text_anomalies:
            message.draw()

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             25,
             (255, 255, 255),
             100,
             25,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             25,
             (255, 255, 255),
             screen_width / 2 + 10,
             25,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             25,
             (255, 255, 255),
             screen_width / 2 + 300,
             25,
             "fonts/pixel.ttf")
