from gameobject import GameObject
from jorcademy import *


class FireBall(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.visible = False
        self.player = player
        self.sprite = "fire_mario/fireball.png"  # TODO: add transparent sprite

    def attack(self):
        self.x = self.player.x + 30
        self.y = self.player.y + 10
        self.visible = True

    def update(self, cam_pos, level_length):
        # super().update(cam_pos, level_length)
        # TODO: make sure fireball takes collision into account
        # TODO: implement movement of fireball
        # TODO: implement proper orientation of fireball
        # TODO: user super.update() to take gravity into account
        pass

    def draw(self):
        if self.visible:
            image(self.sprite, self.x, self.y, 0.5, False, 0)
