import numpy

def fst_delay_snd(fst, snd, samp_rate):
    # Verify argument shape.
    s1, s2 = fst.shape, snd.shape
    if len(s1) != 1 or len(s2) != 1 or s1[0] != s2[0]:
        raise Exception("Argument shape invalid, in 'fst_delay_snd' function")

    half_len = int(s1[0]/2)
    corre = numpy.correlate(fst, snd, 'same')
    max_pos = numpy.argmax(corre)
    return (max_pos - half_len)/samp_rate