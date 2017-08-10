from multiprocessing import Process, Queue, Manager

import micarray
import tdoa_open as tdoa
import visual


def get_location(sample_q, fft_lst):
    sampling, wave_data, sensor_pos = sample_q.get()
    (x, y, z), fouriers, corre = tdoa.tdoa(wave_data, sampling, sensor_pos)

    fft_arr, corre_arr = manager.list(fft_lst[0]), manager.list(fft_lst[1])
    fft_arr.append(fouriers)
    corre_arr.append(fouriers)
    fft_lst[0] = fft_arr
    fft_lst[1] = corre_arr

    print('Calculated. The position is ({0}, {1})'.format(x, y))
    return x, y


def push_record(sample_q):
    rec_len = 0.1  # in second
    while True:
        while sample_q.qsize() > 2:  # don't accumulate too much delay
            sample_q.get()
        sample_q.put(micarray.record(rec_len))
        print('{0} samples in the queue.'.format(sample_q.qsize()))


def pop_record(sample_q, fft_lst):
    while len(fft_lst[0]) < 20:
        result = get_location(sample_q, fft_lst)


if __name__ == '__main__':
    sample_q = Queue()
    manager = Manager()
    fft_lst = manager.list()
    fft_lst.append([])
    fft_lst.append([])
    p1 = Process(target=push_record, args=(sample_q,))
    p1.start()
    p2 = Process(target=pop_record, args=(sample_q, fft_lst))
    p2.start()
    p2.join()
    # If p2 ended
    p1.terminate()
    visual.make_fft_graph(*fft_lst)
