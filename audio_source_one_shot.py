from array import array
import pyaudio
from scratch_ThreadSource import ThreadSource

# from audiostream.sources.thread import ThreadSource


class AudioSourceOneShot(ThreadSource):
    wav_samples = None
    nb_wav_samples = 0
    NB_CHANNELS = 1  # mono
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    FORMAT = pyaudio.paInt16
    OUTPUT = True
    '''
    # def __init__(self, output_stream, p_manager, *args, **kwargs):
    def __init__(self, stream_format, channels, rate, output, *args, **kwargs):    
        pyaudio.Stream.__init__(self.output_stream, 44100, channels, pyaudio.paInt16, False, True, *args, **kwargs)'''
    def __init__(self):
        self.chunk_nb_samples = 32
        self.current_sample_index = 0
        self.buf = array('h', b"\x00\x00" * self.chunk_nb_samples)
        self.stream = pyaudio.PyAudio().open(format=self.FORMAT,
                                             channels=self.NB_CHANNELS,
                                             rate=self.SAMPLE_RATE,
                                             output=True)

    # This causes the sound to play (so this needs to be derived from stream or contain a stream)
    # best to contain a stream because I only need one function (write) anyway.
    def set_wav_samples(self, wav_samples):
        self.stream.write(wav_samples)
        '''self.wav_samples = wav_samples
        self.current_sample_index = 0
        self.nb_wav_samples = len(wav_samples)
        s_bytes = self.get_bytes()
        self.stream.write(s_bytes)
        # self.stream.write(self.get_bytes())    # changed for pyaudio'''

    def get_bytes(self):    # , *args, **kwargs):

        if self.nb_wav_samples > 0:
            for i in range(0, self.chunk_nb_samples):
                if self.current_sample_index < self.nb_wav_samples:
                    self.buf[i] = self.wav_samples[self.current_sample_index]
                else:
                    self.buf[i] = 0
                self.current_sample_index += 1

        return self.buf.tobytes()
        # return self.buf.tostring()

    def start_stream(self):
        self.stream.start_stream()
