import string
from Support.settings import scale, screen_width, screen_height
from jorcademy import *


def show_controls_screen() -> string:
    backdrop((0, 0, 0))

    text("CONTROLS", int(scale * 50), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")
    text("MOVE: ARROW KEYS & WASD", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 50 * scale,
         "fonts/pixel.ttf")
    text("JUMP: SPACE", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2,
         "fonts/pixel.ttf")
    text("ATTACK: SHIFT", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 50 * scale,
         "fonts/pixel.ttf")
    text("PAUSE: ESCAPE", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 100 * scale,
         "fonts/pixel.ttf")
    text("PRESS ENTER TO START", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 200 * scale,
         "fonts/pixel.ttf")

    # Go to game when enter is pressed
    if is_key_down("return"):
        return "TRANSITION_FROM_MAIN_MENU"

    return "CONTROLS"
