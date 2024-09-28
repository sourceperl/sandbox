#!/usr/bin/env python3

import numpy as np


class SimpleNeuralNetwork:
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # initialize weights and biases for layers 1 and 2
        self.l1_weights = np.random.randn(input_size, hidden_size)
        self.l1_biases = np.zeros((1, hidden_size))
        self.l2_weights = np.random.randn(hidden_size, output_size)
        self.l2_biases = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def forward_propagation(self, inputs: np.ndarray) -> np.ndarray:
        # layer 1: apply weights and bias to inputs
        self.l1_z = np.dot(inputs, self.l1_weights) + self.l1_biases
        # layer 1: activation
        self.l1_activations = self.sigmoid(self.l1_z)
        # layer 2: apply weights and bias to layer 1 outputs
        self.l2_z = np.dot(self.l1_activations, self.l2_weights) + self.l2_biases
        # layer 2: activation
        self.l2_activations = self.sigmoid(self.l2_z)
        return self.l2_activations

    def backward_propagation(self, inputs: np.ndarray, outputs: np.ndarray, learning_rate: float) -> None:
        # layer 2
        l2_d_z = self.l2_activations - outputs
        l2_d_weights = np.dot(self.l1_activations.T, l2_d_z)
        l2_d_biases = np.sum(l2_d_z, axis=0, keepdims=True)
        # layer 1
        l1_d_z = np.dot(l2_d_z, self.l2_weights.T) * self.sigmoid_derivative(self.l1_z)
        l1_d_weights = np.dot(inputs.T, l1_d_z)
        l1_d_biases = np.sum(l1_d_z, axis=0, keepdims=True)

        # update weights and biases
        self.l1_weights -= learning_rate * l1_d_weights
        self.l1_biases -= learning_rate * l1_d_biases
        self.l2_weights -= learning_rate * l2_d_weights
        self.l2_biases -= learning_rate * l2_d_biases

    def train(self, inputs: np.ndarray, outputs: np.ndarray, epochs: int, learning_rate: float) -> None:
        for epoch in range(epochs):
            output = self.forward_propagation(inputs)
            self.backward_propagation(inputs, outputs, learning_rate)
            loss = np.mean(np.square(output - outputs))
            print(f'epoch {epoch+1:4d}: loss = {round(loss, 6)}')

    def predict(self, inputs: np.ndarray) -> np.ndarray:
        return self.forward_propagation(inputs)


if __name__ == '__main__':
    # create neural network: 2 input neurons, 3 hidden neurons, 1 output neuron
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=3, output_size=1)

    # training (X is network inputs, y is network outputs)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    nn.train(inputs=X, outputs=y, epochs=1_000, learning_rate=0.1)

    # predictions
    print('\n' + '#'*40 + ' predictions ' + '#'*40 + '\n')
    in_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    for inputs, y in zip(in_data, nn.predict(in_data)):
        print(f'{inputs=} -> {y=}')
