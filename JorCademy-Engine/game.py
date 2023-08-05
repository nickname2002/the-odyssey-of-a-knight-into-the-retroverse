import pygame.mouse
from jorcademy import *
from Support.settings import screen_width, screen_height
from Level.level import Level

# Levels
active_level_index = 0
levels = [
    Level("1_4_0", 1),
    Level("1_1", 10),
    Level("1_2", 10),
    Level("1_3", 10)
]

# Transition properties
transition_started = False
transition_timer = 0
transition_time = 60 * 3

# Menu flags
show_main_menu = True
transitioning_from_main_menu = False
game_paused = False

# Additional timers
pause_cooldown = 30
pause_timer = 0


def show_paused_screen() -> None:
    global show_main_menu, game_paused, active_level_index

    text("PAUSED", 50, (0, 0, 0), screen_width / 2, screen_height / 2 - 30, "fonts/pixel.ttf")

    # Go back to main menu
    text("GO TO MAIN MENU", 30, (0, 255, 255), screen_width / 2, screen_height / 2 + 20, "fonts/pixel.ttf")

    # Check if user clicked on start new game
    if is_mouse_button_down("left"):
        if screen_height / 2 < pygame.mouse.get_pos()[1] < screen_height / 2 + 40 and \
                screen_width / 2 - 140 < pygame.mouse.get_pos()[0] < screen_width / 2 + 140:
            show_main_menu = True
            game_paused = False


# Show main menu screen
def show_main_menu_screen() -> None:
    global show_main_menu, active_level_index, transitioning_from_main_menu

    # Draw menu
    backdrop((255, 255, 255))
    image("other/main_menu_backdrop_light.png", screen_width / 2, screen_height / 2, 1)
    image("icons/odyssey-of-link-into-retroverse.png", screen_width / 2, screen_height / 2 - 90, 0.8)
    text("START NEW GAME", 30, (0, 255, 255), screen_width / 2, screen_height / 2 + 90, "fonts/pixel.ttf")

    # Check if user clicked on start new game
    if is_mouse_button_down("left"):
        if screen_height / 2 + 80 < pygame.mouse.get_pos()[1] < screen_height / 2 + 120 and \
                screen_width / 2 - 140 < pygame.mouse.get_pos()[0] < screen_width / 2 + 140:
            show_main_menu = False
            transitioning_from_main_menu = True
            active_level_index = 0
            levels[active_level_index].link.hard_reset()
            levels[active_level_index].reset()


# Show game over screen
def show_game_over_screen() -> None:
    # Set backdrop to black
    backdrop((0, 0, 0))

    # Display properties on screen
    text("GAME OVER", 50, (255, 255, 255), screen_width / 2, screen_height / 2 - 30, "fonts/pixel.ttf")
    text(f"SCORE: {levels[active_level_index].link.score}", 20, (255, 255, 255), screen_width / 2,
         screen_height / 2 + 20, "fonts/pixel.ttf")


# Pause/play game
def toggle_pause_game() -> None:
    global game_paused, pause_timer

    # Toggle pause
    if not game_paused:
        if pause_timer <= 0:
            game_paused = True
            pause_timer = pause_cooldown
    else:
        if pause_timer <= 0:
            game_paused = False
            pause_timer = pause_cooldown


# Update game timers
def update_timers() -> None:
    global pause_timer

    # Update pause timer
    if pause_timer > 0:
        pause_timer -= 1


# Get name of the current level (might be different from active level)
def get_current_level_name() -> int:
    if levels[active_level_index].link.killed or transitioning_from_main_menu:
        return levels[active_level_index].level_name
    else:
        return levels[get_next_level_index()].level_name


# Show game over screen
def transition_screen() -> None:
    global transition_started, \
        transition_timer, \
        transition_time

    # Set backdrop to black
    backdrop((0, 0, 0))

    # Start transition
    if not transition_started:
        transition_timer = transition_time
        transition_started = True

    # Make sure transition stops eventually
    if transition_started:
        transition_timer -= 1

    # Display properties on screen
    text(f"x{levels[active_level_index].link.lives}", 40, (255, 255, 255), screen_width / 2 + 30, screen_height / 2,
         "fonts/pixel.ttf")
    text(f"WORLD {get_current_level_name()}", 30, (255, 255, 255), screen_width / 2, 30, "fonts/pixel.ttf")
    image("link/link_idle.png", screen_width / 2 - 40, screen_height / 2, 2, 40)


# Get next level index
def get_next_level_index() -> int:
    global active_level_index

    if active_level_index == (len(levels) - 1):
        return 0  # NOTE: find right behavior when outplayed all levels
    else:
        return active_level_index + 1


# Activate next level
def activate_next_level() -> None:
    global active_level_index
    stored_link = levels[active_level_index].link
    active_level_index = get_next_level_index()
    levels[active_level_index].init_link(stored_link)


def setup() -> None:
    # Screen properties
    title("The Odyssey of Link | Into The Retro-Verse")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    global transition_started, \
        transition_timer, \
        active_level_index, \
        game_paused, \
        pause_timer, \
        transitioning_from_main_menu

    if show_main_menu:
        show_main_menu_screen()
        return

    # Check if game is over
    if levels[active_level_index].link.lives == 0:
        show_game_over_screen()
        return

    # Check if level is over
    if levels[active_level_index].transition_requested() or transitioning_from_main_menu:  
        transition_screen()

        # Reset level if timer is over
        if transition_timer <= 0:
            transition_started = False

            # Switch to next level if needed
            if levels[active_level_index].end_game_triforce.reached:
                activate_next_level()

            # Reset level
            levels[active_level_index].reset()
            transitioning_from_main_menu = False
        return

    # Draw sky backdrop
    backdrop(levels[active_level_index].backdrop_color)

    # Draw levels
    levels[active_level_index].draw()

    # Update timers
    update_timers()

    # Check if game paused needs to be toggled
    if is_key_down("esc"):
        toggle_pause_game()

    # Show paused screen if game is paused
    if game_paused:
        show_paused_screen()
        return

    # Update levels
    levels[active_level_index].update()
