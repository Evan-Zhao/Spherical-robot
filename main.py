from multiprocessing import Process, Queue

import matplotlib.pylab as pl
import numpy

import micarray
import tdoa
import visual


def get_location(q):
    sampling, wave_data, sensor_pos = q.get()
    x, y, z = tdoa.tdoa(wave_data, sampling, sensor_pos)
    print('Calculated. The position is ({0}, {1})'.format(x, y))
    return x, y


def push_record(q):
    while True:
        q.put(micarray.record())
        print('{0} samples in the queue.'.format(q.qsize()))


if __name__ == '__main__':
    q = Queue()
    p = Process(target=push_record, args=(q,))
    p.start()
    visual.point_animation(get_location, q)
    p.join()


def plot_channel(audio, sampling):
    channels, nframes = audio.shape[0], audio.shape[1]
    time_range = numpy.arange(0, nframes) * (1.0 / sampling)

    for i in range(1, channels + 1):
        pl.figure(i)
        pl.plot(time_range, audio[i - 1])
        pl.xlabel("time{0}".format(i))

    pl.show()
