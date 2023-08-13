from jorcademy import is_key_down


def move_right_key_pressed():
    return is_key_down("d") or is_key_down('right')


def move_left_key_pressed():
    return is_key_down("a") or is_key_down('left')
