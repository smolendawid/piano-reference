from __future__ import division
import math
from tkinter import Button, Label, Tk

from pyaudio import PyAudio


def sine_tone(frequency, duration, volume=1., sample_rate=22050):
    """
    https://stackoverflow.com/a/974291/6329992
    :param frequency:
    :param duration:
    :param volume:
    :param sample_rate:
    :return:
    """
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=sample_rate,
                    output=True)
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
    for buf in zip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()


def main():

    window = Tk()
    window.title("Piano reference")
    window.geometry('350x200')

    lbl = Label(window, text="A4")
    lbl.grid(column=2, row=1)

    def left_click():
        lbl.configure(text="")

    def right_click():
        lbl.configure(text="")

    btn1 = Button(window, text="<<", command=left_click)
    btn2 = Button(window, text=">>", command=right_click)

    btn1.grid(column=0, row=0)
    btn2.grid(column=1, row=0)

    window.mainloop()


if __name__ == '__main__':
    main()
