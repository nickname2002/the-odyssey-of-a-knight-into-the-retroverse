from Environment.text_anomaly import TextAnomaly
from GameObject.gameobject import GameObject
from Support.settings import screen_width, screen_height, tile_size
import random
from jorcademy import *


class Monster(GameObject):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h)
        self.chunk = chunk
        self.orig_pos = pos
        self.sprite_set = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.state = 0
        self.offset = 0
        self.moving = False
        self.player = player
        self.message = "+20 COINS"
        self.level = level
        self.killed = False
        self.loot = 20
        self.health = 1

        # Jump delay
        self.jump_timer = 0
        self.min_jump_delay = 60 * 1
        self.max_jump_delay = 60 * 4
        self.random_jump_delay = random.randint(self.min_jump_delay, self.max_jump_delay)

        # Attack delay
        self.invincible_timer = 0
        self.invincible_delay = 1000
        self.attack_timer = 0
        self.min_attack_delay = 60 * 5
        self.max_attack_delay = 60 * 10
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

        # Sounds
        self.hit_by_player_sound = load_sound("assets/sounds/monsters/enemy_jump.ogg")
        self.hit_by_sword_sound = load_sound("assets/sounds/link/punch.ogg")

    def is_out_of_frame(self):
        if self.moving:
            return \
                self.x < 0 - self.width and \
                (self.y < 0 - self.width or self.y > screen_height + self.height)

    def ready_to_remove(self):
        return self.is_out_of_frame() or \
            self.die_animation_timer >= self.die_animation_delay

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.get_current_chunk().update_text_anomalies(new_text_anomaly)

    def in_frame(self):
        return self.x + self.width > 0 and self.x - self.width < screen_width

    def die(self):
        if not self.killed:
            self.die_y = self.y
            self.make_text_anomaly()
            self.player.coins_earned_current_level += self.loot

        self.killed = True

    def handle_collision_with_player(self, level):
        self.invincible_timer -= 1

        # Check if fireball is visible and if it collides with the monster
        for fireball in self.player.fire_mario.fireballs:
            if ((self.collision(fireball) and
                    self.invincible_timer <= 0) and
                    not self.killed):
                play_sound(self.hit_by_player_sound, 0.5)
                self.health -= 1
                self.invincible_timer = self.invincible_delay
                fireball.killed = True

        # Process this object's damage
        if self.collision_top(self.player) and self.player.collision_bottom(self):

            # Kill monster
            if not self.killed and self.invincible_timer <= 0:
                play_sound(self.hit_by_player_sound, 0.5)
                self.invincible_timer = self.invincible_delay
                self.health -= 1

                # Make player jump when landing on top of monster
                self.player.is_grounded = True
                self.player.jump(self.player.jump_speed + 4, True)

        # Process player damage
        elif self.collision(self.player) and not self.killed:
            if not self.player.killed:
                self.player.die(level)

        # Make sure to die if health is 0
        if self.health <= 0:
            self.die()

    def handle_collision_with_sword(self):
        if self.player.master_sword.collision(self) and \
                self.player.master_sword.visible and \
                self.invincible_timer <= 0:
            play_sound(self.hit_by_sword_sound, 1)
            self.health -= 1
            self.invincible_timer = self.invincible_delay

    def init_new_attack_delay(self):
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

    def init_new_jump_delay(self):
        self.random_jump_delay = random.randint(self.min_jump_delay, self.max_jump_delay)

    def init_new_jump_speed(self):
        self.jump_speed = random.randint(-13, -5)

    def move_horizontally(self):
        self.offset += self.direction.x * self.speed

    def update(self, cam_pos, level_length):
        if not self.killed:
            super().update(cam_pos, level_length)

        self.correct_position_with_camera(cam_pos)
        self.timer += 1

        if (self.x - self.width) - self.player.x < screen_width / 2:
            self.moving = True
