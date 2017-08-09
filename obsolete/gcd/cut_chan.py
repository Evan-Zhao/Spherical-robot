# This program cut (and shift) the channels to make artifact delay.

import matplotlib.pylab as pl
import numpy

import obsolete.gcd.delay as delay
from obsolete.temp import record


def main():
    sampling, maxvalue, wave_data = record.record()

    # Pick out two channels for our study.
    w1, w2 = wave_data[1:3]
    nframes = w1.shape[0]

    # Cut one channel in the tail, while the other in the head,
    # to guarantee same length and first delays second.
    cut_time_len = 0.2  # second
    cut_len = int(cut_time_len * sampling)
    wp1 = w1[:-cut_len]
    wp2 = w2[cut_len:]

    # Get their reduced (amplitude) version, and
    # calculate correlation.
    a = numpy.array(wp1, dtype=numpy.double) / maxvalue
    b = numpy.array(wp2, dtype=numpy.double) / maxvalue
    delay_time = delay.fst_delay_snd(a, b, sampling)

    # Plot the channels, also the correlation.
    time_range = numpy.arange(0, nframes - cut_len)*(1.0/sampling)

    # Still shows the original signal
    pl.figure(1)
    pl.subplot(211)
    pl.plot(time_range, wp1)
    pl.subplot(212)
    pl.plot(time_range, wp2, c="r")
    pl.xlabel("time")
    pl.show()

    # Print delay
    print("Chan 1 delay chan 2 by {0}".format(delay_time))

main()
