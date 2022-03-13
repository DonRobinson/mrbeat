import unittest
from audio_source_one_shot import AudioSourceOneShot
from sound_kit_service import *
from audio_engine import *
import pyaudio


class MyTestCase(unittest.TestCase):
    NB_CHANNELS = 1  # mono
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    FORMAT = pyaudio.paInt16
    OUTPUT = True

    # def __init__(self):
    p = pyaudio.PyAudio()
    output_stream = p.open(format=FORMAT,
                           channels=NB_CHANNELS,
                           rate=SAMPLE_RATE,
                           output=True)

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_stream(self):
        self.assertIsNotNone(self.output_stream, msg="AudioSourceOneShot not None")

    '''def test_one_shot(self):
        a_s = AudioSourceOneShot(self.output_stream, self.p)
        self.assertIsNotNone(a_s, msg="AudioSourceOneShot not None")
        a_s.start_stream()'''

    def test_main(self):
        sound_kit_service = SoundKitService()
        nb_tracks = sound_kit_service.get_nb_tracks()
        self.assertGreater(nb_tracks, 0, "No tracks")
        sound = sound_kit_service.get_sound_at(1)
        self.assertIsNotNone(sound)
        # audio_engine = AudioEngine()
        # audio_engine.play_sound(sound.samples)
        self.output_stream.write(sound.samples)

        one_shot = AudioSourceOneShot()
        self.assertIsNotNone(one_shot)
        one_shot.set_wav_samples(sound.samples)

if __name__ == '__main__':
    unittest.main()
