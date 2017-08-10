from ctypes import c_long
from math import atan2, pi
from multiprocessing import Process, Queue, Value

import micarray
import tdoa_open as tdoa


def get_location(sample_q):
    sampling, wave_data, sensor_pos = sample_q.get()
    (x, y, z), fouriers, corre = tdoa.tdoa(wave_data, sampling, sensor_pos)
    if x != 0 or y != 0:
        angle = atan2(y, x) * 180 / pi
        print('Calculated. The position is ({0}, {1}); angle {2} degrees'.format(x, y, angle))
    else:
        print('Nullary vector; ignored.')
    return x, y


def push_record(sample_q):
    rec_len = 0.1  # in second
    while True:
        while sample_q.qsize() > 2:  # don't accumulate too much delay
            sample_q.get()
        sample_q.put(micarray.record(rec_len))
        print('{0} samples in the queue.'.format(sample_q.qsize()))


def pop_record(sample_q, cnt):
    while cnt.value < 20:
        result = get_location(sample_q)
        cnt.value += 1


if __name__ == '__main__':
    sample_q = Queue()
    val = Value(c_long)
    p1 = Process(target=push_record, args=(sample_q,))
    p1.start()
    p2 = Process(target=pop_record, args=(sample_q, val))
    p2.start()
    p2.join()
    # If p2 ended
    p1.terminate()
