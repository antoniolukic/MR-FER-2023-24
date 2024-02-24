from __future__ import annotations
from typing import List
import numpy as np
from neural_network import NeuralNetwork
from dataset import Dataset


class EliminationGA:
    def __init__(self, pop_size, elitism, pm: List[float], t: List[float], iterations,
                 neural_network: NeuralNetwork, sigma, eps=1e-7):
        self.population = None
        self.elitism = elitism
        self.pop_size = pop_size
        self.pm = pm
        self.t = t
        self.iter = iterations
        self.neural_network = neural_network
        self.eps = eps
        self.sigma = sigma
        self.init_population()

    def init_population(self):
        self.population = []
        for i in range(self.pop_size):
            self.population.append(np.random.uniform(-4, 4, size=self.neural_network.n_of_parameters()))

    def uniform_crossover(self, parent1, parent2, probability=0.5):
        child = []
        for gene1, gene2 in zip(parent1, parent2):
            if np.random.rand() < probability:
                child.append(gene1)
            else:
                child.append(gene2)
        return np.array(child)

    def arithmetic_crossover(self, parent1, parent2, alpha=0.5):
        child = []
        for gene1, gene2 in zip(parent1, parent2):
            child.append((1 - alpha) * gene1 + alpha * gene2)
        return np.array(child)

    def two_point_crossover(self, parent1, parent2):
        crossover_points = np.sort(np.random.choice(len(parent1), 2, replace=False))
        child = np.concatenate((np.concatenate((np.array(parent1[:crossover_points[0]]),
                                                np.array(parent2[crossover_points[0]:crossover_points[1]]))),
                                np.array(parent1[crossover_points[1]:])))
        return child

    def mutate1(self, model, deviation, p):
        mutation = np.random.choice([0, np.random.normal(0, deviation)],
                                    size=self.neural_network.n_of_parameters(),
                                    p=[1 - p, p])
        return model + mutation

    def mutate2(self, model, deviation, p):
        mutation_mask = np.random.choice([False, True],
                                         size=self.neural_network.n_of_parameters(),
                                         p=[1 - p, p])
        mutated_model = np.copy(model)
        mutated_model[mutation_mask] = np.random.normal(0, deviation, np.count_nonzero(mutation_mask))

        return mutated_model

    def fit(self, dataset: Dataset, trace=False):
        epoch = 0
        best_error = 1e9

        while epoch < self.iter + 1:
            all_errors = []
            for i in range(len(self.population)):
                error = self.neural_network.calc_error(dataset, self.population[i])
                all_errors.append(error)
            goodness = 1 / np.array(all_errors)
            population_sorted = sorted(zip(goodness, self.population), key=lambda x: x[0], reverse=True)  # sortiramo populaciju prema 1/E
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
                p_index = np.random.choice(len(self.population), size=2, replace=False, p=goodness / np.sum(goodness))
                parents = [self.population[p_index[0]], self.population[p_index[1]]]

                crossover_operator = np.random.choice([self.uniform_crossover, self.arithmetic_crossover, self.two_point_crossover])
                crossed = crossover_operator(parents[0], parents[1])

                random_mutation = np.random.rand() * (self.t[0] + self.t[1] + self.t[2])

                if random_mutation < self.t[0]:
                    mutated = self.mutate1(crossed, self.sigma[0], self.pm[0])
                elif random_mutation < self.t[0] + self.t[1]:
                    mutated = self.mutate1(crossed, self.sigma[1], self.pm[1])
                else:
                    mutated = self.mutate2(crossed, self.sigma[2], self.pm[2])

                new_population.append(mutated)

            self.population = new_population

            epoch += 1

    def save_params(self, dataset: Dataset, path):
        errors = []
        for i in range(len(self.population)):
            errors.append(self.neural_network.calc_error(dataset, self.population[i]))
        pairs = sorted(zip(errors, self.population), key=lambda x: x[0])
        print(pairs[0][0], print(pairs[0][1]))
        with open(path, 'w') as file:
            formatted_list = "\n".join(map(str, pairs[0][1]))
            file.write(formatted_list)

    def evaluate(self, dataset: Dataset, path):
        parameters = np.loadtxt(path)
        train_x, train_y = dataset.get_all()
        wrong = 0
        for i in range(len(train_x)):
            y = self.neural_network.calc_outputs(train_x[i], parameters)
            for j in range(3):
                if y[j] < 0.5:
                    y[j] = 0
                else:
                    y[j] = 1
            wrong += int(np.sum(np.abs(train_y[i] - y)) > 0)
        print(wrong)


dataset = Dataset("dataset.txt")
network = NeuralNetwork([2, 6, 4, 3])
sigma = [0.1, 0.2, 1]
pm = [0.02, 0.02, 0.02]
t = [2, 1, 1]
algorithm = EliminationGA(20, 3, pm, t, 20000, network, sigma, 1e-7)
algorithm.fit(dataset)
algorithm.save_params(dataset, "params_task6.txt")
algorithm.evaluate(dataset, "params_task6.txt")
