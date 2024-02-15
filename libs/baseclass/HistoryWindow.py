from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty
import datetime
from kivymd.uix.card import MDCardSwipe
import moneyFormat
from kivymd.uix.list import MDListItem
from database import Database

db = Database()


class ListItemWithIcon(MDListItem):
    '''Custom list item'''


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


class HistoryWindow(Screen):

    Builder.load_file('libs/kv/HistoryWindow.kv')

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

                    self.transit = spent[1]+" to "+spent[2]
                    self.fare = "₱" + str('{:.2f}'.format(spent[6]))
                    add_expenses = SwipeToDeleteItem(pk=spent[0],
                                                     text="[font=Inter/Inter-Medium][size=18sp]" + self.transit + "[/size][/font]", secondary_text="[font=Inter/Inter-Regular][size=14sp]" + spent[8] + "[/size][/font]", icon=self.icon, md_bg_color=self.md_bg_color, icon_color=self.icon_color, fareTextRight=self.fare)

                    self.ids.listexpenses.add_widget(add_expenses)
            else:
                self.ids.overall.text = str((moneyFormat.money(0)))
        except ValueError as e:
            print(e)
