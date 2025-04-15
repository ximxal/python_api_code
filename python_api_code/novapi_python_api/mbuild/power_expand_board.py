
# Copyright (python), 2018-2019, MakeBlock
# file    power_expand_board.py
# @author  payton
# @version V1.0.0
# @date    2018/07/02
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/07/02      1.0.0            build the new.
#  payton            2018/10/13      1.0.0            not use port.
#  
# 
from neurons_engine import *
from decorator import *
from port import *

__CH = {
  "ALL": 0,\
  "DC1": 1,\
  "DC2": 2,\
  "DC3": 3,\
  "DC4": 4,\
  "DC5": 5,\
  "DC6": 6,\
  "DC7": 7,\
  "DC8": 8,\
  "BL1": 9,\
  "BL2": 10,\
}

__PORT = PORT["PORT6"]
__INDEX = INDEX["INDEX1"]
NAME = "power_expand_board"

@decorator
def set_power(ch,percent):
    channel = __CH[ch]
    pwm = percent * 255 // 100
    neurons_send(NAME, "set_power", __PORT, __INDEX, (channel,pwm)) 

@decorator
def stop(ch):
    channel = __CH[ch]
    neurons_send(NAME, "stop", __PORT, __INDEX, (channel,))