from __future__ import annotations
from model import *
import numpy as np


class GenerationGA:
    def __init__(self, pop_size, elitism, p, K, iter):
        self.population = None
        self.elitism = elitism
        self.pop_size = pop_size
        self.p = p
        self.K = K
        self.iter = iter
        self.init_population()

    def init_population(self):
        self.population = []
        for i in range(self.pop_size):
            self.population.append(Model(np.random.normal(0, 0.01, size=5)))

    def cross_arithmetic(self, model1, model2):
        return Model((model1.betas + model2.betas) / 2)

    def mutate(self, model, deviation, p):
        mutation = np.random.choice([0, np.random.normal(0, deviation)],
                                    size=len(model.betas),
                                    p=[1 - p, p])
        return Model(model.betas + mutation)

    def fit(self, train_x, train_y, trace=False):
        epoch = 0
        best_error = 1e9

        while epoch < self.iter + 1:
            all_errors = []
            for i in range(len(self.population)):
                error = 0
                for j in range(len(train_x)):
                    error += np.sum(np.square(self.population[i].output(train_x[j]) - train_y[j]))
                error /= len(train_x)
                all_errors.append(error)
            goodness = 1 / np.array(all_errors)

            population_sorted = sorted(zip(goodness, self.population), reverse=True)  # sortiramo populaciju prema 1/E
            goodness = [pair[0] for pair in population_sorted]
            self.population = [pair[1] for pair in population_sorted]

            if trace and best_error > 1 / goodness[0]:
                best_error = 1 / goodness[0]
                print("Nova najbolja jedinka je pronađena: @{}, {}".format(epoch, 1 / goodness[0]))

            if epoch % 200 == 0:
                print("[Train error @" + str(epoch) + "]: " + str(1 / goodness[0]))

            if 1 / goodness[0] <= 1e-7:
                if epoch % 200 != 0:
                    print("[Train error @" + str(epoch) + "]: " + str(1 / goodness[0]))
                print("greška je dovoljno mala, izlazim")
                return

            new_population = []
            for i in range(self.elitism):  # dodaj n najboljih
                new_population.append(self.population[i])

            for i in range(len(self.population) - self.elitism):  # generiraj novu populaciju
                parents = np.random.choice(self.population, size=2, replace=False, p=goodness / np.sum(goodness))
                crossed = self.cross_arithmetic(parents[0], parents[1])  # križaj
                mutated = self.mutate(crossed, self.K, self.p)  # mutiraj
                new_population.append(mutated)

            self.population = new_population

            epoch += 1

    def predict(self, test_x, test_y):
        best_value = None
        for i in range(len(self.population)):
            error = 0
            for j in range(len(test_x)):
                error += np.sum(np.square(self.population[i].output(test_x[j]) - test_y[j]))
            error /= len(test_x)
            if best_value is None or best_value > error:
                best_value = error
        return best_value


train_x, train_y = get_data("zad4_dataset1.txt")
algorithm = GenerationGA(20, 3, 0.1, 0.1, 5000)
algorithm.fit(train_x, train_y, trace=False)
