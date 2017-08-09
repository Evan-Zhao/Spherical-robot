import numpy as np

import tdoa_open.gcd as gcd
import tdoa_open.pinv as pinv


def tdoa(wave_data, sampling, sensor_pos):
    channels = wave_data.shape[0]
    time_delays = [0]
    length = wave_data.shape[1]

    fouriers = np.zeros([1, length], dtype=np.complex64)
    corre = np.zeros([1, length], dtype=np.complex64)
    for i in range(1, channels):
        delay, R, X1, Xi = gcd.fst_delay_snd(wave_data[0], wave_data[i], sampling)
        fouriers[0] = X1
        fouriers = np.append(fouriers, Xi.reshape([1, -1]), axis=0)
        corre = np.append(corre, R.reshape([1, -1]), axis=0)
        time_delays.append(delay)
    return pinv.tdoa_to_position(time_delays, sensor_pos), fouriers, corre
