from jorcademy import *
from GameObject.gameobject import GameObject


class Triforce(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.sprite = "other/triforce.png"
        self.player = player
        self.reached = False

    def handle_movement(self, cam_pos, level_length):
        pass

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.correct_position_with_camera(cam_pos)

        # If the player collides with the triforce, it is looted
        if self.player.x >= self.x:
            self.reached = True

    def draw(self):
        image(self.sprite, self.x, self.y, 0.5, False, 0)
