from gameobject import GameObject
from tile_data import *
from jorcademy import image
from text_anomaly import TextAnomaly
from settings import screen_width, screen_height, tile_size
import pygame


class Monster(GameObject):

    def __init__(self, pos, w, h, player, level):
        super().__init__(pos, w, h)
        self.orig_pos = pos
        self.sprite_set = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.sel_sprite_index = 0
        self.offset = 0
        self.moving = False
        self.player = player
        self.message = "+20 SCORE"
        self.level = level
        self.killed = False
        self.loot = 100

    def is_out_of_frame(self):
        if self.moving:
            return \
                self.x < 0 - self.width and \
                (self.y < 0 - self.width or self.y > screen_height + self.height)

    def in_frame(self):
        return self.x + self.width > 0 and self.x - self.width < screen_width

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.x = self.orig_pos[0] - cam_pos
        self.x += self.offset
        self.timer += 1

        if (self.x - self.width) - self.player.x < screen_width / 2:
            self.moving = True

    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()

    def update_sprite_state(self):
        if self.sel_sprite_index < len(self.sprite_set) - 1:
            self.sel_sprite_index += 1
        else:
            self.sel_sprite_index = 0


class Bokoblin(Monster):

    # TODO: Add cool dying animation 

    def __init__(self, pos, w, h, player, level):
        super().__init__(pos, w, h, player, level)
        self.sprite_set = [
            "monsters/bokoblin/bokoblin_1.png",
            "monsters/bokoblin/bokoblin_2.png"
        ]
        self.speed = 1
        self.direction = pygame.Vector2(-self.speed, 0)

    def die(self):
        if not self.killed:
            self.make_text_anomaly()
            self.player.coins += self.loot

        self.killed = True

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.update_text_anomalies(new_text_anomaly)

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

    def handle_collision_with_player(self, level):
        if self.collision_top(self.player) and self.player.collision_bottom(self):

            # Kill monster
            if not self.killed:
                self.die()

            # Make player jump when landing on top of monster
            self.player.is_grounded = True
            self.player.jump(self.player.jump_speed + 4)

        # Process player damage
        elif self.collision(self.player):
            self.player.hit(level)
            pass

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible == True:
            self.die()

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        if self.moving:
            self.offset += self.direction.x * self.speed

    def draw(self):
        super().draw()

        # Make sure the monster is drawn facing the right direction
        if self.direction.x > 0:
            image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3)
        else:
            image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3, True)
