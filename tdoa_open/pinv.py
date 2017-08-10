import math

import numpy as np
import numpy.linalg as lin

# Const area
sound_speed = 340.29


def dist(p, q):
    x1, y1, z1 = p
    x2, y2, z2 = q
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def metric_square(p):
    x1, y1, z1 = p
    return x1 ** 2 + y1 ** 2 + z1 ** 2


def diff(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return x1 - x2, y1 - y2, z1 - z2


def normalize(v):
    x1 = v[0, 0]
    y1 = v[1, 0]
    z1 = v[2, 0]
    if x1 == 0 and y1 == 0 and z1 == 0:
        return 0, 0, 0
    else:
        norm = math.sqrt(x1 * x1 + y1 * y1 + z1 * z1)
        return x1 / norm, y1 / norm, z1 / norm


def tdoa_to_position(time_diff, sensor_pos):
    sensors = len(time_diff)
    if len(time_diff) != len(sensor_pos):
        raise Exception('Channel number mismatch.')

    inhom_mat = np.mat(np.zeros([sensors - 1, 1]))
    coeff_mat = np.mat(np.zeros([sensors - 1, 3]))
    for i in range(1, sensors):
        coeff_mat[i - 1, :] = diff(sensor_pos[i], sensor_pos[0])
        inhom_mat[i - 1] = time_diff[i] * sound_speed

    angle_vec = lin.pinv(coeff_mat) * inhom_mat

    return normalize(angle_vec)
