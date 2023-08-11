from GameObject.Monster.ganondorf import Ganondorf
from Level.boss_level import BossLevel
from Level.endscene import EndScene
from Level.level import Level
from Support.settings import screen_width, screen_height, scale
from UI.button import Button
from jorcademy import *

# Levels
active_level_index = 0
levels = [
    EndScene("END",
             1,
             "assets/music/outro_song.ogg",
             (147, 187, 236)),
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
          (0, 0, 0)),
    BossLevel("BOSS",
              1,
              "assets/music/boss.ogg",
              (0, 0, 0), Ganondorf),
    EndScene("END",
             1,
             "assets/music/outro_song.ogg",
             (147, 187, 236))
]

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
show_main_menu = True
transitioning_from_main_menu = False
game_paused = False

# Additional timers
pause_cooldown = 30
pause_timer = 0

# Game Over
game_over_delay = 300
game_over_timer = 0

# Music
main_menu_music = load_sound("assets/music/main_menu.ogg")

# Buttons
start_button = Button(
    (screen_width / 2, screen_height / 2 + 110 * scale),
    275, 50,
    "START NEW GAME", 30, (0, 255, 255),
    (1, 1, 1), (50, 50, 50),
    True, 5, (255, 0, 0))

pause_button = Button(
    (screen_width / 2, screen_height / 2 + 50 * scale),
    250, 50,
    "GO TO MAIN MENU", 25, (0, 0, 0),
    (255, 255, 255), (240, 240, 240),
    True, 5, (200, 200, 200))


def show_paused_screen() -> None:
    global show_main_menu, game_paused, active_level_index

    text("PAUSED",
         int(scale * 50),
         (255, 255, 255),
         screen_width / 2,
         screen_height / 2 - 30 * scale,
         "fonts/pixel.ttf")

    # Go back to main menu
    pause_button.update()
    pause_button.draw()

    # Check if user clicked on start new game
    if pause_button.clicked():
        levels[active_level_index].level_music.fadeout(500)
        show_main_menu = True
        game_paused = False


def show_starting_messages():
    global switch_starting_message_timer, \
        starting_message_shown, \
        starting_message_index, \
        show_controls, \
        skip_allowed

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


# Show main menu screen
def show_main_menu_screen() -> None:
    global show_main_menu, \
        active_level_index, \
        transitioning_from_main_menu

    # Stop music in active level
    levels[active_level_index].level_music.fadeout(500)

    # Play music
    if not main_menu_music.get_num_channels() > 0:
        main_menu_music.play(-1)
        main_menu_music.set_volume(0.5 * volume)

    # Draw menu
    backdrop((255, 255, 255))
    image("other/main_menu_backdrop_light.png",
          screen_width / 2,
          screen_height / 2,
          1.0 * scale)
    image("icons/odyssey-of-a-knight-into-retroverse.png",
          screen_width / 2,
          screen_height / 2 - 80 * scale,
          0.85 * scale)
    text("BY NICKNAME", int(scale * 30), (0, 0, 0),
         screen_width / 2, screen_height / 2 + 40 * scale,
         "fonts/pixel.ttf")

    # Update start button
    start_button.update()
    start_button.draw()

    # Check if user clicked on start new game
    if start_button.clicked():
        show_main_menu = False
        transitioning_from_main_menu = True
        active_level_index = 0
        levels[active_level_index].link.hard_reset()
        levels[active_level_index].reset()


# Show game over screen
def show_game_over_screen() -> None:
    global last_recorded_score, \
        active_level_index, \
        show_main_menu, \
        game_over_timer

    # Stop music in active level
    levels[active_level_index].level_music.fadeout(500)

    # Set backdrop to black
    backdrop((0, 0, 0))

    # Display properties on screen
    text("GAME OVER", int(scale * 50), (255, 255, 255),
         screen_width / 2, screen_height / 2 - 30 * scale, "fonts/pixel.ttf")
    text(f"SCORE: {last_recorded_score}", int(20 * scale), (255, 255, 255), screen_width / 2,
         screen_height / 2 + 20 * scale, "fonts/pixel.ttf")

    game_over_timer += 1

    if game_over_timer >= game_over_delay:
        show_main_menu = True
        game_over_timer = 0


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


def transition_screen() -> None:
    global transition_started, \
        transition_timer, \
        transition_time

    # Stop music from current level
    try:
        levels[active_level_index].level_music.fadeout(500)
    except:
        pass

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


def setup() -> None:
    # Screen properties
    title("The Odyssey of a Knight | Into the Retro-Verse")
    screen(screen_width, screen_height)
    # NOTE: setting up level happened in main.py


def update() -> None:
    global transition_started, \
        transition_timer, \
        active_level_index, \
        game_paused, \
        pause_timer, \
        transitioning_from_main_menu, \
        show_main_menu, \
        last_recorded_score, \
        starting_message_shown

    last_recorded_score = levels[active_level_index].link.coins

    if show_main_menu:
        show_main_menu_screen()
        return
    else:
        main_menu_music.fadeout(500)

    # Check if game is over
    if levels[active_level_index].link.lives == 0:
        show_game_over_screen()
        return

    # Check if level is over
    if levels[active_level_index].transition_requested() or transitioning_from_main_menu:

        # Show starting message when transitioning from main menu
        if transitioning_from_main_menu and not starting_message_shown:
            show_starting_messages()
            return

        # Show controls screen
        if show_controls:
            show_controls_screen()
            return

        # Check if transitioning to main menu from EndScene
        if type(levels[active_level_index]) == EndScene and \
                levels[active_level_index].transition_requested():
            show_main_menu = True
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
            transitioning_from_main_menu = False
        return

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
