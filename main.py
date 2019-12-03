from __future__ import division

from tkinter import Button, Label, Tk
import threading

import pyaudio
import numpy as np

from core.stream import Stream
from core.tone2frequency import tone2frequency
from data.key_midi_mapping import midi_key_mapping


class ThreadPlayer:
    def __init__(self, **kwargs):
        self.play = True
        self.thread_kill = False
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True)

        self.samples = None

    def create_sine_tone(self, frequency, duration):
        self.samples = (np.sin(2 * np.pi * np.arange(self.sample_rate * duration) * frequency
                               / self.sample_rate)).astype(np.float32)

    def callback(self, in_data, frame_count, time_info, status):
        return self.samples, pyaudio.paContinue

    def start_sound(self, f):
        self.p = pyaudio.PyAudio()
        self.create_sine_tone(f, 1/f*10)
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True,
                                  stream_callback=self.callback, frames_per_buffer=len(self.samples))
        self.stream.start_stream()
        # while True and not self.thread_kill:
        #     if self.play:
                # try:
                # self.stream.write(1. * self.samples, exception_on_underflow=False)
                # except:
                #     print("thrown")
                #     continue
        # self.stream.finish()

    def stop_sound(self):
        self.play = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def start_thread(self, frequency):
        self.play = True
        self.start_sound(frequency)
        # t1 = threading.Thread(target=self.start_sound, args=(frequency,))
        # t1.start()


class MainWindow:
    def __init__(self):
        self.tone = 49  # A4
        self.frequency = 440
        self.p1 = ThreadPlayer()
        self.p2 = ThreadPlayer()

    def _frequency_increment(self):
        self.tone += 1
        self.frequency = tone2frequency(self.tone)

    def _frequency_decrement(self):
        self.tone -= 1
        self.frequency = tone2frequency(self.tone)

    def show(self):
        window = Tk()
        window.title("Piano reference")
        window.geometry('350x200')

        lbl_midi = Label(window, text="49")
        lbl_key = Label(window, text="A4")
        lbl_freq = Label(window, text="440.0")

        lbl_midi.grid(column=2, row=1)
        lbl_key.grid(column=2, row=2)
        lbl_freq.grid(column=2, row=3)

        def left_click(event):
            self._frequency_decrement()
            self.p1.stop_sound()
            self.p2.stop_sound()
            self.p1 = ThreadPlayer()
            self.p2 = ThreadPlayer()
            self.p1.start_thread(self.frequency)
            lbl_midi.configure(text=self.tone)
            lbl_key.configure(text=midi_key_mapping[self.tone])
            lbl_freq.configure(text=self.frequency)

        def right_click(event):
            self._frequency_increment()
            self.p1.stop_sound()
            self.p2.stop_sound()
            self.p1 = ThreadPlayer()
            self.p2 = ThreadPlayer()
            self.p2.start_thread(self.frequency)
            lbl_midi.configure(text=self.tone)
            lbl_key.configure(text=midi_key_mapping[self.tone])
            lbl_freq.configure(text=self.frequency)

        btn1 = Button(window, text="<<", command=lambda: left_click(None))
        btn2 = Button(window, text=">>", command=lambda: right_click(None))

        btn1.grid(column=0, row=0)
        btn2.grid(column=1, row=0)

        window.bind('<Left>', left_click)
        window.bind('<Right>', right_click)

        window.mainloop()


if __name__ == '__main__':
    mw = MainWindow()
    mw.show()

