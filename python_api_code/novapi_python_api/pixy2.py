
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
import novapi,time
from decorator import *
from machine import UART
from port import *

MAX_RECEIVE_SIZE = 128


STATE_SYNC              = 0
STATE_PACKET_TYPE       = 1
STATE_DATA_LEN          = 2
STATE_DATA_CHECK_SUM_L  = 3
STATE_DATA_CHECK_SUM_H  = 4
STATE_DATA_BUFF         = 5

PIXY_DEFAULT_ARGVAL            =    0x80000000
PIXY_BUFFERSIZE                =    0x104
PIXY_CHECKSUM_SYNC             =    0xc1af
PIXY_NO_CHECKSUM_SYNC          =    0xc1ae
PIXY_SEND_HEADER_SIZE          =    4
PIXY_MAX_PROGNAME              =    33

PIXY_TYPE_REQUEST_CHANGE_PROG  =    0x02
PIXY_TYPE_REQUEST_RESOLUTION   =    0x0c
PIXY_TYPE_RESPONSE_RESOLUTION  =    0x0d
PIXY_TYPE_REQUEST_VERSION      =    0x0e
PIXY_TYPE_RESPONSE_VERSION     =    0x0f
PIXY_TYPE_RESPONSE_RESULT      =    0x01
PIXY_TYPE_RESPONSE_ERROR       =    0x03
PIXY_TYPE_REQUEST_BRIGHTNESS   =    0x10
PIXY_TYPE_REQUEST_SERVO        =    0x12
PIXY_TYPE_REQUEST_LED          =    0x14
PIXY_TYPE_REQUEST_LAMP         =    0x16
PIXY_TYPE_REQUEST_FPS          =    0x18
CCC_RESPONSE_BLOCKS            =    0x21
CCC_REQUEST_BLOCKS             =    0x20
LINE_REQUEST_GET_FEATURES            =    0x30
LINE_RESPONSE_GET_FEATURES           =    0x31
LINE_REQUEST_SET_MODE                =    0x36
LINE_REQUEST_SET_VECTOR              =    0x38
LINE_REQUEST_SET_NEXT_TURN_ANGLE     =    0x3a
LINE_REQUEST_SET_DEFAULT_TURN_ANGLE  =    0x3c
LINE_REQUEST_REVERSE_VECTOR          =    0x3e
VIDEO_REQUEST_GET_RGB                =    0x70

CCC_SIG1                       =    1 
CCC_SIG2                       =    2
CCC_SIG3                       =    4
CCC_SIG4                       =    8
CCC_SIG5                       =    16
CCC_SIG6                       =    32
CCC_SIG7                       =    64
CCC_COLOR_CODES                =    128
CCC_SIG_ALL                    =    0xff # all bits or'ed together
CCC_MAX_BLOCK                  =    0xFF

LINE_VECTOR                    =    0x01
LINE_INTERSECTION              =    0x02
LINE_BARCODE                   =    0x04
LINE_ALL_FEATURES              =    (LINE_VECTOR | LINE_INTERSECTION | LINE_BARCODE)

LINE_GET_MAIN_FEATURES         =    0x00
LINE_GET_ALL_FEATURES          =    0x01

SIG_DICT = {
    "SIG1": CCC_SIG1,
    "SIG2": CCC_SIG2,
    "SIG3": CCC_SIG3,
    "SIG4": CCC_SIG4,
    "SIG5": CCC_SIG5,
    "SIG6": CCC_SIG6,
    "SIG7": CCC_SIG7,
    "SIG_ALL": CCC_SIG_ALL,
}

LINE_DICT = {
    "vector": LINE_VECTOR,
    "intersection": LINE_INTERSECTION,
    "barcode": LINE_BARCODE,
    "all_features": LINE_ALL_FEATURES,
}

RGB_DICT = {
    "r": 0,
    "g": 1,
    "b": 2,
}

class uart_class(object):
    def __init__(self, port, baudrate = 115200):
        self.port = PORT[port]
        self.uart = UART(self.port, baudrate)
        if (self.port == PORT["PORT1"]):
            self.timeout = 3
        else:
            self.timeout = 20

    @decorator
    def open(baudrate = 115200):
        self.uart.init(baudrate)
        return self.uart

    @decorator
    def close():
        pass

    @decorator
    def write(self, data):
        self.uart.write(data)

    @decorator
    def read(self, len = MAX_RECEIVE_SIZE, timeout = 0):
        _bytes = self.uart.read(len, timeout)
        return _bytes

    @decorator
    def recv_packet(self, respond_type):
        m_state = STATE_SYNC
        m_length = 0
        m_sync = 0
        m_checksum = 0
        while(True):
            buff = self.read(len=1, timeout=self.timeout)
            #print(buff)
            if buff:
                if m_state == STATE_SYNC:
                    m_sync = (buff[0] << 8) | m_sync
                    m_sync = m_sync & 0xFFFF
                    if (m_sync==PIXY_CHECKSUM_SYNC):
                        m_state = STATE_PACKET_TYPE
                    elif (m_sync==PIXY_NO_CHECKSUM_SYNC):
                        m_state = STATE_PACKET_TYPE
                    else:
                        m_sync = buff[0]
                elif m_state == STATE_PACKET_TYPE:
                    if(buff[0] == respond_type):
                        m_state = STATE_DATA_LEN
                    else:
                        m_state = STATE_SYNC
                elif m_state == STATE_DATA_LEN:
                    m_length = buff[0]
                    if m_sync == PIXY_CHECKSUM_SYNC:
                        m_state = STATE_DATA_CHECK_SUM_L
                    else:
                        m_state = STATE_DATA_BUFF
                elif m_state == STATE_DATA_CHECK_SUM_L:
                    m_checksum = buff[0]
                    m_state = STATE_DATA_CHECK_SUM_H
                elif m_state == STATE_DATA_CHECK_SUM_H:
                    m_checksum = (buff[0]<<8) | m_checksum
                    m_state = STATE_DATA_BUFF
                else:
                    pass

                if m_state == STATE_DATA_BUFF:
                    data = self.read(len=m_length, timeout=10)
                    if(data):
                        if(len(data) != m_length):
                            #print("recv_packet tm_length error!")
                            return None
                        if m_sync == PIXY_CHECKSUM_SYNC:
                            csCalc = sum(data) & 0xFFFF
                            if (m_checksum != csCalc):
                                #print("recv_packet checksum error!")
                                return None
                            return data
                        else:
                            return data
                    else:
                        #print("recv_packet read data timeout!")
                        return None
                else:
                    pass
            else:
                #print("recv_packet timeout!")
                return None
    
    @decorator
    def send_packet(self, m_type, m_len, data=[]):
        m_buf = bytearray()
        m_buf.append(PIXY_NO_CHECKSUM_SYNC&0xff)
        m_buf.append(PIXY_NO_CHECKSUM_SYNC>>8)
        m_buf.append(m_type)
        m_buf.append(m_len)
        for i in range(len(data)):
            m_buf.append(data[i])
        return self.write(m_buf)

class ccc_class(object):
    def __init__(self, uart):
        self.uart = uart
        self.blocks = {CCC_SIG1:{}, CCC_SIG2:{}, CCC_SIG3:{}, CCC_SIG4:{}, CCC_SIG5:{}, CCC_SIG6:{}, CCC_SIG7:{}}
    
    @decorator
    def get_blocks(self, sigmap=CCC_SIG_ALL, maxBlocks=0xff):
        self.uart.send_packet(m_type=CCC_REQUEST_BLOCKS, m_len = 2, data=[SIG_DICT[sigmap], maxBlocks])
        data = self.uart.recv_packet(CCC_RESPONSE_BLOCKS)
        if(data != None):
            while((len(data) / 14) > 0):
                ccc_dict = dict()
                ccc_dict["signature"] = (data[1]<<8) | data[0]
                ccc_dict["x"] = (data[3]<<8) | data[2]
                ccc_dict["y"] = (data[5]<<8) | data[4]
                ccc_dict["width"] = (data[7]<<8) | data[6]
                ccc_dict["height"] = (data[9]<<8) | data[8]
                ccc_dict["angel"] = (data[11]<<8) | data[10]
                ccc_dict["index"] = data[12]
                ccc_dict["age"] = data[13]
                if ccc_dict["signature"] in self.blocks:
                    self.blocks[ccc_dict["signature"]] = ccc_dict
                data = data[14:]
            return self.blocks
        return None

    @decorator
    def get_value(self, sigmap, ccc = "x", wait=True):
        while(True):
            res = self.get_blocks(sigmap, CCC_MAX_BLOCK)
            if (res or wait==False):
                block = self.blocks[SIG_DICT[sigmap]]
                if ccc in block:
                    return block[ccc]
                return 0
            else:
                time.sleep(0.005)

class line_class(object):
    def __init__(self, uart):
        self.uart = uart
        self.vector = None
        self.intersection = None
        self.barcode = None

    @decorator
    def get_main_features(self, features="all_features"):
        self.uart.send_packet(LINE_REQUEST_GET_FEATURES, 2, [LINE_GET_MAIN_FEATURES, LINE_DICT[features]])
        data = self.uart.recv_packet(LINE_RESPONSE_GET_FEATURES)
        if(data != None):
            ftype = data[0]
            fsize = data[1]
            if ftype == LINE_VECTOR:
                vector_dict = dict()
                vector_dict["x0"] = data[2]
                vector_dict["y0"] = data[3]
                vector_dict["x1"] = data[4]
                vector_dict["y1"] = data[5]
                vector_dict["index"] = data[6]
                vector_dict["flags"] = data[7]
                self.vector = vector_dict
            elif ftype == LINE_INTERSECTION:
                intersection_dict = dict()
                intersection_dict["x"] = data[2]
                intersection_dict["y"] = data[3]
                intersection_dict["n"] = data[4]
                intersection_dict["reserved"] = data[5]
                self.intersection = intersection_dict
            elif ftype == LINE_BARCODE:
                barcode_dict = dict()
                barcode_dict["x"] = data[2]
                barcode_dict["y"] = data[3]
                barcode_dict["flags"] = data[4]
                barcode_dict["code"] = data[5]
                self.barcode = barcode_dict
            else:
                return None
            return [self.vector, self.intersection, self.barcode]
        return None

    @decorator
    def get_vector_value(self, value, wait=True):
        while(True):
            res = self.get_main_features("vector")
            if (res or wait==False):
                if self.vector:
                    return self.vector[value]
                else:
                    return 0
            else:
                time.sleep(0.005)
    
    @decorator
    def get_intersection_value(self, value, wait=True):
        while(True):
            res = self.get_main_features("intersection")
            if (res or wait==False):
                if self.intersection:
                    return self.intersection[value]
                else:
                    return 0
            else:
                time.sleep(0.005)
    
    @decorator
    def get_barcode_value(self, value, wait=True):
        while(True):
            res = self.get_main_features("barcode")
            if (res or wait==False):
                if self.barcode:
                    return self.barcode[value]
                else:
                    return 0
            else:
                time.sleep(0.005)

class rgb_class(object):
    def __init__(self, uart):
        self.uart = uart
        self.rgb = [0,0,0]
    
    @decorator
    def get_rgb(self, x, y):
        x_l = x & 0xff
        x_h = (x>>8) & 0xff
        y_l = y & 0xff
        y_h = (y>>8) & 0xff
        self.uart.send_packet(m_type=VIDEO_REQUEST_GET_RGB, m_len = 5, data=[x_l,x_h,y_l,y_h,1])
        data = self.uart.recv_packet(PIXY_TYPE_RESPONSE_RESULT)
        if(data != None):
            self.rgb = [data[0], data[1], data[2]]
            return self.rgb
        return None
    
    @decorator
    def get_value(self, x, y, rgb, wait=True):
        while(True):
            res = self.get_rgb(x, y)
            if (res or wait==False):
                return self.rgb[RGB_DICT[rgb]]
            else:
                time.sleep(0.005)

class pixy2_class(object):
    def __init__(self, port, baudrate = 115200):
        self.uart = uart_class(port, baudrate)
        self.ccc = ccc_class(self.uart)
        self.line = line_class(self.uart)
        self.rgb = rgb_class(self.uart)
    
    @decorator
    def get_version(self):
        self.uart.send_packet(m_type=PIXY_TYPE_REQUEST_VERSION, m_len = 0, data=[])
        version = self.uart.recv_packet(PIXY_TYPE_RESPONSE_VERSION)
        if(version != None):
            hardware = (version[1]<<8) | version[0]
            firmwareMajor = version[2]
            firmwareMinor = version[3]
            firmwareBuild = (version[5]<<8) | version[4]
            firmwareType = str(version[6: ], "utf-8")
            return ("hardware ver: 0x%X firmware ver: %d.%d.%d %s" %(hardware, firmwareMajor, firmwareMinor, firmwareBuild, firmwareType))
        return None

    @decorator
    def get_resolution(self):
        self.uart.send_packet(m_type=PIXY_TYPE_REQUEST_RESOLUTION, m_len = 1, data=[1])
        resolution = self.uart.recv_packet(PIXY_TYPE_RESPONSE_RESOLUTION)
        if(resolution != None):
            frameWidth = (resolution[1]<<8) | resolution[0]
            frameHeight = (resolution[3]<<8) | resolution[2]
            return [frameWidth, frameHeight]
        return None