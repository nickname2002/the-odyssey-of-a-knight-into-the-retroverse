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


    def update(self):
        self.handle_movement()


    def handle_movement(self):
        # Update direction & position
        if is_key_down("d"):
            self.move_right()
        elif is_key_down("a"):
            self.move_left()
        else: 
            self.direction.x = 0
        
        if is_key_down("space"):
            self.jump()

        self.apply_gravity()


    def move_right(self):
        self.direction.x = self.speed
        if self.x < screen_width / 2:
            self.x += self.direction.x


    def move_left(self):
        self.direction.x = -self.speed
        if self.x > screen_width / 4:
            self.x += self.direction.x


    def apply_gravity(self):
        if self.direction.y < 5:

            self.direction.y += self.gravity
        self.y += self.direction.y


    def jump(self):
        self.direction.y = self.jump_speed


    def draw(self):
        rect((255, 50, 50), self.x, self.y, self.width, self.height)