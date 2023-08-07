from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width, scale
from jorcademy import *


class BossLevel(Level):

    def __init__(self, level_name, chunk_amount, level_backdrop_color, boss_type):
        super().__init__(level_name, chunk_amount, level_backdrop_color)
        self.end_game_triforce = None
        self.boss_type = boss_type
        self.boss = None
        self.die_sound_played = False
        self.boss_die_sound = load_sound("assets/sounds/ganondorf_die.mp3")

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50, 50, self.link)

        # Move Link
        self.link.x += 30 * scale

        # Record the boss
        for chunk in self.chunks:
            for monster in chunk.monsters:
                if type(monster) == self.boss_type:
                    self.boss = monster

    def reset(self):
        super().reset()
        self.link.at_game_end = True
        self.end_game_triforce.moving_allowed = False

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

            # Play boss kill sound
            if not self.die_sound_played:
                play_sound(self.boss_die_sound, 0.5)
                self.die_sound_played = True

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
             int(25 * scale),
             (255, 255, 255),
             100 + 55 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             int(25 * scale),
             (255, 255, 255),
             screen_width / 2 + 10 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             int(25 * scale),
             (255, 255, 255),
             screen_width / 2 + 300 * scale - 70 * scale,
             25 + 25 * scale,
             "fonts/pixel.ttf")
