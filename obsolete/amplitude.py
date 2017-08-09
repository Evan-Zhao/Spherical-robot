def amp(channels, wave_data, sensor_angles, sensor_pos):
    amplitude = []
    for i in range(0, channels):
        len = wave_data[i].shape[0]
        acc = 0.0
        for d in wave_data[i]:
            acc += d / len * d
        acc = math.sqrt(acc)
        amplitude.append(acc)
        print("Channel {0} amplitude: {1}".format(i, acc))
    idx, _ = max(enumerate(amplitude), key=operator.itemgetter(1))
    print("Angle = {0}".format(
        sensor_angles[idx]
    ))
    return sensor_pos[idx]