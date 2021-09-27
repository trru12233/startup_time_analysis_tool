#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import serial
import logging
import time
import threading
import os
from binascii import a2b_hex


class power_control():
    def __init__(self, mode, com_port=None):
        self.lock = threading.Lock()
        self.com = None
        self.mode = mode
        if self.mode == 3:
            self.serial = serial.Serial(com_port, baudrate=115200)

    def _comrelay_onoff(self, port, onoff):
        data = b'\xAA\x01'
        data += a2b_hex('%02d' % port)
        if onoff:
            onoff = 0
        else:
            onoff = 1
            data += a2b_hex('%02d' % onoff)
            data += b'\xA8'
            self.serial.write(data)

    def on_all(self):
        self.lock.acquire()
        if self.mode == 1:
            os.system('sudo usbrelay 0_1=0 0_2=0 0_3=0 0_4=0 0_5=0 0_6=0')
        elif self.mode == 2:
            os.system('sudo usbrelay 0_1=1 0_2=1 0_2=1 0_4=1 0_5=1 0_6=1')
        elif self.mode == 3:
	        # print('on all')
	        self.serial.write(b'\xAA\x02\xFF\xFF\xA8')
        self.lock.release()

		
    def off_all(self):
        self.lock.acquire()
        if self.mode == 1:
            os.system('sudo usbrelay 0_1=0 0_2=0 0_3=0 0_4=0 0_5=0 0_6=0')
        elif self.mode == 2:
            os.system('sudo usbrelay 0_1=1 0_2=1 0_2=1 0_4=1 0_5=1 0_6=1')
        elif self.mode == 3:
	        # print('off all')
	        self.serial.write(b'\xAA\x02\xFF\x00\xA8')
        self.lock.release()		
		
    def on(self, port, delay=0):
        if delay:
            time.sleep(delay)
        self.lock.acquire()
        for i in range(3):
            ret = 1
            if self.mode == 1:
                ret = os.system('sudo usbrelay 0_%d=0' % port)
            elif self.mode == 2:
                ret = os.system('sudo usbrelay 0_%d=1' % port)
            elif self.mode == 3:

                if self._comrelay_onoff(port, 1):
                    ret = 0
            if ret == 0:
                break
            time.sleep(0.2)
        else:
            self.lock.release()
            logging.error('usbrelay abnormal in on for port %d' % port)
            return False
        self.lock.release()
        return True

    def off(self, port, delay=0):
        if delay:
            time.sleep(delay)
        self.lock.acquire()
        for i in range(3):
            ret = 1
            if self.mode == 1:
                ret = os.system('sudo usbrelay 0_%d=1' % port)
            elif self.mode == 2:
                ret = os.system('sudo usbrelay 0_%d=0' % port)
            elif self.mode == 3:
                if self._comrelay_onoff(port, 0):
                    ret = 0
            if ret == 0:
                break
            time.sleep(0.2)
        else:
            self.lock.release()
            logging.error('usbrelay abnormal in off for port %d' % port)
            return False
        self.lock.release()
        return True


if __name__ == '__main__':
    '''
        usage:
            ./power_control mode com_dev port of_off
    '''
    logging.basicConfig(
                    level=logging.DEBUG, format='[%(levelname)s] %(asctime)s %(filename)s:%(lineid)d %(message)s')
    import sys

    mode = 3
    com_port = '/dev/ttyUSB0'
    port = 0
    onoff = 'on'

    power = power_control(mode, com_port)
    count = 0
    while (count < 10000000):
        power.on_all()
        time.sleep(5)
        power.off_all()
        time.sleep(2)
        count = count + 1
        print('count %d' % count)
