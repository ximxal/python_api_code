
# Copyright (python), 2018-2019, MakeBlock
# file    button.py
# @author  payton
# @version V1.0.0
# @date    2018/07/10
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/07/10     1.0.0            build the new.
#  
# 
from neurons_engine import *
from decorator import *
from port import *

__REPORT_TIME = 30

class button_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.report_time = -1001

    def set_report_mode(self,mode,time = 50):
        neurons_send("button", "set_report_mode", self.port, self.index, (mode, time)) 

    @decorator
    def is_pressed(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            value = neurons_read("button", "is_pressed", self.port, self.index, (), False)
        else:
            value = neurons_read("button", "is_pressed", self.port, self.index, ())
        if(value[0] == 1):
            return True
        else:
            return False 