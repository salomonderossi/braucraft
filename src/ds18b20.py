# -*- coding: utf-8 -*-

from threading import Thread
import time
import Queue
import os
import glob

from kivy.logger import Logger as log


class DS18B20(Thread):

    _running_on_rpi = True
    running = True
    temp_queue = Queue.Queue()

    def __init__(self, *args, **kwargs):
        super(DS18B20, self).__init__(*args, **kwargs)

        # check if running on raspberry
        info = os.uname()
        if info[4][:3] != 'arm':
            log.info("Not running on raspberry")
            self._running_on_rpi = False

        if self._running_on_rpi:
            log.info("Setting up temperature sensors")
            #os.system('modprobe w1-gpio')
            #os.system('modprobe w1-therm')

            self._base_dir = '/sys/bus/w1/devices/'
            self._device_folder = glob.glob(self._base_dir + '28*')[0]
            self._device_file = self._device_folder + '/w1_slave'

    def _read_temp_raw(self):
        if not self._running_on_rpi:
            time.sleep(1)
            return ["YES", "t=47110"]

        f = open(self._device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def run(self):
        while self.running:
            self.temp_queue.put(self._read_temp())
