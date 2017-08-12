import matplotlib.animation as anim
import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy

plt_bound = 1
disp_bound = 1.05

ln_o = None
ln_x = None

get_point_function = None
arguments = None


def init():
    global fig1, ln_o, ln_x

    ln_o, = plt.plot([], [], 'ro')
    ln_x, = plt.plot([], [], 'bx')
    plt.xlim(-disp_bound, disp_bound)
    plt.ylim(-disp_bound, disp_bound)
    plt.xlabel('x')
    plt.ylabel('y')
    return ln_o,


def update(*args):
    global get_point_function, arguments, ln_o, ln_x
    x, y = get_point_function(*arguments)
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
    fig1 = plt.figure()
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


def make_fft_graph(fft, corre):
    fft_np = numpy.array(fft).swapaxes(0, 1).swapaxes(1, 2)
    channel_N, freq_N, sample_N = fft_np.shape
    if (channel_N > 6):  # We don't have space for more than 6 channels
        return
    fig, axes = plt.subplots(2, 3)
    fig.subplots_adjust(hspace=0.3, wspace=0.05)
    for ax, mat, i in zip(axes.flat, fft_np, range(1, channel_N + 1)):
        fft_abs = numpy.abs(mat)
        fft_less_row = fft_abs[0::20]
        n = freq_N / 20
        fft_sqr = numpy.repeat(fft_less_row, int(n / sample_N)).reshape([n, n])
        ax.matshow(fft_sqr, cmap='viridis')
        plt.xlabel('time')
        plt.ylabel('freq')
        ax.set_title('Channel {0}'.format(i))
    plt.show()
    print("Plotted.")
