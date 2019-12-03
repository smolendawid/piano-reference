
import pyaudio
import numpy as np


class Stream:
    def __init__(self, sample_rate):
        self.p = pyaudio.PyAudio()
        self.sample_rate = sample_rate

        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        self.samples = 0.

    def create_sine_tone(self, frequency, duration):
        self.samples = (np.sin(2 * np.pi * np.arange(self.sample_rate * duration) * frequency
                               / self.sample_rate)).astype(np.float32)

    def play_sine_tone(self, volume=1.):
        self.stream.write(volume * self.samples)

    def finish(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
