from jorcademy import rect
from tile_data import *
from settings import screen_width, screen_height
import pygame


class GameObject:

    def __init__(self, pos, w, h):
        self.is_grounded = False
        self.x = pos[0]
        self.y = pos[1]
        self.orig_pos = pos
        self.offset = 0
        self.width = w
        self.height = h
        self.direction = pygame.Vector2(0, 0)
        self.gravity = 0.6
        self.walk_animation_delay = 5
        self.timer = 0
        self.speed = 4
        self.visible = False

    def out_of_screen(self):
        return (self.x - self.width < 0 or self.x + self.width > screen_width) or \
               (self.y - self.height < 0 or self.y + self.height > screen_height)

    def update(self, cam_pos, level_length):
        self.handle_movement(cam_pos, level_length)

    def handle_movement(self, cam_pos, level_length):
        # Apply gravity to Link
        self.apply_gravity()

        if self.timer == 100000:
            self.timer = 0

    def draw(self):
        rect((255, 50, 50), self.x, self.y, self.width, self.height)

    def collision(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_top(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 10) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 10) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y - self.height / 2 - 10) <= (other.y + other.height / 2) and \
                     (self.y - self.height / 2 + 10) >= (other.y - other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_bottom(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 - 10) >= (other.x - other.width / 2) and \
                     (self.x - self.width / 2 + 10) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 10) <= (other.y - other.height / 2) <= (self.y + self.height / 2 + 10)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_left(self, other):
        # Check in range horizontally
        in_x_range = (self.x - self.width / 2 - 5) <= (other.x + other.width / 2) <= (self.x - self.width / 2 + 5)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 5) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2 + 5) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def collision_right(self, other):
        # Check in range horizontally
        in_x_range = (self.x + self.width / 2 + 5) >= (other.x - other.width / 2) and \
                     (self.x + self.width / 2 - 5) <= (other.x + other.width / 2)

        # Check in range vertically
        in_y_range = (self.y + self.height / 2 - 5) >= (other.y - other.height / 2) and \
                     (self.y - self.height / 2 + 5) <= (other.y + other.height / 2)

        # Check horizontally and vertically in range
        return in_x_range and in_y_range

    def handle_collision(self, tile, index, level):
        # Handle collision on left side of object
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.x = tile.x + tile.width / 2 + self.width / 2

        # Handle collision on right side of object
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.x = tile.x - tile.width / 2 - self.width / 2

        # Handle collision on bottom side of object
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

        # Handle collision on top side of object
        elif self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0

                # Handle collision with mystery box
                if tile.code == MYSTERY_BOX:
                    try:
                        loot = tile.give_loot(level)
                        level.tiles.insert(index, loot)
                    except:
                        pass

    # Applying gravity
    def apply_gravity(self):
        if self.direction.y < 5:
            self.direction.y += self.gravity
        self.y += self.direction.y
