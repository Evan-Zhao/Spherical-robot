from multiprocessing import Process, Queue

import micarray
import tdoa
import visual


def get_location(q):
    while q.qsize() > 2:  # don't accumulate too much delay
        q.get()
    sampling, wave_data, sensor_pos = q.get()
    x, y, z = tdoa.tdoa(wave_data, sampling, sensor_pos)
    print('Calculated. The position is ({0}, {1})'.format(x, y))
    return x, y


def push_record(q):
    rec_len = 0.5  # in second
    while True:
        q.put(micarray.record(rec_len))
        print('{0} samples in the queue.'.format(q.qsize()))


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=push_record, args=(q,))
    p1.start()
    visual.point_animation(get_location, q)
    p1.join()
