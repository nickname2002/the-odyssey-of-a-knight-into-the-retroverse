from gameobject import GameObject
from tile_data import *
from jorcademy import image
from settings import screen_width
import pygame


class Monster(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.orig_pos = pos
        self.spriteset = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.sel_sprite_index = 0
        self.offset = 0
        self.moving = False


    def update(self, cam_pos, level_length, player):
        super().update(cam_pos, level_length)
        self.x = self.orig_pos[0] - cam_pos
        self.x += self.offset
        self.timer += 1

        if self.x - player.x < screen_width / 2:
            self.moving = True


    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()        
            

    def update_sprite_state(self):
        if self.sel_sprite_index < len(self.spriteset) - 1:
            self.sel_sprite_index += 1
        else:
            self.sel_sprite_index = 0


class Bokoblin(Monster):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.spriteset = [
            "monsters/bokoblin/bokoblin_1.png",
            "monsters/bokoblin/bokoblin_2.png"
        ]
        self.speed = 1
        self.direction = pygame.Vector2(-self.speed, 0)


    def handle_collision(self, tile, index, level):
        # Handle collision on left side of Link
        if self.collision_left(tile):
            if self.direction.x < 0:
                self.direction.x *= -1
    
        # Handle collision on right side of Link
        elif self.collision_right(tile):
            if self.direction.x > 0:
                self.direction.x *= -1

        # Handle collision on bottom side of Link
        if self.collision_bottom(tile):
            if self.direction.y > 0:
                self.y = tile.y - tile.height / 2 - self.height / 2
                self.direction.y = 0
                
            self.is_grounded = True

        # Handle collision on top side of Link
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
        

    def handle_movement(self, cam_pos, level_length):
        super().handle_movement(cam_pos, level_length)
        if self.moving:
            self.offset += self.direction.x * self.speed


    def draw(self): 
        super().draw()

        if self.direction.x > 0:
            image(self.spriteset[self.sel_sprite_index], self.x, self.y, 3) 
        else:
            image(self.spriteset[self.sel_sprite_index], self.x, self.y, 3, True)

    