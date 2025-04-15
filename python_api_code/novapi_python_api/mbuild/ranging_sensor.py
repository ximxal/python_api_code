
# Copyright (python), 2018-2019, MakeBlock
# file    ranging_sensor.py
# @author  payton
# @version V1.0.0
# @date    2018/07/02
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/08/31      1.0.0            build the new.
#  
# 
from neurons_engine import *
from decorator import *
from port import *

__REPORT_TIME = 30

class ranging_sensor_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.report_mode_time = -1001

    def set_report_mode(self,mode,time = 0):
        neurons_send("ranging_sensor", "set_report_mode", self.port, self.index, (mode,time)) 

    @decorator
    def get_distance(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            value = neurons_read("ranging_sensor", "get_distance", self.port, self.index, (), False)
        else:
            value = neurons_read("ranging_sensor", "get_distance", self.port, self.index, ())
        return value[0]
