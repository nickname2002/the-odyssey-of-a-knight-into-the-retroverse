from Support.settings import tile_size, screen_width, screen_height
from jorcademy import *
from Level.chunk import Chunk
from Level.triforce import Triforce
from Level.tile import StaticTile, MysteryBox, MovingTile, BreakableTile
from Loot.fire_flower import FireFlower
from Loot.coin import Coin
from Loot.extra_life import ExtraLife
from Loot.cherry import Cherry
from GameObject.Link.link import Link
from GameObject.Monster.bokoblin import Bokoblin
from GameObject.Monster.ghost import Ghost
from Support.support import import_level_data, import_tile_set
from Level.tile_data import *


class Level:

    def __init__(self, level_name, chunk_amount):
        # Properties
        self.level_length = None
        self.level_data = None
        self.screen = None
        self.level_name = level_name
        self.cam_pos = 0
        self.link = Link((100, screen_height / 2), 32, 64)
        self.backdrop_color = (147, 187, 236)
        self.end_game_triforce = None
        self.chunk_amount = chunk_amount
        self.chunk_size = None

        # Collections
        self.chunks = []

    def init_tile(self, tile, tile_set, pos, i, j, chunk):

        # Initialize player
        if tile == PLAYER_TILE:
            sel_tile = tile_set[0]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))
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
            chunk.tiles.append(MysteryBox(tile_size, pos, sel_tile, alt_tile, tile, loot))

        # Initialize monsters
        elif tile in MONSTERS:
            self.init_monster(tile, pos, chunk)

        # Initialize breakable tiles
        elif tile in BREAKABLE:
            sel_tile = tile_set[int(tile)]
            alt_tile = tile_set[int(SKY_TILE)]
            chunk.tiles.append(BreakableTile(tile_size, pos, sel_tile, alt_tile, tile))

        # Initialize end of game
        elif tile == END_OF_GAME:
            # Make end-of-game
            self.end_game_triforce = Triforce((pos[0], 230), 481, 371, self.link)

            # Make sky tile
            sel_tile = tile_set[int(SKY_TILE)]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

        # Initialize normal static tiles
        else:
            sel_tile = tile_set[int(tile)]
            chunk.tiles.append(StaticTile(tile_size, pos, sel_tile, tile))

    def init_link(self, new_link):
        self.link = new_link

    def transition_requested(self):
        return self.link.killed or self.end_game_triforce.reached

    def init_chunks(self):
        self.chunk_size = round(self.level_length / self.chunk_amount)  # Maybe we can determine this automatically

        for i in range(self.chunk_amount):
            chunk_end = (i + 1) * self.chunk_size

            # Make sure last chunk is not too long
            if chunk_end > self.level_length:
                chunk_end = self.level_length

            # Make chunk
            self.chunks.append(Chunk(i * self.chunk_size, chunk_end))

    # Determine chunk the player is currently in
    def get_current_chunk(self):
        for chunk in self.chunks:
            if chunk.start <= self.link.x + self.cam_pos <= chunk.end:
                return chunk

    # Determine the chunks to draw
    def get_chunks_to_draw(self):
        chunks_to_draw = []

        # Determine the chunks to draw
        for i, chunk in enumerate(self.chunks):
            if chunk.start < self.link.x + self.cam_pos + screen_width and \
               not chunk.end < self.link.x + self.cam_pos - screen_width:
                chunks_to_draw.append(chunk)

        return chunks_to_draw

    # Initialize level
    def setup(self, game_screen):

        self.screen = game_screen
        self.backdrop_color = (147, 187, 236)
        self.level_data = import_level_data(f"Maps/level_{self.level_name}.csv")
        self.level_length = len(self.level_data[0] * tile_size)
        self.init_chunks()
        tile_set = import_tile_set("Maps/tileset.png")

        # Initial y-coordinate of tile
        y = tile_size / 2

        # Read tiles into tiles list
        for j, row in enumerate(self.level_data):

            # Initial x-coordinate of tile
            x = tile_size / 2

            # Current chunk index
            current_chunk_index = 0

            for i, tile in enumerate(row):
                pos = (x, y)

                if x > self.chunks[current_chunk_index].end:
                    current_chunk_index += 1

                # Treat different tiles correctly
                if tile == SKY_TILE:
                    pass

                # Treat different tiles correctly
                self.init_tile(tile, tile_set, pos, i, j, self.chunks[current_chunk_index])

                # Update tile x-coordinate
                x += tile_size

            # Update tile y-coordinate
            y += tile_size

        # Print chunk properties
        for chunk in self.chunks:
            print(chunk.start, chunk.end)

    # Make new monster object and add it to the list of monsters
    def init_monster(self, tile_code, pos, chunk):
        if tile_code == BOKOBLIN:
            chunk.monsters.append(Bokoblin(pos, tile_size * 1.5, tile_size * 1.5, self.link, self))
        elif tile_code == GHOST:
            chunk.monsters.append(Ghost(pos, 48, 48, self.link, self))

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
        elif loot_code == PAC_MAN:
            loot = Cherry(tile_size, pos, loot_tile, loot_code, self.link)
        else:
            loot = Coin(tile_size, pos, loot_tile, loot_code, self.link)

        return loot

    # Update the camera position
    def world_shift(self):
        if is_key_down("d") and self.link.x >= screen_width / 2:
            self.cam_pos += self.link.speed

    # Handle collision
    def handle_collision(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for i, tile in enumerate(chunk.tiles):

                # No collision when tile is part of backdrop
                if tile.code in BACKDROP_TILES:
                    continue

                # Moving tiles collision
                if issubclass(type(tile), MovingTile):
                    tile.collision(chunk.tiles)

                # Monsters collision
                for monster in chunk.monsters:
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
        self.chunks = []

        # Execute setup again to reset map
        self.setup(self.screen)

    # Update text anomaly buffer
    def update_text_anomalies(self, new_anomaly=None):
        chunks_to_draw = self.get_chunks_to_draw()
        current_chunk = self.get_current_chunk()

        # Add new anomaly to buffer
        if new_anomaly is not None:
            current_chunk.text_anomalies.append(new_anomaly)

        for chunk in chunks_to_draw:

            # Remove inactive text anomalies from buffer
            for msg in chunk.text_anomalies:
                if not msg.visible:
                    chunk.text_anomalies.remove(msg)
                    continue

                msg.update()

    def update_monsters(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for monster in chunk.monsters:
                if monster.is_out_of_frame() or monster.killed:
                    chunk.monsters.remove(monster)
                monster.update(self.cam_pos, self.level_length)

    def update_tiles(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for tile in chunk.tiles:
                if tile.is_out_of_frame():
                    chunk.tiles.remove(tile)
                    continue

                tile.update(self.cam_pos)

    # Update the state of the level
    def update(self):
        if self.end_game_triforce.reached:
            self.reset()

        # Update chunks to draw
        chunks_to_draw = self.get_chunks_to_draw()
        for chunk in chunks_to_draw:
            chunk.update(self.cam_pos, self.level_length)

        # == Player
        self.link.update(self.cam_pos, self.level_length, self.end_game_triforce.reached)

        if not self.prevent_tile_shift():
            self.world_shift()

        # Other
        self.end_game_triforce.update(self.cam_pos, self.level_length)

        # Collision
        self.handle_collision()

    def draw_monsters(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for monster in chunk.monsters:
                if monster.in_frame():
                    monster.draw()

    def draw_tiles(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for tile in chunk.tiles:
                if tile.in_frame():
                    tile.draw(self.screen)

    def draw_text_anomalies(self):
        chunks_to_draw = self.get_chunks_to_draw()

        for chunk in chunks_to_draw:
            for message in chunk.text_anomalies:
                message.draw()

    # Draw the state of the level
    def draw(self):

        # == Player 
        self.link.draw()

        # Draw necessary tiles and monsters
        chunks_to_draw = self.get_chunks_to_draw()
        for chunk in chunks_to_draw:
            chunk.draw(self.screen)

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
