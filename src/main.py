# -*- coding: utf-8 -*-

import kivy
kivy.require('1.7.0')

'''
Check braucraft.kv for the ui design
'''

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import WipeTransition
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

from kivy.logger import Logger as log

from ds18b20 import DS18B20

class TimerWidget(Screen):

    def set_temperature(self, instance, temperature):
        self.label_temperature.text = "%05.1f °C" % temperature

    def on_time_changed(self, instance, time_value):
        print instance
        print time_value

class MainWidget(Screen):

    def set_temperature(self, instance, temperature):
        self.label_temperature.text = "%05.1f °C" % temperature


class BraucraftApp(App, EventDispatcher):

    temp_sensor = DS18B20()
    temperature = NumericProperty(0.0)

    def build(self):
        log.info("Creating BrauCraft")
        screen_manager = ScreenManager()
        #screen_manager.transition = WipeTransition()

        log.info("Starting temperature reader thread")
        self.temp_sensor.start()
        Clock.schedule_interval(self.read_temperature, 0)

        log.info("Creating MainWidget")        
        main_widget = MainWidget(name="main")
        self.bind(temperature=main_widget.set_temperature)
        screen_manager.add_widget(main_widget)

        log.info("Creating TimerWidget")
        timer_widget = TimerWidget(name="timer")
        self.bind(temperature=timer_widget.set_temperature)
        timer_widget.roulette_time.bind(rolling_value=timer_widget.on_time_changed)
        screen_manager.add_widget(timer_widget)

        return screen_manager

    def read_temperature(self, *args):
        if not self.temp_sensor.temp_queue.empty():
            self.temperature = self.temp_sensor.temp_queue.get()
        
    def on_stop(self):
        log.info("Stopping BrauCraft")
        log.info("Try to stop the temperature reading thread")
        self.temp.running = False
        self.temp.join()

if __name__ == '__main__':
    BraucraftApp().run()
