from __future__ import annotations
import numpy as np
from typing import List

def get_data(path):
    train_x, train_y = [], []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.split()
            train_x.append(np.array([float(value) for value in values[:-1]]))
            train_y.append(float(values[-1]))
    train_x = np.array(train_x)
    train_y = np.array(train_y)
    return train_x, train_y


class Model:
    def __init__(self, betas: List[float]):
        self.betas = betas

    def __lt__(self, other):
        return True

    def output(self, train_x):
        x = train_x[0]
        y = train_x[1]
        return np.sin(self.betas[0] + self.betas[1] * x) + self.betas[2] \
               * np.cos(x * (self.betas[3] + y)) * 1 / (1 + np.exp(np.square(x - self.betas[4])))
