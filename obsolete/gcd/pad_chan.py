# This program pads the channels to make artifact delay.

import matplotlib.pylab as pl
import numpy

import obsolete.gcd.delay as delay
from obsolete.temp import record


def main():
    sampling, maxvalue, wave_data = record.record()

    # Pick out two channels for our study.
    w1, w2 = wave_data[0:2]
    nframes = w1.shape[0]

    # Pad one channel in the head, while the other in the tail,
    # to guarantee same length.
    pad_time_len = 0.01  # second
    pad_len = int(pad_time_len * sampling)
    pad_arr = numpy.zeros(pad_len)
    wp1 = numpy.concatenate((pad_arr, w1))
    wp2 = numpy.concatenate((w2, pad_arr))

    # Get their reduced (amplitude) version, and
    # calculate correlation.
    a = numpy.array(wp1, dtype=numpy.double) / maxvalue
    b = numpy.array(wp2, dtype=numpy.double) / maxvalue
    delay_time = delay.fst_delay_snd(a, b, sampling)

    # Plot the channels, also the correlation.
    time_range = numpy.arange(0, nframes + pad_len)*(1.0/sampling)

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
