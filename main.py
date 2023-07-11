from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomsheet import MDBottomSheet
import moneyFormat
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ColorProperty
from kivy.clock import Clock
import threading
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from fareCalculation import Computation
from database import Database
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, OneLineListItem,  MDList, ILeftBodyTouch
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.boxlayout import MDBoxLayout
from routes import *
from datetime import datetime
db = Database()


class ApproveExpense(MDBoxLayout):
    text = StringProperty()
    distance = StringProperty()
    total = StringProperty()

    def cancel(self):
        MDApp.get_running_app().root.second.close_dialog()


class DeniedExpense(MDBoxLayout):
    pass


class RouteOne(FloatLayout):

    Builder.load_file('route1.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.createlist)

    def createlist(self, *args):
        for i in reversed(starting_place_1):
            item = OneLineListItem(text=f"{i}", divider=None)
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
            title='Summary',
            radius=[20, 20, 20, 20],
            auto_dismiss=False,
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
            title='Summary',
            radius=[20, 20, 20, 20],
            auto_dismiss=False,
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


class MainWindow(Screen):

    Builder.load_file('main_window.kv')

    def category_(self, checkbox, active):
        if active:
            self.ids.status.text = "Discount Beneficiary"
        else:
            self.ids.status.text = "Regular Commuter"


class SecondWindow(Screen):

    Builder.load_file('second_window.kv')

    def close_dialog(self, *args):
        self.added.dismiss()

    # Route3: Validate Input

    def input_added(self, transit_, distance_, fare_):

        self.added = MDDialog(
            size_hint=(0.85, None),
            type="custom",
            title='Summary',
            radius=[20, 20, 20, 20],
            auto_dismiss=False,

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
        starting_place3 = self.ids.starting_place.starting_point.text
        destination3 = self.ids.destination.end_point.text
        passenger3 = self.ids.passenger.text
        minimum_fare3 = self.ids.minimum_fare.text
        if (starting_place3 == ''
                or destination3 == ''
                or starting_place3 not in starting_place_1
                or destination3 not in starting_place_1
                or not passenger3.isnumeric()
                or not minimum_fare3.isnumeric()
                or int(passenger3) < 1
                or int(minimum_fare3) < 1):
            self.input_denied()

        else:
            threading.Thread(target=self.output()).start()

    def output(self):
        outputs = Computation.calculate(
            self.manager.main.status.text,
            self.ids.starting_place.starting_point.text,
            self.ids.destination.end_point.text,
            self.ids.passenger.text,
            self.ids.minimum_fare.text
        )
        transit = outputs[2]

        distance = str(outputs[3]) + "KM"

        fare = "₱ " + str('{:.2f}'.format(outputs[4]))
        threading.Thread(target=self.input_added(transit, distance, fare))

        current_date = datetime.now().strftime('%A, %B %d, %Y')
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


class CustomMDBoxLayout(MDBoxLayout):
    pass


class CustomIconLeftWidget(IconLeftWidget):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty()
    md_bg_color = ColorProperty()
    icon_color = ColorProperty()
    fareTextRight = StringProperty()

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def remove_item(self, instance):
        self.parent.remove_widget(instance)

        db.delete_expense(instance.pk)

        try:
            length = db.all_data()
            if length != []:

                expenses = int(db.expenses_sum())

                MDApp.get_running_app().root.history.ids.overall.text = str(
                    (moneyFormat.money(expenses)))
            else:
                MDApp.get_running_app().root.history.ids.overall.text = str(
                    (moneyFormat.money(0)))
        except ValueError:
            pass


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''
    # divider = None


class HistoryWindow(Screen):

    Builder.load_file('history_window.kv')

    def on_enter(self):
        self.ids.listexpenses.clear_widgets()
        current_month = datetime.now().strftime('%B')
        self.ids.month.text = 'Month of ' + current_month
        all_expenses = db.all_data()
        try:
            if all_expenses != []:
                expenses = int(db.expenses_sum())
                self.ids.overall.text = str((moneyFormat.money(expenses)))
                for spent in reversed(all_expenses):
                    if spent[7] == 'Regular Commuter':
                        self.icon_color = (0, 119/255, 1, 1)
                        self.md_bg_color = (189/255, 220/255, 1, 1)
                        self.icon = 'tag-outline'
                    else:
                        self.icon_color = (0, 168/255, 107/255, 1)
                        self.md_bg_color = (207/255, 250/255, 234/255, 1)
                        self.icon = 'tag-minus-outline'

                    self.transit = spent[1]+" - "+spent[2]
                    self.fare = "₱" + str('{:.2f}'.format(spent[6]))
                    add_expenses = SwipeToDeleteItem(pk=spent[0],
                                                     text="[font=Inter/Inter-Medium][size=14]" + self.transit + "[/size][/font]", secondary_text="[font=Inter/Inter-Regular][size=10]" + spent[8] + "[/size][/font]", icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color, fareTextRight=self.fare)

                    self.ids.listexpenses.add_widget(add_expenses)
            else:
                self.ids.overall.text = str((moneyFormat.money(expenses)))
        except ValueError as e:
            print(e)


class WindowManager(ScreenManager):
    pass


class paraApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    paraApp().run()
