import kivy
kivy.require('1.8.0')

'''
Check braucraft.kv for the ui design
'''

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

class BraucraftController(BoxLayout):
    pass

class BraucraftApp(App):
    
    def build(self):
        c = BraucraftController()
        return c

if __name__ == '__main__':
    BraucraftApp().run()
