from GameObject.Monster.ganondorf import Ganondorf
from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width
from jorcademy import *


class BossLevel(Level):

    def __init__(self, level_name, chunk_amount, level_backdrop_color, boss_type):
        super().__init__(level_name, chunk_amount, level_backdrop_color)
        self.end_game_triforce = None
        self.boss_type = boss_type
        self.boss = None

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50, 50, self.link)

        # Record the boss
        for chunk in self.chunks:
            for monster in chunk.monsters:
                if type(monster) == self.boss_type:
                    self.boss = monster

    def transition_requested(self):
        return self.link.killed or self.end_game_triforce.reached

    def update(self):

        # Update chunks in range
        chunks_to_update = self.get_chunks_in_range()
        for chunk in chunks_to_update:
            chunk.update(self.cam_pos, self.level_length)

        # Update player
        self.link.update(self.cam_pos, self.level_length, False)

        # Update endgame triforce
        print(self.boss.killed)
        if self.boss.killed:
            self.end_game_triforce.moving_allowed = True
        self.end_game_triforce.update(self.cam_pos, self.level_length)

        # Collision
        self.handle_collision()

    def draw(self):

        # == Background
        backdrop(self.backdrop_color)

        # == Player
        self.link.draw()

        # Draw necessary tiles and monsters
        chunks_to_draw = self.get_chunks_in_range()
        for chunk in chunks_to_draw:
            chunk.draw(self.screen)

        # Draw triforce key
        self.end_game_triforce.draw()

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             25,
             (255, 255, 255),
             100 + 55,
             25 + 25,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             25,
             (255, 255, 255),
             screen_width / 2 + 10,
             25 + 25,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             25,
             (255, 255, 255),
             screen_width / 2 + 300 - 70,
             25 + 25,
             "fonts/pixel.ttf")
