import matplotlib.pylab as pl
import numpy

import gcd
import pinv
import record
import visual


def tdoa(channels, wave_data, sampling, sensor_pos):
    time_delays = [0]
    for i in range(1, channels):
        delay = gcd.fst_delay_snd(wave_data[0], wave_data[i], sampling)
        time_delays.append(delay)
    return pinv.tdoa_to_position(time_delays, sensor_pos)


def run_once():
    sampling, wave_data, sensor_pos = record.record()
    channels = wave_data.shape[0]

    x, y, z = tdoa(channels, wave_data, sampling, sensor_pos)

    print('Calculated.')
    print("Sound located at ({0}, {1}, {2})".format(x, y, z))

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
