import math
from GameObject.gameobject import GameObject
from jorcademy import *


class FireBall(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.visible = False
        self.player = player
        self.sprite = "fire_mario/fireball.png"
        self.speed = 5
        self.amplitude = 5
        self.frequency = 0.1

    def attack(self):
        if not self.visible:
            self.x = self.player.x + 30
            self.y = self.player.y + 10
            self.visible = True

            # Determine whether fireball should move left or right
            if self.player.facing_left:
                self.direction.x = -1
            else:
                self.direction.x = 1

    def handle_movement(self, cam_pos, level_length):
        self.x += self.direction.x * self.speed

        # Update timer
        if self.visible:
            self.timer += 1

        # Calculate the sine wave movement
        sine_wave = math.sin(2 * math.pi * self.frequency * self.timer)

        # Update the y position using the sine wave formula with amplitude
        self.y += self.amplitude * sine_wave

        # Limit the y position to avoid going out of bounds
        self.y = max(self.y, 0)  # Assuming the minimum y value is 0
        self.y = min(self.y, level_length)  # Assuming the maximum y value is the level length

    def reset(self):

        # Reset position
        self.x = self.player.x
        self.y = self.player.y

        # Hide fireball
        self.visible = False

        # Reset direction
        self.direction.x = 0
        self.direction.y = 0

        # Reset timer
        self.timer = 0

    def handle_collision(self, tile, index, level):
        if self.collision_left(tile) or self.collision_right(tile):
            self.reset()

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Check if fireball is out of screen
        if self.out_of_screen():
            self.reset()

    def draw(self):
        if self.visible:
            image(self.sprite, self.x, self.y, 0.16, False, 0)
