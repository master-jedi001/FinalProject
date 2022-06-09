import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numexpr as ne

logger = logging.getLogger('difequation.main')


def func(f, x):
    return ne.evaluate(f)


def set_first_iteration(n, init):
    y = dict()
    for j in range(n):
        y[j] = list()
        y[j].append(float(init[j]))
    return y


def runge_kutta_iteration(x, y, coef, f, n, i, h, b):
    a = {-1: [0] * n, 0: [], 1: [], 2: [], 3: []}
    summa = [0] * 4
    for k in range(4):
        for j in range(n - 1):
            a[k].append(y[j + 1][i] + b[k] * a[k - 1][j + 1])
            summa[k] += func(coef[j], x[i] + b[k]) * (y[j][i] + b[k] * a[k - 1][j])
        summa[k] += func(coef[n - 1], x[i] + b[k]) * (y[n - 1][i] + b[k] * a[k - 1][n - 1])
        a[k].append((func(f, x[i] + b[k]) - summa[k]) / func(coef[n], x[i] + b[k]))
    for j in range(n):
        y[j].append(y[j][i] + h / 6 * (a[0][j] + 2 * a[1][j] + 2 * a[2][j] + a[3][j]))
    return y


def runge_kutta(n, coefficients, f, begin, end, h, init_conditions):
    logger.info('Запущен алгоритм Рунге-Кутты для решения задачи Коши.')
    init = init_conditions.split(', ')
    coef = coefficients.split(', ')
    x = list()
    N = int((end - begin) / h)
    b = [0, h/2, h/2, h]
    y = set_first_iteration(n, init)
    for i in range(N):
        x.append(begin + i*h)
        y = runge_kutta_iteration(x, y, coef, f, n, i, h, b)
    x.append(end)
    return x, y[0]


def solution_plot(x, y, h, id):
    plt.plot(x, y, label=f'Численное решение задачи. h = {h}', color='blue')
    plt.title("Решение задачи Коши")
    plt.ylabel('ось Y')
    plt.xlabel('ось X')
    plt.legend()
    plt.grid()
    logger.info(f'Построен график {id}.jpg.')
    path = f'static/images/{id}.jpg'
    plt.savefig(path)
    logger.info(f'График {id}.jpg сохранен в {path}.')
    return path


def max_error(y_numerical, y_analytical, x):
    max_err = 0
    for i in range(len(x)):
        difference = y_numerical[i] - y_analytical(x[i])
        if max_err < abs(difference):
            max_err = abs(difference)
    return max_err
