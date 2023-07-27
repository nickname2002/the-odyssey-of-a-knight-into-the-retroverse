from gameobject import GameObject
from settings import screen_width, screen_height
from jorcademy import *

# States for FireMario
IDLE = 0
JUMPING = 1
WALKING_1 = 2
WALKING_2 = 3
WALKING_3 = 4


class FireMario(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.player = player
        self.sprites = [
            'fire_mario/fire_mario_idle.png',
            'fire_mario/fire_mario_jumping.png',
            'fire_mario/fire_mario_walking_1.png',
            'fire_mario/fire_mario_walking_2.png',
            'fire_mario/fire_mario_walking_3.png'
        ]
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.state = IDLE
        self.facing_left = self.player.facing_left
        self.is_grounded = False
        self.visible = False
        # TODO: add fireball

    def handle_movement(self, cam_pos, level_length):
        # Update horizontal direction and position of Link
        if is_key_down("d") and not is_key_down('shift'):
            self.move_right(cam_pos, level_length)
        elif is_key_down("a") and not is_key_down("shift"):
            self.move_left(cam_pos)
        elif self.is_grounded:
            self.direction.x = 0
            self.state = IDLE

        # Update the vertical position of Link
        if is_key_down("space"):
            self.jump(self.player.jump_speed)

    # Move right
    def move_right(self, cam_pos, level_length):
        self.facing_left = False

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_3:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        # Update coordinates
        self.direction.x = self.speed
        if self.x < screen_width / 2 or cam_pos >= (level_length - screen_width):
            self.x += self.direction.x

    # Move left
    def move_left(self, cam_pos):
        self.facing_left = True

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_3:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

    # Let character jump
    def jump(self, speed):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False

    # Update FireMario
    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Derive properties from player
        self.facing_left = self.player.facing_left
        self.is_grounded = self.player.is_grounded
        self.x = self.player.x
        self.y = self.player.y

    # Draw FireMario
    def draw(self):
        sprite = self.sprites[self.state]

        if self.visible:
            image(sprite, self.x, self.y, 2, self.facing_left)
