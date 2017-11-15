#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'admin'

from numpy import *

def predict(alpha, beta, x_i):
    return beta * x_i + alpha

def error(alpha, beta, x_i, y_i):
    return y_i - predict(alpha, beta, x_i)

def sum_of_squared_errors(alpha, beta, x, y):
    return sum(error(alpha, beta, x_i, y_i) ** 2 for x_i, y_i in zip(x, y))

def least_squares_fit(x, y):
    beta = correlate(x, y) * std(y) / std(x)
    alpha = mean(y) - beta * mean(x)
    return beta, alpha

if __name__ == '__main__':
    x = [-2, 1, 0, 1, 2]
    y = [99.98, 99.99, 100, 100.01, 100.02]
    print(least_squares_fit(x, y))