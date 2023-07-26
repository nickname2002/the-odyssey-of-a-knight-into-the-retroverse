from gameobject import GameObject
from settings import screen_width
from tile import MYSTERY_BOX
from jorcademy import *

# States for Link
IDLE = 0
FIGHT = 1
WALKING_1 = 2
WALKING_2 = 3
WALKING_3 = 4
WALKING_4 = 5
WALKING_5 = 6
WALKING_6 = 7
WALKING_7 = 8
WALKING_8 = 9
WALKING_9 = 10
WALKING_10 = 11
JUMPING = 12

class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.lives = 3
        self.coins = 0
        self.speed = 4
        self.facing_left = False
        self.jump_speed = -13 
        self.is_grounded = False
        self.walk_animation_delay = 3
        self.state = IDLE
        self.sprites = [
            'link/link_idle.png',
            'link/link_fight.png',
            'link/link_walking_1.png',
            'link/link_walking_2.png',
            'link/link_walking_3.png',
            'link/link_walking_4.png',
            'link/link_walking_5.png',
            'link/link_walking_6.png',
            'link/link_walking_7.png',
            'link/link_walking_8.png',
            'link/link_walking_9.png',
            'link/link_walking_10.png',
            'link/link_jumping.png'
        ]


    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)

        # Update horizontal direction and position of Link
        if is_key_down("d"):
            self.move_right(cam_pos, level_length)
        elif is_key_down("a"):
            self.move_left(cam_pos)
        else: 
            self.direction.x = 0
            self.state = IDLE

        # Update the vertical position of Link
        if is_key_down("space"):
            self.jump()


    # Move right
    def move_right(self, cam_pos, level_length):
        self.facing_left = False
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_10:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        self.direction.x = self.speed
        if self.x < screen_width / 2 or cam_pos >= (level_length - screen_width):
            self.x += self.direction.x


    # Move left
    def move_left(self, cam_pos):
        self.facing_left = True
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_10:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        self.direction.x = -self.speed
        if self.x > screen_width / 4 or cam_pos <= 0:
            self.x += self.direction.x


    # Let character jump
    def jump(self):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = self.jump_speed
            self.is_grounded = False


    # Draw Link
    def draw(self):
        sprite = self.sprites[self.state]
        image(sprite, self.x, self.y, 1.28, self.facing_left)
