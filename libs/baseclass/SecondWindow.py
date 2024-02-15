from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import validate
from fareCalculation import Computation
import threading
import datetime

from database import Database

db = Database()

class ApproveExpense(MDBoxLayout):
    text = StringProperty()
    distance = StringProperty()
    total = StringProperty()

    def cancel(self):
        MDApp.get_running_app().root.second.close_dialog()
        MDApp.get_running_app().root.second.clear()


class DeniedExpense(MDBoxLayout):
    pass


class SecondWindow(Screen):

    Builder.load_file('libs/kv/SecondWindow.kv')

    def clear(self):
        self.ids.starting_place.starting_point.text = ''
        self.ids.destination.end_point.text = ''
        self.ids.passenger.text = '1'
        self.ids.minimum_fare.text = '12'

    def close_dialog(self, *args):
        self.added.dismiss()

    def input_added(self, transit_, distance_, fare_):

        self.added = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            title='Summary',
            radius=[20, 20, 20, 20],
            auto_dismiss=False,
            md_bg_color='white',
            content_cls=ApproveExpense(
                text=transit_, distance=distance_, total=fare_)
        )
        self.added.open()

    def input_denied(self):
        self.dialog = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            elevation=0,
            auto_dismiss=False,
            radius=[20, 20, 20, 20],
            content_cls=DeniedExpense()
        )
        self.dialog.open()
        # Schedule the dialog dismissal after 3 seconds
        Clock.schedule_once(lambda dt: self.dialog.dismiss(), 3)

    def validate(self):
        if validate.check(self.ids.starting_place.starting_point.text,
                          self.ids.destination.end_point.text,
                          self.ids.passenger.text,
                          self.ids.minimum_fare.text) is True:
            self.input_denied()
        else:
            threading.Thread(target=self.output()).start()

    def output(self):
        outputs = Computation.calculate(
            self.manager.main.status.text,
            self.ids.starting_place.starting_point.text,
            self.ids.destination.end_point.text,
            float(self.ids.passenger.text),
            float(self.ids.minimum_fare.text)
        )
        transit = outputs[2]

        distance = str(outputs[3]) + "KM"

        fare = "₱ " + str('{:.2f}'.format(outputs[4]))
        threading.Thread(target=self.input_added(transit, distance, fare))

        date = datetime.now().strftime('%B %d, %Y')
        current_time = datetime.now().strftime('%I:%M %p')

        current_date = f"{date}, {current_time}"

        db.createFareInfo(
            self.ids.starting_place.starting_point.text,
            self.ids.destination.end_point.text,
            self.ids.minimum_fare.text,
            self.ids.passenger.text,
            outputs[3],
            outputs[4],
            self.manager.main.status.text,
            current_date
        )

    def refresh(self):
        self.ids.starting_place.text = ''
        self.ids.destination.text = ''
        self.ids.passenger.text = '1'
        self.ids.minimum_fare.text = '12'