import numpy


def fst_delay_snd(fst, snd, samp_rate):
    # Verify argument shape.
    s1, s2 = fst.shape, snd.shape
    if len(s1) != 1 or len(s2) != 1 or s1[0] != s2[0]:
        raise Exception("Argument shape invalid, in 'fst_delay_snd' function")

    length = s1[0]
    half_len = int(length / 2)
    Xfst = numpy.fft.fft(fst)
    Xsnd = numpy.fft.fft(snd)
    Xsnd_star = numpy.conj(Xsnd)
    Xall = numpy.zeros(length, dtype=numpy.complex64)
    for i in range(0, length):
        Xall[i] = (Xsnd_star[i] * Xfst[i]) / abs(Xsnd_star[i]) / abs(Xfst[i])
    R = numpy.fft.ifft(Xall)
    max_pos = numpy.argmax(R)
    if max_pos > half_len:
        delta = -(length - 1 - max_pos) / samp_rate
    else:
        delta = max_pos / samp_rate
    return delta, R, Xfst, Xsnd
