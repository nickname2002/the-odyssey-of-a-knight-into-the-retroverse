from jorcademy import *
from settings import screen_width, screen_height
from level import Level

# Levels
level = Level("1_1")

# TODO: Optimize performance. Performance seems to drop linearly when getting loot from lootboxes.


# Show game over screen
def show_game_over_screen() -> None:
    backdrop((0, 0, 0))
    text("GAME OVER", 50, (255, 255, 255), screen_width / 2, screen_height / 2 - 30, "fonts/pixel.ttf")
    text(f"SCORE: {level.link.score}", 20, (255, 255, 255), screen_width / 2, screen_height / 2 + 20, "fonts/pixel.ttf")


def setup() -> None:
    # Screen properties
    title("Link | The Rescue of Princess Zelda")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    if level.link.lives == 0:
        show_game_over_screen()
        return

    # Draw sky backdrop
    backdrop(level.backdrop_color)

    # Update levels
    level.update()

    # Draw levels
    level.draw()
