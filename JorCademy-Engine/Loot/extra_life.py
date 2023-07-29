import sys

sys.path.append('..')
from Loot.loot import Loot
from jorcademy import *
from Support.settings import tile_size


class ExtraLife(Loot):

    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code, player)
        self.message = "+1 UP"
        self.moving = False
        self.speed = 2

    def update(self, shift_x):
        super().update(shift_x)

        # Move mushroom
        if self.moving:
            self.direction.x = self.speed
            self.offset += self.direction.x
            self.apply_gravity()

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.process_loot()
                self.y = 800

    def process_loot(self):
        super().process_loot()
        self.player.lives += 1

    def rise_animation(self):
        super().rise_animation()
        if self.y == self.orig_position[1] - tile_size:
            self.moving = True

    def draw(self, shift_x):
        if self.moving:
            image("power_ups/1up.png", self.x, self.y, 0.129)
        else:
            self.make_image("assets/power_ups/1up.png")
            super().draw(shift_x)
