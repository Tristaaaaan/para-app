from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from kivymd.uix.card import MDCardSwipe
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ColorProperty
from kivy.clock import Clock

import threading
import validate

from fareCalculation import Computation
from routes import *
from datetime import datetime
from database import Database
import moneyFormat


db = Database()

from libs.baseclass import MainWindow
from libs.baseclass import SecondWindow
from libs.baseclass import HistoryWindow





class RouteOne(FloatLayout):

    Builder.load_file('route1.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.createlist)

    def createlist(self, *args):
        for i in reversed(starting_place_1):
            item = OneLineListItem(
                text=f"{i}",
                divider=None
            )
            item.bind(on_release=self.item_selected)
            self.ids.container.add_widget(item)

    def item_selected(self, item):

        MDApp.get_running_app().root.second.starting_place.starting_point.text = item.text
        MDApp.get_running_app().root.second.starting_place.close_dialog()


class StartingPoint(MDRelativeLayout):

    def startingPlace(self):

        # Create and configure the MDDialog
        self.dialog = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            title='[font=Inter/Inter-Medium][size=18sp]Starting Point[/size][/font]',
            radius=[20, 20, 20, 20],
            md_bg_color='white',

            content_cls=RouteOne()
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()


class EndPoint(MDRelativeLayout):
    def destinationPlace(self):

        # Create and configure the MDDialog
        self.dialog = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            title='[font=Inter/Inter-Medium][size=18sp]Destination[/size][/font]',
            radius=[20, 20, 20, 20],
            md_bg_color='white',
            content_cls=RevRouteOne()
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()


class RevRouteOne(FloatLayout):
    Builder.load_file('revroute1.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.createlist)

    def createlist(self, *args):
        for i in starting_place_1:
            item = OneLineListItem(text=f"{i}", divider=None)
            item.bind(on_release=self.item_selected)
            self.ids.container.add_widget(item)

    def item_selected(self, item):
        MDApp.get_running_app().root.second.destination.end_point.text = item.text
        MDApp.get_running_app().root.second.destination.close_dialog()




class CustomMDBoxLayout(MDBoxLayout):
    pass







class WindowManager(ScreenManager):
    pass


class paraApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    paraApp().run()
