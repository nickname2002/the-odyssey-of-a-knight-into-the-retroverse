from GameObject.gameobject import GameObject
from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width, screen_height, tile_size
from jorcademy import *


class EndScene(Level):

    def __init__(self, level_name, chunk_amount, level_backdrop_color):
        super().__init__(level_name, chunk_amount, level_backdrop_color)
        self.zelda = GameObject(
            (screen_width / 2 + 100, screen_height - tile_size * 2 - 97 * 0.7 / 2),
            46 * 0.7,
            97 * 0.7)
        self.end_reached = False
        self.heart = GameObject((screen_width / 2, 0 - 50), 50, 50)
        self.to_subtitles_delay = 300
        self.to_subtitles_timer = 0

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50, 50, self.link)
        self.link.at_game_end = True

    def transition_requested(self):
        pass
        # TODO: Add transition to main menu

    # Make sure the player doesn't move too far to the right
    def stop_moving_link_when_needed(self):
        if self.link.x >= screen_width / 2 - 100:
            self.link.speed = 0
            self.end_reached = True

    def move_world_down(self):
        # Move sprites
        self.link.y += 1
        self.zelda.y += 1
        self.heart.y += 1

        # Move tiles
        for chunk in self.chunks:
            for tile in chunk.tiles:
                tile.y += 1

    def show_heart(self):
        if self.heart.y <= screen_height / 2:
            self.heart.y += 3
        else:
            self.to_subtitles_timer += 1

    def update(self):

        # Update chunks
        chunks_to_update = self.get_chunks_in_range()
        for chunk in chunks_to_update:
            chunk.update(self.cam_pos, self.level_length)

        # Update Link
        self.link.update(self.cam_pos, self.level_length, False)
        self.stop_moving_link_when_needed()

        # Move the map down when needed
        if self.to_subtitles_timer >= self.to_subtitles_delay:
            self.move_world_down()

        # Show the heart when needed
        if self.end_reached:
            self.show_heart()

        # Collision
        self.handle_collision()

    def draw(self):

        # == Background
        backdrop(self.backdrop_color)

        # == Player
        self.link.draw()

        # Zelda
        image("zelda/zelda.png", self.zelda.x, self.zelda.y, 0.7, True, 0)

        # Heart
        if self.end_reached:
            image("other/heart.png", self.heart.x, self.heart.y, 0.2, True, 0)

        # Draw necessary tiles
        chunks_to_draw = self.get_chunks_in_range()
        for chunk in chunks_to_draw:
            chunk.draw(self.screen)

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             25,
             (255, 255, 255),
             100,
             25,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             25,
             (255, 255, 255),
             screen_width / 2,
             25,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             25,
             (255, 255, 255),
             screen_width / 2 + 300,
             25,
             "fonts/pixel.ttf")
