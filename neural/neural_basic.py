#!/usr/bin/env python3

import numpy as np


# sigmoid function (return 0.0 to 1.0 for -inf to +inf value)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# input dataset (3 entry neuron)
in_data = np.array([[0, 0, 1],
                    [0, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]])

# output dataset
out_data = np.array([[1],
                     [0],
                     [1],
                     [1]])

# initialize weights with mean 0.0 with n entry (first in_data width)
synapses = np.full((in_data.shape[1], 1), 0.0)

# auto learn loop (fix weights for each synapse)
for _ in range(10_000):
    # forward propagation
    l1 = sigmoid(np.dot(in_data, synapses))

    # how much did we miss ?
    l1_error = out_data - l1

    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * l1 * (1 - l1)

    # update weights
    synapses += np.dot(in_data.T, l1_delta)

print(f'Synapses weights: {list(synapses)}')

print('')
print('Results:')
for (x0, x1, x2), out in zip(in_data, out_data):
    out_as_str = str(bool(out[0]))
    syn_sum = x0 * synapses[0] + x1 * synapses[1] + x2 * synapses[2]
    msg = f'{x0} {x1} {x2} = {out_as_str:<5s}    ' \
          f'syn. sum = {syn_sum[0]:>8.4f}    ' \
          f'prob. True = {sigmoid(syn_sum)[0] * 100:>6.2f} %'
    print(msg)
