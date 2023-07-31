from Loot.loot import Loot
from Support.settings import tile_size


class Coin(Loot):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, player, index)
        self.timer = 0
        self.disappear_delay = 20
        self.message = "+200 COIN"
        self.coins = 200

    def show(self, level):
        super().show(level)
        self.make_text_anomaly()

        # Process effect of the loot
        if not self.looted:
            self.process_loot()

    def update(self, shift_x):
        super().update(shift_x)

        # Make coin disappear after a while
        if self.activated and self.y <= self.orig_position[1] - tile_size:
            self.timer += 1
            if self.timer % self.disappear_delay == 0:
                self.y = 800
