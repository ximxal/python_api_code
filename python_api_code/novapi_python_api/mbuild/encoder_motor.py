
# Copyright (python), 2018-2019, MakeBlock
# file    encoder_motor.py
# @author  payton
# @version V1.0.0
# @date    2018/07/02
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/07/02      1.0.0            build the new.
#  payton            2018/08/15      1.0.1            solve report mode bug.
#  
# 
from neurons_engine import *
from decorator import *
from port import *

__REPORT_TIME = 20

class encoder_motor_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.speed_report_time = -1001
        self.position_report_time = -1001

    def set_stall_report_mode(self,mode,time = 50):
        neurons_send("encoder_motor", "set_state_report_mode", self.port, self.index, (mode, time))

    def set_speed_report_mode(self,mode,time = 50):
        neurons_send("encoder_motor", "set_speed_report_mode", self.port, self.index, (mode, time))

    def set_position_report_mode(self,mode,time = 50):
        neurons_send("encoder_motor", "set_position_report_mode", self.port, self.index, (mode, time))

    @decorator
    def move_to(self, position, speed):
        neurons_send("encoder_motor", "move_to", self.port, self.index, (position,speed))

    @decorator
    def move(self, position, speed):
        neurons_send("encoder_motor", "move", self.port, self.index, (position,speed))

    @decorator
    def set_speed(self, speed):
        neurons_send("encoder_motor", "set_speed", self.port, self.index, (speed,))

    @decorator
    def set_zero(self):
        neurons_send("encoder_motor", "set_zero", self.port, self.index, ())

    @decorator
    def lock(self):
        neurons_send("encoder_motor", "lock", self.port, self.index, (1,))

    @decorator
    def unlock(self):
        neurons_send("encoder_motor", "lock", self.port, self.index, (0,))

    @decorator
    def stop(self):
        neurons_send("encoder_motor", "stop", self.port, self.index, ())

    @decorator
    def set_power(self, percent):
        pwm = percent * 255 // 100
        neurons_send("encoder_motor", "set_power", self.port, self.index, (pwm,))

    @decorator
    def get_speed(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.speed_report_time > 1000:
                self.speed_report_time = time.ticks_ms()
                self.set_speed_report_mode(CYCLE_REPORT, __REPORT_TIME)
            value = neurons_read("encoder_motor", "get_speed", self.port, self.index, (), False)
        else:
            value = neurons_read("encoder_motor", "get_speed", self.port, self.index, ())
        return value[0]

    @decorator
    def get_position(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.position_report_time > 1000:
                self.position_report_time = time.ticks_ms()
                self.set_position_report_mode(CYCLE_REPORT, __REPORT_TIME)
            value = neurons_read("encoder_motor", "get_position", self.port, self.index, (), False)
        else:
            value = neurons_read("encoder_motor", "get_position", self.port, self.index, ())
        return value[0]

    @decorator
    def is_stall(self):
        value = neurons_read("encoder_motor", "is_stall", self.port, self.index, ())
        if(value[0] == 1):
            return True
        else:
            return False 

    @decorator
    def get_value(self, type):
        if type == "speed":
            return self.get_speed()
        elif type == "angle":
            return self.get_position()
        return 0