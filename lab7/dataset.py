from __future__ import annotations
import numpy as np


class Dataset:

    def __init__(self, path):
        train_x, train_y = [], []
        with open(path, 'r') as file:

            lines = file.readlines()
            for line in lines:
                values = line.split()
                train_x.append(np.array([float(value) for value in values[:-3]]))
                train_y.append([float(values[-3]), float(values[-2]), float(values[-1])])

            self.train_x = np.array(train_x)
            self.train_y = np.array(train_y)

    def size(self):
        return len(self.train_y)

    def get(self, index):
        return self.train_x[index], self.train_y[index]

    def get_all(self):
        return self.train_x, self.train_y
