from GameObject.gameobject import GameObject
from Support.settings import scale
from jorcademy import *

# States for Link
IDLE = 0


class MasterSword(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.visible = False
        self.timer = 0
        self.attack_animation_delay = 20
        self.sword_reach = 10 * scale
        self.sprite = "link/master_sword.png"
        self.player = player
        self.gravity = 0 * scale
        self.rotation = -75

    def attack(self):
        self.x = self.player.x + 30 * scale
        self.y = self.player.y + 10 * scale
        self.visible = True

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Make sure the collider is positioned properly
        # based on the orientation of the player
        if not self.player.facing_left:
            self.x = self.player.x + self.width
        else:
            self.x = self.player.x - self.width

        if self.visible:
            self.timer += 1

            # Make sure cooldown for weapon usage is activated when triggered too long
            if is_key_down("shift"):
                if self.timer == 100000:
                    self.timer = 0
                if self.timer % self.attack_animation_delay == 0:
                    self.player.activate_attack_cooldown()
                    self.visible = False
            # Move back to idle state when shift is not pressed
            else:
                self.timer = 0
                self.visible = False
                self.player.state = IDLE

    def draw(self):
        if self.visible:
            if not self.player.facing_left:
                image(self.sprite, self.x - 32 * scale, self.y, 1 * scale, False, self.rotation)
            else:
                image(self.sprite, self.x, self.y, 1 * scale, False, self.rotation + -(self.rotation * 2))
