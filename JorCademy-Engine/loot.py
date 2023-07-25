from tile import StaticTile
from settings import tile_size
from jorcademy import image
import pygame


class Loot(StaticTile):
    
    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code)
        self.direction_y = 0
        self.activated = False
        self.speed = 2 
        self.player = player
        self.looted = False


    def show(self):
        self.activated = True
        self.direction_y = -self.speed

    
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
        

    def show(self):
        super().show()

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


    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                self.player.lives += 1
                self.looted = True
                self.y = 800


class FireMario(Loot):

    def __init__(self, size, pos, surface, code, player):
        super().__init__(size, pos, surface, code, player)


    def update(self, shift_x):
        super().update(shift_x)

        # Process effect of the loot
        if self.activated and not self.looted:
            if self.collision_with_player():
                # TODO: Implement special looting behavior
                self.looted = True
                self.y = 800


    def draw(self, screen):
        surface = pygame.image.load("assets/power_ups/flower_power.png").convert_alpha()
        # TODO: fix backdrop of surface
        resized_surface = pygame.transform.scale(surface, (int(surface.get_width() * 0.129), surface.get_height() * 0.129))
        new_surf = pygame.Surface((tile_size, tile_size))
        new_surf.blit(resized_surface, (0, 0))
        self.image = new_surf
        super().draw(screen)
            
