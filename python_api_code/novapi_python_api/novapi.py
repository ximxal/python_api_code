
import time
from makeblock import system_error_code
from makeblock import onboard_module
from neurons_engine import *
import random
from decorator import *

__timer_count_s = time.ticks_ms() / 1000
random.seed(int(onboard_module.get_gyroscope(0)*1000))
#index_x = int(random.randint(0,MAX_MESSAGE_NUM))

def query_version():
    value = onboard_module.query_version()
    if(value == None):
        value = []
    return value
    
def get_mbuild_block_ids():
    global online_module_request_dict
    device_info = dict()
    for name in (online_module_request_dict):
        device_id_list = online_module_request_dict[name]["device_id"]
        for i in range(len(device_id_list)):
            device_id = device_id_list[i]
            port = (device_id >> 8) & 0xFF
            block_id = (device_id) & 0xFF 
            if port in device_info:
                device_info[port].append(block_id)
            else:
                device_info[port] = []
                device_info[port].append(block_id)
    return device_info
    #print(online_module_request_dict)

def get_temperature(type):
    if type == "celsius":
        return onboard_module.get_temperature()
    else:
        return 0

def get_roll():
    return onboard_module.get_roll()

def get_pitch():
    return onboard_module.get_pitch()

def get_yaw():
    return onboard_module.get_yaw()

@decorator
def get_acceleration(axis):
    if axis == "x":
        return onboard_module.get_acceleration(0)
    elif axis == "y":
        return onboard_module.get_acceleration(1)
    elif axis == "z":
        return onboard_module.get_acceleration(2)
    else:
        print("Input parameters are out of range")
        return 0

@decorator
def get_gyroscope(axis):
    if axis == "x":
        return onboard_module.get_gyroscope(0)
    elif axis == "y":
        return onboard_module.get_gyroscope(1)
    elif axis == "z":
        return onboard_module.get_gyroscope(2)
    else:
        print("Input parameters are out of range")
        return 0

@decorator
def is_shaked():
    return onboard_module.is_shaked()

@decorator
def set_shake_threshold(threshold):
    threshold = int(threshold)
    if threshold < 0:
        threshold = 0
    elif threshold > 100:
        threshold = 100
    else:
        pass
    onboard_module.set_shake_threshold(threshold)

@decorator
def reset_rotation(axis):
    if axis == "x":
        return onboard_module.reset_rotation(0)
    elif axis == "y":
        return onboard_module.reset_rotation(1)
    elif axis == "z":
        return onboard_module.reset_rotation(2)
    elif axis == "all":
        return onboard_module.reset_rotation(3)
    else:
        print("Input parameters are out of range")
        return 0

def timer():
    global __timer_count_s
    return time.ticks_ms() / 1000 - __timer_count_s

def reset_timer():
    global __timer_count_s
    __timer_count_s = time.ticks_ms() / 1000

@decorator
def set_communication_mode(mode , time = 0.02):
    neurons_set_run_mode(mode, time)