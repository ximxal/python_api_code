
# Copyright (python), 2018-2019, MakeBlock
# file    uart.py
# @author  payton
# @version V1.0.0
# @date    2019/04/20
#
# `<Author>`         `<Time>`        `<Version>`        `<Descr>`
#  payton            2019/04/20     1.0.0            build the new.
#  
# 
import novapi
from decorator import *
from machine import UART
from port import *

MAX_RECEIVE_SIZE = 128

class uart_class(object):
    def __init__(self, port, baudrate=115200, timeout=2, timeout_char=1):
        self.port = PORT[port]
        self.uart = UART(self.port, baudrate, timeout, timeout_char)

    @decorator
    def write(self, data):
        self.uart.write(data)

    @decorator
    def read(self):
        _bytes = self.uart.read(MAX_RECEIVE_SIZE)
        return _bytes

    #@decorator
    def is_received(self, _str):
        _bytes = self.uart.read(MAX_RECEIVE_SIZE)
        #print(_bytes)
        received_str = str(_bytes, "utf-8")
        if(received_str == _str):
            return True
        else:
            return False

    @decorator
    def get_string(self):
        _bytes = self.uart.read(MAX_RECEIVE_SIZE)
        #print(_bytes)
        return str(_bytes, "utf-8")

    @decorator
    def any(self):
        return self.uart.any()