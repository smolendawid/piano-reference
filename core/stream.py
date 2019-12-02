
import pyaudio
import numpy as np


class Stream:
    def __init__(self, sample_rate):
        self.p = pyaudio.PyAudio()
        self.sample_rate = sample_rate

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=sample_rate,
                                  output=True)
        self.samples = 0.

    def create_sine_tone(self, frequency, duration):
        # generate samples, note conversion to float32 array
        self.samples = (np.sin(2 * np.pi * np.arange(self.sample_rate * duration) * frequency
                               / self.sample_rate)).astype(np.float32)

    def play_sine_tone(self, stop, volume=1.):
        """
        :param frequency:
        :param duration:
        :param volume:
        :param sample_rate:
        :return:
        """

        # play. May repeat with different volume values (if done interactively)
        while not stop:
            self.stream.write(volume * self.samples)

        self.p.terminate()
        self.finish()

    def finish(self):
        self.p.terminate()
        self.stream.stop_stream()
        self.stream.close()


