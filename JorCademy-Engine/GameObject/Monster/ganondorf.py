from GameObject.Monster.monster import Monster
from GameObject.Monster.Weapons.enemy_fireball import EnemyFireBall
from jorcademy import *
import random

# Ganondorf states
IDLE = 0
WALKING_1 = 1
WALKING_2 = 2
WALKING_3 = 3
WALKING_4 = 4
WALKING_5 = 5
WALKING_6 = 6
SHORT_RANGE_ATTACK_1 = 7
SHORT_RANGE_ATTACK_2 = 8
SHORT_RANGE_ATTACK_3 = 9
LONG_RANGE_ATTACK = 10


class Ganondorf(Monster):

    def __init__(self, pos, w, h, player, level, chunk):
        super().__init__(pos, w, h, player, level, chunk)
        self.sprite_set = [
            "monsters/ganondorf/ganondorf_idle_1.png",
            "monsters/ganondorf/ganondorf_walking_1.png",
            "monsters/ganondorf/ganondorf_walking_2.png",
            "monsters/ganondorf/ganondorf_walking_3.png",
            "monsters/ganondorf/ganondorf_walking_4.png",
            "monsters/ganondorf/ganondorf_walking_5.png",
            "monsters/ganondorf/ganondorf_walking_6.png",
            "monsters/ganondorf/ganondorf_short_attack_1.png",
            "monsters/ganondorf/ganondorf_short_attack_2.png",
            "monsters/ganondorf/ganondorf_short_attack_3.png",
            "monsters/ganondorf/ganondorf_long_attack.png"
        ]
        self.state = IDLE
        self.speed = 1
        self.health = 10

        # Idle delay
        self.idle_timer = 0
        self.random_idle_delay = random.randint(150, 600)

        # Walking delay
        self.walk_animation_delay = 10
        self.walk_animation_timer = 0
        self.walking_timer = 0
        self.random_walking_delay = random.randint(100, 150)

        # Short range attack
        self.short_range_attack_activated = False
        self.short_range_attack_speed = 3
        self.short_range_attack_timer = 0
        self.short_range_attack_delay = 50
        self.short_range_attack_activation_distance = 200
        self.short_range_attack_animation_delay = 50 / 3
        self.short_range_attack_animation_timer = 0

        # Long range attack
        self.long_range_attack_activated = False
        self.long_range_attack_speed = 3
        self.long_range_attack_timer = 0
        self.long_range_attack_delay = 50
        self.long_range_attack_activation_distance = 200
        self.long_range_attack_animation_delay = 50 / 3
        self.long_range_attack_animation_timer = 0

        # Attack delay
        self.invincible_delay = 1000
        self.attack_timer = 0
        self.min_attack_delay = 60 * 5
        self.max_attack_delay = 60 * 10
        self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)

    def update_sprite_state(self):

        # Idle
        if self.state == IDLE:
            return

        # Short range attack
        elif self.short_range_attack_activated:

            # Activate first short range attack state by default
            if self.state < SHORT_RANGE_ATTACK_1 or self.state > SHORT_RANGE_ATTACK_3:
                self.state = SHORT_RANGE_ATTACK_1

            # Change state
            if self.short_range_attack_timer >= self.short_range_attack_animation_delay:
                self.short_range_attack_animation_timer = 0

                # Activate next frame
                if self.state < SHORT_RANGE_ATTACK_3:
                    self.state += 1

            # Update timer
            self.short_range_attack_animation_timer += 1

        # Long range attack
        elif self.long_range_attack_activated:
            pass

        # Walking
        else:
            # Increase timers
            self.walk_animation_timer += 1

            # Switch states
            if self.walk_animation_timer >= self.walk_animation_delay:
                self.walk_animation_timer = 0
                self.state += 1
                if self.state > WALKING_6:
                    self.state = WALKING_1

    def handle_collision(self, tile, _, level):
        # Handle collision on left side of monster
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.direction.x *= -1

        # Handle collision on right side of monster
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.direction.x *= -1

        # Handle collision on bottom side of monster
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0

            self.is_grounded = True

        # Handle collision on top side of monster
        elif self.collision_top(tile):
            if self.direction.y < 0:
                self.y = tile.y + tile.height / 2 + self.height / 2
                self.direction.y = 0

        # Player game events
        self.handle_collision_with_player(level)
        self.handle_collision_with_sword()

    def face_towards_player(self):
        if self.player.x > self.x:
            self.direction.x = 1
        else:
            self.direction.x = -1

    def get_direction(self):
        # Get the difference between the monster and the player positions
        x_diff = self.player.x - self.x
        y_diff = self.player.y - self.y

        # Form vector
        vec = pygame.Vector2(x_diff, y_diff)
        vec.normalize_ip()

        return vec

    def get_distance_from_player(self):
        return abs(self.player.x - self.x)

    def attack(self):
        pass

    def init_new_walking_delay(self):
        self.random_walking_delay = random.randint(150, 600)

    def init_idle_delay(self):
        self.random_idle_delay = random.randint(100, 150)

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)

        # Perform short range attack if needed
        if self.get_distance_from_player() < self.short_range_attack_activation_distance and \
                self.attack_timer >= self.random_attack_delay:
            self.perform_short_range_attack()
            return
        # Perform long range attack
        elif self.attack_timer >= self.random_attack_delay:
            self.perform_long_range_attack()
            return

        # Update attack cooldown timer
        self.attack_timer += 1

        # Movement behavior based on state
        if self.state == IDLE:
            self.process_idle_state()
        else:
            self.process_walk_state()

    def process_idle_state(self):
        # Check if the timer is up
        if self.idle_timer >= self.random_idle_delay:
            # Reset timer
            self.idle_timer = 0

            # Reset state
            self.state = WALKING_1

            # Reset idle delay
            self.init_idle_delay()

        # Stop moving
        self.direction.x = 0

        # Update timer
        self.idle_timer += 1

    def process_walk_state(self):
        # Check if the timer is up
        if self.walking_timer >= self.random_walking_delay:
            # Reset timer
            self.walking_timer = 0

            # Reset state
            self.state = IDLE

            # Reset walking delay
            self.init_new_walking_delay()

        # Move monster
        self.face_towards_player()
        self.move_horizontally()

        # Update walking timer
        self.walking_timer += 1

    def perform_short_range_attack(self):
        # Check if the timer is up
        if self.short_range_attack_timer >= self.short_range_attack_delay:
            # Reset timer
            self.short_range_attack_timer = 0

            # Reset state
            self.state = IDLE
            self.short_range_attack_activated = False

            # Reset attack delay
            self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)
            self.attack_timer = 0
            self.short_range_attack_animation_timer = 0

            # Reset speed
            self.speed = 1
            return

        self.short_range_attack_activated = True
        if self.state == IDLE:
            self.state = SHORT_RANGE_ATTACK_1

        # Change movement speed
        self.speed = self.short_range_attack_speed

        # Move monster
        self.face_towards_player()
        self.move_horizontally()

        # Update timer
        self.short_range_attack_timer += 1

    def perform_long_range_attack(self):
        # Check if the timer is up
        if self.long_range_attack_timer >= self.long_range_attack_delay:
            # Reset timer
            self.long_range_attack_timer = 0

            # Reset state
            self.state = IDLE
            self.long_range_attack_activated = False

            # Reset attack delay
            self.random_attack_delay = random.randint(self.min_attack_delay, self.max_attack_delay)
            self.attack_timer = 0

            # Reset speed
            self.speed = 1
            return

        # Activate long range attack state
        self.long_range_attack_activated = True
        self.state = LONG_RANGE_ATTACK

        # Make monster stand still
        self.direction.x = 0

        # Shoot fireball
        self.chunk.monsters.append(
            EnemyFireBall((self.x, self.y), 16, 16, self, self.player, self.get_direction()))

        # Update timer
        self.long_range_attack_timer += 1

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.handle_movement(cam_pos, level_length)
        self.update_sprite_state()

    def draw(self):
        # Make sure the monster is drawn facing the right direction
        image(self.sprite_set[self.state], self.x, self.y, 1.5, self.player.x >= self.x)
