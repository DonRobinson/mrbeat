from kivy.config import Config
Config.set('graphics', 'width', '780')
Config.set('graphics', 'height', '360')
Config.set('graphics', 'minimum_width', '650')
Config.set('graphics', 'minimum_height', '300')
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
# from audiostream import get_output
from audio_engine import AudioEngine
from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

TRACKS_NB_STEPS = 16
MIN_BPM = 80
MAX_BPM = 160


class VerticalSpacingWidget(Widget):
    pass


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    # play_button = ObjectProperty()
    # stop_button = ObjectProperty()
    TRACK_STEPS_LEFT_ALIGN = NumericProperty(dp(120))
    step_index = 0
    bpm = NumericProperty(115)
    nb_tracks = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()
        self.audio_engine = AudioEngine()

        self.nb_tracks = self.sound_kit_service.get_nb_tracks()

        # call create_mixer(... 120, TRACKS_NB_STEPS)
        self.mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(),
                                                    self.bpm, TRACKS_NB_STEPS, self.on_mixer_current_step_changed, MIN_BPM)

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps(TRACKS_NB_STEPS)
        # 2 - test your function here
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(VerticalSpacingWidget())
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, TRACKS_NB_STEPS,
                                                      self.mixer.tracks[i], self.TRACK_STEPS_LEFT_ALIGN))
        self.tracks_layout.add_widget(VerticalSpacingWidget())

    def on_play_button_pressed(self):
        print("PLAY")
        self.mixer.audio_play()

    def on_stop_button_pressed(self):
        self.mixer.audio_stop()

    def on_mixer_current_step_changed(self, step_index):
        # print("on_mixer_current_step_changed: " + str(step_index))
        # executed in an audio thread
        self.step_index = step_index
        Clock.schedule_once(self.update_play_indicator_cbk, 0)

    def update_play_indicator_cbk(self, dt):
        if self.play_indicator_widget:
            self.play_indicator_widget.set_current_step_index(self.step_index)

    def on_bpm(self, widget, value):
        if value < MIN_BPM:
            self.bpm = 80
            return
        if value > MAX_BPM:
            self.bpm = 160
            return

        # pass to the audio engine
        self.mixer.set_bpm(self.bpm)


class MrBeatApp(App):
    pass


MrBeatApp().run()
