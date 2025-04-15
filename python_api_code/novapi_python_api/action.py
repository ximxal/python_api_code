# codes make you happy
import novapi,time, math
from decorator import *
from port import *
from mbuild.encoder_motor import encoder_motor_class

class action_class(object):
    def __init__(self, left_front_port, right_front_port, left_back_port="None", right_back_port="None", width=0.22, hight=0):
        self.left_front = encoder_motor_class(left_front_port, "INDEX1")
        self.right_front = encoder_motor_class(right_front_port, "INDEX1")
        if(left_back_port != "None"):
            self.left_back = encoder_motor_class(left_back_port, "INDEX1")
        else:
            self.left_back = None
        if(right_back_port != "None"):
            self.right_back = encoder_motor_class(right_back_port, "INDEX1")
        else:
            self.right_back = None
        self.width = width
        self.hight = hight

    def limit(self, speed, min_speed, max_speed):
        if speed > max_speed:
            speed = max_speed
        if speed < min_speed:
            speed = min_speed
        return speed
        
    def speed(self, L_speed, R_speed):
        self.left_front.set_speed(1 * L_speed)
        self.right_front.set_speed(-1 * R_speed)
        if(self.left_back):
            self.left_back.set_speed(1 * L_speed)
        if self.right_back:
            self.right_back.set_speed(-1 * R_speed)

    def power(self, L_power, R_power):
        self.left_front.set_power(1 * L_power)
        self.right_front.set_power(-1 * R_power)
        if(self.left_back):
            self.left_back.set_power(1 * L_power)
        if self.right_back:
            self.right_back.set_power(-1 * R_power)

    def stop(self):
        self.left_front.set_speed(0)
        self.right_front.set_speed(0)
        if self.left_back:
            self.left_back.set_speed(0)
        if self.right_back:
            self.right_back.set_speed(0)

    #@decorator
    def turn_left(self, speed, keep_time=9999):
        if keep_time==9999:
            self.speed(-speed, speed)
        else:
            novapi.reset_timer()
            while not (novapi.timer() > keep_time):
                self.speed(-speed, speed)
            self.stop()

    def turn_right(self, speed, keep_time=9999):
        self.turn_left(-speed, keep_time)

    def turn_left_by_degree(self, angle, r = 0):
        if r < 0:
            return
        novapi.reset_rotation("z")
        if angle > 0:
            while not (novapi.get_yaw() > angle):
                r0 = r #转弯半径
                r1 = r0 - self.width/2 - self.hight/2 #内径
                r2 = r0 + self.width/2 + self.hight/2 #外径
                L2_error = (2*3.14*r2) * (angle - novapi.get_yaw()) / 360

                v2 = 1000 * L2_error + 5
                v2 = self.limit(v2, 10, 120)
                v1 = v2 * (r1/r2)

                L_speed = v1
                R_speed = v2
                self.speed(L_speed, R_speed)
                time.sleep(0.001)
        else:
            while not (novapi.get_yaw() < angle):
                r0 = r #转弯半径
                r1 = r0 - self.width/2 - self.hight/2 #内径
                r2 = r0 + self.width/2 + self.hight/2 #外径
                L2_error = (2*3.14*r2) * (novapi.get_yaw() - angle) / 360
                
                v2 = 1000 * L2_error + 5
                v2 = self.limit(v2, 10, 120)
                v1 = v2 * (r1/r2)

                L_speed = v2
                R_speed = v1
                self.speed(L_speed, R_speed)
                time.sleep(0.001)
        self.stop()

    def turn_right_by_degree(self, angle, r = 0):
        self.turn_left_by_degree(-angle, r)

    def forward(self, speed, keep_time=9999, straight = False):
        if straight == False:
            if keep_time==9999:
                self.speed(speed, speed)
            else:
                novapi.reset_timer()
                while not (novapi.timer() > keep_time):
                    self.speed(speed, speed)
                    time.sleep(0.001)
                self.stop()
        else:
            novapi.reset_timer()
            novapi.reset_rotation("z")
            while not (novapi.timer() > keep_time):
                # Kp = 10, Ki  = 0, Kd = 0.1
                offset_speed = 10*novapi.get_yaw() + 0.1*novapi.get_gyroscope("z")
                left_speed = (speed + offset_speed)
                right_speed = (speed - offset_speed)
                self.speed(left_speed, right_speed)
                time.sleep(0.001)
            self.stop()

    def backward(self, speed, keep_time=9999, straight = False):
        self.forward(-speed, keep_time, straight)

