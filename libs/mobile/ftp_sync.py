import json
import kivy
kivy.require('1.3.0')

#import math
#import time

from kivy.app import App
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class FtpSyncApp(App):
    def create_sync_list(self):
        try:
            f = open("sync_config.txt", "r")
            config = json.load(f)
            f.close()
        except:
            config = {"urls":[]}


        box_layout = BoxLayout(orientation='vertical')

        stopButtonHeight = 90
        for url in config.get("url", []):
            button = Button(text=url.url, height=stopButtonHeight)
            box_layout.add_widget(button)

        new_button = Button(text="New", height=stopButtonHeight)
        box_layout.add_widget(new_button)

        new_button.bind(on_press=self.create_sync)
        return box_layout

    def build(self):
        self.parent = ScreenManager()
        screen = Screen()
        self.parent.add_widget(screen)
        box_layout = self.create_sync_list()
        screen.add_widget(box_layout)

        return self.parent

    def create_sync(self, *largs):
        print "create sync"


if __name__ in ('__main__', '__android__'):
    FtpSyncApp().run()