import matplotlib.animation as anim
import matplotlib.pyplot as plt

plt_bound = 1

fig1 = plt.figure()
ln_o, = plt.plot([], [], 'ro')
ln_x, = plt.plot([], [], 'bx')

get_point_function = None


def init():
    plt.xlim(-plt_bound, plt_bound)
    plt.ylim(-plt_bound, plt_bound)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('test')
    return ln_o,


def update(*args):
    x, y = get_point_function()
    global ln_o, ln_x
    if -plt_bound < x < plt_bound and -plt_bound < y < plt_bound:
        ln_o.set_data([x], [y])
        ln_x.set_data([], [])
        return ln_o,
    else:
        ln_x.set_data([0], [0])
        ln_o.set_data([], [])
        return ln_x,


def point_animation(point_func):
    global get_point_function
    get_point_function = point_func
    ani = anim.FuncAnimation(fig1, update, init_func=init, blit=True)
    plt.show()
