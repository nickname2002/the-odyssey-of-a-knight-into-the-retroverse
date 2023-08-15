import string
from Support.settings import screen_width, screen_height, scale
from UI.button import Button
from UI.slider import Slider
from jorcademy import *

volume_slider = Slider(
    screen_width / 2,
    screen_height / 2 + 20 * scale,
    500 * scale, 10 * scale,
    (1, 1, 1),
    0, 1, 0.5)

clouds_button = Button(
    (screen_width / 2, screen_height / 2 + 140 * scale),
    500, 50,
    f"CLOUDS {str(settings.clouds).upper()}", 25, (255, 255, 255),
    (1, 1, 1), (50, 50, 50),
    True, 5, (200, 200, 200))

to_main_menu_button = Button(
    (screen_width / 2, screen_height / 2 + 220 * scale),  # Adjust position as needed
    280, 50,  # Button size
    "BACK TO MAIN MENU", 25, (255, 255, 255),  # Text, font size, text color
    (1, 1, 1), (50, 50, 50),  # Button colors (normal, hover)
    True, 5, (200, 200, 200)  # Rounded corners, border size, border color
)

view_displayed_prev_frame = False


# TODO: add support for Nintendo Switch Pro Controller navigation

def show_settings_screen(main_menu_music) -> string:
    global view_displayed_prev_frame

    # Show backdrop
    backdrop((255, 255, 255))

    if not view_displayed_prev_frame:
        clouds_button.clickable = False
        to_main_menu_button.clickable = False
        view_displayed_prev_frame = True

    # Show title
    text("SETTINGS", int(scale * 50), (0, 0, 0),
         screen_width / 2, screen_height / 2 - 150 * scale,
         "fonts/pixel.ttf")

    # Show volume slider
    text("VOLUME", int(scale * 30), (0, 0, 0),
         screen_width / 2 - 200 * scale, screen_height / 2 - 55 * scale,
         "fonts/pixel.ttf")
    volume_slider.draw()
    volume_slider.update()
    settings.volume = volume_slider.value
    main_menu_music.set_volume(0.5 * settings.volume)

    # Show turning on/off clouds button
    text("ENVIRONMENT", int(scale * 30), (0, 0, 0),
         screen_width / 2 - 155 * scale, screen_height / 2 + 80 * scale,
         "fonts/pixel.ttf")
    clouds_button.draw()
    clouds_button.update()

    # Show to main menu button
    to_main_menu_button.draw()
    to_main_menu_button.update()

    # Main menu action
    if clouds_button.clicked():
        settings.clouds = not settings.clouds
        clouds_button.content = "CLOUDS: " + str(settings.clouds).upper()

    # Go to main menu when button is clicked
    if to_main_menu_button.clicked():
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    # De-activate settings screen
    if is_key_down("esc"):
        view_displayed_prev_frame = False
        return "MAIN_MENU"

    return "SETTINGS"
