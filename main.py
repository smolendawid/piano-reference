from __future__ import division
import math
import threading
from tkinter import Button, Label, Tk
from core.stream import Stream
import time


class MainWindow:
    def __init__(self):
        self.frequency = 100

    def show(self):
        window = Tk()
        window.title("Piano reference")
        window.geometry('350x200')

        lbl = Label(window, text="A4")
        lbl.grid(column=2, row=1)

        running = threading.Event()

        def left_click(event):
            running.clear()
            running.set()
            s = Stream(44100)
            s.create_sine_tone(frequency, 1.)
            thread = threading.Thread(target=s.play_sine_tone, args=(running, 1,))
            thread.start()
            lbl.configure(text=frequency)

        def right_click(event):
            running.clear()
            running.set()
            s = Stream(44100)
            s.create_sine_tone(frequency, 1.)
            thread = threading.Thread(target=s.play_sine_tone, args=(running, 1,))
            thread.start()
            lbl.configure(text=frequency)

        btn1 = Button(window, text="<<", command=lambda: left_click(None))
        btn2 = Button(window, text=">>", command=lambda: right_click(None))

        btn1.grid(column=0, row=0)
        btn2.grid(column=1, row=0)

        window.bind('<Left>', left_click)
        window.bind('<Right>', right_click)

        window.mainloop()


class TestThread(threading.Thread):
    def __init__(self, frequency):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event()
        self.frequency = frequency

        threading.Thread.__init__(self)

    def run(self):
        s = Stream(44100)
        s.create_sine_tone(self.frequency, 1.)
        s.play_sine_tone(self._stopevent.isSet(), 1.)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)


if __name__ == '__main__':
    mw = MainWindow()
    mw.show()

