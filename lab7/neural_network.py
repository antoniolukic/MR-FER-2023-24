from __future__ import annotations
from typing import List
import numpy as np
from dataset import Dataset


class NeuralNetwork:

    def __init__(self, layers):
        self.layers = layers

    def n_of_parameters(self):
        sol = self.layers[1] * self.layers[0] * 2
        for i in range(1, len(self.layers) - 1):
            sol += self.layers[i + 1] * self.layers[i]
            sol += self.layers[i + 1]
        return sol

    def calc_outputs(self, inputs, parameters):
        pointer = 0
        outputs = np.copy(inputs)
        for i in range(1, len(self.layers)):
            curr_layer_outputs = np.zeros(self.layers[i])
            for j in range(len(curr_layer_outputs)):
                if i == 1:
                    curr_layer_outputs[j] = self.type_one(inputs, parameters, pointer)
                    pointer += len(inputs) * 2
                else:
                    curr_layer_outputs[j] = self.type_two(inputs, parameters, pointer, outputs)
                    pointer += len(outputs) + 1
            outputs = curr_layer_outputs
        return outputs

    def type_one(self, inputs, parameters, pointer):
        summ = 0.0
        for x in inputs:
            summ += np.abs(x - parameters[pointer]) / np.abs(parameters[pointer + 1])  # w pa s
            pointer += 2
        return 1 / (1 + summ)

    def type_two(self, inputs, parameters, pointer, outputs):
        net = np.dot(parameters[pointer:pointer + len(outputs)], outputs)  # w * h
        net += parameters[pointer + len(outputs)]  # bias
        return self.sigmoid(net)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def calc_error(self, dataset: Dataset, parameters: List[float]):
        mse = 0
        for i in range(dataset.size()):
            x, y = dataset.get(i)
            mse += np.sum(np.square(y - self.calc_outputs(x, parameters)))
        mse /= dataset.size()
        return mse
