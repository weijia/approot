import kivy
kivy.require('1.3.0')

#import math
#import time

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class FtpSyncApp(App):
    def build(self):
        parent = FloatLayout(size=(500,500))
        stopButtonHeight = 90
        self.stopButton = Button(text='Stop', pos_hint={'right':1}, size_hint=(None,None), height=stopButtonHeight)
        parent.add_widget(self.stopButton)
        #self.startButton = Button(text='Start', pos_hint={'right':1}, size_hint=(None,None), height=stopButtonHeight)
        #parent.add_widget(self.startButton)
        return parent


if __name__ in ('__main__', '__android__'):
    FtpSyncApp().run()