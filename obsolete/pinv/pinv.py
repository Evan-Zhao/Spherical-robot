import numpy.linalg as lin
import numpy as np
import math

# Const area
sound_speed = 340.29


def dist(p, q):
    x1, y1, z1 = p
    x2, y2, z2 = q
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


def metric_square(p):
    x1, y1, z1 = p
    return x1 ** 2 + y1 ** 2 + z1 ** 2


def coeff(distdiff_1, distdiff_i, pos_0, pos_1, pos_i):
    xi, yi, zi = pos_i
    x0, y0, z0 = pos_0
    x1, y1, z1 = pos_1
    coef_x = (2 * xi - 2 * x0) / distdiff_i - (2 * x1 - 2 * x0) / distdiff_1
    coef_y = (2 * yi - 2 * y0) / distdiff_i - (2 * y1 - 2 * y0) / distdiff_1
    coef_z = (2 * zi - 2 * z0) / distdiff_i - (2 * z1 - 2 * z0) / distdiff_1
    return coef_x, coef_y, coef_z


def inhom(distdiff_1, distdiff_i, pos_0, pos_1, pos_i):
    term1 = distdiff_i - distdiff_1
    term2 = (metric_square(pos_0) - metric_square(pos_i)) / distdiff_i
    term3 = (metric_square(pos_0) - metric_square(pos_1)) / distdiff_1
    return term1 + term2 - term3


def tdoa_to_position(time_diff, sensor_pos):
    sensors = len(time_diff)
    if len(time_diff) != len(sensor_pos):
        raise Exception('Channel number mismatch.')

    dist_diff = []
    for x in time_diff:
        dist_diff.append(x * sound_speed)

    inhom_mat = np.mat(np.zeros([sensors - 2, 1]))
    coeff_mat = np.mat(np.zeros([sensors - 2, 3]))
    for i in range(2, sensors):
        args = dist_diff[1], dist_diff[i], \
               sensor_pos[0], sensor_pos[1], sensor_pos[i]
        coeff_mat[i - 2, :] = coeff(*args)
        inhom_mat[i - 2] = -inhom(*args)

    x_sol = lin.pinv(coeff_mat) * inhom_mat
    return x_sol[0, 0], x_sol[1, 0], x_sol[2, 0]

