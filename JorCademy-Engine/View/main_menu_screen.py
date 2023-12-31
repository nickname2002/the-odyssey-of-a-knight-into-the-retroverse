import string
from Support.settings import screen_width, screen_height, scale
from Support.input import *
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

menu_buttons = [start_button, settings_button]
selected_index = None

# Music
main_menu_music = load_sound("assets/music/main_menu.ogg")

# Images
menu_backdrop = None
logo = None


def load_main_menu_images():
    global menu_backdrop, logo
    menu_backdrop = load_image("other/main_menu_backdrop_light.png")
    logo = load_image("icons/odyssey-of-a-knight-into-retroverse.png")


def decrease_selected_button_index():
    global selected_index
    if selected_index is None:
        selected_index = 0
    elif selected_index > 0:
        selected_index -= 1


def increase_selected_button_index():
    global selected_index
    if selected_index is None:
        selected_index = 0
    elif selected_index < len(menu_buttons) - 1:
        selected_index += 1

def show_main_menu_screen(active_level) -> string:
    global selected_index

    # Stop music in active level
    active_level.level_music.fadeout(500)

    # Play music
    if not main_menu_music.get_num_channels() > 0:
        main_menu_music.play(-1)
        main_menu_music.set_volume(0.5 * settings.volume)

    # Draw menu
    backdrop((255, 255, 255))
    image(menu_backdrop,
          screen_width / 2,
          screen_height / 2,
          1.0 * scale)
    image(logo,
          screen_width / 2,
          screen_height / 2 - 100 * scale,
          0.85 * scale)
    text("BY NICKNAME", int(scale * 30), (0, 0, 0),
         screen_width / 2, screen_height / 2 + 20 * scale,
         "fonts/pixel.ttf")

    # Nintendo Switch Pro Controller navigation
    if is_nintendo_switch_pro_button_down(SWITCH_D_UP):
        decrease_selected_button_index()
    elif is_nintendo_switch_pro_button_down(SWITCH_D_DOWN):
        increase_selected_button_index()

    # Determine selected button
    if selected_index is not None:
        for i in range(len(menu_buttons)):
            if i == selected_index:
                menu_buttons[i].selected = True
            else:
                menu_buttons[i].selected = False

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
