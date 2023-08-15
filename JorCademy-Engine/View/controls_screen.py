import string

from Support.input import return_key_pressed
from Support.settings import scale, screen_width, screen_height
from jorcademy import *


def show_controls_screen() -> string:
    backdrop((0, 0, 0))

    text("CONTROLS", int(scale * 50), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")
    text("MOVE: ARROW KEYS/WAS/D-PAD", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 50 * scale,
         "fonts/pixel.ttf")
    text("JUMP: SPACE/B/A", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2,
         "fonts/pixel.ttf")
    text("ATTACK: SHIFT/Y", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 50 * scale,
         "fonts/pixel.ttf")
    text("PAUSE: ESCAPE/X", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 100 * scale,
         "fonts/pixel.ttf")
    text("PRESS ENTER/A TO START", int(scale * 30), (255, 255, 255),
         screen_width / 2, screen_height / 2 + 200 * scale,
         "fonts/pixel.ttf")

    # Go to game when enter is pressed
    if return_key_pressed():
        return "TRANSITION_FROM_MAIN_MENU"

    return "CONTROLS"
