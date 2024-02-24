from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from dataset import Dataset


def task1():
    x = np.linspace(-8, 10, 1001)
    s = [1, 0.25, 4]

    def output(x, s, w=2):
        return 1 / (1 + np.abs(x - w) / np.abs(s))

    fig = plt.figure(figsize=(10, 8))
    for si in s:
        plt.plot(x, output(x, si), label="s = {}".format(si))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('img/task1.png')
    plt.show()


def task2(train_x, train_y):
    fig = plt.figure(figsize=(10, 8))
    class_0 = train_x[(train_y == [1, 0, 0]).all(axis=1)]
    class_1 = train_x[(train_y == [0, 1, 0]).all(axis=1)]
    class_2 = train_x[(train_y == [0, 0, 1]).all(axis=1)]
    for cl, color, label in zip([class_0, class_1, class_2], ['red', 'green', 'blue'],
                                ['Class 0', 'Class 1', 'Class 2']):
        plt.plot(cl[:, 0], cl[:, 1], 'o', label=label, color=color)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('img/task2.png')
    plt.show()


def task4(train_x, train_y, params_file):
    fig = plt.figure(figsize=(10, 8))
    class_0 = train_x[(train_y == [1, 0, 0]).all(axis=1)]
    class_1 = train_x[(train_y == [0, 1, 0]).all(axis=1)]
    class_2 = train_x[(train_y == [0, 0, 1]).all(axis=1)]
    for cl, color, label in zip([class_0, class_1, class_2], ['red', 'green', 'blue'],
                                ['Class 0', 'Class 1', 'Class 2']):
        plt.plot(cl[:, 0], cl[:, 1], 'o', label=label, color=color)

    params = np.loadtxt(params_file)
    first_layer = params[:8 * 2 * 2]
    centroid = first_layer[::2]
    plt.scatter(centroid[::2], centroid[1::2], color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig('img/' + params_file[7:-4] + '.png')
    plt.show()


dataset = Dataset('dataset.txt')
train_x, train_y = dataset.get_all()
task1()
task2(train_x, train_y)
task4(train_x, train_y, 'params_task4.txt')
task4(train_x, train_y, 'params_task5.txt')
task4(train_x, train_y, 'params_task6.txt')
