from settings import tile_size, screen_width, screen_height
from jorcademy import *
from triforce import Triforce
from tile import StaticTile, MysteryBox, MovingTile, BreakableTile
from loot import Coin, ExtraLife, FireFlower
from link import Link
from monster import Bokoblin
from support import import_level_data, import_tile_set
from tile_data import *
import threading


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
        self.end_game_triforce = None

        # Collections
        self.tiles = []
        self.text_anomalies = []
        self.monsters = []

    def init_tile(self, tile, tile_set, pos, i, j):

        # Initialize player
        if tile == PLAYER_TILE:
            sel_tile = tile_set[0]
            self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))
            self.link.x = pos[0]
            self.link.y = pos[1]

        # Initialize mystery boxes
        elif tile == MYSTERY_BOX:
            # Setup loot
            loot_code = self.level_data[j + 1][i]
            loot = self.init_loot(loot_code, tile_set, pos)

            # Setup tile
            self.level_data[j + 1][i] = SKY_TILE
            sel_tile = tile_set[int(tile)]
            alt_tile = tile_set[int(EMPTY_BOX)]
            self.tiles.append(MysteryBox(tile_size, pos, sel_tile, alt_tile, tile, loot))

        # Initialize monsters
        elif tile in MONSTERS:
            self.init_monster(tile, pos)

        # Initialize breakable tiles
        elif tile in BREAKABLE:
            sel_tile = tile_set[int(tile)]
            alt_tile = tile_set[int(SKY_TILE)]
            self.tiles.append(BreakableTile(tile_size, pos, sel_tile, alt_tile, tile))

        # Initialize end of game
        elif tile == END_OF_GAME:
            # Make end-of-game
            self.end_game_triforce = Triforce((pos[0], 230), 481, 371, self.link)

            # Make sky tile
            sel_tile = tile_set[int(SKY_TILE)]
            self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

        # Initialize normal static tiles
        else:
            sel_tile = tile_set[int(tile)]
            self.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

    def transition_requested(self):
        return self.link.killed or self.end_game_triforce.reached

    # Initialize level
    def setup(self, screen):

        self.screen = screen
        self.backdrop_color = (147, 187, 236)
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

                # Treat different tiles correctly
                self.init_tile(tile, tile_set, pos, i, j)

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
            loot = FireFlower(tile_size, pos, loot_tile, loot_code, self.link)
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

    # Check whether shift of the tiles should be prevented
    def prevent_tile_shift(self):
        return (self.cam_pos <= 0 and self.link.direction.x < 0) or \
               (self.cam_pos >= (self.level_length - screen_width) and
                self.link.direction.x > 0)

    def reset(self):
        # Properties
        self.cam_pos = 0

        # Reset link
        self.link.x = 100
        self.link.y = screen_height / 2
        self.link.killed = False

        # Collections
        self.tiles = []
        self.text_anomalies = []
        self.monsters = []

        # Execute setup again to reset map
        self.setup(self.screen)

    # Update text anomaly buffer
    def update_text_anomalies(self, new_anomaly=None):

        # Add new anomaly to buffer
        if new_anomaly is not None:
            self.text_anomalies.append(new_anomaly)

        # Remove inactive text anomalies from buffer
        for msg in self.text_anomalies:
            if not msg.visible:
                self.text_anomalies.remove(msg)
                continue

            msg.update()

    def update_monsters(self):
        for monster in self.monsters:
            if monster.is_out_of_frame() or monster.killed:
                self.monsters.remove(monster)

            monster.update(self.cam_pos, self.level_length)

    def update_tiles(self):
        for tile in self.tiles:
            if tile.is_out_of_frame():
                self.tiles.remove(tile)
                continue

            tile.update(self.cam_pos)

    # Update the state of the level
    def update(self):

        # TODO: Handle end of level reached (properly)
        if self.end_game_triforce.reached:
            self.reset()

        # Create threads
        update_monsters_thread = threading.Thread(target=self.update_monsters)
        update_tiles_thread = threading.Thread(target=self.update_tiles)
        update_text_anomalies_thread = threading.Thread(target=self.update_text_anomalies)

        # == Player
        self.link.update(self.cam_pos, self.level_length, self.end_game_triforce.reached)

        if not self.prevent_tile_shift():
            self.world_shift()

        # Update tiles and monsters in parallel
        update_monsters_thread.start()
        update_tiles_thread.start()
        update_text_anomalies_thread.start()
        update_monsters_thread.join()
        update_monsters_thread.join()
        update_text_anomalies_thread.join()

        # Other
        self.end_game_triforce.update(self.cam_pos, self.level_length)

        # Collision
        self.handle_collision()

    def draw_monsters(self):
        for monster in self.monsters:
            if monster.in_frame():
                monster.draw()

    def draw_tiles(self):
        for tile in self.tiles:
            if tile.in_frame():
                tile.draw(self.screen)

    def draw_text_anomalies(self):
        for message in self.text_anomalies:
            message.draw()

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

        # == Text anomalies
        for message in self.text_anomalies:
            message.draw()

        # == Other
        self.end_game_triforce.draw()

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
