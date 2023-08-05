from GameObject.Monster.monster import Monster
from jorcademy import *


class Barrel(Monster):

    def __init__(self, pos, w, h, player, donkey_kong):
        super().__init__(pos, w, h, player, donkey_kong.level, donkey_kong.chunk)
        self.donkey_kong = donkey_kong
        self.sel_sprite_index = 0
        self.orig_cam_pos = donkey_kong.level.cam_pos
        self.sprite_set = [
            "monsters/donkey_kong/barrel/barrel_1.png",
            "monsters/donkey_kong/barrel/barrel_2.png",
            "monsters/donkey_kong/barrel/barrel_3.png",
            "monsters/donkey_kong/barrel/barrel_4.png"
        ]
        self.walk_animation_delay = 5
        self.direction = pygame.Vector2(donkey_kong.get_direction(), 0)
        self.speed = 4
        self.offset = 0

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        self.offset += self.direction.x * self.speed
        self.x = self.orig_pos[0] - (self.donkey_kong.level.cam_pos - self.orig_cam_pos) + self.offset

    def update(self, cam_pos, level_length):
        self.handle_movement(cam_pos, level_length)
        self.timer += 1

    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.sel_sprite_index], self.x, self.y, 3)

    def update_sprite_state(self):
        if self.sel_sprite_index == len(self.sprite_set) - 1:
            self.sel_sprite_index = 0
        else:
            self.sel_sprite_index += 1

    def handle_collision(self, tile, _, level):
        # Handle collision on left side
        if self.collision_left(tile):
            self.killed = True

        # Handle collision on right side
        elif self.collision_right(tile):
            self.killed = True

        # Handle collision on bottom side
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

        # Player game events
        self.handle_collision_with_player(level)
        self.handle_collision_with_sword()

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible:
            self.die()
