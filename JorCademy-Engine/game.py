from jorcademy import *
from Support.settings import screen_width, screen_height
from Level.level import Level

# Levels
# level = Level("1_1")
level = Level("1_2_0")

# TODO: Optimize performance. Performance seems to drop linearly when getting loot from lootboxes.

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
    text(f"SCORE: {level.link.score}", 20, (255, 255, 255), screen_width / 2, screen_height / 2 + 20, "fonts/pixel.ttf")


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
    text(f"x{level.link.lives}", 40, (255, 255, 255), screen_width / 2 + 30, screen_height / 2, "fonts/pixel.ttf")
    text(f"WORLD {level.level_name}", 30, (255, 255, 255), screen_width / 2, 30, "fonts/pixel.ttf")
    image("link/link_idle.png", screen_width / 2 - 40, screen_height / 2, 2, 40)


def setup() -> None:
    # Screen properties
    title("Link | The Rescue of Princess Zelda")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    global transition_started, transition_timer

    # Check if game is over
    if level.link.lives == 0:
        show_game_over_screen()
        return

    # Check if level is over
    if level.transition_requested():
        transition_screen()

        # TODO: Make sure to transition to right destination when level succeeded
        # Reset level if timer is over
        if transition_timer <= 0:
            transition_started = False
            level.reset()
        return

    # Draw sky backdrop
    backdrop(level.backdrop_color)

    # Update levels
    level.update()

    # Draw levels
    level.draw()
