from gameobject import GameObject
from jorcademy import image


class Monster(GameObject):

    def __init__(self, pos, w, h):
        super().__init__(pos, w, h)
        self.orig_pos = pos
        self.spriteset = []
        self.timer = 0
        self.walk_animation_delay = 10
        self.sel_sprite_index = 0


    def update(self, cam_pos):
        self.x = self.orig_pos[0] - cam_pos
        self.timer += 1


    def draw(self):
        if self.timer % self.walk_animation_delay == 0:
            self.update_sprite_state()        
            
        image(self.spriteset[self.sel_sprite_index], self.x, self.y, 1) 


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


    def draw(self):
        super().draw()
        image(self.spriteset[self.sel_sprite_index], self.x, self.y - self.height / 6, 3) 

    