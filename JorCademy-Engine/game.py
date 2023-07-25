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
    backdrop((255, 255, 255))
    # NOTE: setting up level happend in main.py


def update() -> None:
    # Update levels
    level.update()

    # Draw levels
    level.draw()