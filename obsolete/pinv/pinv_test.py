import numpy.linalg as lin
import numpy as np
import random
import math

# Const area
src_actual_pos = (2, 1)  # In meter
error_bound = 0.01
sensors = 10


def dist(p, q):
    x1, y1 = p
    x2, y2 = q
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def metric_square(p):
    x1, y1 = p
    return x1 ** 2 + y1 ** 2


def coeff(distdiff_1, distdiff_i, pos_0, pos_1, pos_i):
    xi, yi = pos_i
    x0, y0 = pos_0
    x1, y1 = pos_1
    coef_x = (2 * xi - 2 * x0) / distdiff_i - (2 * x1 - 2 * x0) / distdiff_1
    coef_y = (2 * yi - 2 * y0) / distdiff_i - (2 * y1 - 2 * y0) / distdiff_1
    return coef_x, coef_y


def inhom(distdiff_1, distdiff_i, pos_0, pos_1, pos_i):
    term1 = distdiff_i - distdiff_1
    term2 = (metric_square(pos_0) - metric_square(pos_i)) / distdiff_i
    term3 = (metric_square(pos_0) - metric_square(pos_1)) / distdiff_1
    return term1 + term2 - term3


def make_data():
    src_poses = [src_actual_pos] * sensors
    for i in range(0, sensors):
        a, b = src_poses[i]
        a += random.uniform(-error_bound, error_bound)
        b += random.uniform(-error_bound, error_bound)
        src_poses[i] = (a, b)

    sensor_poses = [(0, 0)] * sensors
    for i in range(0, sensors):
        arg = 2 * i * math.pi / sensors
        sensor_poses[i] = math.cos(arg), math.sin(arg)

    dist_diff = [0] * sensors
    for i in range(0, sensors):
        dist_diff[i] = dist(sensor_poses[i], src_poses[i]) - dist(sensor_poses[0], src_poses[0])

    #for (i, pos) in zip(range(0, sensors), sensor_poses):
    #    print("Sensor {0} at point {1}".format(i, pos))
    #for (i, pos) in zip(range(0, sensors), src_poses):
    #    print("Sensor {0} detected source at point {1}".format(i, pos))
    #for (i, d) in zip(range(0, sensors), dist_diff):
    #    print("Dist_diff[{0}] = {1}".format(i, d))

    return sensor_poses, dist_diff


def main():
    sensor_poses, dist_diff = make_data()

    inhom_mat = np.mat(np.zeros([sensors - 2, 1]))
    coeff_mat = np.mat(np.zeros([sensors - 2, 2]))
    for i in range(2, sensors):
        args = dist_diff[1], dist_diff[i], \
               sensor_poses[0], sensor_poses[1], sensor_poses[i]
        coeff_mat[i - 2, 0], coeff_mat[i - 2, 1] = coeff(*args)
        inhom_mat[i - 2] = -inhom(*args)

    x_sol = lin.pinv(coeff_mat) * inhom_mat
    x, y = x_sol[0, 0], x_sol[1, 0]
    print("The source is anticipated at ({0}, {1})".format(x, y))

if __name__ == '__main__':
    main()
