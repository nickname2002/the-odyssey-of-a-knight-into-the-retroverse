import pygame
from Environment.text_anomaly import TextAnomaly
from Level.tile import MovingTile
from Support.settings import tile_size


class Loot(MovingTile):

    def __init__(self, size, pos, surface, code, player, index):
        super().__init__(size, pos, surface, code, index)
        self.direction_y = 0
        self.activated = False
        self.speed = 2
        self.player = player
        self.looted = False
        self.message = "SAMPLE_MESSAGE"
        self.level = None
        self.coins = 0
        self.triggered_representation = "SAMPLE_TRIGGERED_REPRESENTATION"

    def show(self, level):
        self.activated = True
        self.direction_y = -self.speed
        self.level = level

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def make_image(self, path):
        surface = pygame.image.load(path).convert_alpha()
        factor = tile_size / int(surface.get_width())
        resized_surface = pygame.transform.scale(surface,
                                                 (int(surface.get_width() * factor), surface.get_height() * factor))
        new_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        new_surf.blit(resized_surface, (0, 0))
        self.image = new_surf

    def rise_animation(self):
        if self.activated and self.y > self.orig_position[1] - tile_size:
            self.y += self.direction_y
        else:
            self.direction_y = 0

    def collision_with_player(self):
        return self.player.collision(self)

    def process_loot(self):
        self.player.coins += self.coins
        self.make_text_anomaly()
        self.looted = True

    def update(self, shift_x):
        super().update(shift_x)
        self.rise_animation()

