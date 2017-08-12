from math import atan2, pi
from multiprocessing import Process, Queue

import com.bidir as bidir
import micarray
import tdoa_open as tdoa


def get_location(sampling, wave_data, sensor_pos):
    (x, y, z), fouriers, corre = tdoa.tdoa(wave_data, sampling, sensor_pos)
    if x != 0 or y != 0:
        angle = atan2(y, x) * 180 / pi
        print('Calculated. The position is ({0}, {1}); angle {2} degrees'.format(x, y, angle))
        return angle
    else:
        print('Nullary vector; ignored.')
        return None


def push_record(sample_q):
    rec_len = 0.1  # in second
    while True:
        while sample_q.qsize() > 2:  # don't accumulate too much delay
            sample_q.get()
        sample_q.put(micarray.record(rec_len))
        print('{0} samples in the queue.'.format(sample_q.qsize()))


def pop_record(sample_q, socket, ip_str, port):
    while True:
        args = sample_q.get()
        result = get_location(*args)
        res_str = '<{0}>'.format(result)
        if not result is None:
            sent = bidir.emit(socket, res_str, ip_str, port)
            if not sent:
                break  # Some fatal error, and socket closed


def signal_terminate(socket):
    while True:
        reply = socket.recv(1024)
        if reply.decode() == "end":
            print('Program term\'ed by remote.')
            break


if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 10002
    sock = bidir.establish(ip, port)
    sample_q = Queue()
    p1 = Process(target=push_record, args=(sample_q,))
    p2 = Process(target=pop_record, args=(sample_q, sock, ip, port))
    p3 = Process(target=signal_terminate, args=(sock,))
    p1.start()
    p2.start()
    p3.start()
    alive = True
    while alive:
        alive = p1.is_alive() and p2.is_alive() and p3.is_alive()
    # If any thread ended,
    # then there's something wrong,
    # or remote side terminated our program (as the end of p3).
    # then we terminate the others.
    p1.terminate()
    p2.terminate()
    p3.terminate()
