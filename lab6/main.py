from __future__ import annotations
from lab4.model import get_data
import matplotlib.pyplot as plt
import numpy as np
from anfis import ANFIS


def original_function(X, y):
    x1 = [point[0] for point in X]
    x2 = [point[1] for point in X]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x1, x2, y, cmap='viridis')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f')
    plt.savefig('img/original_function.png')


def plot_function_error(X, y, n_of_rules, rates, iterations, error):
    for i, learning in enumerate(['stochastic', 'batch']):
        algorithm = ANFIS(n_of_rules, rates[i], iterations * (10 ** i), error, learning)
        algorithm.train(X, y)
        predicted, error_f = algorithm.predict(X, y)

        x1 = [point[0] for point in X]
        x2 = [point[1] for point in X]

        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_trisurf(x1, x2, predicted, cmap='viridis')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('f')

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_trisurf(x1, x2, error_f, cmap='viridis')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_zlabel(r'$\delta$', rotation=0, labelpad=10)

        plt.tight_layout()
        plt.savefig('img/' + learning + '_' + str(n_of_rules) + '.png')
        if n_of_rules == 7:
            algorithm.save_parameters('img/' + learning + "_parameters" + str(n_of_rules) + ".txt")
            algorithm.save_error('img/' + learning + "_error" + str(n_of_rules) + ".txt")


def plot_membership_function():
    with open('img/stochastic_parameters7.txt', 'r') as file:
        for i, line in enumerate(file):
            elements = [float(element) for element in line.strip().split(' ')]
            a, b, c, d = elements[0], elements[1], elements[2], elements[3]
            x = np.linspace(-4, 4, 100)

            def a_membership(x):
                return 1 / (1 + np.exp(b * (x - a)))

            def b_membership(x):
                return 1 / (1 + np.exp(d * (x - c)))

            fig = plt.figure(figsize=(12, 5))
            ax1 = fig.add_subplot(121)
            ax1.plot(x, a_membership(x))
            ax1.set_xlabel('x')
            ax1.set_ylabel(r'$A_1(x)$')
            ax1.set_xlim(-4, 4)
            ax1.set_ylim(0, 1)

            ax2 = fig.add_subplot(122)
            ax2.plot(x, b_membership(x))
            ax2.set_xlabel('x')
            ax2.set_ylabel(r'$B_1(x)$')
            ax2.set_xlim(-4, 4)
            ax2.set_ylim(0, 1)

            plt.tight_layout()
            plt.savefig('img/rule_' + str(i + 1) + '.png')


def plot_loss():
    for learning in ['stochastic', 'batch']:
        with open('img/' + learning + '_error7.txt', 'r') as file:
            values = file.readlines()
            values = [float(_) for _ in values]
            fig = plt.figure(figsize=(7, 5))
            indices = list(range(len(values)))

            plt.plot(indices, values)
            plt.xlabel('Epoha')
            plt.ylabel('Gubitak')
            plt.yscale('log')
            plt.savefig('img/loss_' + learning + '.png')


def plots_loss_etas(X, y, rates):
    for i, learning in enumerate(['stochastic', 'batch']):
        fig = plt.figure(figsize=(7, 5))
        for factor in [0.01, 1, 100]:
            etas = {key: value * factor for key, value in rates[i].items()}
            algorithm = ANFIS(7, etas, 10000, 0.01, learning)
            algorithm.train(X, y)

            indices = list(range(len(algorithm.epoch_error)))
            label = f"eta=({'{:.0e}'.format(etas['a'])}, {'{:.0e}'.format(etas['p'])})"
            plt.plot(indices, algorithm.epoch_error, label=label)
        plt.xlabel('Epoha')
        plt.ylabel('Gubitak')
        plt.yscale('log')
        plt.legend()
        plt.savefig('img/etas_loss_' + learning + '.png')


X, y = get_data('data.txt')
original_function(X, y)

rates = [{
    'a': 1e-3, 'b': 1e-3, 'c': 1e-3, 'd': 1e-3,
    'p': 3 * 1e-4, 'q': 3 * 1e-4, 'r': 3 * 1e-4
}, {
    'a': 1e-4, 'b': 1e-4, 'c': 1e-4, 'd': 1e-4,
    'p': 3 * 1e-5, 'q': 3 * 1e-5, 'r': 3 * 1e-5
}]

#  plot_function_error(X, y, 1, rates, 20000, 0.01)
#  plot_function_error(X, y, 2, rates, 20000, 0.01)
#  plot_function_error(X, y, 7, rates, 20000, 0.01)
#  plot_membership_function()
#  plot_loss()
#  plots_loss_etas(X, y, rates)
