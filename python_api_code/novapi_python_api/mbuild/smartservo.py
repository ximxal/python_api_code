
# Copyright (python), 2018-2019, MakeBlock
# file    smartservo.py
# @author  payton
# @version V1.0.0
# @date    2018/06/26
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2018/06/28      1.0.0            build the new.
#  payton            2018/08/15      1.0.1            rename "back_zero" to "back_to_zero".
#  
# 
from neurons_engine import *
from decorator import *
from port import *

__VALUE = {
    "current": 1,\
    "voltage": 2,\
    "speed":   3,\
    "angle":   4,\
    "temperature": 5,\
}

__REPORT_TIME = 50

class smartservo_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.speed_report_time = -1001
        self.position_report_time = -1001
        self.temperature_report_time = -1001
        self.current_report_time = -1001
        self.voltage_report_time = -1001

    @decorator
    def set_zero(self):
        neurons_send("smartservo", "set_zero", self.port, self.index, ())

    @decorator
    def set_power(self, percent):
        pwm = percent * 255 // 100
        neurons_send("smartservo", "set_power", self.port, self.index, (pwm,))

    @decorator
    def move_to(self, position, speed):
        neurons_send("smartservo", "move_to", self.port, self.index, (position,speed))

    @decorator
    def move(self, position, speed):
        neurons_send("smartservo", "move", self.port, self.index, (position,speed))

    @decorator
    def back_to_zero(self, speed):
        neurons_send("smartservo", "back_to_zero", self.port, self.index, (0, speed))

    @decorator
    def get_speed(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.speed_report_time > 1000:
                self.speed_report_time = time.ticks_ms()
                neurons_send("smartservo", "get_speed", self.port, self.index, (CYCLE_REPORT,)) #12kg-50ms,,25kg-30ms
            value = neurons_read("smartservo", "get_speed", self.port, self.index, (CYCLE_REPORT,), False)
        else:
            value = neurons_read("smartservo", "get_speed", self.port, self.index, (QUERY_REPORT,))
        return value[0]

    @decorator
    def get_position(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.position_report_time > 1000:
                self.position_report_time = time.ticks_ms()
                neurons_send("smartservo", "get_position", self.port, self.index, (CYCLE_REPORT,))#12kg-50ms,,25kg-30ms
            value = neurons_read("smartservo", "get_position", self.port, self.index, (CYCLE_REPORT,), False)
        else:
            value = neurons_read("smartservo", "get_position", self.port, self.index, (QUERY_REPORT,))
        return value[0]

    @decorator
    def get_temperature(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.temperature_report_time > 1000:
                self.temperature_report_time = time.ticks_ms()
                neurons_send("smartservo", "get_temperature", self.port, self.index, (CYCLE_REPORT,))#12kg-50ms,,25kg-30ms
            value = neurons_read("smartservo", "get_temperature", self.port, self.index, (CYCLE_REPORT,), False)
        else:
            value = neurons_read("smartservo", "get_temperature", self.port, self.index, QUERY_REPORT)
        return value[0]

    @decorator
    def get_current(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.current_report_time > 1000:
                self.current_report_time = time.ticks_ms()
                neurons_send("smartservo", "get_current", self.port, self.index, (CYCLE_REPORT,))#12kg-50ms,,25kg-30ms
            value = neurons_read("smartservo", "get_current", self.port, self.index, (CYCLE_REPORT,), False)
        else:
            value = neurons_read("smartservo", "get_current", self.port, self.index, (QUERY_REPORT,))
        return value[0]

    @decorator
    def get_voltage(self):
        if neurons_get_run_mode() == ASYNC_MODE:
            if time.ticks_ms() - self.voltage_report_time > 1000:
                self.voltage_report_time = time.ticks_ms()
                neurons_send("smartservo", "get_voltage", self.port, self.index, (CYCLE_REPORT,))
            value = neurons_read("smartservo", "get_voltage", self.port, self.index, (CYCLE_REPORT,), False)
        else:
            value = neurons_read("smartservo", "get_voltage", self.port, self.index, (QUERY_REPORT,))
        return value[0]

    @decorator
    def get_value(self, type):
        if type == "current":
            return self.get_current()
        elif type == "voltage":
            return self.get_voltage()
        elif type == "speed":
            return self.get_speed()
        elif type == "angle":
            return self.get_position()
        elif type == "temperature":
            return self.get_temperature()
        return 0