from __future__ import annotations
import numpy as np


class Model:

    @staticmethod
    def output(x: float, y: float):
        return ((x - 1) ** 2 + (y + 2) ** 2 - 5 * x * y + 3) * np.cos(x / 5) ** 2


with open('data.txt', 'w') as file:
    for x in range(-4, 5, 1):
        for y in range(-4, 5, 1):
            value = Model.output(x, y)
            file.write(str(x) + ' ' + str(y) + ' ' + str(value) + '\n')
