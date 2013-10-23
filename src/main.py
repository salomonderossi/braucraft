# -*- coding: utf-8 -*-

import kivy
kivy.require('1.7.0')

'''
Check braucraft.kv for the ui design
'''

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger as log

from ds18b20 import DS18B20


class BraucraftController(BoxLayout):

    temp = DS18B20()

    def __init__(self, *args, **kwargs):
        super(BraucraftController, self).__init__(*args, **kwargs)
        log.info("Starting Controller")

        self.temp.start()
        Clock.schedule_interval(self.read_temperature, 0)

    def read_temperature(self, *args):
        if not self.temp.temp_queue.empty():
            temperature = self.temp.temp_queue.get()
            log.info("Got value from temperature queue: %s", temperature)
            self.lbl_temperature.text = "%04.1f °C" % temperature

    def stop_temp_thread(self):
        log.info("Try to stop the temperature reading thread")
        self.temp.running = False
        self.temp.join()


class BraucraftApp(App):

    def build(self):
        log.info("Creating BrauCraft")
        self._controler = BraucraftController()
        return self._controler

    def on_stop(self):
        log.info("Stopping BrauCraft")
        self._controler.stop_temp_thread()

if __name__ == '__main__':
    BraucraftApp().run()
