from tile import StaticTile
from settings import tile_size
from text_anomaly import TextAnomaly
import pygame


class Loot(StaticTile):
    
    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code)
        self.direction_y = 0
        self.activated = False
        self.speed = 2 
        self.player = player
        self.looted = False
        self.message = "SAMPLE_MESSAGE"
        self.level = None


    def show(self, level):
        self.activated = True
        self.direction_y = -self.speed
        self.level = level


    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.update_text_anomalies(new_text_anomaly)

    
    def make_image(self, path):
        surface = pygame.image.load(path).convert_alpha()
        factor = tile_size / int(surface.get_width())
        resized_surface = pygame.transform.scale(surface, (int(surface.get_width() * factor), surface.get_height() * factor))
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


    def update(self, shift_x):
        super().update(shift_x)
        self.rise_animation()


class Coin(Loot):

    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code, player)
        self.timer = 0
        self.disappear_delay = 20
        self.message = "+1 COIN"


    def show(self, level):
        super().show(level)
        self.make_text_anomaly()

        # Process effect of the loot
        if not self.looted:
            self.player.coins += 1
            self.looted = True


    def update(self, shift_x):
        super().update(shift_x)

        # Make coin disappear after a while
        if self.activated and self.y <= self.orig_position[1] - tile_size:
            self.timer += 1
            if self.timer % self.disappear_delay == 0:
                self.y = 800


class ExtraLife(Loot):

    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code, player)
        self.message = "+1 UP"


    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.make_text_anomaly()
                self.player.lives += 1
                self.looted = True
                self.y = 800


    def draw(self, shift_x):
        self.make_image("assets/power_ups/1up.png")
        super().draw(shift_x)


class FireMario(Loot):

    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code, player)
        self.message = ""


    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.make_text_anomaly()
                # TODO: Implement special looting behavior
                self.looted = True
                self.y = 800


    def draw(self, screen):
        self.make_image("assets/power_ups/flower_power.png")
        super().draw(screen)
            
