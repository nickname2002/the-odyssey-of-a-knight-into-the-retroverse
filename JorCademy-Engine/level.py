from settings import tile_size, screen_width, tilemap_list
from jorcademy import *
from tile import Tile, StaticTile
from link import Link
import csv
import cv2
import os

class Level:

    # TODO: Make sure levels can be imported
    def __init__(self, level_data, level_name):
        self.level_name = level_name
        self.level_data = level_data
        self.tiles = []
        self.cam_pos = 0
        self.link = Link((100, 100), 20, 40)
        self.level_length = len(level_data[0]) * tile_size  # NOTE: might need to be reworked    


    # Convert selected level csv-file to list of lists, containing the tiles
    def import_level_data(self):
        filepath = "maps/level_" + self.level_name + ".csv"
        data = []

        # Open and parse csv
        with open(filepath, newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data.append([element for element in row])

        return data


    # Import tiles from a tileset 
    def import_tiles(self, path):
        # Tile properties
        tile_width = 16
        tile_height = 16

        # Read the tileset image using OpenCV
        tileset_image = cv2.imread(path)

        # Get the size of the tileset image
        tileset_height, tileset_width, _ = tileset_image.shape

        # Calculate the number of rows and columns
        num_cols = tileset_width // (tile_width + 2 * 1)
        num_rows = tileset_height // (tile_height + 2 * 1)

        # Create an empty array to store the individual tiles
        tiles_array = []

        # Split the tileset into individual tiles
        for row in range(num_rows):
            for col in range(num_cols):
                left = col * (tile_width + 1 * 1) + 1
                upper = row * (tile_height + 1 * 1) + 1
                right = left + tile_width
                lower = upper + tile_height

                # Crop the tile from the tileset image
                tile = tileset_image[upper:lower, left:right]

                # Append the tile to the array
                tiles_array.append(tile)

        # Export each tile to PNG and store in tiles folder
        for i, tile in enumerate(tiles_array):
            cv2.imwrite(f"tiles/{i}.png", tile)


    # Initialize level
    def setup(self):

        # Initial y-coordinate of tile
        y = tile_size / 2

        # self.level_data = self.import_level_data()

        # Read tiles into tiles list
        for row in self.level_data:
        
            # Initial x-coordinate of tile
            x = tile_size / 2

            for tile in row:
                pos = (x, y)

                # Treat different tiles correctly
                if tile != "L":
                    image_path = f"tiles/{tile}.png"
                    self.tiles.append(Tile(tile_size, pos))
                elif tile == "L":
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
            tile.draw()