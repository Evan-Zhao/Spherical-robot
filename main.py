import matplotlib.pylab as pl
import numpy

import micarray
import tdoa
import visual


def run_once():
    sampling, wave_data, sensor_pos = micarray.record()
    x, y, z = tdoa.tdoa(wave_data, sampling, sensor_pos)
    print('Calculated.')
    return x, y


def main():
    visual.point_animation(run_once)


if __name__ == '__main__':
    main()


def plot_channel(audio, sampling):
    channels, nframes = audio.shape[0], audio.shape[1]
    time_range = numpy.arange(0, nframes) * (1.0 / sampling)

    for i in range(1, channels + 1):
        pl.figure(i)
        pl.plot(time_range, audio[i - 1])
        pl.xlabel("time{0}".format(i))

    pl.show()
