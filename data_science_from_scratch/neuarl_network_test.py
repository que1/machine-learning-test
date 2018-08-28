#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np

def setp_function(x):
    return 1 if x >= 0 else 0

def perceptron_output(weights, bias, x):
    calculation = np.dot(weights, x) + bias
    return setp_function(calculation)

if __name__ == '__main__':
    print(perceptron_output([2, 2], -3, 1))