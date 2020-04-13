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
for i in range(10000):
    # forward propagation
    l1 = sigmoid(np.dot(in_data, synapses))

    # how much did we miss ?
    l1_error = out_data - l1

    # multiply how much we missed by the
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * l1 * (1 - l1)

    # update weights
    synapses += np.dot(in_data.T, l1_delta)

print("Synapses weights: %s" % list(synapses))

print('')
print('Results:')
for i, (x0, x1, x2) in enumerate(in_data):
    syn_sum = x0 * synapses[0] + x1 * synapses[1] + x2 * synapses[2]
    print('%s %s %s = %s\tsyn. sum = %.4f\tprob. True = %.2f %%' % (x0, x1, x2, bool(out_data[i][0]),
                                                                    syn_sum[0], sigmoid(syn_sum) * 100))
