# Copyright (python), 2018-2019, MakeBlock
# file    gamepad.py
# @author  payton
# @version V1.0.0
# @date    2018/07/02
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/07/20      1.0.0            build the new.
#  payton            2018/10/12      1.0.0            not use port.
#  
# 
from makeblock import handle_controller
from neurons_engine import *
from decorator import *

#'+' -> start
#'---' -> Select/mode
__BUTTON = {
    "Lx": 0,\
    "Ly": 1,\
    "Rx": 2,\
    "Ry": 3,\
    "R1": 4,\
    "R2": 5,\
    "L1": 6,\
    "L2": 7,\
    "N1": 8,\
    "N2": 9,\
    "N3": 10,\
    "N4": 11,\
    "Up": 12,\
    "Down": 13,\
    "Left": 14,\
    "Right": 15,\
    "+": 16,\
    "≡": 17,\
    "L_Thumb": 18,\
    "R_Thumb": 19,\
}

def __limit_dead_zone(data, dead_zone):
    result = 0
    if data < (-1*dead_zone):
        result = data + dead_zone
    elif data > (dead_zone):
        result = data - dead_zone
    else:
        result = 0
    return result

@decorator
def is_key_pressed(button):
    data = handle_controller.value(__BUTTON[button]) 
    if data == None:
        if (neurons_is_online_mode() == True):
            return None
        else:
            return False       

    return data

@decorator
def get_joystick(joystick_pos):
    data = handle_controller.value(__BUTTON[joystick_pos])
    if data == None:
        if (neurons_is_online_mode() == True):
            return None
        else:
            return 0

    data = (100 * (128 - data)) // 128
    __limit_dead_zone(data, 10)
    return data