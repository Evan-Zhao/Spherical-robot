import matplotlib.animation as anim
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy

plt_bound = 1
disp_bound = 1.05

fig1 = plt.figure()
ln_o, = plt.plot([], [], 'ro')
ln_x, = plt.plot([], [], 'bx')

get_point_function = None
arguments = None


def init():
    plt.xlim(-disp_bound, disp_bound)
    plt.ylim(-disp_bound, disp_bound)
    plt.xlabel('x')
    plt.ylabel('y')
    return ln_o,


def update(*args):
    x, y = get_point_function(*arguments)
    global ln_o, ln_x
    if -plt_bound <= x <= plt_bound and -plt_bound <= y <= plt_bound:
        ln_o.set_data([x], [y])
        ln_x.set_data([], [])
        return ln_o,
    else:
        ln_x.set_data([0], [0])
        ln_o.set_data([], [])
        return ln_x,


def point_animation(point_func, *args):
    global get_point_function, arguments
    get_point_function = point_func
    arguments = args
    ani = anim.FuncAnimation(fig1, update, init_func=init, blit=True, repeat_delay=0)
    plt.show()


def plot_channel(audio, sampling):
    channels, nframes = audio.shape[0], audio.shape[1]
    time_range = numpy.arange(0, nframes) * (1.0 / sampling)

    for i in range(1, channels + 1):
        pl.figure(i)
        pl.plot(time_range, audio[i - 1])
        pl.xlabel("time{0}".format(i))

    pl.show()
