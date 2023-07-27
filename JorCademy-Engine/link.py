from gameobject import GameObject
from settings import screen_width
from fire_mario import FireMario
from master_sword import MasterSword
from tile_data import *
from jorcademy import *

# States for Link
IDLE = 0
ATTACK = 1
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

# Representations for Link
LINK = 0
FIRE_MARIO = 1
# TODO: add Pac-Man representation


class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.score = 0
        self.lives = 3
        self.coins = 0  # NOTE: maybe change coins into rupees
        self.orig_speed = 4
        self.speed = 4
        self.facing_left = False
        self.jump_speed = -13
        self.is_grounded = False
        self.walk_animation_delay = 3
        self.state = IDLE
        self.representation = LINK  # TODO: change for debugging other representation's behavior
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.master_sword = MasterSword((self.x, self.y), 45, 33, self)
        self.visible = True
        self.fire_mario = FireMario((self.x, self.y), 32, 64, self)
        self.representation_change_timer = 0
        self.representation_change_delay = 1000
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

    def handle_collision(self, tile, index, level):
        # Handle collision on left side of object
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.x = tile.x + tile.width / 2 + self.width / 2

        # Handle collision on right side of object
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.x = tile.x - tile.width / 2 - self.width / 2

        # Handle collision on bottom side of object
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

        # Handle collision on top side of object
        elif self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0

                # Handle collision with mystery box
                if tile.code == MYSTERY_BOX:
                    try:
                        loot = tile.give_loot(level)
                        level.tiles.insert(index, loot)
                    except:
                        pass

        # Handle collision of linked objects
        self.fire_mario.handle_collision(tile, index, level)

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)

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
            self.jump(self.jump_speed)

    # Move right
    def move_right(self, cam_pos, level_length):
        self.facing_left = False

        # Handle animation
        if self.is_grounded:
            if self.state < WALKING_1 or self.state >= WALKING_10:
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
            if self.state < WALKING_1 or self.state >= WALKING_10:
                self.state = WALKING_1
            else:
                if self.timer % self.walk_animation_delay == 0:
                    self.state += 1

        self.timer += 1

        # Update coordinates
        self.direction.x = -self.speed
        if self.x > 0 or cam_pos <= 0:
            self.x += self.direction.x

    def activate_attack_cooldown(self):
        self.state = IDLE
        self.active_cooldown = self.attack_cooldown

    # Attack action
    def attack(self):
        if self.active_cooldown <= 0 and self.visible:
            self.master_sword.attack()
            self.state = ATTACK

    # Let character jump
    def jump(self, speed):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False

    def trigger_new_representation(self, representation):
        if representation == "FIRE_MARIO":
            self.representation = FIRE_MARIO
        # TODO: set timer for representation change

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Start attack
        if is_key_down("shift") and self.is_grounded:
            self.attack()

        # Update weapon attack cooldown
        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        # Update state of linked objects
        self.fire_mario.update(cam_pos, level_length)
        self.master_sword.update(cam_pos, level_length)

    def handle_representation(self):
        # Check if representation should change
        if self.representation_change_timer >= self.representation_change_delay:
            self.representation = LINK
            self.representation_change_timer = 0

            # Disable other representations
            self.fire_mario.visible = False

        # Determine which representation to show
        if self.representation == LINK:
            self.representation_change_timer = 0
            self.visible = True
        elif self.representation == FIRE_MARIO:
            self.visible = False
            self.representation_change_timer += 1
            self.fire_mario.visible = True
        else:
            self.visible = True
            self.representation_change_timer += 1

    # Draw Link
    def draw(self):
        self.handle_representation()
        sprite = self.sprites[self.state]

        # Only draw when visible
        if self.visible:
            image(sprite, self.x, self.y, 1.28, self.facing_left)
            self.master_sword.draw()

        # Draw alternative representations
        self.fire_mario.draw()

    def hit(self, level):
        # TODO: add cool dying animation
        self.lives -= 1
        level.reset()

