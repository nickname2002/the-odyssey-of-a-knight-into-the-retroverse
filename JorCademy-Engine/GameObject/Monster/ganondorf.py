from GameObject.Monster.monster import Monster
from jorcademy import *
import random

# Ganondorf states
IDLE = 0
WALKING_1 = 1
WALKING_2 = 2
WALKING_3 = 3
WALKING_4 = 4
WALKING_5 = 5
WALKING_6 = 6


class Ganondorf(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            "monsters/ganondorf/ganondorf_idle_1.png",
            "monsters/ganondorf/ganondorf_walking_1.png",
            "monsters/ganondorf/ganondorf_walking_2.png",
            "monsters/ganondorf/ganondorf_walking_3.png",
            "monsters/ganondorf/ganondorf_walking_4.png",
            "monsters/ganondorf/ganondorf_walking_5.png",
            "monsters/ganondorf/ganondorf_walking_6.png",
        ]
        self.state = WALKING_1

        # Walking delay
        self.walking_timer = 0
        self.walking_delay = 10

        # Attack delay
        self.invincible_delay = 1000
        self.attack_timer = 0
        self.min_attack_delay = 60 * 5
        self.max_attack_delay = 60 * 10
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.handle_movement(cam_pos, level_length)
        self.update_sprite_state()

    def update_sprite_state(self):
        if self.state != IDLE:
            self.walking_timer += 1
            if self.walking_timer >= self.walking_delay:
                self.walking_timer = 0
                self.state += 1
                if self.state > WALKING_6:
                    self.state = WALKING_1

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

    def attack(self):
        pass

    def init_new_attack_delay(self):
        pass

    def init_new_jump_delay(self):
        pass

    def draw(self):
        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.state], self.x, self.y, 1.5, self.player.x >= self.x)
