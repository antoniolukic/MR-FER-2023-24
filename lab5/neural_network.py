import numpy as np


class Linear:

    def __init__(self, k, l):
        self.k = k
        self.l = l

    def transformation(self, x):
        return [self.k * i + self.l for i in x]

    def derivation(self, x):
        return 1


class Sigmoid:

    def __init__(self, alpha):
        self.alpha = alpha

    def transformation(self, x):
        return 1 / (1 + np.exp(-x))

    def derivation(self, x):
        return x * (1 - x)


class Nnetwork:

    def __init__(self,
                 no_of_in_nodes,
                 hidden_layers,
                 no_of_out_nodes,
                 leaning_rate,
                 transfer_function,
                 derivation_function,
                 max_epoch,
                 loss,
                 algorithm):

        self.layers = [no_of_in_nodes, *hidden_layers, no_of_out_nodes]
        self.learning_rate = leaning_rate
        self.transfer_function = transfer_function
        self.derivation_function = derivation_function
        self.max_epoch = max_epoch
        self.loss = loss
        self.algorithm = algorithm
        self.stop = False
        self.init_weights()

    def init_weights(self):
        var = 1 / self.layers[0]

        self.weights = []
        self.b = []

        for i in range(len(self.layers) - 1):
            self.weights.append(np.random.normal(0, var, (self.layers[i + 1], self.layers[i])))
            self.b.append(np.random.normal(0, var, self.layers[i + 1]))

        self.reset_delta()

    def reset_delta(self):
        self.w_delta = []
        self.b_delta = []

        for i in range(len(self.layers) - 1):
            self.w_delta.append(np.zeros((self.layers[i + 1], self.layers[i])))
            self.b_delta.append(np.zeros((self.layers[i + 1])))

    def permute(self, X, y):
        permuted_indices = np.random.permutation(len(X))
        X = X[permuted_indices, :]
        y = y[permuted_indices, :]
        return X, y

    def permute_mini_batch(self, X, y):
        for i in range(5):  # permutate in group
            indices = np.arange(i * 20, (i + 1) * 20)
            np.random.shuffle(indices)
            X[i * 20: (i + 1) * 20, ] = X[indices, ]
            y[i * 20: (i + 1) * 20, ] = y[indices, ]

        final_indices = []
        for i in range(10):  # extract two from each group
            for j in range(5):
                final_indices.append(j * 20 + i)
                final_indices.append(j * 20 + 1 + i)
        final_indices = np.array(final_indices)
        X = X[final_indices, ]
        y = y[final_indices, ]
        return X, y

    def feed_forward(self, x):
        self.h = [x]

        for i in range(len(self.layers) - 1):
            net = self.weights[i].dot(self.h[i]) + self.b[i]
            self.h.append(self.transfer_function(net))

        return self.h[-1]

    def train(self, X, y):
        if self.algorithm == "Stochastic backpropagation":
            update = 1
        elif self.algorithm == "Mini-batch backpropagation":
            update = 10
        else:
            update = len(X)
        print(update)

        epoch, total_loss = 0, -1 # to generate 1 free pass through the loop
        N = len(X)
        self.epoch_error = []
        org_X, org_y = X, y

        while epoch <= self.max_epoch and (total_loss / N >= self.loss or total_loss == -1) and not self.stop:
            total_loss = 0

            if update == 1:  # stochastic
                X, y = self.permute(org_X, org_y)
            elif update == 10:  # mini-batch
                X, y = self.permute_mini_batch(org_X, org_y)
            else:  # batch
                X, y = org_X, org_y

            for j, x in enumerate(X):
                error = [(self.feed_forward(x) - y[j])]
                total_loss += np.mean(np.square(error[0]))  # error

                error[0] *= self.derivation_function(np.array(self.h[-1]))  # errors are reversed

                for i in range(1, len(self.layers) - 1):  # propagate error
                    error.append(np.transpose(self.weights[-i]).dot(error[i - 1]) *
                                 self.derivation_function(np.array(self.h[-(i + 1)])))

                for i in range(len(self.weights)):  # calculate delta
                    self.w_delta[i] = np.subtract(self.w_delta[i],
                                                  self.learning_rate *
                                                  np.transpose(np.outer(self.h[i], error[-(i + 1)])))

                    self.b_delta[i] = np.subtract(self.b_delta[i],
                                                  self.learning_rate * error[-(i + 1)])

                if j % update >= update - 1:  # adjust the weights when needed and reset delta
                    for i in range(len(self.weights)):
                        self.weights[i] += self.w_delta[i]
                        self.b[i] += self.b_delta[i]
                    self.reset_delta()

            self.epoch_error.append(total_loss / N)
            if epoch % 200 == 0:
                print("Training epoch " + str(epoch) + "/" + str(self.max_epoch) + ":")
                print(self.epoch_error[epoch])
            epoch += 1

        self.stop = False
        print("Gotov s treniranjem!")
