import tdoa.gcd as gcd
import tdoa.pinv as pinv


def tdoa(wave_data, sampling, sensor_pos):
    channels = wave_data.shape[0]
    time_delays = [0]
    for i in range(1, channels):
        delay = gcd.fst_delay_snd(wave_data[0], wave_data[i], sampling)
        time_delays.append(delay)
    print(str(time_delays))
    return pinv.tdoa_to_position(time_delays, sensor_pos)
