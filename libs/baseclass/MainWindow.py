from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class MainWindow(Screen):

    Builder.load_file('libs/kv/MainWindow.kv')

    def category_(self, checkbox, active):
        if active:
            self.ids.status.text = "Discount Beneficiary"
        else:
            self.ids.status.text = "Regular Commuter"