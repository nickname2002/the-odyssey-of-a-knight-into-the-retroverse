import string
from Support.settings import screen_width, screen_height, scale
from Support.input import *
from UI.button import Button
from jorcademy import *

pause_button = Button(
    (screen_width / 2, screen_height / 2 + 50 * scale),
    250, 50,
    "GO TO MAIN MENU", 25, (0, 0, 0),
    (255, 255, 255), (240, 240, 240),
    True, 5, (200, 200, 200))

pause_screen_delay = 30
pause_screen_timer = 0


def show_paused_screen(active_level) -> string:
    global pause_screen_timer

    text("PAUSED",
         int(scale * 50),
         (255, 255, 255),
         screen_width / 2,
         screen_height / 2 - 30 * scale,
         "fonts/pixel.ttf")

    if is_nintendo_switch_pro_button_down(SWITCH_D_UP):
        pause_button.selected = True

    # Go back to main menu
    pause_button.update()
    pause_button.draw()

    # Check if user clicked on start new game
    if pause_button.clicked():
        active_level.level_music.fadeout(500)
        return "MAIN_MENU"

    if pause_key_pressed() and pause_screen_timer >= pause_screen_delay:
        pause_screen_timer = 0
        return "GAME"

    pause_screen_timer += 1
    return "PAUSED"
