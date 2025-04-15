from neurons_engine import *
from decorator import *
from port import *
import binascii


COLUMN_ID_MAX = 15
LINE_ID_MAX = 7 

def _sting_to_bytes(string):
    hex_data = binascii.unhexlify(string)
    return hex_data

def _get_image(image_string):
    temp_list = [0] * 16
    if len(image_string) < 32:  # 16 *2
        image_string = image_string + '0' * (32- len(image_string))
    if len(image_string) > 32:  # 16 *2
        image_string = image_string[0:32]
    return tuple(_sting_to_bytes(image_string))


class led_panel_class(object):
    def __init__(self, port, index):
        self.port = PORT[port]
        self.index = INDEX[index]
        self.report_time = -1001

    @decorator
    def show_image(self, image, pos_x = 0, pos_y = 0, time_s = None):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if pos_x > 15 or pos_x < -15 or pos_y > 7 or  pos_y < -7:
            self.clear()
            
        temp_list = [0] * 16
        show_list = [0] * 16

        if isinstance(image, list):
            for i in range(len(image) if len(image) < 16 else 16):
                temp_list[i] = image[i]
        elif isinstance(image, str):
            temp_list = _get_image(image)
        
        if pos_x >= 0:
            for i in range(pos_x):
                show_list[i] = 0x00
            for i in range(16 - pos_x):
                if pos_y > 0:
                    show_list[pos_x + i] = (temp_list[i] >> pos_y) & 0xFF
                else:
                    show_list[pos_x + i] = (temp_list[i] << pos_y) & 0xFF
        else:
            for i in range(-pos_x):
                show_list[-i - 1] = 0x00;
            for i in range(16 + pos_x):
                if pos_y > 0:
                    show_list[pos_x + i] = (temp_list[i] >> pos_y) & 0xFF
                else:
                    show_list[pos_x + i] = (temp_list[i] << pos_y) & 0xFF

        if time_s == None:
            neurons_send("led_panel", "show_image", self.port, self.index, show_list)
        elif time_s > 0:
            neurons_send("led_panel", "show_image", self.port, self.index, show_list)
            time.sleep(time_s)
            clear()

    @decorator
    def show(self, var, pos_x = None, pos_y = None, wait = False):
        var = str(var)
        if var == '':
            clear()
            return

        str_len = len(var)
        if pos_x != None or pos_y != None:
            if pos_x == None:
                pos_x = 0
            if pos_y == None:
                pos_y = 0
            pos_x = int(pos_x)
            pos_y = int(pos_y)
            neurons_send("led_panel", "show_str_with_pos", self.port, self.index, (pos_x, pos_y, var))
        else:
            neurons_send("led_panel", "show_str", self.port, self.index, (var, ))
            if wait:
                while True:
                    #value = neurons_read("led_panel", "get_status", self.port, self.index, (), True)
                    value = neurons_sync_read("led_panel", "get_status", self.port, self.index, ())
                    if value == None:
                        return
                    if value == [1]:
                        return
                    time.sleep(0.1)

    @decorator
    def set_pixel(self, pos_x, pos_y, status):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
            return  
        if status:
            neurons_send("led_panel", "show_pixel", self.port, self.index, (pos_x, pos_y, 1))
        else:
            neurons_send("led_panel", "show_pixel", self.port, self.index, (pos_x, pos_y, 0))

    @decorator
    def get_pixel(self, pos_x, pos_y):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
            return  False
        #ret = neurons_read("led_panel", "get_pixel", self.port, self.index, (pos_x, pos_y), True)
        ret = neurons_sync_read("led_panel", "get_pixel", self.port, self.index, (pos_x, pos_y))
        return bool(ret[2])

    @decorator
    def toggle_pixel(self, pos_x, pos_y):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
            return  
        neurons_send("led_panel", "toggle_pixel", self.port, self.index, (pos_x, pos_y))

    @decorator
    def clear(self):
        neurons_send("led_panel", "clear", self.port, self.index, ())