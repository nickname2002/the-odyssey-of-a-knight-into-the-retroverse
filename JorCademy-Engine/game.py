from jorcademy import *
from settings import screen_width, screen_height, tilemap_list
from level import Level

# Levels
level = Level(tilemap_list, "1_1")


def setup() -> None:
    # Screen properties
    title("Link | The Rescue of Princess Zelda")
    screen(screen_width, screen_height)
    backdrop((255, 255, 255))

    # Setup levels
    level.setup()
    #level.import_tiles("maps/tileset.png")


def update() -> None:
    # Update levels
    level.update()

    # Draw levels
    level.draw()