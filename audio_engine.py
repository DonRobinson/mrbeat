# from audiostream.core import get_output
from audio_source_mixer import AudioSourceMixer
from audio_source_one_shot import AudioSourceOneShot
from audio_source_track import AudioSourceTrack

import pyaudio


class AudioEngine:
    NB_CHANNELS = 1  # mono
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    FORMAT = pyaudio.paInt16

    # Create an interface to PortAudio
    def __init__(self):
        self.p = pyaudio.PyAudio()
        '''self.output_stream = get_output(channels=self.NB_CHANNELS,
                                        rate=self.SAMPLE_RATE,
                                        buffersize=self.BUFFER_SIZE) '''
        self.output_stream = self.p.open(format=self.FORMAT,
                                         channels=self.NB_CHANNELS,
                                         rate=self.SAMPLE_RATE,
                                         output=True)

        self.audio_source_one_shot = AudioSourceOneShot()  # self.output_stream)
        self.audio_source_one_shot.start_stream()

    def play_sound(self, wav_samples):
        self.audio_source_one_shot.set_wav_samples(wav_samples)

    def create_track(self, wav_samples, bpm):
        source_track = AudioSourceTrack(self.output_stream, wav_samples, bpm, self.SAMPLE_RATE)
        # source_track.set_steps((1, 0, 0, 0))
        source_track.start_stream()
        return source_track

    def create_mixer(self, all_wav_samples, bpm, nb_steps, on_current_step_changed, min_bpm):
        p = pyaudio.PyAudio()
        mixer = AudioSourceMixer(self.output_stream, p, all_wav_samples, bpm, self.SAMPLE_RATE, nb_steps,
                                 on_current_step_changed, min_bpm)
        mixer.start_stream()
        return mixer
        # create the audio source mixer
        # start it
        # return it
