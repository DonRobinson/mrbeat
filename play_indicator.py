from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget


class TrackStepBotton(ToggleButton):
    pass


# ToggleButton -> Image
# normal/down -> source (on/of  .png)
# PlayIndicatorButton -> PlayIndicatorLight
# buttons -> lights
class PlayIndicatorLight(Image):
    pass


class PlayIndicatorWidget(BoxLayout):
    nb_steps = 0
    left_align = NumericProperty(0)
    lights = []

    def set_current_step_index(self, index):
        if index >= len(self.lights):
            return

        button = self.lights[index]
        for i in range(0, len(self.lights)):
            light = self.lights[i]
            if i == index:
                # ON
                light.source = "images/indicator_light_on.png"
            else:
                # OFF
                light.source = "images/indicator_light_off.png"

    def set_nb_steps(self, nb_steps):
        if not nb_steps == self.nb_steps:
            # reconstruct my labout -> add the buttons
            self.nb_steps = nb_steps
            self.clear_widgets()

            dummy_widget = Widget()
            dummy_widget.size_hint_x = None
            dummy_widget.width = self.left_align
            self.add_widget(dummy_widget)

            self.lights = []
            for i in range(0, nb_steps):
                light = PlayIndicatorLight()
                self.lights.append(light)
                self.add_widget(light)

# nb_steps
# current_step_index
# layout offset on the left
