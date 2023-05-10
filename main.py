# MARK TRISTAN FABELLAR
# CPE 2 - 2

# An offline jeepney fare guide mobile application


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineListItem
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from routes import starting_place_1
import validate
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout

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
        MDApp.get_running_app().root.second.starting_place.text = item.text
        MDApp.get_running_app().root.second.close_dialog()
        
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
        MDApp.get_running_app().root.second.destination.text = item.text
        MDApp.get_running_app().root.second.close_dialog()

class MainWindow(Screen):

    Builder.load_file('main_window.kv')

    def category_(self, checkbox, active):
        if active:
            self.ids.status.text = "Student/ Elderly/ Disabled"
        else:
            self.ids.status.text = "Regular"


class SecondWindow(Screen):

    Builder.load_file('second_window.kv')

    # Route 

    def route1(self):
        return_button = MDFlatButton(
            text='SUBMIT',
            on_release=self.close_dialog,
        )

        self.dialog = MDDialog(
            title="Starting Place",
            type="custom",
            content_cls=RouteOne(),
            size_hint=(0.9, None),
            buttons=[
                return_button
            ],
        )

        self.dialog.open()

    def revroute1(self):
        return_button = MDFlatButton(
            text='SUBMIT',
            on_release=self.close_dialog,
        )

        self.dialog = MDDialog(
            title="Destination",
            type="custom",
            content_cls=RevRouteOne(),
            size_hint=(0.9, None),
            buttons=[
                return_button
            ],
        )

        self.dialog.open()

    # Route: Validate Inputs
    def validate(self):
        if validate.check(self.ids.starting_place.text, self.ids.destination.text, self.ids.passenger.text, self.ids.minimum_fare.text) is True:
            self.invalid_input()

        else:
            self.output()
            self.manager.current = "output"
            self.manager.transition.direction = "left"

    def refresh(self):
        self.ids.starting_place.text = ''
        self.ids.destination.text = ''
        self.ids.passenger.text = '1'
        self.ids.minimum_fare.text = '9'

    # Route: Output
    def output(self):

        # Status
        status = self.manager.main.status.text

        # Status and Discount
        if status == "Regular":
            self.manager.output.status.text = "Regular"
            self.manager.output.discount.text = "None"
        else:
            self.manager.output.status.text = "Discounted"
            self.manager.output.discount.text = "20%"

        starting_place = self.ids.starting_place.text
        destination = self.ids.destination.text
        passenger = self.ids.passenger.text
        minimum_fare = self.ids.minimum_fare.text

        # Transit
        self.manager.output.transit.text = starting_place+" - "+destination

        # Total

        # Getting the distance of starting place and destination in km
        distance1 = int(starting_place_1.index(starting_place))
        distance2 = int(starting_place_1.index(destination))

        # Subtracting the distance of the two to get the final distance
        total_distance1 = abs(distance1 - distance2)

        self.manager.output.distance.text = str(total_distance1) + " KM"

        # Number of passenger
        number_of_passenger = int(passenger)

        # Minimum Fare
        minimum_fare = int(minimum_fare)

        # When the total distance is less than 4 then the tentative cost = 9 (Minimum Fare)
        if total_distance1 <= 4:
            tentative_cost = minimum_fare * number_of_passenger
        # Else, the total distance is the result of the formula below.
        else:
            tentative_cost = (((total_distance1 - 4) * 1.50) + minimum_fare) * number_of_passenger

        # If status is student/ elderly/ disabled, discount is 20%
        if status == "Regular":
            fare_cost = tentative_cost
        else:
            discount_ = round((tentative_cost * 0.20), 2)
            fare_cost = tentative_cost - discount_

        self.manager.output.total.text = "₱ " + str('{:.2f}'.format(fare_cost))  # The fare cost


    def invalid_input(self):
        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text='[color=#000000]There was an error processing your data. Kindly fill-up all the required information correctly to proceed to the next step. Thank you![/color]',
            size_hint=(0.9, None),
            radius=[20, 7, 20, 7],
            buttons=[close_button],
        )
        self.dialog.open()

    # Close operation
    def close_dialog(self, *args):
        self.dialog.dismiss()

    def on_pre_enter(self):
        self.ids.starting_place.bind(on_text_validate=self.close_dialog)

class OutputWindow(Screen):

    Builder.load_file('output_window.kv')

    def reset(self):
        self.manager.second.starting_place.text = ''
        self.manager.second.destination.text = ''
        self.manager.second.minimum_fare.text = '9'
        self.manager.second.passenger.text = '1'

        self.ids.status.text = ''
        self.ids.discount.text = ''
        self.ids.transit.text = ''
        self.ids.total.text = ''
        self.ids.distance.test = ''

        self.manager.current = "main"
        self.manager.transition.direction = "right"

        
class WindowManager(ScreenManager):
    pass


class paraApp(MDApp):

    def build(self):

        return WindowManager()

if __name__ == '__main__':
    paraApp().run()
