from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        padding: "12dp"
        adaptive_height: True
        pos_hint: {"top": 1}

        MDIconButton:
            id: smart_tile
            box_radius: [0, 0, 16, 16]
            size_hint_y: None
            height: "240dp"
            icon: 'bus'
            on_release: bottom_sheet.open()

    MDBottomSheet:
        id: bottom_sheet
        bg_color: "grey"
        #default_opening_height: smart_tile.y - dp(12)
        size_hint_y: 1
       # height: root.height - (smart_tile.height + dp(24))
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()
