import math
from GameObject.Monster.monster import Monster
from jorcademy import *


class EnemyFireBall(Monster):

    def __init__(self, pos, w, h, owner, player, shooting_direction):
        super().__init__(pos, w, h, player, owner.level, owner.chunk)
        self.orig_cam_pos = owner.level.cam_pos
        self.visible = False
        self.owner = owner
        self.sprite = "fire_mario/fireball.png"
        self.speed = 5
        self.amplitude = 5
        self.frequency = 0.1
        self.player = player
        self.shooting_direction = shooting_direction

    def attack(self):
        if self.player.facing_left:
            self.direction.x = -1
        else:
            self.direction.x = 1

    def handle_movement(self, cam_pos, level_length):
        self.offset += self.shooting_direction.x * self.speed

        # Calculate the sine wave movement
        sine_wave = math.sin(2 * math.pi * self.frequency * self.timer)

        # Update the y position using the sine wave formula with amplitude
        self.y += self.amplitude * sine_wave

        # Limit the y position to avoid going out of bounds
        self.y = max(self.y, 0)  # Assuming the minimum y value is 0
        self.y = min(self.y, level_length)  # Assuming the maximum y value is the level length

        # Update timer
        self.timer += 1

    def handle_collision(self, tile, index, level):
        if self.collision_left(tile) or self.collision_right(tile):
            self.killed = False

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.correct_position_with_camera(cam_pos)

        # Check if fireball is out of screen
        if self.out_of_screen():
            self.killed = True

    def draw(self):
        image(self.sprite, self.x, self.y, 0.16, False, 0)
