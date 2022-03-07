from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton


Builder.load_file("track.kv")


class TrackStepButton(ToggleButton):
    pass


class TrackSoundButton(Button):
    pass


class TrackWidget(BoxLayout):
    def __init__(self, sound, audio_engine, tracks_nb_steps, track_source, steps_left_align, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.audio_engine = audio_engine
        self.sound = sound
        self.tracks_nb_steps = tracks_nb_steps

        self.track_source = track_source
        # self.track_source = audio_engine.create_track(sound.samples, 120)

        # 1 - Images for the sound button "sound_button_normal.png ...
        # 2 - group sound_button and sparator_ image in a Boxlayout (width = steps_left_align)

        button_separator_box = BoxLayout()
        button_separator_box.orientation: "horizontal"
        button_separator_box.size_hint_x = None
        button_separator_box.width = steps_left_align
        self.add_widget(button_separator_box)
        sound_button = TrackSoundButton()
        sound_button.width = steps_left_align
        sound_button.text = sound.displayname
        sound_button.on_press = self.on_sound_button_press
        # self.add_widget(sound_button)
        button_separator_box.add_widget(sound_button)

        # separator
        separator_image = Image(source="images/track_separator.png")
        separator_image.size_hint_x = None
        separator_image.width = dp(15)
        # self.add_widget(separator_image)
        button_separator_box.add_widget(separator_image)

        self.step_buttons = []
        for i in range(0, self.tracks_nb_steps):
            step_button = TrackStepButton()
            if i % 8 < 4:
                step_button.background_normal: "images/step_normal1.png"
            else:
                step_button.background_normal: "images/step_normal2.png"
            step_button.bind(state=self.on_step_buttton_state)
            self.step_buttons.append(step_button)
            self.add_widget(step_button)

    def on_sound_button_press(self):
        self.audio_engine.play_sound(self.sound.samples)

    def on_step_buttton_state(self, widget, value):
        steps = []
        for i in range(0, self.tracks_nb_steps):
            if self.step_buttons[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)
        # print(steps)
        self.track_source.set_steps(steps)


