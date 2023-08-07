from GameObject.Monster.monster import Monster
from Support.settings import scale
from jorcademy import *


class Bokoblin(Monster):

    # TODO: Add cool dying animation

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            "monsters/bokoblin/bokoblin_1.png",
            "monsters/bokoblin/bokoblin_2.png"
        ]
        self.speed = 1
        self.direction = pygame.Vector2(-self.speed, 0)


    def handle_collision(self, tile, _, level):
        # Handle collision on left side of monster
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.direction.x *= -1

        # Handle collision on right side of monster
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.direction.x *= -1

        # Handle collision on bottom side of monster
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

        # Handle collision on top side of monster
        elif self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0

        # Player game events
        self.handle_collision_with_player(level)
        self.handle_collision_with_sword()

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible:
            # play_sound(self.player.master_sword.hit_sound)
            self.die()

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        if self.moving:
            self.offset += self.direction.x * self.speed

    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        if self.direction.x > 0:
            image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3 * scale)
        else:
            image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3 * scale, True)

    def update_sprite_state(self):
        if self.sel_sprite_index < len(self.sprite_set) - 1:
            self.sel_sprite_index += 1
        else:
            self.sel_sprite_index = 0
