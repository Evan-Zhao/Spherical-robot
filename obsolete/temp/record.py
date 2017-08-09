import wave
import pyaudio
import os
import numpy

# Constant area.
channels = 8
rate = 48000
chunk = 4096
record_len = 5  # in second
filename = 'temp.wav'
devicename = 'USBStreamer: Audio (hw:2,0)'
# Bit depth and max value goes together.
record_format, record_maxvalue, numpy_format = pyaudio.paInt32, 2**(32-1), numpy.int32 #pyaudio.paFloat32, "S32_LE"
p = pyaudio.PyAudio()
idx = None
for i in range(p.get_device_count()):
    if p.get_device_info_by_index(i).get('name') == devicename:
        idx = i
        break
if idx == None:
    raise 'No micarray found.'

def record():
    stream = p.open(format=record_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    output=True,
                    input_device_index=idx,
                    frames_per_buffer=record_len)

    wave_data = numpy.empty((channels,0), dtype=numpy_format)
    for i in range(0, int(rate / chunk * record_len)):
        data = stream.read(chunk, exception_on_overflow = False)
        np_tmp = numpy.frombuffer(data, dtype=numpy_format)
        np_tmp = numpy.reshape(np_tmp, (chunk, channels))
        np_tmp = np_tmp.transpose()
        wave_data = numpy.append(wave_data, np_tmp, axis=1)
    stream.stop_stream()
    stream.close()

    stream2 = p.open(format=record_format,
                    channels=1,
                    rate=rate,
                    output=True,
                    frames_per_buffer=record_len)
    stream2.write(numpy.ndarray.tobytes(wave_data[5]), rate*record_len)

    # # If the temp file is there, delete it.
    # if os.path.exists(filename):
    #     os.remove(filename)
    #
    # # Record an audio file using command line.
    # print("Recording...")
    # os.system("arecord -f {0} -c {1} -r {2} -d {3} {4}"
    #           .format(record_format, channels, rate, record_len, filename)
    #           )
    # # Read in the file.
    # f = wave.open(filename, "rb")
    # params = f.getparams()
    # nchannels, sampwidth, framerate, nframes = params[:4]
    # str_data = f.readframes(nframes)
    #
    # f.close()
    #
    # # Get channels using numpy.
    # wave_data = numpy.fromstring(str_data, dtype=numpy_format)
    # wave_data.shape = -1, channels
    # wave_data = wave_data.T
    #
    return rate, record_maxvalue, wave_data