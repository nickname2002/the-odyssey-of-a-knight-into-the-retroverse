from gameobject import GameObject
from settings import screen_width
from jorcademy import *

class Link(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.speed = 3
        self.direction = pygame.Vector2(0, 0)
        self.gravity = 0.2
        self.jump_speed = -5


    def update(self, cam_pos, level_length):
        self.handle_movement(cam_pos, level_length)


    def handle_movement(self, cam_pos, level_length):
        # Update direction & position
        if is_key_down("d"):
            self.move_right(cam_pos, level_length)
        elif is_key_down("a"):
            self.move_left(cam_pos)
        else: 
            self.direction.x = 0
        
        if is_key_down("space"):
            self.jump()

        self.apply_gravity()


    def move_right(self, cam_pos, level_length):
        self.direction.x = self.speed
        if self.x < screen_width / 2 or cam_pos >= (level_length - screen_width):
            self.x += self.direction.x


    def move_left(self, cam_pos):
        self.direction.x = -self.speed
        if self.x > screen_width / 4 or cam_pos <= 0:
            self.x += self.direction.x


    def apply_gravity(self):
        if self.direction.y < 5:
            self.direction.y += self.gravity
        self.y += self.direction.y


    def jump(self):
        self.direction.y = self.jump_speed


    def draw(self):
        rect((255, 50, 50), self.x, self.y, self.width, self.height)