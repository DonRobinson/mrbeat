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
    def __init__(self, stream, *args, **kwargs):
        ThreadSource.__init__(self, stream, *args, **kwargs)
        self.chunk_nb_samples = 32
        self.current_sample_index = 0
        # self.buf = array('h', b"\x00\x00" * self.chunk_nb_samples)
        self.silence = b'\x00\x00' * self.chunk_nb_samples
        # self.return_bytes = self.silence
        # self.stream = stream
        '''pyaudio.PyAudio().open(format=self.FORMAT,
                                             channels=self.NB_CHANNELS,
                                             rate=self.SAMPLE_RATE,
                                             output=True)'''

    # This causes the sound to play (so this needs to be derived from stream or contain a stream)
    # best to contain a stream because I only need one function (write) anyway.
    def set_wav_samples(self, wav_samples):
        self.wav_samples = wav_samples
        self.current_sample_index = 0
        self.nb_wav_samples = len(wav_samples)

    # Overrides base class get_bytes function
    def get_bytes(self):    # , *args, **kwargs):
        return_bytes = self.silence
        if self.nb_wav_samples > 0:
            start = self.current_sample_index

            if start > self.nb_wav_samples:
                return_bytes = self.silence
            else:
                end = start + self.chunk_nb_samples
                if end < self.nb_wav_samples:
                    return_bytes = self.wav_samples[start:end]
                elif start < self.chunk_nb_samples:  # pad with zeros if not full
                    rem = self.wav_samples - start
                    print(str(rem))
                    return_bytes = self.wav_samples[start:] + self.silence[0:rem]
                self.current_sample_index += self.chunk_nb_samples
        # self.stream.write(return_bytes)
        return return_bytes

        # return self.buf.tobytes()
        # return self.buf.tobytes()
        # return self.buf.tostring()

    '''def start_stream(self):
        self.stream.start_stream()'''
