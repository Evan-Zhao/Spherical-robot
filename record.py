# import wave
# import os
import math

import numpy
import pyaudio

# Constant area.
channels = 6
rate = 48000
chunk = 1200
record_len = 1  # in second
filename = 'temp.wav'
devicename = 'USBStreamer: Audio (hw:2,0)'
# Bit depth and max value goes together.
record_format, record_maxvalue, numpy_format = pyaudio.paInt32, 2**(32-1), numpy.int32 #pyaudio.paFloat32, "S32_LE"

# Initialization.
p = pyaudio.PyAudio()
idx = None
for i in range(p.get_device_count()):
    if p.get_device_info_by_index(i).get('name') == devicename:
        idx = i
        break
if idx == None:
    raise Exception('No micarray found.')


def get_sensor_pos():
    outer_sensors = 6
    outer_sensor_R = 3.25 * (10 ** (-2))  # In meter
    arg0 = 2 * math.pi / outer_sensors
    outer_sensors_arg_multiples = [1, 4, 0, 3, 5, 2]

    sensors_pos = []
    for i in range(0, outer_sensors):
        arg = arg0 * outer_sensors_arg_multiples[i]
        coord_i = outer_sensor_R * math.cos(arg), outer_sensor_R * math.sin(arg), 0
        sensors_pos.append(coord_i)
    return sensors_pos

pos = get_sensor_pos()


def record():
    stream = p.open(format=record_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    output=True,
                    input_device_index=idx,
                    frames_per_buffer=chunk)
    print('Begin recording...')
    wave_data = numpy.empty((channels,0), dtype=numpy_format)
    for i in range(0, int(rate / chunk * record_len)):
        data = stream.read(chunk, exception_on_overflow = False)
        np_tmp = numpy.frombuffer(data, dtype=numpy_format)
        np_tmp = numpy.reshape(np_tmp, (chunk, channels))
        np_tmp = np_tmp.transpose()
        wave_data = numpy.append(wave_data, np_tmp, axis=1)
    stream.stop_stream()
    stream.close()
    print('Finished recording.')
    return rate, record_maxvalue, wave_data, pos