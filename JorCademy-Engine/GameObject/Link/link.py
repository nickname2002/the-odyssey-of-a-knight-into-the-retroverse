from Environment.text_anomaly import TextAnomaly
from GameObject.Link.Weapons.master_sword import MasterSword
from GameObject.Link.fire_mario import FireMario
from GameObject.Link.pac_man import PacMan
from GameObject.gameobject import GameObject
from Level.Tiles.tile_data import *
from Support.settings import screen_width, screen_height, scale, tile_size
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
DEAD = 13


# Representations for Link
LINK = 0
FIRE_MARIO = 1
PAC_MAN = 2


class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.lives = 3
        self.coins = 0  # NOTE: maybe change coins into rupees
        self.orig_speed = 4 * scale
        self.speed = 4 * scale
        self.facing_left = False
        self.jump_speed = -15 * scale
        self.is_grounded = False
        self.walk_animation_delay = 3
        self.state = IDLE
        self.representation = FIRE_MARIO
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.master_sword = MasterSword((self.x, self.y), 45 * scale, 33 * scale, self)
        self.visible = True
        self.fire_mario = FireMario((self.x, self.y), 32 * scale, 64 * scale, self)
        self.pac_man = PacMan((self.x, self.y), 48 * scale, 48 * scale, self)
        self.representation_change_timer = 0
        self.representation_change_delay = 1000
        self.killed = False
        self.max_speed = 0.8 * scale
        self.at_game_end = False
        self.coins_earned_current_level = 0
        self.die_state_index = DEAD
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
            'link/link_jumping.png',
            "link/link_dead.png"
        ]

        # Load sounds
        self.jump_sound = load_sound('assets/sounds/link/jump.ogg')
        self.one_up_sound = load_sound("assets/sounds/power_ups/1_up.ogg")
        self.death_sound = load_sound("assets/sounds/link/link_death_sound.ogg")  # TODO: find improved dead sound

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
                        level.get_current_chunk().tiles.insert(loot.index, loot)
                    except:
                        pass

                elif tile.code in BREAKABLE:
                    tile.break_tile(level.get_right_sky_tile())

        # Handle collision of linked objects
        self.fire_mario.handle_collision(tile, index, level)

    def handle_movement(self, cam_pos, level_length, at_level_end=False):
        super().handle_movement(cam_pos, level_length)
        if self.x < screen_width / 2 or cam_pos >= (level_length - screen_width):
            self.x += self.direction.x * self.speed

        # Prevent movement if at end of level
        if at_level_end or self.speed == 0:
            self.state = IDLE
            return

        # Update horizontal direction and position of Link
        if is_key_down("d") or is_key_down('right') and not is_key_down('shift'):
            self.move_right(cam_pos, level_length)
        elif is_key_down("a") or is_key_down('left') and not is_key_down("shift"):
            self.move_left(cam_pos)
        elif self.is_grounded:
            self.state = IDLE

        # Update the vertical position of Link
        if is_key_down("space") or is_key_down("up") or is_key_down("w"):
            self.jump(self.jump_speed)

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
        if abs(self.direction.x) < self.max_speed:
            self.direction.x += 0.25 * scale

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
        if abs(self.direction.x) < self.max_speed:
            self.direction.x -= 0.25 * scale

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
    def jump(self, speed, enemy_killed=False):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False
            if not enemy_killed and self.representation == LINK:
                play_sound(self.jump_sound, 0.6)
            elif not enemy_killed and self.representation == FIRE_MARIO:
                play_sound(self.fire_mario.jump_sound, 1.5)

    def trigger_new_representation(self, representation):
        if representation == "FIRE_MARIO":
            self.representation = FIRE_MARIO
        elif representation == "PAC_MAN":
            self.representation = PAC_MAN

    def change_velocity(self):
        if abs(self.direction.x) < 0.1:
            self.direction.x = 0
            return

        if self.direction.x < 0:
            self.direction.x += 0.1
        elif self.direction.x > 0:
            self.direction.x -= 0.1

    def make_text_anomaly(self, level, message):
        anomaly_pos = (self.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, message, 20, (255, 255, 255))
        level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def handle_1up_with_coins(self, level):
        if self.coins + self.coins_earned_current_level >= 2500:
            self.coins = 0
            self.coins_earned_current_level = 0
            self.lives += 1
            self.make_text_anomaly(level, "+1 UP")
            play_sound(self.one_up_sound, 0.5)

    def update(self, cam_pos, level, at_level_end=False):
        # Update state of linked representations
        self.fire_mario.update(cam_pos, level.level_length)
        self.pac_man.update(cam_pos, level.level_length)

        # Handle Link DEAD state
        if self.killed:

            if self.visible:
                self.play_death_sound()

            self.y = self.die_y + self.height / 2 - 15 * scale
            self.show_die_animation()
            return

        # Update position
        self.handle_movement(cam_pos, level.level_length, at_level_end)
        self.change_velocity()

        # Die when out of screen
        if self.y > screen_height:
            self.die()

        # Update lives with respect to coins
        self.handle_1up_with_coins(level)

        # Start attack
        if is_key_down("shift") and self.is_grounded:
            self.attack()

        # Update weapon attack cooldown
        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        # Update state of linked objects
        self.master_sword.update(cam_pos, level.level_length)

    def activate_main_representation(self):
        self.jump(self.jump_speed / 2)
        self.representation = LINK
        self.height = 64 * scale
        self.representation_change_timer = 0

        # Disable other representations
        self.fire_mario.visible = False
        self.pac_man.visible = False

    def activate_alt_representation(self, representation):
        self.visible = False
        self.representation_change_timer += 1

        # Activate alt representation
        if representation == FIRE_MARIO:
            self.fire_mario.visible = True
            self.height = self.fire_mario.height
            self.pac_man.visible = False
        elif representation == PAC_MAN:
            self.height = self.pac_man.height
            self.fire_mario.visible = False
            self.pac_man.visible = True

    def handle_representation(self):
        # Check if representation should change
        if self.representation_change_timer >= self.representation_change_delay:
            self.activate_main_representation()

        # Determine which representation to show
        if self.representation == LINK:
            self.representation_change_timer = 0
            self.visible = True
        elif self.representation == FIRE_MARIO:
            self.reset_representation_timer(self.fire_mario)
            self.activate_alt_representation(FIRE_MARIO)
        elif self.representation == PAC_MAN:
            self.reset_representation_timer(self.pac_man)
            self.activate_alt_representation(PAC_MAN)
        else:
            self.visible = True
            self.representation_change_timer += 1

    def reset_representation_timer(self, representation_object):
        if not representation_object.visible:
            self.jump(self.jump_speed / 2)
            self.representation_change_timer = 0

    # Draw Link
    def draw(self):
        self.handle_representation()
        sprite = self.sprites[self.state]

        # Only draw when visible
        if self.visible:
            image(sprite, self.x, self.y, 1.28 * scale, self.facing_left)
            self.master_sword.draw()

        # Draw alternative representations
        self.fire_mario.draw()
        self.pac_man.draw()

    def die(self, level=None):
        if not self.killed:
            self.die_y = self.y

        if not self.at_game_end:
            self.lives -= 1
            self.killed = True

    def soft_reset(self):
        self.x = 100
        self.y = screen_height / 2
        self.gravity = 0.8 * scale
        self.die_animation_timer = 0
        self.speed = self.orig_speed
        self.killed = False
        self.coins_earned_current_level = 0
        self.activate_main_representation()

    def hard_reset(self):
        self.coins = 0
        self.lives = 3
        self.soft_reset()
