# TODO: add game info here

# Levels
from GameObject.Monster.ganondorf import Ganondorf
from Level.boss_level import BossLevel
from Level.endscene import EndScene
from Level.level import Level

# Screens
from View import main_menu_screen
from View.main_menu_screen import show_main_menu_screen
from View.settings_screen import show_settings_screen
from View.game_over_screen import show_game_over_screen
from View.pause_screen import show_paused_screen
from jorcademy import *

# Support
from Support.settings import screen_width, screen_height, scale

# Levels
active_level_index = 0
levels = [
    Level("1_1",
          10,
          "assets/music/1-1.ogg",
          (147, 187, 236)),
    Level("1_2",
          10,
          "assets/music/1-2.ogg",
          (147, 187, 236)),
    Level("1_3",
          10,
          "assets/music/1-3.ogg",
          (147, 187, 236)),
    Level("1_4",
          10,
          "assets/music/1-4.ogg",
          (147, 187, 236)),
    Level("1_5",
          10,
          "assets/music/1-5.ogg",
          (0, 0, 0), False),
    BossLevel("BOSS",
              1,
              "assets/music/boss.ogg",
              (0, 0, 0), Ganondorf),
    EndScene("END",
             1,
             "assets/music/outro_song.ogg",
             (147, 187, 236))
]

current_screen = "MAIN_MENU"

# Starting message properties
starting_message_shown = False
switch_starting_message_timer = 0
starting_message_delay = 300
starting_message_index = 0
skip_allowed = True

# Controls screen
show_controls = False

# Transition properties
transition_started = False
transition_timer = 0
transition_time = 60 * 3
last_recorded_score = 0

# Menu flags
transitioning_from_main_menu = False

# Additional timers
pause_cooldown = 30
pause_timer = 0

# Game Over
game_over_delay = 300
game_over_timer = 0


def show_starting_messages():
    global switch_starting_message_timer, \
        starting_message_shown, \
        starting_message_index, \
        show_controls, \
        skip_allowed, \
        current_screen

    # Starting messages to show
    starting_messages = [
        "The Princess has been captured by an awful monster".upper(),
        "As an honorable knight, it is your duty to save her".upper(),
        "The retro-verse is full of dangerous creatures".upper(),
        "Be careful. And good luck".upper()
    ]

    # Draw backdrop
    backdrop((255, 255, 255))

    # Toggle skip allowed
    if not is_key_down("space"):
        skip_allowed = True

    # Show correct message
    text(starting_messages[starting_message_index],
         int(scale * 20),
         (0, 0, 0),
         screen_width / 2,
         screen_height / 2,
         "fonts/pixel.ttf")

    # Show skip option
    text("PRESS SPACE TO SKIP",
         int(scale * 15),
         (150, 150, 150),
         screen_width / 2,
         screen_height - 30 * scale,
         "fonts/pixel.ttf")

    # Update timer
    switch_starting_message_timer += 1

    # Switch to next message
    if (switch_starting_message_timer >= starting_message_delay or
            is_key_down("space") and skip_allowed):
        skip_allowed = False
        if starting_message_index >= len(starting_messages) - 1:
            starting_message_shown = True
            return

        # Reset timer & change index
        starting_message_index += 1
        switch_starting_message_timer = 0
        show_controls = True


# Show controls screen
def show_controls_screen() -> None:
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
        global show_controls
        show_controls = False


# Update game timers
def update_timers() -> None:
    global pause_timer

    # Update pause timer
    if pause_timer > 0:
        pause_timer -= 1


# Get name of the current level (might be different from active level)
def get_current_level_name() -> int:
    print(current_screen)
    if levels[active_level_index].link.killed or current_screen == "TRANSITION_FROM_MAIN_MENU":
        return levels[active_level_index].level_name
    else:
        return levels[get_next_level_index()].level_name


def transition_screen() -> None:
    global transition_started, \
        transition_timer, \
        transition_time

    # Stop music from current level
    try:
        levels[active_level_index].level_music.fadeout(500)
    except:
        print("No music to fade out")

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
    text(f"x{levels[active_level_index].link.lives}",
         int(40 * scale),
         (255, 255, 255),
         screen_width / 2 + 30 * scale,
         screen_height / 2,
         "fonts/pixel.ttf")
    text(f"WORLD {get_current_level_name()}",
         int(30 * scale),
         (255, 255, 255),
         screen_width / 2,
         30 * scale,
         "fonts/pixel.ttf")
    image("link/link_idle.png", screen_width / 2 - 40 * scale, screen_height / 2, 2 * scale)


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
    global last_recorded_score
    stored_link = levels[active_level_index].link
    active_level_index = get_next_level_index()
    levels[active_level_index].init_link(stored_link)
    levels[active_level_index].clouds_enabled = settings.clouds


def setup() -> None:
    # Screen properties
    title("The Odyssey of a Knight | Into the Retro-Verse")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    global transition_started, \
        transition_timer, \
        active_level_index, \
        pause_timer, \
        transitioning_from_main_menu, \
        last_recorded_score, \
        starting_message_shown, \
        current_screen

    last_recorded_score = levels[active_level_index].link.coins

    # Show settings screen
    if current_screen == "SETTINGS":
        current_screen = show_settings_screen(main_menu_screen.main_menu_music)
        return

    # Show main menu screen
    if current_screen == "MAIN_MENU":
        levels[active_level_index].level_music.fadeout(500)
        current_screen = show_main_menu_screen(levels[active_level_index])
        return
    else:
        main_menu_screen.main_menu_music.fadeout(500)

    # Check if game is over
    if levels[active_level_index].link.lives == 0:
        current_screen = show_game_over_screen(levels[active_level_index], last_recorded_score)
        return

    # Check if level is over
    if (levels[active_level_index].transition_requested() or
            current_screen == "TRANSITION" or
            current_screen == "TRANSITION_FROM_MAIN_MENU"):

        # Show starting message when transitioning from main menu
        if current_screen == "TRANSITION_FROM_MAIN_MENU" and not starting_message_shown:
            show_starting_messages()
            return

        # Show controls screen
        if show_controls:
            show_controls_screen()
            return

        # Check if transitioning to main menu from EndScene
        if type(levels[active_level_index]) == EndScene and \
                levels[active_level_index].transition_requested():
            current_screen = "MAIN_MENU"
            active_level_index = 0
            return

        # Show transition screen
        transition_screen()

        # Reset level if timer is over
        if transition_timer <= 0:
            transition_started = False

            # Switch to next level if needed
            if type(levels[active_level_index]) == Level or \
                    type(levels[active_level_index]) == BossLevel:
                starting_message_shown = False
                if levels[active_level_index].end_game_triforce.reached:
                    activate_next_level()

            # Reset level
            levels[active_level_index].reset()
            current_screen = "GAME"
        return

    # Draw levels
    levels[active_level_index].draw()

    # Check if game paused needs to be toggled
    if current_screen == "GAME":
        if is_key_down("esc") and pause_timer == 0:
            current_screen = "PAUSED"
            pause_timer = 10
    else:
        current_screen = show_paused_screen(levels[active_level_index])
        return

    # Update timers
    update_timers()

    # Update levels
    levels[active_level_index].update()
