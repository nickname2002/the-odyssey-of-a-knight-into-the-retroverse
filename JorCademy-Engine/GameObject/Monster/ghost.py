from GameObject.Monster.monster import Monster
from Support.settings import scale
from jorcademy import *
import pygame
import math

# States
NOT_VULNERABLE_HORIZONTAL = 0
NOT_VULNERABLE_VERTICAL = 1
VULNERABLE = 2

# Player representations
PAC_MAN = 2


class Ghost(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            "monsters/ghost/ghost_horizontal.png",
            "monsters/ghost/ghost_vertical.png",
            "monsters/ghost/ghost_vulnerable.png",
            "monsters/ghost/ghost_dead.png"
        ]
        self.die_state_index = 3
        self.speed = 1.5 * scale
        self.direction = pygame.Vector2(-self.speed, 0)
        self.amplitude = 1 * scale
        self.frequency = 1 * scale
        self.eaten_sound = load_sound("sounds/pac_man/eat_pac_man.ogg")

    def handle_collision_with_player(self, level):
        # Process player damage & damage from player
        if self.collision(self.player):
            if self.player.representation == PAC_MAN:
                play_sound(self.eaten_sound, 0.3)
                self.health -= 1
            elif not self.player.killed:
                self.player.die(level)

        # Make sure to die if health is 0
        if self.health <= 0:
            self.die()

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

    def handle_movement(self, cam_pos, level_length):
        if self.moving:
            self.offset += self.direction.x * self.speed

            # Get the time passed since the game started in milliseconds
            current_time = pygame.time.get_ticks()

            # Calculate the time in seconds
            time_in_seconds = current_time / 1000

            # Calculate the sine wave movement
            sine_wave = math.sin(2 * math.pi * self.frequency * time_in_seconds)

            # Update the y position using the sine wave formula with amplitude
            self.y += self.amplitude * sine_wave

    def determine_sel_sprite_index(self):
        if self.killed:
            self.show_die_animation()
            return

        self.state = NOT_VULNERABLE_HORIZONTAL

        if self.player.representation == PAC_MAN:
            self.state = VULNERABLE
        elif self.player.y < (self.y - self.height / 2) and \
                self.player.x + self.player.width / 2 > self.x - self.width / 2 and \
                self.player.x - self.player.width / 2 < self.x + self.width / 2:
            self.state = NOT_VULNERABLE_VERTICAL

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.determine_sel_sprite_index()

    def draw(self):
        # Make sure the monster is drawn facing the right direction
        if self.direction.x > 0:
            image(self.sprite_set[self.state], self.x, self.y, 1 * scale)
        else:
            image(self.sprite_set[self.state], self.x, self.y, 1 * scale, True)
