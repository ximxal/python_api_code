
# Copyright (python), 2018-2019, MakeBlock
# file    buzzer.py
# @author  payton
# @version V1.0.0
# @date    2018/08/27
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/08/27     1.0.0            build the new.
#  
# 
from neurons_engine import *
from decorator import *
from port import *

class buzzer_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]

    @decorator
    def tone(self, freq, pwm):
        neurons_send("buzzer", "tone", self.port, self.index, (freq, pwm))