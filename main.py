from multiprocessing import Process, Queue

import micarray
import tdoa_open as tdoa


def get_location(q):
    while q.qsize() > 2:  # don't accumulate too much delay
        q.get()
    sampling, wave_data, sensor_pos = q.get()
    x, y, z = tdoa.tdoa(wave_data, sampling, sensor_pos)[0]
    print('Calculated. The position is ({0}, {1})'.format(x, y))
    return x, y


def push_record(q):
    rec_len = 0.1  # in second
    while q.qsize() < 10:
        q.put(micarray.record(rec_len))
        print('{0} samples in the queue.'.format(q.qsize()))


def pop_record(q):
    while True:
        result = get_location(q)


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=push_record, args=(q,))
    p1.start()
    p2 = Process(target=pop_record, args=(q,))
    p2.start()
    p2.join()
    # If p2 ended
    p1.terminate()
