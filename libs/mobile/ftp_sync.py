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

        new_button.bind(on_press=self.go_to_create_sync_page)
        return box_layout

    def create_new_sync(self):
        box_layout = BoxLayout(orientation='vertical')
        stopButtonHeight = 90
        new_button = Button(text="Create", height=stopButtonHeight)
        box_layout.add_widget(new_button)
        new_button.bind(on_press=self.create_sync_clicked)
        return box_layout

    def create_sync_clicked(self, *largs):
        print 'create_sync_clicked'
        self.parent.current = "List"

    def build(self):
        self.parent = ScreenManager()
        screen = Screen(name="List")
        self.parent.add_widget(screen)

        sync_list = self.create_sync_list()
        screen.add_widget(sync_list)

        new_sync = self.create_new_sync()
        new_sync_screen = Screen(name="New")
        new_sync_screen.add_widget(new_sync)
        self.parent.add_widget(new_sync_screen)
        return self.parent

    def go_to_create_sync_page(self, *largs):
        print "create sync"
        self.parent.current = "New"


if __name__ in ('__main__', '__android__'):
    FtpSyncApp().run()