from jorcademy import *
from settings import screen_width, screen_height
from level import Level

# Levels
level = Level("1_1")


# TODO: Optimize performance. Performance seems to drop linearly when getting loot from lootboxes.


def setup() -> None:
    # Screen properties
    title("Link | The Rescue of Princess Zelda")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    # Draw sky backdrop
    backdrop(level.backdrop_color)

    # Update levels
    level.update()

    # Draw levels
    level.draw()