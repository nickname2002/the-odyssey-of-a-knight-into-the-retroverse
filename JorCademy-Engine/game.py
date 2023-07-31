from jorcademy import *
from Support.settings import screen_width, screen_height
from Level.level import Level

# Levels
level_1_1 = Level("1_1")
level_1_2_0 = Level("1_2_0")
active_level_index = 0

# Store levels in order
levels = [level_1_1, level_1_2_0]

# Transition properties
transition_started = False
transition_timer = 0
transition_time = 60 * 3


# Show game over screen
def show_game_over_screen() -> None:
    # Set backdrop to black
    backdrop((0, 0, 0))

    # Display properties on screen
    text("GAME OVER", 50, (255, 255, 255), screen_width / 2, screen_height / 2 - 30, "fonts/pixel.ttf")
    text(f"SCORE: {levels[active_level_index].link.score}", 20, (255, 255, 255), screen_width / 2,
         screen_height / 2 + 20, "fonts/pixel.ttf")


# Get name of the current level (might be different from active level)
def get_current_level_name() -> int:
    if levels[active_level_index].link.killed:
        return levels[active_level_index].level_name
    else:
        return levels[get_next_level_index()].level_name


# Show game over screen
def transition_screen() -> None:
    global transition_started, transition_timer, transition_time

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

    if active_level_index == len(levels):
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
    title("Link | The Rescue of Princess Zelda")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    global transition_started, \
        transition_timer, \
        active_level_index

    # Check if game is over
    if levels[active_level_index].link.lives == 0:
        show_game_over_screen()
        return

    # Check if level is over
    if levels[active_level_index].transition_requested():
        transition_screen()

        # TODO: Make sure to transition to right destination when level succeeded
        # Reset level if timer is over
        if transition_timer <= 0:
            transition_started = False

            # Switch to next level if needed
            if levels[active_level_index].end_game_triforce.reached:
                activate_next_level()

            # Reset level
            levels[active_level_index].reset()
        return

    # Draw sky backdrop
    backdrop(levels[active_level_index].backdrop_color)

    # Update levels
    levels[active_level_index].update()

    # Draw levels
    levels[active_level_index].draw()
