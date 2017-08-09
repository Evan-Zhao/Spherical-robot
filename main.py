import matplotlib.animation as anim
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy
import pyaudio

import record, gcd, pinv

n = 0
max_channel_delay = 0.1
bound = 1

fig1 = plt.figure()
ln_o, = plt.plot([], [], 'ro')
ln_x, = plt.plot([], [], 'bx')

p2 = pyaudio.PyAudio()


def tdoa(channels, wave_data, sampling, sensor_pos):
    time_delays = [0]
    for i in range(1, channels):
        delay = gcd.fst_delay_snd(wave_data[0], wave_data[i], sampling, max_channel_delay)
        time_delays.append(delay)
    print(str(time_delays))
    return pinv.tdoa_to_position(time_delays, sensor_pos)


def update(*args):
    sampling, maxvalue, wave_data, sensor_pos = record.record()
    channels = wave_data.shape[0]

    x, y, z = tdoa(channels, wave_data, sampling, sensor_pos)

    print('Calculated.')
    print("Sound located at ({0}, {1}, {2})".format(x, y, z))

    global ln_o, ln_x
    if -bound < x < bound and -bound < y < bound:
        ln_o.set_data([x], [y])
        ln_x.set_data([], [])
        return ln_o,
    else:
        ln_x.set_data([0], [0])
        ln_o.set_data([], [])
        return ln_x,


def init():
    plt.xlim(-bound, bound)
    plt.ylim(-bound, bound)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('test')
    return ln_o,


def main():
    ani = anim.FuncAnimation(fig1, update, init_func=init, interval=500, blit=True)
    plt.show()

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


