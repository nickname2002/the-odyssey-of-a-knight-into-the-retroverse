from Environment.text_anomaly import TextAnomaly
from GameObject.gameobject import GameObject
from Support.settings import screen_width, screen_height, tile_size


class Monster(GameObject):

    def __init__(self, pos, w, h, player, level):
        super().__init__(pos, w, h)
        self.orig_pos = pos
        self.sprite_set = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.sel_sprite_index = 0
        self.offset = 0
        self.moving = False
        self.player = player
        self.message = "+20 SCORE"
        self.level = level
        self.killed = False
        self.loot = 100
        self.health = 1

    def is_out_of_frame(self):
        if self.moving:
            return \
                self.x < 0 - self.width and \
                (self.y < 0 - self.width or self.y > screen_height + self.height)

    def make_text_anomaly(self):
        anomaly_pos = (self.level.link.x, self.y - tile_size)
        new_text_anomaly = TextAnomaly(anomaly_pos, self.message, 20, (255, 255, 255))
        self.level.update_text_anomalies(new_text_anomaly)

    def in_frame(self):
        return self.x + self.width > 0 and self.x - self.width < screen_width

    def die(self):
        if not self.killed:
            self.make_text_anomaly()
            self.player.coins += self.loot

        self.killed = True

    def handle_collision_with_player(self, level):
        fireball = self.player.fire_mario.fireball

        # Check if fireball is visible and if it collides with the monster
        if fireball.visible:
            if self.collision(fireball):
                self.health -= 1
                fireball.visible = False

        # Process this object's damage
        if self.collision_top(self.player) and self.player.collision_bottom(self):

            # Kill monster
            if not self.killed:
                self.health -= 1

            # Make player jump when landing on top of monster
            self.player.is_grounded = True
            self.player.jump(self.player.jump_speed + 4)

        # Process player damage
        elif self.collision(self.player):
            if not self.player.killed:
                self.player.die(level)

        # Make sure to die if health is 0
        if self.health <= 0:
            self.die()

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)
        self.correct_position_with_camera(cam_pos)
        self.timer += 1

        if (self.x - self.width) - self.player.x < screen_width / 2:
            self.moving = True