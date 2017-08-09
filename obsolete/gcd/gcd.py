import matplotlib.pylab as pl
import numpy

import record


def fst_delay_snd(fst, snd, samp_rate, max_delay):
    # Verify argument shape.
    s1, s2 = fst.shape, snd.shape
    if len(s1) != 1 or len(s2) != 1 or s1[0] != s2[0]:
        raise Exception("Argument shape invalid, in 'fst_delay_snd' function")

    half_len = int(s1[0]/2)
    a = numpy.array(fst, dtype=numpy.double)
    b = numpy.array(snd, dtype=numpy.double)
    corr = numpy.correlate(a, b, 'same')
    max_pos = numpy.argmax(corr)

    # plot(s1[0], samp_rate, a, b, corr)

    return corr, (max_pos - half_len) / samp_rate


def plot(l, samp, w1, w2, cor):
    time_range = numpy.arange(0, l) * (1.0 / samp)

    pl.figure(1)
    pl.subplot(211)
    pl.plot(time_range, w1)
    pl.subplot(212)
    pl.plot(time_range, w2, c="r")
    pl.xlabel("time")

    pl.figure(2)
    pl.plot(time_range, cor)
    pl.show()


def main():
    sampling, channels, maxvalue, wave_data = record.record()
    max_channel_delay = 0.001
    delay = fst_delay_snd(wave_data[0], wave_data[1], sampling, max_channel_delay)


if __name__ == '__main__':
    main()