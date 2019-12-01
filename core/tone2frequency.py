
def tone2frequency(tone: int, use_stretch_factor: bool = True):
    """ Read the post
    https://music.stackexchange.com/questions/17256/what-are-the-true-frequencies-of-the-piano-keys/46021#46021
    stretch factor was set to 0.025 for every octave around the A4=440Hz
    :return:
    """
    a4_int = 49
    a4_tempered = 440.

    if use_stretch_factor:
        mod = abs(tone - a4_int) // 6
        s = mod * 0.025
    else:
        s = 0.

    n = tone - a4_int

    if tone > a4_int:
        freq = a4_tempered * 2 ** ((n + ((s / 2) * ((n / 12) ** 2))) / 12)
    else:
        freq = a4_tempered * 2 ** ((n - ((s / 2) * ((n / 12) ** 2))) / 12)

    return freq


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    tone2frequency(40)

    s1 = [tone2frequency(i) for i in range(88)]
    s2 = [tone2frequency(i, use_stretch_factor=False) for i in range(88)]

    plt.figure()
    plt.plot(np.array(s1) - np.array(s2))
    plt.show()
