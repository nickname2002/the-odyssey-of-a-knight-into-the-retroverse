from settings import tile_size, screen_width
from jorcademy import *
from tile import Tile
from link import Link


class Level:

    # TODO: Make sure levels can be imported
    def __init__(self, level_data):
        self.level_data = level_data
        self.tiles = []
        self.cam_pos = 0
        self.link = Link((100, 100), 20, 40)


    def setup(self):
        y = tile_size / 2

        for row in self.level_data:
            x = tile_size / 2

            for tile in row:
                pos = (x, y)

                if tile == "1":
                    self.tiles.append(Tile((100, 100, 100), pos))
                elif tile == "L":
                    self.link.x = pos[0]
                    self.link.y = pos[1]

                x += tile_size 

            y += tile_size


    def world_shift(self):
        if is_key_down("d") and self.link.x >= screen_width / 2:
            self.cam_pos += self.link.speed
        if is_key_down("a") and self.link.x <= screen_width / 4 and self.cam_pos > 0:         
            self.cam_pos -= self.link.speed


    def horizontal_collision(self):
        player = self.link

        for tile in self.tiles:
            if player.collision_left(tile):
                if player.direction.x < 0:
                    player.x = tile.x + tile.width / 2 + player.width / 2
            elif player.collision_right(tile):
                if player.direction.x > 0:
                    player.x = tile.x - tile.width / 2 - player.width / 2


    def vertical_collision(self):
        player = self.link
        player.apply_gravity()

        for tile in self.tiles:
            if player.collision_bottom(tile):
                if player.direction.y > 0:
                    player.y = tile.y - tile.height / 2 - player.height / 2
                    player.direction.y = 0
            elif player.collision_top(tile):
                if player.direction.y < 0:
                    player.y = tile.y + tile.height / 2 + player.height / 2
            

    def update(self):
        # Player
        self.link.update()
        self.horizontal_collision()
        self.vertical_collision()

        # Tiles
        self.world_shift()
        for tile in self.tiles:
            tile.update(self.cam_pos)


    def draw(self):
        self.link.draw()
        for tile in self.tiles:
            tile.draw()