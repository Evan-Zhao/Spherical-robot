import math

import matplotlib.pylab as pl
import numpy

from obsolete.temp import record

sampling, maxvalue, wave_data = record.record()

# Pick out two channels for our study.
w1, w2 = wave_data[0:2]
nframes = w1.shape[0]

# Get their reduced (amplitude) version, and
# calculate correlation.
a = numpy.array(w1, dtype=numpy.double) / maxvalue
b = numpy.array(w2, dtype=numpy.double) / maxvalue
# cor = numpy.correlate(a, b, 'same')

# Plot the channels, also the correlation.
time_range = numpy.arange(0, nframes)*(1.0/sampling)

pl.figure(1)
pl.plot(time_range, w1)
pl.xlabel("time1")
pl.figure(2)
pl.plot(time_range, w2, c="r")
pl.xlabel("time2")
pl.figure(3)
pl.plot(time_range, wave_data[2])
pl.xlabel("time3")
pl.figure(4)
pl.plot(time_range, wave_data[3])
pl.xlabel("time4")
pl.figure(5)
pl.plot(time_range, wave_data[4])
pl.xlabel("time5")
pl.figure(6)
pl.plot(time_range, wave_data[5])
pl.xlabel("time6")
pl.figure(7)
pl.plot(time_range, wave_data[6])
pl.xlabel("time7")
pl.figure(8)
pl.plot(time_range, wave_data[7])
pl.xlabel("time8")
#pl.show()

amplitude = []
for i in range(0,6):
    w = wave_data[i]
    len = w.shape[0]
    acc = 0.0
    for d in w:
        acc += d / len * d
    acc = math.sqrt(acc)
    amplitude.append(acc)
    print("Channel {0} amplitude: {1}".format(i, acc))

# pl.figure(7)
# pl.plot(time_range, cor)
# pl.show()
