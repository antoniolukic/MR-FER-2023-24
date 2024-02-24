from __future__ import annotations
import numpy as np


class Rule:
    def __init__(self):
        self.a, self.b, \
        self.c, self.d, \
        self.p, self.q, self.r = [np.random.uniform(-1, 1) for _ in range(7)]


class ANFIS:
    def __init__(self, n_of_rules, learning_rate, max_epoch, loss, algorithm):
        self.learning_rate = learning_rate
        self.max_epoch = max_epoch
        self.loss = loss
        self.algorithm = algorithm

        self.rules = []
        for i in range(n_of_rules):
            self.rules.append(Rule())
        self.reset_delta()

    def reset_delta(self):
        self.a_delta, self.b_delta, \
        self.c_delta, self.d_delta, \
        self.p_delta, self.q_delta, self.r_delta = [np.zeros(len(self.rules)) for _ in range(7)]

    def permute(self, X, y):
        permuted_indices = np.random.permutation(len(X))
        X = X[permuted_indices, :]
        y = y[permuted_indices]
        return X, y

    def feed_forward(self, x):
        numerator, denominator = 0, 0
        self.alfas, self.betas, self.pis, self.zs = [], [], [], []
        for rule in self.rules:
            self.alfas.append(1 / (1 + np.exp(rule.b * (x[0] - rule.a))))
            self.betas.append(1 / (1 + np.exp(rule.d * (x[1] - rule.c))))
            self.pis.append(self.alfas[-1] * self.betas[-1])
            self.zs.append(rule.p * x[0] + rule.q * x[1] + rule.r)

            numerator += self.pis[-1] * self.zs[-1]
            denominator += self.pis[-1]

        self.alfas, self.betas, self.pis, self.zs = np.array(self.alfas), np.array(self.betas), np.array(self.pis), np.array(self.zs)
        output = numerator / denominator
        return output

    def train(self, X, y):
        if self.algorithm == "stochastic":
            update = 1
        else:
            update = len(X)

        epoch, total_loss = 0, -1  # to generate 1 free pass through the loop
        N = len(X)
        self.epoch_error = []
        org_X, org_y = X, y

        while epoch <= self.max_epoch and (total_loss / N >= self.loss or total_loss == -1):
            total_loss = 0

            if update == 1:  # stochastic
                X, y = self.permute(org_X, org_y)
            else:  # batch
                X, y = org_X, org_y

            for j, x in enumerate(X):
                error = y[j] - self.feed_forward(x)
                total_loss += 1 / 2 * np.square(error)

                for i in range(len(self.rules)):
                    common_abcd = error * np.sum(self.pis * (self.zs[i] - self.zs)) / np.sum(np.square(self.pis)) * self.betas[i] * self.alfas[i]

                    self.a_delta[i] += common_abcd * (1 - self.alfas[i]) * self.rules[i].b
                    self.b_delta[i] += common_abcd * (1 - self.alfas[i]) * (self.rules[i].a - X[j][0])
                    self.c_delta[i] += common_abcd * (1 - self.betas[i]) * self.rules[i].d
                    self.d_delta[i] += common_abcd * (1 - self.betas[i]) * (self.rules[i].c - X[j][1])

                    common_pqr = error * self.pis[i] / np.sum(self.pis)

                    self.p_delta[i] += common_pqr * X[j][0]
                    self.q_delta[i] += common_pqr * X[j][1]
                    self.r_delta[i] += common_pqr

                if j % update >= update - 1:  # adjust the weights when needed and reset delta
                    for i in range(len(self.rules)):
                        self.rules[i].a += self.learning_rate['a'] * self.a_delta[i]
                        self.rules[i].b += self.learning_rate['b'] * self.b_delta[i]
                        self.rules[i].c += self.learning_rate['c'] * self.c_delta[i]
                        self.rules[i].d += self.learning_rate['d'] * self.d_delta[i]
                        self.rules[i].p += self.learning_rate['p'] * self.p_delta[i]
                        self.rules[i].q += self.learning_rate['q'] * self.q_delta[i]
                        self.rules[i].r += self.learning_rate['r'] * self.r_delta[i]
                    self.reset_delta()

            self.epoch_error.append(total_loss / N)
            if epoch % 200 == 0:
                print("Training epoch " + str(epoch) + "/" + str(self.max_epoch) + ":")
                print(self.epoch_error[epoch])
            epoch += 1

        print("Gotov s treniranjem!")

    def predict(self, X, y):
        predicted, error = [], []
        for i, x in enumerate(X):
            value = self.feed_forward(x)
            predicted.append(value)
            error.append(y[i] - value)
        return predicted, error

    def save_parameters(self, name):
        with open(name, 'w') as file:
            for rule in self.rules:
                file.write(str(rule.a) + ' ' + str(rule.b) + ' ' + str(rule.c) + ' ' + str(rule.d) + ' ' +
                           str(rule.p) + ' ' + str(rule.q) + ' ' + str(rule.r) + '\n')

    def save_error(self, name):
        with open(name, 'w') as file:
            for error in self.epoch_error:
                file.write(str(error) + '\n')
