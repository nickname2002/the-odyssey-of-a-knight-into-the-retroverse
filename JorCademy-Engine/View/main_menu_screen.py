import string
from Support.settings import screen_width, screen_height, scale
from UI.button import Button
from jorcademy import *

# UI components
start_button = Button(
    (screen_width / 2, screen_height / 2 + 90 * scale),
    275, 50,
    "START NEW GAME", 30, (0, 255, 255),
    (1, 1, 1), (50, 50, 50),
    True, 5, (255, 0, 0))

settings_button = Button(
    (screen_width / 2, screen_height / 2 + 150 * scale),
    275, 50,
    "SETTINGS", 30, (0, 255, 255),
    (1, 1, 1), (50, 50, 50),
    True, 5, (255, 0, 0))

# Music
main_menu_music = load_sound("assets/music/main_menu.ogg")


def show_main_menu_screen(active_level) -> string:
    # Stop music in active level
    active_level.level_music.fadeout(500)

    # Play music
    if not main_menu_music.get_num_channels() > 0:
        main_menu_music.play(-1)
        main_menu_music.set_volume(0.5 * settings.volume)

    # Draw menu
    backdrop((255, 255, 255))
    image("other/main_menu_backdrop_light.png",
          screen_width / 2,
          screen_height / 2,
          1.0 * scale)
    image("icons/odyssey-of-a-knight-into-retroverse.png",
          screen_width / 2,
          screen_height / 2 - 100 * scale,
          0.85 * scale)
    text("BY NICKNAME", int(scale * 30), (0, 0, 0),
         screen_width / 2, screen_height / 2 + 20 * scale,
         "fonts/pixel.ttf")

    # Update start button
    start_button.update()
    start_button.draw()

    # Update settings button
    settings_button.update()
    settings_button.draw()

    # Check if user clicked on start new game
    if start_button.clicked():
        active_level.link.hard_reset()
        active_level.reset()
        return "STARTING_MESSAGES"

    # Check if user clicked on settings
    if settings_button.clicked():
        return "SETTINGS"

    return "MAIN_MENU"
