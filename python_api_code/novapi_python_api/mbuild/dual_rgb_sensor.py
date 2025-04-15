
# Copyright (python), 2018-2019, MakeBlock
# file    dual_rgb_sensor.py
# @author  yisi.hu
# @version V1.0.2
# @date    2018/08/31
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  yisi.hu            2018/07/11      1.0.0            build the new.
#  yisi.hu            2018/07/13      1.0.1            add sensor channel parameter.
#  yisi.hu            2018/08/31      1.0.2            1.change the set report mode as self function.
#                                                      2.add get all data protocol and set line follow light color protocol.
# 
from neurons_engine import *
from decorator import *
from port import *

__REPORT_TIME = 10

__CH = {
    "RGB1":  0, \
    "RGB2":  1, \
    "RGB1|2": 2, \
}

__COLOR = {
    "white":  0, \
    "puple":  1, \
    "red":    2, \
    "orange": 3, \
    "yellow": 4, \
    "green":  5, \
    "cyan":   6, \
    "blue":   7, \
    "pink":   8, \
    "black":  9, \
}

__LED_COLOR = {
    "red":  0, \
    "green":  1, \
    "blue": 2, \
}

__STATE = {
    "00":  0, \
    "01":  1, \
    "10": 2, \
    "11": 3, \
}


class dual_rgb_sensor_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.report_time = -1001
        self.kp = 1

    def set_all_data_report_mode(self,mode,time = 20):
        neurons_send("dual_rgb_sensor", "set_all_data_report_mode", self.port, self.index, (mode,time)) 

    def get_all_data(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.report_time > 1000:
                self.report_time = time.ticks_ms()
                self.set_all_data_report_mode(CYCLE_REPORT, __REPORT_TIME)
            value = neurons_read("dual_rgb_sensor", "get_all_data", self.port, self.index, (), False)
        else:
            value = neurons_read("dual_rgb_sensor", "get_all_data", self.port, self.index, ())
        return value

    @decorator
    def study(self):
        neurons_send("dual_rgb_sensor", "study", self.port, self.index, ())

    @decorator
    def set_led_color(self,led_color):
        neurons_send("dual_rgb_sensor", "set_led_color", self.port, self.index, (__LED_COLOR[led_color],))

    @decorator
    def calibration(self):
        neurons_send("dual_rgb_sensor", "calibration", self.port, self.index, ())

    @decorator
    def get_intensity(self, channel):
        value = self.get_all_data()
        return value[__CH[channel]]

    @decorator
    def is_state(self, state):
        value = self.get_all_data()
        _state = (value[2] | (value[3]<<1))
        if(__STATE[state] == _state):
            return True
        else:
            return False

    @decorator
    def get_offset_track_value(self):
        value = self.get_all_data()
        return value[4] * 100 / 512 # -100 ~ 100

    @decorator
    def is_color(self,channel,color):
        value = self.get_all_data()
        check_color = value[__CH[channel] + 5]
        if(__COLOR[color] == check_color):
            return True
        else:
            return False

    @decorator
    def is_on_track(self,channel):
        value = self.get_all_data()
        state = value[__CH[channel] + 2]
        if(state == 0):
            return True
        else:
            return False

    @decorator
    def is_on_background(self,channel):
        value = self.get_all_data()
        state = value[__CH[channel] + 2]
        if(state == 1):
            return True
        else:
            return False

    @decorator
    def set_motor_diff_speed_kp(self, kp):
        self.kp = kp

    @decorator
    def get_motor_diff_speed(self):
        value = self.get_offset_track_value()
        return (value * self.kp)