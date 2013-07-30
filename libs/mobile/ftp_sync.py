import kivy
kivy.require('1.3.0')

#import math
#import time

from kivy.app import App
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class FtpSyncApp(App):
    def build(self):
        parent = BoxLayout()
        stopButtonHeight = 90
        self.stopButton = Button(text='Stop', height=stopButtonHeight)
        parent.add_widget(self.stopButton)
        self.startButton = Button(text='Start', height=stopButtonHeight)
        parent.add_widget(self.startButton)
        return parent


if __name__ in ('__main__', '__android__'):
    FtpSyncApp().run()