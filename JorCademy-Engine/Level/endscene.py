from GameObject.gameobject import GameObject
from Level.level import Level
from Level.triforce_key import TriforceKey
from Support.settings import screen_width, screen_height, tile_size, scale
from jorcademy import *


class EndScene(Level):

    def __init__(self, level_name, chunk_amount, level_backdrop_color):
        super().__init__(level_name, chunk_amount, level_backdrop_color)
        self.subtitles_shown = False
        self.zelda = GameObject(
            (screen_width / 2 + 100 * scale, screen_height - tile_size * 2 - 97 * 0.7 / 2 * scale),
            46 * 0.7 * scale,
            97 * 0.7 * scale)
        self.end_reached = False
        self.heart = GameObject((screen_width / 2, 0 - 50 * scale), 50 * scale, 50 * scale)

        # Transition to subtitles
        self.to_subtitles_delay = 200
        self.to_subtitles_timer = 0

        # Start subtitles
        self.start_subtitles_delay = 600
        self.start_subtitles_timer = 0

        # Switch subtitles
        self.switch_subtitles_delay = 300
        self.switch_subtitles_timer = 0

        # Subtitles index
        self.subtitles_index = 0

    def setup(self, game_screen):
        super().setup(game_screen)
        self.end_game_triforce = TriforceKey((screen_width / 2, 0), 50 * scale, 50 * scale, self.link)
        self.link.at_game_end = True

    def reset(self):
        super().reset()
        self.zelda = GameObject(
            (screen_width / 2 + 100 * scale, screen_height - tile_size * 2 - 97 * 0.7 / 2 * scale),
            46 * 0.7 * scale,
            97 * 0.7 * scale)
        self.heart = GameObject((screen_width / 2, 0 - 50), 50, 50)
        self.link.speed = 4 * scale
        self.subtitles_shown = False
        self.end_reached = False
        self.to_subtitles_timer = 0
        self.start_subtitles_timer = 0
        self.switch_subtitles_timer = 0
        self.subtitles_index = 0
        self.link.at_game_end = True

    def transition_requested(self):
        return self.subtitles_shown

    # Make sure the player doesn't move too far to the right
    def stop_moving_link_when_needed(self):
        if self.link.x >= screen_width / 2 - 100 * scale:
            self.link.speed = 0
            self.end_reached = True

    def move_world_down(self):
        # Move sprites
        self.link.y += 2 * scale
        self.zelda.y += 2 * scale
        self.heart.y += 2 * scale

        # Move tiles
        for chunk in self.chunks:
            for tile in chunk.tiles:
                tile.y += 2 * scale

    def show_heart(self):
        if self.heart.y <= screen_height / 2:
            self.heart.y += 3 * scale
        else:
            self.to_subtitles_timer += 1

    def show_subtitles(self):
        subtitles = [
            # Ending messages for the game
            "LINK'S ODYSSEY HAS COME TO AN END",
            "THANK YOU FOR PLAYING",
            "A GAME BY NICKNAME",
        ]

        # Show correct subtitle
        text(subtitles[self.subtitles_index],
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2,
             screen_height / 2,
             "fonts/pixel.ttf")

        # Update timer
        self.switch_subtitles_timer += 1

        # Switch to next subtitle
        if self.switch_subtitles_timer >= self.switch_subtitles_delay:
            if self.subtitles_index >= len(subtitles) - 1:
                self.subtitles_shown = True
                return

            # Reset timer & change index
            self.subtitles_index += 1
            self.switch_subtitles_timer = 0

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

        # Show subtitles when needed
        self.start_subtitles_timer += 1
        if self.start_subtitles_timer >= self.start_subtitles_delay:
            self.show_subtitles()
            return

        # Collision
        self.handle_collision()

    def draw(self):

        # == Background
        backdrop(self.backdrop_color)

        # == Player
        self.link.draw()

        # Zelda
        image("zelda/zelda.png", self.zelda.x, self.zelda.y, 0.7 * scale, True, 0)

        # Heart
        if self.end_reached:
            image("other/heart.png", self.heart.x, self.heart.y, 0.2 * scale, True, 0)

        # Draw necessary tiles
        chunks_to_draw = self.get_chunks_in_range()
        for chunk in chunks_to_draw:
            chunk.draw(self.screen)

        # Coin amount
        text(f"COINS: {str(self.link.coins)}",
             int(scale * 25),
             (255, 255, 255),
             100 * scale,
             25 * scale,
             "fonts/pixel.ttf")

        # Lives amount
        text(f"LIVES: {str(self.link.lives)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2,
             25 * scale,
             "fonts/pixel.ttf")

        # World number
        text(f"WORLD: {str(self.level_name)}",
             int(scale * 25),
             (255, 255, 255),
             screen_width / 2 + 300 * scale,
             25 * scale,
             "fonts/pixel.ttf")
