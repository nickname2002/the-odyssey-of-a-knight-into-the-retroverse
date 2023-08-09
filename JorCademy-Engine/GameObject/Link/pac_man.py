from GameObject.gameobject import GameObject
from jorcademy import *
from Support.settings import screen_width, scale

IDLE = 0
WALKING_1 = 1
WALKING_2 = 2
WALKING_3 = 3
WALKING_4 = 4
WALKING_5 = 5
JUMPING = 1
DEAD = 6


class PacMan(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.player = player
        self.state = IDLE
        self.facing_left = self.player.facing_left
        self.speed = 6
        self.walk_animation_delay = 5
        self.is_grounded = False
        self.visible = False
        self.sprites = [
            "pac_man/pac_man_walking_1.png",
            "pac_man/pac_man_walking_1.png",
            "pac_man/pac_man_walking_2.png",
            "pac_man/pac_man_walking_3.png",
            "pac_man/pac_man_walking_2.png",
            "pac_man/pac_man_walking_1.png",
            "pac_man/pac_man_death.png"
        ]
        self.waka_sound = load_sound('assets/sounds/pac_man/waka.mp3')
        self.death_sound = load_sound('assets/sounds/pac_man/pac_man_death.mp3')
        self.play_sound_delay = 15
        self.play_sound_timer = 0

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

            if self.play_sound_timer >= self.play_sound_delay and self.visible:
                play_sound(self.waka_sound, 0.15)
                self.play_sound_timer = 0

            self.play_sound_timer += 1

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
            if self.state < WALKING_1 or self.state >= WALKING_5:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

            if self.play_sound_timer >= self.play_sound_delay and self.visible:
                play_sound(self.waka_sound, 0.15)
                self.play_sound_timer = 0

            self.play_sound_timer += 1

        self.timer += 1

    # Let character jump
    def jump(self, speed):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False

    # Update Pac-Man
    def update(self, cam_pos, level_length):
        if self.player.killed and self.visible:
            self.play_death_sound()
            self.y = self.player.y + 10 * scale
            self.state = DEAD
            return

        super().update(cam_pos, level_length)

        # Derive properties from player
        self.facing_left = self.player.facing_left
        self.is_grounded = self.player.is_grounded
        self.x = self.player.x
        self.y = self.player.y

    # Draw Pac-Man
    def draw(self):
        sprite = self.sprites[self.state]

        if self.visible:
            image(sprite, self.x, self.y, self.width / 26, self.facing_left)
