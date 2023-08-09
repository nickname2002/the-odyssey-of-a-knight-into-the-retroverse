from GameObject.Monster.monster import Monster
from GameObject.Monster.Weapons.barrel import Barrel
from Support.settings import scale
from jorcademy import *
import random

# Donkey Kong states
IDLE_1 = 0
IDLE_2 = 1
ATTACK = 2


class DonkeyKong(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            "monsters/donkey_kong/donkey_idle_1.png",
            "monsters/donkey_kong/donkey_idle_2.png",
            "monsters/donkey_kong/donkey_throw.png",
            "monsters/donkey_kong/donkey_kong_dead.png"
        ]
        self.state = IDLE_1
        self.die_state_index = 3
        self.speed = 1 * scale
        self.health = 3
        self.direction = pygame.Vector2(-self.speed, 0)
        self.jump_speed = -16 * scale
        self.walk_animation_delay = 15
        self.y -= 1 * scale

        # Jump delay
        self.min_jump_delay = 60 * 1
        self.max_jump_delay = 60 * 4

        # Attack delay
        self.min_attack_delay = 60 * 5
        self.max_attack_delay = 60 * 10

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

    def jump(self, speed):
        self.jump_timer = 0
        super().jump(speed)

    def attack(self):
        self.state = ATTACK

        # Add new barrel to the chunk's monster list
        barrel = Barrel((self.x, self.y), 36 * scale, 30 * scale, self.player, self)
        self.level.chunks[self.chunk.index].monsters.append(barrel)

        # Reset attack timer
        self.init_new_attack_delay()
        self.attack_timer = 0

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible and \
                self.invincible_timer <= 0:
            self.health -= 1
            self.invincible_timer = self.invincible_delay

    def get_direction(self):
        if self.player.x <= self.x:
            return -1
        else:
            return 1

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.handle_movement(cam_pos, level_length)

        # Stop monster action when dead
        if self.killed:
            return

        # Make the monster jump when the timer is up
        if self.is_grounded and self.jump_timer >= self.random_jump_delay:
            self.jump(self.jump_speed)
            self.init_new_jump_delay()
            self.init_new_jump_speed()

        if self.attack_timer >= self.random_attack_delay:
            self.attack()

        # Update the jump timer
        if self.is_grounded:
            self.jump_timer += 1

        # Update attack timer
        self.attack_timer += 1

    def draw(self):
        self.update_sprite_state()

        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.state], self.x, self.y, 3 * scale, self.player.x >= self.x)

    def update_sprite_state(self):
        if self.killed:
            self.show_die_animation()
            return

        # Update jump animation
        if self.timer % self.walk_animation_delay == 0:
            if self.state != ATTACK:
                if self.state < IDLE_2:
                    self.state += 1
                else:
                    self.state = IDLE_1
            else:
                attack_animation_delay = 15
                if self.timer % attack_animation_delay == 0:
                    self.state = IDLE_1
