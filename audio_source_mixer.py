from array import array

# from audiostream.sources.thread import ThreadSource
import pyaudio

from audio_source_track import AudioSourceTrack

MAX_16bits = 32767
MIN_16bits = -32768


def sum_16bits(n):
    s = sum(n)
    if s > MAX_16bits:
        s = MAX_16bits
    elif s < MIN_16bits:
        s = MIN_16bits
    return s


class AudioSourceMixer(pyaudio.Stream):     # ThreadSource):
    buf = None

    # AudioSourceMixer
    #   init
    #       AudioSourceTrack (but we don't start them)
    #       AudioSourceTrack (but we don't start them)
    #       AudioSourceTrack (but we don't start them)
    #   start()
    #       get_bytes()     // called by the audio library
    #           loop on our tracks
    #               buffers = track.get_bytes

    def __init__(self, output_stream, p_manager, all_wav_samples, bpm, sample_rate, nb_steps, on_current_step_changed, min_bpm, *args, **kwargs):
        # ThreadSource.__init__(self, output_stream, *args, **kwargs)
        super().__init__(p_manager, 44100, 1, pyaudio.paInt16, input=False, output=True, *args, **kwargs)
        self.tracks = []
        for i in range(0, len(all_wav_samples)):
            p = pyaudio.PyAudio()
            track = AudioSourceTrack(output_stream, p, all_wav_samples[i], bpm, sample_rate, min_bpm)
            track.set_steps((0,)*nb_steps)
            self.tracks.append(track)

        buffer_nb_samples = self.tracks[0].buffer_nb_samples
        self.silence = array('h', b"\x00\x00" * buffer_nb_samples)

        self.min_bpm = min_bpm
        self.current_sample_index = 0
        self.current_step_index = 0
        self.bpm = bpm

        self.nb_steps = nb_steps
        self.sample_rate = sample_rate
        self.on_current_step_changed = on_current_step_changed
        self.is_playing = False

    def set_steps(self, index, steps):
        if index >= len(self.tracks):
            return

        if len(steps) == self.nb_steps:
            self.tracks[index].set_steps(steps)

    def set_bpm(self, bpm):
        if bpm < self.min_bpm:
            return
        self.bpm = bpm

    def audio_play(self):
        self.is_playing = True

    def audio_stop(self):
        self.is_playing = False

        # 1 step_nb_samples = 44100x15/bpm

    def get_bytes(self, *args, **kwargs):

        for i in range(0, len(self.tracks)):
            self.tracks[i].set_bpm(self.bpm)

        # initialize self.buf
        step_nb_samples = self.tracks[0].step_nb_samples

        # if not playing, then return silence here
        if not self.is_playing:
            return self.silence[0:step_nb_samples].tostring()

        track_buffers = []
        for i in range(0, len(self.tracks)):
            track = self.tracks[i]
            track_buffer = track.get_bytes_array()
            track_buffers.append(track_buffer)

        '''for i in range(0, step_nb_samples):
            self.buf[i] = 0
            for j in range(0, len(self.tracks)):
                self.buf[i] += track_buffers[j][i]'''
        s = map(sum_16bits, zip(*track_buffers))

        self.buf = array('h', s)

        # transmit current_step_index to the play indicator widget
        if self.on_current_step_changed is not None:
            # We put an offset on the step index so that the visual
            # indictation is matching when the sound will really
            # be played (this is due to audio intermediate buffers latency).
            # We chose 2 steps offset as it's giving good results.
            step_index_with_offset = self.current_step_index-2
            if step_index_with_offset < 0:
                step_index_with_offset += self.nb_steps
            self.on_current_step_changed(step_index_with_offset)

        self.current_step_index += 1
        if self.current_step_index >= self.nb_steps:
            self.current_step_index = 0

        return self.buf[0:step_nb_samples].tostring()

