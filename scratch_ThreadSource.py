import cython, array
from threading import Thread
from pyaudio import  *
# Copied from https://raw.githubusercontent.com/kivy/audiostream/master/audiostream/sources/thread.pyx
# Can't use it because it needs to AudioSample class.

# from audiostream.core import AudioSample

    # Only include code for thread in ThreadSource of now. Omit "stream" code.

''' This is the ThreadSource file from audiostream. I could modify it to work with
    this project which uses PyAudio. If not, I need to change:
    1. get_bytes to the code that gets the bytes - which could be just the bytes passed to the function
    2. run is the code that plays the sample
    3. stop probably closes the thread - check the PyAudio documentation
    4. It could be a good idea to use it, because it is derived from Thread and so can be used to wait etc 
    to make the program threadsafe.'''


class ThreadSource(Thread):
    def __init__(self, stream):
        Thread.__init__(self)
        self.sample = None
        self.daemon = True
        self.stream = stream
        '''self.buffersize = stream.buffersize
        self.channels = stream.channels
        self.rate = stream.rate
        # self.sample = AudioSample()
        stream.add_sample(self.sample)'''

    def get_bytes(self):
        return 'hello'

    def run(self):
        self.stream.start_stream()
        while True:
            self.stream.write(self.get_bytes())

    def stop(self):
        self.stream.close()

