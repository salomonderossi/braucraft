# -*- coding: utf-8 -*-

import kivy
kivy.require('1.7.0')

'''
Check braucraft.kv for the ui design
'''

from kivy.app import App
#from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import WipeTransition
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.clock import Clock

from kivy.logger import Logger as log

from ds18b20 import DS18B20

class TimerWidget(Screen):

    timer_started = False
    timer_paused = False
    timer_value = NumericProperty(0.0)

    def on_timer_value(self, instance, value):
        print "Timer value from root widget: %i" % value
        self.label_timer_value.text = "%03i min" % (value / 60)
    
    def set_temperature(self, instance, temperature):
        self.label_temperature.text = "%05.1f °C" % temperature

    def time_changed(self, instance, value):  # called from roulette
        self.label_timer_value.text = "%03i min" % time_value

    def start_stop_timer(self, instance):
        print "start stop timer"
        print "Selected time: %s" % self.roulette_time.selected_value

        if self.timer_started:
            Clock.unschedule(self.update_timer)
            self.timer_started = False
        else:
            self.timer_value = self.roulette_time.selected_value * 60.0
            Clock.schedule_interval(self.update_timer, 1)  # call the update method every second
            self.timer_started = True

    def pause_resume_timer(self, instance):
        print "pause resume timer"
        print "Selected time: %s" % self.roulette_time.selected_value

    def update_timer(self, dt):  # dt = lapsed time as float
        self.timer_value -= dt

        # check if timer expired ( <0 )
        if self.timer_value < 0:
            self.timer_value = 0.0
            Clock.unschedule(self.update_timer)
            print "Timer expired"


class MainWidget(Screen):

    def set_temperature(self, instance, temperature):
        self.label_temperature.text = "%05.1f °C" % temperature

    def set_timer_label(self, instance, value):
        self.label_timer_value.text = "%03i min" % (value / 60)


#class BraucraftApp(App, EventDispatcher):
class BraucraftApp(App):

    temp_sensor = DS18B20()
    temperature = NumericProperty(0.0)

    def build(self):
        log.info("Creating BrauCraft")
        screen_manager = ScreenManager()
        #screen_manager.transition = WipeTransition()

        log.info("Starting temperature reader thread")
        self.temp_sensor.start()
        Clock.schedule_interval(self.read_temperature, 0)

        log.info("Creating TimerWidget")
        timer_widget = TimerWidget(name="timer")
        self.bind(temperature=timer_widget.set_temperature)
        timer_widget.roulette_time.bind(rolling_value=timer_widget.time_changed)

        log.info("Creating MainWidget")        
        main_widget = MainWidget(name="main")
        self.bind(temperature=main_widget.set_temperature)
        timer_widget.bind(timer_value=main_widget.set_timer_label)
        #self.bind(timer_widget.timer_value=main_widget.set_timer_time)
        #timer_widget.bind(timer_value, main_widget.set_timer_time)

        screen_manager.add_widget(main_widget)
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
