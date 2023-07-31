from Loot.loot import Loot


class FireFlower(Loot):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, player, index)
        self.message = "+1000 COINS"
        self.coins = 1000
        self.triggered_representation = "FIRE_MARIO"

    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.make_text_anomaly()
                self.process_loot()
                self.y = 800

    def process_loot(self):
        super().process_loot()
        self.player.trigger_new_representation(self.triggered_representation)

    def draw(self, screen):
        self.make_image("assets/power_ups/flower_power.png")
        super().draw(screen)
