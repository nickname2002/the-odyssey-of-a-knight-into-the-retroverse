from gameobject import GameObject
from settings import screen_width
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

class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.score = 0
        self.lives = 3
        self.coins = 0                  # NOTE: maybe change coins into rupees
        self.orig_speed = 4
        self.speed = 4
        self.facing_left = False
        self.jump_speed = -13 
        self.is_grounded = False
        self.walk_animation_delay = 3
        self.state = IDLE
        self.attack_cooldown = 50
        self.active_cooldown = 0
        self.master_sword= MasterSword((self.x, self.y), 45, 33, self)
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
        if self.x > 0 or cam_pos <= 0:
            self.x += self.direction.x


    def activate_attack_cooldown(self):
        self.state = IDLE
        self.active_cooldown = self.attack_cooldown


    # Attack action
    def attack(self):
        if self.active_cooldown <= 0:
            self.master_sword.attack()
            self.state = ATTACK


    # Let character jump
    def jump(self, speed):
        self.timer = 0
        self.state = JUMPING
        if self.is_grounded:
            self.direction.y = speed
            self.is_grounded = False


    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        if is_key_down("shift") and self.is_grounded:
            self.attack()

        if self.active_cooldown > 0:
            self.active_cooldown -= 1

        self.master_sword.update(cam_pos, level_length)


    # Draw Link
    def draw(self):
        sprite = self.sprites[self.state]
        image(sprite, self.x, self.y, 1.28, self.facing_left)
        self.master_sword.draw()


    def hit(self, level):
        # TODO: make sure player has less lives and level is reset
        pass 


class MasterSword(GameObject):

    def __init__(self, pos, w, h, player):
        super().__init__(pos, w, h)
        self.visible = False
        self.timer = 0 
        self.attack_animation_delay = 20
        self.sword_reach = 10
        self.sprite = "link/master_sword.png"
        self.player = player
        self.gravity = 0
        self.rotation = 100


    def attack(self):
        self.x = self.player.x + 30
        self.y = self.player.y + 10
        self.visible = True 
        

    def update(self, cam_pos, level_length):
        super().update(cam_pos, level_length)

        # Make sure the collider is positioned properly
        # based on the orientation of the player
        if self.player.facing_left == False:
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
            if self.player.facing_left == False:
                image(self.sprite, self.x - 20, self.y, 0.15, False, self.rotation)
            else:
                image(self.sprite, self.x, self.y, 0.15, False, self.rotation + 160)

